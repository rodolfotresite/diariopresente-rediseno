# Diario Presente — análisis del sitio actual y decisiones del rediseño

Fuente: diariopresente.mx, portada del 20-oct-2026. Mockup base: `gemini-code-1792532454205.html`.

## 1. Estructura actual de la portada (orden real)

| # | Bloque | Notas |
|---|---|---|
| 1 | Topline | Ubicación, enlace a Edición Impresa, 4 redes (FB, X, IG, YT) |
| 2 | Header | Logo (PNG), botón "Menú" en móvil |
| 3 | Menú | 14 entradas planas: Inicio, Sucesos, Villahermosa, Tabasco, México, Política, Mundo, Deportes (▸ Tabasco, Mundo), Espectáculos, Cultura, Sociales, Actualidad, Edición impresa, Contáctanos |
| 4 | Leaderboards | 3 slots GAM de 728×90 apilados: `top_large_leaderboard`, `top_leaderboard`, `bottom_leaderboard` |
| 5 | Destacadas | 1 nota grande + tarjetas con miniatura (hoy: Sheinbaum / La Pastora) |
| 6 | Bloques por categoría | Espectáculos, Villahermosa, Política, México, Mundo, Sucesos, Tabasco, Deportes, Actualidad — cada uno con etiqueta y lista de notas |
| 7 | Opinión | 5 columnistas con avatar genérico (`user-01.png`) + "Ver más columnas" |
| 8 | Multimedia | Galería de notas con ícono de galería |
| 9 | Portada del día | Miniatura de la edición impresa |
| 10 | Footer | Grupo Presente Multimedios, dirección, teléfono, redes, términos y aviso de privacidad |
| — | Plugin Facebook | Timeline de Grupo Presente Multimedios (iframe) |

Longitud: ~5,100 px en escritorio, una sola columna sin sidebar.

## 2. Stack observado (relevante para la migración)

- CMS propio (no WordPress). URLs `/{seccion}/{slug}/{id}`; el `id` numérico debe conservarse.
- Imágenes en Azure Blob (`blob.diariopresente.mx`, `diariopresenterm.blob.core.windows.net`), `.webp` con recorte en el nombre.
- Detrás de Cloudflare. Tipografía actual: Lato. Bootstrap 3 (clases `col-md-*`, `hidden-md`).
- Publicidad: Google Ad Manager (red 461505524), AdSense, Smart AdServer, Cxense, ID5.
- Analítica: GTM, GA4 + Universal Analytics, Hotjar, Scorecard Research.
- Consentimiento: Google Funding Choices. Newsletter: Mailchimp (us18) ya cargado.

## 3. Problemas detectados en el sitio actual

1. Menú de 14 enlaces sin jerarquía; "Edición impresa" y "Contáctanos" compiten con las secciones.
2. Portada muy larga y uniforme: nueve bloques de categoría con el mismo peso visual.
3. Sin sidebar ni módulos de retención (más leído, newsletter, redes).
4. Opinión con el mismo avatar genérico para los cinco columnistas (`user-01.png`).
5. Tres leaderboards 728×90 sin sitio para formatos de sidebar (300×250 / 300×600).
6. No encontré buscador, modo oscuro ni ajuste de tamaño de texto en la portada.
7. Marcas de tiempo en las listas, pero sin tiempo de lectura ni bajada en la nota principal.
8. Dependencia de scripts de terceros (≥10) en la carga inicial.

## 4. Qué se tomó del mockup y qué se cambió

**Identidad (ajuste posterior):** el mockup usaba navy + rojo, pero el sitio actual es solo azul, así que se adoptó su paleta: header `#156DAD`, barra de menú `#184F76`, etiquetas `#1B659A`, enlaces `#337AB7`, texto `#27242F`, fondo blanco. Derivados propios, que no existen en el sitio: `#0F3552` (ticker), `#1E5F90` (hover), y los tintes claros de fondo y línea. En modo oscuro las etiquetas pasan a `#7DBBEA` por contraste. El texto "DIARIO PRESENTE" del mockup se reemplazó por el logo oficial (`Logo_web_presente-01-1-n.svg`, guardado en `assets/`), incrustado como SVG en el HTML. El original es blanco; en el header se recolorea a `#156DAD` para el fondo blanco y en el footer y el modo oscuro se queda blanco.

**Se conserva del mockup:** tipografía Georgia para titulares, masthead centrado, nav sticky, ticker de última hora, hero 1.65fr/0.75fr, sidebar con más leído + newsletter, franja de multimedia, modo oscuro, tamaño de texto, buscador.

**Se ajusta para que coincida con el sitio real:**

- **Menú (decidido):** 14 entradas → 8 principales (Tabasco, Villahermosa, Sucesos, México, Política, Deportes ▾, Espectáculos, Opinión) + "Más ▾" (Mundo, Actualidad, Cultura, Sociales, Multimedia). "Edición impresa" pasa a botón destacado en el topline y "Contáctanos" al topline/footer. Opinión sube a la barra por ser el rasgo más distintivo de un diario regional; Mundo baja a "Más" para priorizar lo local; Sociales y Cultura quedan en "Más" sin bloque en portada. La barra cabe en una sola fila desde 920 px; por debajo de 900 px pasa a menú hamburguesa.
- **Bloques por categoría:** de 9 listas en una columna a una cuadrícula de 2 columnas con 1 nota principal + lista compacta por sección (Sucesos, Villahermosa, México, Política, Mundo, Deportes, Espectáculos, Actualidad; Tabasco queda cubierto por Destacadas y Lo más reciente).
- **Opinión:** el título de cada columna (Altar Mayor, Águila o Sol, etc.) pasa a ser el elemento principal de la tarjeta, con el autor debajo y las iniciales como avatar mientras no haya foto.
- **Móvil:** el mockup no cerraba el menú en pantallas chicas; se añadió menú hamburguesa con submenús desplegados.
- **Accesibilidad:** los submenús abren también con foco de teclado (`:focus-within`), no solo con hover. Contraste de texto secundario subido en ambos temas.
- **Footer:** se usan los datos reales (Av. Pagés Llergo 116, Nueva Villahermosa; tel. 993 312-17-55). Se eliminó "desde 1959" del mockup porque no pude verificarlo.
- **Eslogan:** se usa el del sitio, "Diario del Sureste de México".

## 5. Mapa de publicidad

| Mockup | Formato | Slot actual equivalente |
|---|---|---|
| Anuncio 1 | Leaderboard 970×90 sobre el hero | `top_large_leaderboard` |
| Anuncio 2 | In-feed bajo el hero | `top_leaderboard` |
| Anuncio 3 | In-feed al cierre de "Lo más reciente" | `bottom_leaderboard` |
| Anuncio 4 | Sidebar 300×250 | nuevo (AdSense / Smart AdServer) |
| Anuncio 5 | Sidebar 300×600 | nuevo |

Los slots 4 y 5 son nuevos: hay que crearlos en Ad Manager y confirmar con ventas si los 3 existentes se conservan.

## 6. Pendientes y preguntas abiertas

- **Más leído:** el sitio no lo publica; hoy son 5 notas de relleno. Necesita fuente (GA4 o el CMS).
- **Clima:** placeholder; falta elegir API.
- **Bajada del hero:** el CMS actual no parece tener resumen; se necesita ese campo.
- **Imágenes:** los 38 bloques de foto del home (hero, destacadas, Lo más reciente, 8 secciones, Multimedia) y la portada del día usan notas e imágenes reales del sitio del 20-oct-2026, enlazadas directo a su Azure Blob. Son solo para el draft; en producción cada nota trae su propio recorte del CMS.
- **Multimedia:** son las 4 galerías que hoy muestra el sitio. Sus fotos son de septiembre; el sitio no las ha renovado.
- **Opinión:** sin foto, porque el sitio actual usa el mismo avatar genérico para los cinco columnistas; el draft usa iniciales hasta tener fotos reales.
- **Notas repetidas:** el draft no repite ninguna nota entre bloques. El sitio actual sí lo hace (por ejemplo, las galerías de Multimedia también salen en sus secciones).
- **Cultura y Sociales:** están en el menú actual pero no en la portada; decidir si merecen bloque.
- **Redes:** los enlaces del topline son `#`; faltan las URLs oficiales (solo confirmé Facebook de Grupo Presente Multimedios).
- **Render:** el draft arma las listas con JavaScript desde un objeto de datos; en producción deben salir renderizadas desde el servidor por SEO.

## 7. Página de nota (`nota.html`)

Nota de ejemplo: "Gobierno del Pueblo de Tabasco cumple compromiso con la rehabilitación integral del Parque Museo La Venta" (id 470434), con su texto, fotos y etiquetas reales. Comparte con el home `assets/site.css` y `assets/site.js`.

**Estructura actual de una nota:** foto superior con etiqueta de sección → "NOTICIAS / TABASCO" → fecha, hora, autor y fuente → titular (29 px) → bajada en gris cursiva → anuncio 300×250 y botones AddThis → sumario en mayúsculas → cuerpo (20 px) con una foto intercalada → tags → comentarios de Facebook → anuncios y plugin de página de Facebook al final.

**Qué cambia en el rediseño:**

- **Cabecera de lectura:** sección, titular en Georgia, bajada, firma con avatar, fecha, hora y tiempo de lectura calculado. La foto va después de la firma y ocupa todo el ancho de la columna.
- **Sumario:** el texto en mayúsculas del sitio actual pasa a un recuadro con borde azul, en minúsculas.
- **Cuerpo:** 19 px (escala con el botón Aa), 68 caracteres por línea, interlineado 1.7 y capitular en el primer párrafo.
- **Tamaño del texto:** A− / A+ en la firma de la nota, con 5 niveles (88 %, 100 %, 113 %, 125 % y 150 %), indicador del nivel actual y un clic en el porcentaje para restablecer. El nivel se recuerda entre visitas y el botón Aa del encabezado usa los mismos niveles. En móvil, donde Aa está oculto, A− / A+ es el único control.
- **Compartir:** Facebook, X, WhatsApp y copiar enlace, como enlaces nativos. Se elimina la dependencia de AddThis.
- **Módulos nuevos:** "Lee también" dentro del texto, barra de progreso de lectura, cierre con boletín y "Más de Tabasco" con 3 notas.
- **Comentarios:** el plugin de Facebook se carga solo al pulsar el botón, para no cargar su SDK en cada lectura.
- **Publicidad:** se conservan los slots 1, 4 y 5 del home y se agrega el 6, un 300×250 dentro del texto después del sexto párrafo.
- **SEO:** `<link rel=canonical>`, Open Graph y JSON-LD `NewsArticle` con los datos de la nota.

**Pendientes de la nota:** pie y crédito de foto (el CMS no los expone), autor con nombre en vez de "Redacción", y tags con enlaces reales.

## 8. Página de sección (`seccion.html`, ejemplo: Tabasco)

Usa las notas reales de `diariopresente.mx/tabasco` del 20-oct-2026: 4 destacadas y 37 notas en el listado, todas con titular, resumen, hora y foto. Comparte `assets/site.css` y `assets/site.js`.

**Estructura actual:** título "TABASCO" → 4 destacadas con foto → listado de notas (foto, titular, resumen, hora y fecha) en 8 columnas, con barra lateral de 4 → botón "Más noticias". Mide ~11,500 px y carga unas 25 notas ocultas para ese botón.

**Qué cambia en el rediseño:**

- **Cabecera de sección:** título grande con filete azul, descripción corta, ruta de navegación y un espacio para subsecciones (hoy Tabasco no tiene; Deportes sí tiene Tabasco y Mundo).
- **Destacadas:** una principal grande con resumen y tres secundarias con miniatura, en lugar de 4 tarjetas iguales.
- **Listado cronológico:** separadores por día ("Lunes, 19 de octubre") para que se lea como un archivo. Cada nota lleva foto 3:2, titular, resumen de hasta 3 líneas y hora.
- **Más noticias:** carga de 12 en 12 con contador ("Mostrando 12 de 37 notas") y mensaje al final. Es un botón real, accesible, en lugar de la carga oculta de hoy.
- **Publicidad:** slots 1, 4 y 5 como en el resto del sitio, más dos in-feed dentro del listado (después de la 4.ª y la 10.ª nota).
- **Móvil:** miniaturas cuadradas de 104 px con titular y resumen de 2 líneas, para ver más notas por pantalla.
- **SEO:** `CollectionPage` y `BreadcrumbList` en JSON-LD, y enlace canónico.

**Enlaces:** el menú, el pie, las etiquetas "Tabasco" y los "Ver todas" del home y de la nota ahora apuntan a `seccion.html`.

**Pendientes de la sección:** paginación real con URL por página (hoy "Más noticias" no cambia la dirección y no es indexable), filtro por fecha o por municipio, y el resumen de las 3 destacadas secundarias, que el sitio actual no muestra.

## 9. Opinión (`opinion.html`) y página de columna (`columna.html`)

Datos reales de `diariopresente.mx/opinion` y de la columna "Escala Crítica" (id 470258) del 19-oct-2026, con su texto completo. Los estilos y scripts de lectura (tamaño de texto, compartir, tiempo de lectura, progreso) viven ahora en `assets/article.css` y `assets/article.js`, compartidos con la página de nota.

**Estructura actual del listado:** "COLUMNAS DE HOY" (6 columnas, con avatar genérico) → "COLUMNISTAS" (6 nombres) → "MÁS COLUMNAS" (lista con columna, fecha, titular y autor) → botón "Más contenidos". Mide ~10,600 px.

**Estructura actual de una columna:** nombre de la columna → fecha → titular → puntos clave → texto → correo del autor → descargo editorial → tag → "Más contenido del autor" (6) → comentarios de Facebook. No muestra el nombre del autor en la propia página, solo en el listado.

**Qué cambia en el rediseño (listado):**

- **Columnas de hoy:** la principal ocupa dos columnas y dos filas con el titular en grande; las otras cinco son tarjetas con columna, titular, autor y fecha. Toda la tarjeta es clicable.
- **Columnistas:** un acceso por autor con avatar de iniciales y el nombre de su columna.
- **Más columnas:** separadores por día, 8 por vez con contador, un anuncio in-feed y el descargo editorial al pie.
- **Avatares de iniciales:** el sitio usa el mismo avatar para todos; hasta tener fotos, las iniciales distinguen a cada autor.

**Qué cambia en el rediseño (columna):**

- **Autor al frente:** nombre de la columna como rótulo, titular, y firma con avatar, nombre y enlace "Ver todas sus columnas", que la página actual no tiene.
- **Puntos clave:** las tres viñetas pasan a un recuadro azul antes del texto.
- **Lectura:** mismo texto de 19 px con A− / A+, subtítulos, cita destacada para el párrafo constitucional y tiempo de lectura calculado (3 min).
- **Barra lateral:** ficha del autor, "Más contenido del autor" con fechas y publicidad. Al pie, "Más columnas de hoy".
- **SEO:** `OpinionNewsArticle` con autor y serie, y enlace canónico.

**Pendientes y decisiones:**

- **Datos invertidos en el CMS:** en varias columnas el título y el nombre de la columna vienen intercambiados (por ejemplo, "Dependencia crítica del gas natural estadounidense (II)" / "Estados Unidos y México"). El draft las normaliza; conviene corregirlo en el CMS.
- **Autor sin ficha:** no hay foto ni biografía en el sitio actual. La ficha lleva solo nombre y columna.
- **Correo del autor:** el texto original incluye `vmsamano@hotmail.com`. Se conservó como firma, pero conviene confirmar con el autor si desea que se publique.
- **Autor sin enlace único:** hoy no existe una página por autor; "Todas sus columnas" apunta al listado general.
- **Solo Escala Crítica** tiene página en este draft. Las demás columnas enlazan a su URL real.

## 10. Edición impresa (`edicion.html`)

Portadas y enlaces reales de `diariopresente.mx/edicionimpresa` del 20-oct-2026: la edición de hoy, 6 recientes, 3 de Ventana Sur y 2 suplementos.

**Estructura actual:** "EDICIÓN IMPRESA / MARTES 20 DE OCTUBRE DE 2026" → portada de hoy (380 px, enlaza al lector FlipHTML5) → botón "Calendario" que abre una ventana → "RECIENTES" (6 portadas) → "Ventana Sur" y "Suplementos", cada uno con selectores de año y trimestre. El selector de Ventana Sur dice "Enero-Marzo 2025" aunque muestra ediciones de octubre de 2026.

**Qué cambia en el rediseño:**

- **Edición de hoy como protagonista:** portada grande con sombra de papel, fecha en titular, botón "Leer edición completa" (abre el lector en pestaña nueva) y "Elegir otra fecha".
- **Calendario siempre visible:** junto a las recientes, en lugar de la ventana emergente. Es una tabla accesible, de lunes a domingo, con navegación por mes; solo los días con edición son enlaces, y el de hoy lleva contorno.
- **Recientes:** 6 portadas con día de la semana y fecha. La del 18 de octubre no existe en el sitio (domingo), y el calendario lo refleja.
- **Ventana Sur y Suplementos:** estantes de portadas con su fecha, sin los selectores de año y trimestre que hoy muestran etiquetas incorrectas.
- **SEO:** `PublicationIssue` de la edición del día, además de la colección.
- **Enlaces:** el botón "Edición impresa" del topline, el home y el resto de páginas apuntan a `edicion.html`.

**Pendientes y decisiones:**

- **Archivo histórico:** el sitio permite navegar suplementos desde 2013. El calendario solo tiene datos de octubre de 2026 en este draft; falta conectarlo al archivo del CMS (días con edición, meses y años anteriores).
- **Páginas por fecha:** cada edición del sitio actual tiene una URL propia (`/edicionimpresa/10-19-2026`) que no se rediseñó aquí.
- **Lector externo:** la lectura sigue en FlipHTML5, un servicio de terceros. Si se quiere un lector propio o descarga en PDF, hay que definirlo; hoy el sitio no ofrece descarga.
- **Títulos de suplementos:** el sitio no los muestra (solo la portada y la fecha); el draft los etiqueta "Suplemento".
- **Portadas de Ventana Sur:** el sitio solo ofrece la miniatura de 140 × 176 px, así que se ven algo suaves al ampliarse.

## 11. Revisión general del draft (20-oct-2026)

Se auditaron las 6 páginas (home, nota, sección, opinión, columna, edición impresa) en escritorio (1280 px) y móvil (375 px), con el DOM ya renderizado: estructura, enlaces, imágenes, accesibilidad, contraste en claro y oscuro, objetivos táctiles y consistencia entre páginas.

### Corregido en esta revisión

| Área | Problema | Corrección |
|---|---|---|
| Accesibilidad | 49 enlaces de imagen sin nombre (la foto y el titular enlazaban al mismo destino) en home, sección y nota | El enlace de la foto se oculta a lectores de pantalla y al teclado; el titular sigue enlazando |
| Accesibilidad | Salto de encabezado h1 → h3 en el home | Encabezado h2 oculto "Más destacadas" antes de las notas laterales |
| Accesibilidad | Contraste del texto legal del pie: 3.39:1 | Color aclarado; el resto de textos medidos (≈ 1,000 en 6 páginas, claro y oscuro) cumple 4.5:1 / 3:1 |
| Accesibilidad | Ticker de última hora: dos copias leídas y enfocables, pausa solo con ratón | La copia duplicada se oculta y se quita del orden de tabulación; pausa también con foco de teclado; región etiquetada "Última hora" |
| Accesibilidad | Objetivos táctiles pequeños en móvil: botón Edición impresa (23 px), logo (21 px), enlaces del ticker (25 px) | Ahora 31 px, 60 px y 47 px |
| Accesibilidad | Etiqueta del buscador reutilizaba la clase del enlace "saltar al contenido" | Clase propia `sr-only` |
| Enlaces | "Multimedia" del menú (`#multimedia`) apuntaba a un ancla inexistente en 5 de las 6 páginas | Ahora `index.html#multimedia` |
| Enlaces | Los `href="#"` provisionales saltaban al inicio de la página | Se bloquea ese salto hasta que tengan destino |
| Consistencia | Logo e "Inicio" del home usaban `/`; el resto, `index.html` | Unificado a `index.html` |
| Consistencia | Migas de pan definidas 5 veces (cuatro archivos y `article.css`) | Una sola definición en `site.css` |
| SEO | Home sin `canonical` ni Open Graph | Agregados |

### Resultado de la verificación (después de corregir)

- **Imágenes:** 69 URLs remotas distintas, las 69 cargan.
- **Enlaces locales entre las 6 páginas:** ninguno roto; anclas internas válidas.
- **Estructura:** un `h1` por página, sin saltos de encabezado, un `main` por página, `lang="es-MX"`, `title` y `meta description` en todas, `canonical` en todas, sin ids duplicados, sin referencias ARIA rotas, sin botones ni campos sin nombre.
- **Consistencia:** encabezado y pie idénticos en las 6 páginas salvo el estado activo del menú; mismo logo, paleta, controles de tema y tamaño de texto.
- **Responsivo:** sin desbordes horizontales en ninguna página en 1280 y 375 px, ni con el texto al 150 %.
- **Consola:** sin errores.

### Pendientes (no se pueden resolver en el draft)

**Enlaces a páginas aún no construidas (89 rutas distintas con formato `/ruta`):**
- 12 páginas de sección: Villahermosa, Sucesos, México, Política, Deportes (y sus subsecciones Tabasco y Mundo), Espectáculos, Mundo, Actualidad, Cultura y Sociales; además de Contacto.
- 6 páginas de edición por fecha (`/edicionimpresa/10-19-2026`…).
- ~70 notas y columnas que enlazan a su URL real. En producción funcionan; abiertas desde esta carpeta no abren nada. Las secciones pendientes salen de la misma plantilla de `seccion.html`.

**Enlaces provisionales (`href="#"`):**
- 4 redes sociales del topline (Facebook, X, Instagram, YouTube): faltan las URLs oficiales, solo hay una confirmada (Facebook de Grupo Presente Multimedios).
- "Acerca de Grupo Presente Multimedios" y "Términos legales y aviso de privacidad" (pie), que no tienen página.
- Los 5 tags de la nota, "Explorar →" de Multimedia y los "Ver todas / Ver todos" de Ventana Sur y Suplementos.
- El menú "Más ▾" es un enlace `#` que abre un desplegable: conviene un `<button>` con `aria-expanded` al construir el sitio real.

**Datos y contenido:**
- "Más leído": 5 notas de relleno; falta la fuente (GA4 o el CMS).
- Clima: texto provisional; falta elegir API.
- Multimedia: solo hay 4 galerías, con fotos de septiembre, y ningún video.
- Bajada de la nota principal del home, pie y crédito de foto, nombre del autor en notas y foto de columnistas: el CMS no los expone.
- Archivo histórico de la edición impresa: el calendario solo tiene datos de octubre de 2026.
- Datos del CMS con título y columna invertidos en algunas columnas de opinión.

**Dependencias de producción:**
- Las fotos se enlazan directo desde el servidor del sitio actual (69 imágenes): si allá las mueven o borran, el draft se queda sin ellas.
- El encabezado y el pie se repiten en cada HTML; en producción deben ser componentes del CMS.
- Las listas se arman con JavaScript desde datos en la página; para SEO deben salir ya renderizadas desde el servidor.
- Sección: "Más noticias" no cambia la URL; falta paginación con URL propia (`?pagina=2`).
- Facebook (comentarios y plugin de página), publicidad (Google Ad Manager y AdSense), Mailchimp, analítica y Hotjar están como marcadores, sin integrarse.

**Decisiones pendientes de negocio o editorial:**
- Mundo en "Más" (no en la barra principal) y Opinión en la barra principal (ya acordado).
- Publicar o no el correo del autor en las columnas.
- Modo oscuro: hoy es manual. Se puede respetar la preferencia del sistema; no se cambió por ser una decisión de diseño.
- Cuántos slots de publicidad conservar de los 3 actuales (los 2 de sidebar son nuevos).

### No verificado

- Enlaces externos a FlipHTML5 y Facebook, y la carga real de anuncios, comentarios y newsletter.
- Lectores de pantalla reales (NVDA, VoiceOver): la revisión fue automática sobre el DOM, no con tecnología asistiva.
- Contraste de textos sobre degradados e imágenes (tarjeta del boletín, anuncios, títulos sobre fotos), que el cálculo automático omite.
- Navegadores distintos a Chromium y dispositivos físicos.

## 12. Secciones completas y publicación de la vista previa

### Secciones (`seccion.html?s=…`)

`seccion.html` ahora es una sola plantilla que sirve **13 secciones** con notas reales (453 notas con foto, hora, fecha, resumen y enlace), leídas de `data/secciones.js`. Ese archivo lo genera `tools/fetch_secciones.py` descargando las portadas públicas del sitio actual.

| Sección | Destacadas | Notas en listado |
|---|---|---|
| Tabasco | 4 | 40 |
| Villahermosa | 4 | 19 |
| Sucesos | 4 | 39 |
| México | 4 | 40 |
| Política | 4 | 40 |
| Mundo | 4 | 40 |
| Deportes | 4 | 40 |
| Deportes · Tabasco | 4 (completadas con las más recientes) | 22 |
| Deportes · Mundo | 4 (completadas) | 36 |
| Espectáculos | 4 | 40 |
| Actualidad | 4 | 34 |
| Cultura | 4 | 12 |
| Sociales | 3 (completadas) | 0 (la sección solo tiene 3 notas) |

- **Comportamiento:** accesos rápidos a secciones relacionadas, miga de pan con la sección padre en las subsecciones de Deportes, menú con la sección activa y mensaje cuando no hay más notas. Si el parámetro `s` no existe, muestra Tabasco.
- **Menú y pie** de las 6 páginas enlazan a cada sección. Los 416 enlaces de imagen se verificaron: todos cargan.
- **Subsecciones de Deportes:** el sitio actual no trae destacadas en `/deportes/tabasco/` ni `/deportes/mundo/`; el draft toma las 4 más recientes.
- **Sociales** tiene 3 notas y la más reciente es de septiembre; Cultura, 16. Conviene preguntar al cliente si siguen activas.

### Vista previa en GitHub Pages

- **Enlaces a páginas no rediseñadas** (notas, columnas, ediciones por fecha, Contacto: unas 90 rutas distintas): `site.js` los reescribe a `https://diariopresente.mx/…` y los abre en una pestaña nueva, para que no den 404 en Pages.
- **Distintivo** "Borrador de rediseño · contenido de ejemplo" en todas las páginas.
- **No indexar:** `<meta name="robots" content="noindex, nofollow">` en todas las páginas y `robots.txt` con `Disallow: /`.
- **Notas de ejemplo:** el panel "Más leído" indica que son datos de ejemplo. En secciones se llena con las notas más recientes.
- **Archivos de Pages:** `.nojekyll` y `404.html`.
- **Repositorio público** en la cuenta personal, por elección del usuario. Contiene contenido y fotos de diariopresente.mx y el correo de un columnista, usados como ejemplo.
