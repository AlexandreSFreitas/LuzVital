# LuzVital

> **"A energia pode acabar. O cuidado não."**

## Ficha da CitizenTech

| Campo | Resposta |
|---|---|
| **Nome da CitizenTech** | LuzVital |
| **Cidade e bairro** | _a definir pela equipe_ |
| **Cidadão beneficiado** | Pacientes eletrodependentes em casa (home care, "UTI em casa") e sua rede de apoio: familiares, cuidadores e equipes de saúde |
| **Problema, em uma frase** | Quando falta energia, ninguém sabe rapidamente quais pacientes que dependem de aparelhos elétricos estão em risco nem quem deve agir |
| **Como funciona** | O paciente é cadastrado com endereço, região, equipamentos e autonomia de bateria. Quando uma interrupção de energia é registrada numa região, a LuzVital cruza a região com os pacientes, gera alertas para os contatos responsáveis e acompanha a confirmação e o atendimento |
| **O que cada parte faz** | Veja a tabela abaixo |
| **Link do repositório** | _a preencher após a criação no GitHub_ |
| **Indicador de impacto** | Tempo entre a interrupção de energia e a confirmação do alerta por um responsável (_meta a definir_) |
| **ODS conectados** | _Proposta:_ ODS 3 (saúde e bem-estar), ODS 9 (infraestrutura), ODS 10 (redução das desigualdades), ODS 11 (cidades sustentáveis). _Justificativa em `docs/PROJECT_SPEC.md`_ |

## Partes da solução

| Pasta | Disciplina | O que entrega |
|---|---|---|
| [`backend/`](backend/) | Domain Driven Design - Java | API REST em Spring Boot com Oracle, publicada no render.com |
| [`database/`](database/) | Database Design | Modelo lógico (Oracle Data Modeler) e scripts DDL, DML e DQL |
| [`data-science/`](data-science/) | Data Science & Statistical Computing | Notebook com regressão linear e logística |
| [`dynamic-programming/`](dynamic-programming/) | Dynamic Programming | Algoritmo em Python (memoização, tabulação ou grafos) |
| [`network/`](network/) | Network Architect Solutions | Rede no Packet Tracer (.pkt) e relatório |
| [`ar-vr/`](ar-vr/) | AR-VR Modelling And Simulation | Vídeo 3D de 30 a 60 segundos |
| [`frontend/`](frontend/) | Protótipos (Agile e DDD) | Telas da solução (tecnologia a definir) |
| [`pitch/`](pitch/) | Agile e Testing | Roteiro e storyboard do vídeo de até 3 minutos |
| [`docs/`](docs/) | Todas | Especificação, arquitetura, modelo de dados, API, segurança e checklist |

## Equipe

| Nome | RM |
|---|---|
| _a preencher_ | _a preencher_ |

## Uso de IA

A IA foi usada como copiloto para aprender e revisar, conforme as regras da GS. Os prompts relevantes estão em [`prompts.md`](prompts.md).

## Dados

Este repositório **não contém dados pessoais reais**. Todos os dados são simulados ou públicos, com a fonte indicada.
