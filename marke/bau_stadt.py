#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Stadtsilhouette hinter der Unfall-Sequenz.

Der Hintergrund war leeres Blau. Eine Stadt fuellt ihn, darf aber nichts
kosten: deshalb kein Bild, sondern zwei Silhouetten als je EIN Pfad, plus
ein dritter Pfad fuer alle Fenster zusammen. Ganzzahlige Koordinaten und
relative Befehle halten die Zeichenkette kurz – das Ganze bleibt unter
drei Kilobyte und faellt neben der eingebetteten Schrift nicht auf.

Zwei Ebenen ergeben Tiefe: hinten niedriger und blasser, vorn hoeher und
dunkler. Die Fenster sitzen nur in der vorderen Reihe, sonst wird es
unruhig.

Der Zufall ist festgenagelt (fester Startwert), damit jeder Lauf dieselbe
Stadt ergibt und der Waechter im Workflow greift.
"""
import io
import os
import random
import sys

BREITE = 1600
HOEHE = 220
BODEN = HOEHE


def reihe(zufall, tief, hoch, min_b, max_b, luecke):
    """Silhouette als ein Pfad: hoch, ueber das Dach, wieder runter."""
    teile = ['M0 %d' % BODEN]
    x = 0
    daecher = []
    while x < BREITE:
        b = zufall.randint(min_b, max_b)
        h = zufall.randint(tief, hoch)
        b = min(b, BREITE - x)
        teile.append('V%d' % (BODEN - h))
        teile.append('h%d' % b)
        teile.append('V%d' % BODEN)
        daecher.append((x, BODEN - h, b, h))
        x += b + zufall.randint(0, luecke)
        if x < BREITE:
            teile.append('H%d' % x)
    teile.append('H%d' % BREITE)
    teile.append('V%d' % BODEN)
    teile.append('Z')
    return ' '.join(teile), daecher


def aufbauten(zufall, daecher):
    """Ein paar Antennen und Aufzugshaeuschen – ohne die wirkt es wie Klotz."""
    t = []
    for (x, y, b, h) in daecher:
        if h < 90 or zufall.random() > 0.45:
            continue
        if zufall.random() < 0.5:
            # Mast: hoch, zwei breit, wieder runter. Hoehe EINMAL ziehen und
            # das Vorzeichen im Format setzen – ein negativer Wert in einem
            # 'v-%d' ergibt 'v--22', und daran verwirft der Browser den
            # ganzen Pfad ab dieser Stelle.
            mh = zufall.randint(14, 30)
            t.append('M%d %d v-%d h2 v%d Z' % (x + b // 2, y, mh, mh))
        else:
            kb = max(6, b // 4)
            kh = zufall.randint(6, 12)
            t.append('M%d %d h%d v-%d h-%d Z' % (x + b // 3, y, kb, kh, kb))
    return ' '.join(t)


def fenster(zufall, daecher):
    """Alle Fenster in einem Pfad. Sparsam gesetzt, sonst flimmert es."""
    t = []
    for (x, y, b, h) in daecher:
        spalten = max(1, (b - 8) // 13)
        zeilen = max(1, (h - 14) // 18)
        for sp in range(spalten):
            for ze in range(zeilen):
                if zufall.random() > 0.22:
                    continue
                fx = x + 6 + sp * 13
                fy = y + 10 + ze * 18
                if fy > BODEN - 8:
                    continue
                t.append('M%d %dh5v7h-5Z' % (fx, fy))
    return ''.join(t)


def bauen():
    z = random.Random(20260821)
    hinten, d_hinten = reihe(z, 40, 105, 26, 62, 16)
    z2 = random.Random(7311)
    vorn, d_vorn = reihe(z2, 70, 175, 34, 78, 22)
    return ('<svg class="stadt" viewBox="0 0 %d %d" preserveAspectRatio="xMidYMax slice" '
            'fill="none" aria-hidden="true" focusable="false" '
            'xmlns="http://www.w3.org/2000/svg">'
            '<path d="%s" fill="var(--stadt-hinten,#0a2c6e)"/>'
            '<path d="%s" fill="var(--stadt-vorn,#031843)"/>'
            '<path d="%s" fill="var(--stadt-vorn,#031843)"/>'
            '<path d="%s" fill="var(--stadt-licht,#ffb478)" opacity="0.5"/>'
            '</svg>') % (BREITE, HOEHE, hinten, vorn,
                         aufbauten(z2, d_vorn), fenster(z2, d_vorn))


if __name__ == '__main__':
    svg = bauen()
    io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'stadt.svg'),
            'w', encoding='utf-8').write(svg)
    sys.stderr.write('%d Bytes\n' % len(svg.encode('utf-8')))
    print(svg)
