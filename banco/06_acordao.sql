CREATE TABLE IF NOT EXISTS acordao (
    id_stj VARCHAR(20) PRIMARY KEY,
    numero_processo VARCHAR(30),
    classe VARCHAR(300),
    orgao_julgador VARCHAR(100),
    relator VARCHAR(150),
    data_decisao DATE,
    ementa TEXT,
    relacao_lgpd VARCHAR(30) NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_acordao_data ON acordao (data_decisao);