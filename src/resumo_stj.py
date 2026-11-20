import glob
import json
import os
from collections import Counter

PALAVRAS = ["lgpd", "13.709", "lei geral de proteção de dados", "dados pessoais"]
CAMPOS = [
    "ementa",
    "referenciasLegislativas",
    "termosAuxiliares",
    "informacoesComplementares",
    "notas",
]


def texto_do_acordao(acordao):
    partes = []
    for campo in CAMPOS:
        valor = acordao.get(campo)
        if not valor:
            continue
        if isinstance(valor, str):
            partes.append(valor)
        else:
            partes.append(json.dumps(valor, ensure_ascii=False))
    return " ".join(partes).lower()


todos = {}
for caminho in sorted(glob.glob(os.path.join("dados", "*.json"))):
    with open(caminho, encoding="utf-8") as arquivo:
        for acordao in json.load(arquivo):
            todos[acordao["id"]] = acordao

print("Acórdãos únicos (sem duplicados):", len(todos))

print()
print("Órgãos julgadores mais comuns:")
orgaos = Counter(a.get("nomeOrgaoJulgador") for a in todos.values())
for orgao, quantidade in orgaos.most_common(8):
    print(f"  {orgao}: {quantidade}")

achados = [a for a in todos.values() if any(p in texto_do_acordao(a) for p in PALAVRAS)]
print()
print("Acórdãos que mencionam LGPD ou dados pessoais:", len(achados))

por_ano = Counter((a.get("dataDecisao") or "")[:4] for a in achados)
print("Por ano da decisão:")
for ano, quantidade in sorted(por_ano.items()):
    print(f"  {ano}: {quantidade}")

print()
print("Exemplos:")
for acordao in achados[:5]:
    print("-" * 60)
    print("ID:", acordao.get("id"))
    print("Classe:", acordao.get("descricaoClasse"))
    print("Órgão:", acordao.get("nomeOrgaoJulgador"))
    print("Data:", acordao.get("dataDecisao"))
    print("Ementa:", (acordao.get("ementa") or "")[:300].replace("\n", " "))