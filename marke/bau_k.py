#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Das K aus Nurettins Logo: Balken plus Winkel.

Reine Geometrie, deshalb exakt nachbaubar – anders als der Wagen daneben,
der gespurt wird (bau_wagen.py).

Die Masse sind nicht geschaetzt, sondern werden bei jedem Lauf aus
vorlage/logo_nurettin.webp abgelesen. Der erste Anlauf hatte sie geraten und
lag daneben: die Arme waren 80 % zu dick und das Zeichen 13 % zu breit.

Gemessen wird an drei Zeilen:

  oben    das obere Ende des oberen Arms – waagerecht abgeschnitten, liefert
          Aussen- und Innenkante und damit die waagerechte Armdicke
  Mitte   die Hoehe der Winkelspitze – liefert aeussere und innere Spitze
  Balken  eine Spalte im Balken – liefert Oberkante, Unterkante, Hoehe

Aus Aussenspitze, Armdicke und Gesamtbreite folgt der Rest; beide Kanten
eines Arms sind damit zwangslaeufig parallel. Von Hand im Pfad zu schieben
bricht genau diese Parallelitaet.
"""
import io
import os
import sys

from PIL import Image
import numpy as np

HIER = os.path.dirname(os.path.abspath(__file__))
VORLAGE = os.path.join(HIER, 'vorlage', 'logo_nurettin.webp')

RECHTS_VOM_K = 598   # ab hier steht der Wagen
UNTER_DEM_K = 690    # ab hier steht INGENIEURBUERO
IM_BALKEN = 170      # eine Spalte, die sicher im Balken liegt


def messen():
    a = np.asarray(Image.open(VORLAGE).convert('RGB')).astype(np.int16)
    tinte = (a.sum(2) < 3 * 225)[:UNTER_DEM_K, :RECHTS_VOM_K]

    senkrecht = np.nonzero(tinte[:, IM_BALKEN])[0]
    y_oben, y_unten = senkrecht.min(), senkrecht.max()
    hoehe = y_unten - y_oben + 1
    x_links = np.nonzero(tinte.any(0))[0].min()

    def gruppen(y):
        s = np.nonzero(tinte[y])[0]
        return [(g[0], g[-1]) for g in np.split(s, np.nonzero(np.diff(s) > 1)[0] + 1)]

    # Zwei Gruppen erwartet: Balken, dann der Arm.
    oben = gruppen(y_oben + 2)
    mitte = gruppen((y_oben + y_unten) // 2)
    if len(oben) != 2 or len(mitte) != 2:
        raise SystemExit('Vorlage anders aufgebaut als erwartet: %r / %r' % (oben, mitte))

    s = 100.0 / hoehe                      # alles auf Zeichenhoehe 100
    def n(x): return (x - x_links) * s

    return {
        'balken':   n(oben[0][1]) + s,     # rechte Kante des Balkens
        'spitze':   n(mitte[1][0]),        # aeussere Spitze des Winkels
        'innen':    n(mitte[1][1]),        # innere Spitze (nur zur Kontrolle)
        'arm_aus':  n(oben[1][0]),         # Aussenkante am oberen Ende
        'breite':   n(oben[1][1]) + s,     # Gesamtbreite = Innenkante oben
    }


def bauen(m):
    H = 100.0
    mitte = H / 2.0
    balken, spitze, breite = m['balken'], m['spitze'], m['breite']
    dicke = breite - m['arm_aus']          # waagerechte Armdicke

    # Aussenkante: von der Spitze zur oberen Ecke. Die Innenkante ist
    # dieselbe Gerade, um die Armdicke nach rechts geschoben – daraus ergibt
    # sich die innere Spitze, sie wird nicht gesetzt.
    aus_oben = breite - dicke
    innen = spitze + dicke

    winkel = ('M%.2f 0 L%.2f 0 L%.2f %.2f L%.2f %.2f L%.2f %.2f L%.2f %.2f Z'
              % (aus_oben, breite, innen, mitte, breite, H, aus_oben, H, spitze, mitte))
    stab = 'M0 0 L%.2f 0 L%.2f %.2f L0 %.2f Z' % (balken, balken, H, H)

    return innen, ('<svg class="marke-k" viewBox="0 0 %.1f %.0f" fill="none" '
                   'aria-hidden="true" focusable="false" '
                   'xmlns="http://www.w3.org/2000/svg">'
                   '<path d="%s" fill="var(--k-balken,#002a73)"/>'
                   '<path d="%s" fill="var(--k-winkel,#2563eb)"/>'
                   '</svg>') % (breite, H, stab, winkel)


if __name__ == '__main__':
    m = messen()
    innen, svg = bauen(m)
    abweichung = abs(innen - m['innen'])
    sys.stderr.write(
        'gemessen: Balken %.1f · Spitze %.1f · Armdicke %.1f · Breite %.1f\n'
        'innere Spitze gerechnet %.1f, in der Vorlage %.1f (%.1f daneben)\n'
        % (m['balken'], m['spitze'], m['breite'] - m['arm_aus'], m['breite'],
           innen, m['innen'], abweichung))
    if abweichung > 2.0:
        raise SystemExit('Die Arme der Vorlage sind nicht parallel – Bau abgebrochen.')
    io.open(os.path.join(HIER, 'k.svg'), 'w', encoding='utf-8').write(svg)
    print(svg)
