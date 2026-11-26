import subprocess
import sys
from datetime import datetime
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
ETAPAS = [
    "src/carregar_processos.py",
    "src/baixar_acordaos_stj.py",
    "src/carregar_acordaos.py",
    "src/classificar_temas.py",
]


def agora():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")


resultados = {}
for etapa in ETAPAS:
    print(f"[{agora()}] Iniciando {etapa}", flush=True)
    codigo = subprocess.run([sys.executable, etapa], cwd=RAIZ).returncode
    resultados[etapa] = "ok" if codigo == 0 else f"erro (código {codigo})"
    print(f"[{agora()}] Terminou {etapa}: {resultados[etapa]}", flush=True)

print("\nRESUMO")
for etapa, resultado in resultados.items():
    print(f"  {etapa}: {resultado}")

sys.exit(0 if all(r == "ok" for r in resultados.values()) else 1)