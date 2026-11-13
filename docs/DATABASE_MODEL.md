# Modelo de dados — LuzVital (rascunho)

**Status:** rascunho para discussão. O modelo oficial é o do Oracle Data Modeler. Use a Skill `oracle-database` para evoluir.

## Entidades candidatas

| Entidade | Atributos principais | Relacionamentos |
|---|---|---|
| REGIAO | id, nome, cidade, uf | 1:N PACIENTE, 1:N INTERRUPCAO |
| PACIENTE | id, nome (fictício), data_nascimento, endereço, id_regiao, nivel_risco | N:1 REGIAO; 1:N EQUIPAMENTO; N:N CONTATO |
| EQUIPAMENTO | id, tipo, consumo_watts, autonomia_bateria_min, id_paciente | N:1 PACIENTE |
| CONTATO | id, nome (fictício), tipo (familiar, cuidador, equipe), telefone (fictício) | N:N PACIENTE (via PACIENTE_CONTATO) |
| PACIENTE_CONTATO | id_paciente, id_contato, prioridade | associativa |
| INTERRUPCAO | id, id_regiao, inicio, fim, origem | N:1 REGIAO; 1:N ALERTA |
| ALERTA | id, id_interrupcao, id_paciente, id_contato, status, criado_em, confirmado_em | N:1 INTERRUPCAO, PACIENTE, CONTATO |
| OCORRENCIA | id, id_alerta, descricao, registrada_em | N:1 ALERTA |

## Regras

- PKs numéricas (`IDENTITY` ou sequence, conforme ensinado em aula).
- FKs nomeadas (`fk_<tabela>_<referencia>`), CHECK para domínios (`status`, `tipo`).
- Mínimo de 5 linhas por tabela no DML, todas fictícias.
- Mesmo modelo usado no backend (camada model) e no DER da documentação de DDD.
