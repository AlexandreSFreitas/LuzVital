---
name: oracle-database
description: Use ao modelar ou alterar o banco Oracle da LuzVital — modelo relacional, normalização, DDL, DML, DQL, chaves e relacionamentos, integração com o backend Java, ou ao conferir a entrega de Database Design.
---

# oracle-database

Apoia **Database Design** e a camada de dados de **DDD - Java**. Fonte da verdade do modelo: `docs/DATABASE_MODEL.md` (e o diagrama do Oracle Data Modeler).

## Regras
- Oracle SQL (não MySQL/PostgreSQL): `NUMBER`, `VARCHAR2`, `DATE`/`TIMESTAMP`, `GENERATED ... AS IDENTITY` ou sequences, conforme o padrão da aula.
- Constraints nomeadas: `pk_<tabela>`, `fk_<tabela>_<ref>`, `ck_<tabela>_<coluna>`, `uq_<tabela>_<coluna>`.
- Normalização até a 3FN, salvo justificativa escrita.
- Dados **fictícios**. Nenhum dado real de paciente.
- Nunca execute `DROP`, `TRUNCATE` ou `DELETE` sem `WHERE` num banco conectado sem confirmação explícita.
- Ao mudar o modelo, avise o impacto em: backend (model/DAO), DER e diagrama de classes da documentação de DDD, e notebook de Data Science.

## Arquivos de entrega (em `database/`)
- `ddl.sql`: drops seguros no início (opcional, comentados), CREATE TABLE e ALTER TABLE com todas as constraints.
- `dml.sql`: INSERTs com **≥ 5 linhas por tabela** (exceções justificadas em comentário) e `COMMIT;` ao final.
- `dql.sql`: exatamente as 3 consultas da rubrica, cada uma com comentário explicando a pergunta que responde:
  1. INNER JOIN entre duas tabelas.
  2. INNER JOIN com função de grupo e GROUP BY.
  3. LEFT OUTER JOIN com WHERE e ORDER BY.

## Integração com Java
- Conexão por variáveis de ambiente (`DB_URL`, `DB_USERNAME`, `DB_PASSWORD`).
- Desenvolvimento: Oracle Free em Docker (local). Entrega: servidor Oracle da FIAP.
- Os nomes de tabelas e colunas do DDL devem bater com a camada model.

## Validação
- [ ] Rodar `ddl.sql`, `dml.sql` e `dql.sql` **do zero, em sequência, sem erro** num schema limpo.
- [ ] `SELECT COUNT(*)` de cada tabela ≥ 5 (ou exceção justificada).
- [ ] Cada FK do DDL aparece como relacionamento no diagrama, com cardinalidade.
- [ ] As 3 consultas retornam linhas (os dados de exemplo precisam permitir isso, inclusive o LEFT JOIN com linhas sem correspondência).
