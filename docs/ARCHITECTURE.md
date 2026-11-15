# Arquitetura — LuzVital

## Visão geral

```text
[Site HTML/CSS/JS servido pelo próprio Spring Boot em /] --HTTP/JSON--> [API Spring Boot /api (render.com)] --JDBC--> [Oracle]
                                              |
                                  [Python: análise de dados e algoritmo PD]
                                  (consomem CSV exportado / dados simulados)
```

A rede onde a solução roda fisicamente é projetada no Packet Tracer (`network/`).

## Backend (Domain Driven Design - Java)

- Java 21, Spring Boot 4.1.2, Maven Wrapper. Pacote base `br.com.luzvital` (veja `backend/README.md`).
- Camadas exigidas em aula:

| Camada | Responsabilidade |
|---|---|
| `model` | Entidades do domínio, alinhadas às tabelas Oracle |
| `dao` | Acesso a dados com **JDBC puro** (SQL escrito à mão, `PreparedStatement`), padrão ensinado em aula |
| `bo` | Regras de negócio (ex.: cruzar interrupção com pacientes, gerar alertas) |
| `controller` | Endpoints REST: GET, POST, PUT, DELETE |
| `exception` | Exceções de domínio e handler global com respostas HTTP coerentes |

- Configuração por variáveis de ambiente (`DB_URL`, `DB_USERNAME`, `DB_PASSWORD`); veja `env.example`.
- Perfis: `dev` (Oracle local em Docker) e `prod` (Oracle da FIAP, deploy no render.com).

> ✅ Decidido em 13/11/2026: o padrão de aula é **JDBC puro com DAO manual**. Não usar Spring Data JPA.

## Decisões em aberto

| Decisão | Status |
|---|---|
| Tecnologia do frontend | **Decidido (15/11): HTML5, CSS3 e JavaScript puro**, sem frameworks. Arquivos em `backend/src/main/resources/static/` (um único deploy) |
| JDBC puro vs. JPA no DAO | **Decidido: JDBC puro (DAO manual)** |
| Fonte dos dados para Data Science | A definir (pública ou simulada) |
| Problema de Programação Dinâmica | A definir (ex.: rota de visita a pacientes por grafo; priorização por autonomia) |
