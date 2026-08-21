#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Das K aus Nurettins Logo: Balken plus Winkel.

Reine Geometrie, deshalb exakt nachbaubar – anders als der gerenderte BMW
daneben. Die Arme des Winkels sind parallel und senkrecht abgeschnitten,
genau wie in der Vorlage; die innere Spitze ergibt sich daraus rechnerisch
und ist nicht geraten.
"""
import io

BREITE_BALKEN = 26.0     # Balken links
LUECKE = 6.0             # schmaler Spalt zwischen Balken und Winkelspitze
RECHTS = 120.0           # rechte Kante der Arme
HOEHE = 100.0
DICKE = 30.0             # Armdicke, senkrecht gemessen

spitze_x = BREITE_BALKEN + LUECKE
mitte = HOEHE / 2.0

# Die inneren Kanten sind die aeusseren, um DICKE senkrecht verschoben.
# Ihr Schnittpunkt ist die innere Spitze:
#   oben innen:  y = DICKE + (RECHTS - x) * mitte / (RECHTS - spitze_x)
#   unten innen: y = HOEHE - DICKE - (RECHTS - x) * mitte / (RECHTS - spitze_x)
steig = mitte / (RECHTS - spitze_x)
dx = (mitte - DICKE) / steig
innen_x = RECHTS - dx

WINKEL = ('M%.1f 0 L%.1f %.1f L%.1f %.1f L%.1f %.1f L%.1f %.1f L%.1f %.1f Z'
          % (RECHTS, spitze_x, mitte, RECHTS, HOEHE,
             RECHTS, HOEHE - DICKE, innen_x, mitte, RECHTS, DICKE))
BALKEN = 'M0 0 L%.1f 0 L%.1f %.1f L0 %.1f Z' % (BREITE_BALKEN, BREITE_BALKEN, HOEHE, HOEHE)

SVG = ('<svg class="marke-k" viewBox="0 0 %.0f %.0f" fill="none" aria-hidden="true" '
       'focusable="false" xmlns="http://www.w3.org/2000/svg">'
       '<path d="%s" fill="var(--k-balken,#002a73)"/>'
       '<path d="%s" fill="var(--k-winkel,#2563eb)"/>'
       '</svg>') % (RECHTS, HOEHE, BALKEN, WINKEL)

if __name__ == '__main__':
    io.open('k.svg', 'w', encoding='utf-8').write(SVG)
    print('innere Spitze bei x=%.1f (aus den parallelen Kanten gerechnet)' % innen_x)
    print(SVG)
