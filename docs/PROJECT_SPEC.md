# Especificação do projeto — LuzVital

## Problema

Pacientes que dependem continuamente de equipamentos elétricos em casa (concentradores de oxigênio, ventiladores pulmonares, bombas de alimentação e outros) correm risco quando falta energia. O problema não é só a falta de energia: é a demora para saber **quem** foi afetado, **quem precisa de ajuda** e **quem deve agir**.

## Cidadão beneficiado

- **Paciente eletrodependente** em atendimento domiciliar.
- **Rede de apoio:** familiares, cuidadores, responsáveis.
- **Equipes de saúde:** home care e equipes de referência.

## Proposta de valor

Diminuir o tempo entre a identificação de uma interrupção de energia e o conhecimento de que um paciente vulnerável pode precisar de ajuda.

## Funcionalidades (escopo total)

1. Cadastrar pacientes eletrodependentes.
2. Registrar endereço, região e informações essenciais para o atendimento.
3. Registrar os equipamentos médicos e suas necessidades de energia.
4. Registrar a autonomia estimada das baterias e fontes alternativas.
5. Cadastrar familiares, cuidadores, responsáveis e equipes de home care.
6. Registrar interrupções de energia por região.
7. Cruzar a interrupção com os pacientes cadastrados na região.
8. Gerar alertas para os contatos associados ao paciente.
9. Acompanhar o reconhecimento e a confirmação dos alertas.
10. Registrar ocorrências e o andamento das ações de apoio.

O recorte do MVP está em `MVP_SCOPE.md`.

## As seis perguntas do briefing

| Pergunta | Resposta |
|---|---|
| Quem é o cidadão beneficiado? | Paciente eletrodependente em casa e sua rede de apoio |
| Qual problema será resolvido? | Demora para identificar e mobilizar ajuda quando falta energia |
| Como a solução funcionará? | Cadastro + registro de interrupção por região + cruzamento + alertas com confirmação |
| Quais tecnologias? | Java/Spring Boot, Oracle, Python (análise e algoritmo), rede projetada no Packet Tracer, frontend a definir |
| Quem participa do ecossistema? | Pacientes, familiares, cuidadores, equipes de home care; futuramente distribuidoras de energia e serviços de emergência |
| Como medir e ampliar o impacto? | Tempo até a confirmação do alerta; % de alertas confirmados dentro da autonomia da bateria |

## ODS (proposta — validar com a equipe)

| ODS | Como a LuzVital contribui |
|---|---|
| 3 — Saúde e bem-estar | Reduz o risco de interrupção de tratamentos que sustentam a vida |
| 9 — Indústria, inovação e infraestrutura | Usa dados de infraestrutura elétrica para proteger pessoas |
| 10 — Redução das desigualdades | Prioriza pessoas com deficiência e doenças crônicas, mais vulneráveis a falhas de infraestrutura |
| 11 — Cidades e comunidades sustentáveis | Torna a resposta a emergências urbanas mais rápida e coordenada |

## Pendências da equipe

- [ ] Cidade e bairro de referência.
- [ ] Pessoa real entrevistada (sem expor dados pessoais).
- [ ] Meta do indicador de impacto.
