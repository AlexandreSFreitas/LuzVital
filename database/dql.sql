-- =====================================================================
-- LuzVital — Database Design · GS 2026.2 · FIAP
-- DQL: as 3 consultas da rubrica (rodar depois do ddl.sql e do dml.sql)
-- =====================================================================

-- ---------------------------------------------------------------------
-- Consulta 1 — INNER JOIN com duas tabelas
-- Pergunta: em que região mora cada paciente cadastrado?
-- Uso na LuzVital: é esse vínculo paciente -> região que permite saber
-- quem é afetado quando falta energia num bairro.
-- ---------------------------------------------------------------------
SELECT p.id_paciente,
       p.nome        AS paciente,
       r.nome        AS regiao,
       r.cidade,
       r.uf
  FROM paciente p
 INNER JOIN regiao r ON r.id_regiao = p.id_regiao
 ORDER BY r.nome, p.nome;

-- ---------------------------------------------------------------------
-- Consulta 2 — INNER JOIN com função de grupo e GROUP BY
-- Pergunta: em cada interrupção, quantos alertas estão em cada status?
-- Uso na LuzVital: mostra rapidamente quantos avisos ainda não foram
-- confirmados (PENDENTE / SEM_RESPOSTA) e exigem nova tentativa.
-- ---------------------------------------------------------------------
SELECT i.id_interrupcao,
       r.nome            AS regiao,
       i.status          AS status_interrupcao,
       a.status          AS status_alerta,
       COUNT(*)          AS qtd_alertas,
       MIN(a.prioridade) AS prioridade_mais_alta
  FROM interrupcao i
 INNER JOIN regiao r ON r.id_regiao      = i.id_regiao
 INNER JOIN alerta a ON a.id_interrupcao = i.id_interrupcao
 GROUP BY i.id_interrupcao, r.nome, i.status, a.status
 ORDER BY i.id_interrupcao, a.status;

-- ---------------------------------------------------------------------
-- Consulta 3 — LEFT OUTER JOIN com WHERE e ORDER BY
-- Pergunta: quais pacientes ativos receberam alertas e com que
-- prioridade — incluindo quem nunca recebeu nenhum alerta?
-- Uso na LuzVital: pacientes sem alerta aparecem com colunas nulas
-- (ex.: Rosa, de Pinheiros), o que ajuda a conferir a cobertura.
-- ---------------------------------------------------------------------
SELECT p.id_paciente,
       p.nome         AS paciente,
       a.id_alerta,
       a.id_interrupcao,
       a.prioridade,
       a.status       AS status_alerta,
       a.data_criacao
  FROM paciente p
  LEFT OUTER JOIN alerta a ON a.id_paciente = p.id_paciente
 WHERE p.ativo = 'S'
 ORDER BY a.prioridade NULLS LAST, p.nome, a.id_alerta;
