"""Monta o vídeo pitch da LuzVital com ffmpeg, a partir dos clipes cortados.

Uso:  python pitch/montagem/montar_pitch.py PASTA_DOS_CLIPES PASTA_DE_SAIDA

PASTA_DOS_CLIPES tem os arquivos doc_*.mp4, rep_*.mp4/wav, site_*.mp4 e narracao_*.wav
(material de terceiros: fica FORA do Git). A trilha vem de pitch/trilha/saida/.
Requer: ffmpeg, Pillow e a fonte Inter.

Cada item de SEGMENTOS vira um trecho de vídeo; no fim tudo é unido e recebe
narração, trilha, legendas e a frase final. Para mudar a ordem ou a duração, edite SEGMENTOS.
"""
import os
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

CLIPS = Path(sys.argv[1])
OUT = Path(sys.argv[2])
TMP = OUT / "tmp"
TMP.mkdir(parents=True, exist_ok=True)
TRILHA = Path(__file__).resolve().parents[1] / "trilha" / "saida"

W, H, FPS = 1920, 1080, 30
FONTES = "/usr/share/fonts/opentype/inter/"
AMBAR, NOITE, BRANCO = (242, 177, 52), (27, 42, 65), (255, 255, 255)


def fonte(tam, peso="Regular"):
    return ImageFont.truetype(f"{FONTES}Inter-{peso}.otf", tam)


def tela():
    return Image.new("RGBA", (W, H), (0, 0, 0, 0))


def texto_centro(linhas, y, tam=64, peso="SemiBold", cor=BRANCO, esp=1.35, sombra=False, img=None):
    """Linhas centralizadas a partir de y. Devolve a imagem (tela cheia, transparente)."""
    img = img or tela()
    d = ImageDraw.Draw(img)
    f = fonte(tam, peso)
    for i, ln in enumerate(linhas):
        w = d.textlength(ln, font=f)
        pos = ((W - w) / 2, y + i * tam * esp)
        if sombra:
            d.text((pos[0] + 3, pos[1] + 3), ln, font=f, fill=(0, 0, 0, 200))
        d.text(pos, ln, font=f, fill=cor + (255,))
    return img


def credito(txt, canto="dir"):
    """Crédito pequeno no canto superior."""
    img = tela()
    d = ImageDraw.Draw(img)
    f = fonte(26, "Medium")
    w = d.textlength(txt, font=f)
    x = W - w - 48 if canto == "dir" else 48
    d.rounded_rectangle((x - 14, 34, x + w + 14, 80), 8, fill=(0, 0, 0, 120))
    d.text((x, 41), txt, font=f, fill=(255, 255, 255, 235))
    return img


def legenda(txt):
    img = tela()
    d = ImageDraw.Draw(img)
    f = fonte(44, "SemiBold")
    w = d.textlength(txt, font=f)
    x, y = (W - w) / 2, 948
    d.rounded_rectangle((x - 26, y - 12, x + w + 26, y + 66), 12, fill=(0, 0, 0, 165))
    d.text((x, y), txt, font=f, fill=(255, 255, 255, 255))
    return img


def luz_ambar():
    """Ponto de luz âmbar com brilho (cena da pergunta)."""
    img = tela()
    d = ImageDraw.Draw(img)
    cx, cy = W // 2, 330
    for r, a in [(150, 26), (95, 50), (55, 95)]:
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=AMBAR + (a,))
    img = img.filter(ImageFilter.GaussianBlur(26))
    ImageDraw.Draw(img).ellipse((cx - 20, cy - 20, cx + 20, cy + 20), fill=AMBAR + (255,))
    return img


def cartao_ods():
    img = Image.new("RGBA", (W, H), NOITE + (255,))
    d = ImageDraw.Draw(img)
    texto_centro(["Conectado aos Objetivos de Desenvolvimento Sustentável"], 190, 46, "SemiBold", img=img)
    ods = [("3", "Saúde e", "bem-estar", (76, 159, 56)), ("9", "Indústria, inovação", "e infraestrutura", (253, 105, 37)),
           ("10", "Redução das", "desigualdades", (221, 19, 103)), ("11", "Cidades e comunidades", "sustentáveis", (253, 157, 36))]
    lado, vao = 330, 50
    x0 = (W - (4 * lado + 3 * vao)) // 2
    for i, (n, l1, l2, cor) in enumerate(ods):
        x = x0 + i * (lado + vao)
        d.rounded_rectangle((x, 340, x + lado, 340 + lado), 18, fill=cor + (255,))
        d.text((x + 28, 356), n, font=fonte(120, "ExtraBold"), fill=BRANCO + (255,))
        d.text((x + 28, 536), l1, font=fonte(24, "SemiBold"), fill=BRANCO + (255,))
        d.text((x + 28, 572), l2, font=fonte(24, "SemiBold"), fill=BRANCO + (255,))
    texto_centro(["O que vamos medir: o tempo entre a energia cair e alguém confirmar que vai ajudar."], 770, 34, "Regular",
                 cor=(215, 225, 238), img=img)
    return img


def cartao_creditos():
    img = tela()
    texto_centro(["LuzVital"], 110, 76, "Bold", cor=AMBAR, img=img)
    blocos = [
        ("Equipe", ["Alexandre Freitas Silva — RM 566278", "Arthur Gaspare Gil — RM 555746",
                    "Felipe Rodrigues Gomes Ribeiro — RM 562482"]),
        ("Imagens e depoimentos", ['Documentário "De Volta para Casa (Back Home)", trechos usados com autorização',
                                   "JA 2ª Edição (TV Anhanguera / g1) — Jornal Nacional (TV Globo) — R7",
                                   'Vídeo "UTI Domiciliar" (CPFL Energia / RGE)']),
        ("", ["Trilha original e som do aparelho: equipe LuzVital — Demonstração com dados fictícios",
              "Global Solution 2026.2 — FIAP — Engenharia de Software"]),
    ]
    y = 250
    for titulo, linhas in blocos:
        if titulo:
            texto_centro([titulo], y, 28, "SemiBold", cor=AMBAR, img=img)
            y += 50
        texto_centro(linhas, y, 32, "Regular", img=img, esp=1.5)
        y += int(len(linhas) * 32 * 1.5) + 46
    return img


def png(nome, img):
    p = TMP / f"{nome}.png"
    img.save(p)
    return p


def run(args):
    subprocess.run(["ffmpeg", "-v", "error", "-y", *map(str, args)], check=True)


def segmento(i, dur, video=None, audio=None, a_ini=0.0, lento=1.0, v_ini=0.0, overlays=(), fin=0.0, fout=0.0,
             fundo="black", afade=0.15):
    """Gera TMP/seg_XX.mp4 (1080p, 30 fps, áudio estéreo 48 kHz).

    video: arquivo ou None (fundo liso). audio: None (silêncio), "src" (o do próprio clipe) ou um arquivo.
    overlays: [(png, inicio, fim, fade)] sobre o trecho. fin/fout: fade do vídeo a partir do preto.
    """
    saida = TMP / f"seg_{i:02d}.mp4"
    if os.environ.get("REUSAR") and saida.exists():  # REUSAR=1 aproveita trechos já gerados
        return saida
    ins, fc = [], []
    if video:
        ins += ["-ss", v_ini, "-i", CLIPS / video]
        base = (f"[0:v]setpts={lento}*PTS,scale={W}:{H}:force_original_aspect_ratio=decrease,"
                f"pad={W}:{H}:(ow-iw)/2:(oh-ih)/2:black,setsar=1,fps={FPS}")
    else:
        ins += ["-f", "lavfi", "-i", f"color=c={fundo}:s={W}x{H}:r={FPS}:d={dur}"]
        base = "[0:v]format=yuv420p"
    if fin:
        base += f",fade=t=in:st=0:d={fin}"
    if fout:
        base += f",fade=t=out:st={dur - fout}:d={fout}"
    fc.append(base + "[v0]")
    n = 1
    for k, (p, a, b, f) in enumerate(overlays):
        ins += ["-loop", "1", "-t", dur, "-i", p]
        fc.append(f"[{n}:v]format=rgba,fade=t=in:st={a}:d={f}:alpha=1,fade=t=out:st={b - f}:d={f}:alpha=1[o{k}]")
        fc.append(f"[v{k}][o{k}]overlay=0:0:enable='between(t,{a},{b})'[v{k + 1}]")
        n += 1
    vfinal = f"[v{len(overlays)}]"
    if audio is None:
        ins += ["-f", "lavfi", "-t", dur, "-i", "anullsrc=r=48000:cl=stereo"]
        fc.append(f"[{n}:a]anull[a]")
    else:
        if audio == "src":
            origem = "[0:a]"
        else:
            ins += ["-ss", a_ini, "-i", audio]
            origem = f"[{n}:a]"
        fc.append(f"{origem}aresample=48000,aformat=channel_layouts=stereo,afade=t=in:d={afade},"
                  f"afade=t=out:st={dur - afade}:d={afade},apad[a]")
    run([*ins, "-filter_complex", ";".join(fc), "-map", vfinal, "-map", "[a]", "-t", dur, "-r", FPS,
         "-c:v", "libx264", "-preset", "veryfast", "-crf", "17", "-pix_fmt", "yuv420p",
         "-c:a", "aac", "-b:a", "192k", "-ar", "48000", saida])
    return saida


# ---------- imagens de texto ----------
C_DOC = png("c_doc", credito('Documentário "De Volta para Casa (Back Home)"'))
C_JA = png("c_ja", credito("JA 2ª Edição — TV Anhanguera / g1"))
C_JN = png("c_jn", credito("Jornal Nacional — TV Globo"))
C_JN_AUDIO = png("c_jn_audio", texto_centro(["Áudio: Jornal Nacional — TV Globo"], 980, 28, "Medium", cor=(200, 208, 220)))
C_RGE = png("c_rge", credito("Vídeo: CPFL Energia / RGE", "esq"))
C_R7 = png("c_r7", credito("Portal R7"))
T_11 = png("t_11", texto_centro(["Ela tinha 11 meses."], 495, 68, "Medium"))
LUZ = png("luz", luz_ambar())
T_P1 = png("t_p1", texto_centro(["E se, no momento em que a energia acabasse,", "alguém já soubesse"], 520, 56, "Medium"))
T_P2 = png("t_p2", texto_centro(["que aquela pessoa precisava de ajuda?"], 690, 56, "SemiBold", cor=AMBAR))
ODS = png("ods", cartao_ods())
CRED = png("cred", cartao_creditos())
FINAL = png("final", texto_centro(["A energia pode acabar.", "O cuidado não."], 760, 84, "Bold", sombra=True))

AP = TRILHA / "aparelho_respiratorio_timeline.wav"
doc = lambda d: [(C_DOC, 0.3, d - 0.2, 0.4)]  # noqa: E731

# (duração, kwargs do segmento, marcador)
SEGMENTOS = [
    # 1. A perda
    (4.0, dict(audio=AP, afade=0.3), "abertura"),
    (8.5, dict(video="rep_01_abertura_JA2_bebe_8s.mp4", audio="src", fin=0.25, fout=0.3,
               overlays=[(C_JA, 0.4, 8.3, 0.3)]), "reportagem"),
    (7.0, dict(audio=TRILHA / "aparelho_desligando.wav", afade=0.05, overlays=[(T_11, 4.3, 7.0, 0.9)]), "onze_meses"),
    # 2. Não é um caso isolado
    (5.8, dict(audio=CLIPS / "rep_02_JN_apagao_audio_0m00-0m05s8.wav", overlays=[(C_JN_AUDIO, 0.3, 5.6, 0.4)]), "jn_audio"),
    (2.55, dict(video="rep_03_JN_placa_av_paulista_0m34-0m36_sem_audio.mp4", overlays=[(C_JN, 0.2, 2.5, 0.2)]), "N1"),
    (6.25, dict(video="rep_04_JN_helicoptero_bairros_0m40-0m45_sem_audio.mp4", lento=1.25, fout=0.5,
                overlays=[(C_JN, 0.0, 6.0, 0.3)]), "helicoptero"),
    (5.0, dict(video="doc_02_imagem_forte_4m44-4m49.mp4", fin=0.5, overlays=doc(5.0)), "fotos"),
    (4.0, dict(video="doc_03_imagem_casal_4m51-4m55.mp4", fout=0.5, overlays=doc(4.0)), "foto_casal"),
    (6.0, dict(video="doc_06_consumo_aparelhos_0m21-0m26.mp4", audio="src", overlays=doc(6.0)), "fala_consumo"),
    (7.2, dict(video="rep_05_RGE_senhora_oxigenio_gasto_corte_da_equipe.mp4", audio="src",
               overlays=[(C_RGE, 0.3, 7.0, 0.3)]), "fala_senhora"),
    (5.5, dict(video="doc_07_mesmo_homem_aparelhos_0m54.mp4", overlays=doc(5.5)), "N2"),
    (4.0, dict(video="rep_06_R7_manchete_filho_aparelhos.mp4", fout=0.6, overlays=[(C_R7, 0.3, 3.6, 0.3)]), "r7"),
    # 3. A pergunta
    (10.0, dict(overlays=[(LUZ, 0.3, 10.0, 1.6), (T_P1, 0.8, 9.8, 0.8), (T_P2, 5.4, 9.8, 1.0)], fout=0.5), "N3"),
    # 4 e 5. A LuzVital (site, só música)
    (6.1, dict(video="site_01_pagina_inicial.mp4", fin=0.8), "site"),
    (10.0, dict(video="site_03_o_que_e_luzvital.mp4"), "site_o_que_e"),
    (5.0, dict(video="site_04_como_funciona.mp4"), "site_como"),
    (22.0, dict(video="site_05_demonstracao.mp4"), "site_demo"),
    (3.5, dict(video="site_06_para_quem_e.mp4", fout=0.4), "site_quem"),
    # 6. O que muda
    (10.0, dict(video="doc_01_equipes_indo_as_casas_1m58-2m08.mp4", fin=0.4, overlays=doc(10.0)), "N9"),
    (5.5, dict(video="doc_05_medico_familia_0m02.mp4", overlays=doc(5.5)), "medico"),
    (6.0, dict(video="doc_08_filho_notebook_familiar_acamado_1m18.mp4", fout=0.4, overlays=doc(6.0)), "filho"),
    (4.0, dict(overlays=[(ODS, 0.0, 4.0, 0.5)]), "ods"),
    # 7. Fechamento
    (9.5, dict(video="doc_04b_medica_so_a_fala_4m56-5m06.mp4", audio="src", fin=0.3, overlays=doc(9.5)), "medica"),
    (3.0, dict(video="doc_09_mae_e_filha_abraco_2m44.mp4", v_ini=1.0, overlays=doc(3.0)), "N11"),
    (3.5, dict(video="doc_10_medica_rindo_com_paciente_2m48.mp4", fout=0.8, overlays=doc(3.3)), "riso"),
    (8.0, dict(overlays=[(CRED, 0.3, 7.8, 0.7)]), "creditos"),
]

# narração: marcador do segmento, atraso (s), arquivo, legendas
NARRACOES = [
    ("N1", 0.2, "narracao_N1_ela_nao_e_um_caso_isolado.wav", 8.1,
     ["Ela não é um caso isolado.", "Quando falta energia, um respirador,",
      "um concentrador de oxigênio, uma bomba de alimentação", "param junto."]),
    ("N2", 0.2, "narracao_N2_mesmo_no_cadastro.wav", 6.7,
     ["Mesmo no cadastro da distribuidora,", "ninguém sabe ao certo quem foi afetado,",
      "quem precisa de ajuda primeiro e quem já está indo."]),
    ("N3", 0.8, "narracao_N3_e_se_no_momento.wav", 4.8, []),  # o texto já está na tela
    ("N9", 2.0, "narracao_N9_nao_devolve_a_energia.wav", 5.7,
     ["Não devolve a energia, não substitui o SAMU.", "Encurta o tempo até alguém saber e agir."]),
    ("N11", 0.5, "narracao_N11_a_energia_pode_acabar.wav", 3.9, []),  # vira a frase final na tela
]

if __name__ == "__main__":
    inicio, t, partes = {}, 0.0, []
    for i, (dur, kw, marca) in enumerate(SEGMENTOS):
        inicio[marca] = t
        partes.append(segmento(i, dur, **kw))
        t += dur
    total = t
    lista = TMP / "lista.txt"
    lista.write_text("".join(f"file '{p.name}'\n" for p in partes))
    base = TMP / "base.mp4"
    run(["-f", "concat", "-safe", "0", "-i", lista, "-c", "copy", base])

    ins, fc, mix = ["-i", base], [], ["[0:a]"]
    v, n, k = "[0:v]", 1, 0

    def sobre(img, a, b, fade=0.25):
        global v, n, k
        ins.extend(["-loop", "1", "-t", total, "-i", img])
        fc.append(f"[{n}:v]format=rgba,fade=t=in:st={a}:d={fade}:alpha=1,fade=t=out:st={b - fade}:d={fade}:alpha=1[s{k}]")
        fc.append(f"{v}[s{k}]overlay=0:0:enable='between(t,{a},{b})'[w{k}]")
        v, n, k = f"[w{k}]", n + 1, k + 1

    falas = []
    for marca, atraso, arq, fala, legendas in NARRACOES:
        t0 = inicio[marca] + atraso
        falas.append((arq, t0))
        soma = sum(len(x) for x in legendas)
        ta = t0
        for j, txt in enumerate(legendas):  # tempo de cada legenda proporcional ao tamanho do texto
            tb = ta + fala * len(txt) / soma
            sobre(png(f"leg_{marca}_{j}", legenda(txt)), round(ta, 2), round(tb + 0.15, 2), 0.12)
            ta = tb
    sobre(FINAL, inicio["N11"] + 0.5, inicio["creditos"] - 0.2, 0.8)

    for arq, t0 in falas:
        ins.extend(["-i", CLIPS / arq])
        fc.append(f"[{n}:a]aresample=48000,aformat=channel_layouts=stereo,adelay={int(t0 * 1000)}:all=1[n{n}]")
        mix.append(f"[n{n}]")
        n += 1
    # a trilha foi composta para o roteiro (música entra em 0:18); aqui ela entra junto com o áudio do JN
    atraso_trilha = inicio["jn_audio"] - 18.0
    ins.extend(["-i", TRILHA / "trilha_dramatica_timeline.wav"])
    fc.append(f"[{n}:a]aresample=48000,aformat=channel_layouts=stereo,adelay={int(atraso_trilha * 1000)}:all=1,volume=1.0[m]")
    mix.append("[m]")
    fc.append(f"{''.join(mix)}amix=inputs={len(mix)}:normalize=0:duration=first,alimiter=limit=0.89[a]")

    final = OUT / "LuzVital_pitch.mp4"
    run([*ins, "-filter_complex", ";".join(fc), "-map", v, "-map", "[a]", "-t", total,
         "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p", "-r", FPS,
         "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", final])
    print(f"ok: {final}  duração {int(total // 60)}:{total % 60:04.1f}")
    for m, t0 in inicio.items():
        print(f"  {int(t0 // 60)}:{t0 % 60:04.1f}  {m}")
