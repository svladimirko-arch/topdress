# -*- coding: utf-8 -*-
"""Адаптация index.html референса GORNICA под TOPDRESS.

Читает ../site-Gornica/index.html, заменяет бренд, контакты, тексты, SEO
и параметры изображений, записывает ../index.html. Все подставляемые данные
взяты из карточки Topdress в 2ГИС (70000001034630663).
"""
import os
from urllib.parse import quote

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "..", "site-Gornica", "index.html")
OUT = os.path.join(HERE, "..", "index.html")

HERO_URL = "images/hero-l.webp"
ROUTE = "https://yandex.ru/maps/?text=" + quote("Казань, улица Бурхана Шахиди, 17", safe="")
MAP = ("https://www.openstreetmap.org/export/embed.html?bbox=49.1013%2C55.7839%2C49.1134%2C55.7899"
       "&amp;layer=mapnik&amp;marker=55.786865%2C49.10733")

JSONLD_OLD = '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "ClothingStore",
  "name": "GORNICA — дом свадебной и вечерней моды",
  "description": "Свадебные и вечерние платья, персональная примерка.",
  "image": "https://svladimirko-arch.github.io/gornica/images/hero-l.webp",
  "url": "https://svladimirko-arch.github.io/gornica/",
  "telephone": "+7 917 858-43-43",
  "openingHours": "Mo-Su 10:00-20:00",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "ул. Сибгата Хакима, 51, ЖК «Столичный», 2 этаж",
    "addressLocality": "Казань",
    "addressCountry": "RU"
  },
  "sameAs": ["https://vk.ru/gornica_kzn", "https://t.me/gornica_kazan"]
}
</script>
<link rel="canonical" href="https://svladimirko-arch.github.io/gornica/">'''

JSONLD_NEW = '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "ClothingStore",
  "name": "TOPDRESS, салон свадебной и вечерней моды",
  "description": "Свадебные и вечерние платья в Казани: прокат, розница, примерка и швейное ателье.",
  "image": "%s",
  "telephone": "+7 919 693-82-00",
  "openingHours": "Mo-Su 09:00-19:00",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "ТОЦ «Модная семья», улица Бурхана Шахиди, 17, 3 этаж",
    "addressLocality": "Казань",
    "postalCode": "420111",
    "addressCountry": "RU"
  },
  "sameAs": [
    "http://t.me/goldenladykzn",
    "https://t.me/+79196938200",
    "https://wa.me/79196938200",
    "https://max.ru/u/f9LHodD0cOL5Zo5wj2c5g6uP-RL6dcGuS_8oECukMPuiANmZfbM9NZVuaNQ"
  ]
}
</script>''' % HERO_URL

BOOK_DIRECT_OLD = '''      <ul class="book__direct rv">
        <li><small>Телефон</small><a href="tel:+79178584343" data-cfg="phone" data-cfg-href="tel">+7 917 858-43-43</a></li>
        <li><small>Telegram</small><a href="https://t.me/gornica_kazan" target="_blank" rel="noopener" data-cfg-href="telegram">@gornica_kazan</a></li>
        <li><small>Часы работы</small><span data-cfg="hours">Ежедневно, 10:00–20:00</span></li>
      </ul>'''

BOOK_DIRECT_NEW = '''      <ul class="book__direct rv">
        <li><small>Телефон</small><a href="tel:+79196938200" data-cfg="phone" data-cfg-href="tel">+7 919 693-82-00</a></li>
        <li><small>WhatsApp</small><a href="https://wa.me/79196938200" target="_blank" rel="noopener" data-cfg-href="whatsapp">Написать</a></li>
        <li><small>Telegram</small><a href="https://t.me/+79196938200" target="_blank" rel="noopener" data-cfg-href="telegramChat">Написать</a></li>
        <li><small>Max</small><a href="https://max.ru/u/f9LHodD0cOL5Zo5wj2c5g6uP-RL6dcGuS_8oECukMPuiANmZfbM9NZVuaNQ" target="_blank" rel="noopener" data-cfg-href="max">Написать</a></li>
        <li><small>Часы работы</small><span data-cfg="hours">Ежедневно, 09:00–19:00</span></li>
      </ul>'''

SOC_OLD = '<a href="https://vk.ru/gornica_kzn" target="_blank" rel="noopener" data-cfg-href="vk">ВКонтакте</a> <span class="sep"></span> <a href="https://t.me/gornica_kazan" target="_blank" rel="noopener" data-cfg-href="telegram">Telegram</a>'
SOC_NEW = ('<a href="https://wa.me/79196938200" target="_blank" rel="noopener" data-cfg-href="whatsapp">WhatsApp</a> '
           '<span class="sep"></span> <a href="https://t.me/+79196938200" target="_blank" rel="noopener" data-cfg-href="telegramChat">Telegram</a> '
           '<span class="sep"></span> <a href="https://max.ru/u/f9LHodD0cOL5Zo5wj2c5g6uP-RL6dcGuS_8oECukMPuiANmZfbM9NZVuaNQ" target="_blank" rel="noopener" data-cfg-href="max">Max</a> '
           '<span class="sep"></span> <a href="http://t.me/goldenladykzn" target="_blank" rel="noopener" data-cfg-href="telegram">Канал</a>')

R = [
    # --- SEO / head ---
    ('<title>GORNICA — свадебные и вечерние платья в Казани | Салон на Сибгата Хакима</title>',
     '<title>TOPDRESS — свадебные и вечерние платья в Казани | Салон на Бурхана Шахиди, 17</title>'),
    ('<meta name="description" content="GORNICA — дом свадебной и вечерней моды в Казани. Платья для самого важного дня и особенных вечеров, персональная примерка. Ул. Сибгата Хакима, 51, ЖК «Столичный». Запишитесь на примерку.">',
     '<meta name="description" content="TOPDRESS — салон свадебной и вечерней моды в Казани. Прокат и покупка платьев, примерка, своё ателье. ТОЦ «Модная семья», ул. Бурхана Шахиди, 17, 3 этаж. Ежедневно 09:00–19:00.">'),
    ('<link rel="icon" type="image/jpeg" href="images/logo.jpg">',
     '<link rel="icon" type="image/webp" href="images/hero-s.webp">'),
    ('<meta property="og:site_name" content="GORNICA">',
     '<meta property="og:site_name" content="TOPDRESS">'),
    ('<meta property="og:title" content="GORNICA — платье, в котором начинается ваша история">',
     '<meta property="og:title" content="TOPDRESS — свадебные и вечерние платья в Казани">'),
    ('<meta property="og:description" content="Свадебные и вечерние платья в Казани. Персональная примерка в ЖК «Столичный».">',
     '<meta property="og:description" content="Свадебные и вечерние платья в Казани. ТОЦ «Модная семья», ул. Бурхана Шахиди, 17. Ежедневно 09:00–19:00.">'),
    ('<meta property="og:image" content="https://svladimirko-arch.github.io/gornica/images/hero-l.webp">',
     '<meta property="og:image" content="%s">' % HERO_URL),
    ('<meta property="og:url" content="https://svladimirko-arch.github.io/gornica/">\n', ''),
    ('imagesrcset="images/hero-s.webp 760w, images/hero-l.webp 1080w"',
     'imagesrcset="images/hero-s.webp 760w, images/hero-l.webp 1440w"'),
    (JSONLD_OLD, JSONLD_NEW),

    # --- Шапка ---
    ('<a class="logo" href="#top" aria-label="GORNICA — на главную">',
     '<a class="logo" href="#top" aria-label="TOPDRESS — на главную">'),
    ('<span class="logo__m">GORNICA</span>\n    <span class="logo__s">свадебная и вечерняя мода</span>',
     '<span class="logo__m">TOPDRESS</span>\n    <span class="logo__s">салон свадебной и вечерней моды</span>'),
    ('<a class="menu__tel" href="tel:+79178584343" data-cfg="phone">+7 917 858-43-43</a>',
     '<a class="menu__tel" href="tel:+79196938200" data-cfg="phone">+7 919 693-82-00</a>'),

    # --- Hero ---
    ('srcset="images/hero-s.webp 760w, images/hero-l.webp 1080w" sizes="(max-width: 900px) 100vw, 62vw"\n           width="1080" height="1440" alt="Невеста в платье с перьями на фоне старинной архитектуры"',
     'srcset="images/hero-s.webp 760w, images/hero-l.webp 1440w" sizes="(max-width: 900px) 100vw, 62vw"\n           width="1440" height="1719" alt="Женщина в свадебном платье — фото Topdress"'),
    ('Дом свадебной и вечерней моды · Казань', 'Салон свадебной и вечерней моды · Казань'),
    ('Gornica · Kazan · 2026', 'Topdress · Kazan · 2026'),

    # --- О салоне ---
    ('<p class="scrub" id="scrub">Мы верим, что идеальное платье не просто подчёркивает красоту. Оно помогает почувствовать себя особенной. Важна каждая деталь: силуэт, ткань, движение и то самое ощущение, когда вы понимаете — это оно.</p>',
     '<p class="scrub" id="scrub">В TOPDRESS помогают найти платье, в котором вы почувствуете себя собой. Свадебные и вечерние образы, спокойная примерка и внимание к посадке — чтобы выбор оставался простым, а впечатление от него — самым важным.</p>'),
    ('      <p class="note rv">Рейтинг <b data-cfg="ratingScore">5,0</b> на Яндекс Картах <span class="sep"></span> <span data-cfg="ratingCount">106 отзывов</span></p>\n', ''),
    ('srcset="images/about1-s.webp 760w, images/about1-l.webp 1440w" sizes="(max-width: 900px) 92vw, 44vw" width="1440" height="1812" loading="lazy" alt="Невеста в воздушном платье с фатиновым шлейфом у окна"',
     'srcset="images/about1-s.webp 760w, images/about1-l.webp 1440w" sizes="(max-width: 900px) 92vw, 44vw" width="1440" height="1719" loading="lazy" alt="Женщина в свадебном платье — фото Topdress"'),
    ('srcset="images/e05-s.webp 760w, images/e05-l.webp 928w" sizes="(max-width: 900px) 46vw, 24vw" width="928" height="1039" loading="lazy" alt="Чёрное вечернее платье с открытыми плечами и пышной юбкой"',
     'srcset="images/e05-s.webp 760w, images/e05-l.webp 896w" sizes="(max-width: 900px) 46vw, 24vw" width="896" height="1146" loading="lazy" alt="Женщина в вечернем платье — фото Topdress"'),

    # --- Коллекции ---
    ('srcset="images/wedding-s.webp 760w, images/wedding-l.webp 1080w" sizes="(max-width: 900px) 92vw, 46vw" width="1080" height="1440" loading="lazy" alt="Невеста в платье с длинным шлейфом на мощёной улице"',
     'srcset="images/wedding-s.webp 760w, images/wedding-l.webp 1440w" sizes="(max-width: 900px) 92vw, 46vw" width="1440" height="1719" loading="lazy" alt="Женщина в свадебном платье — фото Topdress"'),
    ('<p class="col__lead rv">Образы для самого важного дня. От лаконичной элегантности до выразительной роскоши.</p>',
     '<p class="col__lead rv">Образы для самого важного дня: свадебные платья на любой вкус. Выберите то, в котором узнаете себя.</p>'),
    ('srcset="images/evening-s.webp 760w, images/evening-l.webp 1290w" sizes="(max-width: 900px) 70vw, 34vw" width="1290" height="2196" loading="lazy" alt="Модель в красном атласном вечернем платье"',
     'srcset="images/evening-s.webp 760w, images/evening-l.webp 1440w" sizes="(max-width: 900px) 70vw, 34vw" width="1440" height="1833" loading="lazy" alt="Женщина в вечернем платье — фото Topdress"'),
    ('srcset="images/evening2-s.webp 760w, images/evening2-l.webp 1092w" sizes="(max-width: 900px) 40vw, 20vw" width="1092" height="1527" loading="lazy" alt="Модель в красном платье-корсете на фоне бархатных штор"',
     'srcset="images/evening2-s.webp 760w, images/evening2-l.webp 1440w" sizes="(max-width: 900px) 40vw, 20vw" width="1440" height="1833" loading="lazy" alt="Женщина в вечернем платье — фото Topdress"'),

    # --- Примерка ---
    ('srcset="images/fitting-s.webp 760w, images/fitting-l.webp 1440w" sizes="(max-width: 900px) 92vw, 44vw" width="1440" height="2062" loading="lazy" alt="Невеста в платье с шлейфом в зале с росписью на стенах"',
     'srcset="images/fitting-s.webp 760w, images/fitting-l.webp 1125w" sizes="(max-width: 900px) 92vw, 44vw" width="1125" height="1341" loading="lazy" alt="Примерка в салоне Topdress"'),

    # --- Почему ---
    ('<b>06</b> Почему GORNICA', '<b>06</b> Почему TOPDRESS'),
    ('<div><h3>Индивидуальный подбор образа</h3><p>По фигуре, событию и вашему референсу — спокойно и без навязывания.</p></div>',
     '<div><h3>Большой выбор платьев</h3><p>15 свадебных моделей и 159 фотографий готовых образов в галерее салона.</p></div>'),
    ('<div><h3>Внимание к каждой детали</h3><p>Силуэт, ткань, посадка. Если нужно, доведём платье до идеала в швейной мастерской.</p></div>',
     '<div><h3>Своё ателье</h3><p>Швейная мастерская и производство: платье можно доработать под фигуру и пожелания.</p></div>'),
    ('<div><h3>Разнообразие силуэтов и стилей</h3><p>Атлас, кружево, фатин; от лаконичных линий до пышных юбок. Уникальные мировые бренды.</p></div>',
     '<div><h3>Прокат и покупка</h3><p>Прокат свадебных и вечерних платьев, покупка и пошив — всё в одном месте.</p></div>'),
    ('<div><h3>Персональная атмосфера примерки</h3><p>Спокойный темп, чай для гостей и парковка у входа.</p></div>',
     '<div><h3>Удобно добраться</h3><p>3 этаж ТОЦ «Модная семья», широкий лифт, парковка: 70 платных и 1 бесплатное место.</p></div>'),
    ('<p class="why__foot rv">Образ «под ключ» — платье, макияж и причёска в одном месте.</p>',
     '<p class="why__foot rv">Свадебные платья 16 000–90 000 ₽, акционное — 7 000 ₽. Информация не является публичной офертой.</p>'),

    # --- Атмосфера / отзывы ---
    ('<p class="wrap note atm__note">ЖК «Столичный» · 2 этаж · <span data-cfg="hours">Ежедневно, 10:00–20:00</span></p>',
     '<p class="wrap note atm__note">ТОЦ «Модная семья» · 3 этаж · <span data-cfg="hours">Ежедневно, 09:00–19:00</span></p>'),
    ('<p class="eyebrow rv"><i class="hr"></i><b>08</b> Отзывы</p>',
     '<p class="eyebrow rv"><i class="hr"></i><b>08</b> Отзывы из 2ГИС</p>'),
    ('      <div class="rev__score rv">\n        <b data-cfg="ratingScore">5,0</b>\n        <span>из 5 · <span data-cfg="ratingSource">Яндекс Карты</span><br><span data-cfg="ratingCount">106 отзывов</span></span>\n      </div>\n', ''),
    ('<dd data-cfg="hours">Ежедневно, 10:00–20:00</dd>',
     '<dd data-cfg="hours">Ежедневно, 09:00–19:00</dd>'),
    ('<span data-cfg="addressShort">Казань, ул. Сибгата Хакима, 51</span>\n      <span data-cfg="hours">Ежедневно, 10:00–20:00</span>',
     '<span data-cfg="addressShort">Казань, ул. Сибгата Хакима, 51</span>\n      <span data-cfg="hours">Ежедневно, 09:00–19:00</span>'),

    # --- Финал ---
    ('srcset="images/finale-s.webp 760w, images/finale-l.webp 1440w" sizes="100vw" width="1440" height="1916" loading="lazy" alt="Невеста в кружевном платье с прозрачными рукавами среди зелени"',
     'srcset="images/finale-s.webp 760w, images/finale-l.webp 1080w" sizes="100vw" width="1080" height="1289" loading="lazy" alt="Женщина в свадебном платье — фото Topdress"'),

    # --- Запись ---
    ('<p class="book__lead rv">Оставьте заявку — мы свяжемся с вами и подберём удобное время. Или позвоните сами.</p>',
     '<p class="book__lead rv">Позвоните, напишите в мессенджер или оставьте заявку — подберём удобное время для примерки.</p>'),
    (BOOK_DIRECT_OLD, BOOK_DIRECT_NEW),
    ('placeholder="Дата события, пожелания по силуэту"', 'placeholder="Дата события, пожелания по образу"'),

    # --- Контакты ---
    ('<dd data-cfg="addressFull">Казань, ул. Сибгата Хакима, 51, ЖК «Столичный», 2 этаж</dd>',
     '<dd data-cfg="addressFull">Казань, улица Бурхана Шахиди, 17, ТОЦ «Модная семья», 3 этаж</dd>'),
    ('<dt>Телефон</dt><dd><a href="tel:+79178584343" data-cfg="phone" data-cfg-href="tel">+7 917 858-43-43</a></dd>',
     '<dt>Телефон</dt><dd><a href="tel:+79196938200" data-cfg="phone" data-cfg-href="tel">+7 919 693-82-00</a></dd>'),
    ('<div class="ftr__c">\n      <a href="tel:+79178584343" data-cfg="phone" data-cfg-href="tel">+7 917 858-43-43</a>',
     '<div class="ftr__c">\n      <a href="tel:+79196938200" data-cfg="phone" data-cfg-href="tel">+7 919 693-82-00</a>'),
    (SOC_OLD, SOC_NEW),
    ('<a class="btn btn--gold rv" id="route" href="https://yandex.ru/maps/?text=%D0%9A%D0%B0%D0%B7%D0%B0%D0%BD%D1%8C%2C%20%D1%83%D0%BB%D0%B8%D1%86%D0%B0%20%D0%A1%D0%B8%D0%B1%D0%B3%D0%B0%D1%82%D0%B0%20%D0%A5%D0%B0%D0%BA%D0%B8%D0%BC%D0%B0%2C%2051"',
     '<a class="btn btn--gold rv" id="route" href="%s"' % ROUTE),
    ('<iframe id="map" title="Карта: GORNICA, ул. Сибгата Хакима, 51, Казань" loading="lazy" referrerpolicy="no-referrer-when-downgrade"\n        src="https://www.openstreetmap.org/export/embed.html?bbox=49.1405%2C55.8138%2C49.1525%2C55.8198&amp;layer=mapnik&amp;marker=55.816791%2C49.146488"></iframe>',
     '<iframe id="map" title="Карта: TOPDRESS, улица Бурхана Шахиди, 17, Казань" loading="lazy" referrerpolicy="no-referrer-when-downgrade"\n        src="%s"></iframe>' % MAP),

    # --- Подвал ---
    ('<div class="ftr__brand"><span class="logo__m">GORNICA</span><p>Дом свадебной и вечерней моды в Казани. Платье, в котором начинается ваша история.</p></div>',
     '<div class="ftr__brand"><span class="logo__m">TOPDRESS</span><p>Салон свадебной и вечерней моды в Казани. Платья для главного дня и особенных вечеров.</p></div>'),
    ('<span data-cfg="addressShort">Казань, ул. Сибгата Хакима, 51</span>',
     '<span data-cfg="addressShort">Казань, улица Бурхана Шахиди, 17</span>'),
    ('<span class="ftr__soc"><a href="https://vk.ru/gornica_kzn" target="_blank" rel="noopener" data-cfg-href="vk">ВКонтакте</a><a href="https://t.me/gornica_kazan" target="_blank" rel="noopener" data-cfg-href="telegram">Telegram</a></span>',
     '<span class="ftr__soc"><a href="https://wa.me/79196938200" target="_blank" rel="noopener" data-cfg-href="whatsapp">WhatsApp</a><a href="https://t.me/+79196938200" target="_blank" rel="noopener" data-cfg-href="telegramChat">Telegram</a><a href="https://max.ru/u/f9LHodD0cOL5Zo5wj2c5g6uP-RL6dcGuS_8oECukMPuiANmZfbM9NZVuaNQ" target="_blank" rel="noopener" data-cfg-href="max">Max</a></span>'),
    ('<span>© <span id="year">2026</span> GORNICA</span>',
     '<span>© <span id="year">2026</span> TOPDRESS</span>'),
    ('<a class="mbar__tel" href="tel:+79178584343" aria-label="Позвонить" data-cfg-href="tel">',
     '<a class="mbar__tel" href="tel:+79196938200" aria-label="Позвонить" data-cfg-href="tel">'),

    # --- Юр. тексты ---
    ('Вы можете отозвать согласие, позвонив по телефону салона или написав в Telegram.',
     'Вы можете отозвать согласие, позвонив по телефону салона или написав в мессенджер.'),
    ('Отправляя форму, вы даёте согласие GORNICA (Казань, ул. Сибгата Хакима, 51) на обработку',
     'Отправляя форму, вы даёте согласие TOPDRESS (Казань, улица Бурхана Шахиди, 17, ТОЦ «Модная семья», 3 этаж) на обработку'),
]

html = open(SRC, encoding="utf-8").read()
for old, new in R:
    n = html.count(old)
    if n != 1:
        raise SystemExit("Ожидалось 1 вхождение, найдено %d:\n%s" % (n, old[:160]))
    html = html.replace(old, new)

open(OUT, "w", encoding="utf-8", newline="\n").write(html)
print("OK: %d замен, %d байт" % (len(R), len(html.encode("utf-8"))))
