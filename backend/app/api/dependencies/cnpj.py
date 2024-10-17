from fastapi import Depends

from backend.app.database.base import get_session
from backend.app.api.repositories.cnpj import CNPJRepository
from backend.app.setup.logging import logger
from backend.app.setup.config import settings

# Define a dependency to create a CNPJRepository instance


def get_cnpj_repository() -> CNPJRepository:
    """
    Create a CNPJRepository instance.

    Args:
        db (Database): Database instance

    Returns:
        CNPJRepository: CNPJRepository instance
    """
    with get_session(settings.POSTGRES_DBNAME_RFB) as session:
        return CNPJRepository(session)


def initialize_CNPJRepository_on_startup():
    try:
        with get_session(settings.POSTGRES_DBNAME_RFB) as session:
            CNPJRepository.initialize_on_startup(session)

        logger.info("CNPJ measure dictionaries initialized!")

    except Exception as e:
        logger.error(f"Error initializing CNPJ measure tables: {e}")
        raise e


CNPJRepositoryDependency = Depends(get_cnpj_repository)
