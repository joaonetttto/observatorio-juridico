CREATE TABLE IF NOT EXISTS coleta (
    id SERIAL PRIMARY KEY,
    tribunal_id INTEGER NOT NULL REFERENCES tribunal(id),
    iniciada_em TIMESTAMP NOT NULL DEFAULT NOW(),
    finalizada_em TIMESTAMP,
    status VARCHAR(20) NOT NULL DEFAULT 'em_andamento',
    qtd_processos INTEGER NOT NULL DEFAULT 0
);