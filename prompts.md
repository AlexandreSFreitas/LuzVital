# Registro de prompts (IA como copiloto)

Exigência da GS: registrar os prompts usados e saber explicar cada linha do que foi produzido.

| Data | Disciplina | Prompt (resumo) | Para que foi usado | O que a equipe revisou ou mudou |
|---|---|---|---|---|
| 13/11/2026 | Agile | "Começar por Agile" (cidade: São Paulo; protótipo em telas HTML) | Ideia com fontes públicas, 3 personas, casos de uso (escopo total), backlog MoSCoW com sugestão de story points, 3 telas HTML com comentários de UX em `docs/agile/` e `frontend/prototipo/` | _a preencher (Planning Poker real da equipe)_ |
| 15/11/2026 | Agile / DDD (frontend) | Briefing "Desenvolvimento do frontend — LuzVital" + 3 imagens de inspiração (landing, logo de sol, painel) | Site em HTML/CSS/JS puro: logo e ilustrações SVG próprias, 10 seções, demonstração interativa com a regra de prioridade, acessibilidade e testes automatizados em 7 larguras | _a preencher_ |
| 15/11/2026 | Agile (pitch) | Direção do pitch: tom documental e sentimental, abertura com o caso da bebê que ficou 15h sem energia, montagem com trechos do documentário e depois a solução | Roteiro com tempos e narração, storyboard, controle de autorizações e script que confere a duração (`pitch/`) | _a preencher_ |
| 16/11/2026 | Agile (pitch) | Cortes dos vídeos (documentário, JA2, JN, R7, CPFL/RGE, site), tratamento das narrações e "crie o som do aparelho e uma música dramática com altos e baixos conforme o vídeo" | Clipes com ffmpeg; trilha e som do aparelho gerados por síntese (`pitch/trilha/gerar_trilha.py`), com a dinâmica ligada ao roteiro | _a preencher_ |
| 17/11/2026 | Agile (pitch) | "Remova o áudio do bebê e edite o vídeo pitch com as cenas, a trilha, cards, legendas e efeitos" | Script `pitch/montagem/montar_pitch.py` (ffmpeg + Pillow) que monta o vídeo de 2:51,9 com créditos por cena, legendas da narração, cartões e mixagem | _a preencher_ |
| 18/11/2026 | Agile | "Mude as telas de Agile e monte o PDF" (link do vídeo e do site) | Telas do site real no protótipo, escuta registrada, diagrama de casos de uso redesenhado, item 6 do pitch e script que gera o PDF único | _a preencher_ |
| 18/11/2026 | Agile | "Faça o Planning Poker por você" | Estimativa de consenso de cada história comparada com a referência US01, com a justificativa (seção 4.3 do backlog) | _a preencher_ |
