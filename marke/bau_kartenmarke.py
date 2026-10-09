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

CLAIM = 'Kfz-Gutachten mit Sachverstand'  # wie im Logo und auf der Seite

# --- Die waagerechte Fassung, an Bilals Vorlage gemessen ----------------
#
# Die erste Fassung war zu gedrungen: der Schriftzug stand dort auf den
# Groessen der Fusszeile (23,2 / 16,8) und war damit halb so gross wie auf
# der Vorlage. Das Zeichen kam auf 4,68 : 1, die Vorlage auf 8,4 : 1 –
# deshalb zog es sich eben nicht von links nach rechts.
#
# Neu gemessen an ref-4 (K dort 138 px hoch), alles auf K = 89 gerechnet:
#
#   K                         150 x 138 px   1,087 x K breit
#   Luft K -> Trennstrich      67 px         0,486 x K
#   Trennstrich                 4 x 165 px   0,029 / 1,196 x K
#   Luft Trennstrich -> Text   69 px         0,500 x K
#   Block                    1093 px breit   7,920 x K
#   INGENIEURBÜRO              59 px Versal  0,428 x K
#   Zeilenluft                 37 px         0,268 x K
#   KALTBRUNN                  43 px Versal  0,312 x K
#   KALTBRUNN, nur das Wort   632 px breit   4,580 x K
#   Strich                    188 px lang    1,362 x K, 5 px stark
#   Luft Strich -> Wort        44 px         0,319 x K
#
# Der Block ist damit so hoch wie das K (38,05 + 23,86 + 27,73 = 89,6) –
# auf der Vorlage ist er es auch. Der Trennstrich ist das hoechste Teil,
# er steht oben und unten ueber.
B_K_LUFT = 43.21
B_TRENNER = 2.58
B_TRENNER_HOCH = 106.41
B_TEXT_LUFT = 44.50
B_BLOCK_BREIT = 704.91
B_WORT_VERSAL = 38.05
B_ZEILENLUFT = 23.86
B_ORT_VERSAL = 27.73
B_ORT_WORT = 407.59
B_STRICH = 121.25
B_STRICH_LUFT = 28.38
B_STRICH_STARK = 3.22                     # 5 px bei K = 138


def versalhoehe(f):
    """Versalhoehe der Schrift in Fonteinheiten, auf 1 em bezogen."""
    os2 = f['OS/2']
    h = getattr(os2, 'sCapHeight', 0) or 0
    if not h:                                  # aeltere Tabellen fuehren sie nicht
        from fontTools.pens.boundsPen import BoundsPen
        gs = f.getGlyphSet()
        stift = BoundsPen(gs)
        gs[f.getBestCmap()[ord('H')]].draw(stift)
        h = stift.bounds[3]
    return h / f['head'].unitsPerEm


def ueber_versal(f, text, groesse):
    """Wie weit ein Text ueber die Versalhoehe hinausragt (Umlautpunkte).

    INGENIEURBÜRO hat ein Ü. Dessen Punkte stehen ueber der Versalhoehe,
    und wenn die Datei ihre Hoehe nur aus der Versalhoehe rechnet, haengen
    sie ausserhalb – auf der Karte sass die oberste Druckfarbe dadurch
    0,27 mm ueber dem Sicherheitsrand. Nachgemessen, nicht geschaetzt.
    """
    from fontTools.pens.boundsPen import BoundsPen
    upem = f['head'].unitsPerEm
    gs, cmap = f.getGlyphSet(), f.getBestCmap()
    hoch = 0.0
    for z in set(text):
        name = cmap.get(ord(z))
        if name is None:
            continue
        stift = BoundsPen(gs)
        gs[name].draw(stift)
        if stift.bounds:
            hoch = max(hoch, stift.bounds[3])
    return max(0.0, hoch / upem - versalhoehe(f)) * groesse


def gesperrt_auf(f, text, groesse, ziel):
    """Sperrung so waehlen, dass der Text genau ziel breit wird."""
    _, roh = L.text_zu_pfad(f, text, groesse, 0.0)
    return (ziel - roh) / ((len(text) - 1) * groesse)


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
        # Masse oben, an Bilals Vorlage gemessen. Der Schriftzug wird hier
        # nicht aus den Fusszeilengroessen genommen, sondern aus der
        # Versalhoehe aufgebaut – nur so stimmt das Verhaeltnis zum K.
        wg = B_WORT_VERSAL / versalhoehe(fett)
        og = B_ORT_VERSAL / versalhoehe(fett)
        b_wort_d, _ = L.text_zu_pfad(fett, 'INGENIEURBÜRO', wg,
                                     gesperrt_auf(fett, 'INGENIEURBÜRO', wg,
                                                  B_BLOCK_BREIT))
        b_ort_d, _ = L.text_zu_pfad(fett, 'KALTBRUNN', og,
                                    gesperrt_auf(fett, 'KALTBRUNN', og, B_ORT_WORT))

        block_h = B_WORT_VERSAL + B_ZEILENLUFT + B_ORT_VERSAL
        innen_b = (k_breite + B_K_LUFT + B_TRENNER + B_TEXT_LUFT + B_BLOCK_BREIT)
        # Hoehe aus der wirklichen Druckfarbe, nicht aus der Versalhoehe:
        # die Punkte des Ü stehen darueber.
        ueber = ueber_versal(fett, 'INGENIEURBÜRO', wg)
        oben = min(-L.K_HOEHE / 2.0, -B_TRENNER_HOCH / 2.0,
                   -block_h / 2.0 - ueber)
        unten = max(L.K_HOEHE / 2.0, B_TRENNER_HOCH / 2.0, block_h / 2.0)
        innen_h = unten - oben
        r = L.RAND * 0.7
        mitte_y = r - oben
        st = ['<g transform="translate(%.3f,%.3f) scale(%.6f)">%s</g>'
              % (r, mitte_y - L.K_HOEHE / 2.0, L.K_HOEHE / kvb[3], L.inneres(k))]
        tx = r + k_breite + B_K_LUFT
        st.append('<rect x="%.3f" y="%.3f" width="%.2f" height="%.2f" fill="%s"/>'
                  % (tx, mitte_y - B_TRENNER_HOCH / 2.0, B_TRENNER,
                     B_TRENNER_HOCH, f['wort']))
        bx = tx + B_TRENNER + B_TEXT_LUFT
        by = mitte_y - block_h / 2.0
        st.append('<g fill="%s" transform="translate(%.3f,%.3f)">%s</g>'
                  % (f['wort'], bx, by + B_WORT_VERSAL, b_wort_d))
        oy = by + B_WORT_VERSAL + B_ZEILENLUFT          # Oberkante KALTBRUNN
        strich_y = oy + B_ORT_VERSAL / 2.0 - B_STRICH_STARK / 2.0
        xo = bx + (B_BLOCK_BREIT - (B_STRICH * 2 + B_STRICH_LUFT * 2
                                    + B_ORT_WORT)) / 2.0
        st.append('<rect x="%.3f" y="%.3f" width="%.2f" height="%.2f" fill="%s"/>'
                  % (xo, strich_y, B_STRICH, B_STRICH_STARK, f['ort']))
        st.append('<g fill="%s" transform="translate(%.3f,%.3f)">%s</g>'
                  % (f['ort'], xo + B_STRICH + B_STRICH_LUFT,
                     oy + B_ORT_VERSAL, b_ort_d))
        st.append('<rect x="%.3f" y="%.3f" width="%.2f" height="%.2f" fill="%s"/>'
                  % (xo + B_STRICH + B_STRICH_LUFT * 2 + B_ORT_WORT, strich_y,
                     B_STRICH, B_STRICH_STARK, f['ort']))
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
