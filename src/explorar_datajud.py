import json
import os

import requests
from dotenv import load_dotenv

load_dotenv()

URL = "https://api-publica.datajud.cnj.jus.br/api_publica_tjac/_search"
CABECALHOS = {
    "Authorization": f"APIKey {os.getenv('DATAJUD_API_KEY')}",
    "Content-Type": "application/json",
}
CORPO = {"size": 3, "query": {"match_all": {}}}

resposta = requests.post(URL, headers=CABECALHOS, json=CORPO, timeout=120)
print("Status:", resposta.status_code)
print(json.dumps(resposta.json(), indent=2, ensure_ascii=False)[:3000])