"""
Genera el logotipo y el icono genericos del Conversor LEDES 98BI.

    python assets/make_logo.py

Salida en assets/: logo.png (298x82, se muestra a la mitad en la cabecera) y
app.ico (16-256). Sin marcas de terceros: documento con esquina doblada, barras
de "registro" y el nombre del formato. Dorado sobre carbon, como PrintDeploy: el
logotipo va en la cabecera carbon de la app.
"""
from __future__ import annotations

import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
GOLD = (201, 169, 110)      # ui.GOLD
GOLD_HI = (232, 205, 150)   # dorado claro para el brillo del icono
INK = (22, 22, 24)          # ui.INK
WHITE = (242, 242, 243)     # ui.TEXT_ON_INK


def font(names: list[str], size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for n in names:
        p = os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts", n)
        if os.path.isfile(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def document(d: ImageDraw.ImageDraw, x: float, y: float, w: float, h: float,
             paper, edge, bars, stroke: float) -> None:
    """Hoja con esquina doblada y tres lineas de registro."""
    fold = w * 0.32
    body = [(x, y), (x + w - fold, y), (x + w, y + fold), (x + w, y + h), (x, y + h)]
    d.polygon(body, fill=paper, outline=edge, width=max(1, round(stroke)))
    d.polygon([(x + w - fold, y), (x + w - fold, y + fold), (x + w, y + fold)],
              fill=edge)
    lw = max(1, round(h * 0.075))
    for i, frac in enumerate((0.48, 0.64, 0.80)):
        yy = y + h * frac
        x2 = x + w * (0.78 if i < 2 else 0.55)
        d.rounded_rectangle([x + w * 0.2, yy - lw / 2, x2, yy + lw / 2],
                            radius=lw / 2, fill=bars)


def logo() -> None:
    s = 4  # supermuestreo
    W, H = 298, 82
    im = Image.new("RGBA", (W * s, H * s), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    document(d, 8 * s, 10 * s, 46 * s, 62 * s, INK + (255,), GOLD + (255,),
             GOLD + (255,), 2.6 * s)
    title = font(["seguisb.ttf", "segoeuib.ttf", "arialbd.ttf"], 34 * s)
    sub = font(["segoeui.ttf", "arial.ttf"], 15 * s)
    d.text((68 * s, 12 * s), "LEDES", font=title, fill=WHITE + (255,))
    tw = d.textlength("LEDES ", font=title)
    d.text((68 * s + tw, 12 * s), "98BI", font=title, fill=GOLD + (255,))
    d.text((70 * s, 54 * s), "Conversor de facturación", font=sub,
           fill=(184, 184, 188, 255))
    im.resize((W, H), Image.Resampling.LANCZOS).save(os.path.join(HERE, "logo.png"))


def icon() -> None:
    sizes = [16, 20, 24, 32, 40, 48, 64, 128, 256]
    frames = []
    for n in sizes:
        s = 8
        N = n * s
        im = Image.new("RGBA", (N, N), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        # placa carbon con borde dorado, hoja dorada (como el icono de PrintDeploy)
        bw = max(N * 0.045, s * 1.2)
        d.rounded_rectangle([0, 0, N - 1, N - 1], radius=N * 0.2, fill=INK + (255,),
                            outline=GOLD + (255,), width=round(bw))
        # a tamanos pequenos la hoja ocupa mas y el trazo engorda (si no, desaparece)
        k = 0.58 if n >= 32 else 0.66
        w, h = N * k * 0.78, N * k
        document(d, (N - w) / 2, (N - h) / 2, w, h, GOLD_HI + (255,),
                 GOLD_HI + (255,), INK + (255,), N * 0.02)
        frames.append(im.resize((n, n), Image.Resampling.LANCZOS))
    frames[-1].save(os.path.join(HERE, "app.ico"), sizes=[(n, n) for n in sizes],
                    append_images=frames[:-1])


if __name__ == "__main__":
    logo()
    icon()
    print("assets/logo.png y assets/app.ico generados")
