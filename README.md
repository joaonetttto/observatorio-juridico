# Observatório Jurídico

Pipeline de dados que coleta, organiza e analisa processos judiciais brasileiros sobre **proteção de dados pessoais (LGPD)**, usando a API pública do DataJud (CNJ).
![Dashboard do Observatório Jurídico](docs/dashboard.png)

> Projeto de portfólio em desenvolvimento, feito para praticar engenharia de dados, bancos de dados e arquitetura de software.

## O que já funciona

- Banco PostgreSQL rodando em Docker, com tabelas de tribunais, processos, assuntos e decisões
- Script em Python que busca processos na API do DataJud (assunto "Proteção de Dados Pessoais"), com paginação, novas tentativas e tratamento de erros
- Gravação dos dados no banco sem duplicar registros
- Consultas SQL de análise (`banco/analises.sql`)

## Stack

PostgreSQL · Docker Compose · Python (requests, psycopg) · SQL

## Primeiras observações

Na amostra coletada (439 processos de 6 tribunais estaduais, em novembro de 2026):

- A quantidade de processos por ano de ajuizamento cresce de 2021 a 2026
- Os assuntos que mais acompanham "Proteção de Dados Pessoais" são Direito de Imagem, Dano Moral e Privacidade
- A maioria dos casos é cível de primeira instância

## Limitações

- A API pública do DataJud é instável (erros 429 e 504) e às vezes devolve resultados parciais, então os dados são uma **amostra** e não o total de processos
- A API entrega apenas metadados, sem o texto das decisões
- Alguns tribunais retornaram poucos ou nenhum processo com esse assunto

## Como rodar

1. Clone o repositório e crie o ambiente: `python -m venv .venv` e `pip install -r requirements.txt`
2. Copie `.env.example` para `.env` e preencha (a chave pública do DataJud está na wiki do CNJ)
3. Suba o banco: `docker compose up -d`
4. Execute os arquivos da pasta `banco` em ordem (01 a 04)
5. Rode a coleta: `python src/carregar_processos.py`

## Próximos passos

- API (FastAPI) e dashboard em Next.js
- Tabela de controle das coletas
- Textos de decisões a partir de outra fonte
- Classificação por tema e busca