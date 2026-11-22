import os

import psycopg
from dotenv import load_dotenv
from fastapi import FastAPI, Query
from psycopg.rows import dict_row
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI(title="Observatório Jurídico")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

def consultar(sql, parametros=None):
    with psycopg.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        row_factory=dict_row,
    ) as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(sql, parametros)
            return cursor.fetchall()


@app.get("/saude")
def saude():
    return {"status": "ok"}


@app.get("/tribunais")
def processos_por_tribunal():
    return consultar(
        """
        SELECT t.sigla, COUNT(*) AS processos
        FROM processo p
        JOIN tribunal t ON t.id = p.tribunal_id
        GROUP BY t.sigla
        ORDER BY processos DESC
        """
    )


@app.get("/processos-por-ano")
def processos_por_ano():
    return consultar(
        """
        SELECT EXTRACT(YEAR FROM data_ajuizamento)::int AS ano, COUNT(*) AS quantidade
        FROM processo
        WHERE data_ajuizamento IS NOT NULL
        GROUP BY ano
        ORDER BY ano
        """
    )


@app.get("/assuntos-relacionados")
def assuntos_relacionados(limite: int = Query(10, ge=1, le=50)):
    return consultar(
        """
        SELECT COALESCE(a.nome, 'sem nome (código ' || a.codigo || ')') AS assunto,
               COUNT(*) AS quantidade
        FROM processo_assunto pa
        JOIN assunto a ON a.codigo = pa.assunto_codigo
        WHERE a.codigo <> 14206
        GROUP BY a.codigo, a.nome
        ORDER BY quantidade DESC
        LIMIT %s
        """,
        (limite,),
    )


@app.get("/classes")
def classes(limite: int = Query(10, ge=1, le=50)):
    return consultar(
        """
        SELECT classe, COUNT(*) AS quantidade
        FROM processo
        GROUP BY classe
        ORDER BY quantidade DESC
        LIMIT %s
        """,
        (limite,),
    )
    
@app.get("/coletas")
def coletas():
    return consultar(
        """
        SELECT DISTINCT ON (t.sigla)
               t.sigla,
               c.status,
               c.qtd_processos,
               (SELECT COUNT(*) FROM processo p WHERE p.tribunal_id = t.id) AS no_banco,
               to_char(c.iniciada_em, 'DD/MM/YYYY HH24:MI') AS iniciada_em
        FROM coleta c
        JOIN tribunal t ON t.id = c.tribunal_id
        ORDER BY t.sigla, c.iniciada_em DESC
        """
    )
    
@app.get("/acordaos-por-ano")
def acordaos_por_ano():
    return consultar(
        """
        SELECT EXTRACT(YEAR FROM data_decisao)::int AS ano, COUNT(*) AS quantidade
        FROM acordao
        WHERE relacao_lgpd = 'cita_lgpd' AND data_decisao IS NOT NULL
        GROUP BY ano
        ORDER BY ano
        """
    )


@app.get("/acordaos-recentes")
def acordaos_recentes():
    return consultar(
        """
        SELECT id_stj,
               orgao_julgador,
               classe,
               to_char(data_decisao, 'DD/MM/YYYY') AS data,
               left(regexp_replace(ementa, '\\s+', ' ', 'g'), 450) AS ementa
        FROM acordao
        WHERE relacao_lgpd = 'cita_lgpd'
        ORDER BY data_decisao DESC
        LIMIT 5
        """
    )