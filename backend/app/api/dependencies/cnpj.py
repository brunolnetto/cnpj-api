from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from backend.app.database.base import get_session
from backend.app.api.repositories.cnpj import CNPJRepository
from backend.app.setup.config import settings

# Define a dependency to create a CNPJRepository instance
async def get_cnpj_repository():
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
