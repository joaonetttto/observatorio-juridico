import json
import re

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
    texto = " ".join(partes).lower()
    return re.sub(r"(\\n|\s)+", " ", texto)


def classificar(acordao):
    texto = texto_do_acordao(acordao)
    if PADRAO_LEI.search(texto) or any(nome in texto for nome in NOMES_FORTES):
        return "cita_lgpd"
    if "dados pessoais" in texto:
        return "menciona_dados_pessoais"
    return None