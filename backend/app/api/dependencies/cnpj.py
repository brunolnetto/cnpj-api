from typing import Iterator

from fastapi import Depends

from backend.app.database.base import get_session
from backend.app.api.repositories.cnpj import CNPJRepository
from backend.app.setup.logging import logger
from backend.app.setup.config import settings

# Define a dependency to create a CNPJRepository instance


def get_cnpj_repository() -> Iterator[CNPJRepository]:
    """
    Yield a CNPJRepository bound to a session that lives for the whole request.

    The session is rolled back on error and closed when the request finishes.
    """
    with get_session(settings.POSTGRES_DBNAME_RFB) as session:
        yield CNPJRepository(session)


def initialize_CNPJRepository():
    try:
        with get_session(settings.POSTGRES_DBNAME_RFB) as session:
            CNPJRepository.initialize_on_startup(session)

        logger.info("CNPJ measure dictionaries initialized!")

    except Exception as e:
        logger.error(f"Error initializing CNPJ measure tables: {e}")
        raise e


CNPJRepositoryDependency = Depends(get_cnpj_repository)
