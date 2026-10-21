# Rediseño de Diario Presente (draft)

Primer borrador del rediseño de <https://diariopresente.mx/>, construido a partir de un mockup en HTML y del análisis de la estructura del sitio actual. Es un sitio estático (HTML, CSS y JavaScript, sin dependencias) con contenido real de la portada del 20 de octubre de 2026.

> **Repositorio privado.** Incluye notas, titulares y fotos de Diario Presente, su logo oficial y el correo de un columnista. Es material de un tercero: no lo hagas público sin limpiarlo.

## Cómo verlo

Desde esta carpeta:

```bash
python -m http.server 8000
```

y abre <http://localhost:8000/index.html>. También funciona abriendo `index.html` directamente en el navegador.

## Páginas

| Archivo | Qué es |
|---|---|
| `index.html` | Portada |
| `nota.html` | Página de una nota (ejemplo: Parque Museo La Venta) |
| `seccion.html` | Página de sección (ejemplo: Tabasco) |
| `opinion.html` | Listado de columnas de opinión |
| `columna.html` | Página de una columna (ejemplo: Escala Crítica) |
| `edicion.html` | Edición impresa: portada del día, calendario y suplementos |

## Estructura

```
assets/
  site.css       Estilos comunes a todas las páginas (paleta, encabezado, pie, anuncios)
  site.js        Tema claro/oscuro, tamaño de texto, buscador, menú, ticker
  article.css    Estilos de lectura (nota y columna)
  article.js     Compartir, tiempo de lectura, progreso, comentarios
  logo-diariopresente-blanco.svg   Logo oficial (el HTML lo incrusta como SVG)
analisis-sitio-actual.md   Análisis del sitio actual, decisiones y pendientes
```

## Decisiones de diseño

- **Paleta:** la del sitio actual: `#156DAD` (marca), `#184F76` (menú y pie), `#1B659A` (etiquetas), blanco. Sin rojo.
- **Logo:** el SVG oficial, recoloreado a azul sobre fondo blanco y en blanco en pie y modo oscuro.
- **Menú:** 8 secciones principales y "Más ▾" (Mundo, Actualidad, Cultura, Sociales, Multimedia).
- **Texto:** 5 niveles (88 %–150 %) que se recuerdan entre visitas; el control A− / A+ está en la nota y la columna.

El detalle de cada página, la revisión de accesibilidad y la lista completa de pendientes están en [`analisis-sitio-actual.md`](analisis-sitio-actual.md) (secciones 7 a 11).

## Pendientes principales

- Páginas de sección que faltan (Villahermosa, Sucesos, México, Política, Deportes, Espectáculos, Mundo, Actualidad, Cultura, Sociales) y Contacto, con la plantilla de `seccion.html`.
- Paginación con URL propia en secciones.
- Convertir encabezado y pie en componentes (hoy se repiten en cada HTML) y generar las listas desde el servidor en lugar de JavaScript.
- Datos sin fuente: "Más leído", clima, videos, créditos de foto, autores, archivo de ediciones.
- URLs de redes sociales y páginas legales; integración de publicidad, comentarios, boletín y analítica.
- Las fotos se cargan directo del servidor actual: en producción deben salir del CMS.
