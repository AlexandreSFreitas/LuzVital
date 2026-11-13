---
name: fiap-agile
description: Use ao trabalhar na entrega de Agile Methodology da LuzVital — descrição do problema, personas, casos de uso, backlog, MoSCoW, Planning Poker, story points, MVP, protótipos de tela/UX ou a montagem do PDF único de entrega.
---

# fiap-agile

Apoia a entrega de **Agile Methodology With Squad Framework** da GS 2026.2. Rubrica completa em `docs/FIAP_REQUIREMENTS_CHECKLIST.md` (seção Agile).

## Antes de começar
1. Leia `docs/PROJECT_SPEC.md` e `docs/MVP_SCOPE.md`.
2. Confira o que já está marcado no checklist.

## Como produzir cada item

| Item (pontos) | Instrução |
|---|---|
| Apresentação da ideia (10) | Problema, foco, público-alvo e solução, **cada escolha justificada**. Use as seis perguntas do briefing |
| Personas (10) | Narrativa com nome fictício, contexto, rotina, dores, objetivos e relação com a energia/equipamentos. Mínimo: paciente ou cuidador, e um profissional de home care |
| Casos de uso (20) | **Escopo total**, não só o MVP. Todos os atores (paciente, familiar/cuidador, equipe de home care, operador/sistema). Gere em PlantUML ou Mermaid em `docs/diagrams/` para exportar como imagem |
| Backlog (20) | Histórias "Como <ator>, quero <ação>, para <benefício>", com critérios de aceite. Cada história ligada a um caso de uso. MoSCoW + story points (Fibonacci: 1, 2, 3, 5, 8, 13) com registro da rodada de Planning Poker. MVP destacado |
| Protótipo (20) | Mínimo 3 telas, cada uma com comentário de intenção e adequação de UX: legibilidade, contraste, linguagem simples, uso sob estresse (falta de energia), celular com pouca bateria |
| Vídeo pitch (20) | Use a Skill `documentary-pitch` |

## Regras
- Coerência entre itens vale nota: ator do diagrama ⇔ persona ⇔ história ⇔ tela.
- Planning Poker é da equipe: proponha estimativas como **sugestão**, nunca como resultado da votação.
- Entrega em **um único PDF**, com todos os integrantes identificados e o link do vídeo (YouTube não listado).

## Validação (antes de marcar no checklist)
- [ ] Cada história aponta para um caso de uso existente.
- [ ] Todo ator do diagrama aparece em pelo menos uma história.
- [ ] Toda história Must tem story points.
- [ ] As 3+ telas cobrem histórias do MVP.
- [ ] PDF único, sem links externos para o conteúdo.
