from sqlalchemy import Column, Integer, String

from backend.app.database.base import multi_database
from backend.app.setup.config import settings

cnpj_database = multi_database.databases[settings.POSTGRES_DBNAME_RFB]


class CNAE(cnpj_database.base):
    __tablename__ = "cnae"
    codigo = Column(Integer, primary_key=True, index=True)
    descricao = Column(String)
