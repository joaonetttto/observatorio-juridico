CREATE TABLE decisao (
    id SERIAL PRIMARY KEY,
    processo_id INTEGER NOT NULL REFERENCES processo(id),
    tipo VARCHAR(50) NOT NULL,
    data_decisao DATE NOT NULL,
    texto TEXT NOT NULL
);

INSERT INTO decisao (processo_id, tipo, data_decisao, texto) VALUES
    (1, 'sentença', '2025-09-15', 'Julgo procedente o pedido. Condeno a ré ao pagamento de indenização por danos morais em razão de vazamento de dados pessoais do autor.'),
    (2, 'sentença', '2025-10-03', 'Julgo improcedente o pedido. Não ficou comprovado o tratamento indevido de dados pessoais pela ré.');