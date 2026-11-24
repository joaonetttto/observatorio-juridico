ALTER TABLE acordao
    ADD COLUMN IF NOT EXISTS busca tsvector
    GENERATED ALWAYS AS (to_tsvector('portuguese', coalesce(ementa, ''))) STORED;

CREATE INDEX IF NOT EXISTS idx_acordao_busca ON acordao USING GIN (busca);