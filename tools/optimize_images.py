"""Gera as imagens otimizadas (WebP) do site a partir das fotos originais.

Uso:  python3 tools/optimize_images.py     (requer Pillow: pip install pillow)

Cada álbum lista a ordem das fotos (índice na pasta, em ordem alfabética) e um
rótulo usado no texto alternativo (alt). A primeira foto é a capa.
Para trocar a ordem ou incluir/remover fotos, edite as listas abaixo.
"""
import glob
import json
import os
from PIL import Image, ImageOps

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "site", "img")

ALBUMS = {
    "bambu-202": ("Apartamento 202 - Condomínio Bambu", [
        (13, "balcony_sea"), (11, "sea_view"), (7, "living"), (8, "living"), (3, "kitchen"),
        (0, "balcony"), (2, "balcony"), (24, "suite"), (20, "suite"), (22, "suite"),
        (23, "bedroom"), (28, "bedroom"), (25, "bedroom"), (26, "bathroom"), (27, "bathroom"),
        (15, "sea_view"), (18, "living"), (4, "kitchen"), (9, "living"), (21, "suite"),
        (6, "kitchen"), (12, "kitchen"), (14, "balcony"),
    ]),
    "bambu-410": ("Apartamento 410 - Condomínio Bambu", [
        (13, "balcony_sea"), (0, "balcony_sea"), (3, "balcony"), (6, "living"), (2, "balcony"),
        (7, "living"), (4, "kitchen"), (14, "suite"), (15, "suite"), (19, "bedroom"),
        (20, "bedroom"), (11, "bathroom"), (9, "living"), (12, "kitchen"), (1, "balcony"),
        (16, "suite"), (18, "suite"), (17, "bathroom"), (21, "suite"), (22, "bedroom"),
    ]),
    "reserva-dna": ("Apartamento 14.4.1 - Condomínio Reserva DNA", [
        (0, "living"), (1, "kitchen"), (3, "living"), (7, "balcony_bbq"), (18, "suite"),
        (27, "bedroom"), (2, "kitchen"), (6, "living"), (4, "living"), (9, "balcony"),
        (31, "balcony"), (19, "suite"), (29, "bedroom"), (14, "bathroom"), (15, "bathroom"),
        (24, "bathroom"), (25, "kitchen"), (12, "kitchen"), (13, "balcony_bbq"), (37, "living"),
        (16, "living"),
    ]),
    "lazer-bambu": ("Áreas Condomínio Bambu", [
        (2, "infinity_pool"), (7, "infinity_pool"), (8, "deck"), (3, "heated_pool"),
        (6, "heated_pool"), (9, "garden"), (4, "facade"), (11, "lobby"), (14, "lobby"),
        (0, "game_room"), (1, "playroom"), (13, "gym"), (16, "gym"), (10, "sauna"),
        (17, "infinity_pool"), (5, "facade"), (12, "laundry"),
    ]),
    "lazer-dna": ("Áreas Condomínio Reserva DNA", [
        (2, "aerial"), (4, "aerial"), (5, "pool"), (0, "pool"), (9, "pool"), (11, "deck"),
        (12, "deck"), (23, "beach_view"), (33, "deck"), (34, "pool"), (26, "pool"),
        (27, "pool"), (28, "pergola"), (3, "aerial"), (13, "aerial"), (6, "hot_tub"),
        (15, "heated_pool"), (25, "heated_pool"), (19, "hot_tub"), (29, "sauna"),
        (16, "game_room"), (32, "game_room"), (14, "gourmet"), (17, "gym"), (20, "playroom"),
        (22, "playroom"), (10, "deck"), (30, "aerial"), (37, "gym"), (36, "game_room"),
    ]),
}

FULL = 1600   # lado maior da imagem ampliada (lightbox)
THUMB = 720   # lado maior da miniatura (cards e grades)


def save(im, path, size, q):
    im = im.copy()
    im.thumbnail((size, size), Image.LANCZOS)
    im.save(path, "WEBP", quality=q, method=6)
    return im.size


def main():
    manifest = {}
    for slug, (folder, order) in ALBUMS.items():
        files = sorted(glob.glob(os.path.join(ROOT, folder, "*.jpeg")))
        os.makedirs(os.path.join(OUT, slug), exist_ok=True)
        items = []
        for n, (idx, label) in enumerate(order, 1):
            im = ImageOps.exif_transpose(Image.open(files[idx])).convert("RGB")
            base = f"{slug}-ubatuba-{n:02d}"
            w, h = save(im, os.path.join(OUT, slug, base + ".webp"), FULL, 74)
            tw, th = save(im, os.path.join(OUT, slug, base + "-t.webp"), THUMB, 66)
            items.append({"src": f"img/{slug}/{base}.webp", "thumb": f"img/{slug}/{base}-t.webp",
                          "w": w, "h": h, "tw": tw, "th": th, "label": label})
        manifest[slug] = items
        print(slug, len(items))

    # Imagem principal (hero): versão retrato (mobile) + recorte paisagem (desktop) + OG
    hero = ImageOps.exif_transpose(Image.open(os.path.join(ROOT, "imagem header.jpeg"))).convert("RGB")
    W, H = hero.size  # 1200x1600
    os.makedirs(os.path.join(OUT, "hero"), exist_ok=True)
    for s in (640, 960, 1200):
        hero.resize((s, int(H * s / W)), Image.LANCZOS).save(
            os.path.join(OUT, "hero", f"bambu-ubatuba-vista-mar-{s}.webp"), "WEBP", quality=72, method=6)
    land = hero.crop((0, 420, W, 420 + 800))  # horizonte + piscina de borda infinita
    land.save(os.path.join(OUT, "hero", "bambu-ubatuba-vista-mar-wide.webp"), "WEBP", quality=74, method=6)
    og = hero.crop((0, 640, W, 640 + 630))
    og.save(os.path.join(OUT, "hero", "og-bambu-ubatuba.jpg"), "JPEG", quality=80, optimize=True, progressive=True)

    with open(os.path.join(ROOT, "tools", "images.json"), "w") as f:
        json.dump(manifest, f, indent=1)


if __name__ == "__main__":
    main()
