import glob
import json
import os

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


for caminho in sorted(glob.glob(os.path.join("dados", "*.json"))):
    with open(caminho, encoding="utf-8") as arquivo:
        acordaos = json.load(arquivo)

    contagem = {palavra: 0 for palavra in PALAVRAS}
    achados = []
    for acordao in acordaos:
        texto = texto_do_acordao(acordao)
        achou = False
        for palavra in PALAVRAS:
            if palavra in texto:
                contagem[palavra] += 1
                achou = True
        if achou:
            achados.append(acordao)

    print("=" * 60)
    print("Arquivo:", os.path.basename(caminho))
    print("Total de acórdãos:", len(acordaos))
    for palavra, quantidade in contagem.items():
        print(f"  menciona '{palavra}': {quantidade}")
    print("Acórdãos com alguma das palavras:", len(achados))

    for acordao in achados[:3]:
        print("-" * 60)
        print("ID:", acordao.get("id"))
        print("Classe:", acordao.get("descricaoClasse"))
        print("Órgão:", acordao.get("nomeOrgaoJulgador"))
        print("Data:", acordao.get("dataDecisao"))
        print("Ementa:", (acordao.get("ementa") or "")[:300].replace("\n", " "))