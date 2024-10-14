from typing import Generator, Any
from contextlib import asynccontextmanager

from fastapi import Depends

from backend.app.database.base import get_session
from backend.app.api.repositories.cnpj import CNPJRepository
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


CNPJRepositoryDependency = Depends(get_cnpj_repository)
