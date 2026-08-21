#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Hintergrundbild fuer den Anriss, aus einer der Schadenaufnahmen.

Nurettin wollte "ein grosses Hintergrundbild Ihres Standorts oder eines
Fahrzeugdetails". Genommen ist die Reflexionspruefung auf dunklem Lack
(05): das Streifenmuster liest sich als technische Struktur und nicht als
Schadenfoto, und es ist dunkel genug, dass der Text darueber traegt.

Beschnitten wird auf die obere Haelfte. Darunter liegen der eingebrannte
Zeitstempel, das Herstelleremblem und eine im Lack gespiegelte Person –
alles drei hat auf einem Hintergrundbild nichts verloren.

Zwei Groessen, damit das Handy nicht die grosse Datei zieht.
"""
import io
import os

from PIL import Image, ImageFilter

HIER = os.path.dirname(os.path.abspath(__file__))
QUELLE = os.path.join(HIER, '05-bmw-lack-detail.webp')
UNTEN = 760          # darunter: Zeitstempel, Emblem, Spiegelung


def bauen():
    im = Image.open(QUELLE).convert('RGB')
    aus = im.crop((0, 0, im.width, UNTEN))
    ergebnis = []
    for name, breite, guete, weich in (('anriss-hintergrund.webp', 1600, 52, 1.4),
                                       ('anriss-hintergrund-klein.webp', 900, 50, 0.9)):
        h = round(aus.height * breite / aus.width)
        b = aus.resize((breite, h), Image.LANCZOS)
        # Das Streifenmuster ist hochfrequent und treibt die Datei hoch.
        # Unter dem blauen Schleier braucht es die Schaerfe nicht – ein
        # leichter Weichzeichner drittelt die Groesse.
        b = b.filter(ImageFilter.GaussianBlur(weich))
        pfad = os.path.join(HIER, name)
        b.save(pfad, 'WEBP', quality=guete, method=6)
        ergebnis.append((name, b.size, os.path.getsize(pfad)))
    return ergebnis


if __name__ == '__main__':
    for name, groesse, bytes_ in bauen():
        print('%-32s %4dx%-4d  %5.1f KB' % (name, groesse[0], groesse[1], bytes_ / 1024))
