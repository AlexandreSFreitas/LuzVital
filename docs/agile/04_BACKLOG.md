# 4. Backlog do Produto — LuzVital

Item 4 da entrega de Agile Methodology (20 pontos).

- **Priorização:** MoSCoW (**M**ust, **S**hould, **C**ould, **W**on't nesta GS).
- **MVP = todas as histórias Must.** São elas que o backend Java e o banco implementam até 19/11.
- **Estimativa:** Story Points na escala Fibonacci (1, 2, 3, 5, 8, 13), com Planning Poker.

## 4.1 Critérios de estimativa

Story Points medem **esforço relativo** (complexidade, volume e incerteza), não horas.

**História de referência:** US01 (cadastrar paciente) = **3 pontos**. É um CRUD de uma tabela com uma FK, validações simples e um endpoint por verbo HTTP. As outras histórias foram comparadas com ela.

| Fator | Aumenta a estimativa quando… |
|---|---|
| Tabelas envolvidas | A história mexe em mais de uma tabela ou numa associativa (N:N) |
| Regra de negócio | Existe uma decisão do sistema (cruzar, priorizar, mudar status) e não só gravar e ler |
| Interface | Precisa de uma tela nova além da API |
| Integração ou incerteza | Depende de serviço externo, hardware ou algo que a equipe nunca fez |

| Pontos | Significado para a equipe |
|---|---|
| 1 | Ajuste pequeno, sem tabela nova |
| 2 | Uma operação simples numa tabela existente |
| 3 | CRUD de uma tabela (referência) |
| 5 | CRUD com associativa, ou regra de negócio simples envolvendo 2 a 3 tabelas |
| 8 | Regra de negócio central envolvendo várias tabelas, ou integração externa conhecida |
| 13 | Muita incerteza (hardware, parceiro externo). Deve ser quebrada antes de entrar numa sprint |

## 4.2 Histórias de usuário

### Must — MVP

| ID | História | UC | Critérios de aceite | SP |
|---|---|---|---|---|
| US01 | **Como** equipe de home care, **quero** cadastrar um paciente com endereço e região, **para** que ele seja encontrado quando faltar energia naquela região | UC01 | Nome, nascimento, endereço, CEP e região são obrigatórios; a região precisa existir; é possível listar, consultar, atualizar e desativar o paciente | **3** |
| US02 | **Como** equipe de home care, **quero** registrar os equipamentos do paciente e a autonomia da bateria de cada um, **para** saber quanto tempo ele aguenta sem energia | UC03 | O equipamento vem do catálogo; a autonomia em minutos é ≥ 0 (0 = sem bateria); um paciente pode ter vários equipamentos | **3** |
| US03 | **Como** equipe de home care, **quero** cadastrar contatos de apoio e definir a ordem de acionamento de cada paciente, **para** que as pessoas certas sejam avisadas | UC04 | O tipo do contato é FAMILIAR, CUIDADOR ou EQUIPE_SAUDE; um contato pode apoiar vários pacientes; não há ordem repetida para o mesmo paciente | **5** |
| US04 | **Como** operador da central, **quero** registrar uma interrupção de energia (simulada) numa região, **para** iniciar o atendimento | UC07 | Região e início são obrigatórios; a origem é registrada como SIMULADA ou MANUAL; o status começa como ABERTA | **3** |
| US05 | **Como** operador da central, **quero** que, ao registrar a interrupção, o sistema identifique os pacientes ativos da região e gere um alerta para cada contato deles, **para** não precisar descobrir isso manualmente | UC08, UC09 | Só pacientes ativos da região; um alerta por par paciente–contato; não duplica alertas se o processo rodar de novo; a resposta informa quantos pacientes e alertas foram gerados | **8** |
| US06 | **Como** operador da central, **quero** que os alertas tenham prioridade 1 a 3 segundo a regra operacional documentada, **para** atender primeiro quem tem menos autonomia | UC09 | Regra de `DATABASE_MODEL.md` §4; prioridade 1 quando há equipamento de suporte à vida com autonomia menor que a duração estimada; documentado como regra **não clínica** | **3** |
| US07 | **Como** contato de apoio, **quero** confirmar que recebi o alerta, **para** que os outros saibam que alguém assumiu | UC10, UC11 | O status muda de PENDENTE para CONFIRMADO com data e hora; não é possível confirmar duas vezes; confirmar um alerta inexistente devolve 404 | **2** |
| US08 | **Como** operador da central, **quero** ver os alertas de uma interrupção ordenados por prioridade e status, **para** acompanhar quem ainda não respondeu | UC13 | Lista com paciente, contato, prioridade, status e horário; filtro por status | **3** |
| US09 | **Como** operador da central, **quero** encerrar uma interrupção, **para** registrar que a energia voltou | UC14 | Exige data de fim ≥ início; status ENCERRADA; não aceita encerrar duas vezes | **2** |
| US10 | **Como** usuário da API, **quero** mensagens de erro claras e padronizadas, **para** entender o que corrigir | Transversal | Erros 400/404/409 no formato de `API_CONTRACT.md`; nunca mostra stack trace nem SQL | **3** |

**Total do MVP: 35 pontos.**

### Should

| ID | História | UC | Critérios de aceite | SP |
|---|---|---|---|---|
| US11 | **Como** contato de apoio ou equipe, **quero** registrar o que fiz depois do alerta, **para** que haja histórico do atendimento | UC12 | Tipo da ação a partir de uma lista; descrição obrigatória; data automática | **3** |
| US12 | **Como** contato de apoio, **quero** ver na tela do alerta a orientação de ligar para o 192 em emergência médica, **para** saber o que fazer | UC15 | Texto fixo e visível, com o número 192 como link de discagem | **1** |
| US13 | **Como** operador da central, **quero** um painel web da interrupção, **para** acompanhar tudo numa tela | UC13 | Mostra contadores (pendentes/confirmados) e a lista da US08; funciona em notebook e celular | **5** |
| US14 | **Como** administrador, **quero** manter o catálogo de equipamentos, **para** padronizar o cadastro | UC05 | CRUD; não remove equipamento em uso | **2** |
| US15 | **Como** administrador, **quero** manter as regiões, **para** organizar o cruzamento | UC06 | CRUD; nome único por cidade; não remove região com pacientes | **2** |

### Could

| ID | História | UC | SP |
|---|---|---|---|
| US16 | **Como** operador, **quero** que um alerta sem resposta em X minutos seja marcado SEM_RESPOSTA e o próximo contato seja acionado, **para** não depender de uma única pessoa | UC16 | **5** |
| US17 | **Como** operador, **quero** ver o tempo médio entre a interrupção e a primeira confirmação, **para** medir o impacto | UC19 | **5** |
| US18 | **Como** paciente ou responsável, **quero** registrar meu consentimento para o uso dos meus dados, **para** que o tratamento siga a LGPD | UC02 | **3** |
| US19 | **Como** usuário, **quero** entrar com login e ver só o que meu perfil permite, **para** proteger os dados dos pacientes | UC20, UC21 | **8** |
| US20 | **Como** contato de apoio, **quero** receber o alerta por SMS ou WhatsApp, **para** ser avisado mesmo sem abrir o sistema | UC10 | **8** |

### Won't (futuro)

| ID | História | UC | Por que não agora |
|---|---|---|---|
| US21 | **Como** sistema, **quero** receber sinais periódicos de um dispositivo na tomada e detectar a ausência de sinal, **para** identificar uma possível falta de energia na casa | UC17, UC18 | Exige hardware, avaliação elétrica e de segurança, e comunicação independente do Wi-Fi. Só pode ser **simulado** (13) |
| US22 | **Como** sistema, **quero** receber interrupções da distribuidora, **para** não depender de registro manual | UC07 | Não há API pública confirmada; depende de acordo formal. Não fazer scraping (13) |
| US23 | **Como** central, **quero** integração formal com serviços de emergência | — | Depende de autorização e acordos institucionais |

## 4.3 Registro do Planning Poker

**Como foi feito:** cada história foi comparada com a história de referência (US01 = 3 pontos), usando os fatores da seção 4.1, na escala Fibonacci. Nas histórias em que houve dúvida entre dois valores, valeu o maior, porque a equipe ainda está aprendendo as tecnologias. A rodada foi feita com apoio de IA, conforme a regra "IA como copiloto" da GS e o registro em `prompts.md`.

| ID | História (resumo) | Valores em discussão | **Consenso** | Por quê |
|---|---|---|---|---|
| US01 | Cadastrar paciente | 3 | **3** | Referência: CRUD de uma tabela com uma FK |
| US02 | Equipamentos e autonomia da bateria | 2 ou 3 | **3** | Usa o catálogo e uma tabela de ligação, mas a regra é simples |
| US03 | Contatos e ordem de acionamento | 3 ou 5 | **5** | Relação N:N com ordem que não pode se repetir por paciente |
| US04 | Registrar interrupção simulada | 2 ou 3 | **3** | Uma tabela, mas com status e origem validados |
| US05 | Cruzar região e gerar alertas | 8 ou 13 | **8** | Regra central com várias tabelas e transação; não é 13 porque não depende de nada externo |
| US06 | Prioridade dos alertas | 3 ou 5 | **3** | A regra está documentada; é um cálculo sobre dados que a US05 já carrega |
| US07 | Confirmar alerta | 2 | **2** | Muda um status e grava a data, com duas validações |
| US08 | Listar alertas por prioridade | 2 ou 3 | **3** | Consulta com junção e filtro por status |
| US09 | Encerrar interrupção | 1 ou 2 | **2** | Uma operação com duas validações (data e status) |
| US10 | Erros padronizados | 3 | **3** | Handler global e exceções de domínio usadas por todas as histórias |
| US11 | Registrar ação de apoio | 3 | **3** | CRUD de uma tabela ligada ao alerta |
| US12 | Orientação SAMU 192 | 1 | **1** | Texto fixo na tela |
| US13 | Painel web da interrupção | 5 | **5** | Tela nova que consome a API e precisa funcionar no celular |
| US14 | Catálogo de equipamentos | 2 | **2** | CRUD simples com uma restrição de exclusão |
| US15 | Regiões | 2 | **2** | CRUD simples com nome único |
| US16 | Escalar alerta sem resposta | 5 | **5** | Precisa de controle de tempo e de mudança de status em lote |
| US17 | Tempo até a primeira confirmação | 3 ou 5 | **5** | Consulta agregada e definição clara do indicador |
| US18 | Consentimento LGPD | 3 | **3** | Uma tabela e um texto revisado |
| US19 | Login e perfis | 8 | **8** | Autenticação e autorização em todas as rotas |
| US20 | Alerta por SMS ou WhatsApp | 8 | **8** | Integração externa, custo e cadastro no provedor |

Histórias Won't (futuro) (US21 a US23) não foram estimadas, porque dependem de hardware ou de acordos externos.

## 4.4 Rastreabilidade

| Ator | Histórias |
|---|---|
| Equipe de home care | US01, US02, US03, US07, US11 |
| Operador da central | US04, US05, US06, US08, US09, US13, US16, US17 |
| Contato de apoio | US07, US11, US12, US20 |
| Administrador | US14, US15, US19 |
| Paciente | US18 |
| Simulador / Distribuidora / Dispositivo / Serviço de mensagens | US04 (simulador), US22, US21, US20 |

Todos os casos de uso de `03_CASOS_DE_USO.md` têm pelo menos uma história (UC20 e UC21 estão juntos na US19).
