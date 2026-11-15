import os
import time
from datetime import datetime

import psycopg
import requests
from dotenv import load_dotenv

load_dotenv()

TRIBUNAIS = {
    "TJDFT": "Tribunal de Justiça do Distrito Federal e dos Territórios",
    "TJAC": "Tribunal de Justiça do Acre",
    "TJRR": "Tribunal de Justiça de Roraima",
    "TJAP": "Tribunal de Justiça do Amapá",
    "TJTO": "Tribunal de Justiça do Tocantins",
    "TJRO": "Tribunal de Justiça de Rondônia",
    "TJMS": "Tribunal de Justiça de Mato Grosso do Sul",
}

CODIGO_ASSUNTO = 14206
TAMANHO_PAGINA = 100
MAX_PAGINAS = 50
TENTATIVAS = 4
ESPERA_SEGUNDOS = 15

CABECALHOS = {
    "Authorization": f"APIKey {os.getenv('DATAJUD_API_KEY')}",
    "Content-Type": "application/json",
}


def buscar_pagina(sigla, search_after):
    url = f"https://api-publica.datajud.cnj.jus.br/api_publica_{sigla.lower()}/_search"
    corpo = {
        "size": TAMANHO_PAGINA,
        "track_total_hits": False,
        "query": {"match": {"assuntos.codigo": CODIGO_ASSUNTO}},
        "sort": [{"@timestamp": {"order": "asc"}}],
    }
    if search_after:
        corpo["search_after"] = search_after

    for tentativa in range(1, TENTATIVAS + 1):
        try:
            resposta = requests.post(url, headers=CABECALHOS, json=corpo, timeout=180)
            if resposta.status_code == 200:
                return resposta.json()["hits"]["hits"]
            print(f"  Tentativa {tentativa}/{TENTATIVAS}: status {resposta.status_code}")
        except requests.exceptions.RequestException as erro:
            print(f"  Tentativa {tentativa}/{TENTATIVAS}: {type(erro).__name__}")
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


def garantir_tribunal(cursor, sigla, nome):
    cursor.execute(
        """
        INSERT INTO tribunal (sigla, nome, esfera) VALUES (%s, %s, 'estadual')
        ON CONFLICT (sigla) DO NOTHING
        """,
        (sigla, nome),
    )
    cursor.execute("SELECT id FROM tribunal WHERE sigla = %s", (sigla,))
    return cursor.fetchone()[0]


def gravar_processo(cursor, tribunal_id, processo):
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


resumo = {}

with conectar_banco() as conexao:
    for sigla, nome in TRIBUNAIS.items():
        print(f"{sigla}: buscando...")

        with conexao.cursor() as cursor:
            tribunal_id = garantir_tribunal(cursor, sigla, nome)
        conexao.commit()

        total = 0
        search_after = None
        falhou = False

        for pagina in range(1, MAX_PAGINAS + 1):
            resultados = buscar_pagina(sigla, search_after)
            if resultados is None:
                falhou = True
                break
            if not resultados:
                break

            with conexao.cursor() as cursor:
                for item in resultados:
                    gravar_processo(cursor, tribunal_id, item["_source"])
            conexao.commit()

            total += len(resultados)
            search_after = resultados[-1]["sort"]
            print(f"  página {pagina}: {total} processos até agora")

            if len(resultados) < TAMANHO_PAGINA:
                break
            time.sleep(1)

        resumo[sigla] = f"{total}" + (" (parou no meio por erro da API)" if falhou else "")

print()
print("RESUMO")
for sigla, resultado in resumo.items():
    print(f"  {sigla}: {resultado}")