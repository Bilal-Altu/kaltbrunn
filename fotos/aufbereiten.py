#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Macht aus den Originalaufnahmen die Bilder für die Referenzseite.

Legt die Originale (JPEG aus der Kamera) in fotos/original/ ab, benennt sie
01.jpg, 02.jpg … in der Reihenfolge, in der sie auf der Seite stehen sollen,
und ruft dann auf:

    python3 fotos/aufbereiten.py

Ergebnis: die in bau_referenzen.py eingetragenen .webp-Dateien, auf 1600 px
Kantenlänge gebracht und so weit komprimiert, dass eine Aufnahme rund
120–200 KB wiegt. Danach einmal

    python3 bau_referenzen.py

damit referenzen.html die neuen Bilder bekommt.

VOR DEM VERÖFFENTLICHEN PRÜFEN
------------------------------
Diese Bilder gehen an die Öffentlichkeit, nicht in eine Akte:

* Kennzeichen unkenntlich? (Auf mehreren Aufnahmen sind sie schon geschwärzt.)
* Menschen im Bild oder in einer Scheibe gespiegelt? Auf der Aufnahme des
  BMW X1 spiegelt sich Nurettin selbst – das ist in Ordnung. Bei fremden
  Personen wäre es das nicht.
* Aufkleber, Beschriftungen, Firmennamen am Fahrzeug? Auf dem Toyota steht
  "…eförderer." – daraus lässt sich der Halter erschließen.
* Einwilligung der Auftraggeber: Fahrzeugaufnahmen aus einem Gutachten sind
  Auftragsdaten. Für die Veröffentlichung braucht es das Einverständnis –
  am besten schriftlich, und am besten schon im Auftragsformular.
"""
import os
import sys

try:
    from PIL import Image, ImageOps
except ImportError:
    sys.exit('Pillow fehlt:  pip install pillow')

HIER = os.path.dirname(os.path.abspath(__file__))
ORIGINALE = os.path.join(HIER, 'original')

# Reihenfolge wie in bau_referenzen.py
ZIELE = [
    '01-bmw-x1-streifschaden.webp',
    '02-toyota-corolla-heck-links.webp',
    '03-toyota-corolla-heck-detail.webp',
    '04-mercedes-e-front-links.webp',
    '05-bmw-lack-detail.webp',
    '06-audi-a5-front.webp',
    '07-audi-a6-heck-rechts.webp',
]

KANTE = 1600
GUETE = 78


def main():
    if not os.path.isdir(ORIGINALE):
        sys.exit('Bitte die Originale nach %s legen (01.jpg, 02.jpg …).' % ORIGINALE)

    dateien = sorted(f for f in os.listdir(ORIGINALE)
                     if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.heic')))
    if not dateien:
        sys.exit('In %s liegt kein Bild.' % ORIGINALE)
    if len(dateien) != len(ZIELE):
        print('Achtung: %d Originale, aber %d Plätze auf der Seite.'
              % (len(dateien), len(ZIELE)))

    for quelle, ziel in zip(dateien, ZIELE):
        b = Image.open(os.path.join(ORIGINALE, quelle))
        b = ImageOps.exif_transpose(b)          # Hochformat richtig herum
        b = b.convert('RGB')
        b.thumbnail((KANTE, KANTE), Image.LANCZOS)
        pfad = os.path.join(HIER, ziel)
        b.save(pfad, 'WEBP', quality=GUETE, method=6)
        print('%-38s → %-40s %4d KB  %dx%d'
              % (quelle, ziel, os.path.getsize(pfad) // 1024, b.width, b.height))

    print('\nJetzt noch:  python3 bau_referenzen.py')


if __name__ == '__main__':
    main()
