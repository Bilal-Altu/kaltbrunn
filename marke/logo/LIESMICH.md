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

### Zwei Fassungen nur für die Visitenkarte

`karte-front-…` und `karte-marke-…` entstehen in `bau_kartenmarke.py` aus
denselben Teilen wie alles andere, es sind nur zwei weitere Anordnungen:

- **`karte-front-…`** ist das ganze Zeichen mit Wagen, aber der Claim steht
  auf **KALTBRUNN-Größe** (16,8) statt auf Fußzeilengröße (13,12) – und er
  heißt dort „Gutachten mit Sachverstand" ohne „Kfz-".
- **`karte-marke-…`** ist die waagerechte Fassung in Versalien: K, ein
  senkrechter Trennstrich, rechts daneben INGENIEURBÜRO über KALTBRUNN mit
  den beiden Strichen. Nicht zu verwechseln mit `logo-quer-…`, das ohne
  Trennstrich und in gemischter Schreibung aus ihrer Kopfzeile stammt.

Beide gibt es in den drei `web-`Farbfassungen.

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

## Visitenkarte

**Das ist die aktuelle Karte.** Gebaut von `bau_karte_nuri.py` nach Bilals
Vorgabe vom 9. Oktober und den beiden Vorlagen, die er dazu geschickt hat.

| Datei | was drin ist |
|---|---|
| `Visitenkarte-Nuri-Druck.pdf` | **für die Druckerei** – 2 Seiten, 91 × 61 mm, Vektor |
| `Visitenkarte-Nuri-Vorderseite.svg` | dieselbe Vorderseite einzeln |
| `Visitenkarte-Nuri-Rueckseite.svg` | dieselbe Rückseite einzeln |

**Vorderseite:** nur das Zeichen **mit** Wagen, darunter „Gutachten mit
Sachverstand" – in derselben Schriftgröße wie KALTBRUNN, nicht kleiner wie
im Seitenfuß. Sonst nichts.

**Rückseite:** das Zeichen **ohne** Wagen, waagerecht (K, Trennstrich,
INGENIEURBÜRO über KALTBRUNN), **oben rechts**. Links darunter Name, die
Zeile „Maschinenbau-Ing. – Fahrzeugtechnik (B. Eng.)", Mobilnummer,
E-Mail, Domain, Büroanschrift. **Kein Festnetz** – so bestellt. Rechts
unten der QR-Code.

Das Zeichen steht rechts, nicht links: so hat die Karte **eine** rechte
Flucht – Zeichen oben, QR-Code unten – und **eine** linke für allen Text.
Zwei saubere Kanten statt einer Kante und einer Ecke.

### Der QR-Code

Er führt auf `https://wa.me/4917637998836`, öffnet also direkt den
WhatsApp-Chat mit Nurettin. Gebaut mit segno, Version 4 (33 × 33 Module).

Er steht **als Pfad in der Datei**, nicht als Bild – auch der Code ist
Vektor und wird beim Vergrößern nicht kantig.

Drei Dinge unterscheiden ihn von dem Raster, das ein Generator ausspuckt:

- **Die Module sind gerundet** (Radius 0,26 Modul).
- **Die drei Augen sind gezeichnet**, als Rahmen und Kern, nicht aus
  49 Einzelmodulen zusammengesetzt.
- **In der Mitte bleiben 9 × 9 Module frei**, da steht das WhatsApp-Zeichen
  als grüner Kreis mit weißer Kurve. Damit sieht man dem Code an, wohin er
  führt, statt es daneben schreiben zu müssen.

| | |
|---|---|
| bedruckte Fläche | 18 × 18 mm |
| ein Modul | 0,545 mm (empfohlen sind ≥ 0,4 mm im Offset) |
| Ruhebereich | 2,18 mm = 4 Module, **außerhalb** der 18 mm |
| Fehlerkorrektur | **H** (30 %) |
| vom Zeichen verdeckt | 81 von 1089 Modulen = **7,4 %** |

Fehlerkorrektur H statt M, weil das Zeichen in der Mitte Module verdeckt.
M verträgt 15 %, und die 15 % sind die Reserve für Knicke, Fingerabdrücke
und schlechtes Licht – nicht für unser Zeichen.

**Das WhatsApp-Zeichen** liegt als `marke/whatsapp.svg` daneben, unverändert
so, wie es von Simple Icons 13.20 kommt (das Icon-Set steht unter CC0). Die
Marke selbst gehört WhatsApp; sie steht auf der Karte, um zu zeigen, wohin
der Code führt — genau dafür ist sie da. Eingelesen statt abgetippt: eine
Kurve mit 1104 Zeichen tippt man nicht fehlerfrei ab.

#### Gestaltung kostet Lesbarkeit — deshalb nachgemessen

Die Rundung der **Augen** war zuerst viel zu stark (Radius 1,9 Module). Der
Bogen frisst dann die Eckmodule weg und setzt sie diagonal nach innen:
23 von 1089 Modulen standen falsch, und der Code war **nicht mehr lesbar**.
Das fällt beim Hinsehen nicht auf — nur beim Auslesen. Jetzt 0,30.

Geprüft wird mit **zwei** Lesern, weil einer allein in die Irre führt:

| | OpenCV | ZXing |
|---|---|---|
| ohne Zeichen, eckig | 18/23 | 23/23 |
| wie auf der Karte | 3/23 | 23/23 |

OpenCVs `QRCodeDetector` kommt mit gestalteten Codes schlecht zurecht und
hätte die Karte durchfallen lassen. ZXing ist die Familie, auf der die
Leser in den Telefonen aufsetzen — danach richten wir uns.

**Der Prüflauf am fertigen PDF** (600 dpi, Ausschnitt wie ein schnelles
Handyfoto, gedreht, unscharf, verrauscht, flau):

| Prüfung | Ergebnis |
|---|---|
| ganze Karte, sauber, 400–2150 px | **6 von 6** |
| hart: 180–520 px, ±35°, Unschärfe 0–7, Rauschen | **112 von 120** |

Durchgefallen sind nur die acht härtesten Fälle: 180–220 px breit **und**
7 px Unschärfe, also ein unscharfes Daumennagelbild. Bei 17 mm Codegröße
waren es 88 von 120 — der Millimeter mehr war den Platz wert.

### Nachgemessen

| Regel | Karte |
|---|---|
| höchstens 3 Schriftgrößen | **2** (11 pt Name, 8 pt Rest) |
| Kontaktdaten ≥ 8 pt | **8 pt**, nichts darunter |
| eine Ausrichtung | alles auf der linken Kante, nur der QR rechts – und der ist kein Text |
| Weißraum 25–35 % | **77 %** vorn, **56 %** hinten |
| Sicherheitsabstand ≥ 3 mm | **4 mm**; Druckfarbe liegt in 7,0–84,1 × 7,0–52,5 mm |
| Anschnitt 2–3 mm | **3 mm** |
| Schrift im Dokument | **keine** – alles Kurven, `/BaseFont` kommt im PDF nicht vor |
| Bilder im Dokument | **keine** – `/Subtype /Image` kommt nicht vor |

Unterschieden wird über **Gewicht und Farbe**, nicht über immer neue Größen:
Name 800 in `#15171a`, Rolle 500 in `#003da5`, Telefon 600 in `#15171a`,
restliche Daten 400 in `#5d6470`.

Die einzige dritte Farbe ist das WhatsApp-Grün `#25D366` im Code — und das
ist keine Gestaltungsentscheidung, sondern die Marke, an der man WhatsApp
erkennt. In irgendeinem anderen Ton wäre sie nutzlos.

### Was offen ist

- **„Freier Kfz-Sachverständiger" steht nicht mehr auf der Karte.** Bilals
  Vorgabe ersetzt die Zeile „Inhaber" durch den Grad; eine zweite Rollenzeile
  stand nicht in der Liste. Wenn die Berufsbezeichnung drauf soll, kommt sie
  zwischen Name und Grad.
- **Der Claim heißt auf der Karte „Gutachten mit Sachverstand"**, im Logo und
  auf der Webseite dagegen „**Kfz**-Gutachten mit Sachverstand". So hat Bilal
  es geschrieben. Entweder zieht die Karte das „Kfz-" nach oder Logo und Seite
  lassen es weg – zwei Fassungen desselben Claims sollten es nicht bleiben.
- **Die Domain wechselt noch.** Vor dem Druck bestätigen lassen; ein falscher
  Aufdruck kostet die ganze Auflage, nicht eine Datei.

Die Datei ist **RGB**, nicht CMYK – siehe die Farbtabelle weiter unten.

## Visitenkarte, erste Fassung (überholt)

Steht nur noch da, falls jemand den alten Satz vergleichen will.
**Nicht in den Druck geben** – es gilt die Karte oben.


Es gibt sie in **zwei Varianten**, damit Nurettin wählen kann. Der
Unterschied ist genau einer — die Rückseite:

| Datei | Rückseite |
|---|---|
| `Visitenkarte-Variante-1-Druck.pdf` | Zeichen **ohne** Wagen |
| `Visitenkarte-Variante-2-Druck.pdf` | Zeichen **mit** Wagen |
| `Visitenkarte-Auswahl.pdf` | A4-Blatt mit beiden in Originalgröße, zum Vorlegen |

Die Vorderseite ist in beiden gleich — so steht genau eine Frage zur
Entscheidung und nicht zwei. Der Wagen steht in Variante 2 auf 27 statt
32 mm Zeichenhöhe, weil das Zeichen mit Wagen breiter als hoch ist; der
Wagen bekommt so immer noch rund 13 mm eigene Höhe und bleibt weit über
den gemessenen 20 px, ab denen er zu Matsch wird.

Beide Druckdateien haben zwei Seiten, 91 × 61 mm. Das ist 85 × 55 mm
Endformat plus **3 mm Anschnitt** ringsum. Alles, was stehen bleiben muss,
hält **4 mm** Abstand von der Schnittkante (deutsche Druckereien verlangen 3).
Gebaut von `bau_visitenkarte.py`.

**Die erste Fassung war durchgefallen** — sie hatte fünf Schriftgrößen, die
Kontaktdaten standen auf 6,8 pt und die Daten liefen in zwei Spalten mit je
eigener Kante. Was Setzer und Druckereien dazu sagen, ist eindeutig:
höchstens drei Größen, Kontaktdaten nicht unter 8 pt, eine Ausrichtung
durchhalten, Struktur statt Dekoration, 25–35 % der Karte leer lassen.

Nachgemessen an der zweiten Fassung:

| Regel | Karte |
|---|---|
| höchstens 3 Schriftgrößen | **2** (11 pt Name, 8 pt Rest) |
| Kontaktdaten ≥ 8 pt | **8 pt**, nichts darunter |
| eine Ausrichtung | alle vier Blöcke auf **derselben linken Kante** |
| Weißraum 25–35 % | **55 %** |
| Sicherheitsabstand ≥ 3 mm | **4 mm** |
| Anschnitt 2–3 mm | **3 mm** |

Unterschieden wird über **Gewicht und Farbe**, nicht über immer neue Größen:
Name 800 in `#002a73`, Rolle 600 in `#003da5`, Grad 400 in `#5d6470`,
Telefon 600, restliche Daten 400.

**Die Datei ist RGB, nicht CMYK.** Chromium kann kein CMYK. Die Druckerei muss
nach **FOGRA51 (PSO Coated v3)** wandeln — bei gestrichenem Papier — oder
FOGRA52 für ungestrichenes. Die Hex-Werte als Referenz:

| | Hex |
|---|---|
| Marke | `#003DA5` |
| Marke tief | `#002A73` |
| Dunkelfläche | `#171D29` |
| Text | `#15171A` |
| Text gedämpft | `#5D6470` |

Wenn die Farbe über mehrere Auflagen exakt gleich sein soll, lässt man sich
von der Druckerei einen Pantone-Ton am Fächer heraussuchen statt in CMYK zu
drucken. Das ist teurer und lohnt erst ab größeren Mengen.

**Die Karte steht auf `ing-kaltbrunn.de`** — so hat Bilal es am 25.08.
korrigiert. Der Web-Verweis zieht mit: eine Karte mit
`info@ing-kaltbrunn.de` neben `www.ing-nuri.de` sieht nach Fehler aus,
egal welche der beiden stimmt.

**Die Webseite steht noch auf `ing-nuri.de`**, an 16 Stellen. Wenn sie
mitziehen soll:

    python3 setze_domain.py ing-kaltbrunn.de info@ing-kaltbrunn.de
    python3 bau_referenzen.py
