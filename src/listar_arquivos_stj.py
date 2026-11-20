import requests

URL_DA_PAGINA = "https://dadosabertos.web.stj.jus.br/dataset/espelhos-de-acordaos-primeira-secao"

slug = URL_DA_PAGINA.rstrip("/").split("/")[-1]
base = URL_DA_PAGINA.split("/dataset/")[0]

resposta = requests.get(
    f"{base}/api/3/action/package_show",
    params={"id": slug},
    timeout=60,
)
print("Status:", resposta.status_code)

if resposta.status_code != 200:
    raise SystemExit("A API não respondeu como esperado.")

recursos = resposta.json()["result"]["resources"]
print("Arquivos encontrados:", len(recursos))
for recurso in recursos:
    print(recurso.get("name"), "|", recurso.get("format"), "|", recurso.get("url"))