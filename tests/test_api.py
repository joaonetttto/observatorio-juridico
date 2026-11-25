from fastapi.testclient import TestClient

from api import app

client = TestClient(app)


def test_saude_responde_ok():
    resposta = client.get("/saude")
    assert resposta.status_code == 200
    assert resposta.json() == {"status": "ok"}


def test_busca_exige_um_termo():
    assert client.get("/acordaos-busca").status_code == 422


def test_busca_recusa_termo_muito_curto():
    assert client.get("/acordaos-busca?q=a").status_code == 422


def test_endpoint_devolve_o_que_vem_do_banco(monkeypatch):
    dados_falsos = [{"ano": 2025, "quantidade": 3}]
    monkeypatch.setattr("api.consultar", lambda sql, parametros=None: dados_falsos)

    resposta = client.get("/processos-por-ano")

    assert resposta.status_code == 200
    assert resposta.json() == dados_falsos