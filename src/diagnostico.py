import os

import requests
from dotenv import load_dotenv

load_dotenv()

TRIBUNAL = "tjdft"

URL = f"https://api-publica.datajud.cnj.jus.br/api_publica_{TRIBUNAL}/_search"
CABECALHOS = {
    "Authorization": f"APIKey {os.getenv('DATAJUD_API_KEY')}",
    "Content-Type": "application/json",
}


def buscar(corpo):
    resposta = requests.post(URL, headers=CABECALHOS, json=corpo, timeout=180)
    print("Status:", resposta.status_code)
    if resposta.status_code != 200:
        raise SystemExit("A API não respondeu direito. Tente de novo.")
    return resposta.json()["hits"]["hits"]


print("=== TESTE 1: como são os assuntos de 3 processos quaisquer ===")
for item in buscar({"size": 3, "track_total_hits": False, "query": {"match_all": {}}}):
    processo = item["_source"]
    print("Campos disponíveis:", list(processo.keys()))
    print("Assuntos:", processo.get("assuntos"))
    print("-" * 40)

print("=== TESTE 2: busca por texto 'dados pessoais' no nome do assunto ===")
corpo = {
    "size": 5,
    "track_total_hits": False,
    "query": {"match": {"assuntos.nome": "dados pessoais"}},
}
for item in buscar(corpo):
    processo = item["_source"]
    print("Número:", processo["numeroProcesso"])
    print("Assuntos:", processo.get("assuntos"))
    print("-" * 40)