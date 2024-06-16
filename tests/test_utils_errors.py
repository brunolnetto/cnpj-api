from backend.utils.errors import error_message


def test_error_message():
    """Tests the error_message function."""

    cnpj = "12345678901234"
    nome_tabela = "tabela_teste"

    message = (
        "Nenhum registro encontrado para CNPJ 12345678901234 na tabela tabela_teste."
    )
    assert error_message(cnpj, nome_tabela) == message
