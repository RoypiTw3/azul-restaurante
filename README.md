# Azul Restaurante — sitio web

Sitio del restaurante **Azul · Cocina con aromas** (Carrera 5 #2-130, barrio San Antonio, Cali). Aromas mediterráneos, India y norte de África. Usa la misma estructura y sistema visual de los sitios de Koi y Perú Peñón (header flotante, hero a sangre, bloques partidos, tipografía ancha en mayúsculas), con la paleta del logo de Azul: crema, verde y azul petróleo.

Sitio 100 % estático: no necesita instalación ni build. Se sube tal cual a cualquier hosting (GitHub Pages, Netlify, cPanel…).

## Estructura

```
index.html           Inicio
menu.html            Carta completa por categorías, con índice fijo para celular
conoce-azul.html     Los aromas, los clandestinos, la barra y la opción vegana
contacto.html        Datos, horarios, formulario (WhatsApp o correo) y mapa
css/style.css        Estilos y tokens de diseño (colores, tipografía)
js/main.js           Preloader, menú, revelado al hacer scroll, carrusel, índice de la carta, formulario
img/                 Fotos optimizadas (JPG + WebP), logo en varias versiones, favicon, imagen OG
_fuentes/build.py    Generador de las 4 páginas: aquí están los DATOS DE LA CARTA y los textos
_fuentes/imagenes.py Genera las fotos de img/ a partir de _fuentes/originales/
_fuentes/logo.py     Genera el logo (color, blanco, negro), favicon y og.jpg
```

## Cómo editar

- **Carta, precios y textos**: editar `_fuentes/build.py` (lista `MENU` y las funciones `page_*`) y luego ejecutar `python3 build.py` desde `_fuentes/`. Eso regenera los cuatro `.html`.
  También se pueden editar los `.html` directamente y olvidarse del generador (pero entonces no volver a ejecutarlo o se pierden los cambios).
- **Horarios**: lista `HOURS` al inicio de `_fuentes/build.py` (aparecen en el inicio, en contacto y en la banda de contacto).
- **WhatsApp**: `WA_NUM` en `_fuentes/build.py` y `WA` en `js/main.js` (hoy `573235105573`).
- **Dirección, correo, redes y enlaces de Canva**: variables `ADDRESS`, `MAIL`, `IG`, `FB`, `MAPS`, `CANVA_CARTA`, `CANVA_DIA` al inicio de `_fuentes/build.py`.
- **Fotos**: poner el original en `_fuentes/originales/`, agregar la línea correspondiente en `JOBS` de `_fuentes/imagenes.py` y ejecutar `python3 imagenes.py` desde `_fuentes/` (necesita Pillow).
- **Colores**: variables al inicio de `css/style.css` (`--cream`, `--ink`, `--azul`, `--verde`, `--terracota`, `--sand`, `--mist`, `--stone`).

## Ver en local

```bash
python3 -m http.server 8080
```

y abrir http://localhost:8080
