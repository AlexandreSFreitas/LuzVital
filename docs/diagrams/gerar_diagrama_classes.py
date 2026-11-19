"""Gera o diagrama de classes do backend lendo o código Java (backend/src/main/java).

Uso: python docs/diagrams/gerar_diagrama_classes.py   (requer Graphviz: dot)
Saídas: docs/diagrams/classes_camadas.png (controller, bo, dao, exceções, config)
        docs/diagrams/classes_modelo.png  (model, enums e dto)
Getters e setters são omitidos para o diagrama caber na página; atributos e demais métodos públicos aparecem.
"""
import re
import subprocess
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
SRC = RAIZ / "backend" / "src" / "main" / "java" / "br" / "com" / "luzvital"
OUT = Path(__file__).parent


def ler(arq):
    txt = arq.read_text(encoding="utf-8")
    txt = re.sub(r"/\*.*?\*/", "", txt, flags=re.S)
    txt = re.sub(r"//[^\n]*", "", txt)
    m = re.search(r"public\s+(?:final\s+|abstract\s+)?(class|enum|record|interface)\s+(\w+)(?:\(([^)]*)\))?"
                  r"(?:\s+extends\s+(\w+))?(?:\s+implements\s+([\w, ]+))?", txt)
    if not m:
        return None
    tipo, nome, comps, pai, _ = m.groups()
    corpo = txt[m.end():]
    campos, metodos, valores = [], [], []
    if tipo == "record":
        partes, nivel, atual = [], 0, ""
        for ch in comps:  # divide só nas vírgulas fora de <...>
            nivel += (ch == "<") - (ch == ">")
            if ch == "," and nivel == 0:
                partes.append(atual); atual = ""
            else:
                atual += ch
        partes.append(atual)
        for p_ in (x.strip() for x in partes if x.strip()):
            t, n = p_.rsplit(" ", 1)
            campos.append(f"+ {n}: {t}")
    if tipo == "enum":
        bloco = corpo[corpo.index("{") + 1:]
        valores = [v.strip().split("(")[0].strip("} \n") for v in re.split(r"[,;]", bloco.split(";")[0]) if v.strip("} \n")]
    for f in re.finditer(r"^\s{4}(private|protected|public)\s+(static\s+)?(final\s+)?([\w<>, ?\[\]]+?)\s+(\w+)\s*(=[^;]*)?;", corpo, re.M):
        vis, st, fin, t, n, _ = f.groups()
        if st:
            continue
        campos.append(f"{'-' if vis == 'private' else '+'} {n}: {t.strip()}")
    for mt in re.finditer(r"^\s{4}(public|protected)\s+(static\s+)?([\w<>, ?\[\]]+?\s+)?(\w+)\s*\(([^)]*)\)\s*(throws [\w, ]+)?\s*\{",
                          corpo, re.M):
        vis, st, ret, n, params, _ = mt.groups()
        if ret is None:  # construtor
            continue
        if re.match(r"(get|set|is)[A-Z]", n) or n in ("equals", "hashCode", "toString"):
            continue
        ps = ", ".join(p.strip().split()[-2] if len(p.strip().split()) > 1 else p.strip()
                       for p in re.sub(r"@\w+(\([^)]*\))?\s*", "", params).split(",") if p.strip())
        metodos.append(f"+ {'«static» ' if st else ''}{n}({ps}): {ret.strip()}")
    return dict(nome=nome, tipo=tipo, pai=pai, campos=campos, metodos=metodos, valores=valores, texto=txt)


classes = {}
for arq in sorted(SRC.rglob("*.java")):
    c = ler(arq)
    if c:
        c["pacote"] = arq.parent.name if arq.parent != SRC else "app"
        classes[c["nome"]] = c


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def no(c):
    est = {"enum": "«enum»", "record": "«record»", "interface": "«interface»"}.get(c["tipo"], "")
    cab = (f'<TR><TD BGCOLOR="#163B6D"><FONT COLOR="white" POINT-SIZE="9">{est}</FONT><BR/>' if est else
           '<TR><TD BGCOLOR="#163B6D">') + f'<FONT COLOR="white"><B>{c["nome"]}</B></FONT></TD></TR>'
    linhas = c["valores"] if c["tipo"] == "enum" else c["campos"]
    a = "<BR ALIGN='LEFT'/>".join(esc(x) for x in linhas) + "<BR ALIGN='LEFT'/>" if linhas else " "
    m = "<BR ALIGN='LEFT'/>".join(esc(x) for x in c["metodos"]) + "<BR ALIGN='LEFT'/>" if c["metodos"] else " "
    return (f'"{c["nome"]}" [label=<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4" BGCOLOR="#FFFFFF">'
            f'{cab}<TR><TD ALIGN="LEFT"><FONT POINT-SIZE="9">{a}</FONT></TD></TR>'
            f'<TR><TD ALIGN="LEFT"><FONT POINT-SIZE="9">{m}</FONT></TD></TR></TABLE>>];')


def usa(a, b):
    """a referencia b como tipo de atributo (associação) ou só no código (dependência)."""
    ca = classes[a]
    if any(re.search(rf"\b{b}\b", f) for f in ca["campos"]):
        return "assoc"
    if re.search(rf"\b{b}\b", ca["texto"]):
        return "dep"
    return None


def gerar(nome, pacotes, rotulos, saida, rankdir="TB", dep=True):
    L = [f'digraph {nome} {{', f'rankdir={rankdir}; newrank=true; nodesep=0.35; ranksep=0.6; fontname="Arial";',
         'node [shape=plain, fontname="Arial"]; edge [fontname="Arial", fontsize=8, color="#56606e"];']
    nos = [n for n, c in classes.items() if c["pacote"] in pacotes]
    for p in pacotes:
        L.append(f'subgraph cluster_{p} {{ label="{rotulos[p]}"; fontsize=12; style="rounded,dashed"; color="#c9a227";')
        L += [no(classes[n]) for n in nos if classes[n]["pacote"] == p]
        L.append("}")
    for a in nos:
        if classes[a]["pai"] in nos:
            L.append(f'"{a}" -> "{classes[a]["pai"]}" [arrowhead=onormal];')
        for b in nos:
            if a == b or classes[a]["pai"] == b:
                continue
            k = usa(a, b)
            if k == "assoc":
                L.append(f'"{a}" -> "{b}" [arrowhead=vee];')
            elif k == "dep" and dep and (classes[b]["pacote"] != "exception" or classes[a]["pacote"] == "exception"):
                L.append(f'"{a}" -> "{b}" [arrowhead=vee, style=dashed, color="#9aa3af"];')
    L.append("}")
    dot = saida.with_suffix(".dot")
    dot.write_text("\n".join(L), encoding="utf-8")
    subprocess.run(["dot", "-Tpng", "-Gdpi=170", str(dot), "-o", str(saida)], check=True)
    subprocess.run(["dot", "-Tsvg", str(dot), "-o", str(saida.with_suffix(".svg"))], check=True)
    dot.unlink()


ROT = {"controller": "controller (endpoints REST)", "bo": "bo (regras de negócio)", "dao": "dao (JDBC puro)",
       "exception": "exception (tratamento de erros)", "config": "config", "model": "model (tabelas do banco)",
       "dto": "dto"}
gerar("camadas", ["controller", "bo", "dao", "config", "exception"], ROT, OUT / "classes_camadas.png", rankdir="LR")
gerar("modelo", ["model", "dto"], ROT, OUT / "classes_modelo.png", rankdir="LR")
print("ok:", len(classes), "classes lidas")
