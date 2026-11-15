import os
import time

import requests
from dotenv import load_dotenv

load_dotenv()

TRIBUNAL = "tjdft"
TENTATIVAS = 6
ESPERA_SEGUNDOS = 15

URL = f"https://api-publica.datajud.cnj.jus.br/api_publica_{TRIBUNAL}/_search"
CABECALHOS = {
    "Authorization": f"APIKey {os.getenv('DATAJUD_API_KEY')}",
    "Content-Type": "application/json",
}
CORPO = {
    "size": 5,
    "track_total_hits": False,
    "query": {"match": {"assuntos.codigo": 14206}},
}


def buscar_com_tentativas():
    for tentativa in range(1, TENTATIVAS + 1):
        try:
            resposta = requests.post(URL, headers=CABECALHOS, json=CORPO, timeout=180)
            if resposta.status_code == 200:
                return resposta.json()
            print(f"Tentativa {tentativa}/{TENTATIVAS}: status {resposta.status_code}")
        except requests.exceptions.RequestException as erro:
            print(f"Tentativa {tentativa}/{TENTATIVAS}: {type(erro).__name__}")
        if tentativa < TENTATIVAS:
            time.sleep(ESPERA_SEGUNDOS)
    return None


dados = buscar_com_tentativas()
if dados is None:
    raise SystemExit("A API não respondeu depois de várias tentativas. Tente mais tarde.")

resultados = dados["hits"]["hits"]
print("Tribunal:", TRIBUNAL)
print("Processos retornados:", len(resultados))

for item in resultados:
    processo = item["_source"]
    print("-" * 40)
    print("Número:", processo["numeroProcesso"])
    print("Ajuizamento:", processo["dataAjuizamento"])
    print("Classe:", processo["classe"]["nome"])
    print("Assuntos:", processo.get("assuntos"))