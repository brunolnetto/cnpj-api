# API para consulta de CNPJ

Esta aplicação depende da base de dados da receita federal de CNPJs. O autor desta API utiliza scrapper em repositório [1]. 

Veja arquivo `Makefile` para aprender como: 

- Testar;
- Gerar ambiente virtual;
- Instalar dependencias;
- Rodar aplicação localmente;

Atualmente, esta aplicação acessa instância de banco de dados não dockerizada, como local ou hospedada na nuvem. 

Nota: Esta aplicação considera ambiente Unix (Linux ou MacOS).

[1] https://github.com/brunolnetto/scrapper-rf-cnpj

## Autenticação

A API usa credenciais de cliente trocadas por um JWT.

1. Crie um cliente (o segredo é exibido uma única vez; só o hash fica no banco de auditoria):

   ```bash
   python -m backend.app.cli.clients create "Nome do cliente"
   ```

2. Troque as credenciais por um token:

   ```bash
   curl -X POST http://localhost:8000/api/token \
     -H "Content-Type: application/json" \
     -d '{"client_id": "cli_...", "client_secret": "..."}'
   ```

3. Envie o token nas requisições: `Authorization: Bearer <access_token>`.

Para revogar o acesso, use `python -m backend.app.cli.clients deactivate <client_id>`. A revogação vale em até 60 segundos, inclusive para tokens já emitidos. `list` e `activate` também estão disponíveis.
