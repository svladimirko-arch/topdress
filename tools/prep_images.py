# -*- coding: utf-8 -*-
"""TOPDRESS: подготовка фотографий из галереи 2ГИС для сайта.

Исходники — реальные фото салона из 2ГИС (159 кадров в альбоме организации).
Отобраны 46 кадров, на каждом подтверждено лицо (YuNet). Повторы и кадры без
лица исключены. Нижние 4,5% кадра обрезаются: там может быть водяной знак 2ГИС.

Запуск: python tools/prep_images.py "C:\\path\\to\\source-photos"
На выходе: images/<ключ>-s.webp (до 760 px) и images/<ключ>-l.webp (до 1500 px).
"""
import json, os, sys
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "images")
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "..", "..", "topdress_photos")
os.makedirs(OUT, exist_ok=True)

# ключ -> индекс в topdress_photos/candidates.json (дедуплицированный список с лицами)
MAP = {
    # ключевые кадры
    "hero": 36, "about1": 25, "wedding": 23,
    "evening": 11, "evening2": 44, "fitting": 72, "finale": 69,
    # свадебная галерея (21)
    "w01": 14, "w02": 24, "w03": 27, "w04": 28, "w05": 30, "w06": 37,
    "w07": 38, "w08": 39, "w09": 42, "w10": 43, "w11": 50, "w12": 52,
    "w13": 57, "w14": 58, "w15": 60, "w16": 65, "w17": 67, "w18": 68,
    "w19": 70, "w20": 5, "w21": 2,
    # вечерняя галерея (9)
    "e01": 1, "e02": 3, "e03": 4, "e04": 8, "e05": 9,
    "e06": 12, "e07": 13, "e08": 15, "e09": 17,
    # атмосфера (9)
    "a01": 33, "a02": 53, "a03": 18, "a04": 19, "a05": 21,
    "a06": 22, "a07": 26, "a08": 29, "a09": 31,
}

meta = {}
candidates = json.load(open(os.path.join(SRC, "candidates.json"), encoding="utf-8"))
for key, idx in MAP.items():
    c = candidates[idx]
    im = Image.open(c["file"]).convert("RGB")
    W, H = im.size
    im = im.crop((0, 0, W, int(H * 0.955)))  # водяной знак 2ГИС снизу
    w, h = im.size
    for suf, mx, q in (("s", 760, 76), ("l", 1500, 80)):
        k = min(1.0, mx / w)
        out = im.resize((round(w * k), round(h * k)), Image.LANCZOS) if k < 1 else im
        out.save(os.path.join(OUT, f"{key}-{suf}.webp"), "WEBP", quality=q, method=6)
        if suf == "l":
            meta[key] = {"w": out.width, "h": out.height, "url": c["url"], "src": c["file"]}

json.dump(meta, open(os.path.join(HERE, "sizes.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps({k: [v["w"], v["h"]] for k, v in meta.items()}, ensure_ascii=False))
