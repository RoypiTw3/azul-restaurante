# Contexto del proyecto — Azul Restaurante

Resumen para continuar el trabajo con otra persona u otro modelo. Fecha: 21 de septiembre de 2026.

## Objetivo

El restaurante **Azul · Cocina con aromas** (barrio San Antonio, Cali) no tenía página web: solo un Linktree (https://linktr.ee/Azulrestaurantecali) con la carta en Canva, un enlace de WhatsApp para reservar, el mapa y un formulario de sugerencias. Se construyó un sitio con la misma estructura del de Koi Sushi (`/Volumes/Tw3/Proyecto Claude/koi`, publicado en https://roypitw3.github.io/koisushi/), adaptado a la identidad y a la información real de Azul. Prioridad: que se vea bien en celular, con la carta en una página aparte y pocos destacados en el inicio.

## Estado actual

Sitio estático (HTML/CSS/JS, sin framework ni build), verificado en 375 px (móvil) y 1440 px sin errores de consola. Falta publicarlo.

```
azul/
├── index.html            Inicio: hero, bloque "La barra", foto completa, intro, 5 platos destacados, 3 bloques de texto (clandestinos, vegano, cuencos), bloque "Una casa en San Antonio" con horarios
├── menu.html             Carta completa (16 categorías) con barra de categorías fija y resaltado automático; íconos de opción vegana y picante
├── conoce-azul.html      Los aromas · Los clandestinos · La barra · Vegano, niños y celebraciones
├── contacto.html         Datos, horarios, formulario (WhatsApp; las sugerencias van por correo) y mapa de Google embebido
├── css/style.css         Tokens y estilos
├── js/main.js            Interacción
├── img/                  Fotos, logos, favicon, og.jpg
└── _fuentes/
    ├── build.py          Generador. Datos de la carta (MENU), horarios (HOURS) y textos. `python3 build.py` desde _fuentes/
    ├── imagenes.py       Recortes y optimización de fotos (JPG + WebP) desde originales/
    ├── logo.py           Recrea el logo "azul" en alta resolución con Arial Black
    └── originales/       Fotos y logo originales sin optimizar (no se suben al hosting; está en .gitignore)
```

## Sistema de diseño

- Misma base que Koi y Perú Peñón (a su vez de ballenacabo.com): header flotante centrado (botón "Reservar mesa" izquierda, logo centro, hamburguesa derecha), menú que cae desde la barra, preloader oscuro con frase (solo la primera vez por sesión), hero a sangre, bloque partido foto + panel de color, imagen completa, intro, tarjetas con carrusel, banda de contacto, footer con el logo grande.
- Paleta (medida del logo y del tema del Linktree): crema `#F0EBE2`, casi negro `#121A1A`, azul petróleo `#4B7A80` (acento principal: panel del bloque partido, enlaces activos, títulos de subcategorías), azul marino `#374A5B`, verde `#3E7065` (banda de contacto, ícono vegano), terracota `#D9773C` (ícono picante, tomado del color de los nombres de plato en la carta), arena `#C6BDAB`, niebla `#C9CFC8`, piedra `#DDD7CA`.
- Tipografía: Archivo ancha (`wdth 125`) para títulos, DM Sans para texto, Bodoni Moda para los títulos de los tres bloques de texto del inicio.
- Logo: el único disponible era la foto de perfil del Linktree (276 px, wordmark "azul" en Arial Black con la "z" azul superpuesta y los cruces en azul marino). `_fuentes/logo.py` lo recrea en alta resolución (`logo-color.png`, `logo-blanco.png`, `logo-negro.png`, `favicon.png`, `og.jpg`). Es una recreación fiel pero no el archivo original: **pedir al cliente el logo vectorial**.
- Fotos: seis salen de la carta en Canva (son fotos propias del restaurante subidas al diseño): tabla de entradas con cuencos de cobre, barra con botellas y flores secas, pasta con camarón, sangría, lomo con romero y rollo de frutos secos con yogur. La fachada es la foto que el propio restaurante subió a Google Maps (dic. 2021). Todas son verticales; los recortes horizontales para escritorio están definidos en `imagenes.py`. Las fotos de stock de Canva (atardecer, trigo, camino) no se usaron.

## Datos del negocio (verificados)

- Nombre: Azul Restaurante. Lema en la carta: "Cocina con aromas". Descripción en Linktree/Instagram/Facebook: "Aromas mediterráneos, India y norte de África".
- WhatsApp reservas: **+57 323 510 5573** (`573235105573`). El Linktree usa wa.link/4pmnfn con el texto "Quiero reservar 💙"; Google Maps enlaza wa.me/message/ECIC2BIUNNNQH1.
- Dirección: **Carrera 5 #2-130, barrio San Antonio, Cali** (Google Maps: https://maps.app.goo.gl/DkUhVbc9DqKPwAG36, plus code CFX6+69).
- Correo: azul.azulrestaurante@gmail.com (Linktree y Facebook).
- Redes: Instagram @azulrestaurantecali · Facebook facebook.com/azulclandestino ("AZUL Restaurante").
- Horarios (ficha de Google Maps, no confirmados por el cliente): lunes a jueves 12:00–2:30 p. m. y 7:00–9:00 p. m.; viernes y sábado 12:00–3:00 p. m. y 7:00–10:00 p. m.; domingo cerrado.
- Carta: Canva "CARTA AZUL 3" (6 páginas), enlazada desde el Linktree. Precios en COP tal cual. Íconos de la carta: hoja = "Vegano: opción de excluir cualquier producto de origen animal"; ají = picante; triángulo = "Si eres intolerante o alérgico, infórmanos".
- Clandestinos (texto de la carta): "Un clandestino es un plato único preparado e inspirado en ti. Si Martha se encuentra, pregunta por los clandestinos." Martha es la cocinera (Facebook etiqueta a Martha C. Izquierdo Perez).
- "Cuencos de mediodía": enlace del Linktree a un Canva llamado "Menú QR" que cambia; el 21 de septiembre mostraba el menú de Amor y Amistad del 19 de septiembre (cóctel de bienvenida, trío a bocados, paella de pastoreo o de mar, torta de quesos y manzanas). Por eso el sitio lo enlaza como "menú del día" sin transcribirlo.
- Celebraciones: Facebook publicó un menú especial de Amor y Amistad (10 sep 2026) y la bio de Instagram anuncia "Cenas de Navidad" con otro número (322 544 6498). El sitio dice que hay menús de celebración para fechas especiales, sin más detalle.
- Google Maps: 4,6 ★ (257 reseñas), categoría "Restaurante mediterráneo". Facebook: 100 % recomendado (26 opiniones), rango de precios $$$. No se pusieron en el sitio porque cambian.
- El tour 360 que aparece en Google Maps (360.mittos.co/azulcali) ya no existe (404).

## Decisiones tomadas

1. Cuarta página: "Conoce Azul" (el Linktree tuvo un enlace con ese nombre) en lugar de "Experiencias". No se inventó historia del restaurante ni testimonios; los textos salen de la carta, el Linktree, Instagram, Facebook y Google Maps.
2. Los tres bloques de "Lo que hace a Azul" en el inicio van sin foto (variante `.exp-item--text`) porque solo hay siete fotos verificadas.
3. Las 20 secciones de la carta se agruparon en 16 categorías para que la barra fija sea manejable: "Cócteles y aperitivos" (cócteles, sin licor, aperitivos, digestivos), "Sangría y vinos" (refrescantes, blancos, cava, rosados, tintos), "Licores", "Bebidas y cervezas".
4. Se corrigieron erratas de la carta ("Chardoney", "Rose", "mozarella", "San Peregrino", "expendió", "leche de coco" con mayúscula) y se normalizaron los nombres a mayúscula inicial.
5. Las fotos de las tarjetas se emparejaron con platos por parecido con la carta (el rollo de frutos secos aparece junto a "Postres" en el Canva; el lomo con romero, junto a "Carnes rojas"). Confirmar con el cliente.
6. El formulario de contacto abre WhatsApp, salvo cuando el motivo es "Sugerencia": entonces abre el correo, como el formulario del Linktree. No hay backend.
7. "Reservar" abre WhatsApp con un mensaje listo; el botón flotante de WhatsApp está en todas las páginas.
8. La página de la carta no usa el efecto `reveal` en los platos para que al saltar a una categoría el contenido esté visible de inmediato.

## Pendientes / preguntas para el cliente

- Confirmar horarios (los del sitio vienen de Google Maps).
- Logo vectorial original y fotos propias del local, del equipo (Martha) y de más platos; con ellas se pueden poner fotos en los tres bloques de texto del inicio y cambiar el hero.
- Confirmar qué son los "cuencos de mediodía" (¿almuerzo de lunes a viernes?, ¿precio?) para hacerles una sección propia.
- Confirmar que las fotos de las tarjetas corresponden a los platos indicados (rollo de frutos secos, lomo con aromas al bosque, pasta al limón y camarón).
- ¿Precios vigentes? La carta de Canva no tiene fecha.
- ¿Cenas de Navidad 2026? Si aplica, agregar con su número (322 544 6498).
- Publicación: crear repositorio en GitHub (RoypiTw3) y activar GitHub Pages, como https://roypitw3.github.io/koisushi/.

## Cómo ver en local

```bash
cd "/Volumes/Tw3/Proyecto Claude/azul" && python3 -m http.server 8080
```

y abrir http://localhost:8080. Desde el navegador integrado de Claude el servidor no puede leer el volumen Tw3: hay que copiar la carpeta al scratchpad (`sync.sh`) y servir esa copia (`serve.py`, configuración "azul" en `dancali/.claude/launch.json`).
