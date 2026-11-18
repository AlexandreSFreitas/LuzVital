# 1. Apresentação descritiva da ideia — LuzVital

> **"A energia pode acabar. O cuidado não."**

Item 1 da entrega de Agile Methodology (10 pontos). Fonte de verdade do texto que vai para o PDF único.

## 1.1 O problema

Na Grande São Paulo, faltas de energia longas se repetem. Em outubro de 2024, um temporal deixou **3,1 milhões** de unidades sem energia num único dia [1]. Em dezembro de 2025, um ciclone extratropical deixou **mais de 2 milhões** de consumidores sem energia por vários dias [2].

Para a maioria das pessoas, isso significa desconforto e prejuízo. Para quem **depende de um equipamento elétrico para respirar, se alimentar ou manter um tratamento em casa**, cada hora conta. Alguns casos noticiados:

- Um paciente de 68 anos com doença rara usa cilindro de oxigênio, respirador e sonda de alimentação, todos elétricos. A família teve que comprar um gerador depois de três dias sem energia [3].
- A filha de uma idosa que depende de aparelhos para respirar contou que a mãe estava no cadastro de "cliente vital" da distribuidora e, mesmo assim, não recebeu nenhum suporte [4].

**O que observamos:** a falta de energia em si não é o único problema. Também faltam respostas rápidas para três perguntas:

1. **Quem** foi afetado entre os pacientes que dependem de energia?
2. **Quem precisa de ajuda primeiro?** Isso depende da autonomia da bateria de cada um.
3. **Quem deve agir?** Família, cuidador ou equipe de home care, e se alguém já está cuidando.

Hoje essa informação fica espalhada em ligações, grupos de mensagem e na memória de cada cuidador.

## 1.2 Foco

Escolhemos atuar no **intervalo entre "a energia caiu" e "alguém responsável sabe e está agindo"**.

| O que **não** é o foco | Por quê |
|---|---|
| Restabelecer a energia | É responsabilidade da distribuidora. Ela já mantém um cadastro de clientes vitais com atendimento preferencial [5] |
| Atendimento médico ou triagem | É papel de profissionais de saúde e do SAMU 192. A LuzVital **não** substitui esses serviços |
| Fornecer equipamentos | Está fora do alcance de um software. A distribuição de kits de bateria aparece como **apoio à decisão** (Dynamic Programming), não como logística real |

**Justificativa:** o cadastro da distribuidora prioriza o **reparo da rede**, mas não mobiliza a **rede de apoio do paciente**. Essa lacuna pode ser atacada com software simples, dados que a própria família e a equipe de saúde já têm, e baixo custo.

## 1.3 Público-alvo

| Grupo | Papel | Justificativa |
|---|---|---|
| **Paciente eletrodependente** em casa (home care, "UTI em casa") | Beneficiário principal | É quem corre o risco |
| **Família e cuidadores** | Usuários que recebem e confirmam alertas | São os primeiros que podem agir: levar um gerador, trocar a bateria, remover o paciente |
| **Equipes de home care** | Usuários que cadastram pacientes e acompanham as ocorrências | Já conhecem os equipamentos e a autonomia de cada paciente |
| **Operador da central de monitoramento** | Acompanha o painel e coordena as ações | Concentra a visão de todos os afetados |

**Território de referência:** São Paulo, com foco no **Jardim Ângela (Zona Sul)**. Esse bairro foi o mais afetado da capital no desligamento de agosto de 2025 [6]. É um bairro periférico, onde a distância até os serviços aumenta o tempo de resposta. *(Proposta da equipe; os dados do sistema são simulados.)*

## 1.4 A solução

A **LuzVital** é uma plataforma web que funciona assim:

1. **Cadastro:** a equipe de home care registra o paciente com dados fictícios na versão acadêmica. O cadastro inclui a região, os equipamentos, a **autonomia da bateria** de cada um e os contatos de apoio em **ordem de acionamento**.
2. **Interrupção:** uma falta de energia numa região é registrada. No MVP, ela é **simulada** pelo operador. No futuro, a informação pode vir da distribuidora ou de um dispositivo na tomada do paciente.
3. **Cruzamento:** o sistema identifica os pacientes cadastrados naquela região.
4. **Alertas priorizados:** o sistema cria alertas para os contatos de cada paciente. A ordem segue uma **regra operacional** (equipamento de suporte à vida e autonomia menor que a duração estimada) que **não** é um índice clínico.
5. **Confirmação:** o contato confirma que recebeu o alerta e registra o que fez. A tela sempre lembra: em emergência médica, ligue **192 (SAMU)**.
6. **Acompanhamento:** o operador vê no painel quem confirmou, quem ainda não respondeu e quais ações já foram tomadas, até encerrar a interrupção.

**Proposta de valor:** diminuir o tempo entre a falta de energia e o momento em que alguém responsável sabe que um paciente vulnerável pode precisar de ajuda.

## 1.5 As seis perguntas do briefing

| Pergunta | Resposta |
|---|---|
| Quem é o cidadão beneficiado? | O paciente eletrodependente em casa e sua rede de apoio (família, cuidadores e equipe de home care) |
| Qual problema será resolvido? | A demora para saber quem foi afetado por uma falta de energia, quem precisa de ajuda primeiro e quem deve agir |
| Como a solução funcionará? | Cadastro, registro da interrupção por região, cruzamento com os pacientes, alertas priorizados, confirmação e acompanhamento |
| Quais tecnologias serão empregadas? | API REST em Java/Spring Boot com Oracle; telas web; Python para análise de dados (regressões) e para a distribuição de kits (programação dinâmica); rede da central projetada no Cisco Packet Tracer; vídeo 3D da casa do paciente |
| Quem participará do ecossistema? | Pacientes, famílias, cuidadores, empresas de home care e a central de monitoramento. No futuro: distribuidoras de energia, fabricantes de dispositivos e serviços de saúde, mediante acordos formais |
| Como o impacto poderá ser medido e ampliado? | **Indicador principal:** tempo entre a interrupção e a primeira confirmação de um responsável. **Secundário:** % de alertas confirmados antes de a bateria acabar. Para ampliar: integração com dados oficiais de interrupção e um dispositivo de monitoramento na tomada |

## 1.6 ODS conectados

| ODS | Contribuição |
|---|---|
| **3 — Saúde e bem-estar** | Reduz o risco de interrupção de tratamentos que sustentam a vida em casa |
| **9 — Indústria, inovação e infraestrutura** | Usa informação sobre a infraestrutura elétrica para proteger pessoas e pensa uma infraestrutura mais resiliente |
| **10 — Redução das desigualdades** | Prioriza pessoas com deficiência e doenças crônicas, mais expostas a falhas de infraestrutura, começando por um bairro periférico |
| **11 — Cidades e comunidades sustentáveis** | Torna a resposta a eventos climáticos urbanos (temporais e apagões) mais rápida e coordenada |

## 1.7 Limites e cuidados

- **Não é serviço de emergência.** A plataforma registra, avisa e orienta a ligar para o 192. Ela não despacha ambulâncias nem decide para qual hospital levar o paciente.
- **Dados de saúde são dados pessoais sensíveis (LGPD).** Por isso usamos minimização: só o essencial para quem vai ajudar. Tudo no projeto acadêmico é **fictício**.
- **Integrações reais (distribuidora, SMS, dispositivo IoT) são futuras.** No MVP elas são simuladas, e isso é dito claramente.

## 1.8 Escuta (etapa "Escutar" do briefing)

A escuta foi feita a partir de depoimentos públicos de quem convive com o problema, usados com crédito e, no caso do documentário, com autorização da ONG produtora:

- **Documentário "De Volta para Casa (Back Home)":** mostra o cotidiano do tratamento domiciliar, com equipes de saúde chegando às casas e pacientes que dependem de concentradores de oxigênio e outros aparelhos. Um paciente conta que o alto consumo de energia dos aparelhos torna o tratamento dispendioso para a família.
- **Vídeo "UTI Domiciliar" (CPFL Energia / RGE):** uma senhora relata que precisa de oxigênio em casa durante 16 horas por dia e que o aparelho gasta bastante energia.
- **Reportagens (JA 2ª Edição, Jornal Nacional, R7):** relatam famílias que ficaram horas sem energia com parentes dependentes de aparelhos, e o caso de uma bebê de 11 meses que morreu depois de ficar cerca de 15 horas sem energia em casa.

**O que a escuta confirmou:**
1. A dependência é contínua: são muitas horas por dia ligado à tomada, e o custo da energia já pesa.
2. Quando falta energia, a família improvisa sozinha (gerador, bateria do carro, energia do vizinho) e nem sempre sabe se alguém já está ajudando.
3. Existe uma rede de cuidado (família, cuidadores, equipe de home care), mas ela não é avisada de forma organizada.

Esses três pontos sustentam as personas (Mariana não sabe quem já está indo; Rafael não sabe quais pacientes foram afetados) e as histórias Must do backlog.

## Fontes

1. eixos — crise de energia em SP após temporal de 11/10/2024: https://eixos.com.br/?p=314604
2. VIVA — "O abandono de quem depende de energia elétrica para viver" (19/12/2025): https://viva.com.br/cidadania-e-direitos/o-abandono-de-quem-depende-de-energia-eletrica-para-viver.html
3. SBT News — família compra gerador para manter idoso vivo após três dias sem energia: https://sbtnews.sbt.com.br/noticia/brasil/familia-tem-que-comprar-gerador-para-manter-idoso-vivo-apos-tres-dias-sem-energia
4. Band — "Mulher se revolta com falta de luz em SP" (12/12/2025): https://www.band.com.br/noticias/brasil-urgente/ultimas/mulher-se-revolta-com-falta-de-luz-em-sp-nao-tem-nenhum-suporte-202512121839
5. VIVA (mesma reportagem do item 2) — resposta da Enel sobre o cadastro de clientes vitais
6. BandNews FM — desligamento de 28/08/2025, Jardim Ângela como bairro mais afetado: https://www.band.com.br/bandnews-fm/noticias/apagao-sp-202508280636
7. Documentário "De Volta para Casa (Back Home)" (YouTube), trechos usados com autorização
8. CPFL Energia / RGE — vídeo "UTI Domiciliar: um projeto que transformou centenas de vidas" (YouTube)
