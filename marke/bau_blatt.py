#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Baut das Markenblatt als eine einzige Datei zum Weitergeben.

Bilal braucht etwas, das er Nurettin schicken kann. Ein Ordner mit
fuenfundzwanzig SVG geht dafuer nicht – ein PDF schon: es oeffnet sich auf
jedem Handy, und der Werbetechniker kann die Zeichnung direkt daraus
entnehmen, weil sie im PDF Vektor bleibt und kein Bild wird.

Das Blatt entsteht als HTML und wird von Chromium gedruckt. Die Zeichen
werden dabei nicht neu gebaut, sondern aus marke/logo/ genommen – was auf
dem Blatt steht, ist genau das, was in den Dateien steht.

    python3 bau_blatt.py

Ergebnis: marke/logo/Ingenieurbuero-Kaltbrunn-Zeichen.pdf
"""
import base64
import io
import os
import re
import subprocess
import sys

HIER = os.path.dirname(os.path.abspath(__file__))
LOGO = os.path.join(HIER, 'logo')
SEITE = os.path.join(HIER, os.pardir, 'index.html')
CHROM = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'
NODE_PW = '/opt/node22/lib/node_modules/playwright'

DUNKEL = '#171d29'
BLAU = '#003da5'
TIEF = '#002a73'
TEXT = '#15171a'
GRAU = '#5d6470'
LINIE = '#dce1e7'


def schrift():
    s = io.open(SEITE, encoding='utf-8').read()
    m = re.search(r"@font-face\{font-family:'([^']+)'.*?(base64,[A-Za-z0-9+/=]+)\)", s, re.S)
    if not m:
        raise SystemExit('Keine eingebettete Schrift in index.html gefunden')
    return m.group(1), m.group(2)


def zeichen(name, hoehe):
    """Ein Zeichen aus marke/logo/ als eingebettetes SVG, auf Hoehe gebracht."""
    svg = io.open(os.path.join(LOGO, name + '.svg'), encoding='utf-8').read()
    svg = re.sub(r'\swidth="[\d.]+"\s+height="[\d.]+"', '', svg, count=1)
    return svg.replace('<svg ', '<svg style="height:%dpx;width:auto;display:block" ' % hoehe, 1)


def feld(name, hoehe, grund, beschriftung):
    return ('<figure class="feld" style="background:%s">'
            '<div class="bild">%s</div>'
            '<figcaption>%s</figcaption></figure>'
            % (grund, zeichen(name, hoehe), beschriftung))


def blatt():
    familie, daten = schrift()
    css = """
      @page { size: A4; margin: 16mm 15mm; }
      * { box-sizing: border-box; margin: 0; padding: 0; }
      @font-face { font-family: '%(fam)s'; font-style: normal; font-weight: 300 900;
                   src: url(data:font/woff2;%(daten)s) format('woff2'); }
      body { font-family: '%(fam)s', system-ui, sans-serif; color: %(text)s;
             font-size: 9.4pt; line-height: 1.5; -webkit-print-color-adjust: exact;
             print-color-adjust: exact; }
      h1 { font-size: 19pt; font-weight: 800; letter-spacing: -0.02em; color: %(tief)s; }
      h2 { font-size: 10.5pt; font-weight: 800; letter-spacing: 0.09em;
           text-transform: uppercase; color: %(blau)s; margin: 0 0 9px;
           padding-bottom: 5px; border-bottom: 1.4px solid %(linie)s; }
      .kopf { display: flex; justify-content: space-between; align-items: flex-end;
              border-bottom: 2.4px solid %(tief)s; padding-bottom: 9px; margin-bottom: 16px; }
      .kopf p { color: %(grau)s; font-size: 8.6pt; text-align: right; }
      section { margin-bottom: 17px; }
      .gross { background: %(dunkel)s; border-radius: 8px; padding: 24px 26px;
               display: flex; justify-content: center; }
      .reihe { display: flex; gap: 9px; margin-top: 9px; }
      .feld { flex: 1; border: 1.2px solid %(linie)s; border-radius: 7px;
              padding: 13px 10px 9px; display: flex; flex-direction: column;
              align-items: center; gap: 9px; }
      .feld .bild { flex: 1; display: flex; align-items: center; }
      figcaption { font-size: 6.6pt; color: %(grau)s; text-align: center;
                   font-family: ui-monospace, monospace; word-break: break-all; }
      .feld[style*="%(dunkel)s"] figcaption { color: #aab4c4; }
      .farben { display: flex; gap: 9px; }
      .farbe { flex: 1; border: 1.2px solid %(linie)s; border-radius: 7px; overflow: hidden; }
      .farbe .klecks { height: 42px; }
      .farbe .wort { padding: 7px 9px; }
      .farbe b { display: block; font-size: 8.4pt; }
      .farbe span { font-family: ui-monospace, monospace; font-size: 7.6pt; color: %(grau)s; }
      .hinweise { display: flex; gap: 20px; }
      .hinweise div { flex: 1; }
      .hinweise b { color: %(tief)s; }
      ul { margin-left: 15px; }
      li { margin-bottom: 4px; }
      footer { margin-top: 16px; padding-top: 8px; border-top: 1.2px solid %(linie)s;
               color: %(grau)s; font-size: 7.6pt; display: flex; justify-content: space-between; }
    """ % dict(fam=familie, daten=daten, text=TEXT, tief=TIEF, blau=BLAU,
               grau=GRAU, linie=LINIE, dunkel=DUNKEL)

    farben = [('Marke', BLAU, '#ffffff'), ('Marke tief', TIEF, '#ffffff'),
              ('Dunkelfläche', DUNKEL, '#ffffff'), ('Text', TEXT, '#ffffff'),
              ('Text gedämpft', GRAU, '#ffffff'), ('Linie', LINIE, TEXT)]
    farbfelder = ''.join(
        '<div class="farbe"><div class="klecks" style="background:%s"></div>'
        '<div class="wort"><b>%s</b><span>%s</span></div></div>' % (hex_, name, hex_.upper())
        for name, hex_, _ in farben)

    html = """<!doctype html><html lang="de"><head><meta charset="utf-8">
<title>Ingenieurbüro Kaltbrunn – Zeichen</title><style>%s</style></head><body>

<div class="kopf">
  <h1>Ingenieurbüro Kaltbrunn</h1>
  <p>Das Zeichen und seine Fassungen<br>Alle Dateien sind Vektor (SVG)</p>
</div>

<section>
  <h2>Hauptfassung</h2>
  <div class="gross">%s</div>
</section>

<section>
  <h2>Waagerecht</h2>
  <div class="reihe">%s%s%s</div>
</section>

<section>
  <h2>Gestapelt</h2>
  <div class="reihe">%s%s%s%s</div>
</section>

<section>
  <h2>Farben</h2>
  <div class="farben">%s</div>
</section>

<section>
  <h2>Wozu welche Fassung</h2>
  <div class="hinweise">
    <div><ul>
      <li><b>Waagerecht</b> für Kopfzeilen, Briefbogen, E-Mail-Signatur — überall dort, wo wenig Höhe ist.</li>
      <li><b>Gestapelt</b> für Deckblätter, Stempel, Anzeigen, soziale Netze.</li>
      <li><b>Mit Wagen</b>, wo das Zeichen groß steht. Nachgemessen: unter
          20&nbsp;px eigener Höhe wird der Wagen zu Matsch — gestapelt heißt
          das etwa 15&nbsp;mm Gesamthöhe als Untergrenze.</li>
    </ul></div>
    <div><ul>
      <li><b>Nur das K</b> für kleine Anwendungen — nachgemessen bei
          120/64/40/28/18&nbsp;px: es trägt bis 18&nbsp;px, also gut 5&nbsp;mm.</li>
      <li><b>Heller Grund:</b> die dunkle Schrift-Fassung. <b>Dunkler Grund:</b> die weiße.</li>
      <li>Der Hintergrund der Dateien ist <b>durchsichtig</b>, nicht weiß.</li>
    </ul></div>
  </div>
</section>

<footer><span>Schriftzug in Kurven — keine Schrift nötig zum Öffnen. Die
einzelnen Dateien (SVG) liegen bei Bilal.</span>
<span>Hausschrift: %s</span></footer>
</body></html>""" % (
        css,
        zeichen('logo-quer-web-dunkel', 74),
        feld('logo-quer-web-hell', 40, '#ffffff', 'logo-quer-web-hell.svg'),
        feld('logo-quer-web-dunkel', 40, DUNKEL, 'logo-quer-web-dunkel.svg'),
        feld('logo-quer-web-dunkel-blau', 40, DUNKEL, 'logo-quer-web-dunkel-blau.svg'),
        feld('logo-web-hell', 88, '#ffffff', 'logo-web-hell.svg'),
        feld('logo-web-dunkel', 88, DUNKEL, 'logo-web-dunkel.svg'),
        feld('logo-ohne-wagen-web-hell', 88, '#ffffff', 'logo-ohne-wagen-web-hell.svg'),
        feld('logo-k-web-hell', 66, '#ffffff', 'logo-k-web-hell.svg'),
        farbfelder, familie)
    return html


def drucken(html):
    quelle = os.path.join(LOGO, '.blatt.html')
    io.open(quelle, 'w', encoding='utf-8').write(html)
    ziel = os.path.join(LOGO, 'Ingenieurbuero-Kaltbrunn-Zeichen.pdf')
    skript = """
const { chromium } = require('%s');
(async()=>{
  const b = await chromium.launch({executablePath:'%s'});
  const p = await b.newPage();
  await p.goto('file://%s');
  await p.evaluate(()=>document.fonts.ready);
  await p.waitForTimeout(400);
  await p.pdf({path:'%s', format:'A4', printBackground:true});
  await b.close();
})();
""" % (NODE_PW, CHROM, quelle, ziel)
    lauf = os.path.join(LOGO, '.blatt.js')
    io.open(lauf, 'w', encoding='utf-8').write(skript)
    subprocess.run(['node', lauf], check=True)
    os.remove(quelle)
    os.remove(lauf)
    return ziel


if __name__ == '__main__':
    ziel = drucken(blatt())
    print('%s  %.1f KB' % (os.path.basename(ziel), os.path.getsize(ziel) / 1024))
