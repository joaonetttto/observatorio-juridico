SELECT t.sigla, COUNT(*) AS processos
FROM processo p
JOIN tribunal t ON t.id = p.tribunal_id
GROUP BY t.sigla
ORDER BY processos DESC;