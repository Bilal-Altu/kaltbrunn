#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Baut die zwei Zeichen, die nur die Visitenkarte braucht.

Bilal hat zwei Vorlagen geschickt:

  Vorderseite: das Zeichen MIT Wagen, darunter "Gutachten mit Sachverstand"
               – und zwar in derselben Schriftgroesse wie KALTBRUNN, nicht
               kleiner wie im Seitenfuss.
  Rueckseite:  das Zeichen OHNE Wagen, waagerecht: K, ein senkrechter
               Trennstrich, rechts daneben INGENIEURBÜRO ueber KALTBRUNN.

Beides sind Anordnungen, die es in marke/logo/ noch nicht gab. Gebaut wird
aus denselben Teilen wie alles andere – k.svg, wagen.svg und der Schrift
aus index.html – damit nichts auseinanderlaufen kann.

    python3 bau_kartenmarke.py
"""
import io
import os

import bau_logo as L

HIER = os.path.dirname(os.path.abspath(__file__))
AUS = os.path.join(HIER, 'logo')

CLAIM = 'Gutachten mit Sachverstand'      # so hat Bilal ihn geschrieben
TRENNER = 2.4                             # Staerke des senkrechten Strichs
TRENNER_LUFT = 22.0                       # Luft links und rechts davon


def bauen():
    familie, pfad = L.schrift_aus_seite()
    fett = L.schnitt(pfad, 800)
    normal = L.schnitt(pfad, 400)

    k_roh, wagen_roh = L.teil('k.svg'), L.teil('wagen.svg')
    kvb, wvb = L.viewbox(k_roh), L.viewbox(wagen_roh)
    k_breite = L.K_HOEHE * kvb[2] / kvb[3]
    wagen_breite = L.WAGEN_HOEHE * wvb[2] / wvb[3]

    wort_d, wort_b = L.text_zu_pfad(fett, 'INGENIEURBÜRO',
                                    L.WORT_GROESSE, L.WORT_SPERRUNG)
    ort_d, ort_b = L.text_zu_pfad(fett, 'KALTBRUNN',
                                  L.ORT_GROESSE, L.ORT_SPERRUNG)
    # Der Claim steht hier auf KALTBRUNN-Groesse, nicht auf 13,12.
    claim_d, claim_b = L.text_zu_pfad(normal, CLAIM, L.ORT_GROESSE)
    ort_gesamt = L.ORT_STRICH * 2 + L.ORT_LUECKE * 2 + ort_b

    ergebnis = []
    for ton, f in L.TOENE.items():
        if not ton.startswith('web'):
            continue
        k = L.farben(k_roh, {'k_balken': f['k_balken'], 'k_winkel': f['k_winkel']})
        wagen = L.farben(wagen_roh, {'w_lack': f['w_lack'], 'w_mittel': f['w_mittel'],
                                     'w_linie': f['w_linie']})

        # ---- Vorderseite: mit Wagen, Claim gross ------------------------
        reihe_b = k_breite + L.SPALT + wagen_breite
        reihe_h = max(L.K_HOEHE, L.WAGEN_HOEHE)
        innen = max(reihe_b, wort_b, ort_gesamt, claim_b)
        r = L.RAND
        y = r
        st = ['<g transform="translate(%.3f,%.3f) scale(%.6f)">%s</g>'
              % (r + (innen - reihe_b) / 2, y + (reihe_h - L.K_HOEHE) / 2,
                 L.K_HOEHE / kvb[3], L.inneres(k)),
              '<g transform="translate(%.3f,%.3f) scale(%.6f)">%s</g>'
              % (r + (innen - reihe_b) / 2 + k_breite + L.SPALT,
                 y + (reihe_h - L.WAGEN_HOEHE) / 2, L.WAGEN_HOEHE / wvb[3],
                 L.inneres(wagen))]
        y += reihe_h + L.ZEILEN_ABSTAND
        y += L.WORT_GROESSE * 0.74
        st.append('<g fill="%s" transform="translate(%.3f,%.3f)">%s</g>'
                  % (f['wort'], r + (innen - wort_b) / 2, y, wort_d))
        y += L.WORT_GROESSE * 0.26 + L.ZEILEN_ABSTAND
        mitte = y + L.ORT_GROESSE * 0.5
        xo = r + (innen - ort_gesamt) / 2
        st.append('<rect x="%.3f" y="%.3f" width="%.1f" height="2" fill="%s"/>'
                  % (xo, mitte - 1, L.ORT_STRICH, f['ort']))
        st.append('<g fill="%s" transform="translate(%.3f,%.3f)">%s</g>'
                  % (f['ort'], xo + L.ORT_STRICH + L.ORT_LUECKE,
                     y + L.ORT_GROESSE * 0.74, ort_d))
        st.append('<rect x="%.3f" y="%.3f" width="%.1f" height="2" fill="%s"/>'
                  % (xo + L.ORT_STRICH + L.ORT_LUECKE * 2 + ort_b, mitte - 1,
                     L.ORT_STRICH, f['ort']))
        y += L.ORT_GROESSE + L.ZEILEN_ABSTAND * 0.8
        y += L.ORT_GROESSE * 0.74
        st.append('<g fill="%s" transform="translate(%.3f,%.3f)">%s</g>'
                  % (f['claim'], r + (innen - claim_b) / 2, y, claim_d))
        y += L.ORT_GROESSE * 0.26
        b, h = innen + r * 2, y + r
        ergebnis.append(('karte-front-%s.svg' % ton,
                         kopf(b, h) + ''.join(st) + '</svg>'))

        # ---- Rueckseite: ohne Wagen, waagerecht mit Trennstrich ---------
        block_b = max(wort_b, ort_gesamt)
        block_h = L.WORT_GROESSE + L.ZEILEN_ABSTAND + L.ORT_GROESSE
        innen_b = k_breite + TRENNER_LUFT + TRENNER + TRENNER_LUFT + block_b
        innen_h = max(L.K_HOEHE, block_h)
        r = L.RAND * 0.7
        st = ['<g transform="translate(%.3f,%.3f) scale(%.6f)">%s</g>'
              % (r, r + (innen_h - L.K_HOEHE) / 2, L.K_HOEHE / kvb[3], L.inneres(k))]
        # Der Trennstrich reicht ueber die Hoehe des K, nicht ueber das Bild.
        # Er steht voll deckend, nicht abgeschwaecht: auf Bilals Vorlage ist
        # er dieselbe Farbe wie INGENIEURBÜRO. Ein grauer Strich daneben
        # sieht nach Versehen aus.
        tx = r + k_breite + TRENNER_LUFT
        st.append('<rect x="%.3f" y="%.3f" width="%.1f" height="%.1f" fill="%s"/>'
                  % (tx, r + (innen_h - L.K_HOEHE) / 2, TRENNER, L.K_HOEHE, f['wort']))
        bx = tx + TRENNER + TRENNER_LUFT
        by = r + (innen_h - block_h) / 2
        st.append('<g fill="%s" transform="translate(%.3f,%.3f)">%s</g>'
                  % (f['wort'], bx, by + L.WORT_GROESSE * 0.74, wort_d))
        y2 = by + L.WORT_GROESSE + L.ZEILEN_ABSTAND
        mitte = y2 + L.ORT_GROESSE * 0.5
        xo = bx + (block_b - ort_gesamt) / 2
        st.append('<rect x="%.3f" y="%.3f" width="%.1f" height="2" fill="%s"/>'
                  % (xo, mitte - 1, L.ORT_STRICH, f['ort']))
        st.append('<g fill="%s" transform="translate(%.3f,%.3f)">%s</g>'
                  % (f['ort'], xo + L.ORT_STRICH + L.ORT_LUECKE,
                     y2 + L.ORT_GROESSE * 0.74, ort_d))
        st.append('<rect x="%.3f" y="%.3f" width="%.1f" height="2" fill="%s"/>'
                  % (xo + L.ORT_STRICH + L.ORT_LUECKE * 2 + ort_b, mitte - 1,
                     L.ORT_STRICH, f['ort']))
        b, h = innen_b + r * 2, innen_h + r * 2
        ergebnis.append(('karte-marke-%s.svg' % ton,
                         kopf(b, h) + ''.join(st) + '</svg>'))

    os.makedirs(AUS, exist_ok=True)
    for name, svg in ergebnis:
        io.open(os.path.join(AUS, name), 'w', encoding='utf-8').write(svg)
    return ergebnis


def kopf(b, h):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %.2f %.2f" '
            'width="%.0f" height="%.0f" fill="none" role="img" '
            'aria-label="Ingenieurbüro Kaltbrunn">'
            '<title>Ingenieurbüro Kaltbrunn</title>' % (b, h, b, h))


if __name__ == '__main__':
    for name, svg in bauen():
        print('  marke/logo/%-34s %6.1f KB' % (name, len(svg.encode('utf-8')) / 1024))
