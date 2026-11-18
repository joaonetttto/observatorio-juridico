-- 1. Processos por ano de ajuizamento
SELECT EXTRACT(YEAR FROM data_ajuizamento)::int AS ano, COUNT(*) AS quantidade
FROM processo
GROUP BY ano
ORDER BY ano;

-- 2. Assuntos que mais aparecem junto com "Proteção de Dados Pessoais"
SELECT COALESCE(a.nome, 'sem nome (código ' || a.codigo || ')') AS assunto, COUNT(*) AS quantidade
FROM processo_assunto pa
JOIN assunto a ON a.codigo = pa.assunto_codigo
WHERE a.codigo <> 14206
GROUP BY a.codigo, a.nome
ORDER BY quantidade DESC
LIMIT 10;

-- 3. Classes de processo mais comuns
SELECT classe, COUNT(*) AS quantidade
FROM processo
GROUP BY classe
ORDER BY quantidade DESC
LIMIT 10;