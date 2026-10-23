# Rediseño de Diario Presente (borrador)

Primer borrador del rediseño de <https://diariopresente.mx/>, construido a partir de un mockup en HTML y del análisis de la estructura del sitio actual. Es un sitio estático (HTML, CSS y JavaScript, sin dependencias) con contenido real de la portada del 20 de octubre de 2026.

**Vista previa para revisión:** <https://rodolfotresite.github.io/diariopresente-rediseno/>

> El sitio muestra un distintivo "Borrador de rediseño · contenido de ejemplo", pide a los buscadores que no lo indexen (`noindex` y `robots.txt`) y abre en el sitio actual las notas y páginas que todavía no se rediseñaron.

## Cómo verlo en local

Desde esta carpeta:

```bash
python -m http.server 8000
```

y abre <http://localhost:8000/index.html>. Las páginas de sección cargan datos con `<script>`, así que también funcionan abriendo `index.html` directamente, pero se recomienda el servidor.

## Páginas

| Archivo | Qué es |
|---|---|
| `index.html` | Portada |
| `nota.html` | Plantilla de nota: `?id=470434` muestra cualquiera de las ~400 notas enlazadas en el borrador, con su texto real (sin `?id=` muestra la nota de ejemplo, Parque Museo La Venta) |
| `seccion.html` | Plantilla de sección para **13 secciones** con notas reales: `?s=tabasco` (por defecto), `villahermosa`, `sucesos`, `mexico`, `politica`, `mundo`, `deportes`, `deportes-tabasco`, `deportes-mundo`, `espectaculos`, `actualidad`, `cultura`, `sociales` |
| `opinion.html` | Listado de columnas de opinión |
| `columna.html` | Plantilla de columna de opinión: `?id=470258` (sin `?id=` muestra Escala Crítica) |
| `edicion.html` | Edición impresa: portada del día, calendario y suplementos |
| `404.html` | Página de error de GitHub Pages |

### Espacios publicitarios

Los 11 espacios del *Media Kit 2026* del Grupo SIT (página "Espacios web") están en `assets/ads.js`; cada página los declara con `<div class="adslot" data-kit="N"></div>`. El botón "Espacios publicitarios" (abajo a la izquierda) abre la guía, resalta cada espacio en la página y muestra el Layer y el Intersticial móvil. Detalle y dudas para el área comercial: `analisis-sitio-actual.md`, sección 14.

## Estructura

```
assets/
  site.css       Estilos comunes (paleta, encabezado, pie, anuncios, distintivo de borrador)
  site.js        Tema claro/oscuro, tamaño de texto, buscador, menú, ticker y la vista previa
  ads.js         Catálogo de espacios publicitarios del media kit, guía y demostraciones
  article.css    Estilos de lectura (nota y columna)
  article.js     Compartir, tiempo de lectura, progreso, comentarios
  logo-diariopresente-blanco.svg   Logo oficial (el HTML lo incrusta como SVG)
data/
  secciones.js   Notas reales de las secciones (generado, no editar a mano)
  notas/<id>.js  Texto, foto, autor y etiquetas de cada nota (generado)
  columnas/<id>.js   Texto de cada columna de opinión (generado)
tools/
  fetch_secciones.py   Regenera data/secciones.js desde diariopresente.mx
  fetch_notas.py       Regenera data/notas/ (descarga y limpia cada nota enlazada)
  fetch_columnas.py    Regenera data/columnas/ (sin correos de los autores)
analisis-sitio-actual.md   Análisis del sitio actual, decisiones, revisión y pendientes
```

### Actualizar los datos

```bash
python tools/fetch_secciones.py   # portadas de sección
python tools/fetch_notas.py       # cada nota enlazada (usa data/secciones.js y los HTML)
python tools/fetch_columnas.py    # columnas de opinión
```

Descargan páginas públicas de diariopresente.mx con pausa entre peticiones. Ejecutar siempre en ese orden: las notas se buscan en lo que enlazan las secciones. Las notas se limpian con una lista blanca de etiquetas (párrafos, subtítulos, listas, citas, enlaces, imágenes y videos de YouTube).

### Enlaces entre páginas

Los datos traen rutas del sitio actual (`/seccion/slug/id`). Al final de `assets/site.js`, un bloque las reescribe en el navegador:

- `/seccion/slug/id` → `nota.html?id=id`
- `/opinion/slug/id` → `columna.html?id=id`
- cualquier otra ruta (Contacto, ediciones por fecha, etiquetas) → `https://diariopresente.mx/...`, en una pestaña nueva.

Si una nota o columna no está en `data/`, la plantilla muestra un aviso con enlace al sitio actual. Ese bloque debe eliminarse cuando las páginas salgan del CMS.

## Decisiones de diseño

- **Paleta:** la del sitio actual: `#156DAD` (marca), `#184F76` (menú y pie), `#1B659A` (etiquetas), blanco. Sin rojo.
- **Logo:** el SVG oficial, recoloreado a azul sobre fondo blanco y en blanco en pie y modo oscuro.
- **Menú:** 8 secciones principales y "Más ▾" (Mundo, Actualidad, Cultura, Sociales, Multimedia).
- **Texto:** 5 niveles (88 %–150 %) que se recuerdan entre visitas; el control A− / A+ está en la nota y la columna.

El detalle de cada página, la revisión de accesibilidad y la lista completa de pendientes están en [`analisis-sitio-actual.md`](analisis-sitio-actual.md) (secciones 7 a 12).

## Pendientes principales

- Páginas por fecha de la edición impresa y de etiquetas (`/tags/...`), que hoy abren el sitio actual.
- Paginación con URL propia en secciones.
- Convertir encabezado y pie en componentes (hoy se repiten en cada HTML) y generar las listas desde el servidor en lugar de JavaScript.
- Datos sin fuente: "Más leído", clima, videos, créditos de foto, autores, archivo de ediciones.
- URLs de redes sociales y páginas legales; integración de publicidad, comentarios, boletín y analítica.
- Las fotos se cargan directo del servidor actual: en producción deben salir del CMS.
- Subsecciones: Sociales tiene solo 3 notas en el sitio actual y Cultura 16.

## Aviso

El repositorio es público y contiene notas, titulares y fotos de diariopresente.mx, su logo oficial y el correo de un columnista, usados como contenido de ejemplo para la revisión del rediseño.
