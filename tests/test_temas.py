from temas import temas_do_texto


def test_cadastro_e_credito():
    texto = "sistema de informações de crédito (scr). notificação prévia."
    assert "Cadastro e crédito" in temas_do_texto(texto)


def test_vazamento():
    texto = "vazamento de dados sensíveis. dano moral presumido."
    assert "Vazamento e incidentes" in temas_do_texto(texto)


def test_um_acordao_pode_ter_mais_de_um_tema():
    texto = "código de defesa do consumidor. vazamento de dados."
    temas = temas_do_texto(texto)
    assert "Consumidor" in temas
    assert "Vazamento e incidentes" in temas


def test_internet_e_provedores():
    texto = "responsabilidade do provedor de aplicação de internet."
    assert "Internet e provedores" in temas_do_texto(texto)


def test_texto_sem_tema_devolve_lista_vazia():
    assert temas_do_texto("recurso especial inadmissível") == []