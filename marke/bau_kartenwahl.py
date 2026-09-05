#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Baut das Blatt, auf dem Nurettin zwischen den zwei Karten waehlt.

Eine A4-Seite, beide Varianten in Originalgroesse nebeneinander. Wer sie
auf einem Blatt sieht, entscheidet in Sekunden; wer zwei PDF nacheinander
aufmacht, vergleicht aus dem Gedaechtnis.

Die Karten werden nicht nachgebaut, sondern aus bau_visitenkarte.py
geholt – auf dem Blatt steht also genau das, was gedruckt wird.

    python3 bau_kartenwahl.py
"""
import io
import os
import re

import bau_visitenkarte as VK

HIER = os.path.dirname(os.path.abspath(__file__))
LOGO = os.path.join(HIER, 'logo')


def seiten(variante):
    """Holt Vorder- und Rueckseite als fertige Kaesten, ohne Anschnitt."""
    html = VK.karte(variante)
    return re.findall(r'<div class="karte (?:vorn|hinten)">.*?</div></div>', html, re.S)


def blatt():
    familie, daten = VK.schrift()
    # Der Satz der Karte kommt unveraendert mit; nur der Anschnitt faellt
    # weg, damit auf dem Blatt das Endformat steht und nicht das Druckmass.
    karten_css = re.search(r'<style>(.*?)</style>', VK.karte(1), re.S).group(1)
    karten_css = karten_css.replace('@page { size: 91mm 61mm; margin: 0; }', '')
    karten_css = karten_css.replace(
        '.karte { width: 91mm; height: 61mm;',
        '.karte { width: %.0fmm; height: %.0fmm;' % (VK.BREITE, VK.HOEHE))
    karten_css = karten_css.replace(
        '.satz { position: absolute; inset: %.1fmm;' % (VK.ANSCHNITT + VK.SICHER),
        '.satz { position: absolute; inset: %.1fmm;' % VK.SICHER)
    karten_css = karten_css.replace('page-break-after: always;', '')

    css = """
      @page { size: A4; margin: 18mm 16mm; }
      body { font-family: '%(fam)s', system-ui, sans-serif; color: %(text)s;
             font-size: 9.6pt; line-height: 1.5;
             -webkit-print-color-adjust: exact; print-color-adjust: exact; }
      h1 { font-size: 18pt; font-weight: 800; letter-spacing: -0.02em;
           color: %(tief)s; }
      .kopf { border-bottom: 2.4px solid %(tief)s; padding-bottom: 9px;
              margin-bottom: 8mm; }
      .kopf p { color: %(grau)s; font-size: 9pt; margin-top: 2mm; }
      h2 { font-size: 11pt; font-weight: 800; color: %(blau)s; margin-bottom: 3mm; }
      .paar { display: flex; gap: 6mm; margin-bottom: 9mm; }
      .karte { box-shadow: 0 0 0 0.6px %(linie)s; border-radius: 0; }
      .frage { margin-top: 4mm; padding-top: 4mm; border-top: 1.2px solid %(linie)s;
               color: %(grau)s; font-size: 9pt; }
      .frage b { color: %(tief)s; }
    """ % dict(fam=familie, text=VK.TEXT, tief=VK.TIEF, blau=VK.BLAU,
               grau=VK.GRAU, linie='#dce1e7')

    teile = []
    for v, titel, satz in (
            (1, 'Variante 1 — ohne Wagen',
             'Ruhiger. Das Zeichen allein, wie in der Kopfzeile der Webseite.'),
            (2, 'Variante 2 — mit Wagen',
             'Erzählt sofort, worum es geht. Der Wagen ist das, was man wiedererkennt.')):
        v_seiten = seiten(v)
        teile.append('<h2>%s</h2><p style="color:%s;margin-bottom:3mm">%s</p>'
                     '<div class="paar">%s%s</div>'
                     % (titel, VK.GRAU, satz, v_seiten[0], v_seiten[1]))

    return ('<!doctype html><html lang="de"><head><meta charset="utf-8">'
            '<title>Visitenkarte – zwei Varianten</title>'
            '<style>%s\n%s</style></head><body>'
            '<div class="kopf"><h1>Visitenkarte — bitte auswählen</h1>'
            '<p>Beide Karten in Originalgröße, 85 × 55 mm. Vorderseite links, '
            'Rückseite rechts. Die Vorderseite ist in beiden gleich — '
            'zu entscheiden ist nur die Rückseite.</p></div>'
            '%s'
            '<div class="frage"><b>Bitte einmal Bescheid geben:</b> Variante 1 '
            'oder Variante 2? Danach geht die Datei in den Druck.<br>'
            'Vorher noch zu klären: die Domain wechselt noch — auf der Karte '
            'steht bisher ing-nuri.de.</div>'
            '</body></html>' % (karten_css, css, ''.join(teile)))


if __name__ == '__main__':
    ziel = VK.drucken(blatt(), 'Visitenkarte-Auswahl.pdf', format_mm=(210, 297))
    print('%s  %.1f KB' % (os.path.basename(ziel), os.path.getsize(ziel) / 1024))
