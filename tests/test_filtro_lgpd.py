from filtro_lgpd import classificar


def test_cita_a_lei_pelo_numero_na_ementa():
    acordao = {"ementa": "Indenização por danos morais. Lei n. 13.709/2018."}
    assert classificar(acordao) == "cita_lgpd"


def test_cita_a_sigla_lgpd():
    acordao = {"ementa": "Ação de indenização por violação da LGPD."}
    assert classificar(acordao) == "cita_lgpd"


def test_cita_a_lei_nas_referencias_legislativas():
    acordao = {
        "ementa": "Recurso especial.",
        "referenciasLegislativas": ["leg:fed lei:013709 ano:2018"],
    }
    assert classificar(acordao) == "cita_lgpd"


def test_nome_da_lei_quebrado_em_duas_linhas():
    acordao = {"ementa": "Lei geral de proteção\nde dados pessoais. Violação."}
    assert classificar(acordao) == "cita_lgpd"


def test_so_menciona_dados_pessoais():
    acordao = {"ementa": "Habeas data. Informação de dados pessoais."}
    assert classificar(acordao) == "menciona_dados_pessoais"


def test_acordao_sem_relacao_com_o_tema():
    acordao = {"ementa": "Direito tributário. Crédito de PIS e COFINS."}
    assert classificar(acordao) is None


def test_numero_parecido_nao_conta_como_a_lei():
    acordao = {"ementa": "Condenação ao pagamento de R$ 113.709,00."}
    assert classificar(acordao) is None


def test_campos_vazios_nao_quebram():
    assert classificar({"ementa": None}) is None
    assert classificar({}) is None