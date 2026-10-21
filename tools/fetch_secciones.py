"""Genera data/secciones.js con las notas reales de cada sección de diariopresente.mx.

Uso (desde la raíz del proyecto):
    python tools/fetch_secciones.py

Descarga las portadas de sección (páginas públicas), extrae destacadas y listado
(titular, resumen, hora, fecha, foto, enlace) y escribe un archivo JS que
seccion.html carga como datos. Es solo para el draft: en producción las notas
vienen del CMS.
"""
import html
import json
import re
import sys
import time
import urllib.request
from pathlib import Path

BASE = "https://diariopresente.mx"
UA = "Mozilla/5.0 (compatible; rediseno-draft/1.0)"

# slug del draft -> (ruta en el sitio actual, nombre, descripción)
SECCIONES = {
    "tabasco": ("/tabasco", "Tabasco", "Gobierno, municipios, seguridad, salud, educación y cultura: las noticias del estado, de la más reciente a la más antigua."),
    "villahermosa": ("/villahermosa", "Villahermosa", "Lo que pasa en la capital tabasqueña: obras, servicios, vida comunitaria y cultura local."),
    "sucesos": ("/sucesos", "Sucesos", "Seguridad, justicia, accidentes y emergencias en Tabasco y el país."),
    "mexico": ("/mexico", "México", "Las noticias nacionales: gobierno federal, economía, salud y sociedad."),
    "politica": ("/politica", "Política", "Poderes, partidos, elecciones y decisiones públicas, a nivel local y nacional."),
    "mundo": ("/mundo", "Mundo", "Lo más importante del acontecer internacional."),
    "deportes": ("/deportes", "Deportes", "Fútbol, beisbol y deporte nacional e internacional, con la mirada puesta en Tabasco."),
    "deportes-tabasco": ("/deportes/tabasco/", "Deportes · Tabasco", "El deporte tabasqueño: equipos, atletas y competencias locales."),
    "deportes-mundo": ("/deportes/mundo/", "Deportes · Mundo", "El deporte internacional: ligas, torneos y figuras."),
    "espectaculos": ("/espectaculos", "Espectáculos", "Música, cine, televisión y farándula."),
    "actualidad": ("/actualidad", "Actualidad", "Ciencia, salud, tecnología y temas que están en la conversación."),
    "cultura": ("/cultura", "Cultura", "Arte, letras, tradiciones y agenda cultural de Tabasco."),
    "sociales": ("/sociales", "Sociales", "Eventos, celebraciones y vida social."),
}

DATE_RE = re.compile(r'<span class="date">\s*([^<|]*?)\s*\|\s*<i[^>]*></i>(?:&nbsp;|\s)*([\d/]{10})\s*</span>')


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "replace")


def txt(s):
    s = re.sub(r"<[^>]+>", " ", s)
    return re.sub(r"\s+", " ", html.unescape(s)).strip()


def nota(href, titulo, resumen, fecha, img):
    return {"h": href, "t": titulo, "s": resumen, "f": fecha, "i": img}


def parse(page):
    # Destacadas: bloques con overlay (título en h2, foto 570x356)
    dest = []
    for m in re.finditer(r'<div class="pic-with-overlay-2">(.*?)<span class="date">(.*?)</span>', page, re.S):
        blk, dt = m.group(1), m.group(2)
        a = re.search(r'<h2[^>]*>\s*<a[^>]*href="([^"]+)"[^>]*>(.*?)</a>', blk, re.S)
        im = re.search(r'<img[^>]*src="([^"]+)"', blk)
        d = DATE_RE.search('<span class="date">' + dt + "</span>")
        if a and im and d:
            dest.append(nota(a.group(1), txt(a.group(2)), "", f"{d.group(1)} {d.group(2)}", im.group(1)))
    # Listado: <li class="noline"> (las comillas de los atributos varían entre simples y dobles)
    notas = []
    for li in re.findall(r'<li class="noline">(.*?)</li>', page, re.S):
        href = re.search(r'<a[^>]*href=[\x22\x27]([^\x22\x27]+)[\x22\x27]', li)
        im = re.search(r'data-original=[\x22\x27]([^\x22\x27]+)[\x22\x27]', li) or re.search(r'<img[^>]*src=[\x22\x27]([^\x22\x27]+)[\x22\x27]', li)
        hora = re.search(r'(\d\d:\d\d [ap]\.m\.)', li)
        dia = re.search(r'(\d\d/\d\d/\d{4})', li)
        anchors = [txt(x) for x in re.findall(r'<a[^>]*href=[\x22\x27][^\x22\x27]+[\x22\x27][^>]*>(.*?)</a>', li, re.S)]
        anchors = [a for a in anchors if a]
        if not (href and im and hora and dia and anchors):
            continue
        titulo = anchors[0]
        resumen = anchors[1] if len(anchors) > 1 and anchors[1] != titulo else ""
        notas.append(nota(href.group(1), titulo, resumen, f"{hora.group(1)} {dia.group(1)}", im.group(1)))
    # sin duplicados, manteniendo el orden
    visto, out = set(), []
    for n in notas:
        if n["h"] not in visto:
            visto.add(n["h"])
            out.append(n)
    dest_ids = {n["h"] for n in dest}
    out = [n for n in out if n["h"] not in dest_ids]
    seen, d2 = set(), []
    for n in dest:
        if n["h"] not in seen:
            seen.add(n["h"])
            d2.append(n)
    return d2, out


def main():
    destino = Path(__file__).resolve().parent.parent / "data" / "secciones.js"
    datos = {}
    for slug, (ruta, nombre, desc) in SECCIONES.items():
        try:
            page = get(BASE + ruta)
        except Exception as e:  # noqa: BLE001
            print(f"  ! {slug}: {e}", file=sys.stderr)
            continue
        dest, notas = parse(page)
        datos[slug] = {"nombre": nombre, "ruta": ruta, "descripcion": desc, "destacadas": dest, "notas": notas}
        print(f"{slug:18} destacadas={len(dest):2} notas={len(notas):2}")
        time.sleep(0.8)  # trato amable con el servidor
    destino.parent.mkdir(exist_ok=True)
    cuerpo = json.dumps(datos, ensure_ascii=False, indent=1)
    destino.write_text(
        "/* Generado por tools/fetch_secciones.py (notas reales de diariopresente.mx). No editar a mano. */\n"
        "window.SECCIONES = " + cuerpo + ";\n",
        encoding="utf-8",
    )
    print("Escrito", destino)


if __name__ == "__main__":
    main()
