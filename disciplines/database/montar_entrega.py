"""Monta a entrega de Database Design.

Uso: python disciplines/database/montar_entrega.py
Saída em disciplines/database/entrega/ (fora do Git):
  - LuzVital_Database_Design.pdf  (itens 1 e 2: apresentação e diagrama lógico)
  - ddl.sql, dml.sql, dql.sql      (itens 3 a 5: cópias dos scripts de database/)
Requer: playwright e Google Chrome.
"""
import asyncio
import shutil
from pathlib import Path

from playwright.async_api import async_playwright

RAIZ = Path(__file__).resolve().parents[2]
DB = RAIZ / "database"
SAIDA = Path(__file__).with_name("entrega")
SAIDA.mkdir(exist_ok=True)
PDF = SAIDA / "LuzVital_Database_Design.pdf"

NOME_EQUIPE = ""  # preencher com o nome oficial da equipe
SOLUCAO = "LuzVital"
VIDEO = "https://youtu.be/WZSq77cMLtg"
SITE = "https://luzvital.onrender.com"
REPO = "https://github.com/AlexandreSFreitas/LuzVital"
EQUIPE = [("Alexandre Freitas Silva", "566278"), ("Arthur Gaspare Gil", "555746"),
          ("Felipe Rodrigues Gomes Ribeiro", "562482")]

TABELAS = [
    ("REGIAO", "Bairro ou área da cidade. É a chave do cruzamento entre a falta de energia e os pacientes."),
    ("PACIENTE", "Paciente eletrodependente (dados fictícios), com endereço e região."),
    ("EQUIPAMENTO", "Catálogo de equipamentos médicos, com consumo e indicação de suporte à vida."),
    ("PACIENTE_EQUIPAMENTO", "Equipamento que cada paciente usa, com a autonomia da bateria daquela unidade."),
    ("CONTATO", "Familiar, cuidador ou equipe de saúde que pode ajudar."),
    ("PACIENTE_CONTATO", "Liga paciente e contato, com a ordem de acionamento."),
    ("INTERRUPCAO", "Falta de energia numa região (no MVP, simulada)."),
    ("ALERTA", "Aviso para um contato de um paciente afetado, com prioridade, status e confirmação."),
    ("ACAO_APOIO", "O que foi feito depois do alerta (histórico do atendimento)."),
]


def capa():
    equipe = "".join(f"<tr><td>{n}</td><td>RM {rm}</td></tr>" for n, rm in sorted(EQUIPE))
    nome = NOME_EQUIPE or '<span class="pendente">[NOME DA EQUIPE]</span>'
    return f"""
<section class="capa">
  <div class="topo">FIAP · Engenharia de Software · 2º ano<br>Global Solution 2026.2 — CitizenTech<br>Database Design</div>
  <div>
    <h1>{SOLUCAO}</h1>
    <div class="frase">A energia pode acabar. O cuidado não.</div>
    <div class="faixa"></div>
    <p>Modelo de dados da plataforma de apoio a pacientes eletrodependentes quando falta energia.</p>
  </div>
  <div>
    <p><b>Equipe:</b> {nome}<br><b>Solução:</b> {SOLUCAO}</p>
    <h3>Integrantes</h3>
    <table>{equipe}</table>
  </div>
</section>"""


SUMARIO = """
<section class="secao sumario">
  <h1>Sumário</h1>
  <ol>
    <li>Objetivo e escopo do projeto</li>
    <li>Principais funcionalidades da solução</li>
    <li>Diagrama do modelo lógico (Oracle Data Modeler)</li>
    <li>Scripts entregues</li>
  </ol>
</section>"""


def corpo():
    tabelas = "".join(f"<tr><td><code>{t}</code></td><td>{d}</td></tr>" for t, d in TABELAS)
    return f"""
<section class="secao">
  <h1>1. Objetivo e escopo do projeto</h1>
  <h2>Contexto da solução</h2>
  <p>Pacientes que dependem de equipamentos elétricos em casa, como concentradores de oxigênio, ventiladores
  pulmonares e bombas de alimentação, correm risco quando falta energia. O problema não é só a falta de energia:
  é a demora para saber <b>quem</b> foi afetado, <b>quem precisa de ajuda primeiro</b> e <b>quem deve agir</b>.</p>
  <p>A <b>LuzVital</b> é uma plataforma que cruza uma falta de energia numa região com os pacientes cadastrados
  ali e avisa a rede de apoio de cada um (família, cuidadores e equipe de home care), acompanhando quem já
  confirmou que vai ajudar.</p>
  <p class="destaque"><b>Vídeo pitch da solução:</b> <a href="{VIDEO}">{VIDEO}</a><br>
  <b>Site:</b> <a href="{SITE}">{SITE}</a></p>

  <h2>Objetivo do banco de dados</h2>
  <p>Organizar, num banco Oracle, as informações que a LuzVital precisa para agir numa falta de energia:
  onde cada paciente mora, de quais equipamentos depende e por quanto tempo a bateria aguenta, quem deve ser
  avisado e em que ordem, quais interrupções aconteceram, quais alertas foram gerados e o que foi feito depois.</p>

  <h2>Escopo</h2>
  <ul>
    <li><b>Dentro do escopo:</b> 9 tabelas normalizadas até a 3ª forma normal, com chaves primárias, chaves
    estrangeiras, restrições de domínio (CHECK) e de unicidade (UNIQUE), e dados de exemplo <b>fictícios</b>.</li>
    <li><b>Fora do escopo (versão futura):</b> login e perfis de usuário, consentimento LGPD, integração real
    com a distribuidora de energia e com dispositivos de monitoramento.</li>
    <li>O mesmo modelo é usado pela API Java (Spring Boot com JDBC) publicada no Render.</li>
  </ul>

  <h2>Tabelas do modelo</h2>
  <table><tr><th>Tabela</th><th>Para que serve</th></tr>{tabelas}</table>
</section>

<section class="secao">
  <h1>2. Principais funcionalidades da solução</h1>
  <ol>
    <li><b>Cadastro de pacientes</b> com endereço e região (tabelas <code>PACIENTE</code> e <code>REGIAO</code>).</li>
    <li><b>Equipamentos e autonomia da bateria</b> de cada paciente (<code>EQUIPAMENTO</code> e <code>PACIENTE_EQUIPAMENTO</code>).</li>
    <li><b>Rede de apoio</b>: contatos e a ordem em que devem ser avisados (<code>CONTATO</code> e <code>PACIENTE_CONTATO</code>).</li>
    <li><b>Registro de interrupção de energia</b> por região, com início, fim e duração estimada (<code>INTERRUPCAO</code>).</li>
    <li><b>Geração de alertas priorizados</b> para os contatos dos pacientes da região afetada. A prioridade (1 a 3)
    segue uma regra operacional, não clínica: equipamento de suporte à vida e bateria menor que a duração estimada (<code>ALERTA</code>).</li>
    <li><b>Confirmação do alerta</b>: o status passa de PENDENTE para CONFIRMADO, com a data e a hora.</li>
    <li><b>Histórico das ações de apoio</b> depois do alerta, incluindo a orientação de ligar para o SAMU 192 (<code>ACAO_APOIO</code>).</li>
  </ol>
  <h2>Regras garantidas pelo banco</h2>
  <ul>
    <li>Um alerta por par paciente–contato em cada interrupção (<code>UNIQUE</code>).</li>
    <li>A ordem de acionamento não se repete para o mesmo paciente (<code>UNIQUE</code>).</li>
    <li>Domínios fechados para tipo de contato, categoria de equipamento, origem e status (<code>CHECK</code>).</li>
    <li>O fim de uma interrupção nunca é anterior ao início (<code>CHECK</code>).</li>
  </ul>
</section>

<section class="secao">
  <h1>3. Diagrama do modelo lógico (Oracle Data Modeler)</h1>
  <p>Diagrama gerado no Oracle Data Modeler. Mostra as 9 tabelas com atributos e tipos, chaves primárias (P),
  chaves estrangeiras (F), restrições de unicidade (U) e os relacionamentos 1:N com cardinalidade.</p>
  <img class="diagrama" src="{(DB / 'luzvital_logico.png').as_uri()}">
</section>

<section class="secao">
  <h1>4. Scripts entregues</h1>
  <table>
    <tr><th>Arquivo</th><th>Conteúdo</th></tr>
    <tr><td><code>ddl.sql</code></td><td>CREATE TABLE com PK, NOT NULL, CHECK e UNIQUE; ALTER TABLE com as 9 chaves estrangeiras.</td></tr>
    <tr><td><code>dml.sql</code></td><td>INSERT com dados fictícios, no mínimo 5 linhas por tabela, e COMMIT.</td></tr>
    <tr><td><code>dql.sql</code></td><td>As 3 consultas: INNER JOIN; INNER JOIN com GROUP BY e funções de grupo; LEFT OUTER JOIN com WHERE e ORDER BY.</td></tr>
  </table>
  <p>Ordem de execução no SQL Developer: <code>ddl.sql</code>, depois <code>dml.sql</code>, depois <code>dql.sql</code> (executar como script, F5).</p>
  <p>Repositório: <a href="{REPO}">{REPO}</a> (pasta <code>database/</code>).</p>
</section>"""


CSS = """
* { box-sizing: border-box; }
body { font-family: Inter, Arial, sans-serif; font-size: 10.5pt; line-height: 1.55; color: #172B4D; }
h1 { font-size: 20pt; color: #0F2A50; border-bottom: 3px solid #F2B134; padding-bottom: 6px; margin: 0 0 14px; }
h2 { font-size: 13pt; color: #155EEF; margin: 18px 0 8px; }
table { width: 100%; border-collapse: collapse; margin: 8px 0 14px; font-size: 9.5pt; }
th { background: #EAF2FF; text-align: left; }
th, td { border: 1px solid #DCE4F0; padding: 5px 7px; vertical-align: top; }
code { font-size: 9pt; background: #F5F8FC; padding: 0 3px; border-radius: 3px; }
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
.pendente { color: #B42318; background: #FEF3F2; padding: 0 6px; font-weight: 700; }
img.diagrama { display: block; max-width: 100%; max-height: 215mm; margin: 10px auto; }
"""


async def main():
    html = (f'<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8"><style>{CSS}</style></head>'
            f"<body>{capa()}{SUMARIO}{corpo()}</body></html>")
    tmp = SAIDA / "_tmp.html"
    tmp.write_text(html, encoding="utf-8")
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
        pg = await b.new_page()
        await pg.goto(tmp.as_uri())
        await pg.wait_for_timeout(500)
        await pg.pdf(path=str(PDF), format="A4", print_background=True, display_header_footer=True,
                     header_template="<span></span>",
                     footer_template='<div style="font-size:8pt;width:100%;text-align:center;color:#888">'
                                     'LuzVital — Database Design — <span class="pageNumber"></span>/<span class="totalPages"></span></div>',
                     margin={"top": "16mm", "bottom": "18mm", "left": "16mm", "right": "16mm"})
        await b.close()
    tmp.unlink()
    for nome in ("ddl.sql", "dml.sql", "dql.sql"):
        shutil.copy(DB / nome, SAIDA / nome)
    print("ok:", *sorted(f.name for f in SAIDA.iterdir()), "| nome da equipe pendente" if not NOME_EQUIPE else "")


asyncio.run(main())
