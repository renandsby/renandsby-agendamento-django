# Backend do Projeto Jornada - SEJUS/DF

Sistema de Backend do **Projeto Jornada** desenvolvido pela Sejus-DF

## Rodando o projeto

Os passos para rodar o sistema são:
1. Clone o projeto
2. Crie um arquivo com as variáveis de ambiente de nome `.env` utilizando o exemplo `.env.example` 
4. Rode o comando: `make setup`

## Explicando os comandos

- `make setup`: Faz a build do projeto. Se já existir, vai apagar os containers com todos os dados e recriar
- `make start`: Roda os containers
- `make logs`: Roda os containers e mostra os logs em tempo real
- `make restart`: Reinicia os containers
- `make stop`: Para os containers
- `make dump <app>`: Faz o dump das fixtures do app
- `make migrations`: Checa as alterações estruturais no código e gera as migrations
- `make migrate`: Aplica as migrations, fazendo as alterações no Banco de Dados
- `make app <nome>`: Cria um novo app (já cria e coloca na pasta correta)
- `make module <nome>`: Cria um novo modulo (já cria e coloca na pasta correta)
- `make populate`: Popula o banco de dados a partir das fixtures
# renandsby-agendamento-django
