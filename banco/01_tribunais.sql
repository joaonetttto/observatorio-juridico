CREATE TABLE tribunal (
    id SERIAL PRIMARY KEY,
    sigla VARCHAR(10) NOT NULL UNIQUE,
    nome VARCHAR(200) NOT NULL,
    esfera VARCHAR(30) NOT NULL
);

INSERT INTO tribunal (sigla, nome, esfera) VALUES
    ('TJSP', 'Tribunal de Justiça de São Paulo', 'estadual'),
    ('TJRJ', 'Tribunal de Justiça do Rio de Janeiro', 'estadual'),
    ('STJ', 'Superior Tribunal de Justiça', 'superior');