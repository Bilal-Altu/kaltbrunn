#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Wagenskizze in Seitenansicht fuer die Unfall-Sequenz.

Warum Seitenansicht: eine Dreiviertelansicht von Hand zu setzen ist in
diesem Projekt viermal gescheitert, weil jede Linie zur Fluchtung passen
muss. Die Seitenansicht ist orthogonal – da gibt es keine Perspektive, die
man verfehlen kann. Fuer zwei Wagen, die frontal aufeinander zufahren, ist
sie ausserdem die richtige Ansicht.

Die Masse sind keine Erfindung, sondern eine gaengige Limousine
(Laenge 4700, Hoehe 1450, Radstand 2850, Rad 650, Ueberhang vorn 900,
hinten 950 – alles in Millimetern), umgerechnet auf 240 Einheiten Laenge.
Deshalb sitzen Raeder, Ueberhaenge und Dachhoehe zueinander wie bei einem
echten Wagen und nicht wie bei einem Spielzeug.

Die Aufprallstrahlen gehoeren NICHT hierher. In der alten Marke steckten
sie im Wagen – dadurch fuhren beide Wagen schon vor dem Knall mit Strahlen
herum. Sie liegen jetzt allein in .knall.
"""
import io
import math
import os
import sys

# ── Umrechnung: 4700 mm Laenge auf 240 Einheiten ─────────────────────────
MM = 240.0 / 4700.0
BODEN = 88.0

RAD_R      = 650 * MM / 2          # 16.6
ACHSE_V_X  = 240 - 900 * MM        # 194.0
ACHSE_H_X  = ACHSE_V_X - 2850 * MM # 48.5
ACHSE_Y    = BODEN - RAD_R
DACH_Y     = BODEN - 1450 * MM     # 14.0
GUERTEL_Y  = BODEN - 1000 * MM     # 37.0
BOGEN_R    = RAD_R + 2.6           # Spalt zwischen Reifen und Radlauf


def glatt(punkte, zu=True):
    """Weicher Zug durch die Punkte. (x, y) oder (x, y, True) fuer eine Ecke."""
    pk = [(q[0], q[1]) for q in punkte]
    scharf = [len(q) > 2 and q[2] for q in punkte]
    n = len(pk)

    def hole(i):
        j = i % n if zu else max(0, min(n - 1, i))
        return pk[j], scharf[j]

    teile = ['M%.1f %.1f' % pk[0]]
    for i in range(n if zu else n - 1):
        p0, _ = hole(i - 1)
        p1, s1 = hole(i)
        p2, s2 = hole(i + 1)
        p3, _ = hole(i + 2)
        c1 = ((p1[0] + (p2[0] - p1[0]) / 3.0, p1[1] + (p2[1] - p1[1]) / 3.0) if s1
              else (p1[0] + (p2[0] - p0[0]) / 6.0, p1[1] + (p2[1] - p0[1]) / 6.0))
        c2 = ((p2[0] - (p2[0] - p1[0]) / 3.0, p2[1] - (p2[1] - p1[1]) / 3.0) if s2
              else (p2[0] - (p3[0] - p1[0]) / 6.0, p2[1] - (p3[1] - p1[1]) / 6.0))
        teile.append('C%.1f %.1f %.1f %.1f %.1f %.1f' % (c1 + c2 + p2))
    return ' '.join(teile) + (' Z' if zu else '')


def bogen(mx):
    """Radlauf ueber einer Achse: rein, Scheitel, raus."""
    return [(mx + BOGEN_R, 76.5, True),
            (mx, ACHSE_Y - BOGEN_R + 1.0),
            (mx - BOGEN_R, 76.5, True)]


# ── Aussenkontur, im Uhrzeigersinn ab Heck unten, Front rechts ───────────
KONTUR = (
    [(5, 72, True), (1, 60), (4, 45, True),      # Heckschuerze, Kofferraumkante
     (28, 40),                                    # Kofferraumdeckel
     (54, 36),                                    # Guertellinie hinten
     (76, 17, True),                              # C-Saeule, hintere Dachkante
     (104, 14), (146, 14, True),                  # Dach, A-Saeule oben
     (170, 32), (182, 38, True),                  # Windschutzscheibe, Windlauf
     (208, 40),                                   # Haube
     (231, 44, True), (238, 54), (239, 66),       # Nase, Frontflaeche
     (234, 76, True), (219, 77)]                  # Stossfaenger unten
    + bogen(ACHSE_V_X)
    + [(150, 77), (95, 77)]                       # Schweller
    + bogen(ACHSE_H_X)
    + [(15, 77)]
)

# Fensterflaeche, von der B-Saeule geteilt
FENSTER_H = [(79, 20, True), (104, 17), (110, 17, True),
             (110, 34, True), (66, 34, True)]
FENSTER_V = [(116, 17, True), (144, 17, True), (166, 33, True), (116, 34, True)]

# Fugen, Griffe, Leuchten
TUERFUGE_1 = [(66, 36), (68, 73)]
TUERFUGE_2 = [(112, 34), (114, 74)]
GRIFF_1 = [(88, 41), (100, 41)]
GRIFF_2 = [(130, 41), (142, 41)]
SCHWELLER = [(72, 71), (172, 71)]
LEUCHTE_H = [(3, 47, True), (15, 45, True), (15, 51, True), (3, 53, True)]
LEUCHTE_V = [(226, 47, True), (236, 50, True), (236, 56, True), (226, 54, True)]
LUFT = [(216, 68), (236, 70)]


def rad(mx):
    t = []
    t.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="var(--sk-reifen,#0a2260)" '
             'stroke="var(--sk-linie,#dbe7fb)" stroke-width="3"/>' % (mx, ACHSE_Y, RAD_R))
    t.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="none" '
             'stroke="var(--sk-linie,#dbe7fb)" stroke-width="1.8"/>' % (mx, ACHSE_Y, RAD_R * 0.62))
    speichen = ''.join(
        '<path d="M%.1f %.1f L%.1f %.1f"/>'
        % (mx + RAD_R * 0.14 * math.cos(math.radians(w)),
           ACHSE_Y + RAD_R * 0.14 * math.sin(math.radians(w)),
           mx + RAD_R * 0.58 * math.cos(math.radians(w)),
           ACHSE_Y + RAD_R * 0.58 * math.sin(math.radians(w)))
        for w in range(18, 360, 72))
    t.append('<g stroke="var(--sk-linie,#dbe7fb)" stroke-width="1.7" '
             'stroke-linecap="round">%s</g>' % speichen)
    t.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="var(--sk-linie,#dbe7fb)"/>'
             % (mx, ACHSE_Y, RAD_R * 0.16))
    return t


def zeichne():
    L = 'var(--sk-linie,#dbe7fb)'
    S = 'stroke="%s" stroke-linejoin="round" stroke-linecap="round"' % L
    t = []
    t.append('<path d="%s" fill="var(--sk-lack,#0d2f63)" %s stroke-width="3.2"/>'
             % (glatt(KONTUR), S))
    for f in (FENSTER_H, FENSTER_V):
        t.append('<path d="%s" fill="var(--sk-glas,#3f6fb5)" %s stroke-width="2.2"/>'
                 % (glatt(f), S))
    for paar in (TUERFUGE_1, TUERFUGE_2, GRIFF_1, GRIFF_2, SCHWELLER, LUFT):
        t.append('<path d="M%.1f %.1f L%.1f %.1f" %s stroke-width="1.8" opacity="0.75"/>'
                 % (paar[0][0], paar[0][1], paar[1][0], paar[1][1], S))
    for f in (LEUCHTE_H, LEUCHTE_V):
        t.append('<path d="%s" fill="var(--sk-licht,#8fb4e8)" %s stroke-width="1.6"/>'
                 % (glatt(f), S))
    for mx in (ACHSE_H_X, ACHSE_V_X):
        t.extend(rad(mx))
    return '\n  '.join(t)


SVG = ('<svg class="skizze" viewBox="0 0 242 92" fill="none" aria-hidden="true" '
       'focusable="false" xmlns="http://www.w3.org/2000/svg">\n  %s\n</svg>')

if __name__ == '__main__':
    svg = SVG % zeichne()
    io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'skizze.svg'),
            'w', encoding='utf-8').write(svg)
    sys.stderr.write('Achsen bei x=%.1f und %.1f, Rad r=%.1f, Dach y=%.1f\n'
                     % (ACHSE_H_X, ACHSE_V_X, RAD_R, DACH_Y))
    print(svg)
