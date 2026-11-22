TEMAS = {
    "Cadastro e crédito": [
        "sistema de informações de crédito",
        "cadastro positivo",
        "lei:012414",
        "12.414",
        "serasa",
        "negativação",
        "cadastro de inadimplentes",
        "proteção ao crédito",
    ],
    "Bancário e fraude": [
        "instituição financeira",
        "bancário",
        "bancária",
        "fraude",
        "cartão de crédito",
        "conta corrente",
        "golpe",
    ],
    "Internet e provedores": [
        "marco civil",
        "lei:012965",
        "12.965",
        "provedor",
        "aplicação de internet",
        "aplicações de internet",
        "rede social",
        "redes sociais",
        "desindexação",
        "direito ao esquecimento",
        "plataforma digital",
        "whatsapp",
        "google",
        "facebook",
        "instagram",
    ],
    "Acesso à informação": [
        "acesso à informação",
        "lei:012527",
        "12.527",
        "habeas data",
        "transparência",
    ],
    "Investigação criminal e sigilo": [
        "quebra de sigilo",
        "interceptação",
        "inquérito",
        "investigação criminal",
        "processo penal",
        "processual penal",
        "sigilo bancário",
        "sigilo telefônico",
        "organização criminosa",
        "busca e apreensão",
    ],
    "Saúde": [
        "plano de saúde",
        "operadora de saúde",
        "prontuário",
        "dados de saúde",
        "hospital",
    ],
    "Consumidor": [
        "código de defesa do consumidor",
        "direito do consumidor",
        "relação de consumo",
        "consumidor",
    ],
}


def temas_do_texto(texto):
    return [
        tema
        for tema, palavras in TEMAS.items()
        if any(palavra in texto for palavra in palavras)
    ]