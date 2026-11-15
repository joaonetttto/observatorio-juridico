CREATE TABLE processo (
    id SERIAL PRIMARY KEY,
    numero_cnj VARCHAR(25) NOT NULL UNIQUE,
    tribunal_id INTEGER NOT NULL REFERENCES tribunal(id),
    classe VARCHAR(200),
    assunto VARCHAR(300),
    data_ajuizamento DATE
);

INSERT INTO processo (numero_cnj, tribunal_id, classe, assunto, data_ajuizamento) VALUES
    ('0000001-00.2025.8.26.0100', 1, 'Procedimento Comum Cível', 'Vazamento de dados pessoais', '2025-03-10'),
    ('0000002-00.2025.8.19.0001', 2, 'Procedimento Comum Cível', 'Tratamento indevido de dados', '2025-05-22');