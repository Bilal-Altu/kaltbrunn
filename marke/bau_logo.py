#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Baut das ganze Zeichen als eigenstaendige SVG-Dateien.

Auf der Seite entsteht die Marke aus drei Teilen, die der Browser
zusammensetzt: dem K (k.svg), dem Wagen (wagen.svg) und dem Schriftzug
als echtem Text. Als Datei zum Weitergeben taugt das nicht – wer sie
oeffnet, hat die Schrift nicht und bekommt einen anderen Schriftzug.

Dieses Skript setzt dieselben Teile zu einer Datei zusammen und wandelt
den Schriftzug in Kurven um. Die Schrift wird dafuer aus index.html
gezogen, nicht aus einer Kopie daneben: so kann der Schriftzug in der
Datei gar nicht von dem auf der Seite abweichen.

Groessen und Abstaende sind dieselben wie in der Fusszeile und stammen
aus der Messung an Nurettins Vorlage: der Wagen ist 1,082 mal so hoch wie
das K, der Spalt betraegt 6 px bei 89 px K-Hoehe.

    python3 bau_logo.py

Ergebnis in marke/logo/:
    logo-dunkel.svg   ganzes Zeichen fuer dunklen Grund (wie in der Fusszeile)
    logo-hell.svg     ganzes Zeichen fuer hellen Grund
    logo-zeile.svg    nur K und Wagen, ohne Schriftzug
    logo-k.svg        nur das Monogramm
"""
import base64
import io
import os
import re
import tempfile

from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from fontTools.pens.svgPathPen import SVGPathPen

HIER = os.path.dirname(os.path.abspath(__file__))
SEITE = os.path.join(HIER, os.pardir, 'index.html')
AUS = os.path.join(HIER, 'logo')

# --- Masse aus der Fusszeile (px bei K-Hoehe 89) -------------------------
K_HOEHE = 89.0
WAGEN_HOEHE = 96.0          # 1,082 x K, an der Vorlage gemessen
SPALT = 6.0
ZEILEN_ABSTAND = 9.0
WORT_GROESSE = 23.2         # 1,45 rem
WORT_SPERRUNG = 0.20        # em
ORT_GROESSE = 16.8          # 1,05 rem
ORT_SPERRUNG = 0.28         # em
ORT_STRICH = 52.0
ORT_LUECKE = 14.0
CLAIM_GROESSE = 13.12       # 0,82 rem
RAND = 28.0

# Zwei Farbwelten:
#
# "dunkel"/"hell" gehoeren zu unserer Seite (Fusszeile auf Marineblau).
#
# "web-*" ist auf die Seite abgestimmt, fuer die sich Bilal entschieden hat
# (ak-learn-code.github.io/Ingenieurbuero-Kaltbrunn). Deren Kopfzeile ist
# fast schwarz (#171d29), und genau daran scheitern ihre eigenen
# Markenblaus: #003da5 kommt dort auf Kontrast 1,78, #0050cc auf 2,43 –
# der Balken des K ist auf dem Grund praktisch unsichtbar. Nachgemessen,
# deshalb steht es hier. Der helle Winkel #4d8bf5 (5,09) ist derselbe
# Blauton, nur aufgehellt.
TOENE = {
    'dunkel': dict(grund='#0a2352',
                   k_balken='#ffffff', k_winkel='#4d8bf5',
                   w_lack='#ffffff', w_mittel='#7ea8e8', w_linie='#0a2260',
                   wort='#ffffff', ort='#8fbaff', claim='#b9c9e4'),
    'hell':   dict(grund='#ffffff',
                   k_balken='#002a73', k_winkel='#2563eb',
                   w_lack='#ffffff', w_mittel='#bcd3f0', w_linie='#12356e',
                   wort='#002a73', ort='#2563eb', claim='#4a5568'),
    # Farben aus deren CSS: --color-brand #003da5, --color-brand-deep
    # #002a73, --color-text #15171a, --color-text-muted #5d6470.
    'web-dunkel': dict(grund='#171d29',
                       k_balken='#ffffff', k_winkel='#4d8bf5',
                       w_lack='#ffffff', w_mittel='#7ea8e8', w_linie='#002a73',
                       wort='#ffffff', ort='#8fbaff', claim='#aab4c4'),
    'web-hell':   dict(grund='#ffffff',
                       k_balken='#002a73', k_winkel='#003da5',
                       w_lack='#ffffff', w_mittel='#bcd3f0', w_linie='#002a73',
                       wort='#002a73', ort='#003da5', claim='#5d6470'),
}


def schrift_aus_seite():
    """Holt die eingebettete Schrift aus index.html."""
    s = io.open(SEITE, encoding='utf-8').read()
    m = re.search(r"@font-face\{font-family:'([^']+)'.*?base64,([A-Za-z0-9+/=]+)\)", s, re.S)
    if not m:
        raise SystemExit('Keine eingebettete Schrift in index.html gefunden')
    roh = base64.b64decode(m.group(2))
    pfad = os.path.join(tempfile.mkdtemp(), 'schrift.woff2')
    open(pfad, 'wb').write(roh)
    return m.group(1), pfad


def schnitt(pfad, gewicht):
    """Variable Schrift auf ein festes Gewicht festlegen."""
    f = TTFont(pfad)
    if 'fvar' in f:
        f = instancer.instantiateVariableFont(f, {'wght': gewicht}, inplace=False)
    return f


def text_zu_pfad(f, text, groesse, sperrung_em=0.0):
    """Text in einen einzigen SVG-Pfad umwandeln. Gibt (d, breite) zurueck."""
    upem = f['head'].unitsPerEm
    massstab = groesse / upem
    cmap = f.getBestCmap()
    gs = f.getGlyphSet()
    hmtx = f['hmtx']
    teile = []
    x = 0.0
    sperrung = sperrung_em * groesse / massstab      # in Fonteinheiten
    for i, zeichen in enumerate(text):
        name = cmap.get(ord(zeichen))
        if name is None:
            raise SystemExit('Zeichen %r fehlt in der Schrift' % zeichen)
        stift = SVGPathPen(gs)
        gs[name].draw(stift)
        d = stift.getCommands()
        if d:
            teile.append('<path d="%s" transform="translate(%.3f,0)"/>' % (d, x))
        x += hmtx[name][0]
        if i < len(text) - 1:
            x += sperrung
    breite = x * massstab
    # y nach unten spiegeln, Font-Koordinaten laufen nach oben
    inhalt = ''.join(teile)
    gruppe = ('<g transform="scale(%.6f,-%.6f)">%s</g>' % (massstab, massstab, inhalt))
    return gruppe, breite


def teil(name):
    return io.open(os.path.join(HIER, name), encoding='utf-8').read()


def farben(svg, zuordnung):
    for schluessel, wert in zuordnung.items():
        svg = re.sub(r'var\(--%s,#[0-9a-fA-F]+\)' % schluessel.replace('_', '-'), wert, svg)
    return svg


def inneres(svg):
    """Inhalt eines SVG ohne die aeussere Huelle."""
    return re.sub(r'^<svg[^>]*>|</svg>$', '', svg.strip())


def viewbox(svg):
    m = re.search(r'viewBox="([\d.\s-]+)"', svg)
    return [float(v) for v in m.group(1).split()]


def bauen():
    familie, pfad = schrift_aus_seite()
    fett = schnitt(pfad, 800)
    normal = schnitt(pfad, 400)

    k_roh, wagen_roh = teil('k.svg'), teil('wagen.svg')
    kvb, wvb = viewbox(k_roh), viewbox(wagen_roh)
    k_breite = K_HOEHE * kvb[2] / kvb[3]
    wagen_breite = WAGEN_HOEHE * wvb[2] / wvb[3]
    reihe_breite = k_breite + SPALT + wagen_breite
    reihe_hoehe = max(K_HOEHE, WAGEN_HOEHE)

    wort_d, wort_b = text_zu_pfad(fett, 'INGENIEURBÜRO', WORT_GROESSE, WORT_SPERRUNG)
    ort_d, ort_b = text_zu_pfad(fett, 'KALTBRUNN', ORT_GROESSE, ORT_SPERRUNG)
    claim_d, claim_b = text_zu_pfad(normal, 'Kfz-Gutachten mit Sachverstand', CLAIM_GROESSE)
    ort_gesamt = ORT_STRICH * 2 + ORT_LUECKE * 2 + ort_b

    inhalt_breite = max(reihe_breite, wort_b, ort_gesamt, claim_b)
    ergebnis = []

    def zeichen(f, mit_wagen):
        """Setzt ein ganzes Zeichen zusammen. Ohne Wagen steht das K allein
        ueber dem Schriftzug – es behaelt dabei genau dieselbe Hoehe wie in
        der vollen Fassung, damit beide Dateien nebeneinander im selben
        Massstab stehen."""
        k = farben(k_roh, {'k_balken': f['k_balken'], 'k_winkel': f['k_winkel']})
        wagen = farben(wagen_roh, {'w_lack': f['w_lack'], 'w_mittel': f['w_mittel'],
                                   'w_linie': f['w_linie']})
        reihe_b = reihe_breite if mit_wagen else k_breite
        reihe_h = reihe_hoehe if mit_wagen else K_HOEHE
        breite_innen = max(reihe_b, wort_b, ort_gesamt, claim_b)

        y = RAND
        stuecke = []
        x0 = RAND + (breite_innen - reihe_b) / 2
        stuecke.append('<g transform="translate(%.3f,%.3f) scale(%.6f)">%s</g>'
                       % (x0, y + (reihe_h - K_HOEHE) / 2, K_HOEHE / kvb[3], inneres(k)))
        if mit_wagen:
            stuecke.append('<g transform="translate(%.3f,%.3f) scale(%.6f)">%s</g>'
                           % (x0 + k_breite + SPALT, y + (reihe_h - WAGEN_HOEHE) / 2,
                              WAGEN_HOEHE / wvb[3], inneres(wagen)))
        y += reihe_h + ZEILEN_ABSTAND

        y += WORT_GROESSE * 0.74
        stuecke.append('<g fill="%s" transform="translate(%.3f,%.3f)">%s</g>'
                       % (f['wort'], RAND + (breite_innen - wort_b) / 2, y, wort_d))
        y += WORT_GROESSE * 0.26 + ZEILEN_ABSTAND

        mitte = y + ORT_GROESSE * 0.5
        xo = RAND + (breite_innen - ort_gesamt) / 2
        stuecke.append('<rect x="%.3f" y="%.3f" width="%.1f" height="2" fill="%s"/>'
                       % (xo, mitte - 1, ORT_STRICH, f['ort']))
        stuecke.append('<g fill="%s" transform="translate(%.3f,%.3f)">%s</g>'
                       % (f['ort'], xo + ORT_STRICH + ORT_LUECKE, y + ORT_GROESSE * 0.74, ort_d))
        stuecke.append('<rect x="%.3f" y="%.3f" width="%.1f" height="2" fill="%s"/>'
                       % (xo + ORT_STRICH + ORT_LUECKE * 2 + ort_b, mitte - 1, ORT_STRICH, f['ort']))
        y += ORT_GROESSE + ZEILEN_ABSTAND * 0.7

        y += CLAIM_GROESSE * 0.74
        stuecke.append('<g fill="%s" transform="translate(%.3f,%.3f)">%s</g>'
                       % (f['claim'], RAND + (breite_innen - claim_b) / 2, y, claim_d))
        y += CLAIM_GROESSE * 0.26

        b = breite_innen + RAND * 2
        h = y + RAND
        return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %.2f %.2f" '
                'width="%.0f" height="%.0f" fill="none" role="img" '
                'aria-label="Ingenieurbüro Kaltbrunn">' % (b, h, b, h)
                + '<title>Ingenieurbüro Kaltbrunn</title>' + ''.join(stuecke) + '</svg>'), k

    for ton, f in TOENE.items():
        voll, k = zeichen(f, True)
        ohne, _ = zeichen(f, False)
        ergebnis.append(('logo-%s.svg' % ton, voll))
        ergebnis.append(('logo-ohne-wagen-%s.svg' % ton, ohne))

        # Reihe (K + Wagen, ohne Schriftzug) und Monogramm allein – fuer
        # jede Farbfassung, nicht nur fuer eine. Im Kopf der Seite steht
        # genau das Monogramm, und dort entscheidet die Farbe alles.
        wagen = farben(wagen_roh, {'w_lack': f['w_lack'], 'w_mittel': f['w_mittel'],
                                   'w_linie': f['w_linie']})
        b = reihe_breite + RAND
        h = reihe_hoehe + RAND
        zeile = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %.2f %.2f" '
                 'width="%.0f" height="%.0f" fill="none" role="img" '
                 'aria-label="Ingenieurbüro Kaltbrunn">' % (b, h, b, h)
                 + '<g transform="translate(%.3f,%.3f) scale(%.6f)">%s</g>'
                   % (RAND / 2, RAND / 2 + (reihe_hoehe - K_HOEHE) / 2, K_HOEHE / kvb[3], inneres(k))
                 + '<g transform="translate(%.3f,%.3f) scale(%.6f)">%s</g>'
                   % (RAND / 2 + k_breite + SPALT, RAND / 2 + (reihe_hoehe - WAGEN_HOEHE) / 2,
                      WAGEN_HOEHE / wvb[3], inneres(wagen))
                 + '</svg>')
        # Das Monogramm bekommt feste Masse und etwas Luft. Ohne Rand sitzt
        # es beim Platzieren randlos auf der Kante; k.svg selbst bleibt
        # unveraendert, das prueft der CI-Waechter gegen index.html.
        r = 10.0
        k_datei = ('<svg xmlns="http://www.w3.org/2000/svg" '
                   'viewBox="%.1f %.1f %.1f %.1f" width="%.0f" height="%.0f" '
                   'fill="none" role="img" aria-label="Ingenieurbüro Kaltbrunn">'
                   % (-r, -r, kvb[2] + 2 * r, kvb[3] + 2 * r,
                      (kvb[2] + 2 * r) * 2, (kvb[3] + 2 * r) * 2)
                   + '<title>Ingenieurbüro Kaltbrunn</title>' + inneres(k) + '</svg>')
        if ton == 'dunkel':
            ergebnis.append(('logo-zeile.svg', zeile))
            ergebnis.append(('logo-k.svg', k_datei))
        else:
            ergebnis.append(('logo-zeile-%s.svg' % ton, zeile))
            ergebnis.append(('logo-k-%s.svg' % ton, k_datei))

    os.makedirs(AUS, exist_ok=True)
    for name, svg in ergebnis:
        io.open(os.path.join(AUS, name), 'w', encoding='utf-8').write(svg)
    return familie, ergebnis


if __name__ == '__main__':
    familie, dateien = bauen()
    print('Schriftzug in Kurven umgewandelt (%s)' % familie)
    for name, svg in dateien:
        print('  marke/logo/%-18s %6.1f KB' % (name, len(svg.encode('utf-8')) / 1024))
