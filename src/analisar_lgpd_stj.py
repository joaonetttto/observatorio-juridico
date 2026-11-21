import glob
import json
import os
import re
from collections import Counter

PADRAO_LEI = re.compile(r"(?<!\d)0?13\.?709(?!\d)")
NOMES_FORTES = ["lgpd", "lei geral de proteção de dados"]
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


def posicao_forte(texto):
    posicoes = []
    achou = PADRAO_LEI.search(texto)
    if achou:
        posicoes.append(achou.start())
    for nome in NOMES_FORTES:
        posicao = texto.find(nome)
        if posicao >= 0:
            posicoes.append(posicao)
    return min(posicoes) if posicoes else None


def trecho(texto, posicao, tamanho=120):
    inicio = max(0, posicao - tamanho)
    fim = min(len(texto), posicao + tamanho)
    return texto[inicio:fim].replace("\n", " ")


todos = {}
for caminho in sorted(glob.glob(os.path.join("dados", "*.json"))):
    try:
        with open(caminho, encoding="utf-8") as arquivo:
            for acordao in json.load(arquivo):
                todos[acordao["id"]] = acordao
    except (json.JSONDecodeError, UnicodeDecodeError):
        print("Ignorado (erro no arquivo):", os.path.basename(caminho))

fortes = []
fracos = []
for acordao in todos.values():
    texto = texto_do_acordao(acordao)
    posicao = posicao_forte(texto)
    if posicao is not None:
        fortes.append((acordao, texto, posicao))
    elif "dados pessoais" in texto:
        fracos.append((acordao, texto, texto.find("dados pessoais")))

print("Acórdãos únicos:", len(todos))
print("Fortes (citam a LGPD / Lei 13.709):", len(fortes))
print("Fracos (só falam 'dados pessoais'):", len(fracos))

print()
print("FORTES por órgão julgador:")
for orgao, qtd in Counter(a.get("nomeOrgaoJulgador") for a, _, _ in fortes).most_common():
    print(f"  {orgao}: {qtd}")

print("FORTES por ano da decisão:")
por_ano = Counter((a.get("dataDecisao") or "")[:4] for a, _, _ in fortes)
for ano, qtd in sorted(por_ano.items()):
    print(f"  {ano}: {qtd}")


def mostrar(titulo, lista):
    print()
    print("=" * 60)
    print(titulo)
    for acordao, texto, posicao in lista[:5]:
        print("-" * 60)
        print("ID:", acordao.get("id"), "|", acordao.get("nomeOrgaoJulgador"))
        print("Classe:", acordao.get("descricaoClasse"))
        print("Trecho:", "..." + trecho(texto, posicao) + "...")


mostrar("EXEMPLOS FORTES", fortes)
mostrar("EXEMPLOS FRACOS", fracos)