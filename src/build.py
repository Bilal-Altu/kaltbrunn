#!/usr/bin/env python3
"""Baut die Einzeldatei-Seite: Teile zusammenfügen, Assets als Data-URI einsetzen.

  python3 build.py ../index.html                  Grundfassung (Tiefschwarz)
  python3 build.py ../index-tuev.html tuev        Farbvariante „Prüfblau“

Eine Farbvariante ist eine Datei theme-<name>.css, die ans Ende des
Stylesheets gehängt wird und dort nur Farb-Token überschreibt.
"""
import base64, pathlib, sys

here = pathlib.Path(__file__).parent
out = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else here / "index.html"
theme = sys.argv[2] if len(sys.argv) > 2 else None

# Marke je Fassung: Ordnername der Schnipsel, Favicon, theme-color (dunkel)
FAV = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='7' fill='%23{bg}'/%3E{fig}%3C/svg%3E"
K_LETTER = "%3Ctext x='16' y='23' font-size='19' font-weight='700' font-family='Helvetica,Arial,sans-serif' text-anchor='middle' fill='%23fff'%3EK%3C/text%3E"
WINKEL   = "%3Cpath d='M9 7h4.6v13.4H24V25H9z' fill='%23fff'/%3E"

BRANDS = {
    None:   {"files": "schwarz", "fav": FAV.format(bg="0b0c0e", fig=K_LETTER), "dark": "#0b0c0e"},
    "tuev": {"files": "tuev",    "fav": FAV.format(bg="00396a", fig=WINKEL),   "dark": "#00396a"},
}
if theme not in BRANDS:
    sys.exit(f"Unbekannte Variante: {theme} (bekannt: {', '.join(str(k) for k in BRANDS)})")
brand = BRANDS[theme]

def b64(name):
    return base64.b64encode((here / name).read_bytes()).decode()

html = "".join((here / p).read_text(encoding="utf-8")
               for p in ("part1_head.html", "part2_body.html", "part3_script.html"))

tokens = {
    "{{FONT_SG}}":      b64("schibsted-grotesk-latin.woff2"),
    "{{FONT_IS}}":      b64("instrument-serif-latin.woff2"),
    "{{IMG_PORTRAIT}}": b64("nuri_cut.webp"),
    "{{IMG_ABOUT}}":    b64("nuri_portrait.webp"),
    "{{IMG_WAPPEN}}":   b64("wappen_s.webp"),
    "{{FAVICON}}":      brand["fav"],
    "{{DARKCOLOR}}":    brand["dark"],
    "{{BRAND_NAV}}":    (here / f"brand-{brand['files']}-nav.html").read_text(encoding="utf-8").strip(),
    "{{BRAND_FOOT}}":   (here / f"brand-{brand['files']}-foot.html").read_text(encoding="utf-8").strip(),
    "/* {{THEME}} */":  (here / f"theme-{theme}.css").read_text(encoding="utf-8") if theme else "",
}
for token, data in tokens.items():
    if token not in html:
        sys.exit(f"Token {token} nicht in der Vorlage gefunden")
    html = html.replace(token, data)

if "{{" in html:
    sys.exit("Es sind noch unaufgelöste Platzhalter enthalten")

out.write_text(html, encoding="utf-8")
print(f"{out}  ({out.stat().st_size/1024:.0f} KB){'  Variante: ' + theme if theme else ''}")
