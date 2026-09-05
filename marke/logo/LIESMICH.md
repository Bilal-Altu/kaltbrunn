# Das Zeichen als Datei

Gebaut von `marke/bau_logo.py`, nicht von Hand. **Nicht hier hineinschreiben** —
beim nächsten Lauf des Skripts wäre die Änderung weg.

## Zwei Farbwelten

`logo-…` ohne Zusatz gehört zu **unserer Seite** (Fußzeile auf Marineblau).

`logo-…-web-…` ist auf die Seite abgestimmt, für die sich Bilal entschieden
hat (`ak-learn-code.github.io/Ingenieurbuero-Kaltbrunn`). Deren Farben, aus
ihrem CSS gelesen: `--color-brand #003da5`, `--color-brand-deep #002a73`,
`--color-text #15171a`, `--color-text-muted #5d6470`, dunkle Flächen `#171d29`.

**Ein Ton stammt nicht aus ihrer Palette, und zwar mit Absicht:** der Winkel
des K ist auf Dunkel `#4d8bf5`. Ihre eigenen Markenblaus tragen auf `#171d29`
nicht — `#003da5` kommt dort auf Kontrast **1,78**, `#0050cc` auf **2,43**.
`#4d8bf5` ist derselbe Blauton, nur aufgehellt, und kommt auf **5,09**.

## Die Dateien

| | mit Wagen | ohne Wagen | nur Reihe | nur K |
|---|---|---|---|---|
| unsere Seite, dunkel | `logo-dunkel` | `logo-ohne-wagen-dunkel` | `logo-zeile` | `logo-k` |
| unsere Seite, hell | `logo-hell` | `logo-ohne-wagen-hell` | `logo-zeile-hell` | `logo-k-hell` |
| ihre Seite, dunkel | `logo-web-dunkel` | `logo-ohne-wagen-web-dunkel` | `logo-zeile-web-dunkel` | `logo-k-web-dunkel` |
| ihre Seite, hell | `logo-web-hell` | `logo-ohne-wagen-web-hell` | `logo-zeile-web-hell` | `logo-k-web-hell` |

**Das K ist in allen Fassungen gleich hoch** (89 Einheiten). Wer die Fassung
mit und ohne Wagen nebeneinander legt, sieht dasselbe Zeichen im selben
Maßstab.

## Zwei Dinge, die man wissen muss

**Der Schriftzug steht in Kurven**, nicht als Text. Wer eine Datei öffnet,
braucht die Schrift also nicht installiert zu haben. Nachgemessen gegen die
Fußzeile: INGENIEURBÜRO 253,5 px in der Datei gegen 253,4 px auf der Seite.

**In Kopf- und Fußzeile ihrer Seite ist die Farbe wirkungslos.** Dort steht

    .site-header__brand img { filter: brightness(0) invert(); }
    .site-footer__brand img { filter: brightness(0) invert(); }

Das walzt jede Farbe platt und malt das Zeichen rein weiß. Das Monogramm
sieht dort also einfarbig aus, egal welche Datei eingesetzt wird — es ist
nicht kaputt, aber der blaue Winkel ist weg. Wer ihn haben will, muss die
beiden `filter`-Zeilen streichen und `logo-k-web-dunkel.svg` einsetzen.

Für alles andere — Briefbogen, Angebote, Gutachten-Deckblatt,
E-Mail-Signatur, Fahrzeugbeschriftung, soziale Netze — greifen die Farben
ganz normal.

## Wartung

**Wenn sich die Schrift der Seite ändert**, muss `python3 bau_logo.py` noch
einmal laufen: das Skript zieht die Schrift aus `index.html`, damit der
Schriftzug in der Datei gar nicht vom Schriftzug auf der Seite abweichen kann.

Größen und Abstände sind dieselben wie in der Fußzeile und stammen aus der
Messung an Nurettins Vorlage: der Wagen ist 1,082-mal so hoch wie das K, der
Spalt beträgt 6 px bei 89 px K-Höhe.
