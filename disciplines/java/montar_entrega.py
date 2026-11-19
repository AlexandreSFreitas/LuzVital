"""Monta a entrega de Domain Driven Design - Java.

Uso: python disciplines/java/montar_entrega.py
Saída em disciplines/java/entrega/ (fora do Git):
  - LuzVital_DDD_Java.pdf   (documentação única)
  - LuzVital_DDD_Java.zip   (só o PDF), para o Portal do Aluno
Requer: playwright, Google Chrome; antes rode docs/diagrams/gerar_diagrama_classes.py.
"""
import asyncio
import zipfile
from pathlib import Path

from playwright.async_api import async_playwright

RAIZ = Path(__file__).resolve().parents[2]
SAIDA = Path(__file__).with_name("entrega")
SAIDA.mkdir(exist_ok=True)
PDF = SAIDA / "LuzVital_DDD_Java.pdf"

EQUIPE_NOME = "Equipe Luz Vital"
EQUIPE = [("Alexandre Freitas Silva", "566278"), ("Arthur Gaspare Gil", "555746"),
          ("Felipe Rodrigues Gomes Ribeiro", "562482")]
REPO = "https://github.com/AlexandreSFreitas/LuzVital"
DEPLOY = "https://luzvital.onrender.com"
VIDEO = "https://youtu.be/WZSq77cMLtg"
IMG = lambda p: (RAIZ / p).as_uri()  # noqa: E731

ENDPOINTS = [
    ("GET", "/api/regioes", "—", "Lista todas as regiões", "200"),
    ("GET", "/api/regioes/{id}", "—", "Busca uma região", "200, 404"),
    ("POST", "/api/regioes", '{"nome":"Jardim Ângela","cidade":"São Paulo","uf":"SP"}', "Cadastra uma região", "201, 400, 409"),
    ("PUT", "/api/regioes/{id}", '{"nome":"Jardim Ângela","cidade":"São Paulo","uf":"SP"}', "Atualiza uma região", "200, 400, 404, 409"),
    ("DELETE", "/api/regioes/{id}", "—", "Remove uma região (409 se houver pacientes ou interrupções ligados)", "204, 404, 409"),
    ("GET", "/api/pacientes", "—", "Lista todos os pacientes", "200"),
    ("GET", "/api/pacientes/{id}", "—", "Busca um paciente", "200, 404"),
    ("POST", "/api/pacientes", '{"nome":"Paciente Fictício","dataNascimento":"1950-03-10","logradouro":"Rua Exemplo",'
     '"numero":"10","cep":"04101-000","idRegiao":1}', "Cadastra um paciente", "201, 400, 404"),
    ("PUT", "/api/pacientes/{id}", "mesmo formato do POST (\"ativo\": false desativa)", "Atualiza um paciente", "200, 400, 404"),
    ("DELETE", "/api/pacientes/{id}", "—", "Remove um paciente (409 se tiver contatos ou alertas; use PUT com ativo=false)", "204, 404, 409"),
    ("GET", "/api/interrupcoes", "—", "Lista as interrupções de energia", "200"),
    ("GET", "/api/interrupcoes/{id}", "—", "Busca uma interrupção", "200, 404"),
    ("POST", "/api/interrupcoes", '{"idRegiao":1,"duracaoEstimadaMin":120}',
     "Registra uma falta de energia e, na mesma transação, gera os alertas priorizados para os contatos dos pacientes da região",
     "201, 400, 404"),
]


def capa():
    linhas = "".join(f"<tr><td>{n}</td><td>RM {rm}</td></tr>" for n, rm in sorted(EQUIPE))
    return f"""
<section class="capa">
  <div class="topo">FIAP · Engenharia de Software · 2º ano<br>Global Solution 2026.2 — CitizenTech<br>Domain Driven Design - Java</div>
  <div>
    <h1>LuzVital</h1>
    <div class="frase">A energia pode acabar. O cuidado não.</div>
    <div class="faixa"></div>
    <p>API RESTful em Java com Spring Boot e Oracle para apoiar pacientes eletrodependentes quando falta energia.</p>
  </div>
  <div>
    <p><b>Equipe:</b> {EQUIPE_NOME}</p>
    <table>{linhas}</table>
    <p class="links"><b>GitHub:</b> <a href="{REPO}">{REPO}</a><br><b>Deploy:</b> <a href="{DEPLOY}">{DEPLOY}</a><br><b>Teste da API:</b> <a href="{DEPLOY}/api.html">{DEPLOY}/api.html</a></p>
  </div>
</section>
<section class="secao sumario">
  <h1>Índice</h1>
  <ol>
    <li>Descritivo da solução</li><li>Justificativa</li><li>Objetivos</li><li>Arquitetura em camadas</li>
    <li>Diagrama de classes</li><li>Protótipos de tela</li><li>Endpoints HTTP</li>
    <li>Diagrama Entidade-Relacionamento (DER)</li><li>Instruções para executar o projeto</li>
  </ol>
</section>"""


def corpo():
    eps = "".join(f'<tr><td class="m m-{m}">{m}</td><td><code>{u}</code></td><td><code>{b}</code></td><td>{d}</td><td>{s}</td></tr>'
                  for m, u, b, d, s in ENDPOINTS)
    return f"""
<section class="secao">
  <h1>1. Descritivo da solução</h1>
  <p>Pacientes que dependem de equipamentos elétricos em casa, como concentradores de oxigênio, ventiladores pulmonares
  e bombas de alimentação, correm risco quando falta energia. O problema não é só a falta de energia: é a demora para saber
  <b>quem</b> foi afetado, <b>quem precisa de ajuda primeiro</b> e <b>quem deve agir</b>.</p>
  <p>A <b>LuzVital</b> é uma CitizenTech que cadastra esses pacientes com a região onde moram, os equipamentos que usam, a
  autonomia da bateria de cada um e a rede de apoio (família, cuidadores e equipe de home care), em ordem de acionamento.
  Quando uma falta de energia é registrada numa região, a API identifica os pacientes ativos dali, calcula a prioridade de
  cada um e gera alertas para os contatos, tudo numa única transação no banco Oracle.</p>
  <p class="destaque"><b>Vídeo pitch da solução:</b> <a href="{VIDEO}">{VIDEO}</a></p>
  <p>Esta entrega implementa a capacidade central da solução: o domínio de regiões, pacientes, interrupções de energia e
  alertas, numa API REST em Spring Boot com JDBC, publicada no Render e ligada ao servidor Oracle da FIAP.</p>

  <h1 class="sub">2. Justificativa</h1>
  <ul>
    <li>Na Grande São Paulo, temporais de 2024 e 2025 deixaram milhões de unidades sem energia por horas ou dias, e
    reportagens mostraram famílias improvisando para manter aparelhos de pacientes ligados.</li>
    <li>A distribuidora mantém um cadastro de clientes que dependem de equipamentos, mas ele prioriza o reparo da rede e não
    avisa a família, os cuidadores e a equipe de saúde.</li>
    <li>Um sistema simples, que cruza a região da falta de energia com os pacientes cadastrados e avisa a rede de apoio na
    ordem certa, diminui o tempo até alguém responsável saber que um paciente vulnerável pode precisar de ajuda.</li>
  </ul>

  <h1 class="sub">3. Objetivos</h1>
  <ul>
    <li><b>Geral:</b> diminuir o tempo entre uma falta de energia e o momento em que alguém responsável sabe que um paciente
    eletrodependente pode precisar de ajuda.</li>
    <li>Manter o cadastro de regiões e pacientes (CRUD completo com GET, POST, PUT e DELETE).</li>
    <li>Registrar interrupções de energia por região e gerar alertas priorizados automaticamente.</li>
    <li>Aplicar uma regra de prioridade operacional (não clínica): prioridade 1 quando há equipamento de suporte à vida com
    bateria menor que a duração estimada; 2 quando qualquer equipamento não aguenta; 3 nos demais casos.</li>
    <li>Responder com erros claros e padronizados, sem expor detalhes do banco.</li>
    <li>Publicar a API e o site no Render, com as credenciais apenas em variáveis de ambiente.</li>
  </ul>
</section>

<section class="secao">
  <h1>4. Arquitetura em camadas</h1>
  <p>Pacote base <code>br.com.luzvital</code>, organizado nas camadas pedidas em aula:</p>
  <table>
    <tr><th>Camada</th><th>Responsabilidade</th><th>Classes</th></tr>
    <tr><td><code>model</code></td><td>Uma classe por tabela do banco e enums dos domínios (CHECK)</td>
      <td>Regiao, Paciente, Equipamento, PacienteEquipamento, PacienteContato, Interrupcao, Alerta; CategoriaEquipamento,
      OrigemInterrupcao, StatusInterrupcao, StatusAlerta</td></tr>
    <tr><td><code>dao</code></td><td>Acesso ao Oracle com JDBC puro (<code>PreparedStatement</code>, SQL escrito à mão)</td>
      <td>RegiaoDAO, PacienteDAO, EquipamentoDAO, PacienteEquipamentoDAO, PacienteContatoDAO, InterrupcaoDAO, AlertaDAO,
      SqlErrorTranslator, JdbcUtil</td></tr>
    <tr><td><code>bo</code></td><td>Regras de negócio e validações</td>
      <td>RegiaoBO, PacienteBO, InterrupcaoBO, GeradorAlertas, RegraPrioridade, Validacoes, Fusos</td></tr>
    <tr><td><code>controller</code></td><td>Endpoints REST em <code>/api</code></td>
      <td>RegiaoController, PacienteController, InterrupcaoController</td></tr>
    <tr><td><code>exception</code></td><td>Exceções de domínio e tratamento global (respostas 400, 404, 405, 409, 500)</td>
      <td>GlobalExceptionHandler, ErroResponse, ValidacaoException, RecursoNaoEncontradoException, ConflitoException,
      PersistenciaException</td></tr>
    <tr><td><code>dto</code> / <code>config</code></td><td>Resposta do registro de interrupção; pool de conexões (HikariCP)</td>
      <td>ResultadoRegistroInterrupcao; ConnectionFactory</td></tr>
  </table>
  <p>Fluxo de uma requisição: <b>Controller</b> recebe o JSON → <b>BO</b> valida e aplica as regras → <b>DAO</b> executa o
  SQL no Oracle → erros do banco (ORA-00001, ORA-02292 etc.) viram exceções de domínio no <code>SqlErrorTranslator</code> →
  o <code>GlobalExceptionHandler</code> devolve <code>{{"status", "erro", "timestamp"}}</code>.</p>
</section>

<section class="secao">
  <h1>5. Diagrama de classes</h1>
  <p>Gerado a partir do código-fonte (<code>docs/diagrams/gerar_diagrama_classes.py</code>). Getters e setters foram omitidos.
  Setas cheias: associação (atributo do tipo); tracejadas: dependência (uso no código).</p>
  <h2>5.1 Camadas controller, bo, dao, exception e config</h2>
  <img class="diag" src="{IMG('docs/diagrams/classes_camadas.svg')}">
</section>
<section class="secao">
  <h2>5.2 Camada model e dto</h2>
  <img class="diag" src="{IMG('docs/diagrams/classes_modelo.svg')}">
</section>

<section class="secao">
  <h1>6. Protótipos de tela</h1>
  <p>Telas do site da LuzVital, servido pelo próprio Spring Boot (HTML, CSS e JavaScript puro) em <a href="{DEPLOY}">{DEPLOY}</a>.
  A demonstração usa dados fictícios.</p>
  <h2>Página inicial</h2>
  <img src="{IMG('docs/agile/img/site_inicio.png')}">
  <h2>Painel da central durante uma falta de energia simulada</h2>
  <img class="alta" src="{IMG('docs/agile/img/site_demonstracao.png')}">
  <h2>O mesmo painel no celular</h2>
  <img class="cel" src="{IMG('docs/agile/img/site_demonstracao_celular.png')}">
  <p>O site também traz um guia interativo da API em <a href="{DEPLOY}/api.html">{DEPLOY}/api.html</a>.</p>
</section>

<section class="secao">
  <h1>7. Endpoints HTTP</h1>
  <p>Base: <code>{DEPLOY}</code>. Corpo e respostas em JSON. Erros no formato
  <code>{{"status": 404, "erro": "Paciente não encontrado", "timestamp": "..."}}</code>.</p>
  <table class="eps"><colgroup><col style="width:9%"><col style="width:24%"><col style="width:27%"><col style="width:28%"><col style="width:12%"></colgroup><tr><th>Método</th><th>Rota</th><th>Corpo (exemplo)</th><th>O que faz</th><th>Respostas</th></tr>{eps}</table>
  <p><b>Resposta do POST /api/interrupcoes (201):</b> a interrupção criada, <code>pacientesAfetados</code>,
  <code>alertasGerados</code>, <code>alertasPorPrioridade</code>, a lista de alertas e <code>pacientesSemContato</code>.</p>
</section>

<section class="secao">
  <h1>8. Diagrama Entidade-Relacionamento (DER)</h1>
  <p>Modelo gerado no Oracle Data Modeler a partir do <code>database/ddl.sql</code>. São 9 tabelas; as classes da camada
  <code>model</code> seguem os mesmos nomes de colunas.</p>
  <img class="diag" src="{IMG('database/luzvital_logico.png')}">
</section>

<section class="secao">
  <h1>9. Instruções para executar o projeto</h1>
  <h2>Ferramentas e versões</h2>
  <table>
    <tr><th>Ferramenta</th><th>Versão</th></tr>
    <tr><td>Java JDK</td><td>21 (LTS) — Microsoft OpenJDK 21 ou Eclipse Temurin 21</td></tr>
    <tr><td>Spring Boot</td><td>4.1.2 (spring-boot-starter-webmvc e spring-boot-starter-jdbc)</td></tr>
    <tr><td>Maven</td><td>3.10.0, pelo Maven Wrapper do projeto (<code>mvnw</code> / <code>mvnw.cmd</code>); não precisa instalar</td></tr>
    <tr><td>Banco de dados</td><td>Oracle Database (servidor da FIAP), driver JDBC <code>ojdbc17</code></td></tr>
    <tr><td>IDE</td><td>IntelliJ IDEA (ou outra IDE com suporte a Java 21 e Maven)</td></tr>
    <tr><td>Banco: modelagem e scripts</td><td>Oracle SQL Developer e Oracle Data Modeler</td></tr>
    <tr><td>Deploy</td><td>Render (render.com), com Docker (imagem <code>eclipse-temurin:21</code>)</td></tr>
  </table>
  <h2>Links</h2>
  <p><b>GitHub:</b> <a href="{REPO}">{REPO}</a> (código em <code>backend/</code>)<br>
  <b>Deploy:</b> <a href="{DEPLOY}">{DEPLOY}</a> · API em <code>{DEPLOY}/api/...</code><br>
  <b>Teste da API (guia interativo no navegador):</b> <a href="{DEPLOY}/api.html">{DEPLOY}/api.html</a></p>
  <h2>Passo a passo (execução local)</h2>
  <ol>
    <li>Clone o repositório: <code>git clone {REPO}.git</code></li>
    <li>No Oracle (SQL Developer), rode <code>database/ddl.sql</code> e depois <code>database/dml.sql</code> (F5, executar como script).</li>
    <li>Defina as variáveis de ambiente no terminal (modelo em <code>env.example</code>; nunca versionar as credenciais):
      <code>DB_URL</code> (ex.: <code>jdbc:oracle:thin:@//&lt;host&gt;:1521/&lt;servico&gt;</code>), <code>DB_USERNAME</code>,
      <code>DB_PASSWORD</code>. Opcionais: <code>SPRING_PROFILES_ACTIVE</code> (<code>dev</code> ou <code>prod</code>) e <code>PORT</code> (8080).</li>
    <li>Execute: <code>cd backend</code> e <code>./mvnw spring-boot:run</code> (Windows: <code>mvnw.cmd spring-boot:run</code>).
      No IntelliJ, também é possível rodar a classe <code>LuzvitalApiApplication</code>.</li>
    <li>Acesse <code>http://localhost:8080</code> (site) e <code>http://localhost:8080/api/regioes</code> (API).</li>
    <li>Testes automatizados (sem banco, com DAOs falsos e MockMvc): <code>./mvnw test</code>.</li>
  </ol>
  <h2>Deploy no Render</h2>
  <ol>
    <li>Web Service ligado ao repositório do GitHub, ambiente <b>Docker</b>, usando o <code>backend/Dockerfile</code>.</li>
    <li>Variáveis de ambiente no painel do Render: <code>DB_URL</code>, <code>DB_USERNAME</code>, <code>DB_PASSWORD</code>;
      o perfil <code>prod</code> já vem definido no Dockerfile e a porta é lida de <code>PORT</code>.</li>
    <li>No plano gratuito, o serviço "dorme" sem uso: a primeira requisição pode levar cerca de um minuto.</li>
  </ol>
  <h2>Teste rápido da API</h2>
  <pre>curl {DEPLOY}/api/regioes
curl -X POST {DEPLOY}/api/interrupcoes -H "Content-Type: application/json" -d '{{"idRegiao":1,"duracaoEstimadaMin":120}}'</pre>
</section>"""


CSS = """
* { box-sizing: border-box; }
body { font-family: Inter, Arial, sans-serif; font-size: 10.5pt; line-height: 1.5; color: #172B4D; }
h1 { font-size: 19pt; color: #0F2A50; border-bottom: 3px solid #F2B134; padding-bottom: 6px; margin: 0 0 12px; }
h1.sub { margin-top: 22px; }
h2 { font-size: 12.5pt; color: #155EEF; margin: 16px 0 6px; break-after: avoid; }
table { width: 100%; border-collapse: collapse; margin: 8px 0 14px; font-size: 9pt; }
th { background: #EAF2FF; text-align: left; }
th, td { border: 1px solid #DCE4F0; padding: 5px 7px; vertical-align: top; }
tr { break-inside: avoid; }
code { font-size: 8.6pt; background: #F5F8FC; padding: 0 3px; border-radius: 3px; word-break: break-word; }
pre { font-size: 8.4pt; background: #F5F8FC; padding: 8px; border-radius: 6px; white-space: pre-wrap; }
a { color: #155EEF; }
li { margin-bottom: 4px; }
.secao { break-before: page; }
.destaque { border-left: 4px solid #F2B134; background: #FFF8E1; padding: 8px 12px; }
.capa { height: 255mm; display: flex; flex-direction: column; justify-content: space-between; }
.capa .topo { color: #4A5A70; }
.capa h1 { font-size: 40pt; border: 0; margin: 0; }
.capa .frase { font-size: 15pt; color: #4A5A70; margin-top: 6px; }
.capa .faixa { width: 70mm; height: 6px; background: #F2B134; margin: 18px 0; }
.capa table { width: auto; font-size: 11pt; }
.sumario ol { font-size: 11pt; line-height: 2; }
img { display: block; max-width: 100%; margin: 8px auto; border: 1px solid #DCE4F0; border-radius: 6px; }
img.diag { border: 0; width: 100%; max-height: 225mm; object-fit: contain; }
img.alta { max-height: 150mm; }
img.cel { max-width: 70mm; }
.eps { table-layout: fixed; } .eps td { font-size: 8.2pt; } .eps td:nth-child(2) code { white-space: nowrap; font-size: 8pt; }
.m { font-weight: 700; text-align: center; }
.m-GET { color: #067647; } .m-POST { color: #155EEF; } .m-PUT { color: #B54708; } .m-DELETE { color: #B42318; }
"""


async def main():
    html = (f'<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8"><style>{CSS}</style></head>'
            f"<body>{capa()}{corpo()}</body></html>")
    tmp = SAIDA / "_tmp.html"
    tmp.write_text(html, encoding="utf-8")
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
        pg = await b.new_page()
        await pg.goto(tmp.as_uri())
        await pg.wait_for_timeout(600)
        await pg.pdf(path=str(PDF), format="A4", print_background=True, display_header_footer=True,
                     header_template="<span></span>",
                     footer_template='<div style="font-size:8pt;width:100%;text-align:center;color:#888">'
                                     'LuzVital — Domain Driven Design - Java — <span class="pageNumber"></span>/<span class="totalPages"></span></div>',
                     margin={"top": "16mm", "bottom": "18mm", "left": "16mm", "right": "16mm"})
        await b.close()
    tmp.unlink()
    (SAIDA / "links.txt").unlink(missing_ok=True)
    with zipfile.ZipFile(SAIDA / "LuzVital_DDD_Java.zip", "w", zipfile.ZIP_DEFLATED) as z:
        z.write(PDF, PDF.name)
    print("ok:", *sorted(f.name for f in SAIDA.iterdir()))


asyncio.run(main())
