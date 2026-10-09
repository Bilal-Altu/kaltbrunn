#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Baut Nurettins Visitenkarte als echte Vektordatei.

Bilals Vorgabe, Wort fuer Wort:

    Frontseite: das Zeichen MIT Wagen, "Gutachten mit Sachverstand" in
                derselben Schriftgroesse wie KALTBRUNN.
    Rueckseite: Zeichen OHNE Wagen, Name, statt "Inhaber" die Zeile
                Maschinenbau-Ing. – Fahrzeugtechnik (B. Eng.), Kontakt wie
                auf der alten Karte, kein Festnetz, info@ing-kaltbrunn.de,
                ing-kaltbrunn.de, dazu ein QR-Code fuer WhatsApp.

ALS VEKTORDATEI heisst hier: keine Schrift im Dokument, sondern Kurven.
Jeder Buchstabe wird ueber bau_logo.text_zu_pfad in einen Pfad gewandelt,
genau wie in den Logodateien. Wer die SVG oeffnet, braucht Rubik nicht –
und die Druckerei bekommt nichts, was sie ersetzen koennte.

Gerechnet wird in Millimetern: die viewBox ist 91 x 61, ein Nutzer ist ein
Millimeter. 85 x 55 mm Endformat plus 3 mm Anschnitt ringsum. Alles, was
stehen bleiben muss, haelt 4 mm von der Schnittkante (3 mm verlangen
Druckereien, die vierte ist Reserve).

Die Regeln aus der Recherche zur ersten Karte gelten weiter:

  * Hoechstens drei Schriftgroessen – hier sind es zwei (11 pt / 8 pt).
  * Kontaktdaten nicht unter 8 pt.
  * Eine Ausrichtung durchhalten – alles liegt auf der linken Kante,
    nur der QR-Code steht rechts, weil er kein Text ist.
  * 25 bis 35 Prozent der Karte leer lassen.

Der QR-Code kommt aus segno, als Pfad, nicht als Bild. Fehlerkorrektur M,
vier Modul breiter Ruhebereich innerhalb des Feldes. Bei 19 mm Feldbreite
ist ein Modul 0,51 mm – ueber der Grenze, ab der Offsetdruck Module
zulaufen laesst.

DIE DATEI IST RGB. Chromium kann kein CMYK; die Druckerei wandelt nach
FOGRA51 (PSO Coated v3).

    python3 bau_karte_nuri.py
"""
import io
import os
import re
import subprocess

import segno

import bau_logo as L
import bau_visitenkarte as V

HIER = os.path.dirname(os.path.abspath(__file__))
AUS = os.path.join(HIER, 'logo')

PT = 25.4 / 72.0                  # ein Punkt in Millimetern

BREITE, HOEHE, ANSCHNITT = 85.0, 55.0, 3.0
BLATT_B, BLATT_H = BREITE + 2 * ANSCHNITT, HOEHE + 2 * ANSCHNITT
SICHER = 4.0
X0, Y0 = ANSCHNITT + SICHER, ANSCHNITT + SICHER
X1, Y1 = BLATT_B - ANSCHNITT - SICHER, BLATT_H - ANSCHNITT - SICHER

GROSS, KLEIN = 11 * PT, 8 * PT
ZEILE = 1.40 * KLEIN              # Zeilenabstand im Datenblock
GRUPPE = 1.4                      # Luft vor der Anschrift

SCHWARZ, BLAU, GRAU = '#15171a', '#003da5', '#5d6470'

NAME = 'Nurettin Sogukcesme'
ROLLE = 'Maschinenbau-Ing. – Fahrzeugtechnik (B. Eng.)'
TELEFON = '+49 176 37998836'
MAIL = 'info@ing-kaltbrunn.de'
WEB = 'ing-kaltbrunn.de'
STRASSE = 'Mannheimer Straße 1'
ORT = '64646 Heppenheim'
WHATSAPP = 'https://wa.me/4917637998836'

QR_DUNKEL = 15.0                  # Kantenlaenge der bedruckten Flaeche
QR_RAND = 4                       # Module Ruhebereich, Norm sind vier.
# Der Ruhebereich wird NICHT mitgerechnet, sondern liegt ausserhalb. Sonst
# steht der sichtbare Code zwei Millimeter weiter innen als alles andere
# und die rechte Kante der Karte hat zwei Fluchten statt einer. Weiss ist
# ringsum genug da: rechts und unten folgen Sicherheitsrand und Anschnitt.


# --- Bausteine ----------------------------------------------------------

def kopf(titel):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %.1f %.1f" '
            'width="%.0fmm" height="%.0fmm" role="img" aria-label="%s">'
            '<title>%s</title>'
            '<rect width="%.1f" height="%.1f" fill="#ffffff"/>'
            % (BLATT_B, BLATT_H, BLATT_B, BLATT_H, titel, titel,
               BLATT_B, BLATT_H))


def marke(name, hoehe_mm, x, y, am_bild=False):
    """Ein fertiges Zeichen aus marke/logo/ einsetzen.

    am_bild=True richtet nicht die Datei aus, sondern das, was man sieht:
    die Dateien tragen einen Rand, der sonst als schiefe Kante auffaellt.
    """
    svg = io.open(os.path.join(AUS, name + '.svg'), encoding='utf-8').read()
    vb = L.viewbox(svg)
    s = hoehe_mm / vb[3]
    if am_bild:
        rand = (L.RAND * 0.7 if name.startswith('karte-marke') else L.RAND) * s
        x, y = x - rand, y - rand
    return ('<g transform="translate(%.4f,%.4f) scale(%.6f)">%s</g>'
            % (x, y, s, L.inneres(svg)), vb[2] * s, vb[3] * s)


def zeile(f, text, groesse, farbe, x, grundlinie, rechts=None):
    d, b = L.text_zu_pfad(f, text, groesse)
    if rechts is not None:
        x = rechts - b
    return ('<g fill="%s" transform="translate(%.4f,%.4f)">%s</g>'
            % (farbe, x, grundlinie, d)), b


def qr_pfad(rechts, unten, dunkel):
    """QR-Code als ein einziger Pfad, ohne Bild und ohne Raster.

    rechts/unten sind die Kanten der BEDRUCKTEN Flaeche – daran richtet
    sich der Code aus, nicht an seinem Ruhebereich.
    """
    code = segno.make(WHATSAPP, error='m')
    matrix = [list(r) for r in code.matrix]
    m = dunkel / len(matrix)                       # Modulbreite in mm
    x, y = rechts - dunkel, unten - dunkel
    stuecke = []
    for zi, reihe in enumerate(matrix):
        for si, wert in enumerate(reihe):
            if wert:
                stuecke.append('M%.4f %.4fh%.4fv%.4fh-%.4fz'
                               % (x + si * m, y + zi * m, m, m, m))
    return ('<path fill="%s" shape-rendering="crispEdges" d="%s"/>'
            % (SCHWARZ, ''.join(stuecke))), code.version, m


# --- Die beiden Seiten --------------------------------------------------

def vorderseite():
    g, b, h = marke('karte-front-web-hell', 40.0,
                    (BLATT_B - 40.0 * 332 / 234) / 2.0, (BLATT_H - 40.0) / 2.0)
    return kopf('Ingenieurbüro Kaltbrunn – Visitenkarte Vorderseite') + g + '</svg>'


def rueckseite():
    _, pfad = L.schrift_aus_seite()
    acht = L.schnitt(pfad, 800)
    sechs = L.schnitt(pfad, 600)
    fuenf = L.schnitt(pfad, 500)
    vier = L.schnitt(pfad, 400)

    st = []
    g, mb, mh = marke('karte-marke-web-hell', 8.6, X0, Y0, am_bild=True)
    st.append(g)

    s, _ = zeile(acht, NAME, GROSS, SCHWARZ, X0, 21.8)
    st.append(s)
    s, rollen_breite = zeile(fuenf, ROLLE, KLEIN, BLAU, X0, 26.6)
    st.append(s)

    grund = 34.6
    daten = [(TELEFON, sechs, SCHWARZ), (MAIL, vier, GRAU), (WEB, vier, GRAU),
             (STRASSE, vier, GRAU), (ORT, vier, GRAU)]
    breiteste = 0.0
    for i, (text, f, farbe) in enumerate(daten):
        if i == 3:
            grund += GRUPPE
        s, b = zeile(f, text, KLEIN, farbe, X0, grund)
        st.append(s)
        breiteste = max(breiteste, b)
        grund += ZEILE
    unterste = grund - ZEILE

    # QR unten buendig mit der letzten Datenzeile, Beschriftung darueber.
    # Ohne Beschriftung weiss niemand, dass der Code zu WhatsApp fuehrt –
    # und einen Code, von dem man das nicht weiss, scannt niemand.
    s, _ = zeile(sechs, 'WhatsApp', KLEIN, BLAU, 0, 33.0, rechts=X1)
    st.append(s)
    q, version, modul = qr_pfad(X1, unterste, QR_DUNKEL)
    st.append(q)

    pruefung = dict(zeichen_unten=Y0 + (128 - 2 * L.RAND * 0.7) * 8.6 / 128,
                    rolle=rollen_breite, daten=breiteste,
                    unterste=unterste, ruhe=QR_RAND * modul,
                    version=version, modul=modul)
    return (kopf('Ingenieurbüro Kaltbrunn – Visitenkarte Rückseite')
            + ''.join(st) + '</svg>'), pruefung


# --- Ausgabe ------------------------------------------------------------

def drucken(vorn, hinten, ziel_name):
    css = ('@page{size:%.0fmm %.0fmm;margin:0}'
           '*{margin:0;padding:0}'
           'body{-webkit-print-color-adjust:exact;print-color-adjust:exact}'
           '.s{width:%.0fmm;height:%.0fmm;overflow:hidden;page-break-after:always}'
           '.s:last-child{page-break-after:auto}'
           '.s svg{display:block;width:%.0fmm;height:%.0fmm}'
           % (BLATT_B, BLATT_H, BLATT_B, BLATT_H, BLATT_B, BLATT_H))
    html = ('<!doctype html><html lang="de"><head><meta charset="utf-8">'
            '<title>Visitenkarte Ingenieurbüro Kaltbrunn</title>'
            '<style>%s</style></head><body>'
            '<div class="s">%s</div><div class="s">%s</div>'
            '</body></html>' % (css, vorn, hinten))
    return V.drucken(html, ziel_name, (BLATT_B, BLATT_H))


if __name__ == '__main__':
    vorn = vorderseite()
    hinten, p = rueckseite()
    os.makedirs(AUS, exist_ok=True)
    namen = ('Visitenkarte-Nuri-Vorderseite.svg', 'Visitenkarte-Nuri-Rueckseite.svg')
    for name, svg in zip(namen, (vorn, hinten)):
        io.open(os.path.join(AUS, name), 'w', encoding='utf-8').write(svg)
        print('  marke/logo/%-36s %6.1f KB' % (name, len(svg.encode('utf-8')) / 1024))
    ziel = drucken(vorn, hinten, 'Visitenkarte-Nuri-Druck.pdf')
    print('  marke/logo/%-36s %6.1f KB  (%.0f x %.0f mm, 2 Seiten)'
          % (os.path.basename(ziel), os.path.getsize(ziel) / 1024, BLATT_B, BLATT_H))
    print()
    print('  Zeichen endet bei      %.2f mm' % p['zeichen_unten'])
    print('  Rollenzeile breit      %.2f mm  (Platz: %.2f)' % (p['rolle'], X1 - X0))
    print('  Datenblock breit       %.2f mm  (Platz bis QR: %.2f)'
          % (p['daten'], X1 - QR_DUNKEL - X0 - p['ruhe']))
    print('  unterste Grundlinie    %.2f mm  (Sicherheit: %.2f)' % (p['unterste'], Y1))
    print('  QR %.0f mm, Version %s, Modul %.3f mm, Ruhebereich %.2f mm'
          % (QR_DUNKEL, p['version'], p['modul'], p['ruhe']))
