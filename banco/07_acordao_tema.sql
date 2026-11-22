CREATE TABLE IF NOT EXISTS acordao_tema (
    id_stj VARCHAR(20) NOT NULL REFERENCES acordao(id_stj),
    tema VARCHAR(60) NOT NULL,
    PRIMARY KEY (id_stj, tema)
);