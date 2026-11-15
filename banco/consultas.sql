SELECT p.numero_cnj, t.sigla, p.assunto
FROM processo p
JOIN tribunal t ON t.id = p.tribunal_id;