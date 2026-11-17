"""Confere o roteiro do pitch: soma dos tempos (<= 3:00) e se cada narração cabe na cena.

Uso: python pitch/verificar_roteiro.py
"""
import re
import sys
from pathlib import Path

LIMITE_S = 180
MAX_PALAVRAS_POR_S = 2.5  # ~150 palavras por minuto

texto = Path(__file__).with_name("roteiro.md").read_text(encoding="utf-8")


def seg(t: str) -> int:
    m, s = t.split(":")
    return int(m) * 60 + int(s)


cenas = []
for linha in texto.splitlines():
    m = re.match(r"\|\s*(\w+)\s*\|\s*(\d:\d\d)–(\d:\d\d)\s*\|(.*)", linha)
    if m:
        cena, ini, fim, resto = m.groups()
        falas = re.findall(r"\*\*N\d+[^*]*\*\*[^\"|]*\"([^\"]+)\"", resto)
        cenas.append((cena, seg(ini), seg(fim), falas))

erros = 0
anterior = 0
print(f"{'Cena':<5}{'Início':>7}{'Fim':>6}{'Dur.':>6}{'Palavras':>10}{'Pal./s':>8}")
for cena, ini, fim, falas in cenas:
    if ini != anterior:
        print(f"  ! buraco ou sobreposição antes da cena {cena}")
        erros += 1
    dur = fim - ini
    palavras = sum(len(f.split()) for f in falas)
    ritmo = palavras / dur if dur else 0
    alerta = "  <- rápido demais" if ritmo > MAX_PALAVRAS_POR_S else ""
    erros += bool(alerta)
    print(f"{cena:<5}{ini:>7}{fim:>6}{dur:>6}{palavras:>10}{ritmo:>8.2f}{alerta}")
    anterior = fim

total = anterior
print(f"\nTotal: {total // 60}:{total % 60:02d} (limite 3:00)")
if total > LIMITE_S:
    print("  ! passou de 3:00")
    erros += 1
sys.exit(1 if erros else 0)
