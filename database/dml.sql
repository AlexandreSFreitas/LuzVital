-- =====================================================================
-- LuzVital — Database Design · GS 2026.2 · FIAP
-- DML: dados de exemplo (rodar depois do ddl.sql)
--
-- TODOS OS DADOS SÃO FICTÍCIOS. Nomes, endereços, CEPs, telefones e
-- e-mails foram inventados pela equipe (e-mails no domínio reservado
-- example.com). Os bairros são reais apenas como referência geográfica.
-- Consumo em watts: valores aproximados, só para fins acadêmicos.
--
-- Os IDs são informados de forma explícita para que as FKs fiquem
-- legíveis. No final, as colunas IDENTITY são ajustadas para continuar
-- depois do maior ID, evitando conflito com inserts feitos pela API.
--
-- Cenário montado para as consultas do dql.sql:
--   * Rosa (Pinheiros) não recebeu nenhum alerta  -> aparece no LEFT JOIN
--   * Butantã teve interrupção, mas não tem pacientes cadastrados
-- =====================================================================

-- REGIAO (6 linhas)
INSERT INTO regiao (id_regiao, nome, cidade, uf) VALUES (1, 'Vila Mariana',  'São Paulo', 'SP');
INSERT INTO regiao (id_regiao, nome, cidade, uf) VALUES (2, 'Itaquera',      'São Paulo', 'SP');
INSERT INTO regiao (id_regiao, nome, cidade, uf) VALUES (3, 'Capão Redondo', 'São Paulo', 'SP');
INSERT INTO regiao (id_regiao, nome, cidade, uf) VALUES (4, 'Santana',       'São Paulo', 'SP');
INSERT INTO regiao (id_regiao, nome, cidade, uf) VALUES (5, 'Pinheiros',     'São Paulo', 'SP');
INSERT INTO regiao (id_regiao, nome, cidade, uf) VALUES (6, 'Butantã',       'São Paulo', 'SP');

-- PACIENTE (6 linhas)
INSERT INTO paciente (id_paciente, nome, data_nascimento, logradouro, numero, complemento, cep, id_regiao, observacao_atendimento, ativo, data_cadastro)
VALUES (1, 'Helena Ramos Teixeira', DATE '1946-03-12', 'Rua das Acácias', '120', 'Apto 31', '04101001', 1,
        'Prédio sem elevador; acesso pela escada', 'S', TIMESTAMP '2026-09-01 10:00:00');
INSERT INTO paciente (id_paciente, nome, data_nascimento, logradouro, numero, complemento, cep, id_regiao, observacao_atendimento, ativo, data_cadastro)
VALUES (2, 'Joaquim Batista Nogueira', DATE '1959-07-25', 'Rua Ipê Amarelo', '45', NULL, '08210002', 2,
        NULL, 'S', TIMESTAMP '2026-09-03 14:30:00');
INSERT INTO paciente (id_paciente, nome, data_nascimento, logradouro, numero, complemento, cep, id_regiao, observacao_atendimento, ativo, data_cadastro)
VALUES (3, 'Lúcia Ferraz Moreira', DATE '1972-11-02', 'Travessa dos Girassóis', '8', 'Casa 2', '05870003', 3,
        'Portão azul no fim da viela', 'S', TIMESTAMP '2026-09-10 09:15:00');
INSERT INTO paciente (id_paciente, nome, data_nascimento, logradouro, numero, complemento, cep, id_regiao, observacao_atendimento, ativo, data_cadastro)
VALUES (4, 'Benedito Alves Prado', DATE '1940-01-30', 'Avenida das Palmeiras', '1500', 'Bloco B, apto 104', '02020004', 4,
        'Cuidadora presente só à noite', 'S', TIMESTAMP '2026-09-15 16:45:00');
INSERT INTO paciente (id_paciente, nome, data_nascimento, logradouro, numero, complemento, cep, id_regiao, observacao_atendimento, ativo, data_cadastro)
VALUES (5, 'Rosa Menezes Cardoso', DATE '1951-05-18', 'Rua dos Jacarandás', '310', NULL, '05420005', 5,
        NULL, 'S', TIMESTAMP '2026-10-02 11:20:00');
INSERT INTO paciente (id_paciente, nome, data_nascimento, logradouro, numero, complemento, cep, id_regiao, observacao_atendimento, ativo, data_cadastro)
VALUES (6, 'Caio Henrique Duarte', DATE '1985-09-09', 'Rua Flor de Lis', '77', NULL, '05870006', 3,
        'Usa cadeira de rodas; entrada pela garagem', 'S', TIMESTAMP '2026-10-20 08:05:00');

-- EQUIPAMENTO (6 linhas, catálogo)
INSERT INTO equipamento (id_equipamento, nome, categoria, consumo_watts, suporte_vida) VALUES (1, 'Concentrador de oxigênio',          'RESPIRATORIO',  350, 'S');
INSERT INTO equipamento (id_equipamento, nome, categoria, consumo_watts, suporte_vida) VALUES (2, 'Ventilador mecânico domiciliar',    'RESPIRATORIO',  120, 'S');
INSERT INTO equipamento (id_equipamento, nome, categoria, consumo_watts, suporte_vida) VALUES (3, 'Bomba de infusão de dieta enteral', 'ALIMENTACAO',    15, 'N');
INSERT INTO equipamento (id_equipamento, nome, categoria, consumo_watts, suporte_vida) VALUES (4, 'Aspirador de secreções',            'RESPIRATORIO',   90, 'N');
INSERT INTO equipamento (id_equipamento, nome, categoria, consumo_watts, suporte_vida) VALUES (5, 'Monitor multiparamétrico',          'MONITORAMENTO',  40, 'N');
INSERT INTO equipamento (id_equipamento, nome, categoria, consumo_watts, suporte_vida) VALUES (6, 'Cama hospitalar elétrica',          'OUTRO',         180, 'N');

-- PACIENTE_EQUIPAMENTO (9 linhas)
INSERT INTO paciente_equipamento (id_paciente_equipamento, id_paciente, id_equipamento, autonomia_bateria_min, fonte_alternativa) VALUES (1, 1, 1,   0, NULL);
INSERT INTO paciente_equipamento (id_paciente_equipamento, id_paciente, id_equipamento, autonomia_bateria_min, fonte_alternativa) VALUES (2, 1, 5, 120, NULL);
INSERT INTO paciente_equipamento (id_paciente_equipamento, id_paciente, id_equipamento, autonomia_bateria_min, fonte_alternativa) VALUES (3, 2, 2, 240, 'nobreak');
INSERT INTO paciente_equipamento (id_paciente_equipamento, id_paciente, id_equipamento, autonomia_bateria_min, fonte_alternativa) VALUES (4, 3, 3, 480, NULL);
INSERT INTO paciente_equipamento (id_paciente_equipamento, id_paciente, id_equipamento, autonomia_bateria_min, fonte_alternativa) VALUES (5, 3, 6,   0, NULL);
INSERT INTO paciente_equipamento (id_paciente_equipamento, id_paciente, id_equipamento, autonomia_bateria_min, fonte_alternativa) VALUES (6, 4, 1,  60, 'nobreak');
INSERT INTO paciente_equipamento (id_paciente_equipamento, id_paciente, id_equipamento, autonomia_bateria_min, fonte_alternativa) VALUES (7, 5, 2, 300, 'gerador');
INSERT INTO paciente_equipamento (id_paciente_equipamento, id_paciente, id_equipamento, autonomia_bateria_min, fonte_alternativa) VALUES (8, 6, 4,  30, NULL);
INSERT INTO paciente_equipamento (id_paciente_equipamento, id_paciente, id_equipamento, autonomia_bateria_min, fonte_alternativa) VALUES (9, 6, 1,   0, NULL);

-- CONTATO (8 linhas)
INSERT INTO contato (id_contato, nome, tipo, telefone, email) VALUES (1, 'Paula Ramos Teixeira',        'FAMILIAR',     '(11) 90000-0001', 'paula.teixeira@example.com');
INSERT INTO contato (id_contato, nome, tipo, telefone, email) VALUES (2, 'Equipe Home Care Zona Sul',   'EQUIPE_SAUDE', '(11) 3000-0002',  'homecare.sul@example.com');
INSERT INTO contato (id_contato, nome, tipo, telefone, email) VALUES (3, 'Marcos Batista Nogueira',     'FAMILIAR',     '(11) 90000-0003', NULL);
INSERT INTO contato (id_contato, nome, tipo, telefone, email) VALUES (4, 'Sônia Lima',                  'CUIDADOR',     '(11) 90000-0004', 'sonia.lima@example.com');
INSERT INTO contato (id_contato, nome, tipo, telefone, email) VALUES (5, 'Renato Ferraz',               'FAMILIAR',     '(11) 90000-0005', NULL);
INSERT INTO contato (id_contato, nome, tipo, telefone, email) VALUES (6, 'Equipe Home Care Zona Norte', 'EQUIPE_SAUDE', '(11) 3000-0006',  'homecare.norte@example.com');
INSERT INTO contato (id_contato, nome, tipo, telefone, email) VALUES (7, 'Teresa Cardoso',              'FAMILIAR',     '(11) 90000-0007', 'teresa.cardoso@example.com');
INSERT INTO contato (id_contato, nome, tipo, telefone, email) VALUES (8, 'Ana Duarte',                  'FAMILIAR',     '(11) 90000-0008', NULL);

-- PACIENTE_CONTATO (11 linhas)
INSERT INTO paciente_contato (id_paciente, id_contato, ordem_acionamento, vinculo) VALUES (1, 1, 1, 'filha');
INSERT INTO paciente_contato (id_paciente, id_contato, ordem_acionamento, vinculo) VALUES (1, 2, 2, 'equipe de home care');
INSERT INTO paciente_contato (id_paciente, id_contato, ordem_acionamento, vinculo) VALUES (2, 3, 1, 'filho');
INSERT INTO paciente_contato (id_paciente, id_contato, ordem_acionamento, vinculo) VALUES (2, 4, 2, 'cuidadora diurna');
INSERT INTO paciente_contato (id_paciente, id_contato, ordem_acionamento, vinculo) VALUES (3, 5, 1, 'irmão');
INSERT INTO paciente_contato (id_paciente, id_contato, ordem_acionamento, vinculo) VALUES (3, 2, 2, 'equipe de home care');
INSERT INTO paciente_contato (id_paciente, id_contato, ordem_acionamento, vinculo) VALUES (4, 6, 1, 'equipe de home care');
INSERT INTO paciente_contato (id_paciente, id_contato, ordem_acionamento, vinculo) VALUES (4, 4, 2, 'cuidadora noturna');
INSERT INTO paciente_contato (id_paciente, id_contato, ordem_acionamento, vinculo) VALUES (5, 7, 1, 'neta');
INSERT INTO paciente_contato (id_paciente, id_contato, ordem_acionamento, vinculo) VALUES (6, 8, 1, 'esposa');
INSERT INTO paciente_contato (id_paciente, id_contato, ordem_acionamento, vinculo) VALUES (6, 2, 2, 'equipe de home care');

-- INTERRUPCAO (5 linhas)
INSERT INTO interrupcao (id_interrupcao, id_regiao, data_inicio, data_fim, duracao_estimada_min, origem, status)
VALUES (1, 1, TIMESTAMP '2026-10-05 14:10:00', TIMESTAMP '2026-10-05 17:40:00', 180, 'SIMULADA', 'ENCERRADA');
INSERT INTO interrupcao (id_interrupcao, id_regiao, data_inicio, data_fim, duracao_estimada_min, origem, status)
VALUES (2, 2, TIMESTAMP '2026-10-12 08:30:00', TIMESTAMP '2026-10-12 09:15:00',  60, 'SIMULADA', 'ENCERRADA');
INSERT INTO interrupcao (id_interrupcao, id_regiao, data_inicio, data_fim, duracao_estimada_min, origem, status)
VALUES (3, 3, TIMESTAMP '2026-11-10 19:00:00', NULL,                             240, 'SIMULADA', 'ABERTA');
INSERT INTO interrupcao (id_interrupcao, id_regiao, data_inicio, data_fim, duracao_estimada_min, origem, status)
VALUES (4, 6, TIMESTAMP '2026-11-08 10:00:00', TIMESTAMP '2026-11-08 11:30:00',  90, 'MANUAL',   'ENCERRADA');
INSERT INTO interrupcao (id_interrupcao, id_regiao, data_inicio, data_fim, duracao_estimada_min, origem, status)
VALUES (5, 4, TIMESTAMP '2026-11-11 22:15:00', NULL,                             NULL, 'MANUAL',  'ABERTA');

-- ALERTA (10 linhas)
-- Prioridade pela regra da seção 4 de docs/DATABASE_MODEL.md (equipamento de menor autonomia):
--   Helena  (int. 1): concentrador, suporte de vida, 0 min < 180   -> 1
--   Joaquim (int. 2): ventilador, 240 min >= 60                    -> 3
--   Lúcia   (int. 3): cama elétrica sem suporte de vida, 0 < 240   -> 2
--   Caio    (int. 3): concentrador, suporte de vida, 0 < 240       -> 1
--   Benedito(int. 5): concentrador, suporte de vida, duração desconhecida -> 1
INSERT INTO alerta (id_alerta, id_interrupcao, id_paciente, id_contato, prioridade, status, data_criacao, data_confirmacao)
VALUES (1, 1, 1, 1, 1, 'CONFIRMADO',   TIMESTAMP '2026-10-05 14:12:00', TIMESTAMP '2026-10-05 14:20:00');
INSERT INTO alerta (id_alerta, id_interrupcao, id_paciente, id_contato, prioridade, status, data_criacao, data_confirmacao)
VALUES (2, 1, 1, 2, 1, 'CONFIRMADO',   TIMESTAMP '2026-10-05 14:12:00', TIMESTAMP '2026-10-05 14:35:00');
INSERT INTO alerta (id_alerta, id_interrupcao, id_paciente, id_contato, prioridade, status, data_criacao, data_confirmacao)
VALUES (3, 2, 2, 3, 3, 'SEM_RESPOSTA', TIMESTAMP '2026-10-12 08:32:00', NULL);
INSERT INTO alerta (id_alerta, id_interrupcao, id_paciente, id_contato, prioridade, status, data_criacao, data_confirmacao)
VALUES (4, 2, 2, 4, 3, 'CONFIRMADO',   TIMESTAMP '2026-10-12 08:32:00', TIMESTAMP '2026-10-12 08:41:00');
INSERT INTO alerta (id_alerta, id_interrupcao, id_paciente, id_contato, prioridade, status, data_criacao, data_confirmacao)
VALUES (5, 3, 3, 5, 2, 'CONFIRMADO',   TIMESTAMP '2026-11-10 19:02:00', TIMESTAMP '2026-11-10 19:10:00');
INSERT INTO alerta (id_alerta, id_interrupcao, id_paciente, id_contato, prioridade, status, data_criacao, data_confirmacao)
VALUES (6, 3, 3, 2, 2, 'PENDENTE',     TIMESTAMP '2026-11-10 19:02:00', NULL);
INSERT INTO alerta (id_alerta, id_interrupcao, id_paciente, id_contato, prioridade, status, data_criacao, data_confirmacao)
VALUES (7, 3, 6, 8, 1, 'CONFIRMADO',   TIMESTAMP '2026-11-10 19:02:00', TIMESTAMP '2026-11-10 19:05:00');
INSERT INTO alerta (id_alerta, id_interrupcao, id_paciente, id_contato, prioridade, status, data_criacao, data_confirmacao)
VALUES (8, 3, 6, 2, 1, 'PENDENTE',     TIMESTAMP '2026-11-10 19:02:00', NULL);
INSERT INTO alerta (id_alerta, id_interrupcao, id_paciente, id_contato, prioridade, status, data_criacao, data_confirmacao)
VALUES (9, 5, 4, 6, 1, 'PENDENTE',     TIMESTAMP '2026-11-11 22:16:00', NULL);
INSERT INTO alerta (id_alerta, id_interrupcao, id_paciente, id_contato, prioridade, status, data_criacao, data_confirmacao)
VALUES (10, 5, 4, 4, 1, 'CONFIRMADO',  TIMESTAMP '2026-11-11 22:16:00', TIMESTAMP '2026-11-11 22:24:00');

-- ACAO_APOIO (7 linhas)
INSERT INTO acao_apoio (id_acao, id_alerta, tipo, descricao, data_registro)
VALUES (1, 1, 'CONTATO_REALIZADO', 'Filha ligou para a paciente e confirmou que o concentrador parou.', TIMESTAMP '2026-10-05 14:22:00');
INSERT INTO acao_apoio (id_acao, id_alerta, tipo, descricao, data_registro)
VALUES (2, 2, 'DESLOCAMENTO', 'Equipe levou cilindro de oxigênio reserva até a residência.', TIMESTAMP '2026-10-05 15:05:00');
INSERT INTO acao_apoio (id_acao, id_alerta, tipo, descricao, data_registro)
VALUES (3, 2, 'ENERGIA_RESTABELECIDA', 'Energia voltou; concentrador religado e paciente estável.', TIMESTAMP '2026-10-05 17:45:00');
INSERT INTO acao_apoio (id_acao, id_alerta, tipo, descricao, data_registro)
VALUES (4, 4, 'CONTATO_REALIZADO', 'Cuidadora verificou o nobreak do ventilador; autonomia suficiente.', TIMESTAMP '2026-10-12 08:45:00');
INSERT INTO acao_apoio (id_acao, id_alerta, tipo, descricao, data_registro)
VALUES (5, 5, 'CONTATO_REALIZADO', 'Irmão confirmou que a bomba de dieta está funcionando na bateria.', TIMESTAMP '2026-11-10 19:15:00');
INSERT INTO acao_apoio (id_acao, id_alerta, tipo, descricao, data_registro)
VALUES (6, 7, 'ORIENTADO_SAMU_192', 'Esposa orientada a ligar para o SAMU 192 se houver falta de ar.', TIMESTAMP '2026-11-10 19:08:00');
INSERT INTO acao_apoio (id_acao, id_alerta, tipo, descricao, data_registro)
VALUES (7, 10, 'DESLOCAMENTO', 'Cuidadora a caminho com um nobreak extra.', TIMESTAMP '2026-11-11 22:30:00');

COMMIT;

-- ---------------------------------------------------------------------
-- Ajuste das colunas IDENTITY: o próximo ID gerado passa a ser
-- (maior ID existente + 1). Sem isso, o primeiro INSERT feito pela API
-- tentaria usar o ID 1 e falharia por PK duplicada.
-- ---------------------------------------------------------------------
ALTER TABLE regiao               MODIFY id_regiao               GENERATED BY DEFAULT AS IDENTITY (START WITH LIMIT VALUE);
ALTER TABLE paciente             MODIFY id_paciente             GENERATED BY DEFAULT AS IDENTITY (START WITH LIMIT VALUE);
ALTER TABLE equipamento          MODIFY id_equipamento          GENERATED BY DEFAULT AS IDENTITY (START WITH LIMIT VALUE);
ALTER TABLE paciente_equipamento MODIFY id_paciente_equipamento GENERATED BY DEFAULT AS IDENTITY (START WITH LIMIT VALUE);
ALTER TABLE contato              MODIFY id_contato              GENERATED BY DEFAULT AS IDENTITY (START WITH LIMIT VALUE);
ALTER TABLE interrupcao          MODIFY id_interrupcao          GENERATED BY DEFAULT AS IDENTITY (START WITH LIMIT VALUE);
ALTER TABLE alerta               MODIFY id_alerta               GENERATED BY DEFAULT AS IDENTITY (START WITH LIMIT VALUE);
ALTER TABLE acao_apoio           MODIFY id_acao                 GENERATED BY DEFAULT AS IDENTITY (START WITH LIMIT VALUE);
