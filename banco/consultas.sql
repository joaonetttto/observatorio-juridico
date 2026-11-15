SELECT t.sigla, p.assunto, d.tipo, d.data_decisao, d.texto
FROM decisao d
JOIN processo p ON p.id = d.processo_id
JOIN tribunal t ON t.id = p.tribunal_id;