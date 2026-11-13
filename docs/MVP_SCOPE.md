# Escopo do MVP — LuzVital

**Status:** proposta inicial. Será confirmada no backlog priorizado por MoSCoW (Skill `fiap-agile`).

Prazo: 19/11/2026. Regra da GS: *"Comecem pequeno: uma solução simples que funciona vale mais que uma ideia enorme pela metade."*

## Must (MVP)

- CRUD de **paciente** (dados simulados), com região.
- CRUD de **equipamento** do paciente, com consumo e autonomia de bateria.
- CRUD de **contato** de apoio (familiar, cuidador, equipe).
- Registro de **interrupção de energia** por região.
- **Alerta** gerado para os contatos dos pacientes da região afetada.
- **Confirmação** do alerta por um contato.

## Should

- Priorizar alertas pela menor autonomia de bateria restante.
- Histórico de ocorrências e ações de apoio.

## Could

- Notificação real (SMS, WhatsApp, e-mail).
- Integração com dados públicos de interrupções da distribuidora.

## Won't (nesta GS)

- Dados reais de pacientes.
- Integração com prontuário eletrônico.
- Aplicativo móvel nativo.
