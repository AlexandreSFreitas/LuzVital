# CLAUDE.md — LuzVital

> "A energia pode acabar. O cuidado não."

Este arquivo orienta o Claude Code neste repositório. Ele é curto de propósito: os detalhes ficam em `docs/`.

## O projeto em 5 linhas

- **LuzVital** é a CitizenTech da equipe na Global Solution 2026.2 da FIAP (Engenharia de Software, 2º ano).
- Ela ajuda **pacientes eletrodependentes** (home care, ventiladores, concentradores de O₂) quando falta energia: correlaciona a interrupção com os pacientes da região e alerta familiares, cuidadores e equipes.
- Uma única solução atravessa **7 disciplinas**. Cada pasta do repositório é uma parte dela.
- **Prazo final: 19/11/2026, 23h55.** Commits depois do prazo **zeram a parte técnica** de Domain Driven Design - Java.
- Nome oficial: **LuzVital**. Nunca use "VitaAlerta" (nome antigo).

## Leia antes de agir

| Se a tarefa envolve... | Leia primeiro |
|---|---|
| Qualquer funcionalidade nova | `docs/PROJECT_SPEC.md` e `docs/MVP_SCOPE.md` |
| Requisitos de uma disciplina | `docs/FIAP_REQUIREMENTS_CHECKLIST.md` |
| Backend Java / API | `docs/ARCHITECTURE.md` e `docs/API_CONTRACT.md` |
| Banco Oracle | `docs/DATABASE_MODEL.md` e a Skill `oracle-database` |
| Dados de pacientes, login, segredos | `docs/SECURITY_AND_PRIVACY.md` e a Skill `luzvital-security` |
| Agile, personas, backlog | Skill `fiap-agile` |
| Vídeo pitch | Skill `documentary-pitch` |
| Packet Tracer | Skill `network-design` |

## Mapa do repositório

| Pasta | Disciplina | Tecnologia |
|---|---|---|
| `backend/` | Domain Driven Design - Java | Java 21, Spring Boot, Maven Wrapper, Oracle |
| `database/` | Database Design | Oracle SQL (DDL, DML, DQL), Oracle Data Modeler |
| `data-science/` | Data Science & Statistical Computing | Python, pandas, scikit-learn, Jupyter |
| `dynamic-programming/` | Dynamic Programming | Python (memoização, tabulação, grafos) |
| `network/` | Network Architect Solutions | Cisco Packet Tracer (.pkt) |
| `ar-vr/` | AR-VR Modelling And Simulation | Vídeo de 30 a 60 s no YouTube |
| `frontend/` | Protótipos e telas (Agile e DDD) | **Ainda não definida.** Não escolha framework sem perguntar |
| `pitch/` | Agile (vídeo de até 3 min) e Testing | Roteiro e storyboard |
| `disciplines/` | Empacotamento final de cada entrega | PDFs, ZIPs (fora do Git) |
| `docs/` | Documentação central | Markdown |

## Fluxo de trabalho obrigatório

1. Identifique a disciplina afetada (tabela acima).
2. Leia os documentos indicados e o item correspondente no checklist FIAP.
3. Analise o código existente antes de propor mudanças.
4. Apresente um plano curto antes de implementar algo com mais de um arquivo.
5. Implemente em passos pequenos.
6. Rode os testes da parte alterada (veja "Como validar").
7. Revise segurança e privacidade (Skill `luzvital-security`) se tocar em dados pessoais, autenticação ou configuração.
8. Atualize a documentação e marque o item no `docs/FIAP_REQUIREMENTS_CHECKLIST.md`.
9. Registre o prompt relevante em `prompts.md` (exigência da FIAP: "IA como copiloto").

**Não altere a pasta de outra disciplina** sem antes explicar o impacto e pedir confirmação. As partes conversam entre si: mudar o modelo do banco afeta o backend, o DER, o diagrama de classes e o notebook.

## Regras de desenvolvimento

- Simples primeiro: uma função que funciona vale mais que dez pela metade.
- Backend em camadas, como pedido em aula: **model, DAO, BO, controller e tratamento de exceções**. Detalhes em `docs/ARCHITECTURE.md`.
- Java 21 (LTS). Use `./mvnw` (ou `mvnw.cmd` no Windows), nunca um Maven global.
- Python sempre em ambiente virtual (`.venv`). Não instale bibliotecas fora do `requirements.txt` sem perguntar.
- Interfaces para o cidadão real: letras legíveis, bom contraste, linguagem simples, telas pequenas.
- Código e identificadores em inglês ou português, mas consistentes dentro de cada parte. Documentação em português.

## Segurança e privacidade (inegociável)

- **Nenhum dado pessoal real.** Só dados simulados ou públicos, sempre com a fonte indicada.
- Nunca leia, imprima nem faça commit de `.env`, wallets Oracle, chaves ou tokens. Use variáveis de ambiente e `env.example`.
- Nunca peça senhas no chat. Credenciais ficam no ambiente do usuário.
- Banco: use usuário com o mínimo de privilégios. Nada de `DROP` ou `TRUNCATE` sem confirmação explícita.
- Commits: **somente em nome do usuário**, sem linhas de coautoria ou "Generated with". Isso já está configurado em `.claude/settings.json`.

## Como validar

| Parte | Comando ou critério |
|---|---|
| Backend | `cd backend && ./mvnw test` (Windows: `mvnw.cmd test`) |
| Banco | Scripts rodam do zero sem erro: DDL, depois DML (≥ 5 linhas por tabela), depois DQL |
| Data Science | Notebook roda do início ao fim ("Restart & Run All") sem erro |
| Dynamic Programming | `python -m pytest` em `dynamic-programming/` |
| Rede | Testes exigidos com prints: ping entre VLANs, DHCP, página por nome, `show ip nat translations`, acesso barrado pela ACL |
| Entrega | Item marcado no checklist só quando o artefato existe **e** foi conferido |

Não declare algo como pronto sem ter rodado a verificação correspondente.

## Ambiente local (Windows)

- Java: Microsoft OpenJDK 21 (`JAVA_HOME` do usuário).
- Oracle: **local por enquanto** (Docker), mas a entrega de DDD exige o **servidor Oracle da FIAP** e deploy no **render.com**. Planeje a troca por variáveis de ambiente.
- Frontend: tecnologia não definida.
