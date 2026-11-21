import os
import time

import requests

BASE = "https://dadosabertos.web.stj.jus.br"
PASTA = "dados"
PAUSA_SEGUNDOS = 1
IGNORAR = ["primeira seção", "primeira secao"]

os.makedirs(PASTA, exist_ok=True)

resposta = requests.get(
    f"{BASE}/api/3/action/package_search",
    params={"q": "espelhos de acórdãos", "rows": 50},
    timeout=60,
)
resposta.raise_for_status()
conjuntos = resposta.json()["result"]["results"]

selecionados = []
for conjunto in conjuntos:
    titulo = conjunto["title"]
    if "espelho" not in titulo.lower():
        continue
    if any(trecho in titulo.lower() for trecho in IGNORAR):
        print("Pulando (já baixado):", titulo)
        continue
    selecionados.append(conjunto)

print(f"{len(selecionados)} conjuntos para baixar:")
for conjunto in selecionados:
    print("  -", conjunto["title"])

baixados = 0
for conjunto in selecionados:
    prefixo = conjunto["name"]
    arquivos = [
        r for r in conjunto["resources"] if (r.get("format") or "").upper() == "JSON"
    ]
    print(f"\n{conjunto['title']}: {len(arquivos)} arquivos")

    for recurso in arquivos:
        destino = os.path.join(PASTA, f"{prefixo}__{recurso['name']}")
        if os.path.exists(destino):
            continue
        try:
            conteudo = requests.get(recurso["url"], timeout=300)
            conteudo.raise_for_status()
        except requests.exceptions.RequestException as erro:
            print(f"  {recurso['name']}: falhou ({type(erro).__name__}), pulando")
            continue
        with open(destino, "wb") as arquivo:
            arquivo.write(conteudo.content)
        baixados += 1
        time.sleep(PAUSA_SEGUNDOS)

    print(f"  concluído, total de arquivos novos até agora: {baixados}")

print(f"\nPronto. Novos arquivos baixados: {baixados}")