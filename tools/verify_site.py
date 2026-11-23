# -*- coding: utf-8 -*-
"""Быстрая проверка сайта TOPDRESS: конфиг, фото, остатки бренда референса."""
import json
import os
import subprocess
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")

cfg = json.loads(subprocess.check_output([
    "node", "-e",
    "global.window={};require('./assets/config.js');console.log(JSON.stringify(window.TOPDRESS))"
], cwd=ROOT, encoding="utf-8"))

errors = []
if len(cfg["gallery"]) != 30:
    errors.append("gallery != 30")
if len(cfg["atmosphere"]) != 9:
    errors.append("atmosphere != 9")
if len(cfg["reviews"]) != 6:
    errors.append("reviews != 6")

static = ["hero", "about1", "wedding", "evening", "evening2", "fitting", "finale"]
for key in static:
    if not os.path.exists(os.path.join(ROOT, "images", key + "-l.webp")):
        errors.append("нет images/%s-l.webp" % key)

for item in cfg["gallery"] + cfg["atmosphere"]:
    for suf in ("s", "l"):
        path = os.path.join(ROOT, "images", "%s-%s.webp" % (item["k"], suf))
        if not os.path.exists(path):
            errors.append("нет " + os.path.basename(path))
            continue
        if suf == "l":
            size = Image.open(path).size
            if size != (item["w"], item["h"]):
                errors.append("%s: %s != %s" % (item["k"], size, (item["w"], item["h"])))

html = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
for bad in ("GORNICA", "Сибгата", "Яндекс Карты", "79178584343", "106 отзывов", "4,4", "Рейтинг", "ratingScore"):
    if bad in html:
        errors.append("в index.html осталось: " + bad)

print("Фото: %d галерея + %d атмосфера + %d статичных = %d" % (
    len(cfg["gallery"]), len(cfg["atmosphere"]), len(static),
    len(cfg["gallery"]) + len(cfg["atmosphere"]) + len(static)))
print("Ошибок: %d" % len(errors))
for e in errors:
    print(" - " + e)
raise SystemExit(1 if errors else 0)
