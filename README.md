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
| `nota.html` | Página de una nota (ejemplo: Parque Museo La Venta) |
| `seccion.html` | Plantilla de sección para **13 secciones** con notas reales: `?s=tabasco` (por defecto), `villahermosa`, `sucesos`, `mexico`, `politica`, `mundo`, `deportes`, `deportes-tabasco`, `deportes-mundo`, `espectaculos`, `actualidad`, `cultura`, `sociales` |
| `opinion.html` | Listado de columnas de opinión |
| `columna.html` | Página de una columna (ejemplo: Escala Crítica) |
| `edicion.html` | Edición impresa: portada del día, calendario y suplementos |
| `404.html` | Página de error de GitHub Pages |

## Estructura

```
assets/
  site.css       Estilos comunes (paleta, encabezado, pie, anuncios, distintivo de borrador)
  site.js        Tema claro/oscuro, tamaño de texto, buscador, menú, ticker y la vista previa
  article.css    Estilos de lectura (nota y columna)
  article.js     Compartir, tiempo de lectura, progreso, comentarios
  logo-diariopresente-blanco.svg   Logo oficial (el HTML lo incrusta como SVG)
data/
  secciones.js   Notas reales de las secciones (generado, no editar a mano)
tools/
  fetch_secciones.py   Regenera data/secciones.js desde diariopresente.mx
analisis-sitio-actual.md   Análisis del sitio actual, decisiones, revisión y pendientes
```

### Actualizar los datos de las secciones

```bash
python tools/fetch_secciones.py
```

Descarga las portadas públicas de cada sección (con una pausa entre peticiones) y reescribe `data/secciones.js`.

### Vista previa: enlaces a páginas no rediseñadas

Las notas, columnas, ediciones por fecha y Contacto usan rutas del sitio actual (`/seccion/slug/id`). En el borrador, `assets/site.js` las convierte en enlaces a `https://diariopresente.mx/...` que abren en una pestaña nueva. Ese bloque (al final de `site.js`) debe eliminarse cuando las páginas salgan del CMS.

## Decisiones de diseño

- **Paleta:** la del sitio actual: `#156DAD` (marca), `#184F76` (menú y pie), `#1B659A` (etiquetas), blanco. Sin rojo.
- **Logo:** el SVG oficial, recoloreado a azul sobre fondo blanco y en blanco en pie y modo oscuro.
- **Menú:** 8 secciones principales y "Más ▾" (Mundo, Actualidad, Cultura, Sociales, Multimedia).
- **Texto:** 5 niveles (88 %–150 %) que se recuerdan entre visitas; el control A− / A+ está en la nota y la columna.

El detalle de cada página, la revisión de accesibilidad y la lista completa de pendientes están en [`analisis-sitio-actual.md`](analisis-sitio-actual.md) (secciones 7 a 12).

## Pendientes principales

- Páginas de nota individuales por sección (hoy solo hay una de ejemplo) y páginas por fecha de la edición impresa.
- Paginación con URL propia en secciones.
- Convertir encabezado y pie en componentes (hoy se repiten en cada HTML) y generar las listas desde el servidor en lugar de JavaScript.
- Datos sin fuente: "Más leído", clima, videos, créditos de foto, autores, archivo de ediciones.
- URLs de redes sociales y páginas legales; integración de publicidad, comentarios, boletín y analítica.
- Las fotos se cargan directo del servidor actual: en producción deben salir del CMS.
- Subsecciones: Sociales tiene solo 3 notas en el sitio actual y Cultura 16.

## Aviso

El repositorio es público y contiene notas, titulares y fotos de diariopresente.mx, su logo oficial y el correo de un columnista, usados como contenido de ejemplo para la revisión del rediseño.
