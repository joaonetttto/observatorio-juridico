SELECT relacao_lgpd, COUNT(*) AS quantidade
FROM acordao
GROUP BY relacao_lgpd;