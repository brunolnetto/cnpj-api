from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from backend.app.database.base import get_session
from backend.app.api.repositories.cnpj import CNPJRepository
from backend.app.setup.config import settings

CNPJSessionDependency=Annotated[
    AsyncSession, Depends(lambda: get_session(settings.POSTGRES_DBNAME_RFB))
]

# Define a dependency to create a CNPJRepository instance
async def get_cnpj_repository(session: CNPJSessionDependency):
    """
    Create a CNPJRepository instance.

    Args:
        db (Database): Database instance

    Returns:
        CNPJRepository: CNPJRepository instance
    """
    return CNPJRepository(session)


CNPJRepositoryDependency = Depends(get_cnpj_repository)
