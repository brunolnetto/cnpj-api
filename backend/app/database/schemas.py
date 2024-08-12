from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class CNAE(Base):
    __tablename__ = 'cnae'
    codigo = Column(Integer, primary_key=True, index=True)
    descricao = Column(String)
