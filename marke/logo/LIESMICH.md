# Das Zeichen als Datei

Gebaut von `marke/bau_logo.py`, nicht von Hand. **Nicht hier hineinschreiben** —
beim nächsten Lauf des Skripts wäre die Änderung weg.

| Datei | wofür |
|---|---|
| `logo-dunkel.svg` | ganzes Zeichen für dunklen Grund (wie in der Fußzeile) |
| `logo-hell.svg` | ganzes Zeichen für hellen Grund |
| `logo-ohne-wagen-dunkel.svg` | dasselbe ohne den Wagen, dunkler Grund |
| `logo-ohne-wagen-hell.svg` | dasselbe ohne den Wagen, heller Grund |
| `logo-zeile.svg` | nur K und Wagen, ohne Schriftzug — für kleine Anwendungen |
| `logo-k.svg` | nur das Monogramm — trägt bis 18 px herunter, der Wagen nicht |

**Das K ist in allen Fassungen gleich hoch** (89 Einheiten). Wer die Fassung
mit und ohne Wagen nebeneinander legt, sieht dasselbe Zeichen im selben
Maßstab — nur einmal mit und einmal ohne Wagen.

**Der Schriftzug steht in Kurven**, nicht als Text. Wer die Datei öffnet,
braucht die Schrift also nicht installiert zu haben und bekommt trotzdem
denselben Schriftzug. Nachgemessen gegen die Fußzeile: INGENIEURBÜRO
253,5 px in der Datei gegen 253,4 px auf der Seite.

**Der Hintergrund ist durchsichtig.** `logo-dunkel.svg` ist für dunklen Grund
gemacht — auf Weiß verschwindet das weiße K.

**Wenn sich die Schrift der Seite ändert**, muss `python3 bau_logo.py` noch
einmal laufen: das Skript zieht die Schrift aus `index.html`, damit der
Schriftzug in der Datei gar nicht vom Schriftzug auf der Seite abweichen kann.

Größen und Abstände sind dieselben wie in der Fußzeile und stammen aus der
Messung an Nurettins Vorlage: der Wagen ist 1,082-mal so hoch wie das K, der
Spalt beträgt 6 px bei 89 px K-Höhe.
