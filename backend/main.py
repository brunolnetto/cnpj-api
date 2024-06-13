import json
import time
from collections import Counter

from repositories.cnpj import CNPJRepository
from api.models.cnpj import CNPJ
from database.base import Database, get_db_uri

# Example of a CNPJ to be searched
cnpj_basico='9236040'
cnpj_ordem='1' 
cnpj_dv='1'
cnae_exemplo='6202300'

cnpj=CNPJ(cnpj_basico, cnpj_ordem, cnpj_dv)

t0 = time.perf_counter()

# Folders and database setup
uri = get_db_uri()
cnpj_repository=CNPJRepository(uri)

print(cnpj_repository.get_cnpjs())
print(cnpj_repository.get_cnae_description(cnae_exemplo))
print(cnpj_repository.get_establishment(cnpj))
print(cnpj_repository.get_company(cnpj))
print(cnpj_repository.get_partners(cnpj))
print(cnpj_repository.get_activities(cnpj))
print(cnpj_repository.get_cnpj_info(cnpj))

cnpjs=cnpj_repository.get_cnpjs(limit=100)
cnpjs_obj = [
    CNPJ(
        row['cnpj_basico'],
        row['cnpj_ordem'],
        row['cnpj_dv']
    )
    for index, row in cnpjs.iterrows()
]

validations=[
    cnpj_obj.is_valid_dict()['is_valid']
    for cnpj_obj in cnpjs_obj
]

print(Counter(validations))

len_validation=len(validations)

t1 = time.perf_counter()

print(f"Tempo: {t1-t0} segundos.")

if __name__ == "__main__":
    print("Executando main.py")
    # print(cnpj_repository.get_cnpj_info(cnpj))

# print(cnpj_repository.get_establishments_with_cnae(cnae_exemplo))