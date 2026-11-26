from typing import List, Optional, Tuple

from sqlalchemy.orm import Session

from backend.app.database.models.auth import ApiClient
from backend.app.utils.security import (
    generate_client_credentials,
    hash_client_secret,
    verify_client_secret,
)


class ApiClientRepository:
    """Stores API clients. Only the hash of each client secret is persisted."""

    def __init__(self, session: Session):
        self.session = session

    def get_by_client_id(self, client_id: str) -> Optional[ApiClient]:
        return (
            self.session.query(ApiClient)
            .filter(ApiClient.apcl_client_id == client_id)
            .one_or_none()
        )

    def list(self) -> List[ApiClient]:
        return self.session.query(ApiClient).order_by(ApiClient.apcl_created_at).all()

    def create(self, name: str) -> Tuple[ApiClient, str]:
        """Create a client and return it together with its plain-text secret."""
        client_id, client_secret = generate_client_credentials()

        client = ApiClient(
            apcl_client_id=client_id,
            apcl_name=name,
            apcl_secret_hash=hash_client_secret(client_secret),
            apcl_is_active=True,
        )
        self.session.add(client)
        self.session.commit()
        self.session.refresh(client)

        return client, client_secret

    def set_active(self, client_id: str, is_active: bool) -> bool:
        """Activate or deactivate a client. Returns False if it does not exist."""
        client = self.get_by_client_id(client_id)
        if client is None:
            return False

        client.apcl_is_active = is_active
        self.session.commit()

        return True

    def authenticate(self, client_id: str, client_secret: str) -> Optional[ApiClient]:
        """Return the client if the credentials match an active client."""
        client = self.get_by_client_id(client_id)

        if client is None or not client.apcl_is_active:
            return None

        if not verify_client_secret(client_secret, client.apcl_secret_hash):
            return None

        return client

    def is_active(self, client_id: str) -> bool:
        client = self.get_by_client_id(client_id)

        return client is not None and client.apcl_is_active
