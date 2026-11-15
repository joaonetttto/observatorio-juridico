import os
import time
from datetime import datetime

import psycopg
import requests
from dotenv import load_dotenv

load_dotenv()

TRIBUNAL = "tjdft"
QUANTIDADE = 50
TENTATIVAS = 6
ESPERA_SEGUNDOS = 15

URL = f"https://api-publica.datajud.cnj.jus.br/api_publica_{TRIBUNAL}/_search"
CABECALHOS = {
    "Authorization": f"APIKey {os.getenv('DATAJUD_API_KEY')}",
    "Content-Type": "application/json",
}
CORPO = {
    "size": QUANTIDADE,
    "track_total_hits": False,
    "query": {"match": {"assuntos.codigo": 14206}},
}


def buscar_processos():
    for tentativa in range(1, TENTATIVAS + 1):
        try:
            resposta = requests.post(URL, headers=CABECALHOS, json=CORPO, timeout=180)
            if resposta.status_code == 200:
                return [item["_source"] for item in resposta.json()["hits"]["hits"]]
            print(f"Tentativa {tentativa}/{TENTATIVAS}: status {resposta.status_code}")
        except requests.exceptions.RequestException as erro:
            print(f"Tentativa {tentativa}/{TENTATIVAS}: {type(erro).__name__}")
        if tentativa < TENTATIVAS:
            time.sleep(ESPERA_SEGUNDOS)
    return None


def conectar_banco():
    return psycopg.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )


def converter_data(texto):
    if not texto:
        return None
    return datetime.strptime(texto, "%Y%m%d%H%M%S")


def gravar_processo(cursor, processo):
    cursor.execute("SELECT id FROM tribunal WHERE sigla = %s", (processo["tribunal"],))
    linha = cursor.fetchone()
    if linha is None:
        print("Tribunal não cadastrado:", processo["tribunal"])
        return False
    tribunal_id = linha[0]

    cursor.execute(
        """
        INSERT INTO processo (numero_cnj, tribunal_id, classe, data_ajuizamento, grau, orgao_julgador)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (numero_cnj, grau) DO UPDATE
            SET classe = EXCLUDED.classe, orgao_julgador = EXCLUDED.orgao_julgador
        RETURNING id
        """,
        (
            processo["numeroProcesso"],
            tribunal_id,
            processo.get("classe", {}).get("nome"),
            converter_data(processo.get("dataAjuizamento")),
            processo.get("grau"),
            processo.get("orgaoJulgador", {}).get("nome"),
        ),
    )
    processo_id = cursor.fetchone()[0]

    for assunto in processo.get("assuntos", []):
        nome = assunto.get("nome")
        nome = nome.strip() if nome else None
        cursor.execute(
            """
            INSERT INTO assunto (codigo, nome) VALUES (%s, %s)
            ON CONFLICT (codigo) DO UPDATE
                SET nome = COALESCE(EXCLUDED.nome, assunto.nome)
            """,
            (assunto["codigo"], nome),
        )
        cursor.execute(
            """
            INSERT INTO processo_assunto (processo_id, assunto_codigo) VALUES (%s, %s)
            ON CONFLICT DO NOTHING
            """,
            (processo_id, assunto["codigo"]),
        )
    return True


processos = buscar_processos()
if processos is None:
    raise SystemExit("A API não respondeu depois de várias tentativas. Tente mais tarde.")

print(f"Recebidos da API: {len(processos)} processos")

gravados = 0
with conectar_banco() as conexao:
    with conexao.cursor() as cursor:
        for processo in processos:
            if gravar_processo(cursor, processo):
                gravados += 1

print(f"Gravados no banco: {gravados} processos")