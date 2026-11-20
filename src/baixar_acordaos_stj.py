import os
import time

import requests

BASE = "https://dadosabertos.web.stj.jus.br"
DATASET_ID = "a96a175b-a54b-4bfd-82b8-fcd7cc0200bc"
PASTA = "dados"
PAUSA_SEGUNDOS = 2

os.makedirs(PASTA, exist_ok=True)

resposta = requests.get(
    f"{BASE}/api/3/action/package_show",
    params={"id": DATASET_ID},
    timeout=60,
)
resposta.raise_for_status()
recursos = resposta.json()["result"]["resources"]

arquivos = [r for r in recursos if (r.get("format") or "").upper() == "JSON"]
print(f"{len(arquivos)} arquivos JSON na fonte")

baixados = 0
for recurso in arquivos:
    nome = recurso["name"]
    destino = os.path.join(PASTA, nome)
    if os.path.exists(destino):
        continue
    try:
        conteudo = requests.get(recurso["url"], timeout=300)
        conteudo.raise_for_status()
    except requests.exceptions.RequestException as erro:
        print(f"{nome}: falhou ({type(erro).__name__}), pulando")
        continue
    with open(destino, "wb") as arquivo:
        arquivo.write(conteudo.content)
    baixados += 1
    print(f"{nome}: baixado ({len(conteudo.content) / 1_000_000:.1f} MB)")
    time.sleep(PAUSA_SEGUNDOS)

print(f"Pronto. Novos arquivos baixados: {baixados}")