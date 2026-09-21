#!/usr/bin/env python3
"""Genera las fotos optimizadas de ../img a partir de originales/.

Ejecutar desde esta carpeta:  python3 imagenes.py
Cada salida se define con (original, nombre, proporción ancho/alto, anclaje vertical 0-1, ancho máximo).
Se escribe .jpg y .webp. El logo se genera aparte con logo.py.
"""
import os
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'originales')
OUT = os.path.join(HERE, '..', 'img')

# (archivo original, nombre de salida, proporción w/h (None = sin recorte), anclaje vertical, ancho máximo)
JOBS = [
    # Tabla de entradas (manos y cuencos): hero de inicio y de "Conoce Azul", tarjeta
    ('tabla-entradas.jpg', 'tabla',        1.6,  0.55, 1600),
    ('tabla-entradas.jpg', 'tabla-m',      2/3,  0.5,  900),
    ('tabla-entradas.jpg', 'card-tabla',   0.8,  0.62, 1000),
    # Barra (botellas y flores secas): bloque partido, hero de contacto escritorio, imagen del menú desplegable
    ('barra.jpg',          'barra',        None, 0.5,  1200),
    ('barra.jpg',          'barra-m',      4/3,  0.45, 900),
    ('barra.jpg',          'barra-wide',   1.6,  0.45, 1200),
    ('barra.jpg',          'barra-nav',    16/9, 0.42, 1200),
    # Pasta con camarón: imagen completa e hero del menú
    ('pasta-camaron.jpg',  'pasta',        1.6,  0.62, 1320),
    ('pasta-camaron.jpg',  'pasta-m',      None, 0.5,  900),
    ('pasta-camaron.jpg',  'card-pasta',   0.8,  0.62, 1000),
    # Tarjetas y bloques de "Conoce Azul"
    ('sangria.jpg',        'card-sangria', 0.8,  0.45, 800),
    ('lomo.jpg',           'card-lomo',    0.8,  0.45, 800),
    ('rollo-frutos-secos.jpg', 'card-rollo', 0.8, 0.5, 800),
    ('sangria.jpg',        'sangria',      None, 0.5,  800),
    ('lomo.jpg',           'lomo',         None, 0.5,  800),
    ('rollo-frutos-secos.jpg', 'rollo',    None, 0.5,  800),
    # Fachada (Google Maps, subida por el restaurante): bloque "Ven a San Antonio", hero móvil de contacto, pie
    ('fachada.jpg',        'fachada',      0.8,  0.42, 800),
    ('fachada.jpg',        'fachada-m',    2/3,  0.45, 900),
    ('fachada.jpg',        'fachada-thumb', 0.75, 0.42, 300),
]


def crop_aspect(im, aspect, anchor):
    w, h = im.size
    if aspect is None:
        return im
    if w / h > aspect:            # sobra ancho: recortar a los lados (centrado)
        nw = int(h * aspect)
        x = (w - nw) // 2
        return im.crop((x, 0, x + nw, h))
    nh = int(w / aspect)          # sobra alto: recortar arriba/abajo según anclaje
    y = int((h - nh) * anchor)
    return im.crop((0, y, w, y + nh))


def main():
    os.makedirs(OUT, exist_ok=True)
    for src, name, aspect, anchor, maxw in JOBS:
        im = Image.open(os.path.join(SRC, src)).convert('RGB')
        im = crop_aspect(im, aspect, anchor)
        if im.width > maxw:
            im = im.resize((maxw, int(im.height * maxw / im.width)), Image.LANCZOS)
        im.save(os.path.join(OUT, name + '.jpg'), quality=82, optimize=True, progressive=True)
        im.save(os.path.join(OUT, name + '.webp'), quality=80, method=6)
        print(f'{name:14s} {im.width}x{im.height}')


if __name__ == '__main__':
    main()
