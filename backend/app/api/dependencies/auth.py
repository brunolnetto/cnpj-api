from threading import Lock
from time import monotonic
from typing import Callable, Dict, Tuple

from fastapi import Depends
from fastapi.concurrency import run_in_threadpool
from fastapi.requests import Request
from fastapi.security import HTTPBearer
from jose import ExpiredSignatureError, JWTError, jwt

from backend.app.api.repositories.auth import ApiClientRepository
from backend.app.database.base import get_session
from backend.app.exceptions import (
    ExpiredTokenException,
    InvalidTokenException,
    MissingTokenException,
)
from backend.app.setup.config import settings

JWT_SECRET_KEY = settings.JWT_SECRET_KEY
JWT_ALGORITHM = settings.JWT_ALGORITHM

# How long a client's active status is trusted before checking the database
# again. Deactivating a client takes effect within this window.
CLIENT_STATUS_TTL_SECONDS = 60


def _is_client_active_in_database(client_id: str) -> bool:
    with get_session(settings.POSTGRES_DBNAME_AUDIT) as session:
        return ApiClientRepository(session).is_active(client_id)


class ClientStatusCache:
    """Caches whether a client is active, so requests don't each hit the database."""

    def __init__(
        self,
        lookup: Callable[[str], bool] = _is_client_active_in_database,
        ttl_seconds: float = CLIENT_STATUS_TTL_SECONDS,
    ):
        self.lookup = lookup
        self.ttl_seconds = ttl_seconds
        self._entries: Dict[str, Tuple[bool, float]] = {}
        self._lock = Lock()

    def is_active(self, client_id: str) -> bool:
        now = monotonic()

        with self._lock:
            entry = self._entries.get(client_id)
            if entry is not None and entry[1] > now:
                return entry[0]

        is_active = self.lookup(client_id)

        with self._lock:
            self._entries[client_id] = (is_active, now + self.ttl_seconds)

        return is_active

    def clear(self) -> None:
        with self._lock:
            self._entries.clear()


client_status_cache = ClientStatusCache()


class JWTBearer(HTTPBearer):
    """Validates the bearer JWT and that it belongs to an active API client."""

    def __init__(self, status_cache: ClientStatusCache = client_status_cache):
        super().__init__(
            auto_error=False,
            description="Token obtained from POST /token with client credentials.",
        )
        self.status_cache = status_cache

    async def __call__(self, request: Request):
        authorization = request.headers.get("Authorization", "")

        try:
            scheme, token = authorization.split()
        except ValueError:
            raise MissingTokenException()

        if scheme.lower() != "bearer":
            raise MissingTokenException()

        try:
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        except ExpiredSignatureError as e:
            raise ExpiredTokenException() from e
        except JWTError as e:
            raise InvalidTokenException() from e

        client_id = payload.get("sub")
        if not client_id:
            # Tokens issued before client credentials existed carry no subject
            raise InvalidTokenException()

        is_active = await run_in_threadpool(self.status_cache.is_active, client_id)
        if not is_active:
            raise InvalidTokenException()

        return payload


jwt_bearer = JWTBearer()

JWTDependency = Depends(jwt_bearer)
