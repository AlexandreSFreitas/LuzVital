# 3. Diagrama de Casos de Uso — LuzVital

Item 3 da entrega de Agile Methodology (20 pontos). Representa o **escopo total** da solução, não só o MVP.

- Fonte do diagrama: [`../diagrams/casos_de_uso.puml`](../diagrams/casos_de_uso.puml) (PlantUML; abre no IntelliJ com o plugin PlantUML ou em plantuml.com)
- Imagem para o PDF: [`../diagrams/casos_de_uso.png`](../diagrams/casos_de_uso.png)

## Atores

| Ator | Tipo | Quem é | Persona |
|---|---|---|---|
| Paciente | Primário (beneficiário) | Pessoa eletrodependente em casa | Dona Lúcia |
| Contato de apoio | Primário | Familiar ou cuidador | Mariana |
| Equipe de home care | Primário | Profissional de saúde que acompanha o paciente | Rafael |
| Operador da central | Primário | Quem monitora o painel e coordena (pode ser alguém da equipe de home care) | Rafael |
| Administrador | Primário | Mantém os cadastros de apoio e os usuários | — |
| Simulador de interrupções | Secundário (sistema) | Gera interrupções fictícias no MVP | — |
| Distribuidora de energia | Secundário (externo, **futuro**) | Fonte oficial de interrupções, mediante acordo | — |
| Dispositivo de monitoramento | Secundário (externo, **futuro**) | Aparelho na tomada que envia sinais periódicos | — |
| Serviço de mensagens | Secundário (externo, **futuro**) | SMS/WhatsApp/e-mail para entregar alertas | — |

## Casos de uso

| ID | Caso de uso | Atores | Fase |
|---|---|---|---|
| UC01 | Cadastrar paciente (com endereço e região) | Equipe de home care | **MVP** |
| UC02 | Registrar consentimento do paciente ou responsável | Paciente, Equipe de home care | Futuro (Could) |
| UC03 | Gerenciar equipamentos do paciente e autonomia da bateria | Equipe de home care | **MVP** |
| UC04 | Gerenciar contatos de apoio e a ordem de acionamento | Equipe de home care | **MVP** |
| UC05 | Manter catálogo de equipamentos | Administrador | Should |
| UC06 | Manter regiões | Administrador | Should |
| UC07 | Registrar interrupção de energia | Operador, Simulador, Distribuidora (futuro) | **MVP** |
| UC08 | Identificar pacientes afetados | (incluído em UC07) | **MVP** |
| UC09 | Gerar alertas priorizados | (incluído em UC08) | **MVP** |
| UC10 | Receber alerta | Contato de apoio, Equipe de home care, Serviço de mensagens (futuro) | **MVP** (pela tela) |
| UC11 | Confirmar alerta | Contato de apoio, Equipe de home care | **MVP** |
| UC12 | Registrar ação de apoio | Contato de apoio, Equipe de home care, Operador | Should |
| UC13 | Acompanhar painel da interrupção | Operador | **MVP** |
| UC14 | Encerrar interrupção | Operador | **MVP** |
| UC15 | Consultar orientações de emergência (SAMU 192) | Paciente, Contato de apoio | Should (estende UC10) |
| UC16 | Escalar alerta sem resposta para o próximo contato | (estende UC09) | Could |
| UC17 | Enviar sinal de funcionamento | Dispositivo de monitoramento | Futuro |
| UC18 | Detectar ausência de sinal | (sistema; inclui UC07) | Futuro |
| UC19 | Consultar indicadores (tempo até confirmação) | Operador, Administrador | Could |
| UC20 | Autenticar-se | Todos os atores humanos, exceto o Paciente | Could |
| UC21 | Gerenciar usuários e perfis | Administrador | Could |

## Relacionamentos

- **UC07 «include» UC08 «include» UC09:** registrar uma interrupção sempre dispara o cruzamento e a geração de alertas.
- **UC01 «include» UC02:** o consentimento faz parte do cadastro quando estiver implementado.
- **UC15 «extend» UC10:** as orientações de emergência aparecem a partir do alerta.
- **UC16 «extend» UC09:** escalonamento quando o contato não responde.
- **UC18 «include» UC07:** no futuro, a ausência de sinal do dispositivo registra uma interrupção.

## Decisões

- O **Paciente** aparece como ator, mas só em casos de uso passivos ou opcionais (consentimento e orientações). A persona Dona Lúcia mostra que ele **não deve depender** do sistema para ser ajudado.
- **Operador** e **Equipe de home care** são atores separados porque fazem coisas diferentes, mesmo que a mesma pessoa (Rafael) faça os dois papéis.
- Os atores externos marcados como **futuro** aparecem para mostrar o escopo total. Nenhum deles é integrado no MVP.
