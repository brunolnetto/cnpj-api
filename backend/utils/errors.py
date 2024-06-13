from backend.repositories.cnpj import CNPJ

def error_message(cnpj: CNPJ, nome_tabela):
    return f"Nenhum registro encontrado para CNPJ {cnpj} na tabela {nome_tabela}."
