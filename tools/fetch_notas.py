"""Descarga las notas del sitio actual a data/notas/<id>.js para que nota.html las muestre.

Uso (desde la raíz del proyecto):
    python tools/fetch_notas.py            # todas las notas enlazadas en el mockup
    python tools/fetch_notas.py 470434     # solo ids concretos

Busca en los HTML y en data/secciones.js todas las rutas con la forma /seccion/slug/id,
descarga cada nota (páginas públicas, con pausa entre peticiones) y guarda su contenido
ya limpio: solo se conservan párrafos, subtítulos, listas, citas, enlaces, imágenes y
videos de YouTube. Es solo para el draft: en producción las notas vienen del CMS.
"""
import html
import json
import re
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from html.parser import HTMLParser
from pathlib import Path

BASE = "https://diariopresente.mx"
UA = "Mozilla/5.0 (compatible; rediseno-draft/1.0)"
RAIZ = Path(__file__).resolve().parent.parent
SALIDA = RAIZ / "data" / "notas"
SECCIONES_NOTA = {"tabasco", "villahermosa", "sucesos", "mexico", "politica", "mundo", "deportes", "espectaculos", "actualidad", "cultura", "sociales"}


def get(url):
    for intento in range(3):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.read().decode("utf-8", "replace")
        except Exception:  # noqa: BLE001
            time.sleep(1.5 * (intento + 1))
    raise RuntimeError("no se pudo descargar " + url)


def rutas_en_el_mockup():
    rutas = {}
    patron = re.compile(r"""["'](/([a-z0-9-]+)/[^"'/\s]+/(\d{4,}))["']""")
    archivos = list(RAIZ.glob("*.html")) + [RAIZ / "data" / "secciones.js"]
    for f in archivos:
        for m in patron.finditer(f.read_text(encoding="utf-8")):
            if m.group(2) in SECCIONES_NOTA:
                rutas[m.group(3)] = m.group(1)
    return rutas


def txt(s):
    s = re.sub(r"<[^>]+>", " ", s)
    return re.sub(r"\s+", " ", html.unescape(s)).strip()


class Limpia(HTMLParser):
    """Deja solo etiquetas seguras. Las imágenes y videos salen como bloques propios."""

    PERMITIDAS = {"p", "h2", "h3", "h4", "strong", "b", "em", "i", "br", "ul", "ol", "li", "blockquote", "a"}
    SALTAR = {"script", "style", "noscript", "form", "button", "svg", "template"}
    RENOMBRAR = {"h1": "h2", "h5": "h4", "h6": "h4"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out = []
        self.salto = 0
        self.p_abierto = False
        self.imagenes = []
        self.video = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if self.salto:
            if tag in self.SALTAR:
                self.salto += 1
            return
        if tag in self.SALTAR:
            self.salto = 1
            return
        if tag == "img":
            src = a.get("src") or a.get("data-original") or ""
            if src.startswith("https://"):
                self._cerrar_p()
                alt = html.escape(a.get("alt") or "", quote=True)
                self.out.append(f'<figure class="inline-figure"><div class="media ph"><img src="{html.escape(src, quote=True)}" alt="{alt}" loading="lazy" onerror="this.remove()"></div></figure>')
                self.imagenes.append(src)
            return
        if tag == "iframe":
            src = a.get("src") or ""
            m = re.match(r"^(?:https?:)?//(?:www\.)?(?:youtube\.com|youtube-nocookie\.com)/embed/([\w-]+)", src)
            if m:
                self._cerrar_p()
                self.out.append(f'<div class="embed"><iframe src="https://www.youtube-nocookie.com/embed/{m.group(1)}" title="Video" loading="lazy" allowfullscreen></iframe></div>')
                self.video = True
            return
        tag = self.RENOMBRAR.get(tag, tag)
        if tag not in self.PERMITIDAS:
            return
        if tag == "a":
            href = a.get("href") or ""
            if href.startswith(("http://", "https://", "/")):
                self.out.append(f'<a href="{html.escape(href, quote=True)}">')
            else:
                self.out.append("<a>")
            return
        if tag == "br":
            self.out.append("<br>")
            return
        if tag == "p":
            self._cerrar_p()
            self.p_abierto = True
        self.out.append(f"<{tag}>")

    def handle_endtag(self, tag):
        if self.salto:
            if tag in self.SALTAR:
                self.salto -= 1
            return
        tag = self.RENOMBRAR.get(tag, tag)
        if tag not in self.PERMITIDAS or tag == "br":
            return
        if tag == "p":
            self.p_abierto = False
        self.out.append(f"</{tag}>")

    def handle_data(self, data):
        if self.salto:
            return
        self.out.append(html.escape(data))

    def _cerrar_p(self):
        if self.p_abierto:
            self.out.append("</p>")
            self.p_abierto = False

    def resultado(self):
        s = "".join(self.out)
        s = re.sub(r"<p>(?:\s|&nbsp;|\xa0|<br>)*</p>", "", s)
        s = re.sub(r"<(strong|b|em|i)>(?:\s|&nbsp;|\xa0)*</\1>", "", s)
        s = re.sub(r"<(h2|h3|h4|li|blockquote)>(?:\s|&nbsp;|\xa0)*</\1>", "", s)
        # correos ofuscados por Cloudflare: no se publican en el draft
        s = re.sub(r'<a href="/cdn-cgi/l/email-protection[^"]*">.*?</a>', "(correo protegido en el sitio original)", s, flags=re.S)
        s = re.sub(r"\s{2,}", " ", s)
        return s.strip()


def parsear(id_, ruta, page):
    m = re.search(r"<article[^>]*>(.*?)</article>", page, re.S)
    if not m:
        return None
    a = m.group(1)

    def uno(pat, grupo=1, flags=re.S):
        r = re.search(pat, a, flags)
        return txt(r.group(grupo)) if r else ""

    titulo = uno(r"<h1[^>]*>(.*?)</h1>")
    if not titulo:
        # formato antiguo (galerías): el título va en un bloque "caption" antes de los botones de compartir
        titulo = uno(r'<div class="caption"[^>]*>(.*?)<div class="sharepost">')
    if not titulo:
        return None
    img = re.search(r'<div class="category-image"><img[^>]*(?:data-original|src)="([^"]+)"', a)
    if not img:
        # sin foto principal: la primera imagen fechada del artículo
        img = re.search(r'<img[^>]*(?:data-original|src)="(https://[^"]*blob[^"]*/images/20\d\d/[^"]+)"', a)
    spans = [txt(x) for x in re.findall(r'<span class="date">(.*?)</span>', a, re.S)]
    fecha = next((s for s in spans if re.fullmatch(r"\d\d/\d\d/\d{4}", s)), "")
    hora = next((s for s in spans if re.fullmatch(r"\d\d:\d\d [ap]\.m\.", s)), "")
    autor = next((s.split(":", 1)[1].strip() for s in spans if s.lower().startswith("autor")), "")
    fuente = next((s.split(":", 1)[1].strip() for s in spans if s.lower().startswith("fuente")), "")
    bajada = uno(r'<div style="color: #aaaaaa[^"]*">(.*?)</div>')
    # cuerpo: desde el contenedor de la nota hasta la primera línea horizontal (antes de las etiquetas)
    i = a.find("notacuerpocontenido")
    if i < 0:
        i = a.find('<div class="description"')  # formato antiguo
    if i < 0:
        return None
    i = a.index(">", i) + 1
    j = a.find("<hr", i)
    cuerpo_html = a[i:j if j > 0 else len(a)]
    p = Limpia()
    p.feed(cuerpo_html)
    cuerpo = p.resultado()
    tags = []
    for href, t in re.findall(r'<li><a href="(/tags/[^"]+)"[^>]*>(.*?)</a></li>', a, re.S):
        tags.append({"t": txt(t), "h": href})
    return {
        "id": id_,
        "ruta": ruta,
        "seccion": uno(r'<span class="overlay-category">(.*?)</span>') or uno(r'<h2 class="pull-left sub-cat"[^>]*>(.*?)</h2>'),
        "subcat": uno(r'<h2 class="pull-left sub-cat">(.*?)</h2>'),
        "titulo": titulo,
        "bajada": bajada,
        "fecha": fecha,
        "hora": hora,
        "autor": autor,
        "fuente": fuente,
        "imagen": img.group(1) if img else "",
        "cuerpo": cuerpo,
        "tags": tags,
        "video": p.video,
    }


def descargar(par):
    id_, ruta = par
    try:
        nota = parsear(id_, ruta, get(BASE + ruta))
    except Exception as e:  # noqa: BLE001
        return id_, None, str(e)
    time.sleep(0.25)
    return id_, nota, ""


def completar_imagenes():
    """Las notas de galería no traen foto principal: se toma la que usa el bloque Multimedia del home."""
    h = (RAIZ / "index.html").read_text(encoding="utf-8")
    base = re.search(r"const B1='([^']+)'", h)
    a = h.find("multimedia:[")
    if not base or a < 0:
        return
    bloque = h[a : h.index("ranking:[", a)]
    for id_, ruta in re.findall(r"\['[^']*','[^']*/(\d{4,8})',B1\+'([^']+)'\]", bloque):
        f = SALIDA / f"{id_}.js"
        if not f.exists():
            continue
        t = f.read_text(encoding="utf-8")
        d = json.loads(t[t.index("(") + 1 : t.rindex(")")])
        if not d["imagen"]:
            d["imagen"] = base.group(1) + ruta
            cuerpo = json.dumps(d, ensure_ascii=False, separators=(",", ":"))
            f.write_text(f"window.NOTA_CB&&NOTA_CB({cuerpo});\n", encoding="utf-8")


def main():
    rutas = rutas_en_el_mockup()
    if len(sys.argv) > 1:
        rutas = {i: r for i, r in rutas.items() if i in sys.argv[1:]}
    SALIDA.mkdir(parents=True, exist_ok=True)
    print(f"{len(rutas)} notas por descargar")
    ok, fallos, sin_cuerpo, videos, sin_imagen = 0, [], [], [], []
    with ThreadPoolExecutor(max_workers=4) as ex:
        for k, (id_, nota, err) in enumerate(ex.map(descargar, rutas.items()), 1):
            if not nota:
                fallos.append((id_, err))
                continue
            if len(re.sub(r"<[^>]+>", "", nota["cuerpo"]).strip()) < 40:
                sin_cuerpo.append(id_)
            if nota["video"]:
                videos.append(id_)
            if not nota["imagen"]:
                sin_imagen.append(id_)
            cuerpo = json.dumps(nota, ensure_ascii=False, separators=(",", ":"))
            (SALIDA / f"{id_}.js").write_text(f"window.NOTA_CB&&NOTA_CB({cuerpo});\n", encoding="utf-8")
            ok += 1
            if k % 50 == 0:
                print(f"  {k}/{len(rutas)}")
    completar_imagenes()
    print(f"guardadas: {ok}; fallos: {len(fallos)}; sin cuerpo: {len(sin_cuerpo)}; con video: {len(videos)}; sin imagen: {len(sin_imagen)}")
    if fallos:
        print("fallos:", fallos[:10])
    if sin_cuerpo:
        print("sin cuerpo:", sin_cuerpo[:20])


if __name__ == "__main__":
    main()
