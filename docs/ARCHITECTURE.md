# Arquitetura — LuzVital

## Visão geral

```text
[Frontend (a definir)] --HTTP/JSON--> [API Spring Boot (render.com)] --JDBC--> [Oracle]
                                              |
                                  [Python: análise de dados e algoritmo PD]
                                  (consomem CSV exportado / dados simulados)
```

A rede onde a solução roda fisicamente é projetada no Packet Tracer (`network/`).

## Backend (Domain Driven Design - Java)

- Java 21, Spring Boot, Maven Wrapper.
- Camadas exigidas em aula:

| Camada | Responsabilidade |
|---|---|
| `model` | Entidades do domínio, alinhadas às tabelas Oracle |
| `dao` | Acesso a dados (SQL/JDBC ou o padrão ensinado em aula) |
| `bo` | Regras de negócio (ex.: cruzar interrupção com pacientes, gerar alertas) |
| `controller` | Endpoints REST: GET, POST, PUT, DELETE |
| `exception` | Exceções de domínio e handler global com respostas HTTP coerentes |

- Configuração por variáveis de ambiente (`DB_URL`, `DB_USERNAME`, `DB_PASSWORD`); veja `env.example`.
- Perfis: `dev` (Oracle local em Docker) e `prod` (Oracle da FIAP, deploy no render.com).

> ⚠️ Antes de escrever código, confirme com o material da disciplina se o padrão é JDBC puro (DAO manual) ou Spring Data JPA. A rubrica cita **DAO e BO** explicitamente.

## Decisões em aberto

| Decisão | Status |
|---|---|
| Tecnologia do frontend | Não definida |
| JDBC puro vs. JPA no DAO | Confirmar com o material da aula |
| Fonte dos dados para Data Science | A definir (pública ou simulada) |
| Problema de Programação Dinâmica | A definir (ex.: rota de visita a pacientes por grafo; priorização por autonomia) |
