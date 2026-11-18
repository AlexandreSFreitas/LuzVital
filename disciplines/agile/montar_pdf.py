"""Monta o PDF único da entrega de Agile Methodology a partir de docs/agile/*.md.

Uso: python disciplines/agile/montar_pdf.py
Saída: disciplines/agile/LuzVital_Agile.pdf (fora do Git). Requer: markdown, playwright e Google Chrome.
Os textos ficam nos .md (fonte de verdade); este script só junta, limpa notas internas e formata.
"""
import asyncio
import re
from pathlib import Path

import markdown
from playwright.async_api import async_playwright

RAIZ = Path(__file__).resolve().parents[2]
AGILE = RAIZ / "docs" / "agile"
SAIDA = Path(__file__).with_name("LuzVital_Agile.pdf")
VIDEO = "https://youtu.be/WZSq77cMLtg"
SITE = "https://luzvital.onrender.com"
EQUIPE = [("Alexandre Freitas Silva", "566278"), ("Arthur Gaspare Gil", "555746"),
          ("Felipe Rodrigues Gomes Ribeiro", "562482")]
ARQUIVOS = ["01_IDEIA.md", "02_PERSONAS.md", "03_CASOS_DE_USO.md", "04_BACKLOG.md", "05_PROTOTIPO.md", "06_PITCH.md"]


def limpar(md: str) -> str:
    """Remove notas internas do repositório que não fazem sentido no PDF."""
    fora = [r"^Item \d da entrega.*$", r"^> ⚠️.*$", r"^- Fonte do diagrama:.*$", r"^- Imagem para o PDF:.*$",
            r"^- \*\*Priorização:.*$"]
    linhas = [ln for ln in md.splitlines() if not any(re.match(p, ln) for p in fora)]
    md = "\n".join(linhas)
    md = md.replace("](../diagrams/", f"]({(RAIZ / 'docs' / 'diagrams').as_uri()}/")
    md = md.replace("](img/", f"]({(AGILE / 'img').as_uri()}/")
    return md


def html_secao(nome: str) -> str:
    md = limpar((AGILE / nome).read_text(encoding="utf-8"))
    if nome == "03_CASOS_DE_USO.md":  # diagrama deitado, numa página só, logo depois do título
        from PIL import Image
        girado = SAIDA.with_name("_casos_de_uso_girado.png")
        Image.open(RAIZ / "docs" / "diagrams" / "casos_de_uso.png").rotate(90, expand=True).save(girado)
        titulo, resto = md.split("\n", 1)
        corpo = markdown.markdown(resto, extensions=["tables", "sane_lists"])
        return (f'<section class="secao">{markdown.markdown(titulo)}<img class="diagrama" src="{girado.as_uri()}">'
                f'<div class="secao">{corpo}</div></section>')
    corpo = markdown.markdown(md, extensions=["tables", "sane_lists"])
    return f'<section class="secao">{corpo}</section>'


CSS = """
@page { size: A4; margin: 18mm 16mm 18mm 16mm; }
* { box-sizing: border-box; }
body { font-family: Inter, Arial, sans-serif; font-size: 10pt; line-height: 1.5; color: #172B4D; }
h1 { font-size: 20pt; color: #0F2A50; border-bottom: 3px solid #F2B134; padding-bottom: 6px; margin: 0 0 14px; }
h2 { font-size: 13pt; color: #155EEF; margin: 20px 0 8px; break-after: avoid; }
h3 { font-size: 11pt; margin: 14px 0 6px; break-after: avoid; }
p, li { orphans: 3; widows: 3; }
table { width: 100%; border-collapse: collapse; margin: 8px 0 14px; font-size: 8.6pt; break-inside: auto; }
th { background: #EAF2FF; text-align: left; }
th, td { border: 1px solid #DCE4F0; padding: 5px 7px; vertical-align: top; }
tr { break-inside: avoid; }
img { display: block; max-width: 100%; max-height: 225mm; margin: 10px auto; border: 1px solid #DCE4F0; border-radius: 6px; }
img[src*="celular"], img[src*="tela_alerta"] { max-width: 62mm; }
img.diagrama { border: 0; max-height: 228mm; }
blockquote { margin: 8px 0; padding: 6px 12px; border-left: 4px solid #F2B134; background: #FFF8E1; }
code { font-size: 8.6pt; background: #F5F8FC; padding: 0 3px; border-radius: 3px; }
a { color: #155EEF; }
.secao { break-before: page; }
.capa { height: 255mm; display: flex; flex-direction: column; justify-content: space-between; }
.capa .topo { color: #4A5A70; font-size: 10pt; }
.capa h1 { font-size: 40pt; border: 0; margin: 0; }
.capa .frase { font-size: 15pt; color: #4A5A70; margin-top: 6px; }
.capa .faixa { width: 70mm; height: 6px; background: #F2B134; margin: 18px 0; }
.capa table { width: auto; font-size: 11pt; }
.capa .links p { margin: 4px 0; font-size: 11pt; }
.sumario ol { font-size: 11pt; line-height: 2; }
.pendente { border: 2px solid #B42318; background: #FEF3F2; color: #B42318; padding: 8px 12px; border-radius: 6px; font-weight: 600; }
"""


def capa() -> str:
    linhas = "".join(f"<tr><td>{n}</td><td>RM {rm}</td></tr>" for n, rm in sorted(EQUIPE))
    return f"""
<section class="capa">
  <div class="topo">FIAP · Engenharia de Software · 2º ano<br>Global Solution 2026.2 — CitizenTech<br>
  Agile Methodology With Squad Framework</div>
  <div>
    <h1>LuzVital</h1>
    <div class="frase">A energia pode acabar. O cuidado não.</div>
    <div class="faixa"></div>
    <p>Plataforma de apoio a pacientes eletrodependentes em casa e à sua rede de cuidado
    quando falta energia elétrica.</p>
  </div>
  <div>
    <h3>Equipe</h3>
    <table>{linhas}</table>
    <div class="links">
      <p><b>Vídeo pitch (YouTube, não listado):</b> <a href="{VIDEO}">{VIDEO}</a></p>
      <p><b>Site:</b> <a href="{SITE}">{SITE}</a></p>
    </div>
  </div>
</section>
<section class="secao sumario">
  <h1>Sumário</h1>
  <ol>
    <li>Apresentação descritiva da ideia</li>
    <li>Personas</li>
    <li>Diagrama de casos de uso</li>
    <li>Backlog do produto (MoSCoW, Planning Poker e MVP)</li>
    <li>Protótipo das telas e decisões de UX</li>
    <li>Vídeo pitch</li>
  </ol>
</section>"""


def planning_poker_vazio() -> bool:
    texto = (AGILE / "04_BACKLOG.md").read_text(encoding="utf-8")
    return bool(re.search(r"^\| US01 \| \| \| \|", texto, re.M))


async def main():
    corpo = capa() + "".join(html_secao(a) for a in ARQUIVOS)
    if planning_poker_vazio():
        corpo = corpo.replace("<h2>4.3 Registro do Planning Poker</h2>",
                              '<h2>4.3 Registro do Planning Poker</h2><p class="pendente">PENDENTE: preencher os votos '
                              "da equipe em docs/agile/04_BACKLOG.md e gerar o PDF de novo.</p>")
    html = f'<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8"><style>{CSS}</style></head><body>{corpo}</body></html>'
    tmp = SAIDA.with_suffix(".html")
    tmp.write_text(html, encoding="utf-8")
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
        pg = await b.new_page()
        await pg.goto(tmp.as_uri())
        await pg.wait_for_timeout(800)
        await pg.pdf(path=str(SAIDA), format="A4", print_background=True, display_header_footer=True,
                     header_template="<span></span>",
                     footer_template='<div style="font-size:8pt;width:100%;text-align:center;color:#888">'
                                     'LuzVital — Agile Methodology — <span class="pageNumber"></span>/<span class="totalPages"></span></div>',
                     margin={"top": "16mm", "bottom": "18mm", "left": "16mm", "right": "16mm"})
        await b.close()
    tmp.unlink()
    SAIDA.with_name("_casos_de_uso_girado.png").unlink(missing_ok=True)
    print("ok:", SAIDA, "| Planning Poker pendente" if planning_poker_vazio() else "")


asyncio.run(main())
