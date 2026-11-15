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

TESTES = {
    "A: match no codigo": {"match": {"assuntos.codigo": 14206}},
    "B: terms no codigo como texto": {"terms": {"assuntos.codigo": ["14206"]}},
    "C: match_phrase no nome": {"match_phrase": {"assuntos.nome": "Proteção de Dados Pessoais"}},
}

for nome, consulta in TESTES.items():
    corpo = {"size": 3, "track_total_hits": False, "query": consulta}
    resposta = requests.post(URL, headers=CABECALHOS, json=corpo, timeout=180)
    if resposta.status_code != 200:
        print(nome, "-> erro", resposta.status_code)
        continue
    resultados = resposta.json()["hits"]["hits"]
    print(nome, "->", len(resultados), "processos")
    for item in resultados:
        print("    ", item["_source"]["numeroProcesso"], item["_source"].get("assuntos"))