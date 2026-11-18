"""Desenha docs/diagrams/casos_de_uso.png com layout fixo (mesmo conteúdo de casos_de_uso.puml).

Uso: python docs/diagrams/desenhar_casos_de_uso.py   (requer Pillow e a fonte Inter)
Atores da rede de apoio à esquerda, da operação à direita; casos de uso agrupados por área.
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ESC = 2  # desenha em 2x para ficar nítido no PDF
W, H = 2600, 1900
F = "/usr/share/fonts/opentype/inter/Inter-{}.otf"
img = Image.new("RGB", (W * ESC, H * ESC), "white")
d = ImageDraw.Draw(img)


def fonte(t, p="Regular"):
    return ImageFont.truetype(F.format(p), t * ESC)


def s(*v):
    return [x * ESC for x in v]


OURO, CINZA, LINHA = (141, 110, 0), (150, 150, 150), (86, 96, 110)
UC = {  # id: (texto, x, y, futuro)
    "UC01": ("UC01 Cadastrar paciente\n(endereço e região)", 880, 230, 0),
    "UC02": ("UC02 Registrar\nconsentimento", 880, 345, 0),
    "UC03": ("UC03 Gerenciar equipamentos\ne autonomia da bateria", 880, 460, 0),
    "UC04": ("UC04 Gerenciar contatos\ne ordem de acionamento", 880, 575, 0),
    "UC10": ("UC10 Receber alerta", 880, 790, 0),
    "UC11": ("UC11 Confirmar alerta", 880, 905, 0),
    "UC15": ("UC15 Consultar orientações\nde emergência (SAMU 192)", 880, 1020, 0),
    "UC12": ("UC12 Registrar ação\nde apoio", 1300, 1180, 0),
    "UC20": ("UC20 Autenticar-se", 1300, 1560, 0),
    "UC07": ("UC07 Registrar interrupção\nde energia", 1720, 230, 0),
    "UC08": ("UC08 Identificar pacientes\nafetados", 1720, 345, 0),
    "UC09": ("UC09 Gerar alertas\npriorizados", 1720, 460, 0),
    "UC16": ("UC16 Escalar alerta\nsem resposta", 1720, 575, 0),
    "UC13": ("UC13 Acompanhar painel\nda interrupção", 1720, 790, 0),
    "UC14": ("UC14 Encerrar interrupção", 1720, 905, 0),
    "UC19": ("UC19 Consultar indicadores", 1720, 1020, 0),
    "UC05": ("UC05 Manter catálogo\nde equipamentos", 1720, 1180, 0),
    "UC06": ("UC06 Manter regiões", 1720, 1295, 0),
    "UC21": ("UC21 Gerenciar usuários\ne perfis", 1720, 1410, 0),
    "UC17": ("UC17 Enviar sinal\nde funcionamento", 1720, 1620, 1),
    "UC18": ("UC18 Detectar ausência\nde sinal", 1720, 1740, 1),
}
ATOR = {  # id: (texto, x, y, lado, externo)
    "Equipe": ("Equipe de\nhome care", 170, 420, "e", 0),
    "Paciente": ("Paciente", 170, 820, "e", 0),
    "Contato": ("Contato de apoio\n(familiar/cuidador)", 170, 1200, "e", 0),
    "Mensagens": ("Serviço de mensagens\n(futuro, externo)", 170, 1600, "e", 1),
    "Simulador": ("Simulador de\ninterrupções (sistema)", 2430, 150, "d", 1),
    "Distribuidora": ("Distribuidora de energia\n(futuro, externo)", 2430, 390, "d", 1),
    "Operador": ("Operador\nda central", 2430, 880, "d", 0),
    "Admin": ("Administrador", 2430, 1300, "d", 0),
    "Dispositivo": ("Dispositivo de\nmonitoramento\n(futuro, externo)", 2430, 1650, "d", 1),
}
LIGA = {
    "Equipe": ["UC01", "UC02", "UC03", "UC04", "UC10", "UC11", "UC12", "UC20"],
    "Paciente": ["UC02", "UC15"],
    "Contato": ["UC10", "UC11", "UC15", "UC12", "UC20"],
    "Mensagens": ["UC10"],
    "Simulador": ["UC07"], "Distribuidora": ["UC07"],
    "Operador": ["UC07", "UC12", "UC13", "UC14", "UC19", "UC20"],
    "Admin": ["UC05", "UC06", "UC19", "UC21", "UC20"],
    "Dispositivo": ["UC17", "UC18"],
}
RX, RY = 212, 50

# moldura do sistema e grupos
d.rounded_rectangle(s(440, 60, 2160, 1840), 28 * ESC, outline=OURO, width=5 * ESC)
d.text(s(1300, 95), "LuzVital", font=fonte(40, "Bold"), fill=OURO, anchor="mm")
GRUPOS = [("Cadastro", 640, 132, 1120, 640, 0), ("Rede de apoio", 640, 694, 1120, 1085, 0),
          ("Interrupção e alertas", 1480, 132, 1960, 640, 0), ("Acompanhamento", 1480, 694, 1960, 1068, 0),
          ("Administração", 1480, 1086, 1960, 1475, 0), ("Monitoramento por dispositivo (futuro)", 1480, 1522, 1960, 1810, 1)]
for nome, x0, y0, x1, y1, fut in GRUPOS:
    cor = CINZA if fut else (201, 162, 39)
    for i in range(x0, x1, 18):  # borda tracejada
        d.line(s(i, y0, min(i + 10, x1), y0), fill=cor, width=2 * ESC)
        d.line(s(i, y1, min(i + 10, x1), y1), fill=cor, width=2 * ESC)
    for j in range(y0, y1, 18):
        d.line(s(x0, j, x0, min(j + 10, y1)), fill=cor, width=2 * ESC)
        d.line(s(x1, j, x1, min(j + 10, y1)), fill=cor, width=2 * ESC)
    d.text(s((x0 + x1) // 2, y0 + 20), nome, font=fonte(23, "SemiBold"), fill=(91, 74, 0), anchor="mm")


def borda_ator(a):
    _, x, y, lado, _ = ATOR[a]
    return (x + 70, y) if lado == "e" else (x - 70, y)


def borda_uc(u, de_x):
    _, x, y, _ = UC[u]
    return (x - RX, y) if de_x < x else (x + RX, y)


# associações (linhas por baixo das elipses)
for a, lista in LIGA.items():
    ax, ay = borda_ator(a)
    for u in lista:
        ux, uy = borda_uc(u, ax)
        d.line(s(ax, ay, ux, uy), fill=LINHA, width=2 * ESC)


def seta(pontos, rotulo, pos_rot):
    """Dependência tracejada com ponta de seta no último ponto."""
    for (x0, y0), (x1, y1) in zip(pontos, pontos[1:]):
        comp = max(abs(x1 - x0), abs(y1 - y0))
        n = max(1, comp // 16)
        for k in range(0, n, 2):
            a = (x0 + (x1 - x0) * k / n, y0 + (y1 - y0) * k / n)
            b = (x0 + (x1 - x0) * min(k + 1, n) / n, y0 + (y1 - y0) * min(k + 1, n) / n)
            d.line(s(*a, *b), fill=OURO, width=2 * ESC)
    (x0, y0), (x1, y1) = pontos[-2], pontos[-1]
    if x0 == x1:
        sg = 1 if y1 > y0 else -1
        d.polygon(s(x1, y1, x1 - 9, y1 - 16 * sg, x1 + 9, y1 - 16 * sg), fill=OURO)
    else:
        sg = 1 if x1 > x0 else -1
        d.polygon(s(x1, y1, x1 - 16 * sg, y1 - 9, x1 - 16 * sg, y1 + 9), fill=OURO)
    d.text(s(*pos_rot), rotulo, font=fonte(17, "Medium"), fill=OURO, anchor="mm")


seta([(1720, 276), (1720, 299)], "", (0, 0))
seta([(1720, 391), (1720, 414)], "", (0, 0))
seta([(1720, 529), (1720, 506)], "", (0, 0))
seta([(880, 276), (880, 299)], "", (0, 0))
seta([(675, 1020), (655, 1020), (655, 790), (675, 790)], "«extend»", (590, 905))
seta([(1925, 1740), (2120, 1740), (2120, 230), (1925, 230)], "«include»", (2105, 1000))
for (x, y, r) in [(1790, 288, "«include»"), (1790, 403, "«include»"), (1795, 517, "«extend»"), (955, 288, "«include»")]:
    d.text(s(x, y), r, font=fonte(16, "Medium"), fill=OURO, anchor="lm")

# casos de uso
for u, (t, x, y, fut) in UC.items():
    d.ellipse(s(x - RX, y - RY, x + RX, y + RY), fill=(241, 241, 241) if fut else (255, 248, 225),
              outline=(153, 153, 153) if fut else OURO, width=2 * ESC)
    d.multiline_text(s(x, y), t, font=fonte(23, "Medium"), fill=(30, 30, 30), anchor="mm", align="center", spacing=4 * ESC)

# atores (boneco + nome)
for a, (t, x, y, lado, ext) in ATOR.items():
    k = (120, 120, 120) if ext else (40, 40, 40)
    cy = y - 30
    d.ellipse(s(x - 14, cy - 44, x + 14, cy - 16), outline=k, width=3 * ESC)
    d.line(s(x, cy - 16, x, cy + 22), fill=k, width=3 * ESC)
    d.line(s(x - 26, cy - 2, x + 26, cy - 2), fill=k, width=3 * ESC)
    d.line(s(x, cy + 22, x - 20, cy + 52), fill=k, width=3 * ESC)
    d.line(s(x, cy + 22, x + 20, cy + 52), fill=k, width=3 * ESC)
    d.multiline_text(s(x, y + 50), t, font=fonte(23, "SemiBold"), fill=k, anchor="ma", align="center", spacing=3 * ESC)

d.text(s(60, 1870), "Linhas: associação ator–caso de uso. Tracejado: «include» / «extend». Cinza: escopo futuro, fora do MVP.",
       font=fonte(18), fill=(90, 90, 90), anchor="ls")
img.save(Path(__file__).with_name("casos_de_uso.png"))
print("ok")
