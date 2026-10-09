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
  auf **KALTBRUNN-Größe** (16,8) statt auf Fußzeilengröße (13,12). Der
  Wortlaut ist derselbe wie im Logo und auf der Seite: „Kfz-Gutachten mit
  Sachverstand".
- **`karte-marke-…`** ist die waagerechte Fassung in Versalien: K, ein
  senkrechter Trennstrich, rechts daneben INGENIEURBÜRO über KALTBRUNN mit
  den beiden Strichen. Nicht zu verwechseln mit `logo-quer-…`, das ohne
  Trennstrich und in gemischter Schreibung aus ihrer Kopfzeile stammt.

  **Die erste Fassung war zu gedrungen.** Der Schriftzug stand dort auf
  den Größen der Fußzeile (23,2 / 16,8) und war damit halb so groß wie auf
  Bilals Vorlage; das Zeichen kam auf 4,7 : 1, die Vorlage auf 8,4 : 1.
  Neu gemessen an der Vorlage (K dort 138 px hoch), alles auf K = 89
  gerechnet:

  | | Vorlage | × K | bei K = 89 |
  |---|---|---|---|
  | K | 150 × 138 px | 1,087 | 96,7 breit |
  | Luft K → Trennstrich | 67 px | 0,486 | 43,2 |
  | Trennstrich | 4 × 165 px | 0,029 / 1,196 | 2,6 × 106,4 |
  | Luft Trennstrich → Text | 69 px | 0,500 | 44,5 |
  | Block breit | 1093 px | 7,920 | 704,9 |
  | INGENIEURBÜRO, Versalhöhe | 59 px | 0,428 | 38,1 |
  | Zeilenluft | 37 px | 0,268 | 23,9 |
  | KALTBRUNN, Versalhöhe | 43 px | 0,312 | 27,7 |
  | KALTBRUNN, nur das Wort | 632 px | 4,580 | 407,6 |
  | Strich | 188 px lang, 5 stark | 1,362 | 121,3 × 3,2 |
  | Luft Strich → Wort | 44 px | 0,319 | 28,4 |

  Der Schriftzug wird daraus **über die Versalhöhe** aufgebaut, nicht über
  eine Schriftgröße, und die Sperrung wird auf die gemessene Breite
  gerechnet. Der Block ist so hoch wie das K – auf der Vorlage ist er es
  auch. Das Größenverhältnis der beiden Wörter stimmte übrigens schon
  vorher: 59 : 43 auf der Vorlage, 23,2 : 16,8 bei uns, beides 1,37.

  Die Höhe der Datei kommt aus der **wirklichen Druckfarbe**, nicht aus
  der Versalhöhe: die Punkte des Ü stehen darüber, und ohne das saß die
  oberste Druckfarbe auf der Karte 0,27 mm über dem Sicherheitsrand.

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

**Vorderseite:** nur das Zeichen **mit** Wagen, darunter „Kfz-Gutachten
mit Sachverstand" – in derselben Schriftgröße wie KALTBRUNN, nicht kleiner
wie im Seitenfuß. Sonst nichts.

Der Claim stand hier zuerst ohne „Kfz-", weil Bilal ihn so geschrieben
hatte; am 9. Oktober hat er das „Kfz-" nachgezogen. Damit heißt er auf der
Karte, im Logo und auf der Seite gleich. Die Vorderseite wird deshalb
**nicht mehr nach einer eingetippten Breite** mittig gerückt, sondern nach
der, die das Zeichen wirklich hat – beim nächsten geänderten Wort wäre
eine feste Zahl sonst wieder falsch.

**Rückseite:** das Zeichen **ohne** Wagen, waagerecht (K, Trennstrich,
INGENIEURBÜRO über KALTBRUNN), oben über die **ganze Breite** – von der
linken Kante bis zur rechten, 77 mm. Darunter Name, die Zeile
„Maschinenbau-Ing. – Fahrzeugtechnik (B. Eng.)", Mobilnummer, E-Mail,
Domain, Büroanschrift. **Kein Festnetz** – so bestellt. Rechts unten der
QR-Code.

Jede Angabe trägt ihr Zeichen: Handy, Brief, Globus, Haus – wie auf
Nurettins alter Karte, und unter dem Haus steht **„Büro"**. Die zweite
Adresszeile bekommt kein Zeichen; sie gehört zur selben Angabe, und ein
zweites Haus daneben würde eine zweite Adresse behaupten. Hinter der Mobilnummer steht zusätzlich das grüne
WhatsApp-Zeichen: es sagt dem, der **liest**, dass diese Nummer auf
WhatsApp erreichbar ist. Der Code unten rechts sagt dasselbe dem, der
**scannt**.

Die Zeichen stehen in einer eigenen Spalte links, der Text rückt um
5,4 mm ein. Das ist die einzige Stelle, an der die Karte eine zweite
senkrechte Kante hat – eine Zeichenspalte liest sich aber als Spalte,
nicht als zweite Flucht.

Das Zeichen wird dafür nicht vergrößert und nicht verschoben, es ist
**gezogen**: die waagerechte Fassung steht auf 8,1 : 1 und füllt die
Breite bei 9,5 mm Höhe. Eine Fassung in den Fußzeilenmaßen (4,7 : 1)
wäre bei 77 mm Breite 16,4 mm hoch gewesen – dann hätte der Satz
darunter nicht mehr gepasst.

### Der QR-Code

**Der Link kommt nicht von uns.** Er steht so in dem QR-Code, den die
WhatsApp-Business-App für Nurettins Unternehmenskonto ausgibt; Bilal hat
den Code geschickt, hier ist er ausgelesen worden:

    https://wa.me/message/CALFEXQOLNHND1?src=qr

Ein selbst gebautes `wa.me/<Nummer>` hätte auch funktioniert, aber am
Unternehmenskonto vorbei – die App zählt über diesen Link, woher ein Chat
kommt. Das `?src=qr` ist WhatsApps eigener Zusatz und bleibt deshalb
stehen. **Ändert sich das Konto, ändert sich der Link**; dann neu
auslesen, nicht neu erfinden.

Der Code steht **als Pfad in der Datei**, nicht als Bild – auch er ist
Vektor und wird beim Vergrößern nicht kantig.

Drei Dinge unterscheiden ihn von dem Raster, das ein Generator ausspuckt:

- **Die Module sind gerundet** (Radius 0,26 Modul).
- **Die drei Augen sind gezeichnet**, als Rahmen und Kern, nicht aus
  49 Einzelmodulen zusammengesetzt.
- **In der Mitte bleiben 11 × 11 Module frei**, da steht das
  WhatsApp-Zeichen als grüner Kreis mit weißer Kurve.

| | |
|---|---|
| bedruckte Fläche | 19 × 19 mm |
| Version | 5, 37 × 37 Module |
| ein Modul | 0,514 mm (empfohlen sind ≥ 0,4 mm im Offset) |
| Ruhebereich | 2,05 mm = 4 Module, **außerhalb** der 19 mm |
| Fehlerkorrektur | **H** (30 %) |
| vom Zeichen verdeckt | 121 von 1369 Modulen = **8,8 %** |

Der längere Link kostet eine Version: `wa.me/<Nummer>` passte in Version 4
mit 33 Modulen, der Unternehmenslink braucht Version 5 mit 37. Deshalb
steht der Code jetzt auf 19 statt 18 mm – damit ein Modul wieder über
0,5 mm liegt.

Die Öffnung ist mit 11 Modulen größer als nötig. Nachgemessen kostet sie
fast nichts: ohne Zeichen 96 von 120 harten Durchläufen, mit 9 Modulen 92,
mit 11 noch 91. Das Zeichen soll man erkennen und nicht suchen müssen.

**Das WhatsApp-Zeichen** liegt als `marke/whatsapp.svg` daneben, unverändert
so, wie es von Simple Icons 13.20 kommt (das Icon-Set steht unter CC0). Die
Marke selbst gehört WhatsApp; sie steht auf der Karte, um zu zeigen, wohin
der Code führt — genau dafür ist sie da.

### Die Zeichen neben den Zeilen

Handy, Brief, Globus und Haus kommen aus **Lucide** (`lucide-static`
0.544.0, ISC-Lizenz) und liegen unverändert in `marke/symbole/`. Sie sind
**gestrichen, nicht gefüllt**: bei 3,8 mm Kantenlänge landet die
Strichstärke bei rund 0,32 mm und bleibt damit über dem, was im Offset
noch sauber durchkommt. Wer sie kleiner setzt, muss die Stärke nachziehen.

Sie stehen in `#003DA5`, dem Markenblau – als Akzent, so wie auf der
gewählten Seite die Überschriften schwarz und die Akzente blau sind.

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
| hart: 180–520 px, ±35°, Unschärfe 0–7, Rauschen | **108 von 120** |

Durchgefallen sind nur die härtesten Fälle: um 200 px breit **und** stark
unscharf, also ein verwackeltes Daumennagelbild. Der Unternehmenslink ist
länger als ein `wa.me/<Nummer>` und damit dichter — mit dem kurzen Link
waren es 112 von 120.

### Nachgemessen

| Regel | Karte |
|---|---|
| höchstens 3 Schriftgrößen | **3** (11 pt Name, 8 pt Rest, 6 pt „Büro") |
| Kontaktdaten ≥ 8 pt | **8 pt**, nichts darunter |
| eine Ausrichtung | linke Kante für alles; die Zeichenspalte rückt den Satz ein, der QR steht rechts – und der ist kein Text |
| Weißraum 25–35 % | **77 %** vorn, **43 %** hinten |
| Sicherheitsabstand ≥ 3 mm | **4 mm**; Druckfarbe liegt in 7,0–84,1 × 7,0–52,4 mm (Rückseite), 21,9–69,0 × 15,6–45,0 mm (Vorderseite) |
| Anschnitt 2–3 mm | **3 mm** |
| Schrift im Dokument | **keine** – alles Kurven, `/BaseFont` kommt im PDF nicht vor |
| Bilder im Dokument | **keine** – `/Subtype /Image` kommt nicht vor |

Unterschieden wird über **Gewicht und Farbe**, nicht über immer neue Größen:
Name 800 in `#15171a`, Rolle 500 in `#003da5`, Telefon 600 in `#15171a`,
restliche Daten 400 in `#5d6470`.

**„Büro" ist die einzige Ausnahme von den 8 pt** – es steht auf 6 pt. Das
Wort ist aber keine Kontaktangabe, sondern die Beschriftung eines
Zeichens: wer die Adresse lesen will, liest die Zeile daneben, nicht das
Wort unter dem Haus. Die Zeichenspalte ist so breit wie das breitere von
Zeichen und Wort (4,90 mm), beide stehen darin mittig – sonst hinge das
Wort links aus dem Sicherheitsrand.

Die einzige dritte Farbe ist das WhatsApp-Grün `#25D366` im Code — und das
ist keine Gestaltungsentscheidung, sondern die Marke, an der man WhatsApp
erkennt. In irgendeinem anderen Ton wäre sie nutzlos.

### Was offen ist

- **„Freier Kfz-Sachverständiger" steht nicht mehr auf der Karte.** Bilals
  Vorgabe ersetzt die Zeile „Inhaber" durch den Grad; eine zweite Rollenzeile
  stand nicht in der Liste. Wenn die Berufsbezeichnung drauf soll, kommt sie
  zwischen Name und Grad.
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
| höchstens 3 Schriftgrößen | **3** (11 pt Name, 8 pt Rest, 6 pt „Büro") |
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
