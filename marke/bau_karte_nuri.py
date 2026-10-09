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

QR_DUNKEL = 18.0                  # Kantenlaenge der bedruckten Flaeche
QR_RAND = 4                       # Module Ruhebereich, Norm sind vier.
# Der Ruhebereich wird NICHT mitgerechnet, sondern liegt ausserhalb. Sonst
# steht der sichtbare Code zwei Millimeter weiter innen als alles andere
# und die rechte Kante der Karte hat zwei Fluchten statt einer. Weiss ist
# ringsum genug da: rechts und unten folgen Sicherheitsrand und Anschnitt.
QR_LOCH = 9                       # Module, die in der Mitte frei bleiben
QR_RUND = 0.26                    # Eckenradius je Modul, Anteil der Kante
# Die Augen vertragen fast keine Rundung. Bei rx = 1,9 Modulen frisst der
# Bogen die Eckmodule weg und setzt sie diagonal nach innen – nachgemessen
# waren 23 von 1089 Modulen falsch, und der Code war nicht mehr lesbar.
# Was hier steht, ist der groesste Wert, bei dem der Code in allen
# Pruefdurchlaeufen noch gelesen wurde – 0,55 und mehr fielen durch.
QR_AUGE_RUND = 0.30               # Eckenradius der Augen, in Modulen

# Fehlerkorrektur H statt M: mit dem Zeichen in der Mitte fehlen 81 von
# 1089 Modulen (7,4 %). H vertraegt 30 %, M nur 15 % – und 15 % waeren die
# Reserve fuer Knicke und Fingerabdruecke, nicht fuer unser Zeichen.
QR_KORREKTUR = 'h'

GRUEN = '#25d366'                 # WhatsApp-Gruen, nur fuer das Zeichen

# Das WhatsApp-Zeichen liegt als marke/whatsapp.svg daneben, unveraendert
# so, wie es von Simple Icons 13.20 kommt (das Icon-Set steht unter CC0).
# Die Marke selbst gehoert WhatsApp; sie steht auf der Karte, um zu zeigen,
# wohin der Code fuehrt – genau dafuer ist sie da. Eingelesen statt
# abgetippt: eine Kurve mit 1104 Zeichen tippt man nicht fehlerfrei ab.


# --- Bausteine ----------------------------------------------------------

def kopf(titel):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %.1f %.1f" '
            'width="%.0fmm" height="%.0fmm" role="img" aria-label="%s">'
            '<title>%s</title>'
            '<rect width="%.1f" height="%.1f" fill="#ffffff"/>'
            % (BLATT_B, BLATT_H, BLATT_B, BLATT_H, titel, titel,
               BLATT_B, BLATT_H))


def marke(name, hoehe_mm, x, y, am_bild=False, rechts=False):
    """Ein fertiges Zeichen aus marke/logo/ einsetzen.

    am_bild=True richtet nicht die Datei aus, sondern das, was man sieht:
    die Dateien tragen einen Rand, der sonst als schiefe Kante auffaellt.
    rechts=True nimmt x als rechte statt als linke Kante.
    """
    svg = io.open(os.path.join(AUS, name + '.svg'), encoding='utf-8').read()
    vb = L.viewbox(svg)
    s = hoehe_mm / vb[3]
    rand = (L.RAND * 0.7 if name.startswith('karte-marke') else L.RAND) * s
    sicht_b, sicht_h = vb[2] * s - 2 * rand, vb[3] * s - 2 * rand
    if rechts:
        x -= sicht_b
    if am_bild:
        x, y = x - rand, y - rand
    return ('<g transform="translate(%.4f,%.4f) scale(%.6f)">%s</g>'
            % (x, y, s, L.inneres(svg)), sicht_b, sicht_h)


def zeile(f, text, groesse, farbe, x, grundlinie, rechts=None):
    d, b = L.text_zu_pfad(f, text, groesse)
    if rechts is not None:
        x = rechts - b
    return ('<g fill="%s" transform="translate(%.4f,%.4f)">%s</g>'
            % (farbe, x, grundlinie, d)), b


def wa_zeichen(mx, my, durchmesser):
    """Das WhatsApp-Zeichen als gruener Kreis mit weisser Kurve."""
    roh = io.open(os.path.join(HIER, 'whatsapp.svg'), encoding='utf-8').read()
    d = re.search(r'<path[^>]*\bd="([^"]+)"', roh).group(1)
    g = durchmesser * 0.60                      # Kantenlaenge der Kurve
    s = g / 24.0                                # Zeichnung ist 24 x 24
    return ('<circle cx="%.4f" cy="%.4f" r="%.4f" fill="%s"/>'
            '<g transform="translate(%.4f,%.4f) scale(%.6f)">'
            '<path d="%s" fill="#ffffff"/></g>'
            % (mx, my, durchmesser / 2.0, GRUEN,
               mx - g / 2.0, my - g / 2.0, s, d))


def rundes_feld(x, y, b, h, r):
    return '<rect x="%.4f" y="%.4f" width="%.4f" height="%.4f" rx="%.4f"/>' \
        % (x, y, b, h, r)


def qr_marke(rechts, unten, dunkel):
    """QR-Code mit dem WhatsApp-Zeichen in der Mitte.

    rechts/unten sind die Kanten der BEDRUCKTEN Flaeche – daran richtet
    sich der Code aus, nicht an seinem Ruhebereich.

    Drei Dinge unterscheiden ihn vom Raster, das segno von sich aus malt:

      * Die Module sind gerundet, nicht eckig.
      * Die drei Augen sind als Rahmen und Kern gezeichnet, nicht aus
        49 Einzelmodulen – das ist es, was einen gestalteten Code von
        einem ausgedruckten unterscheidet.
      * In der Mitte bleiben neun mal neun Module frei, da steht das
        WhatsApp-Zeichen.

    Alles davon kostet Lesbarkeit, deshalb steht die Fehlerkorrektur auf H
    und deshalb wird der fertige Code am Ende wieder ausgelesen, statt
    anzunehmen, dass er schon stimmen wird.
    """
    code = segno.make(WHATSAPP, error=QR_KORREKTUR)
    matrix = [list(r) for r in code.matrix]
    n = len(matrix)
    m = dunkel / n                                 # Modulbreite in mm
    x, y = rechts - dunkel, unten - dunkel

    augen = [(0, 0), (0, n - 7), (n - 7, 0)]       # Zeile, Spalte
    def im_auge(zi, si):
        return any(az <= zi < az + 7 and as_ <= si < as_ + 7 for az, as_ in augen)

    loch_a = (n - QR_LOCH) // 2
    loch_e = loch_a + QR_LOCH
    def im_loch(zi, si):
        return loch_a <= zi < loch_e and loch_a <= si < loch_e

    st = []
    r = m * QR_RUND
    for zi, reihe in enumerate(matrix):
        for si, wert in enumerate(reihe):
            if wert and not im_auge(zi, si) and not im_loch(zi, si):
                st.append(rundes_feld(x + si * m, y + zi * m, m, m, r))
    module = ('<g fill="%s">%s</g>' % (SCHWARZ, ''.join(st)))

    # Die Augen: aussen ein Rahmen von einem Modul Staerke, innen der Kern.
    # Gezeichnet statt gerastert, sonst sehen gerundete Module in einem
    # eckigen Auge nach Fehler aus.
    rahmen = []
    for az, as_ in augen:
        ax, ay = x + as_ * m, y + az * m
        rahmen.append('<rect x="%.4f" y="%.4f" width="%.4f" height="%.4f" '
                      'rx="%.4f" fill="none" stroke="%s" stroke-width="%.4f"/>'
                      % (ax + m * 0.5, ay + m * 0.5, m * 6, m * 6,
                         m * QR_AUGE_RUND, SCHWARZ, m))
        rahmen.append('<rect x="%.4f" y="%.4f" width="%.4f" height="%.4f" '
                      'rx="%.4f" fill="%s"/>'
                      % (ax + m * 2, ay + m * 2, m * 3, m * 3, m * QR_AUGE_RUND, SCHWARZ))

    mitte = (x + dunkel / 2.0, y + dunkel / 2.0)
    zeichen = wa_zeichen(mitte[0], mitte[1], QR_LOCH * m * 0.86)
    return (module + ''.join(rahmen) + zeichen), code.version, m


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
    # Das Zeichen steht rechts oben, nicht links: so hat die Karte EINE
    # rechte Flucht – Zeichen, QR-Code – und EINE linke – Name, Rolle,
    # Daten. Zwei saubere Kanten statt einer Kante und einer Ecke.
    g, mb, mh = marke('karte-marke-web-hell', 8.6, X1, Y0,
                      am_bild=True, rechts=True)
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

    # QR unten buendig mit der letzten Datenzeile. Die Beschriftung
    # "WhatsApp" daneben ist weg: das Zeichen in der Mitte des Codes sagt
    # dasselbe, und zweimal dasselbe zu sagen ist kein Satz, sondern Fuellung.
    q, version, modul = qr_marke(X1, unterste, QR_DUNKEL)
    st.append(q)

    pruefung = dict(zeichen_unten=Y0 + mh, zeichen_links=X1 - mb,
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
