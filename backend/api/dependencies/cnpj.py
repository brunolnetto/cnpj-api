from fastapi import Depends

from backend.database.base import Database, get_db
from backend.repositories.cnpj import CNPJRepository

# Define a dependency to create a CNPJRepository instance
async def get_cnpj_repository(db: Database = Depends(get_db)):
    return CNPJRepository(db.uri)

CNPJRepositoryDependency = Depends(get_cnpj_repository)