#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Baut die Visitenkarte, druckfertig, im Look der gewaehlten Seite.

85 x 55 mm plus 3 mm Anschnitt ringsum – die Seiten sind deshalb
91 x 61 mm gross. Alles, was stehen bleiben muss, haelt 4 mm Abstand von
der Schnittkante; deutsche Druckereien verlangen 3 mm, die vierte ist
Reserve.

DIE ERSTE FASSUNG IST DURCHGEFALLEN. Sie hatte fuenf Schriftgroessen, die
Kontaktdaten standen auf 6,8 pt und der Grad auf 6,4 pt, und die Daten
liefen in zwei Spalten mit je eigener Kante. Was Setzer und Druckereien
dazu sagen, ist eindeutig:

  * Hoechstens drei Groessen, besser drei Ebenen: Name, Rolle, Rest.
  * Kontaktdaten nicht unter 8 pt; 7 pt ist die aeusserste Grenze, 6 pt
    liest niemand mehr.
  * Eine Ausrichtung durchhalten. Zwei Spalten sind zwei Kanten.
  * Struktur statt Dekoration – ein Zierstrich ist keine Struktur.
  * 25 bis 35 Prozent der Karte leer lassen.

Danach gebaut: drei Ebenen (Name 11 pt / Rolle 8 pt / Daten 8 pt), alles
auf einer Kante links, nichts unter 8 pt, kein Zierstrich. Unterschieden
wird ueber Gewicht und Farbe, nicht ueber immer neue Groessen.

Seite 1 ist die Vorderseite (hell, Kontaktdaten), Seite 2 die Rueckseite
(dunkel, Zeichen gross). So herum, weil die helle Seite die ist, die man
liest, und die dunkle die, die man wiedererkennt.

Farben und Schrift wie auf der Seite: #171d29, #003da5, #15171a, Rubik.
Die Zeichen kommen aus marke/logo/, werden also nicht neu gezeichnet.

DIE DATEI IST RGB. Chromium kann kein CMYK. Fuer den Druck muss die
Druckerei nach FOGRA51 (PSO Coated v3) wandeln; die Hex-Werte stehen im
LIESMICH als Referenz.

    python3 bau_visitenkarte.py
"""
import io
import os
import re
import subprocess

HIER = os.path.dirname(os.path.abspath(__file__))
LOGO = os.path.join(HIER, 'logo')
SEITE = os.path.join(HIER, os.pardir, 'index.html')
CHROM = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'
NODE_PW = '/opt/node22/lib/node_modules/playwright'

BREITE, HOEHE, ANSCHNITT = 85.0, 55.0, 3.0
SICHER = 4.0                      # 3 mm verlangen Druckereien, 1 mm Reserve

DUNKEL, BLAU, TIEF = '#171d29', '#003da5', '#002a73'
TEXT, GRAU = '#15171a', '#5d6470'

# Die Angaben stehen so auf der Seite. ACHTUNG: die Domain wechselt noch –
# vor dem Druck bestaetigen lassen. Ein falscher Aufdruck kostet die ganze
# Auflage, nicht eine Datei.
NAME = 'Nurettin Sogukcesme'
ROLLE = 'Freier Kfz-Sachverständiger'
GRAD = 'Ingenieur B.&nbsp;Eng. Maschinenbau'
ADRESSE = 'Mannheimer Straße 1, 64646 Heppenheim'
TELEFON = '+49 176 37998836'
MAIL = 'info@ing-nuri.de'
WEB = 'www.ing-nuri.de'
STRASSE = 'Mannheimer Straße 1'
ORT = '64646 Heppenheim'
CLAIM = 'Kfz-Gutachten mit Sachverstand'


def schrift():
    s = io.open(SEITE, encoding='utf-8').read()
    m = re.search(r"@font-face\{font-family:'([^']+)'.*?(base64,[A-Za-z0-9+/=]+)\)", s, re.S)
    if not m:
        raise SystemExit('Keine eingebettete Schrift in index.html gefunden')
    return m.group(1), m.group(2)


def zeichen(name, hoehe_mm):
    svg = io.open(os.path.join(LOGO, name + '.svg'), encoding='utf-8').read()
    svg = re.sub(r'\swidth="[\d.]+"\s+height="[\d.]+"', '', svg, count=1)
    return svg.replace('<svg ', '<svg style="height:%.2fmm;width:auto;display:block" '
                       % hoehe_mm, 1)


def karte():
    familie, daten = schrift()
    css = """
      @page { size: %(sb).0fmm %(sh).0fmm; margin: 0; }
      * { box-sizing: border-box; margin: 0; padding: 0; }
      @font-face { font-family: '%(fam)s'; font-style: normal; font-weight: 300 900;
                   src: url(data:font/woff2;%(daten)s) format('woff2'); }
      body { font-family: '%(fam)s', system-ui, sans-serif; color: %(text)s;
             -webkit-print-color-adjust: exact; print-color-adjust: exact; }
      .karte { width: %(sb).0fmm; height: %(sh).0fmm; position: relative;
               overflow: hidden; page-break-after: always; }
      .karte:last-child { page-break-after: auto; }
      .satz { position: absolute; inset: %(rand).1fmm; display: flex;
              flex-direction: column; }

      /* Vorderseite. Drei Ebenen, eine Kante, nichts unter 8 pt. */
      .vorn { background: #ffffff; }
      .vorn .marke { margin-bottom: auto; }
      .name { font-size: 11pt; font-weight: 800; letter-spacing: -0.02em;
              color: %(tief)s; line-height: 1.05; }
      .rolle { font-size: 8pt; font-weight: 600; color: %(blau)s;
               line-height: 1.35; margin-top: 1.4mm; }
      .rolle span { font-weight: 400; color: %(grau)s; }
      .daten { font-size: 8pt; line-height: 1.5; margin-top: 3.6mm; }
      .daten b { font-weight: 600; color: %(text)s; }
      .daten span { color: %(grau)s; display: block; }
      /* Rueckseite */
      .hinten { background: %(dunkel)s; }
      .hinten .satz { align-items: center; justify-content: center; }
    """ % dict(sb=BREITE + 2 * ANSCHNITT, sh=HOEHE + 2 * ANSCHNITT,
               rand=ANSCHNITT + SICHER, fam=familie, daten=daten,
               text=TEXT, tief=TIEF, blau=BLAU, grau=GRAU, dunkel=DUNKEL)

    vorn = """
    <div class="karte vorn"><div class="satz">
      <div class="marke">%s</div>
      <div>
        <div class="name">%s</div>
        <div class="rolle">%s<br><span>%s</span></div>
        <div class="daten">
          <span><b>%s</b></span>
          <span>%s</span>
          <span>%s</span>
          <span>%s</span>
        </div>
      </div>
    </div></div>""" % (zeichen('logo-quer-web-hell', 9.6), NAME, ROLLE, GRAD,
                       TELEFON, MAIL, WEB, ADRESSE)

    hinten = """
    <div class="karte hinten"><div class="satz">
      %s
    </div></div>""" % zeichen('logo-ohne-wagen-web-dunkel', 32.0)

    return ('<!doctype html><html lang="de"><head><meta charset="utf-8">'
            '<title>Visitenkarte Ingenieurbüro Kaltbrunn</title>'
            '<style>%s</style></head><body>%s%s</body></html>' % (css, vorn, hinten))


def drucken(html, ziel_name='Visitenkarte-Druck.pdf'):
    quelle = os.path.join(LOGO, '.karte.html')
    io.open(quelle, 'w', encoding='utf-8').write(html)
    ziel = os.path.join(LOGO, ziel_name)
    skript = """
const { chromium } = require('%s');
(async()=>{
  const b = await chromium.launch({executablePath:'%s'});
  const p = await b.newPage();
  await p.goto('file://%s');
  await p.evaluate(()=>document.fonts.ready);
  await p.waitForTimeout(400);
  await p.pdf({path:'%s', width:'%.0fmm', height:'%.0fmm', printBackground:true,
               margin:{top:'0',right:'0',bottom:'0',left:'0'}});
  await b.close();
})();
""" % (NODE_PW, CHROM, quelle, ziel, BREITE + 2 * ANSCHNITT, HOEHE + 2 * ANSCHNITT)
    lauf = os.path.join(LOGO, '.karte.js')
    io.open(lauf, 'w', encoding='utf-8').write(skript)
    subprocess.run(['node', lauf], check=True)
    os.remove(quelle)
    os.remove(lauf)
    return ziel


if __name__ == '__main__':
    ziel = drucken(karte())
    print('%s  %.1f KB  (%.0f x %.0f mm inkl. %.0f mm Anschnitt, 2 Seiten)'
          % (os.path.basename(ziel), os.path.getsize(ziel) / 1024,
             BREITE + 2 * ANSCHNITT, HOEHE + 2 * ANSCHNITT, ANSCHNITT))
