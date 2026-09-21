#!/usr/bin/env python3
"""Genera las páginas del sitio de Azul Restaurante.

Ejecutar desde esta carpeta:  python3 build.py
Escribe index.html, menu.html, conoce-azul.html y contacto.html en la carpeta padre.
El header, el menú desplegable, la banda de contacto y el footer se comparten.
Los datos de la carta están en MENU (abajo). Precios en COP, tal como en la carta
publicada en Canva ("CARTA AZUL 3", enlazada desde el Linktree del restaurante).
"""
import html
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')

# ---------------------------------------------------------------- datos
WA_NUM = '573235105573'
WA_TEL = '+57 323 510 5573'
WA_RESERVA = f'https://wa.me/{WA_NUM}?text=Hola%2C%20Azul.%20Quiero%20reservar%20una%20mesa.'
WA_EVENTO = f'https://wa.me/{WA_NUM}?text=Hola%2C%20Azul.%20Quiero%20informaci%C3%B3n%20para%20una%20celebraci%C3%B3n.'
WA_CUENCOS = f'https://wa.me/{WA_NUM}?text=Hola%2C%20Azul.%20Quiero%20saber%20sobre%20los%20cuencos%20de%20mediod%C3%ADa.'
WA_CLANDESTINO = f'https://wa.me/{WA_NUM}?text=Hola%2C%20Azul.%20Quiero%20reservar%20y%20preguntar%20por%20los%20clandestinos.'
IG = 'https://www.instagram.com/azulrestaurantecali/'
FB = 'https://www.facebook.com/azulclandestino/'
MAIL = 'azul.azulrestaurante@gmail.com'
ADDRESS = 'Carrera 5 #2-130, barrio San Antonio'
CITY = 'Cali, Colombia'
MAPS = 'https://maps.app.goo.gl/DkUhVbc9DqKPwAG36'
MAPS_EMBED = 'https://www.google.com/maps?q=azul+Restaurante%2C+Cra.+5+%232-130%2C+Cali%2C+Valle+del+Cauca&output=embed'
CANVA_CARTA = 'https://www.canva.com/design/DAGTgvjahco/Z-BCri-0cz8dW5cpxGTmbg/view'
CANVA_DIA = 'https://www.canva.com/design/DAE2sISrbO4/a6WqI5szoXSBquzjH-Kesw/view'

# Horarios publicados en la ficha de Google Maps del restaurante (confirmar con el cliente)
HOURS = [
    ('Lunes a jueves', '12:00 – 2:30 p. m. · 7:00 – 9:00 p. m.'),
    ('Viernes y sábado', '12:00 – 3:00 p. m. · 7:00 – 10:00 p. m.'),
    ('Domingo', 'Cerrado'),
]

ARROW = '<span class="ic"><svg viewBox="0 0 10 10" fill="none" stroke-width="1.4"><path d="M1 5h8M5.5 1.5 9 5l-3.5 3.5"/></svg></span>'
EXT = '<span class="ic"><svg viewBox="0 0 10 10" fill="none" stroke-width="1.4"><path d="M2 8 8 2M3 2h5v5"/></svg></span>'
EXT_SM = '<svg viewBox="0 0 10 10" fill="none" stroke="currentColor" stroke-width="1.4"><path d="M2 8 8 2M3 2h5v5"/></svg>'
LEAF = '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M20 3c-7 0-12 3-14 8-1.4 3.4-.5 6.6.6 8.4L4 22l1.4 1 2.9-2.7C10 21.4 13 22 15.5 20c4-3.2 4.5-9.4 4.5-17zm-2.2 2.3c-.2 5.6-1 10.2-3.6 12.4-1.6 1.3-3.6 1.2-5 .6C11 15 13 11.8 17 9.5c-4.2 1.4-6.8 4.6-8.3 8-.7-1.4-1-3.6-.1-5.8 1.5-3.7 5.3-6 9.2-6.4z"/></svg>'
CHILI = '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M17.5 2c.3 1.2.1 2.3-.5 3.2 2.4 1.3 4 3.9 4 6.8 0 5.5-6.2 10-13 10-2 0-3.9-.4-5.5-1.1 1.3-.6 2.2-1.6 2.7-2.9C9.6 17.6 12.5 15.4 14 12c1-2.3 1.2-4.6.3-6.6.6-.5 1-1.1 1.2-1.9L17.5 2zM7 16.9c-.4.9-1 1.6-1.9 2.1.9.2 1.9.3 2.9.3 5.6 0 11-3.7 11-8.3 0-2.2-1.2-4.1-3.1-5.1-.1 2-.8 4.1-2 6.1-1.6 2.9-4.3 4.5-6.9 4.9z"/></svg>'
WARN = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M12 3 2.5 20h19L12 3zm0 6v5m0 3v.5"/></svg>'
TAG_VEG = f'<span class="tag tag--veg" title="Opción vegana">{LEAF}</span>'
TAG_HOT = f'<span class="tag tag--hot" title="Picante">{CHILI}</span>'

# ---------------------------------------------------------------- carta
# Cada categoría: id, título, nota opcional y una lista de bloques.
# Bloque = dict con 'items' (lista) y opcionalmente 'title', 'note'.
# Item = (nombre, precio, descripción[, etiquetas]) — precio puede ser:
#   '48.000'                                      precio único
#   {'price': '48.000', 'extra': ('Con pollo', '+ 18.000')}   precio con adición opcional
#   [('Shot', '40.000'), ('Media', '280.000')]    opciones con precio cada una
# Etiquetas: 'veg' (opción vegana, hoja) y 'hot' (picante, ají), tal como en la carta.

MENU = [
    dict(id='entradas', title='Entradas', blocks=[dict(items=[
        ('Berenjenas Casa Blanca', '48.000', 'Berenjena ahumada, menta, tomate, aceitunas negras, queso de cabra.', 'veg'),
        ('Pulpo con aroma mediterráneo', '68.000', 'Pulpo asado, apio, aceitunas negras, aceitunas kalamata, vinagreta de limón.'),
        ('Samosas a mi modo', '48.000', 'Pollo, cebolla, jengibre, limones fermentados, leche de coco, especias de la India.'),
        ('Tuna mediterránea', '48.000', 'Atún fresco, aceitunas kalamata, aceitunas negras, cebolla roja, tomates secos, salsa tzatziki, especias de la casa.', 'hot'),
        ('Los callos del tío', '60.000', 'Garbanzos, chorizo, cerdo, especias de la casa.', 'hot'),
        ('Tomates del sur al sartén', '38.000', 'Tomates frescos, mozzarella de búfala y albahaca.'),
    ])]),

    dict(id='compartir', title='Sharing entradas', note='Entradas para compartir en la mesa, servidas con pan árabe o pan servilleta.', blocks=[dict(items=[
        ('Tabla mediterránea', '48.000', 'Berenjena ahumada, dátiles, pimientos asados, aceitunas negras, ensalada griega, hummus de garbanzo, labneh, queso feta. Acompañada de pan árabe.', 'veg'),
        ('Azul baba ganoush', '45.000', 'Berenjena ahumada con especias de la casa, acompañada de aceitunas, pistacho, limón en salmuera, labneh, tomates confitados y garbanzos. Servido con pan árabe.'),
        ('Plato marroquí', '48.000', 'Hummus de garbanzo, baba ganoush de berenjena, puré de calabaza, tapenade marroquí y frutos secos. Acompañado de pan servilleta.'),
    ])]),

    dict(id='sopas', title='Sopas', blocks=[dict(items=[
        ('Sopa roja', '40.000', 'Tomates, mozzarella, parmesano.', 'veg'),
        ('Sopa de lentejas con aromas Azrú', '40.000', 'Lentejas, especias de Marruecos, limón en salmuera, tomate cherry, hierbabuena.'),
    ])]),

    dict(id='campo', title='Del campo y ensaladas', blocks=[dict(items=[
        ('Ensalada de garbanzos', {'price': '48.000', 'extra': ('Opcional con pollo', '+ 18.000')},
         'Lechugas, cebolla roja, pimentones asados, tomate cherry, aceitunas negras, kalamata, queso feta, ajonjolí, especias de la casa.', 'veg hot'),
        ('Vegetales al sartén', '46.000', 'Berenjenas asadas, aceitunas verdes, tomate, pesto, albahaca, queso mozzarella y parmesano, champiñones y pan servilleta.', 'veg'),
        ('Ensalada de gyozas de pulpo', '58.000', 'Vegetales encurtidos: pepino, zanahoria, cebolla, rábano y apio, aceitunas verdes y negras.'),
        ('Ensalada Azul', {'price': '55.000', 'extra': ('Opcional con pollo', '+ 18.000')},
         'Lechuga, tomates cherry, champiñones, almendras, uchuvas, aceitunas verdes, queso azul, mozzarella, parmesano.', 'veg'),
    ])]),

    dict(id='carnes-rojas', title='Carnes rojas', blocks=[dict(items=[
        ('Lomo Azul', '79.000', 'Queso azul, champiñones, puré de papa.'),
        ('Cuscús de cordero', '78.000', 'Estofado de vegetales.'),
        ('Musaka de cordero a mi modo', '78.000', 'Berenjena ahumada, cebolla, tomate, yogur, queso de cabra, parmesano, especias de la casa.'),
        ('Lomo con aromas al bosque', '78.000', 'Salsa de champiñones secos en vino blanco y especias de la casa. Acompañado de calabacín asado y tomates confitados.'),
        ('Entre el Mediterráneo', '68.000', 'Pan árabe, carne molida, grasa de cordero, pimienta, tomate, cebolla, aceitunas verdes, pimientos asados, aceite de oliva, mozzarella, parmesano, yogur y papas crocantes.'),
    ])]),

    dict(id='arroces', title='Arroces', blocks=[dict(items=[
        ('Meloso de conejo', '75.000', 'Timbal de conejo con albaricoque y dátiles, sobre arroz cremoso de queso de cabra.'),
        ('Caldoso de mar', '79.000', 'Arroz de mariscos (camarón, calamar y mejillones), con ensaladilla de la casa.'),
    ])]),

    dict(id='carnes-blancas', title='Carnes blancas', blocks=[dict(items=[
        ('Pollo en Tikkazul', '68.000', 'Pollo con masala y leche de coco. Acompañado de arroz basmati y almendras.', 'hot'),
        ('Pollo en alcaparras', '68.000', 'Pollo, pesto rojo (tomates secos), alcaparras, parmesano. Acompañado de pasta larga.'),
        ('Pollo siete perfumes', '65.000', 'Cuscús con tomates cherry, berenjena ahumada, aceitunas, dátiles, yerbabuena, especias de la casa y yogur.'),
    ])]),

    dict(id='de-mar', title='De mar', blocks=[dict(items=[
        ('Pescado fresco con aromas al Mediterráneo', '86.000', 'Pescado fresco a la sartén, mantequilla con hierbas mediterráneas. Acompañado de vegetales asados bañados en salsa rústica de tomates.'),
        ('Envuelto de pescado y camarón', '88.000', 'Trocitos de pescado salteados en cebolla, pimentón, leche de coco, especias. Acompañados de arroz aromatizado en hoja de plátano.'),
        ('Mejillones con aromas del sur', '68.000', 'Cebolla, tomate, chorizo español, pimentón dulce y picante. Papas crocantes.'),
    ])]),

    dict(id='pastas', title='Pastas', note='Todas se pueden pedir con pasta de arroz.', blocks=[dict(items=[
        ('Marrakech', '58.000', 'Aceitunas verdes y negras, alcaparras, tomate, limón en salmuera, yogur, berenjena, hierbabuena, queso fresco.', 'veg'),
        ('Mediterránea', '58.000', 'Tomates cherry, pimentón, aceitunas negras, berenjena, alcachofas, pesto rojo, variedad de quesos. Es una pasta a temperatura ambiente.', 'veg'),
        ('Pasta al limón y camarón', '69.000', 'Camarones salteados con tomillo, almendras y un toque de limón.'),
    ])]),

    dict(id='infantil', title='Menú infantil', blocks=[dict(items=[
        ('Pasta napolitana', {'price': '30.000', 'extra': ('Opcional con pollo', '+ 18.000')}, 'Tomate, albahaca, queso parmesano.'),
    ])]),

    dict(id='clandestinos', title='Clandestinos', text='Un clandestino es un plato único preparado e inspirado en ti. Si Martha se encuentra, pregunta por los clandestinos.', blocks=[]),

    dict(id='postres', title='Postres', blocks=[dict(items=[
        ('Mousse de limón', '26.000', 'Limones en salmuera, frutos rojos y agua de azahar.'),
        ('Torta caliente de chocolate', '32.000', 'Con helado.'),
        ('Tierra de chocolate', '28.000', 'Con mousse de maracuyá.'),
        ('Rollo de frutos secos', '32.000', 'Con yogur aromatizado.'),
    ])]),

    dict(id='cocteles', title='Cócteles y aperitivos', blocks=[
        dict(title='Cócteles', items=[
            ('Old fashioned a mi modo', '48.000', 'Bourbon, jarabe, Angostura bitter, soda y cereza.'),
            ('Manhattan vermouth', '48.000', 'Bourbon, vermouth rosso y Angostura bitter.'),
            ('Gin tonic', '48.000', 'Ginebra y tónica.'),
            ('Dry martini', '48.000', 'Ginebra, dry vermouth y aceitunas verdes.'),
            ('Negroni', '48.000', 'Campari, vermouth rosso, ginebra y naranja.'),
            ('Margarita tradicional', '46.000', 'Tequila blanco, Cointreau y zumo de limón.'),
            ('Margarita especial', '58.000', 'Tequila Don Julio añejo, Cointreau y zumo de limón.'),
            ('Mojito tradicional', '42.000', 'Ron blanco, azúcar, limón, hierbabuena y soda.'),
            ('Mojito Zacapa 23', '58.000', 'Ron Zacapa, hierbabuena y soda.'),
        ]),
        dict(title='Sin licor', items=[
            ('Mojito virgen', '26.000', 'Limón, azúcar, hierbabuena y ginger.'),
        ]),
        dict(title='Aperitivos', items=[
            ('Aperol', '42.000', ''), ('Dubonnet', '36.000', ''), ('Campari', '36.000', ''),
            ('Jerez', '36.000', ''), ('Vermouth rosso', '38.000', ''),
        ]),
        dict(title='Digestivos', items=[
            ('Cointreau', '38.000', 'Shot.'), ('Amaretto Disaronno', '38.000', 'Shot.'),
        ]),
    ]),

    dict(id='vinos', title='Sangría y vinos', blocks=[
        dict(title='Refrescantes', items=[
            ('Sangría', [('Copa', '45.000'), ('Jarra', '155.000')], 'De vino tinto o blanco.'),
            ('Vino de verano', [('Copa', '40.000'), ('Jarra', '140.000')], 'Tinto o blanco.'),
        ]),
        dict(title='Vinos blancos', items=[
            ('Piccolo de vino blanc (Livana)', '40.000', ''),
            ('San Felipe Chardonnay', '140.000', ''),
            ('Pinot Grigio Zonin', '168.000', ''),
            ('Gérard Bertrand Gris Blanc', '168.000', ''),
            ('Flor de Vetus Verdejo', '230.000', ''),
            ('Marqués de Vizhoja Albariño', '230.000', ''),
        ]),
        dict(title='Cava', items=[('Alta Vista Extra Brut', '230.000', '')]),
        dict(title='Vinos rosados', items=[('Luis Felipe Edwards Rosé', '140.000', '')]),
        dict(title='Vinos tintos', items=[
            ('Piccolo de vino (Chile)', '40.000', ''),
            ('Luis Felipe Edwards Gran Reserva Carmenere', [('Media', '90.000'), ('Botella', '185.000')], ''),
            ('San Felipe Malbec', '140.000', ''),
            ('Altos de las Hormigas Malbec (Argentina)', '270.000', ''),
        ]),
    ]),

    dict(id='licores', title='Licores', blocks=[
        dict(title='Whisky y ron', items=[
            ('Chivas Regal 18 años', '65.000', 'Shot.'),
            ('Old Parr 12 años', [('Shot', '40.000'), ('Media', '280.000')], ''),
            ("Buchanan's 12 años", [('Shot', '40.000'), ('Media', '280.000')], ''),
            ('Ron Havana Club 7 años', '40.000', 'Shot.'),
            ('Ron Zacapa 23 años', '68.000', 'Shot.'),
        ]),
        dict(title='Ginebra, tequila, vodka y aguardiente', items=[
            ('Ginebra Bombay Sapphire', '40.000', 'Shot.'),
            ('Ginebra Tanqueray', '42.000', 'Shot.'),
            ("Ginebra Hendrick's", '48.000', 'Shot.'),
            ('Tequila Don Julio reposado', '65.000', 'Shot.'),
            ('Vodka Absolut', [('Shot', '35.000'), ('Media', '190.000')], ''),
            ('Aguardiente del Valle', [('Shot', '26.000'), ('Media', '80.000')], ''),
        ]),
    ]),

    dict(id='bebidas', title='Bebidas y cervezas', blocks=[
        dict(title='Bebidas', items=[
            ('Limonada', '15.000', ''), ('Limonada de azahar', '16.000', ''),
            ('Soda italiana', '18.000', 'Fruta de temporada.'),
            ('Agua San Pellegrino', '18.500', ''),
            ('Coca-Cola', '9.000', ''), ('Soda Bretaña', '9.000', ''), ('Ginger Canada Dry', '9.000', ''),
            ('Agua Hatsu', '7.500', 'Con gas o sin gas.'),
            ('Tónica 1976', '14.000', ''), ('Café', '8.500', ''), ('Agua aromática', '6.000', ''),
        ]),
        dict(title='Cervezas', items=[
            ('Club Colombia rubia', '14.500', ''), ('Poker', '14.500', ''),
            ('Stella Artois', '18.000', ''), ('Corona', '18.000', ''),
            ('Michelado', '+ 3.500', ''),
        ]),
    ]),
]

# ---------------------------------------------------------------- helpers
def price_html(p):
    if isinstance(p, str):
        return f'<span class="menu-item__price">{p}</span>'
    if isinstance(p, dict) and 'price' in p:
        return f'<span class="menu-item__price">{p["price"]}</span>'
    return '<span class="menu-item__price"></span>'


def item_html(name, price, desc, tags=''):
    marks = ''
    if 'veg' in tags:
        marks += TAG_VEG
    if 'hot' in tags:
        marks += TAG_HOT
    out = f'<div class="menu-item"><span class="menu-item__name">{html.escape(name)}{marks}</span>'
    if isinstance(price, list):
        out += '<span class="menu-item__price"></span>'
        if desc:
            out += f'<p class="menu-item__desc">{html.escape(desc)}</p>'
        out += '<div class="menu-item__opts">' + ''.join(
            f'<span>{html.escape(n)}</span><span>{v}</span>' for n, v in price) + '</div>'
    else:
        out += price_html(price)
        if desc:
            out += f'<p class="menu-item__desc">{html.escape(desc)}</p>'
        if isinstance(price, dict) and price.get('extra'):
            n, v = price['extra']
            out += f'<div class="menu-item__opts"><span>{html.escape(n)}</span><span>{v}</span></div>'
    return out + '</div>'


def block_html(b):
    out = '<div class="menu-sub">'
    if b.get('title'):
        note = f'<span class="menu-sub__note">{html.escape(b["note"])}</span>' if b.get('note') else ''
        out += f'<h4 class="label menu-sub__title">{html.escape(b["title"])}{note}</h4>'
    elif b.get('note'):
        out += f'<p class="menu-cat__note">{html.escape(b["note"])}</p>'
    out += ''.join(item_html(*it) for it in b['items'])
    return out + '</div>'


def cat_html(c):
    note = f'<p class="menu-cat__note">{html.escape(c["note"])}</p>' if c.get('note') else ''
    out = f'<section class="menu-cat" id="{c["id"]}">'
    out += f'<div class="menu-cat__head"><h2 class="menu-cat__title">{html.escape(c["title"])}</h2>{note}</div>'
    if c.get('text'):
        out += f'<div class="menu-clandestino"><p class="lede">{html.escape(c["text"])}</p><a class="arrow-link on-light" href="{WA_CLANDESTINO}" target="_blank" rel="noopener">Reservar y preguntar {ARROW}</a></div>'
    blocks = c['blocks']
    if len(blocks) > 1 and c['id'] in ('cocteles', 'vinos', 'licores', 'bebidas'):
        out += '<div class="menu-cat__cols">' + ''.join(block_html(b) for b in blocks) + '</div>'
    else:
        out += ''.join(block_html(b) for b in blocks)
    return out + '</section>'


def hours_html(cls='hours-list'):
    return f'<ul class="{cls}">' + ''.join(f'<li><span>{html.escape(d)}</span><span>{html.escape(h)}</span></li>' for d, h in HOURS) + '</ul>'


# ---------------------------------------------------------------- plantilla
FONTS = 'https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@110,400;110,500;125,400;125,500&family=Bodoni+Moda:wght@400&family=DM+Sans:wght@300;400;500&display=swap'


def head(title, desc, og_img, body_class, preload=None):
    preload_tags = ''
    if preload:
        preload_tags = '\n  ' + '\n  '.join(preload)
    return f'''<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{html.escape(title)}</title>
  <meta name="description" content="{html.escape(desc)}">
  <meta name="theme-color" content="#121A1A">
  <link rel="icon" type="image/png" href="img/favicon.png">
  <link rel="apple-touch-icon" href="img/favicon.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>{preload_tags}
  <link rel="preload" as="style" href="{FONTS}">
  <link rel="stylesheet" href="{FONTS}" media="print" onload="this.media='all'">
  <noscript><link rel="stylesheet" href="{FONTS}"></noscript>
  <link rel="stylesheet" href="css/style.css">
  <meta property="og:title" content="{html.escape(title)}">
  <meta property="og:description" content="{html.escape(desc)}">
  <meta property="og:image" content="img/{og_img}">
  <meta property="og:type" content="website">
</head>
<body class="{body_class}">'''


HEADER = f'''
  <header class="header">
    <div class="header__bar">
      <a class="btn-outline header__cta" href="{WA_RESERVA}" target="_blank" rel="noopener"><span class="full">Reservar mesa</span><span class="short">Reservar</span></a>
      <a class="header__logo" href="index.html" aria-label="Azul Restaurante, inicio">
        <img class="light" src="img/logo-blanco.png" alt="azul" width="1969" height="788">
        <img class="dark" src="img/logo-color.png" alt="" width="1969" height="788">
      </a>
      <button class="header__burger" aria-label="Abrir menú" aria-expanded="false" aria-controls="nav"><span></span></button>
    </div>
  </header>
  <div class="nav__scrim"></div>
  <nav class="nav" id="nav" aria-label="Principal">
    <div class="nav__panel">
      <div class="nav__links">
        <a href="index.html">Inicio</a>
        <a href="menu.html">Carta</a>
        <a href="conoce-azul.html">Conoce Azul</a>
        <a href="contacto.html">Contacto</a>
      </div>
      <div class="nav__ext">
        <a class="arrow-link ext" href="{IG}" target="_blank" rel="noopener">Instagram {EXT}</a>
        <a class="arrow-link ext" href="{FB}" target="_blank" rel="noopener">Facebook {EXT}</a>
        <a class="arrow-link ext" href="{WA_RESERVA}" target="_blank" rel="noopener">WhatsApp {EXT}</a>
      </div>
      <div class="nav__media">
        <picture>
          <source type="image/webp" srcset="img/barra-nav.webp">
          <img src="img/barra-nav.jpg" alt="La barra de Azul" loading="lazy" decoding="async">
        </picture>
        <div class="cap"><span class="label">Cocina con aromas</span><img src="img/logo-blanco.png" alt=""><span class="label">San Antonio · Cali</span></div>
      </div>
    </div>
  </nav>
'''

CONTACT_BAND = f'''
  <section class="contact-band">
    <div class="grid">
      <div class="contact-band__title reveal">
        <p class="label">Contacto y ubicación</p>
        <h2>Reserva tu mesa en San Antonio</h2>
      </div>
      <div class="contact-band__info reveal reveal-d1">
        <p>WhatsApp <a href="{WA_RESERVA}" target="_blank" rel="noopener">{WA_TEL}</a><br>Correo <a href="mailto:{MAIL}">{MAIL}</a></p>
        <p><a href="{MAPS}" target="_blank" rel="noopener">{ADDRESS}<br>{CITY}</a></p>
        <p>Lunes a sábado, almuerzo y cena · Domingo cerrado</p>
      </div>
    </div>
  </section>
'''

FOOTER = f'''
  <footer class="footer">
    <div class="footer__top">
      <div class="footer__brand reveal">
        <picture>
          <source type="image/webp" srcset="img/fachada-thumb.webp">
          <img src="img/fachada-thumb.jpg" alt="Fachada de Azul en el barrio San Antonio" loading="lazy" decoding="async" width="150" height="200">
        </picture>
        <div>
          <p>Aromas mediterráneos, India y norte de África en una casa del barrio San Antonio, Cali.</p>
          <a class="arrow-link on-light" href="conoce-azul.html">Conoce Azul {ARROW}</a>
        </div>
      </div>
      <div class="footer__nav reveal reveal-d1">
        <p class="label footer__col-title">Navegación</p>
        <ul>
          <li><a href="index.html">Inicio</a></li>
          <li><a href="menu.html">Carta</a></li>
          <li><a href="conoce-azul.html">Conoce Azul</a></li>
          <li><a href="contacto.html">Contacto</a></li>
        </ul>
        <ul>
          <li><a href="{IG}" target="_blank" rel="noopener">Instagram {EXT_SM}</a></li>
          <li><a href="{FB}" target="_blank" rel="noopener">Facebook {EXT_SM}</a></li>
          <li><a href="{MAPS}" target="_blank" rel="noopener">Cómo llegar {EXT_SM}</a></li>
        </ul>
      </div>
      <div class="footer__order reveal reveal-d2">
        <p class="label footer__col-title">Reservas</p>
        <p>Escríbenos por WhatsApp con la fecha, la hora y el número de personas.</p>
        <a class="btn-solid" href="{WA_RESERVA}" target="_blank" rel="noopener">Reservar por WhatsApp</a>
        <a class="tel" href="tel:+573235105573">{WA_TEL}</a>
      </div>
    </div>
    <div class="footer__wordmark" aria-hidden="true">
      <img src="img/logo-color.png" alt="" loading="lazy" decoding="async" width="1969" height="788">
      <span class="label">Cocina con aromas · San Antonio, Cali</span>
    </div>
    <div class="footer__legal">
      <span>Azul Restaurante © 2026 · Todos los derechos reservados</span>
      <span>{CITY}</span>
    </div>
  </footer>
  <a class="wa-float" href="{WA_RESERVA}" target="_blank" rel="noopener" aria-label="Escríbenos por WhatsApp"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.6.8-.8 1-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.8 12 12 0 0 0 4.6 4c1.7.7 2.4.8 3.2.7a2.8 2.8 0 0 0 1.8-1.3 2.2 2.2 0 0 0 .2-1.3c-.1-.1-.3-.2-.5-.3z"/></svg></a>
  <script src="js/main.js" defer></script>
</body>
</html>
'''


def card(img, title, price, text, anchor, badge=''):
    b = f'<span class="card__badge">{badge}</span>' if badge else ''
    webp = img.replace('.jpg', '.webp')
    return f'''        <article class="card">
          <picture>
            <source type="image/webp" srcset="img/{webp}">
            <img src="img/{img}" alt="{html.escape(title)}" loading="lazy" decoding="async">
          </picture>
          <div class="card__head">{b}<h3 class="h3 card__title">{html.escape(title)}</h3><span class="card__price">{price}</span></div>
          <div>
            <p class="card__text">{html.escape(text)}</p>
            <a class="arrow-link on-dark" href="menu.html#{anchor}">Ver en la carta {ARROW}</a>
          </div>
        </article>
'''


def picture(name, alt, mobile=None, cls='', extra=''):
    """<picture> con webp/jpg y, si se indica, una variante para celular."""
    if mobile:
        return f'''<picture>
          <source type="image/webp" media="(max-width: 767px)" srcset="img/{mobile}.webp">
          <source type="image/webp" srcset="img/{name}.webp">
          <source media="(max-width: 767px)" srcset="img/{mobile}.jpg">
          <img src="img/{name}.jpg" alt="{html.escape(alt)}" {extra}>
        </picture>'''
    return f'''<picture>
          <source type="image/webp" srcset="img/{name}.webp">
          <img src="img/{name}.jpg" alt="{html.escape(alt)}" {extra}>
        </picture>'''


def hero_preload(name, mobile=None):
    if mobile:
        return [f'<link rel="preload" as="image" href="img/{mobile}.webp" type="image/webp" media="(max-width: 767px)">',
                f'<link rel="preload" as="image" href="img/{name}.webp" type="image/webp" media="(min-width: 768px)">']
    return [f'<link rel="preload" as="image" href="img/{name}.webp" type="image/webp">']


# ---------------------------------------------------------------- páginas
def page_index():
    return head('Azul Restaurante · Aromas mediterráneos, India y norte de África · San Antonio, Cali',
                'Restaurante en el barrio San Antonio de Cali con aromas del Mediterráneo, la India y el norte de África: entradas para compartir, cordero, arroces, pastas, cócteles y vinos. Reservas por WhatsApp.',
                'og.jpg', 'page-inicio', preload=hero_preload('tabla', 'tabla-m')) + '''
  <div class="preloader" aria-hidden="true"><p>Aromas mediterráneos, India<br>y norte de África. <em>Azul</em>,<br>en San Antonio.</p></div>''' + HEADER + f'''
  <main>
    <section class="hero">
      <div class="hero__media">
        {picture('tabla', 'Cuencos de cobre con entradas para compartir en Azul', 'tabla-m', extra='fetchpriority="high" decoding="async"')}
      </div>
      <p class="label hero__label reveal">Azul Restaurante <span class="sub">San Antonio · Cali</span></p>
      <h1 class="hero__title reveal reveal-d1">Cocina con aromas</h1>
      <div class="hero__foot reveal reveal-d2">
        <div>
          <p class="lede">Aromas mediterráneos, India y norte de África: berenjena ahumada, cordero, arroces, especias y una barra de cócteles, en una casa del barrio San Antonio.</p>
          <div class="hero__actions">
            <a class="arrow-link on-dark" href="menu.html">Ver la carta {ARROW}</a>
            <a class="arrow-link on-dark" href="{WA_RESERVA}" target="_blank" rel="noopener">Reservar {ARROW}</a>
          </div>
        </div>
      </div>
    </section>

    <section class="split">
      <div class="split__media">
        {picture('barra', 'Botellas y flores secas en la barra de Azul', 'barra-m', extra='loading="lazy" decoding="async"')}
      </div>
      <div class="split__panel">
        <div>
          <p class="label reveal">La barra</p>
          <h2 class="reveal reveal-d1">Cócteles, vinos y sangría</h2>
        </div>
        <div class="split__foot reveal reveal-d2">
          <p class="lede">Negroni, dry martini, old fashioned a mi modo, sangría y vino de verano por copa o jarra, y una selección de vinos blancos, tintos, rosados y cava.</p>
          <a class="arrow-link on-dark" href="menu.html#cocteles">Ver tragos y bebidas {ARROW}</a>
        </div>
      </div>
    </section>

    <section class="full-image">
      {picture('pasta', 'Pasta al limón y camarón de Azul', 'pasta-m', extra='loading="lazy" decoding="async"')}
    </section>

    <section class="intro on-sand">
      <div class="grid">
        <p class="label intro__label reveal">Bienvenidos a Azul</p>
        <div class="intro__body">
          <h2 class="reveal">Tres cocinas en una mesa</h2>
          <p class="lede reveal reveal-d1">Azul reúne los aromas del Mediterráneo, de la India y del norte de África: hummus y baba ganoush, cuscús y musaka de cordero, pollo con masala y leche de coco, arroces melosos y pastas con limón en salmuera. Platos para compartir, en una casa del barrio San Antonio.</p>
          <a class="arrow-link on-light reveal reveal-d2" href="menu.html">Ver la carta completa {ARROW}</a>
        </div>
      </div>
    </section>

    <section class="cards on-sand">
      <div class="cards__head reveal">
        <p class="label">Platos destacados</p>
        <a class="arrow-link on-light" href="menu.html">Carta completa {ARROW}</a>
      </div>
      <div class="cards__track reveal reveal-d1">
{card('card-tabla.jpg', 'Tabla mediterránea', '$48.000', 'Berenjena ahumada, dátiles, pimientos asados, aceitunas negras, ensalada griega, hummus, labneh y queso feta, con pan árabe.', 'compartir', 'Para compartir')}{card('card-lomo.jpg', 'Lomo con aromas al bosque', '$78.000', 'Salsa de champiñones secos en vino blanco y especias de la casa, con calabacín asado y tomates confitados.', 'carnes-rojas')}{card('card-pasta.jpg', 'Pasta al limón y camarón', '$69.000', 'Camarones salteados con tomillo, almendras y un toque de limón. También con pasta de arroz.', 'pastas')}{card('card-sangria.jpg', 'Sangría', '$45.000 la copa', 'De vino tinto o blanco, por copa o en jarra para toda la mesa.', 'vinos', 'La barra')}{card('card-rollo.jpg', 'Rollo de frutos secos', '$32.000', 'Con yogur aromatizado. Uno de los cuatro postres de la carta, junto al mousse de limón y la tierra de chocolate.', 'postres', 'Postre')}      </div>
      <div class="cards__nav">
        <button data-prev aria-label="Anterior"><svg viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="1.3"><path d="M11 6H1M5 1.5 1 6l4 4.5"/></svg></button>
        <div class="cards__bar"><i></i></div>
        <button data-next aria-label="Siguiente"><svg viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="1.3"><path d="M1 6h10M7 1.5 11 6l-4 4.5"/></svg></button>
      </div>
    </section>

    <section class="exp on-cream">
      <div class="exp__head reveal">
        <div>
          <p class="label">Lo que hace a Azul</p>
          <h2>Cocina a tu medida</h2>
        </div>
        <a class="arrow-link on-light" href="conoce-azul.html">Conoce Azul {ARROW}</a>
      </div>
      <div class="exp__grid">
        <article class="exp-item exp-item--text reveal">
          <span class="exp-item__num">01</span>
          <div class="exp-item__body">
            <h3 class="exp-item__title">Los clandestinos</h3>
            <span class="label exp-item__sub">Un plato único</span>
            <p class="exp-item__text">Un clandestino es un plato único preparado e inspirado en ti. Si Martha se encuentra, pregunta por los clandestinos.</p>
            <a class="arrow-link on-light" href="{WA_CLANDESTINO}" target="_blank" rel="noopener">Reservar y preguntar {ARROW}</a>
          </div>
        </article>
        <article class="exp-item exp-item--text reveal reveal-d1">
          <span class="exp-item__num">02</span>
          <div class="exp-item__body">
            <h3 class="exp-item__title">Opción vegana</h3>
            <span class="label exp-item__sub">Cocina para todos</span>
            <p class="exp-item__text">En los platos marcados con la hoja se puede excluir cualquier producto de origen animal. Si eres intolerante o alérgico, avísanos: las recetas llevan frutos secos, harinas, lácteos, mariscos y picante, entre otros.</p>
            <a class="arrow-link on-light" href="menu.html">Ver la carta {ARROW}</a>
          </div>
        </article>
        <article class="exp-item exp-item--text reveal reveal-d2">
          <span class="exp-item__num">03</span>
          <div class="exp-item__body">
            <h3 class="exp-item__title">Cuencos de mediodía</h3>
            <span class="label exp-item__sub">Al almuerzo</span>
            <p class="exp-item__text">Al mediodía Azul tiene una propuesta propia, los cuencos de mediodía. La carta del día se publica aparte; consúltala o pregúntanos por WhatsApp.</p>
            <a class="arrow-link on-light ext" href="{CANVA_DIA}" target="_blank" rel="noopener">Ver el menú del día {EXT}</a>
          </div>
        </article>
      </div>
    </section>

    <section class="about on-mist">
      <div class="grid">
        <p class="label about__label reveal">Reservas</p>
        <div class="about__media reveal reveal-d1">
          {picture('fachada', 'Puerta de Azul en la Carrera 5 #2-130, San Antonio', extra='loading="lazy" decoding="async"')}
        </div>
        <div class="about__body">
          <h2 class="reveal">Una casa en San Antonio</h2>
          <p class="lede reveal reveal-d1">Estamos en la Carrera 5 #2-130, en el barrio San Antonio de Cali. Reserva por WhatsApp y cuéntanos si celebras algo: para fechas especiales preparamos menús de celebración.</p>
          <div class="reveal reveal-d2">{hours_html()}</div>
          <ul class="pill-list reveal reveal-d2">
            <li>Reservas por WhatsApp</li><li>Menú infantil</li><li>Opción vegana</li><li>Celebraciones</li>
          </ul>
          <a class="arrow-link on-light reveal reveal-d2" href="{WA_RESERVA}" target="_blank" rel="noopener">Reservar por WhatsApp {ARROW}</a>
        </div>
      </div>
    </section>
  </main>''' + CONTACT_BAND + FOOTER


def page_menu():
    nav = ''.join(f'<a href="#{c["id"]}">{html.escape(c["title"])}</a>' for c in MENU)
    cats = ''.join(cat_html(c) for c in MENU)
    return head('Carta · Azul Restaurante, San Antonio, Cali',
                'Carta completa de Azul: entradas para compartir, sopas, ensaladas, cordero, arroces, pollo, pescado, pastas, postres, cócteles, sangría, vinos y licores. Precios en pesos colombianos.',
                'og.jpg', 'page-menu', preload=hero_preload('pasta', 'pasta-m')) + HEADER + f'''
  <main>
    <section class="hero hero--short">
      <div class="hero__media">
        {picture('pasta', 'Pasta al limón y camarón de Azul', 'pasta-m', extra='fetchpriority="high" decoding="async"')}
      </div>
      <p class="label hero__label reveal">Azul Restaurante <span class="sub">Carta</span></p>
      <h1 class="hero__title reveal reveal-d1">Nuestra carta</h1>
      <div class="hero__foot reveal reveal-d2">
        <div>
          <p class="lede">Entradas para compartir, cordero, arroces, pescado, pastas y una barra de cócteles y vinos. Precios en pesos colombianos.</p>
          <div class="hero__actions">
            <a class="arrow-link on-dark" href="{WA_RESERVA}" target="_blank" rel="noopener">Reservar mesa {ARROW}</a>
            <a class="arrow-link on-dark" href="#cocteles">Tragos y bebidas {ARROW}</a>
          </div>
        </div>
      </div>
    </section>

    <nav class="menu-nav" aria-label="Categorías de la carta"><div class="menu-nav__track">{nav}</div></nav>

    <section class="menu-page on-cream">
      <div class="menu-page__intro">
        <h2 class="reveal">Aromas mediterráneos, India y norte de África</h2>
        <div class="reveal reveal-d1">
          <p class="lede">Platos pensados para compartir. Los clandestinos, platos únicos preparados e inspirados en ti, se piden en la mesa.</p>
          <div class="menu-legend">
            <span><i class="tag--veg">{LEAF}</i>Opción vegana</span>
            <span><i class="tag--hot">{CHILI}</i>Picante</span>
          </div>
        </div>
      </div>
      {cats}
      <div class="menu-band reveal">
        <div>
          <h3>¿Reservamos?</h3>
          <p>Escríbenos por WhatsApp con la fecha, la hora y el número de personas. Si quieres un clandestino o celebras algo, cuéntanos desde ya.</p>
        </div>
        <div class="menu-band__actions">
          <a class="btn-outline" href="{WA_RESERVA}" target="_blank" rel="noopener">Reservar mesa</a>
          <a class="btn-outline" href="{CANVA_DIA}" target="_blank" rel="noopener">Menú del día</a>
        </div>
      </div>
      <p class="menu-note">Precios en pesos colombianos (COP) según la carta vigente; pueden cambiar sin previo aviso. <span class="tag--veg" style="display:inline-block;width:11px;height:11px;vertical-align:-1px">{LEAF}</span> Opción vegana: se puede excluir cualquier producto de origen animal. Si eres intolerante o alérgico, avísanos: nuestras recetas contienen frutos secos, harinas, lácteos, mariscos, vegetales, frutas y picante, entre otros. Se prohíbe el expendio de bebidas embriagantes a menores de edad; el exceso de alcohol es perjudicial para la salud. <a href="{CANVA_CARTA}" target="_blank" rel="noopener">Ver la carta original</a>.</p>
    </section>
  </main>''' + CONTACT_BAND + FOOTER


def page_conoce():
    return head('Conoce Azul · Aromas, clandestinos y la barra · Azul Restaurante, Cali',
                'Azul es un restaurante del barrio San Antonio, Cali, con aromas del Mediterráneo, la India y el norte de África. Conoce los clandestinos, la opción vegana, la barra de cócteles y vinos y los cuencos de mediodía.',
                'og.jpg', 'page-conoce', preload=hero_preload('tabla', 'tabla-m')) + HEADER + f'''
  <main>
    <section class="hero hero--short">
      <div class="hero__media">
        {picture('tabla', 'Entradas para compartir servidas en cuencos de cobre', 'tabla-m', extra='fetchpriority="high" decoding="async"')}
      </div>
      <p class="label hero__label reveal">Conoce Azul <span class="sub">San Antonio · Cali</span></p>
      <h1 class="hero__title reveal reveal-d1">Así es Azul</h1>
      <div class="hero__foot reveal reveal-d2">
        <div>
          <p class="lede">Una casa en San Antonio donde se cruzan el Mediterráneo, la India y el norte de África.</p>
          <div class="hero__actions">
            <a class="arrow-link on-dark" href="{WA_RESERVA}" target="_blank" rel="noopener">Reservar mesa {ARROW}</a>
          </div>
        </div>
      </div>
    </section>

    <section class="feature on-cream">
      <div class="grid">
        <div class="feature__media reveal">
          {picture('lomo', 'Lomo con romero y salsa de champiñones', extra='loading="lazy" decoding="async"')}
        </div>
        <div class="feature__body">
          <p class="label reveal">Los aromas</p>
          <h2 class="reveal reveal-d1">Mediterráneo, India y norte de África</h2>
          <p class="lede reveal reveal-d2">La carta se mueve entre tres cocinas: berenjena ahumada, hummus, aceitunas kalamata y queso feta del Mediterráneo; masala, leche de coco y samosas de la India; cuscús, limones en salmuera y especias de Marruecos del norte de África.</p>
          <ul class="feature__list reveal reveal-d2">
            <li>Entradas para compartir: tabla mediterránea, Azul baba ganoush y plato marroquí</li>
            <li>Cordero en cuscús y musaka, lomo, arroz meloso de conejo y caldoso de mar</li>
            <li>Pescado fresco, envuelto de pescado y camarón, mejillones con aromas del sur</li>
          </ul>
          <a class="btn-solid reveal reveal-d3" href="menu.html">Ver la carta</a>
        </div>
      </div>
    </section>

    <section class="feature feature--reverse on-stone">
      <div class="grid">
        <div class="feature__media reveal">
          {picture('rollo', 'Rollo de frutos secos con yogur aromatizado', extra='loading="lazy" decoding="async"')}
        </div>
        <div class="feature__body">
          <p class="label reveal">Un plato único</p>
          <h2 class="reveal reveal-d1">Los clandestinos</h2>
          <p class="lede reveal reveal-d2">Un clandestino es un plato único preparado e inspirado en ti. Si Martha se encuentra, pregunta por los clandestinos.</p>
          <ul class="feature__list reveal reveal-d2">
            <li>Pregunta por ellos al reservar o en la mesa</li>
            <li>Cuéntanos qué te gusta y qué no: el plato se inspira en ti</li>
            <li>Sujeto a que Martha esté en la cocina ese día</li>
          </ul>
          <a class="btn-solid reveal reveal-d3" href="{WA_CLANDESTINO}" target="_blank" rel="noopener">Reservar y preguntar</a>
        </div>
      </div>
    </section>

    <section class="feature on-cream">
      <div class="grid">
        <div class="feature__media reveal">
          {picture('barra', 'La barra de Azul con botellas y flores secas', extra='loading="lazy" decoding="async"')}
        </div>
        <div class="feature__body">
          <p class="label reveal">La barra</p>
          <h2 class="reveal reveal-d1">Cócteles, vinos y sangría</h2>
          <p class="lede reveal reveal-d2">Clásicos como el negroni, el dry martini o el old fashioned a mi modo; sangría y vino de verano por copa o jarra, y vinos blancos, tintos, rosados y cava.</p>
          <ul class="feature__list reveal reveal-d2">
            <li>Cócteles desde $42.000 y mojito virgen sin licor</li>
            <li>Sangría de vino tinto o blanco: copa $45.000, jarra $155.000</li>
            <li>Vinos de Argentina, Chile, España, Italia y Francia</li>
          </ul>
          <a class="btn-solid reveal reveal-d3" href="menu.html#cocteles">Ver tragos y bebidas</a>
        </div>
      </div>
    </section>

    <section class="feature feature--reverse on-stone">
      <div class="grid">
        <div class="feature__media reveal">
          {picture('sangria', 'Copa de sangría de vino blanco con frutas', extra='loading="lazy" decoding="async"')}
        </div>
        <div class="feature__body">
          <p class="label reveal">Para todos</p>
          <h2 class="reveal reveal-d1">Vegano, niños y celebraciones</h2>
          <p class="lede reveal reveal-d2">En los platos marcados con la hoja se puede excluir cualquier producto de origen animal, hay pasta napolitana para los niños y, para fechas especiales, preparamos menús de celebración.</p>
          <ul class="feature__list reveal reveal-d2">
            <li>Opción vegana en entradas, ensaladas, sopas y pastas</li>
            <li>Avísanos si eres intolerante o alérgico: las recetas contienen frutos secos, harinas, lácteos, mariscos y picante</li>
            <li>Cuencos de mediodía: la propuesta de almuerzo, publicada en el menú del día</li>
          </ul>
          <a class="btn-solid reveal reveal-d3" href="{WA_EVENTO}" target="_blank" rel="noopener">Reservar por WhatsApp</a>
        </div>
      </div>
    </section>
  </main>''' + CONTACT_BAND + FOOTER


def page_contacto():
    return head('Contacto y reservas · Azul Restaurante, San Antonio, Cali',
                f'Reserva por WhatsApp al {WA_TEL} o visítanos en la Carrera 5 #2-130, barrio San Antonio, Cali. Lunes a sábado, almuerzo y cena.',
                'og.jpg', 'page-contacto', preload=[
                    '<link rel="preload" as="image" href="img/fachada-m.webp" type="image/webp" media="(max-width: 767px)">',
                    '<link rel="preload" as="image" href="img/barra-wide.webp" type="image/webp" media="(min-width: 768px)">']) + HEADER + f'''
  <main>
    <section class="hero hero--short">
      <div class="hero__media">
        {picture('barra-wide', 'Fachada y barra de Azul en San Antonio', 'fachada-m', extra='fetchpriority="high" decoding="async"')}
      </div>
      <p class="label hero__label reveal">Azul Restaurante <span class="sub">Contacto</span></p>
      <h1 class="hero__title reveal reveal-d1">Hablemos</h1>
      <div class="hero__foot reveal reveal-d2">
        <div>
          <p class="lede">Reservas, celebraciones o cualquier pregunta: por WhatsApp respondemos más rápido. Las sugerencias también llegan por correo.</p>
          <div class="hero__actions">
            <a class="arrow-link on-dark" href="{WA_RESERVA}" target="_blank" rel="noopener">Reservar por WhatsApp {ARROW}</a>
          </div>
        </div>
      </div>
    </section>

    <section class="contact on-cream">
      <div class="grid">
        <div class="contact__aside">
          <p class="label reveal">Contacto</p>
          <h2 class="reveal reveal-d1">Estamos en San Antonio</h2>
          <p class="lede reveal reveal-d2">Una casa en la Carrera 5 #2-130, en el barrio San Antonio de Cali.</p>
          <dl class="reveal reveal-d2">
            <div><dt>Dirección</dt><dd><a href="{MAPS}" target="_blank" rel="noopener">{ADDRESS}<br>{CITY}</a></dd></div>
            <div><dt>WhatsApp</dt><dd><a href="{WA_RESERVA}" target="_blank" rel="noopener">{WA_TEL}</a></dd></div>
            <div><dt>Correo</dt><dd><a href="mailto:{MAIL}">{MAIL}</a></dd></div>
            <div><dt>Horario</dt><dd>{'<br>'.join(f'{html.escape(d)}: {html.escape(h)}' for d, h in HOURS)}</dd></div>
            <div><dt>Redes</dt><dd><a href="{IG}" target="_blank" rel="noopener">Instagram @azulrestaurantecali</a><br><a href="{FB}" target="_blank" rel="noopener">Facebook AZUL Restaurante</a></dd></div>
          </dl>
        </div>
        <form class="contact__form reveal reveal-d1" id="contact-form">
          <div class="form-row">
            <div class="field"><label for="f-nombre">Nombre</label><input id="f-nombre" name="nombre" type="text" autocomplete="name" required></div>
            <div class="field"><label for="f-tel">Teléfono</label><input id="f-tel" name="telefono" type="tel" autocomplete="tel" inputmode="tel" required></div>
          </div>
          <div class="field">
            <label for="f-motivo">Motivo</label>
            <select id="f-motivo" name="motivo">
              <option>Reserva de mesa</option>
              <option>Celebración o evento</option>
              <option>Cuencos de mediodía</option>
              <option>Sugerencia</option>
              <option>Otro</option>
            </select>
          </div>
          <div class="field"><label for="f-msg">Mensaje</label><textarea id="f-msg" name="mensaje" required placeholder="Cuéntanos qué necesitas: fecha, hora, número de personas…"></textarea></div>
          <button class="btn-solid btn-solid--azul" type="submit">Enviar por WhatsApp</button>
          <p class="form-hint">Al enviar se abre WhatsApp con tu mensaje listo para que lo envíes desde tu número.</p>
        </form>
      </div>
      <div class="map reveal"><iframe src="{MAPS_EMBED}" title="Mapa: Azul Restaurante, Carrera 5 #2-130, San Antonio, Cali" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe></div>
    </section>
  </main>''' + CONTACT_BAND + FOOTER


PAGES = {
    'index.html': page_index,
    'menu.html': page_menu,
    'conoce-azul.html': page_conoce,
    'contacto.html': page_contacto,
}

if __name__ == '__main__':
    for name, fn in PAGES.items():
        path = os.path.join(OUT, name)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(fn())
        print('escrito', os.path.relpath(path, OUT))
