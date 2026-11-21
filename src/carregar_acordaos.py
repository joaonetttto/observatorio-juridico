import glob
import json
import os
from collections import Counter
from datetime import datetime

import psycopg
from dotenv import load_dotenv

from filtro_lgpd import classificar

load_dotenv()


def converter_data(texto):
    if not texto:
        return None
    try:
        return datetime.strptime(texto, "%Y%m%d").date()
    except ValueError:
        return None


todos = {}
for caminho in sorted(glob.glob(os.path.join("dados", "*.json"))):
    try:
        with open(caminho, encoding="utf-8") as arquivo:
            for acordao in json.load(arquivo):
                todos[acordao["id"]] = acordao
    except (json.JSONDecodeError, UnicodeDecodeError):
        print("Ignorado (erro no arquivo):", os.path.basename(caminho))

selecionados = []
for acordao in todos.values():
    relacao = classificar(acordao)
    if relacao:
        selecionados.append((acordao, relacao))

print(f"Acórdãos lidos: {len(todos)}")
print(f"Selecionados para gravar: {len(selecionados)}")

with psycopg.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
) as conexao:
    with conexao.cursor() as cursor:
        for acordao, relacao in selecionados:
            cursor.execute(
                """
                INSERT INTO acordao
                    (id_stj, numero_processo, classe, orgao_julgador, relator,
                     data_decisao, ementa, relacao_lgpd)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id_stj) DO UPDATE SET
                    ementa = EXCLUDED.ementa,
                    relacao_lgpd = EXCLUDED.relacao_lgpd
                """,
                (
                    acordao["id"],
                    acordao.get("numeroProcesso"),
                    acordao.get("descricaoClasse"),
                    acordao.get("nomeOrgaoJulgador"),
                    acordao.get("ministroRelator"),
                    converter_data(acordao.get("dataDecisao")),
                    acordao.get("ementa"),
                    relacao,
                ),
            )
    conexao.commit()

print("Gravados no banco:")
for relacao, quantidade in Counter(r for _, r in selecionados).items():
    print(f"  {relacao}: {quantidade}")