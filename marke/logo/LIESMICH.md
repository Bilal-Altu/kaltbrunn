# Das Zeichen als Datei

Gebaut von `marke/bau_logo.py`, nicht von Hand. **Nicht hier hineinschreiben** —
beim nächsten Lauf des Skripts wäre die Änderung weg.

## Zwei Farbwelten

`logo-…` ohne Zusatz gehört zu **unserer Seite** (Fußzeile auf Marineblau).

`logo-…-web-…` ist auf die Seite abgestimmt, für die sich Bilal entschieden
hat (`ak-learn-code.github.io/Ingenieurbuero-Kaltbrunn`).

**Ihre Sprache ist knapp:** fast schwarz (`#171d29`), weiß, und **ein**
gesättigtes Blau (`#003da5`). Ein helles Blau kommt bei ihnen nirgends vor.
Die Farben sind nicht nur aus dem CSS gelesen, sondern an den gerenderten
Pixeln nachgeprüft — auf ihren dunklen Flächen malen sie `#0038a0`, also
ihr `--color-brand`.

Daraus folgen zwei Regeln, die von unserer Seite abweichen:

- **Auf Dunkel ist das Zeichen einfarbig weiß.** Sie setzen Blau dort nur
  als Fläche (Knöpfe, Striche), nie als Text — Text ist immer weiß. Genau
  so erscheint das Logo auf ihrer Seite ohnehin, siehe unten.
- **Auf Hell ist INGENIEURBÜRO fast schwarz** (`#15171a`, ihr `--color-text`),
  nicht blau. Blau trägt nur KALTBRUNN und der Winkel des K — wie bei ihnen
  die Überschriften schwarz und die Akzente blau sind.

Wer das Zeichen auf Dunkel doch zweifarbig will, nimmt die Fassung
`…-web-dunkel-blau`. Der Winkel steht dort auf `#003da5`; das ist auf
`#171d29` schwach (Kontrast 1,78), als Fläche neben dem weißen Balken liest
es sich trotzdem.

## Die Dateien

| | mit Wagen | ohne Wagen | nur Reihe | nur K |
|---|---|---|---|---|
| unsere Seite, dunkel | `logo-dunkel` | `logo-ohne-wagen-dunkel` | `logo-zeile` | `logo-k` |
| unsere Seite, hell | `logo-hell` | `logo-ohne-wagen-hell` | `logo-zeile-hell` | `logo-k-hell` |
| ihre Seite, dunkel | `logo-web-dunkel` | `logo-ohne-wagen-web-dunkel` | `logo-zeile-web-dunkel` | `logo-k-web-dunkel` |
| ihre Seite, dunkel, blauer Winkel | `logo-web-dunkel-blau` | `logo-ohne-wagen-web-dunkel-blau` | `logo-zeile-web-dunkel-blau` | `logo-k-web-dunkel-blau` |
| ihre Seite, hell | `logo-web-hell` | `logo-ohne-wagen-web-hell` | `logo-zeile-web-hell` | `logo-k-web-hell` |

Dazu je Farbfassung eine waagerechte: `logo-quer-dunkel`, `logo-quer-hell`,
`logo-quer-web-dunkel`, `logo-quer-web-dunkel-blau`, `logo-quer-web-hell`.

### Die waagerechte Fassung

`logo-quer-…` ist die Marke aus der **Kopfzeile ihrer Seite**: K links,
daneben zweizeilig „Ingenieurbüro" über „Kaltbrunn", ohne Striche, ohne
Claim, in gemischter Schreibung statt Versalien.

An ihrer Kopfzeile abgemessen und mit 89/38 hochgerechnet, damit das K so
hoch ist wie in allen anderen Dateien:

| | bei ihnen | in der Datei |
|---|---|---|
| K | 41 × 38 px | 94,7 × 89 |
| Abstand zum Schriftzug | 12 px | 28,1 |
| „Ingenieurbüro" | 11 px, Gewicht 600, +0,035 em | 25,8 |
| „Kaltbrunn" | 18 px, Gewicht 700, −0,025 em | 42,2 |
| Zeilenabstand | 1,04 | 1,04 |

Der einzige Unterschied zu ihrer Kopfzeile ist die Schrift: ihre Seite hat
keine eingebettete Schrift und nimmt, was das Gerät hergibt. Die Datei
steht in **Rubik**, der Schrift, die als Hausschrift gewählt wurde.

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

## Zum Weitergeben

`Ingenieurbuero-Kaltbrunn-Zeichen.pdf` ist **eine** Datei, die man
verschicken kann: eine A4-Seite mit allen Fassungen, den Farbwerten und
den Hinweisen, wozu welche Fassung gehört. Gebaut von `bau_blatt.py`,
das die Zeichen aus diesem Ordner nimmt — was auf dem Blatt steht, ist
genau das, was in den Dateien steht.

Das PDF enthält **keine Bilder**, alles ist Vektor und die Schrift ist
eingebettet. Ein Werbetechniker kann die Zeichnung also direkt daraus
entnehmen, ohne dass man ihm die SVG einzeln schicken muss. Nachgeprüft:
eine Seite, `/Subtype /Image` kommt nicht vor, `/FontFile` schon.

## Wartung

**Wenn sich die Schrift der Seite ändert**, muss `python3 bau_logo.py` noch
einmal laufen: das Skript zieht die Schrift aus `index.html`, damit der
Schriftzug in der Datei gar nicht vom Schriftzug auf der Seite abweichen kann.

Größen und Abstände sind dieselben wie in der Fußzeile und stammen aus der
Messung an Nurettins Vorlage: der Wagen ist 1,082-mal so hoch wie das K, der
Spalt beträgt 6 px bei 89 px K-Höhe.
