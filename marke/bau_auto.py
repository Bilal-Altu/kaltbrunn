#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Erzeugt die Marke: Limousine in Dreiviertelansicht, Front rechts.

Von Hand gesetzte Koordinaten sind bei einer Dreiviertelansicht Gluecksache –
deshalb steht hier ein Seitenprofil in Fahrzeugkoordinaten, und die Ansicht
wird daraus projiziert. Dadurch fluchten Dach, Haube und Front automatisch.

    x  Laenge, 0 = Front, waechst nach hinten
    y  Breite, 0 = zugewandte Seite, waechst zur abgewandten
    z  Hoehe ueber der Fahrbahn
"""
import io
import math

# ── Projektion (axonometrisch) ────────────────────────────────────────────
AX, AY = -1.00, -0.045     # nach hinten: nach links, minimal nach oben
BX, BY =  0.55, -0.15      # zur abgewandten Seite: Blick knapp ueber Dachhoehe,
OX, OY = 268.0, 126.0      # nicht von der Leiter – deshalb nur wenig Anstieg
BREITE = 68

RAD_V = (48, 25, 24)       # Mitte x, Mitte z, Radius
RAD_H = (190, 25, 24)


def p(x, y, z):
    return (OX + x * AX + y * BX, OY + x * AY + y * BY - z)


def d(punkte, zu=True):
    t = 'M%.1f %.1f' % punkte[0] + ''.join(' L%.1f %.1f' % q for q in punkte[1:])
    return t + (' Z' if zu else '')


def bogen(mx, mz, r, von, bis, n=14):
    """Radlauf als Punktfolge in Fahrzeugkoordinaten (Winkel in Grad)."""
    return [(mx + r * math.cos(math.radians(w)), mz + r * math.sin(math.radians(w)))
            for w in (von + (bis - von) * i / n for i in range(n + 1))]


# ── Seitenprofil ──────────────────────────────────────────────────────────
OBEN = [
    (5, 19), (0, 41),                    # Frontschuerze, Haubenvorderkante
    (42, 46), (88, 50),                  # lange Haube bis zum Windlauf
    (116, 72), (140, 77),                # flach stehende A-Saeule, Dachkante
    (168, 77), (186, 68),                # Dach, C-Saeule
    (208, 53), (222, 49),                # Heckscheibe, Kofferraumdeckel
    (228, 36), (226, 19),                # Heckabschluss
]
# Unterkante mit Radlaeufen: von hinten nach vorn
UNTEN = ([(220, 9)]
         + bogen(RAD_H[0], RAD_H[1] - 2, RAD_H[2] + 3, 5, 175)[::-1]
         + [(78, 9)]
         + bogen(RAD_V[0], RAD_V[1] - 2, RAD_V[2] + 3, 5, 175)[::-1]
         + [(15, 11), (5, 19)])
PROFIL = OBEN + UNTEN
# Die abgewandte Seite steht hinter dem Wagen – ihre Radlaeufe sieht man nie.
# Mit Boegen woelbten sie sich als Buckel ueber das Dach.
PROFIL_FERN = OBEN + [(226, 9), (15, 9), (5, 19)]

FENSTER_V = [(96, 51), (120, 71), (142, 71), (142, 51)]
FENSTER_H = [(148, 51), (148, 71), (172, 71), (180, 60), (180, 51)]


def zeichne():
    linie = 'var(--linie,#0b2f66)'
    lack = 'var(--lack,#ffffff)'
    dach = 'var(--dach,#ffffff)'
    glas = 'var(--glas,#bcd4f0)'
    strahl = 'var(--strahl,#0b2f66)'
    t = []

    # 1) Abgewandte Flanke – schaut als Dach-, Hauben- und Deckelflaeche hervor
    t.append('<path d="%s" fill="%s" stroke="%s" stroke-width="3" '
             'stroke-linejoin="round"/>'
             % (d([p(x, BREITE, z) for x, z in PROFIL_FERN]), dach, linie))

    # 2) Frontflaeche: Querschnitt bei x ≈ 0, von der zugewandten zur abgewandten Seite
    front = [p(5, 0, 19), p(0, 0, 41), p(0, BREITE, 41), p(5, BREITE, 19), p(15, BREITE, 11), p(15, 0, 11)]
    t.append('<path d="%s" fill="%s" stroke="%s" stroke-width="3.2" '
             'stroke-linejoin="round"/>' % (d(front), lack, linie))

    # 3) Niere und Scheinwerfer auf der Frontflaeche
    for y0, y1 in ((11, 31), (37, 57)):      # zwei Nieren
        t.append('<path d="%s" fill="%s" opacity=".92"/>'
                 % (d([p(1, y0, 33), p(1, y1, 33), p(1, y1, 20), p(1, y0, 20)]), linie))
    for y0, y1 in ((5, 26), (44, 65)):        # Scheinwerfer
        t.append('<path d="%s" fill="%s" stroke="%s" stroke-width="2.2" '
                 'stroke-linejoin="round"/>'
                 % (d([p(2, y0, 40), p(2, y1, 40), p(2, y1, 33), p(2, y0, 33)]), glas, linie))

    # 4) Zugewandte Flanke
    t.append('<path d="%s" fill="%s" stroke="%s" stroke-width="3.4" '
             'stroke-linejoin="round"/>'
             % (d([p(x, 0, z) for x, z in PROFIL]), lack, linie))

    # 5) Fenster
    for f in (FENSTER_V, FENSTER_H):
        t.append('<path d="%s" fill="%s" stroke="%s" stroke-width="2.4" '
                 'stroke-linejoin="round"/>'
                 % (d([p(x, 0, z) for x, z in f]), glas, linie))

    # 6) Guertellinie
    t.append('<path d="%s" stroke="%s" stroke-width="2.2" stroke-linecap="round" fill="none"/>'
             % (d([p(22, 0, 38), p(90, 0, 46), p(182, 0, 46), p(218, 0, 40)], False), linie))

    # 7) Raeder mit Speichen
    for (mx, mz, r) in (RAD_V, RAD_H):
        cx, cy = p(mx, -3, mz)
        rx, ry = r * 0.96, r
        t.append('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="%s" '
                 'stroke="%s" stroke-width="3.2"/>' % (cx, cy, rx, ry, lack, linie))
        speichen = ''.join(
            '<path d="M%.1f %.1f L%.1f %.1f"/>'
            % (cx + rx * 0.24 * math.cos(math.radians(w)), cy + ry * 0.24 * math.sin(math.radians(w)),
               cx + rx * 0.74 * math.cos(math.radians(w)), cy + ry * 0.74 * math.sin(math.radians(w)))
            for w in range(18, 360, 72))
        t.append('<g stroke="%s" stroke-width="2.2" stroke-linecap="round">%s</g>' % (linie, speichen))
        t.append('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="%s"/>'
                 % (cx, cy, rx * 0.2, ry * 0.21, linie))

    # 8) Aufprallstrahlen, frei vor der Front
    strahlen = [((316, 48), (334, 32)), ((310, 32), (321, 12)),
                ((320, 66), (342, 62)), ((299, 24), (303, 6))]
    t.append('<g stroke="%s" stroke-width="4.2" stroke-linecap="round">%s</g>'
             % (strahl, ''.join('<path d="M%d %d L%d %d"/>' % (a[0], a[1], b[0], b[1])
                                for a, b in strahlen)))
    return '\n  '.join(t)


SVG = '''<svg viewBox="24 2 326 132" fill="none" xmlns="http://www.w3.org/2000/svg">
  %s
</svg>'''


if __name__ == '__main__':
    svg = SVG % zeichne()
    io.open('auto.svg', 'w', encoding='utf-8').write(svg)
    seite = '''<!DOCTYPE html><html><head><meta charset="utf-8"><style>
body{background:#eef1f7;font-family:system-ui;margin:0;padding:24px}
.reihe{display:flex;align-items:flex-end;gap:30px;flex-wrap:wrap;background:#fff;padding:22px;border-radius:12px;margin-bottom:16px}
.reihe.dunkel{background:#002a73}
figure{margin:0;text-align:center}figcaption{font-size:11px;color:#8296b4;margin-top:6px}
svg{display:block}
</style></head><body>
<div class="reihe" id="a"></div><div class="reihe dunkel" id="b"></div>
<template id="t">''' + svg + '''</template>
<script>
for (const [id,l,la,da,gl,st] of [
 ['a','#0b2f66','#ffffff','#ffffff','#bcd4f0','#0b2f66'],
 ['b','#ffffff','#0b2f66','#0b2f66','#4d78bb','#ff8a1f']]) {
  const r=document.getElementById(id);
  for (const g of [470,270,140,70]) {
    const f=document.createElement('figure');
    const s=document.getElementById('t').content.cloneNode(true).firstElementChild;
    s.style.width=g+'px'; s.style.height=(g*132/326)+'px';
    s.style.setProperty('--linie',l); s.style.setProperty('--lack',la);
    s.style.setProperty('--dach',da); s.style.setProperty('--glas',gl);
    s.style.setProperty('--strahl',st);
    f.appendChild(s);
    const c=document.createElement('figcaption'); c.textContent=g+'px'; f.appendChild(c);
    r.appendChild(f);
  }
}
</script></body></html>'''
    io.open('logo2.html', 'w', encoding='utf-8').write(seite)
    print('auto.svg und logo2.html geschrieben')
