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
com_erro = []
caminhos = sorted(glob.glob(os.path.join("dados", "*.json")))

for caminho in caminhos:
    try:
        with open(caminho, encoding="utf-8") as arquivo:
            acordaos = json.load(arquivo)
    except (json.JSONDecodeError, UnicodeDecodeError) as erro:
        com_erro.append((os.path.basename(caminho), str(erro)))
        continue
    for acordao in acordaos:
        todos[acordao["id"]] = acordao

print("Arquivos lidos:", len(caminhos) - len(com_erro), "de", len(caminhos))
print("Arquivos com erro:", len(com_erro))
for nome, erro in com_erro[:10]:
    print("  ", nome, "->", erro)

print()
print("Acórdãos únicos (sem duplicados):", len(todos))

print()
print("Órgãos julgadores:")
orgaos = Counter(a.get("nomeOrgaoJulgador") for a in todos.values())
for orgao, quantidade in orgaos.most_common():
    print(f"  {orgao}: {quantidade}")

achados = [a for a in todos.values() if any(p in texto_do_acordao(a) for p in PALAVRAS)]
print()
print("Acórdãos que mencionam LGPD ou dados pessoais:", len(achados))

print("Por órgão julgador:")
for orgao, quantidade in Counter(a.get("nomeOrgaoJulgador") for a in achados).most_common():
    print(f"  {orgao}: {quantidade}")

print("Por ano da decisão:")
por_ano = Counter((a.get("dataDecisao") or "")[:4] for a in achados)
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