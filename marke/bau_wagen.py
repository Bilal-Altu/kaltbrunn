#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Der Wagen aus Nurettins Logo – nachvektorisiert, nicht nachgezeichnet.

Vier Anlaeufe, ihn von Hand zu zeichnen, sind gescheitert; die Vorlage ist
eine gerenderte Strichzeichnung und keine Konstruktion. Sie liegt jetzt als
Datei vor (vorlage/logo_nurettin.webp), damit laesst sie sich spuren.

Drei Ebenen, von unten nach oben:

  lack    die gefuellte Silhouette. Sie entsteht nicht aus einer eigenen
          Maske, sondern indem vom Bildrand her geflutet wird: was die Flut
          nicht erreicht, ist Wagen. Ohne diese Ebene waere die Karosserie
          durchsichtig und der Wagen stuende auf dunklem Grund als
          Negativbild da.
  mittel  die hellen Schattierungen (Scheiben, Falten, Radhaeuser)
  linie   die Konturen und die dunklen Flaechen (Niere, Reifen, Schatten)

Die Aufloesung der Bitmap bestimmt die Zahl der Stuetzpunkte und damit die
Dateigroesse. 430 px ist gemessen der Punkt, ab dem mehr Aufloesung in den
Groessen, in denen der Wagen auf der Seite steht, nichts mehr sichtbar
hinzufuegt.
"""
import io
import os
import re
import subprocess
import sys
import tempfile

from PIL import Image, ImageDraw, ImageOps
import numpy as np

HIER = os.path.dirname(os.path.abspath(__file__))
VORLAGE = os.path.join(HIER, 'vorlage', 'logo_nurettin.webp')

BREITE = 430          # Zielbreite der Bitmap, siehe Kopf
SCHWELLE_LINIE = 96   # Helligkeit, unter der es Kontur ist
SCHWELLE_MITTEL = 200 # Helligkeit, unter der es ueberhaupt Tinte ist
TURD = 2              # potrace: Flecken unter so vielen Punkten verwerfen
ALPHA = 1.1           # potrace: Eckenschwelle
OPT = 0.6             # potrace: Kurventoleranz


def wagen_ausschneiden(bild):
    """Den Wagen aus dem Gesamtlogo holen: rechts vom K, ueber der Schrift."""
    a = np.asarray(bild.convert('RGB')).astype(np.int16)
    tinte = a.sum(2) < 3 * 225
    m = tinte.copy()
    m[:, :600] = False   # links davon steht das K
    m[690:, :] = False   # darunter steht INGENIEURBUERO
    ys, xs = np.nonzero(m)
    return bild.crop((xs.min() - 10, ys.min() - 10, xs.max() + 11, ys.max() + 11))


def silhouette(tinte):
    """Gefuellte Aussenform: vom Rand her fluten, der Rest ist Wagen.

    Ein Loch-Fueller ueber die Tinte allein taete es nicht – die Karosserie
    ist im Original weiss und damit gar keine Tinte.
    """
    bild = Image.fromarray(np.where(tinte, 0, 255).astype(np.uint8), 'L')
    randlos = ImageOps.expand(bild, 1, fill=255)
    ImageDraw.floodfill(randlos, (0, 0), 128)
    aussen = np.asarray(randlos)[1:-1, 1:-1] == 128
    return ~aussen


def spur(maske, arbeitsordner, name):
    pbm = os.path.join(arbeitsordner, name + '.pbm')
    Image.fromarray(np.where(maske, 0, 255).astype(np.uint8), 'L').convert('1').save(pbm)
    svg = os.path.join(arbeitsordner, name + '.svg')
    subprocess.check_call(['potrace', '-s', '-t', str(TURD), '-a', str(ALPHA),
                           '-O', str(OPT), '-o', svg, pbm])
    roh = io.open(svg, encoding='utf-8').read()
    return ' '.join(re.findall(r'<path d="([^"]+)"', roh))


def bauen():
    bild = wagen_ausschneiden(Image.open(VORLAGE))
    hoehe = round(bild.height * BREITE / bild.width)
    bild = bild.resize((BREITE, hoehe), Image.LANCZOS)

    a = np.asarray(bild.convert('RGB')).astype(np.float64)
    L = 0.2126 * a[:, :, 0] + 0.7152 * a[:, :, 1] + 0.0722 * a[:, :, 2]
    tinte = L < SCHWELLE_MITTEL
    form = silhouette(tinte)

    # Der Wagen fuellt den eng beschnittenen Ausschnitt zu rund drei Vierteln.
    # Laeuft die Flut durch ein Loch in der Kontur aus, geht der Wert gegen
    # null oder gegen eins – nur das soll hier auffallen.
    anteil = form.mean()
    if not 0.40 < anteil < 0.92:
        raise SystemExit('Silhouette deckt %.0f %% ab – die Flut ist vermutlich '
                         'durch ein Loch in der Aussenkontur ausgelaufen.' % (100 * anteil))

    with tempfile.TemporaryDirectory() as ordner:
        pfade = {
            'lack':   spur(form, ordner, 'lack'),
            'mittel': spur(tinte, ordner, 'mittel'),
            'linie':  spur(L < SCHWELLE_LINIE, ordner, 'linie'),
        }

    # potrace gibt die Pfade im zehnfachen Raum aus und holt sie im transform
    # wieder herunter – der viewBox ist deshalb die Bitmapgroesse.
    return ('<svg class="marke-wagen" viewBox="0 0 %d %d" fill="none" aria-hidden="true" '
            'focusable="false" xmlns="http://www.w3.org/2000/svg">'
            '<g transform="translate(0,%d) scale(0.1,-0.1)" stroke="none">'
            '<path d="%s" fill="var(--w-lack,#ffffff)"/>'
            '<path d="%s" fill="var(--w-mittel,#bcd3f0)"/>'
            '<path d="%s" fill="var(--w-linie,#12356e)"/>'
            '</g></svg>') % (BREITE, hoehe, hoehe,
                             pfade['lack'], pfade['mittel'], pfade['linie'])


if __name__ == '__main__':
    svg = bauen()
    io.open(os.path.join(HIER, 'wagen.svg'), 'w', encoding='utf-8').write(svg)
    sys.stderr.write('%d Bytes bei %d px Bitmapbreite\n' % (len(svg.encode('utf-8')), BREITE))
    print(svg)
