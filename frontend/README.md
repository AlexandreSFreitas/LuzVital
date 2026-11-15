# Frontend — LuzVital

Site institucional da LuzVital com **demonstração interativa**, em **HTML5, CSS3 e JavaScript puro**. Não usa frameworks, bibliotecas, etapa de build nem serviços externos.

> Decisão de 15/11/2026: a tecnologia do frontend é **HTML/CSS/JS puro**.
>
> **Onde está o site:** em `backend/src/main/resources/static/`. O Spring Boot serve essa pasta sozinho, então o mesmo deploy no Render entrega o site em `/`, o guia da API em `/api.html` e a API em `/api/...`. Há uma única cópia do site, que não se repete aqui.
>
> **Nesta pasta (`frontend/`)** ficam o protótipo de Agile (`prototipo/`), o script das ilustrações (`ferramentas/`) e esta documentação.

## Como abrir

- **Como no deploy:** suba o backend (`cd backend` e `mvnw.cmd spring-boot:run`) e abra `http://localhost:8080/`. O guia da API fica em `http://localhost:8080/api.html`.
- **Só o visual, sem backend:** dê dois cliques em `backend/src/main/resources/static/index.html`. A demonstração funciona; o testador da API precisa do servidor.

## Estrutura (em `backend/src/main/resources/static/`)

| Caminho | O que é |
|---|---|
| `index.html` | Página única: hero, problema, o que é, como funciona, demonstração, públicos, privacidade, FAQ, CTA e rodapé |
| `api.html` | Guia da API para avaliadores: tabela das 13 rotas, formato dos erros e um testador simples (GET, POST, PUT, DELETE) |
| `css/styles.css` | Tokens (cores, raios, sombras), componentes e seções. Mobile-first, com ajustes em 600, 768, 960 e 1100 px |
| `js/main.js` | Menu móvel acessível, cabeçalho ao rolar, seção atual no menu, acordeão do FAQ e animações de entrada |
| `js/api.js` | Rotas documentadas e testador (`fetch` na mesma origem; DELETE exige confirmação; `{id}` precisa ser trocado) |
| `css/api.css` | Estilos só da página da API |
| `js/simulacao.js` | Demonstração do painel: dados fictícios, regra de prioridade e fluxo da simulação |
| `assets/logo/` | Símbolo (sol), logo completo e favicon, em SVG próprio |
| `assets/images/` | Ilustrações próprias em SVG (casa com energia e sem energia) |
| `assets/fonts/` | Inter (subconjunto latino, `.woff`) e a licença `OFL.txt` |


Em `frontend/`:

| Caminho | O que é |
|---|---|
| `ferramentas/gerar_svgs.py` | Gera o logo, o favicon e as ilustrações. Na raiz do repositório: `python frontend/ferramentas/gerar_svgs.py backend/src/main/resources/static/assets` |
| `prototipo/` | Protótipo de 3 telas da entrega de Agile (não foi alterado) |

## Identidade visual

| Uso | Cor | Contraste |
|---|---|---|
| Azul principal (botões, links, destaques) | `#155EEF` | 5,41:1 sobre branco |
| Azul escuro (títulos, seção de privacidade) | `#163B6D` | 11,17:1 sobre branco |
| Azul claro (fundos de destaque) | `#EAF2FF` | — |
| Fundo neutro | `#F5F8FC` | — |
| Texto principal | `#172B4D` | 13,24:1 sobre `#F5F8FC` |
| Texto secundário | `#58677C` | 5,41:1 sobre `#F5F8FC` |
| Estados: ok / atenção / crítico | `#067647` / `#B54708` / `#B42318` | ≥ 5,4:1 sobre os fundos claros correspondentes |

- **Logo:** sol minimalista (círculo, núcleo e 8 raios de ponta arredondada). Representa energia e continuidade do cuidado.
- **Tipografia:** Inter Display nos títulos e Inter no texto. Fica hospedada no próprio site, para carregar rápido e não enviar dados de visitantes a terceiros.
- **Imagens:** ilustrações próprias em SVG, sem fotos de pessoas reais e sem cenas sensacionalistas.

## Demonstração

- Funciona **sem backend**, com dados fictícios do cenário das personas (Jardim Ângela, Dona Lúcia, Mariana).
- O fluxo é **Ocorrência → Identificação → Alertas → Acompanhamento**, com botões "Simular confirmação", "Energia voltou: encerrar" e "Reiniciar simulação".
- A **duração estimada** (2, 4 ou 6 horas) muda a prioridade pela mesma regra do backend (`docs/DATABASE_MODEL.md`, seção 4).
- Mostra um paciente de **outra região** como "não afetado", para deixar claro o cruzamento por região.
- O selo "Simulação · dados fictícios" e o aviso acima do painel ficam sempre visíveis.
- **Nada é salvo no navegador** (sem `localStorage` e sem `sessionStorage`).
- **Integração futura:** em `simulacao.js`, o objeto `fonteLocal` tem os mesmos métodos que uma fonte ligada à API (`registrarInterrupcao`, `confirmarAlerta`). Para usar o backend, crie uma fonte com `fetch('/api/...')` e troque a constante `FONTE`.

## Página da API (`api.html`)

- Quando o site é servido pelo Spring Boot no Render, a página fica em `https://<app>.onrender.com/api.html` e a API continua em `/api/...`, no mesmo endereço.
- O testador envia requisições ao próprio servidor (mesma origem, sem CORS). Aberta como arquivo, a página avisa e aceita o endereço de um servidor local.
- Por segurança, `PUT` e `DELETE` vêm com `{id}` no caminho, e o `DELETE` só é enviado depois de marcar a confirmação. Os exemplos usam dados fictícios.
- Se o servidor do Render estiver "dormindo", a página avisa que a primeira requisição pode levar cerca de 1 minuto.
- Testada contra um servidor simulado (200, 201 com `Location`, 204, 404 e JSON inválido). **Ainda falta testar contra o backend real.**

## Acessibilidade

- HTML semântico (`header`, `nav`, `main`, `section`, `footer`), títulos sem pular níveis e link "Pular para o conteúdo principal".
- Tudo funciona pelo teclado, com foco visível (contorno de 3 px, branco nas seções escuras).
- Menu móvel com `aria-expanded`. A tecla **Esc** fecha o menu e devolve o foco ao botão.
- FAQ no padrão WAI-ARIA de acordeão: botão com `aria-expanded` e região associada.
- A simulação anuncia cada etapa numa região `aria-live`. Depois de confirmar um alerta, o foco vai para o novo status, sem se perder.
- Estados nunca dependem só da cor: prioridade, status e reserva sempre têm texto.
- Respeita `prefers-reduced-motion`: sem animações e simulação sem esperas.
- Alvos de toque de 44 px ou mais. Funciona com zoom e a partir de 320 px de largura.

## Testes realizados (15/11/2026)

Chrome automatizado (Playwright) servindo a pasta por HTTP:

| Verificação | Resultado |
|---|---|
| Larguras 320, 360, 390, 768, 1024, 1100 e 1440 px | Sem rolagem horizontal |
| Console e recursos | Nenhum erro, nenhum arquivo faltando |
| Imagens sem `alt`, botões e links sem nome, âncoras quebradas, ids duplicados | Nenhum |
| Simulação (4 h) | 4 afetados, 8 alertas; Antônio e Lúcia com prioridade 1, Benedito 2, Helena 3; Joana (outra região) não afetada |
| Simulação (2 h) | Só Antônio com prioridade 1, como manda a regra |
| Confirmar pelo teclado, encerrar e reiniciar | Métricas, linha do tempo, foco e anúncios corretos |
| Menu móvel pelo teclado e Esc; FAQ com Enter e Espaço | Funcionam |

## Limitações

- A demonstração é local. O site ainda **não** chama a API do backend.
- A identificação automática de faltas de energia, os dispositivos IoT e a integração com a distribuidora não existem. O site apresenta tudo isso como possibilidade futura.
- Não houve teste com leitor de tela real (NVDA/VoiceOver). Recomendado antes da entrega.
