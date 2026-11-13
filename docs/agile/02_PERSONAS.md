# 2. Personas — LuzVital

Item 2 da entrega de Agile Methodology (10 pontos).

> As personas são **fictícias**. Foram construídas a partir de situações relatadas em reportagens públicas (ver `01_IDEIA.md`, fontes 3 a 5) e devem ser ajustadas depois da conversa com uma pessoa real.

Cada persona corresponde a um ator do diagrama de casos de uso:

| Persona | Ator no diagrama |
|---|---|
| Dona Lúcia | Paciente |
| Mariana | Contato de apoio (familiar/cuidador) |
| Rafael | Equipe de home care **e** Operador da central |

---

## Persona 1 — Dona Lúcia Andrade, 71 anos (Paciente)

**Onde vive:** casa térrea no Jardim Ângela, Zona Sul de São Paulo. Mora com a filha, o genro e um neto adolescente.

**Saúde e equipamentos:** tem doença pulmonar crônica e usa um **concentrador de oxigênio** quase 24 horas por dia. O aparelho é ligado na tomada. Como reserva, tem um cilindro pequeno de oxigênio que dura **cerca de 3 horas**. É acompanhada por uma empresa de home care com visitas semanais.

**Relação com a tecnologia:** usa o celular para ligar e mandar áudio pelo WhatsApp. Tem dificuldade para ler letras pequenas.

**Rotina:** passa a maior parte do dia em casa. Durante a semana, fica sozinha entre 7h e 18h enquanto a família trabalha e estuda. Uma vizinha passa para vê-la na hora do almoço.

**Dores:**
- *"Quando a luz cai, eu ligo o cilindro, mas fico contando o tempo."*
- Não sabe se a família ficou sabendo da queda.
- Fica ansiosa ao imaginar que precisaria pedir ajuda e o celular estaria descarregado.

**Objetivos:**
- Ter a certeza de que, se a energia cair, alguém vai saber e vir ajudar antes que o oxigênio de reserva acabe.
- Não precisar mexer em nenhum aplicativo complicado.

**O que a LuzVital faz por ela:** Dona Lúcia **não precisa operar nada**. O alerta vai para a filha e para a equipe dela. *(Isso define uma decisão de UX: o paciente é beneficiário, não operador.)*

---

## Persona 2 — Mariana Andrade, 42 anos (Contato de apoio: filha e cuidadora principal)

**Onde vive e trabalha:** mora com a mãe. É auxiliar administrativa numa empresa no centro e leva cerca de **1h30 de ônibus** para chegar em casa.

**Relação com a tecnologia:** celular Android de entrada, com plano de dados limitado. Usa WhatsApp e alguns aplicativos de banco. Não tem tempo para aprender ferramentas complexas.

**Rotina:** sai às 6h30 e volta às 19h. Deixa o celular no bolso, muitas vezes no modo silencioso durante reuniões.

**Dores:**
- *"No último apagão, eu só fiquei sabendo à tarde, porque a vizinha mandou mensagem."*
- Não sabe se a distribuidora vai priorizar o bairro dela, mesmo com a mãe no cadastro de cliente vital.
- Quando a luz cai, liga para o irmão, para a vizinha e para a home care, e ninguém sabe quem já está indo.

**Objetivos:**
- Saber **na hora** que a energia caiu na casa da mãe.
- Avisar com um toque "estou ciente, estou indo" para que os outros saibam.
- Ver quanto tempo a mãe ainda tem de oxigênio de reserva.

**Frustrações com soluções existentes:** grupos de família ficam cheios de mensagens e ninguém sabe quem assumiu. Os aplicativos da distribuidora informam a falta de luz, mas não avisam a família.

**O que a LuzVital faz por ela:** um alerta claro com o nome da mãe, a autonomia estimada e um **botão grande "Confirmar que vou ajudar"**. Depois que ela confirma, os outros contatos e a equipe veem que alguém assumiu.

---

## Persona 3 — Rafael Souza, 35 anos (Enfermeiro coordenador de home care / operador da central)

**Onde trabalha:** coordena a equipe de uma empresa de home care que acompanha **28 pacientes** na Zona Sul. Trabalha numa pequena **central de monitoramento** com dois colegas. *(Esse espaço físico é a rede projetada em Network Architect Solutions.)*

**Relação com a tecnologia:** usa computador o dia todo e está acostumado com sistemas de prontuário e planilhas.

**Rotina:** organiza visitas, responde famílias e resolve intercorrências. Em dias de temporal, o telefone não para.

**Dores:**
- *"Num apagão grande, eu preciso descobrir sozinho quais dos meus 28 pacientes estão sem energia."*
- Não tem uma lista de quem usa equipamento de suporte à vida **e** tem pouca bateria.
- Não sabe se a família já foi avisada e se alguém está a caminho.
- Registra tudo depois, de memória.

**Objetivos:**
- Ver num **painel** todos os pacientes afetados, ordenados por prioridade.
- Saber quais alertas foram confirmados e quais estão sem resposta.
- Registrar as ações (contato feito, deslocamento, orientação para ligar no 192) para ter histórico.
- Manter o cadastro dos pacientes, dos equipamentos e dos contatos atualizado.

**O que a LuzVital faz por ele:** cadastro organizado, um painel único da interrupção e o histórico das ações. Ele também mede o **tempo até a confirmação**, que é o indicador de impacto do projeto.

---

## Como as personas guiam o produto

| Necessidade | Persona | Onde aparece |
|---|---|---|
| Saber rápido quem foi afetado | Rafael | UC08 e a tela "Painel da interrupção" |
| Ser avisada e avisar que assumiu | Mariana | UC10 e UC11, tela "Alerta" |
| Não precisar operar nada | Dona Lúcia | Decisão de UX: o paciente não é usuário obrigatório |
| Ver a autonomia restante | Mariana e Rafael | Campo de autonomia em `PACIENTE_EQUIPAMENTO` |
| Ter histórico das ações | Rafael | UC12, tabela `ACAO_APOIO` |
