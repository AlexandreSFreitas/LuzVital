# Checklist de requisitos FIAP — GS 2026.2 (CitizenTech)

Fonte: "GS CitizenTech - 2ES Fev - FIAP 2026.pdf". **Entrega de todas as disciplinas: 19/11/2026, até 23h55.** Um envio por equipe em cada disciplina.

Marque `[x]` somente quando o artefato existir **e** tiver sido conferido.

## Comum a todas

- [ ] Ficha da CitizenTech no início do `README.md` (nome, cidade e bairro, cidadão, problema em uma frase, como funciona, o que cada parte faz, link do repositório, indicador de impacto, ODS)
- [ ] ODS identificados **e** explicado como a solução contribui para eles (obrigatório)
- [ ] `prompts.md` com os prompts de IA usados
- [ ] Nenhum dado pessoal real; fontes dos dados indicadas
- [ ] Todos os integrantes identificados (nome e RM) em cada entrega
- [ ] Conversa com uma pessoa real que convive com o problema (registrada) — decisão: depoimentos do documentário "De Volta para Casa" + contato com a ONG (ver `docs/agile/01_IDEIA.md`)

## Agile Methodology With Squad Framework — PDF único (+ link do vídeo)

- [x] 1. Apresentação descritiva da ideia: problema, foco, público-alvo e solução, com justificativas (10)
- [x] 2. Persona(s) com descrição narrativa (10)
- [x] 3. Diagrama de Casos de Uso com o escopo total e todos os atores (20)
- [ ] 4. Backlog com histórias coerentes com o diagrama, MoSCoW, Story Points por Planning Poker e destaque do MVP (20)
- [x] 5. Protótipo de no mínimo 3 telas, com comentários sobre a intenção e a UX (20)
- [x] 6. Vídeo pitch de até 3 min, ilustrado, com narração da equipe, no YouTube como **não listado** (20)
- [ ] Tudo em **um único PDF** (`python disciplines/agile/montar_pdf.py`; falta só o Planning Poker) (mais de um PDF ou link externo = −10 pontos)
- [ ] Link do vídeo testado em janela anônima (inacessível = zero no item)

## AR-VR Modelling And Simulation

- [ ] Vídeo de **30 a 60 segundos** no YouTube, tema "CitizenTech", representando a LuzVital em 3D/imersivo
- [ ] PDF com nomes de todos os integrantes e o link do vídeo

## Data Science & Statistical Computing — ZIP

- [ ] Contexto, perguntas e variáveis-alvo definidas (1,0)
- [ ] Preparação dos dados e divisão treino/teste **sem vazamento** (2,0)
- [ ] Regressão linear com MAE, RMSE, R² e interpretação (2,0)
- [ ] Regressão logística com matriz de confusão, precisão, recall e F1 (2,0)
- [ ] Recomendações de ação baseadas nas previsões, com limitações e impactos (3,0)
- [ ] ZIP com: notebook `.ipynb` **executado**, CSV (ou link) com a fonte indicada, TXT com nomes e RMs

## Database Design — PDF + scripts `.sql`

- [ ] PDF: capa (integrantes em ordem alfabética, RM, nome da equipe e da solução), sumário, objetivo e escopo, principais funcionalidades (10)
- [ ] PDF: diagrama do modelo lógico no **Oracle Data Modeler** com tabelas, atributos, PKs, FKs, relacionamentos e cardinalidades (20)
- [x] `ddl.sql`: CREATE/ALTER com todas as tabelas e constraints (20)
- [x] `dml.sql`: INSERTs com **no mínimo 5 linhas por tabela** (exceções justificadas) (20)
- [x] `dql.sql`: 3 consultas (30)
  - [x] INNER JOIN com duas tabelas
  - [x] INNER JOIN com função de grupo e GROUP BY
  - [x] LEFT OUTER JOIN com WHERE e ORDER BY
- [ ] Sem links para diagramas em nuvem

> 13/11: scripts rodados do zero no Oracle da FIAP sem erro (9 tabelas, 9 PK, 9 FK, 4 UNIQUE; 5 a 11 linhas por tabela; DQL com 6, 7 e 11 linhas). Diagrama exportado em `database/luzvital_logico.png` (falta colocar no PDF).

## Domain Driven Design - Java — ZIP pelo Portal do Aluno

Documentação (PDF único, 30 pontos):
- [ ] Capa (projeto, nome completo e RM), índice, descritivo, justificativa e objetivos (5)
- [ ] Diagrama de classes fiel ao código Java (10)
- [ ] Protótipos de tela, tabela de endpoints (GET, POST, PUT, DELETE) e DER (10)
- [ ] Instruções de execução: ferramentas, versões (JDK 21, Oracle), link do GitHub, link do deploy, passo a passo (5)

Parte técnica (70 pontos):
- [ ] Camada model alinhada ao banco (**servidor Oracle da FIAP**) (10) — em andamento: 7 de 9 tabelas no `model` (faltam CONTATO e ACAO_APOIO); leitura e gravação conferidas no Oracle da FIAP em 15/11
- [ ] Camadas DAO e BO (10) — em andamento: regiões, pacientes e registro de interrupção (conferidos no Oracle da FIAP em 15/11)
- [ ] Controller com GET, POST, PUT e DELETE (10) — em andamento: `/regioes` e `/pacientes` completos
- [x] Tratamento de exceções (10) — `GlobalExceptionHandler`, conferido por testes e pela API rodando (14/11)
- [ ] Deploy no **render.com** funcionando (30)
- [ ] ZIP com PDF, link do GitHub e link do deploy
- [ ] ⚠️ **Nenhum commit depois do prazo** (zera a parte técnica)

## Dynamic Programming — ZIP

- [ ] Algoritmo em Python com memoização, tabulação e/ou grafos, resolvendo uma necessidade da LuzVital
- [ ] Escolha do algoritmo justificada, funcionamento correto e noção de eficiência
- [ ] README com nomes e RMs, descrição dos algoritmos e das funcionalidades
- [ ] ZIP com código-fonte completo e README

## Network Architect Solutions — `.pkt` + PDF

- [ ] Faixa 192.168.X.0/24 (X = número da equipe) em pelo menos 3 sub-redes: Equipe, Cidadão (Wi-Fi público), Servidores/Sensores
- [ ] Uma VLAN por setor, trunk 802.1Q, router-on-a-stick
- [ ] DHCP com um pool por VLAN, excluindo gateway e servidor
- [ ] NAT/PAT até um roteador provedor com servidor externo simulando a internet
- [ ] Servidor da solução com DNS e HTTP (página com a Ficha da CitizenTech)
- [ ] ACL estendida: Wi-Fi do cidadão só acessa HTTP e DNS do servidor e a internet, nada da VLAN Equipe
- [ ] Roteador só por SSH, com senhas e `enable secret`; Wi-Fi com WPA2
- [ ] PDF: Ficha, topologia, plano de endereçamento, trechos de `show running-config`
- [ ] Prints: ping entre VLANs, DHCP, página aberta pelo nome, `show ip nat translations`, acesso barrado pela ACL

## Pitch (Testing)

- [ ] Vídeo de até 3 minutos no YouTube com a solução e as entregas que mais somaram; link enviado
