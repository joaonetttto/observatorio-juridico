import os

import psycopg
from dotenv import load_dotenv

load_dotenv()

conexao_texto = (
    f"host={os.getenv('DB_HOST')} "
    f"port={os.getenv('DB_PORT')} "
    f"dbname={os.getenv('DB_NAME')} "
    f"user={os.getenv('DB_USER')} "
    f"password={os.getenv('DB_PASSWORD')}"
)

with psycopg.connect(conexao_texto) as conexao:
    with conexao.cursor() as cursor:
        cursor.execute("SELECT sigla, nome FROM tribunal")
        for linha in cursor.fetchall():
            print(linha)