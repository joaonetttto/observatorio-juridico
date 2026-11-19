SELECT t.sigla, c.iniciada_em, c.status, c.qtd_processos
FROM coleta c
JOIN tribunal t ON t.id = c.tribunal_id
ORDER BY c.iniciada_em DESC;