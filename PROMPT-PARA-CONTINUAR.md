# Prompt para continuar con otro modelo

Copia y pega esto tal cual (ajusta la parte de "Lo que necesito ahora"):

---

Voy a continuar un proyecto web que ya está avanzado. Antes de hacer nada, lee estos dos archivos y confirma que entendiste el estado:

- `/Volumes/Tw3/Proyecto Claude/azul/CONTEXTO.md` (resumen del proyecto, decisiones tomadas y pendientes)
- `/Volumes/Tw3/Proyecto Claude/azul/README.md` (dónde se edita cada cosa)

Contexto rápido: es el sitio de Azul Restaurante (aromas mediterráneos, India y norte de África; Carrera 5 #2-130, barrio San Antonio, Cali, Colombia; Instagram @azulrestaurantecali). Está hecho con el mismo estilo de los sitios de Koi Sushi y Perú Peñón. Son cuatro páginas estáticas en HTML/CSS/JS (`index.html`, `menu.html`, `conoce-azul.html`, `contacto.html`), sin framework, en `/Volumes/Tw3/Proyecto Claude/azul/`. Las páginas se generan con `_fuentes/build.py` (ahí están la carta, los horarios y los textos).

Reglas para trabajar:

1. Respeta el sistema de diseño: colores y tipografía están como variables al inicio de `css/style.css` (crema #F0EBE2, casi negro #121A1A, azul #4B7A80, verde #3E7065, terracota #D9773C; Archivo ancha para títulos, DM Sans para texto). No introduzcas otros colores ni fuentes.
2. Para cambiar textos, carta, precios u horarios edita `_fuentes/build.py` y ejecuta `python3 build.py` desde `_fuentes/`. No edites los `.html` a mano si vas a volver a usar el generador. Las fotos se generan con `_fuentes/imagenes.py` y el logo con `_fuentes/logo.py`.
3. No inventes datos del negocio. Verificados: WhatsApp +57 323 510 5573, Carrera 5 #2-130 barrio San Antonio (Cali), correo azul.azulrestaurante@gmail.com, Instagram @azulrestaurantecali, Facebook facebook.com/azulclandestino. Los horarios del sitio salen de Google Maps y NO están confirmados por el cliente. Los precios son los de la carta en Canva.
4. Escríbeme en español de Colombia, sin voseo.
5. Después de cada cambio, abre el sitio en local (`python3 -m http.server 8080` dentro de la carpeta) y revisa en móvil (375 px) y escritorio antes de darlo por terminado. La carta (`menu.html`) es lo más importante en celular.
6. La carpeta `_fuentes/originales/` es material de trabajo; no la incluyas al publicar.

Lo que necesito ahora:

[describe aquí el cambio: por ejemplo "confirmaron los horarios: martes a sábado X–Y", "agregar la sección de cuencos de mediodía con estos platos y precios", "reemplazar el logo por el archivo SVG que me mandaron", "publicar en GitHub Pages como koisushi", etc.]

---
