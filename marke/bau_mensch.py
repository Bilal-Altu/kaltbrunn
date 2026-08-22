#!/usr/bin/env python3
"""Baut marke/mensch.svg – die Figur in der Unfall-Sequenz.

Vorher stand dort ein Strichmaennchen aus CSS-Kaesten. Es hatte Gelenke
und war beweglich, sah aber gezeichnet aus. Bilals Vorlage: eine einfache
Comic-Figur als Umrisszeichnung. Genau so ist sie hier gebaut – im selben
Strich wie die Wagen (gefuellte Flaeche, weisser Umriss), damit Figur und
Wagen aus derselben Zeichnung stammen.

Die Teile ueberdecken sich absichtlich: jede Flaeche ist gefuellt, also
verdeckt das Hemd die Oberarme und der Kopf den Hals. So entstehen aus
einfachen Formen saubere Aussenkonturen ohne Hilfslinien.

Zwei Armstellungen liegen als eigene Gruppen im Bild – Arm unten und Arm
mit Handy oben. Die Seite blendet zwischen ihnen um; ein gedrehtes Glied
haette einen zweiten Umriss gebraucht, der nie gepasst haette.
"""
import math, pathlib

BREIT, HOCH = 120, 256
LACK  = 'var(--mn-lack,#0d2f63)'
GLAS  = 'var(--mn-glas,#3f6fb5)'
LINIE = 'var(--mn-linie,#ffffff)'
HAAR  = 'var(--mn-haar,#ffffff)'

# Strichstaerken. Der Wagen traegt 3,2 bei 240 Einheiten Breite; die Figur
# ist mit 120 Einheiten halb so breit gerastert, also braucht sie fuer
# denselben Strich auf dem Schirm etwa die Haelfte davon mal dem
# Groessenverhaeltnis – nachgemessen passen 4,4 fuer den Umriss.
D_UMRISS, D_FEIN, D_HAUT = 4.4, 3.0, 2.6


def kapsel(x1, y1, w1, x2, y2, w2):
    """Umriss eines Glieds: zwei Seiten, zwei runde Enden."""
    dx, dy = x2 - x1, y2 - y1
    lang = math.hypot(dx, dy) or 1.0
    px, py = -dy / lang, dx / lang          # Senkrechte auf der Achse
    r1, r2 = w1 / 2.0, w2 / 2.0
    a = (x1 + px * r1, y1 + py * r1)
    b = (x2 + px * r2, y2 + py * r2)
    c = (x2 - px * r2, y2 - py * r2)
    d = (x1 - px * r1, y1 - py * r1)
    return (f"M{a[0]:.1f} {a[1]:.1f} L{b[0]:.1f} {b[1]:.1f} "
            f"A{r2:.1f} {r2:.1f} 0 0 1 {c[0]:.1f} {c[1]:.1f} "
            f"L{d[0]:.1f} {d[1]:.1f} "
            f"A{r1:.1f} {r1:.1f} 0 0 1 {a[0]:.1f} {a[1]:.1f} Z")


def pfad(d, fuell, strich=LINIE, dicke=D_UMRISS, extra=''):
    f = f'fill="{fuell}"' if fuell else 'fill="none"'
    return (f'<path d="{d}" {f} stroke="{strich}" stroke-width="{dicke}" '
            f'stroke-linejoin="round" stroke-linecap="round"{extra}/>')


teile = []

# ---- Beine und Schuhe (ganz hinten) --------------------------------------
hose = ("M42 136 L78 136 "
        "C77.5 160 77 190 74.5 238 L61.5 238 "
        "C62.5 200 62 182 60 166 "
        "C58 182 57.5 200 58.5 238 L45.5 238 "
        "C43 190 42.5 160 42 136 Z")
teile.append(pfad(hose, LACK))
# Naht in der Mitte – ohne sie sind es nicht zwei Beine, sondern ein Sack.
teile.append(pfad("M60 140 L60 163", None, LINIE, D_FEIN, ' opacity="0.8"'))

# Schuhe: die Spitze zeigt nach aussen, die Ferse bleibt unter dem Bein.
# Die erste Fassung ragte 15 Einheiten ueber das Bein hinaus – das waren
# Clownsschuhe. Vier Einheiten reichen.
for r, x_innen in ((1, 59.0), (-1, 61.0)):
    x_a = x_innen - r * 14          # Aussenkante des Beins
    schuh = (f"M{x_a:.1f} 234 L{x_innen:.1f} 234 L{x_innen:.1f} 247 "
             f"C{x_innen:.1f} 250 {x_innen - r*2:.1f} 251 {x_innen - r*5:.1f} 251 "
             f"L{x_a - r*3:.1f} 251 "
             f"C{x_a - r*5.5:.1f} 251 {x_a - r*6.5:.1f} 249 {x_a - r*5.5:.1f} 246.5 "
             f"C{x_a - r*4:.1f} 242 {x_a - r*1.5:.1f} 238 {x_a:.1f} 234 Z")
    teile.append(pfad(schuh, LACK))

# ---- Arme: gemeinsame Oberarme, dann die zwei Stellungen -----------------
def hand(cx, cy, rx=7.5, ry=9.5):
    return (f"M{cx:.1f} {cy-ry:.1f} C{cx+rx*0.7:.1f} {cy-ry:.1f} {cx+rx:.1f} {cy-ry*0.5:.1f} "
            f"{cx+rx:.1f} {cy:.1f} C{cx+rx:.1f} {cy+ry*0.7:.1f} {cx+rx*0.7:.1f} {cy+ry:.1f} "
            f"{cx:.1f} {cy+ry:.1f} C{cx-rx*0.7:.1f} {cy+ry:.1f} {cx-rx:.1f} {cy+ry*0.7:.1f} "
            f"{cx-rx:.1f} {cy:.1f} C{cx-rx:.1f} {cy-ry*0.5:.1f} {cx-rx*0.7:.1f} {cy-ry:.1f} "
            f"{cx:.1f} {cy-ry:.1f} Z")

arm_rechts = kapsel(88, 102, 15, 91, 164, 12)
hand_rechts = hand(91, 168)

# Der linke Arm liegt in zwei gezeichneten Stellungen vor, zwischen denen
# die Seite umblendet. Ein starres Glied zu drehen ginge nicht: den Arm
# gebeugt vors Gesicht bekommt man nur mit zwei Gelenken, und genau die
# Zweigelenk-Mechanik hat die Figur vorher wie Technik aussehen lassen.
# Zwei richtig gezeichnete Haltungen sind ehrlicher als eine falsche
# bewegliche.
arm_unten = kapsel(32, 102, 15, 29, 164, 12)
hand_unten = hand(29, 168)
# Das Handy in der haengenden Hand: es taucht dort auf ("zieht das Handy
# aus der Tasche"), bevor der Arm hochgeht.
handy_unten = ("M18.5 161 C18.5 158.5 20.5 156.5 23 156.5 L31 156.5 "
               "C33.5 156.5 35.5 158.5 35.5 161 L35.5 179 "
               "C35.5 181.5 33.5 183.5 31 183.5 L23 183.5 "
               "C20.5 183.5 18.5 181.5 18.5 179 Z")
handy_unten_schirm = "M21.5 160 L32.5 160 L32.5 176 L21.5 176 Z"

# Handy hoch: der Ellbogen bleibt im Aermel, der Unterarm klappt nach oben.
arm_hoch = kapsel(32, 108, 15, 25, 66, 12)
hand_hoch = hand(24, 61)
# Das Handy war 24x44 und damit fast so hoch wie der Kopf. Ein Handy ist
# gut halb so hoch wie ein Kopf; 21x40 laesst es noch erkennbar, ohne dass
# die Figur ein Tablett hochhaelt.
handy_hoch = ("M13 26 C13 23.5 15 21.5 17.5 21.5 L29.5 21.5 C32 21.5 34 23.5 34 26 "
              "L34 57 C34 59.5 32 61.5 29.5 61.5 L17.5 61.5 C15 61.5 13 59.5 13 57 Z")
handy_hoch_schirm = "M16.5 27 L30.5 27 L30.5 54 L16.5 54 Z"

teile.append(pfad(arm_rechts, LACK))
teile.append(pfad(hand_rechts, LACK, LINIE, D_HAUT))
teile.append(
    '<g class="mn-arm mn-arm-unten">'
    + pfad(arm_unten, LACK)
    + pfad(hand_unten, LACK, LINIE, D_HAUT)
    + '<g class="mn-handy-unten">'
    + pfad(handy_unten, LACK, LINIE, D_HAUT)
    + pfad(handy_unten_schirm, GLAS, LINIE, 1.8)
    + '</g></g>')
teile.append(
    '<g class="mn-arm mn-arm-hoch">'
    + pfad(arm_hoch, LACK)
    + pfad(hand_hoch, LACK, LINIE, D_HAUT)
    + pfad(handy_hoch, LACK, LINIE, D_HAUT, ' class="mn-handy"')
    + pfad(handy_hoch_schirm, GLAS, LINIE, 1.8)
    + '</g>')

# ---- Hals, dann Hemd darueber -------------------------------------------
teile.append(pfad("M52 52 L68 52 L68 78 L52 78 Z", LACK, LINIE, D_HAUT))

hemd = ("M37 75 C40 71 44 69 48 67 "          # linke Schulter
        "C50 67 51 68 52 69 "
        "C55 75 65 75 68 69 "                 # Kragen
        "C69 68 70 67 72 67 "
        "C76 69 80 71 83 75 "                 # rechte Schulter
        "C88 78 92 82 94 88 "
        "C95 95 95 100 95 106 "               # rechter Aermel
        "C90 108 84 109 79 109 "
        "C79 122 79 130 78 139 "              # rechte Seite
        "C66 141 54 141 42 139 "              # Saum
        "C41 130 41 122 41 109 "              # linke Seite
        "C36 109 30 108 25 106 "
        "C25 100 25 95 26 88 "                # linker Aermel
        "C28 82 32 78 37 75 Z")
teile.append(pfad(hemd, LACK))
# Aermelkante – sonst ist das T-Shirt ein Umhang.
teile.append(pfad("M41 106 C36 108 30 107 25 105", None, LINIE, D_FEIN, ' opacity="0.8"'))
teile.append(pfad("M79 106 C84 108 90 107 95 105", None, LINIE, D_FEIN, ' opacity="0.8"'))

# ---- Kopf, Haar, Gesicht ------------------------------------------------
teile.append(pfad("M60 4 C74 4 82 15 82 32 C82 49 74 60 60 60 "
                  "C46 60 38 49 38 32 C38 15 46 4 60 4 Z", LACK))
# Haare: Kappe ueber der Stirn mit einem Scheitel nach rechts.
teile.append(pfad("M39 30 C39 13 47 4 60 4 C73 4 81 13 81 30 "
                  "C79 25 76 21 72 19 C66 22 58 23 51 21 "
                  "C46 22 42 25 39 30 Z", HAAR, HAAR, 1.6))
for x in (52, 68):
    teile.append(f'<circle cx="{x}" cy="34" r="2.6" fill="{LINIE}"/>')
teile.append(pfad("M53 44 C56 48 64 48 67 44", None, LINIE, D_HAUT))

svg = (f'<svg class="mensch" viewBox="0 0 {BREIT} {HOCH}" fill="none" '
       f'xmlns="http://www.w3.org/2000/svg" aria-hidden="true">'
       + ''.join(teile) + '</svg>')

ziel = pathlib.Path(__file__).with_name('mensch.svg')
ziel.write_text(svg, encoding='utf-8')
print(f'{ziel.name} geschrieben, {len(svg)} Zeichen')
