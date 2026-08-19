#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Marke: Limousine in Dreiviertelansicht, direkt gezeichnet.

Der Versuch, die Ansicht aus einem Seitenprofil zu projizieren, ist an der
Aussenkontur gescheitert: nahe und ferne Flanke ergaben entweder einen
Geisterumriss oder ein Knaeuel. Eine Dreiviertelansicht hat genau eine
Aussenkontur – die steht hier als Punktfolge im Bild, an Nurettins Vorlage
abgemessen, und wird als weicher Zug durchfahren.

Alle Koordinaten in Bildeinheiten, Wagen 210 x 100, Front rechts.
"""
import io
import math


def glatt(punkte, zu=True):
    """Weicher Zug durch die Punkte. (x, y) oder (x, y, True) fuer eine Ecke."""
    pk = [(q[0], q[1]) for q in punkte]
    scharf = [len(q) > 2 and q[2] for q in punkte]
    n = len(pk)

    def hole(i):
        j = i % n if zu else max(0, min(n - 1, i))
        return pk[j], scharf[j]

    teile = ['M%.2f %.2f' % pk[0]]
    for i in range(n if zu else n - 1):
        p0, _ = hole(i - 1)
        p1, s1 = hole(i)
        p2, s2 = hole(i + 1)
        p3, _ = hole(i + 2)
        c1 = ((p1[0] + (p2[0] - p1[0]) / 3.0, p1[1] + (p2[1] - p1[1]) / 3.0) if s1
              else (p1[0] + (p2[0] - p0[0]) / 6.0, p1[1] + (p2[1] - p0[1]) / 6.0))
        c2 = ((p2[0] - (p2[0] - p1[0]) / 3.0, p2[1] - (p2[1] - p1[1]) / 3.0) if s2
              else (p2[0] - (p3[0] - p1[0]) / 6.0, p2[1] - (p3[1] - p1[1]) / 6.0))
        teile.append('C%.2f %.2f %.2f %.2f %.2f %.2f' % (c1 + c2 + p2))
    return ' '.join(teile) + (' Z' if zu else '')


# ── Aussenkontur, im Uhrzeigersinn ab Heck unten ──────────────────────────
KONTUR = [
    (14, 74, True),                     # Heck unten
    (9, 60), (12, 46, True),            # Heckschuerze, Kante zum Kofferraum
    (38, 40),                           # Kofferraumdeckel
    (64, 18, True),                     # C-Saeule, hintere Dachkante
    (104, 11), (134, 14, True),         # Dach, vordere Dachkante
    (158, 34),                          # Windschutzscheibe
    (170, 41, True),                    # Windlauf
    (192, 42),                          # Haube
    (208, 35, True),                    # obere Ecke der Front, abgewandte Seite
    (214, 58), (210, 74, True),         # Frontflaeche, untere Ecke
    (200, 84),                          # Stossfaenger unten
    (150, 88), (70, 88), (30, 84),      # Unterkante
]

# Kante zwischen Flanke und Frontflaeche
FRONTKANTE = [(170, 41, True), (174, 60), (176, 86, True)]

# Fensterflaeche der zugewandten Seite
FENSTER = [
    (72, 30, True), (96, 22), (124, 24, True),
    (146, 44, True), (100, 47), (78, 44, True),
]
B_SAEULE = [(107, 23), (112, 46)]

# Guertellinie
GUERTEL = [(16, 50), (60, 47), (120, 47), (168, 46)]

RAD_V = (150, 72, 23)
RAD_H = (58, 68, 21)

# Front: Nieren, Scheinwerfer, Lufteinlass (in der Frontflaeche)
NIERE_A = [(182, 52, True), (194, 49, True), (194, 66, True), (182, 68, True)]
NIERE_B = [(197, 48, True), (208, 46, True), (208, 63, True), (197, 65, True)]
LICHT_A = [(172, 44, True), (180, 43), (181, 50), (173, 52, True)]
LICHT_B = [(199, 39, True), (209, 37, True), (210, 44), (200, 46, True)]
EINLASS = [(180, 74), (208, 71)]

STRAHLEN = [((228, 30), (248, 12)), ((220, 14), (230, -6)),
            ((234, 50), (256, 44)), ((207, 6), (210, -12))]


def zeichne():
    linie = 'var(--linie,#12356e)'
    lack = 'var(--lack,#ffffff)'
    glas = 'var(--glas,#c9dcf4)'
    strahl = 'var(--strahl,#12356e)'
    S = 'stroke="%s" stroke-linejoin="round" stroke-linecap="round"' % linie
    t = []

    t.append('<path d="%s" fill="%s" %s stroke-width="3.4"/>' % (glatt(KONTUR), lack, S))
    t.append('<path d="%s" fill="none" %s stroke-width="2.6"/>' % (glatt(FRONTKANTE, False), S))
    t.append('<path d="%s" fill="%s" %s stroke-width="2.6"/>' % (glatt(FENSTER), glas, S))
    t.append('<path d="M%d %d L%d %d" %s stroke-width="2.4"/>'
             % (B_SAEULE[0][0], B_SAEULE[0][1], B_SAEULE[1][0], B_SAEULE[1][1], S))
    t.append('<path d="%s" fill="none" %s stroke-width="2"/>' % (glatt(GUERTEL, False), S))

    for f, farbe, w in ((NIERE_A, linie, 1.8), (NIERE_B, linie, 1.8),
                        (LICHT_A, glas, 1.8), (LICHT_B, glas, 1.8)):
        t.append('<path d="%s" fill="%s" %s stroke-width="%s"/>' % (glatt(f), farbe, S, w))
    t.append('<path d="M%d %d L%d %d" %s stroke-width="2.2"/>'
             % (EINLASS[0][0], EINLASS[0][1], EINLASS[1][0], EINLASS[1][1], S))

    for (cx, cy, r) in (RAD_H, RAD_V):
        t.append('<circle cx="%d" cy="%d" r="%d" fill="%s" %s stroke-width="3"/>'
                 % (cx, cy, r, lack, S))
        t.append('<circle cx="%d" cy="%d" r="%.1f" fill="none" %s stroke-width="1.8"/>'
                 % (cx, cy, r * 0.78, S))
        sp = ''.join('<path d="M%.1f %.1f L%.1f %.1f"/>'
                     % (cx + r * 0.18 * math.cos(math.radians(w)), cy + r * 0.18 * math.sin(math.radians(w)),
                        cx + r * 0.74 * math.cos(math.radians(w)), cy + r * 0.74 * math.sin(math.radians(w)))
                     for w in range(12, 360, 36))
        t.append('<g stroke="%s" stroke-width="1.6" stroke-linecap="round">%s</g>' % (linie, sp))
        t.append('<circle cx="%d" cy="%d" r="%.1f" fill="%s"/>' % (cx, cy, r * 0.17, linie))

    t.append('<g stroke="%s" stroke-width="4.4" stroke-linecap="round">%s</g>'
             % (strahl, ''.join('<path d="M%d %d L%d %d"/>' % (a + b) for a, b in STRAHLEN)))
    return '\n  '.join(t)


SVG = '''<svg viewBox="0 -16 262 110" fill="none" xmlns="http://www.w3.org/2000/svg">
  %s
</svg>'''

if __name__ == '__main__':
    svg = SVG % zeichne()
    io.open('auto.svg', 'w', encoding='utf-8').write(svg)
    io.open('logo2.html', 'w', encoding='utf-8').write('''<!DOCTYPE html><html><head><meta charset="utf-8"><style>
body{background:#eef1f7;font-family:system-ui;margin:0;padding:24px}
.reihe{display:flex;align-items:flex-end;gap:30px;flex-wrap:wrap;background:#fff;padding:22px;border-radius:12px;margin-bottom:16px}
.reihe.dunkel{background:#002a73}
figure{margin:0;text-align:center}figcaption{font-size:11px;color:#8296b4;margin-top:6px}
svg{display:block}
</style></head><body>
<div class="reihe" id="a"></div><div class="reihe dunkel" id="b"></div>
<template id="t">''' + svg + '''</template>
<script>
for (const [id,l,la,gl,st] of [
 ['a','#12356e','#ffffff','#c9dcf4','#12356e'],
 ['b','#ffffff','#002a73','#5b8ad0','#ff8a1f']]) {
  const r=document.getElementById(id);
  for (const g of [470,270,140,86]) {
    const f=document.createElement('figure');
    const s=document.getElementById('t').content.cloneNode(true).firstElementChild;
    s.style.width=g+'px'; s.style.height=(g*110/262)+'px';
    s.style.setProperty('--linie',l); s.style.setProperty('--lack',la);
    s.style.setProperty('--glas',gl); s.style.setProperty('--strahl',st);
    f.appendChild(s);
    const c=document.createElement('figcaption'); c.textContent=g+'px'; f.appendChild(c);
    r.appendChild(f);
  }
}
</script></body></html>''')
    print('geschrieben')
