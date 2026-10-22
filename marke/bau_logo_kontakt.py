#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Marke mit Kontaktdaten – als EIGENE Dateien, nicht als neues Logo.

Nurettin hat gefragt, ob die Kontaktdaten mit ins Logo koennen. Die
Antwort ist zweigeteilt:

NEIN, nicht ins Logo. Ein Logo muss auf dem Stempel funktionieren, auf
der Fahrzeugtuer, im Briefkopf, als 16 Pixel grosses Zeichen im Browser-
Reiter. Mit einer Telefonnummer darin ist es an jeder dieser Stellen
entweder unlesbar oder falsch – und wenn sich eine Angabe aendert, ist
jede Datei auf einen Schlag Altpapier. Die Domain steht noch nicht
endgueltig fest; genau dieser Fall droht hier real.

JA, als eigene Fassung. Was er meint, ist kein Logo, sondern ein
Werbemittel: Marke plus Kontakt, fuer Flyer, Fahrzeugbeschriftung,
E-Mail-Signatur, Instagram. Genau das baut dieses Skript – daneben, nicht
anstelle. Die Dateien heissen deshalb logo-kontakt-… und nicht logo-….

Zwei Anordnungen:

    hoch  Zeichen mit Wagen, Claim, darunter der Kontakt gestapelt.
          Fuer Flyer, Aushang, Beitrag in sozialen Netzen.
    quer  Das waagerechte Band, darunter ein Strich und der Kontakt in
          EINER Zeile. Fuer Signatur, Brieffuss, Fahrzeugbeschriftung.

Gerechnet wird in denselben Einheiten wie alle Markendateien: das K ist
89 hoch. Der Schriftzug wird wie dort in Kurven gewandelt.

    python3 bau_logo_kontakt.py
"""
import io
import os
import re

import bau_logo as L
import bau_kartenmarke as M

HIER = os.path.dirname(os.path.abspath(__file__))
AUS = os.path.join(HIER, 'logo')

TELEFON = '+49 176 37998836'
MAIL = 'info@ing-kaltbrunn.de'
WEB = 'ing-kaltbrunn.de'

# Kontakt steht kleiner als KALTBRUNN und groesser als nichts: dieselbe
# Groesse wie der Claim im Seitenfuss.
KONTAKT = L.CLAIM_GROESSE
ZEICHEN = KONTAKT * 1.45                  # Kantenlaenge der Symbole
ZEICHEN_STRICH = 2.0                      # in den 24 Einheiten der Symbole
ZEICHEN_LUFT = KONTAKT * 0.55             # Symbol -> Text
PUNKT_LUFT = KONTAKT * 0.45               # Text -> WhatsApp-Zeichen
WA = KONTAKT * 1.15                       # Durchmesser des WhatsApp-Zeichens
ZEILE = KONTAKT * 1.95                    # Zeilenabstand im Kontaktblock
TRENNER = KONTAKT * 2.2                   # Luft zwischen den Angaben, quer
GRUEN = '#25d366'


def symbol(name, x, mitte_y, farbe, kante=ZEICHEN):
    roh = io.open(os.path.join(HIER, 'symbole', 'lucide-%s.svg' % name),
                  encoding='utf-8').read()
    vb = L.viewbox(roh)
    s = kante / vb[3]
    return ('<g fill="none" stroke="%s" stroke-width="%.2f" '
            'stroke-linecap="round" stroke-linejoin="round" '
            'transform="translate(%.3f,%.3f) scale(%.6f)">%s</g>'
            % (farbe, ZEICHEN_STRICH, x, mitte_y - kante / 2.0, s, inhalt(roh)))


def wa_zeichen(mx, my, d):
    roh = io.open(os.path.join(HIER, 'whatsapp.svg'), encoding='utf-8').read()
    kurve = re.search(r'<path[^>]*\bd="([^"]+)"', roh).group(1)
    g = d * 0.60
    return ('<circle cx="%.3f" cy="%.3f" r="%.3f" fill="%s"/>'
            '<g transform="translate(%.3f,%.3f) scale(%.6f)">'
            '<path d="%s" fill="#ffffff"/></g>'
            % (mx, my, d / 2.0, GRUEN, mx - g / 2.0, my - g / 2.0, g / 24.0, kurve))


def inhalt(svg):
    svg = re.sub(r'<!--.*?-->', '', svg, flags=re.S).strip()
    svg = re.sub(r'^<svg\b[^>]*>', '', svg, flags=re.S)
    return re.sub(r'</svg>\s*$', '', svg).strip()


def angabe(f, zeichen, text, farbe, ton, x, mitte_y, mit_wa=False):
    """Ein Symbol mit Text daneben. Gibt (svg, breite) zurueck."""
    st = [symbol(zeichen, x, mitte_y, ton['ort'])]
    d, b = L.text_zu_pfad(f, text, KONTAKT)
    tx = x + ZEICHEN + ZEICHEN_LUFT
    st.append('<g fill="%s" transform="translate(%.3f,%.3f)">%s</g>'
              % (farbe, tx, mitte_y + M.versalhoehe(f) * KONTAKT / 2.0, d))
    breite = ZEICHEN + ZEICHEN_LUFT + b
    if mit_wa:
        st.append(wa_zeichen(tx + b + PUNKT_LUFT + WA / 2.0, mitte_y, WA))
        breite += PUNKT_LUFT + WA
    return ''.join(st), breite


def kopf(b, h):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %.2f %.2f" '
            'width="%.0f" height="%.0f" fill="none" role="img" '
            'aria-label="Ingenieurbüro Kaltbrunn – Kontakt">'
            '<title>Ingenieurbüro Kaltbrunn – Kontakt</title>' % (b, h, b, h))


def zeichenteil(name, ton):
    """Eine fertige Markendatei einsetzen, ohne ihren Rand."""
    svg = io.open(os.path.join(AUS, '%s-%s.svg' % (name, ton)),
                  encoding='utf-8').read()
    vb = L.viewbox(svg)
    rand = L.RAND * 0.7 if name.startswith('karte-marke') else L.RAND
    return L.inneres(svg), vb[2] - 2 * rand, vb[3] - 2 * rand, rand


def bauen():
    _, pfad = L.schrift_aus_seite()
    halbfett = L.schnitt(pfad, 600)
    normal = L.schnitt(pfad, 400)

    ergebnis = []
    for ton, f in L.TOENE.items():
        if not ton.startswith('web'):
            continue
        posten = [('smartphone', TELEFON, halbfett, True),
                  ('mail', MAIL, normal, False),
                  ('globe', WEB, normal, False)]

        # ---- hoch: Zeichen mit Wagen, Kontakt gestapelt darunter -------
        mark, mb, mh, rand = zeichenteil('karte-front', ton)
        breiten = []
        for z, t, s, w in posten:
            _, b = angabe(s, z, t, f['claim'], f, 0, 0, w)
            breiten.append(b)
        block_b = max(breiten)
        innen = max(mb, block_b)
        r = L.RAND
        st = ['<g transform="translate(%.3f,%.3f)">%s</g>'
              % (r + (innen - mb) / 2.0 - rand, r - rand, mark)]
        y = r + mh + L.ZEILEN_ABSTAND * 2.2
        bx = r + (innen - block_b) / 2.0
        for i, (z, t, s, w) in enumerate(posten):
            g, _ = angabe(s, z, t, f['claim'], f, bx, y + ZEILE * i + ZEICHEN / 2.0, w)
            st.append(g)
        h = y + ZEILE * (len(posten) - 1) + ZEICHEN + r
        ergebnis.append(('logo-kontakt-hoch-%s.svg' % ton,
                         kopf(innen + 2 * r, h) + ''.join(st) + '</svg>'))

        # ---- quer: Band, Strich, Kontakt in einer Zeile -----------------
        mark, mb, mh, rand = zeichenteil('karte-marke', ton)
        teile = []
        gesamt = 0.0
        for i, (z, t, s, w) in enumerate(posten):
            _, b = angabe(s, z, t, f['claim'], f, 0, 0, w)
            teile.append(b)
            gesamt += b + (TRENNER if i < len(posten) - 1 else 0)
        innen = max(mb, gesamt)
        r = L.RAND * 0.7
        st = ['<g transform="translate(%.3f,%.3f)">%s</g>'
              % (r + (innen - mb) / 2.0 - rand, r - rand, mark)]
        sy = r + mh + L.ZEILEN_ABSTAND * 1.6
        st.append('<rect x="%.3f" y="%.3f" width="%.2f" height="1.6" '
                  'fill="%s" opacity="0.35"/>' % (r, sy, innen, f['ort']))
        zy = sy + L.ZEILEN_ABSTAND * 1.6 + ZEICHEN / 2.0
        x = r + (innen - gesamt) / 2.0
        for (z, t, s, w), b in zip(posten, teile):
            g, _ = angabe(s, z, t, f['claim'], f, x, zy, w)
            st.append(g)
            x += b + TRENNER
        h = zy + ZEICHEN / 2.0 + r
        ergebnis.append(('logo-kontakt-quer-%s.svg' % ton,
                         kopf(innen + 2 * r, h) + ''.join(st) + '</svg>'))

    for name, svg in ergebnis:
        io.open(os.path.join(AUS, name), 'w', encoding='utf-8').write(svg)
    return ergebnis


if __name__ == '__main__':
    for name, svg in bauen():
        print('  marke/logo/%-36s %6.1f KB' % (name, len(svg.encode('utf-8')) / 1024))
