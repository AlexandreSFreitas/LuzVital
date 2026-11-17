"""Gera a trilha original do pitch LuzVital por síntese (sem samples nem direitos de terceiros).

Saídas (em pitch/trilha/saida/, fora do Git):
  - aparelho_respiratorio_timeline.wav : som do aparelho já na posição do roteiro (0:00–0:04 e 0:12–0:15)
  - aparelho_respiratorio_loop.wav     : 3 ciclos soltos, para usar livremente
  - trilha_dramatica_timeline.wav      : música com a dinâmica do roteiro (2:51), começa em 0:18

Uso: python pitch/trilha/gerar_trilha.py
A dinâmica (volume por trecho) está em DINAMICA; os acordes em SECOES. Ajuste e rode de novo.
"""
from pathlib import Path

import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, sosfilt

SR = 44100
TOTAL = 171.0  # 2:51
OUT = Path(__file__).with_name("saida")
OUT.mkdir(exist_ok=True)
rng = np.random.default_rng(7)


def t_axis(dur):
    return np.arange(int(dur * SR)) / SR


def nota(nome):
    """'A3' -> frequência em Hz."""
    idx = {"C": -9, "C#": -8, "D": -7, "D#": -6, "E": -5, "F": -4, "F#": -3,
           "G": -2, "G#": -1, "A": 0, "A#": 1, "B": 2}
    n, o = nome[:-1], int(nome[-1])
    return 440.0 * 2 ** ((idx[n] + (o - 4) * 12) / 12)


def lowpass(x, fc):
    return sosfilt(butter(2, fc, "low", fs=SR, output="sos"), x)


def bandpass(x, lo, hi):
    return sosfilt(butter(2, [lo, hi], "band", fs=SR, output="sos"), x)


def reverb(x, mix=0.35):
    """Reverb simples (Schroeder: 4 combs + 2 allpass)."""
    y = np.zeros_like(x)
    for d, g in [(1557, .84), (1617, .83), (1491, .85), (1422, .86)]:
        c = np.copy(x)
        for i in range(d, len(c), d):  # feedback em blocos (rápido o bastante)
            c[i:i + d] += g * c[i - d:i][:len(c[i:i + d])]
        y += c / 4
    for d, g in [(225, .5), (556, .5)]:
        a = np.zeros_like(y)
        a[:d] = -g * y[:d]
        for i in range(d, len(y), d):
            seg = y[i:i + d]
            a[i:i + d] = -g * seg + y[i - d:i][:len(seg)] + g * a[i - d:i][:len(seg)]
        y = a
    return (1 - mix) * x + mix * lowpass(y, 5000)


# ---------- som do aparelho respiratório ----------
def ciclo_aparelho():
    """Um ciclo de ~3,6 s: clique da válvula, inspiração (sopro subindo), expiração, bip suave."""
    dur = 3.6
    t = t_axis(dur)
    y = np.zeros_like(t)
    # clique mecânico
    k = int(0.012 * SR)
    y[:k] += rng.normal(0, 0.5, k) * np.exp(-np.linspace(0, 8, k))
    # inspiração: ruído filtrado com envelope subindo e descendo (1,3 s)
    n_in = int(1.3 * SR)
    ins = bandpass(rng.normal(0, 1, n_in), 500, 2500) * np.sin(np.linspace(0, np.pi, n_in)) ** 1.5
    y[int(0.05 * SR):int(0.05 * SR) + n_in] += 0.35 * ins
    # expiração: mais grave e longa (1,6 s)
    n_ex = int(1.6 * SR)
    ex = bandpass(rng.normal(0, 1, n_ex), 250, 1200) * np.sin(np.linspace(0, np.pi, n_ex)) ** 2
    s0 = int(1.55 * SR)
    y[s0:s0 + n_ex] += 0.22 * ex
    # bip do monitor (discreto)
    nb = int(0.09 * SR)
    tb = np.arange(nb) / SR
    bip = np.sin(2 * np.pi * 1046.5 * tb) * np.sin(np.linspace(0, np.pi, nb))
    b0 = int(3.25 * SR)
    y[b0:b0 + nb] += 0.12 * bip
    return y


def aparelho():
    ciclo = ciclo_aparelho()
    tl = np.zeros(int(TOTAL * SR))
    # 0:00–0:04: um ciclo + começo do segundo
    tl[:len(ciclo)] += ciclo
    tl[len(ciclo):int(4.0 * SR)] += ciclo[:int(4.0 * SR) - len(ciclo)]
    # 0:12–0:15: volta por um ciclo e PARA (sem bip, sem efeito sensacionalista)
    c2 = ciclo[:int(3.0 * SR)].copy()
    c2[-int(0.05 * SR):] *= np.linspace(1, 0, int(0.05 * SR))
    tl[int(12.0 * SR):int(12.0 * SR) + len(c2)] += c2
    loop = np.concatenate([ciclo, ciclo, ciclo])
    return reverb(tl, 0.2), reverb(loop, 0.2)


# ---------- música ----------
# (início, fim, acordes, duração de cada acorde em s, caráter)
SECOES = [
    (18, 65, ["A2 E3 A3 C4", "F2 C3 A3 C4", "D2 A2 F3 A3", "E2 B2 G#3 B3"], 6.0, "menor"),
    (65, 75, ["A3 E4"], 10.0, "suspenso"),
    (75, 147, ["C3 G3 C4 E4", "G2 D3 G3 B3", "A2 E3 A3 C4", "F2 C3 A3 C4"], 4.5, "maior"),
    (147, 171, ["F2 C3 A3 C4", "G2 D3 G3 B3", "C3 G3 C4 E4 G4"], 6.0, "resolucao"),
]

# volume (dB) em pontos do tempo; entre eles a curva é interpolada.
# Baixo sob voz e falas; sobe quando a imagem fala sozinha.
DINAMICA = [
    (0, -90), (17.5, -90),
    (18, -40), (24, -34),          # 2a: entra fraca sob o áudio do JN
    (24.1, -34), (33, -32),        # sob a N1
    (34, -22), (42, -22),          # 2b: fotos fortes, sem voz -> sobe
    (43, -34), (64, -32),          # 2c: falas e N2 -> baixa
    (65, -40), (75, -36),          # 3: a pergunta, quase silêncio
    (76, -24), (96, -18),          # 4: site, sem voz -> cresce
    (118, -14), (122, -16),        # 5: ápice na demonstração
    (123, -30), (131, -30),        # 6: sob a N9
    (132, -20), (147, -16),        # 6: equipes e ODS, crescendo
    (148, -32), (157, -32),        # 7a: fala da médica -> baixa
    (158, -24), (163, -22),        # 7b: N11, resolução
    (165, -20), (171, -90),        # 7c: créditos e fade final
]


def pad(freqs, dur, brilho):
    t = t_axis(dur)
    y = np.zeros_like(t)
    for f in freqs:
        for det in (-0.12, 0.0, 0.12):  # leve desafinação = coro
            ff = f * 2 ** (det / 12)
            for h, a in [(1, 1), (2, .35 * brilho), (3, .15 * brilho), (4, .06 * brilho)]:
                y += a * np.sin(2 * np.pi * ff * h * t + rng.uniform(0, 6.28))
    ataque = min(1.5, dur / 3)
    env = np.minimum(1, t / ataque) * np.minimum(1, (dur - t) / 1.2 + 0.0)
    return y * np.clip(env, 0, 1) / (len(freqs) * 3)


def piano(f, dur=3.0):
    t = t_axis(dur)
    y = sum(a * np.sin(2 * np.pi * f * h * t) for h, a in [(1, 1), (2, .4), (3, .18), (4, .08)])
    return y * np.exp(-t * 1.6) * np.minimum(1, t / 0.005)


def musica():
    out = np.zeros(int(TOTAL * SR))
    for ini, fim, acordes, dur_ac, carater in SECOES:
        brilho = {"menor": .6, "suspenso": .3, "maior": 1.0, "resolucao": .9}[carater]
        t0, i = ini, 0
        while t0 < fim:
            d = min(dur_ac + 1.0, fim - t0 + 1.0)  # sobreposição de 1 s entre acordes
            fr = [nota(n) for n in acordes[i % len(acordes)].split()]
            seg = pad(fr, d, brilho)
            a = int(t0 * SR)
            out[a:a + len(seg)] += seg[:len(out) - a]
            # melodia de piano nas partes sem voz (2b, 4–5 e 6 final)
            if carater in ("maior", "resolucao") or 33 <= t0 < 42:
                topo = sorted(fr)[-1] * 2
                for k, mult in enumerate([1, 9 / 8, 5 / 4][: 1 + (carater == "maior")]):
                    p = piano(topo * mult) * 0.25
                    b = int((t0 + 0.8 + k * dur_ac / 2) * SR)
                    out[b:b + len(p)] += p[:max(0, len(out) - b)]
            t0 += dur_ac
            i += 1
        # nota suspensa da pergunta (luz âmbar acendendo em ~1:06)
        if carater == "suspenso":
            p = piano(nota("E5"), 6.0) * 0.4
            b = int(66.0 * SR)
            out[b:b + len(p)] += p
    xs, ys = zip(*DINAMICA)
    curva_db = np.interp(np.arange(len(out)) / SR, xs, ys)
    out = out / (np.max(np.abs(out)) + 1e-9) * 10 ** (curva_db / 20) * 4
    return reverb(lowpass(out, 7000), 0.4)


def salvar(nome, x, pico_db=-1.0):
    x = x / (np.max(np.abs(x)) + 1e-9) * 10 ** (pico_db / 20) if pico_db is not None else x
    wavfile.write(OUT / nome, SR, (np.clip(x, -1, 1) * 32767).astype(np.int16))


if __name__ == "__main__":
    tl, loop = aparelho()
    salvar("aparelho_respiratorio_timeline.wav", tl, -6)
    salvar("aparelho_respiratorio_loop.wav", loop, -6)
    m = musica()
    salvar("trilha_dramatica_timeline.wav", m, None)  # mantém a dinâmica absoluta
    print("ok:", *sorted(p.name for p in OUT.glob("*.wav")))


# ---------- som extra (16/11): aparelho desligando ----------
def aparelho_desligando():
    """~6 s (cabe na cena 1c): um ciclo normal; o seguinte começa mais lento e mais grave,
    o motor desacelera, clique de desligar e silêncio."""
    normal = ciclo_aparelho()
    c = ciclo_aparelho()
    idx = np.arange(0, len(c), 0.6)  # 40% mais lento e mais grave
    lento = np.interp(idx, np.arange(len(c)), c)[: int(2.0 * SR)]
    lento *= np.linspace(1, 0, len(lento)) ** 1.5  # vai perdendo força
    y = np.concatenate([normal, lento])
    t = np.arange(len(y)) / SR
    queda = len(normal) / SR  # o motor desacelera no último ciclo
    f = np.where(t < queda, 95.0, 95.0 * np.maximum(0.1, 1 - (t - queda) / 2.0))
    hum = 0.05 * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.where(t < queda, 1, np.maximum(0, 1 - (t - queda) / 2.0))
    y = y + hum
    k = int(0.02 * SR)
    clique = rng.normal(0, 0.6, k) * np.exp(-np.linspace(0, 10, k))
    y = np.concatenate([y, clique, np.zeros(int(0.4 * SR))])
    return reverb(y, 0.2)


if __name__ == "__main__":
    salvar("aparelho_desligando.wav", aparelho_desligando(), -6)
    print("ok: aparelho_desligando.wav")
