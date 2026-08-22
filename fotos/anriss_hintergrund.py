#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Hintergrundbild fuer den Anriss, aus einer der Schadenaufnahmen.

Nurettin wollte "ein grosses Hintergrundbild Ihres Standorts oder eines
Fahrzeugdetails". Genommen ist die Reflexionspruefung auf dunklem Lack
(05): das Streifenmuster liest sich als technische Struktur und nicht als
Schadenfoto, und es ist dunkel genug, dass der Text darueber traegt.

Beschnitten wird so, dass drei Dinge draussen bleiben: der eingebrannte
Zeitstempel (ab x 1113, y 1000), das Herstelleremblem (ab x 1547, y 867)
und eine im Lack gespiegelte Person (x 560..1227, y 840..1160).

ENTRAUSCHEN STATT WEICHZEICHNEN. Die erste Fassung hat das Bild mit einem
Gauss von 1,4 weichgezeichnet, um es klein zu bekommen – und genau das sah
dann billig aus: die Streifen wurden zu Matsch. Teuer an dem Foto ist
nicht die Struktur, sondern der Lackflitter und das Sensorrauschen; beide
sind hochfrequent, unkomprimierbar und unter dem blauen Schleier ohnehin
unsichtbar. Ein Medianfilter nimmt genau die weg und laesst die Kanten
stehen. Ohne jede Filterung waeren es 226 KB, mit Gauss 43 KB und matschig,
mit Median 51 KB und scharf.

ZWEI AUSSCHNITTE, NICHT ZWEI GROESSEN. Der Anriss ist am Handy hoch und
schmal, das Bild ein breiter Streifen: mit "cover" wurde das kleine Bild
dort 6,7-fach hochskaliert. Deshalb gibt es fuer das Handy einen eigenen,
fast quadratischen Ausschnitt, der oben im Anriss liegt und nach unten in
den Verlauf auslaeuft – der wird nur noch 1,5-fach hochskaliert.
"""
import os

from PIL import Image, ImageFilter

HIER = os.path.dirname(os.path.abspath(__file__))
QUELLE = os.path.join(HIER, '05-bmw-lack-detail.webp')

# (Datei, Ausschnitt, Median-Kette, WebP-Guete)
# Der Handy-Ausschnitt bekommt den kleineren Median: er wird weniger
# hochskaliert und darf deshalb mehr Feinzeichnung behalten.
BAUPLAN = (
    ('anriss-hintergrund.webp',       (0, 0, 1600, 760), (7, 3), 72),
    ('anriss-hintergrund-handy.webp', (300, 0, 1100, 780), (5, 3), 72),
)


def bauen():
    im = Image.open(QUELLE).convert('RGB')
    ergebnis = []
    for name, kasten, median, guete in BAUPLAN:
        b = im.crop(kasten)
        for gr in median:
            b = b.filter(ImageFilter.MedianFilter(gr))
        pfad = os.path.join(HIER, name)
        b.save(pfad, 'WEBP', quality=guete, method=6)
        ergebnis.append((name, b.size, os.path.getsize(pfad)))
    return ergebnis


if __name__ == '__main__':
    for name, groesse, bytes_ in bauen():
        print('%-32s %4dx%-4d  %5.1f KB' % (name, groesse[0], groesse[1], bytes_ / 1024))
