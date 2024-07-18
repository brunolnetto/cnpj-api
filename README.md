# cnpj-api

Esta aplicação depende da base de dados da receita federal de CNPJs. O autor desta API utiliza scrapper em repositório [1]. 

Veja arquivo `Makefile` para aprender como: 

- Testar;
- Gerar ambiente virtual;
- Instalar dependencias;
- Rodar aplicação localmente;

Atualmente, esta aplicação acessa instância de banco de dados não dockerizada, como local ou hospedada na nuvem. 

Nota: Esta aplicação considera ambiente Unix (Linux ou MacOS).

[1] https://github.com/brunolnetto/scrapper-rf-cnpj
