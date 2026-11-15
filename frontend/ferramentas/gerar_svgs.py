"""Gera os SVGs próprios da LuzVital (logo, favicon e ilustrações).
Uso (na raiz do repositório): python frontend/ferramentas/gerar_svgs.py backend/src/main/resources/static/assets
"""
import math, sys, os
OUT = sys.argv[1]

def raios(cx, cy, r1, r2, n=8, rot=0):
    out = []
    for i in range(n):
        a = math.radians(rot + i * 360 / n)
        out.append(f'<line x1="{cx+r1*math.cos(a):.2f}" y1="{cy+r1*math.sin(a):.2f}" x2="{cx+r2*math.cos(a):.2f}" y2="{cy+r2*math.sin(a):.2f}"/>')
    return "".join(out)

def simbolo(cor="#155EEF", sw=3.2, centro=True):
    nucleo = f'<circle cx="24" cy="24" r="5" fill="{cor}" stroke="none"/>' if centro else ""
    return (f'<g fill="none" stroke="{cor}" stroke-width="{sw}" stroke-linecap="round">'
            f'<circle cx="24" cy="24" r="10"/>{raios(24,24,15.5,21)}</g>{nucleo}')

w = lambda name, s: open(os.path.join(OUT, name), "w").write(s)

w("logo/luzvital-simbolo.svg",
  f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" role="img" aria-label="LuzVital">{simbolo()}</svg>\n')
w("logo/favicon.svg",
  f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48"><rect width="48" height="48" rx="12" fill="#155EEF"/>'
  f'<g fill="none" stroke="#fff" stroke-width="4" stroke-linecap="round"><circle cx="24" cy="24" r="8"/>{raios(24,24,14,19)}</g></svg>\n')
w("logo/luzvital-logo.svg",
  f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 220 48" role="img" aria-label="LuzVital">{simbolo()}'
  '<text x="58" y="33" font-family="Inter, system-ui, sans-serif" font-size="26" font-weight="700" letter-spacing="-0.5">'
  '<tspan fill="#163B6D">Luz</tspan><tspan fill="#155EEF">Vital</tspan></text></svg>\n')

def cena(noite=False):
    """Sala de casa com paciente sentada, concentrador de oxigênio e janela.
    noite=True: falta de energia (tons escuros, aparelho apagado, celular aceso)."""
    P = dict(
        fundo="#EAF2FF", parede="#F5F8FC", chao="#DCE7FB", janela="#FFFFFF", ceu="#CFE0FF",
        astro="#FFC93C", moveis="#163B6D", poltrona="#9DB9F2", manta="#155EEF", pele="#E8B998",
        cabelo="#C9CED6", aparelho="#FFFFFF", visor="#155EEF", tom="#58677C", planta="#4E9F80",
    ) if not noite else dict(
        fundo="#163B6D", parede="#1D4680", chao="#14325E", janela="#0F2A50", ceu="#0B2142",
        astro="#E9EEF7", moveis="#0B1F3D", poltrona="#3A5F9A", manta="#2A5BC4", pele="#B88D73",
        cabelo="#8E96A3", aparelho="#C9D3E3", visor="#3B4A60", tom="#8EA3C3", planta="#2F6B57",
    )
    p = P
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 560 480">']
    s.append(f'<rect width="560" height="480" rx="36" fill="{p["fundo"]}"/>')
    s.append(f'<rect x="28" y="28" width="504" height="340" rx="24" fill="{p["parede"]}"/>')
    s.append(f'<rect x="28" y="352" width="504" height="100" rx="20" fill="{p["chao"]}"/>')
    # janela
    s.append(f'<rect x="300" y="64" width="190" height="150" rx="18" fill="{p["ceu"]}"/>')
    if noite:
        s.append(f'<circle cx="440" cy="110" r="20" fill="{p["astro"]}"/><circle cx="450" cy="102" r="18" fill="{p["ceu"]}"/>')
        for x, y in [(340, 96), (372, 130), (410, 160), (466, 170)]:
            s.append(f'<circle cx="{x}" cy="{y}" r="2.2" fill="#E9EEF7"/>')
    else:
        s.append(f'<circle cx="438" cy="112" r="18" fill="{p["astro"]}"/>')
        s.append(f'<g stroke="{p["astro"]}" stroke-width="4" stroke-linecap="round">{raios(438,112,26,34)}</g>')
        s.append('<path d="M318 190c14-16 34-16 46 0 10-10 28-8 34 6H318z" fill="#FFFFFF" opacity=".9"/>')
    s.append(f'<rect x="300" y="64" width="190" height="150" rx="18" fill="none" stroke="{p["janela"]}" stroke-width="10"/>')
    s.append(f'<line x1="395" y1="64" x2="395" y2="214" stroke="{p["janela"]}" stroke-width="8"/>')
    # planta
    s.append(f'<rect x="452" y="300" width="44" height="56" rx="10" fill="{p["moveis"]}"/>')
    s.append(f'<g fill="{p["planta"]}"><ellipse cx="462" cy="282" rx="12" ry="26" transform="rotate(-24 462 282)"/>'
             f'<ellipse cx="486" cy="276" rx="12" ry="28" transform="rotate(22 486 276)"/><ellipse cx="474" cy="268" rx="11" ry="30"/></g>')
    # poltrona
    s.append(f'<rect x="70" y="210" width="190" height="150" rx="40" fill="{p["poltrona"]}"/>')
    s.append(f'<rect x="52" y="270" width="54" height="110" rx="24" fill="{p["poltrona"]}"/>')
    s.append(f'<rect x="224" y="270" width="54" height="110" rx="24" fill="{p["poltrona"]}"/>')
    s.append(f'<rect x="84" y="372" width="12" height="34" rx="6" fill="{p["moveis"]}"/><rect x="232" y="372" width="12" height="34" rx="6" fill="{p["moveis"]}"/>')
    # pessoa (sem rosto detalhado: forma simples e digna)
    s.append(f'<path d="M110 360C110 296 130 250 165 250S220 296 220 360z" fill="{p["moveis"]}"/>')
    s.append(f'<circle cx="165" cy="214" r="30" fill="{p["pele"]}"/>')
    s.append(f'<path d="M135 212c0-24 14-36 30-36s32 10 32 34c-8-12-22-16-34-14-12 2-22 8-28 16z" fill="{p["cabelo"]}"/>')
    s.append(f'<path d="M104 318h130a14 14 0 0 1 14 14v34H92v-34a14 14 0 0 1 12-14z" fill="{p["manta"]}"/>')
    s.append(f'<path d="M120 336h98M120 352h98" stroke="#FFFFFF" stroke-opacity=".35" stroke-width="4" stroke-linecap="round"/>')
    # cânula até o concentrador
    s.append(f'<path d="M148 226c-14 18-6 46 30 52 40 7 82 0 118 26" fill="none" stroke="{p["tom"]}" stroke-width="3" stroke-linecap="round" opacity=".8"/>')
    # concentrador
    s.append(f'<rect x="290" y="250" width="92" height="132" rx="18" fill="{p["aparelho"]}" stroke="{p["moveis"]}" stroke-opacity=".15" stroke-width="2"/>')
    s.append(f'<rect x="304" y="266" width="64" height="34" rx="8" fill="{p["visor"]}"/>')
    if not noite:
        s.append('<text x="336" y="289" text-anchor="middle" font-family="Inter, system-ui, sans-serif" font-size="15" font-weight="700" fill="#FFFFFF">O₂</text>')
    for i in range(4):
        s.append(f'<rect x="306" y="{316+i*12}" width="60" height="5" rx="2.5" fill="{p["tom"]}" opacity=".35"/>')
    s.append(f'<rect x="300" y="382" width="16" height="10" rx="4" fill="{p["moveis"]}"/><rect x="356" y="382" width="16" height="10" rx="4" fill="{p["moveis"]}"/>')
    # cabo e tomada
    s.append(f'<path d="M382 360c34 0 30-56 62-56h-2" fill="none" stroke="{p["moveis"]}" stroke-width="4" stroke-linecap="round"/>')
    s.append(f'<rect x="428" y="292" width="26" height="26" rx="6" fill="{p["janela"]}" stroke="{p["moveis"]}" stroke-opacity=".25" stroke-width="2"/>')
    s.append(f'<circle cx="437" cy="305" r="2.4" fill="{p["moveis"]}"/><circle cx="445" cy="305" r="2.4" fill="{p["moveis"]}"/>')
    if noite:
        # celular aceso com alerta
        s.append('<circle cx="125" cy="428" r="38" fill="#FFE8A3" opacity=".14"/>')
        s.append('<g transform="translate(96 410) rotate(-8)"><rect width="58" height="40" rx="9" fill="#0B1F3D"/>'
                 '<rect x="4" y="4" width="50" height="32" rx="6" fill="#FFF4E5"/>'
                 '<rect x="10" y="11" width="30" height="5" rx="2.5" fill="#B54708"/><rect x="10" y="21" width="38" height="4" rx="2" fill="#B54708" opacity=".5"/></g>')
        
    s.append('</svg>\n')
    return "".join(s)

w("images/casa-energia.svg", cena(False))
w("images/casa-sem-energia.svg", cena(True))
print("ok")
