import glob
import json
import os
from collections import Counter

import psycopg
from dotenv import load_dotenv

from filtro_lgpd import texto_do_acordao
from temas import temas_do_texto

load_dotenv()

with psycopg.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
) as conexao:
    with conexao.cursor() as cursor:
        cursor.execute("SELECT id_stj, relacao_lgpd FROM acordao")
        relacoes = dict(cursor.fetchall())

    guardados = {}
    for caminho in sorted(glob.glob(os.path.join("dados", "*.json"))):
        try:
            with open(caminho, encoding="utf-8") as arquivo:
                for acordao in json.load(arquivo):
                    if acordao["id"] in relacoes:
                        guardados[acordao["id"]] = acordao
        except (json.JSONDecodeError, UnicodeDecodeError):
            pass

    classificados = {
        id_stj: temas_do_texto(texto_do_acordao(acordao))
        for id_stj, acordao in guardados.items()
    }

    with conexao.cursor() as cursor:
        cursor.execute("DELETE FROM acordao_tema")
        for id_stj, temas in classificados.items():
            for tema in temas:
                cursor.execute(
                    "INSERT INTO acordao_tema (id_stj, tema) VALUES (%s, %s)",
                    (id_stj, tema),
                )
    conexao.commit()

print("Acórdãos classificados:", len(classificados))

for grupo in ["cita_lgpd", "menciona_dados_pessoais"]:
    ids = [i for i in classificados if relacoes[i] == grupo]
    contagem = Counter(t for i in ids for t in classificados[i])
    sem_tema = [i for i in ids if not classificados[i]]
    print()
    print(f"{grupo}: {len(ids)} acórdãos")
    for tema, quantidade in contagem.most_common():
        print(f"  {tema}: {quantidade}")
    print(f"  (sem nenhum tema: {len(sem_tema)})")

sem_tema_cita = [
    i for i in classificados if relacoes[i] == "cita_lgpd" and not classificados[i]
]
print()
print("Exemplos de acórdãos que citam a LGPD e ficaram sem tema:")
for id_stj in sem_tema_cita[:6]:
    ementa = (guardados[id_stj].get("ementa") or "")[:220].replace("\n", " ")
    print("-", id_stj, "|", ementa)