@echo off
cd /d "%~dp0.."
if not exist logs mkdir logs
docker compose up -d
.venv\Scripts\python.exe src\atualizar_tudo.py >> logs\atualizacao.log 2>&1