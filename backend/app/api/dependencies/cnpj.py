from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.database.base import get_session
from backend.app.repositories.cnpj import CNPJRepository


# Define a dependency to create a CNPJRepository instance
async def get_cnpj_repository(session: AsyncSession = Depends(get_session)):
    """
    Create a CNPJRepository instance.

    Args:
        db (Database): Database instance

    Returns:
        CNPJRepository: CNPJRepository instance
    """
    return CNPJRepository(session)


CNPJRepositoryDependency = Depends(get_cnpj_repository)
