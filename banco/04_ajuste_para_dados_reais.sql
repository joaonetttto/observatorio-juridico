-- Remove os dados de exemplo
DELETE FROM decisao;
DELETE FROM processo;

-- Ajusta a tabela processo para o formato real
ALTER TABLE processo DROP COLUMN IF EXISTS assunto;
ALTER TABLE processo ALTER COLUMN numero_cnj TYPE VARCHAR(20);
ALTER TABLE processo ALTER COLUMN data_ajuizamento TYPE TIMESTAMP USING data_ajuizamento::timestamp;
ALTER TABLE processo ADD COLUMN IF NOT EXISTS grau VARCHAR(5);
ALTER TABLE processo ADD COLUMN IF NOT EXISTS orgao_julgador VARCHAR(200);
ALTER TABLE processo DROP CONSTRAINT IF EXISTS processo_numero_cnj_key;
ALTER TABLE processo DROP CONSTRAINT IF EXISTS processo_numero_grau_unico;
ALTER TABLE processo ADD CONSTRAINT processo_numero_grau_unico UNIQUE (numero_cnj, grau);

-- Assuntos e a ligação entre processos e assuntos
CREATE TABLE IF NOT EXISTS assunto (
    codigo INTEGER PRIMARY KEY,
    nome VARCHAR(200)
);

CREATE TABLE IF NOT EXISTS processo_assunto (
    processo_id INTEGER NOT NULL REFERENCES processo(id),
    assunto_codigo INTEGER NOT NULL REFERENCES assunto(codigo),
    PRIMARY KEY (processo_id, assunto_codigo)
);

-- Adiciona o TJDFT
INSERT INTO tribunal (sigla, nome, esfera) VALUES
    ('TJDFT', 'Tribunal de Justiça do Distrito Federal e dos Territórios', 'estadual')
ON CONFLICT (sigla) DO NOTHING;