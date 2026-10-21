"""Descarga las columnas de opinión del sitio actual a data/columnas/<id>.js para que columna.html las muestre.

Uso (desde la raíz del proyecto):
    python tools/fetch_columnas.py

Parte de las columnas enlazadas en el mockup (opinion.html y columna.html), descarga cada una y también
las que cada página lista como "Más contenido del autor" (un nivel). Los correos de los autores NO se
guardan: el sitio actual los ofusca y el draft no debe publicarlos. Es solo para el draft.
"""
import json
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from fetch_notas import BASE, Limpia, get, txt  # noqa: E402

RAIZ = Path(__file__).resolve().parent.parent
SALIDA = RAIZ / "data" / "columnas"
AUTOR_POR_DEFECTO = "Redacción"
BLOQUE = re.compile(r"(<p>.*?</p>|<h[234]>.*?</h[234]>|<ul>.*?</ul>|<ol>.*?</ol>|<blockquote>.*?</blockquote>|<figure.*?</figure>|<div class=\"embed\">.*?</div>)", re.S)


def rutas_y_autores():
    """ids -> (ruta, autor) leídos de los arreglos de opinion.html y de los enlaces de los HTML."""
    rutas, autores = {}, {}
    for f in RAIZ.glob("*.html"):
        t = f.read_text(encoding="utf-8")
        for m in re.finditer(r"""["'](/opinion/[^"'\s]+/(\d{4,8}))["']""", t):
            rutas[m.group(2)] = m.group(1)
        if f.name == "opinion.html":
            for m in re.finditer(r"\['([^'/]+/(\d{4,8}))','([^']*)','([^']*)','([^']*)','(\d\d/\d\d/\d{4})'\]", t):
                rutas[m.group(2)] = "/opinion/" + m.group(1)
                autores[m.group(2)] = m.group(5)
    # las columnas de "Escala Crítica" listadas en columna.html son del mismo autor
    t = (RAIZ / "columna.html").read_text(encoding="utf-8")
    for m in re.finditer(r"'(/opinion/escala-critica/(\d{4,8}))'", t):
        rutas[m.group(2)] = m.group(1)
        autores.setdefault(m.group(2), "Víctor M. Sámano Labastida")
    return rutas, autores


def oracion(s):
    s = s.strip()
    return s[:1].upper() + s[1:].lower() if s else s


def procesar_cuerpo(crudo):
    p = Limpia()
    p.feed(crudo)
    limpio = p.resultado()
    puntos, partes = [], []
    for b in BLOQUE.findall(limpio):
        t = txt(b)
        if b.startswith("<p>"):
            if not t or "email" in t.lower() and "protected" in t.lower() or re.fullmatch(r"\(?\s*\[?.*@.*\]?\s*\)?", t) and len(t) < 60:
                continue  # correo del autor (ofuscado en el sitio) o párrafo vacío
            if t.startswith("Las opiniones aquí expresadas"):
                continue  # el descargo lo pone la plantilla
            if t.startswith("*"):
                puntos.append(t.lstrip("* ").strip())
                continue
            letras = re.sub(r"[^A-Za-zÁÉÍÓÚÜÑáéíóúüñ]", "", t)
            if letras and t == t.upper() and len(t) <= 90:
                partes.append(f"<h2>{oracion(t)}</h2>")
                continue
        partes.append(b)
    return puntos, "".join(partes)


def parsear(id_, ruta, autor, page):
    m = re.search(r"<article[^>]*>(.*?)</article>", page, re.S)
    if not m:
        return None
    a = m.group(1)
    titulo = re.search(r'<h2[^>]*class="lead[^"]*"[^>]*>(.*?)</h2>', a, re.S)
    if not titulo:
        return None
    columna = re.search(r'<div class="caption"[^>]*>(.*?)</div>', a, re.S)
    fecha = re.search(r"(\d\d/\d\d/\d{4})", a)
    i = a.find('<div class="description"')
    if i < 0:
        return None
    i = a.index(">", i) + 1
    j = a.find("<hr", i)
    puntos, cuerpo = procesar_cuerpo(a[i:j if j > 0 else len(a)])
    tags = [{"t": txt(t), "h": h} for h, t in re.findall(r'<li><a href="(/tags/[^"]+)"[^>]*>(.*?)</a></li>', a, re.S)]
    mas = []
    k = a.find("CONTENIDO DEL AUTOR")
    if k < 0:
        k = a.find("CONTENIDO DEL AUTOR".replace("Ó", "&Oacute;"))
    for blk in re.findall(r'<div class="detail">(.*?)</div></div></div>', a[k:] if k > 0 else "", re.S):
        h = re.findall(r'<a href="(/opinion/[^"]+/(\d{4,8}))"[^>]*>(.*?)</a>', blk, re.S)
        f = re.search(r"(\d\d/\d\d/\d{4})", blk)
        if len(h) >= 2 and f:
            mas.append({"h": h[1][0], "id": h[1][1], "t": txt(h[1][2]), "f": f.group(1)})
    nombre = txt(columna.group(1)) if columna else ""
    titular = txt(titulo.group(1))
    # En algunas columnas el sitio invierte los campos (nombre largo y "titular" corto): se intercambian
    if len(nombre) >= 25 and len(nombre) >= 2 * len(titular):
        nombre, titular = titular, nombre
    if titular == titular.upper() and re.search(r"[A-ZÁÉÍÓÚÑ]", titular):
        titular = re.sub(r"\((i{1,3}|iv|v|vi{1,3}|ix|x)\)", lambda m: m.group(0).upper(), oracion(titular))  # conserva números romanos
    return {
        "id": id_,
        "ruta": ruta,
        "columna": nombre,
        "titulo": titular,
        "autor": autor or AUTOR_POR_DEFECTO,
        "fecha": fecha.group(1) if fecha else "",
        "puntos": puntos,
        "cuerpo": cuerpo,
        "tags": tags,
        "mas": mas,
    }


def descargar(item):
    id_, (ruta, autor) = item
    try:
        col = parsear(id_, ruta, autor, get(BASE + ruta))
    except Exception as e:  # noqa: BLE001
        return id_, None, str(e)
    time.sleep(0.25)
    return id_, col, ""


def guardar(col):
    cuerpo = json.dumps(col, ensure_ascii=False, separators=(",", ":"))
    (SALIDA / f"{col['id']}.js").write_text(f"window.COLUMNA_CB&&COLUMNA_CB({cuerpo});\n", encoding="utf-8")


def main():
    rutas, autores = rutas_y_autores()
    pendientes = {i: (r, autores.get(i, "")) for i, r in rutas.items()}
    SALIDA.mkdir(parents=True, exist_ok=True)
    hechos, fallos, sin_cuerpo = {}, [], []
    for nivel in (0, 1):
        if not pendientes:
            break
        print(f"nivel {nivel}: {len(pendientes)} columnas")
        nuevos = {}
        with ThreadPoolExecutor(max_workers=4) as ex:
            for id_, col, err in ex.map(descargar, pendientes.items()):
                if not col:
                    fallos.append((id_, err))
                    continue
                if len(txt(col["cuerpo"])) < 80:
                    sin_cuerpo.append(id_)
                hechos[id_] = col
                guardar(col)
                for x in col["mas"]:
                    if x["id"] not in hechos and x["id"] not in pendientes and x["id"] not in nuevos:
                        nuevos[x["id"]] = (x["h"], col["autor"])
        pendientes = nuevos if nivel == 0 else {}
    print(f"guardadas: {len(hechos)}; fallos: {len(fallos)}; sin cuerpo: {len(sin_cuerpo)}")
    if fallos:
        print("fallos:", fallos[:10])


if __name__ == "__main__":
    main()
