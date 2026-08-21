# Ingenieurbüro Kaltbrunn — Website

Kfz-Gutachten mit Sachverstand · Heppenheim, Kreis Bergstraße

Zwei Seiten: `index.html` und `referenzen.html` — **ohne jede externe
Verbindung**.
Schriften, Bilder und Skripte stecken als Data-URI darin — keine Google Fonts,
keine Cookies, kein Tracking. Damit entfällt der DSGVO-Klassiker „IP-Adresse an
Google übertragen“, und die Seite lädt in einem einzigen Request.

| | index.html | referenzen.html |
|---|---|---|
| Größe | 250 KB | 183 KB + 423 KB Fotos |
| Requests | 1 | 1 + 7 Fotos (eigene Adresse) |
| externe Verbindungen | 0 | 0 |

## Referenzen

`referenzen.html` wird **gebaut, nicht von Hand bearbeitet**:

```
python3 bau_referenzen.py
```

Kopf, Schrift, Navigation und Fußzeile kommen aus `index.html`, damit die
beiden Seiten nicht auseinanderlaufen. Neu ist nur der Inhalt zwischen
`<main>` und `</main>`; Fälle und Bildtexte stehen in der Liste `FAELLE`
oben im Skript. Der Pages-Workflow baut die Datei nach und bricht ab, wenn
das Ergebnis vom eingecheckten Stand abweicht.

Die Fotos liegen als Dateien unter `fotos/` und werden verlinkt statt
eingebettet: eigene Adresse, kein Fremdanbieter, und der Browser lädt sie
erst beim Scrollen.

Von jedem Foto liegen zwei Größen bereit: `…-klein.webp` (800 px) steht im
Raster, `….webp` (1600 px) lädt der Browser erst, wenn jemand ein Bild
anklickt. Das Raster kommt damit auf 423 KB statt 1,6 MB.

Neue Aufnahmen nach `fotos/original/` legen (01.jpg, 02.jpg … in der
gewünschten Reihenfolge), Beschriftung in `FAELLE` ergänzen, dann:

```
python3 fotos/aufbereiten.py    # erzeugt beide Größen, ohne Kameradaten
python3 bau_referenzen.py
```

`fotos/original/` wird nicht veröffentlicht — der Workflow kopiert nur
`fotos/*.webp`.

Vor dem Veröffentlichen der Fotos: siehe die Liste im Kopf von
`fotos/aufbereiten.py` — Kennzeichen, gespiegelte Personen, Firmenaufkleber
und die Einwilligung der Auftraggeber.

## Marke

Vorlage ist Nurettins eigener Logo-Entwurf, der als Datei unter
`marke/vorlage/logo_nurettin.webp` liegt: ein **K** aus Balken und Winkel,
daneben der verunfallte Wagen, darunter INGENIEURBÜRO / KALTBRUNN.
Übernommen ist alles davon.

**Das K** entsteht in `marke/bau_k.py`. Die Maße sind nicht geschätzt,
sondern werden bei jedem Lauf aus der Vorlage abgelesen — an drei Zeilen:
dem oberen Ende des oberen Arms (waagerechte Armdicke), der Höhe der
Winkelspitze (äußere und innere Spitze) und einer Spalte im Balken
(Gesamthöhe). Der erste Anlauf hatte sie geraten und lag daneben: die Arme
waren **80 % zu dick**, das Zeichen 13 % zu breit. Aus Außenspitze,
Armdicke und Gesamtbreite folgt der Rest, beide Kanten eines Arms sind
damit zwangsläufig parallel; das Skript bricht ab, wenn die gerechnete
innere Spitze mehr als zwei Einheiten von der gemessenen abweicht.

**Der Wagen** entsteht in `marke/bau_wagen.py` — nachvektorisiert, nicht
nachgezeichnet. Vier Anläufe, ihn von Hand zu setzen, sind gescheitert; die
Vorlage ist eine gerenderte Strichzeichnung und keine Konstruktion. Drei
Ebenen von unten nach oben: `lack` (die gefüllte Silhouette), `mittel` (die
hellen Schattierungen), `linie` (Konturen und dunkle Flächen). Die
Silhouette entsteht nicht aus einer eigenen Maske, sondern indem vom
Bildrand her geflutet wird — was die Flut nicht erreicht, ist Wagen. Ohne
diese Ebene wäre die Karosserie durchsichtig und der Wagen stünde auf
dunklem Grund als Negativbild da.

Die Bitmapbreite (`BREITE = 430`) bestimmt die Zahl der Stützpunkte und
damit die Dateigröße. Gemessen ist 430 px der Punkt, ab dem mehr Auflösung
in den Größen, in denen der Wagen auf der Seite steht, nichts Sichtbares
mehr hinzufügt: 62 KB roh, rund 23 KB gzip.

Größenverhältnisse in der Fußzeile sind ebenfalls an der Vorlage gemessen:
der Wagen ist **1,082 mal so hoch** wie das K, beide stehen mittig
zueinander, der Spalt beträgt 0,068 K-Höhen, und die Reihe ist ungefähr so
breit wie der Schriftzug darunter — daraus folgt die K-Höhe von 89 px.

Wo die Marke steht:

| Ort | Form | Farben |
|---|---|---|
| Navigationskopf | nur das Monogramm, 34 × 32 px | Balken weiß, Winkel `#4d8bf5` |
| Fußzeile | ganzes Zeichen: K + Wagen + Schriftzug | dazu Lack weiß, Linie `#0a2260` |
| Unfall-Sequenz | die Seitenansicht aus `marke/bau_skizze.py`, **nicht** der Wagen aus dem Logo | eigene `--sk-*`-Töne |

Warum im Kopf nur das K: der Wagen wird unter 20 px zu Matsch, das
Monogramm trägt bis 18 px. Nachgeprüft bei 120/64/40/28/18 px auf Weiß und
auf Marineblau.

Warum die Sequenz einen eigenen Wagen hat: der aus dem Logo ist
frontal-schräg gezeichnet und **vorne bereits eingedrückt**. Zwei davon
zeigen beide zur Kamera statt aufeinander, und ein Wagen, der schon vor dem
Aufprall verbeult ist, erzählt die Sequenz falsch herum.

Der Sequenzwagen ist deshalb eine eigene **Seitenansicht**
(`marke/bau_skizze.py`). Warum Seitenansicht: eine Dreiviertelansicht von
Hand zu setzen ist hier viermal gescheitert, weil jede Linie zur Fluchtung
passen muss — die Seitenansicht ist orthogonal, da gibt es keine
Perspektive, die man verfehlen kann. Für zwei Wagen, die frontal
aufeinander zufahren, ist sie ohnehin die richtige Ansicht.

Die Maße sind keine Erfindung, sondern eine gängige Limousine (Länge 4700,
Höhe 1450, Radstand 2850, Rad 650, Überhang vorn 900, hinten 950 — in
Millimetern), umgerechnet auf 240 Einheiten Länge. Deshalb stehen Räder,
Überhänge und Dachhöhe zueinander wie bei einem echten Wagen und nicht wie
bei einem Spielzeug.

Auf Marineblau bleibt beim Wagen der Lack weiß. Als reine Kontur (Lack
durchsichtig) kippt er ins Negativbild und ist nicht mehr derselbe Wagen —
ausprobiert und verworfen.

`marke/k.svg` und `marke/wagen.svg` sind die eingecheckten Bauergebnisse;
der Workflow prüft, dass `index.html` sie wörtlich enthält. Von Hand im
Pfad zu schieben bricht beim K die Parallelität sichtbar.

## Tonfall

Die Seite spricht in der **Ich-Form**. Ein Ingenieurbüro mit einer Person
klingt im „wir“ nach Behörde, und genau das war die Rückmeldung. Ebenso
bewusst weg sind: der Rundstempel mit Umlaufschrift, die Eckmarken und der
Maßstab am Blattrand, gesperrte Versalien als Etikettenschrift und die
scharfen Kanten. Dazu ein warmer Akzent (`--flamme`), der aus dem Feuer der
Marke kommt und dem Blau die Amtskühle nimmt.

## Bearbeiten

`index.html` wird direkt bearbeitet — kein Build, kein Werkzeug. Die langen
Base64-Blöcke sind die eingebettete Schrift (Archivo, variabel) und das
Porträt; dazwischen steht ganz normales HTML, CSS und JavaScript.

Lokal genügt ein Doppelklick auf die Datei — mangels relativer Pfade verhält sie
sich genauso wie über einen Server. Wer trotzdem einen will:

```
python -m http.server 4599
```

## Veröffentlichen

**Live: https://bilal-altu.github.io/kaltbrunn/**

Jeder Push auf `main` veröffentlicht beide Seiten. Der Workflow prüft sie
zuerst und bricht ab, sobald eine wieder eine Fremdressource nachlädt — die
DSGVO-Sauberkeit kann so nicht unbemerkt verloren gehen; danach schiebt er das
Ergebnis auf den Zweig `gh-pages`.

Der Zweig `gh-pages` enthält ausschließlich die ausgelieferte Seite und wird
vom Workflow überschrieben — dort nichts von Hand ändern. Gearbeitet wird auf
`main`.

Bewusst nicht über die Pages-API (`configure-pages` / `deploy-pages`): das
Workflow-Token darf keine Pages-Site anlegen. Ein Zweig namens `gh-pages`
schaltet Pages dagegen ohne Zutun in den Einstellungen frei.

`robots.txt` sperrt die Vorschauadresse für Suchmaschinen, damit sie der
späteren echten Domain keine doppelten Inhalte macht. **Vor dem Livegang unter
eigener Domain muss die Datei weg.**

## Unfall-Sequenz

Zwischen Vertrauensleiste und Leistungen liegt eine Scroll-Erzählung: zwei
Wagen stoßen zusammen, ein Strichmännchen steigt aus, zieht das Handy aus
der Tasche, ruft diese Seite auf — und der Schirm wächst, bis er die Seite
**ist**.

Sie steht **bewusst nicht als Vorspann vor der Seite**. Wer gerade einen
Unfall hatte, will die Nummer sofort — ein Vorspann hätte genau die
Anrufe gekostet, um die es geht. Anriss und Telefonnummer sind ab der
ersten Sekunde da.

Gesteuert wird über acht Fortschrittswerte plus eine Gangwelle, die das
Skript beim Scrollen als CSS-Variablen auf `.unfall-szene` setzt. Bewegt
werden ausschließlich `transform` und `opacity`.

```
--anfahrt      0 – 20 %     --tasche  50 – 58 %     Hand in die Tasche
--knall       19 – 26 %     --hoch    58 – 66 %     Handy hoch
--nach        24 – 36 %     --handy   66 – 80 %     fliegt in die Mitte
--aussteigen  34 – 50 %     --zoom    80 – 100 %    wird zur Seite
```

`--gang` ist `sin(aussteigen · 4π) · (1 − aussteigen)`: zwei volle
Schritte, die zum Stillstand hin auslaufen. In CSS gibt es dafür nichts
Verlässliches, im Skript ist es eine Zeile.

Das Strichmännchen ist aus Kästen gebaut und nicht aus SVG, damit jedes
Glied einen eigenen Drehpunkt hat, ohne von `transform-box` abzuhängen.
Der rechte Arm hat drei Lagen — gehen, in die Tasche, Handy hoch — deren
Gewichte sich in jedem Moment zu eins addieren.

Drei Fehler steckten in der ersten Fassung und sind raus:

- **Die Aufprallstrahlen steckten im Wagen.** In der alten Marke waren sie
  Teil der Zeichnung — dadurch fuhren beide Wagen schon vor dem Knall mit
  Strahlen herum. Sie liegen jetzt allein in `.knall` und verschwinden mit
  `(1 − nach)`, statt mit 0,55 stehen zu bleiben, wenn die Wagen längst
  wieder auseinander sind.
- **Die Wagen fuhren ineinander.** `-96 %` setzt die Front vier Prozent
  einer Wagenlänge *hinter* die Bildmitte, beim Gegner ebenso — macht acht
  Prozent Durchdringung. Jetzt `-100 %` (Front genau in der Mitte), plus
  zwei Prozent während des Knalls als Knautschung. Nachgemessen über den
  ganzen Anfahrtsweg: höchstens 1,7 % bei 1440 und 2,3 % bei 390 px, und
  zwar genau im Moment des Aufpralls.
- **Die Sätze überblendeten sich sichtbar.** Zwei verschieden lange Zeilen
  standen übereinander. Der abgehende Satz geht jetzt in 0,16 s raus, der
  nächste kommt mit 0,16 s Verzögerung — sie überlappen nicht mehr.

Zwei weitere Dinge lagen daneben und wären es geblieben, hätte ich nicht
nachgemessen:

- **Am Handy füllen die beiden Wagen die ganze Breite.** Links neben dem
  Wagen ist dort kein Platz; die Figur lief aus dem Bild (linke Kante bei
  −29 px). Am Handy tritt sie deshalb nach vorn **vor** den Wagen statt
  zur Seite. Nachgemessen bei 320, 360, 390, 768 und 1440 px über den
  ganzen Scrollweg: die Figur bleibt überall im Bild.
- **Der Startpunkt des großen Handys** ist an der erhobenen Hand gemessen,
  nicht geschätzt (`--hand-x`, `--hand-y`), sonst springt es beim
  Übernehmen. Wer den Armwinkel ändert, muss neu messen — beim Wechsel von
  −58° auf −108° lag der Startpunkt sofort wieder daneben.
- **Der erhobene Arm muss über die Waagerechte.** −58° schwenkt ihn nur
  zur Seite; „Handy hoch" liest sich erst ab etwa −100°. Das Handy in der
  Hand dreht mit demselben Betrag zurück, damit es aufrecht bleibt — die
  beiden Winkel müssen gespiegelt bleiben.

### Der Schirm wird die Seite

Der Schirm **wächst nicht nur, er ändert dabei sein Seitenverhältnis**.
Deshalb werden Breite und Höhe gerechnet und nicht per `scale()` gezogen:
ein Maßstab kann aus 9:17,5 nie 16:9 machen, und genau das muss passieren,
damit der Schirm das Fenster wirklich ausfüllt.

```
--f = min(1, --zoom / 0,82)          Füllgrad
Breite = w0 + (100 % − w0) · f       w0 = clamp(270px, 40vh + 28px, 470px)
Höhe   = h0 + (100 % − h0) · f       h0 = (w0 − 28px) · 17,5/9 + 28px
```

Für den Flug aus der Hand in die Bildmitte bleibt es bei `scale()` — dort
ändert sich der Kasten nicht, und das ist billiger. Erst im Zoom übernehmen
Breite und Höhe. **Hochskaliert wird nie**: bei `--handy` 1 steht der
Maßstab auf 1 und bleibt dort.

Die Schrift wächst über **Container-Anfragen** mit (`container-type:
inline-size` auf dem Schirm, Größen in `cqw` mit `clamp()`). Sie wird
dadurch in jeder Größe frisch gesetzt statt als Bild aufgezogen — das ist
der zweite Grund, warum nichts mehr unscharf werden kann.

Nachgemessen: der Schirm erreicht bei 1440×900, 1280×700, 390×844 und
320×650 jeweils **100 % der Bildfläche** und sitzt exakt auf (0,0). Die
Textspalte ist auf 680 px begrenzt und mittig — bei 1440 px sind das
380 px Rand auf jeder Seite; über die volle Breite wären die Zeilen
unlesbar lang.

Kosten: Layout je Bild statt nur `transform`. Gemessen über 180 Schritte
durch den Scrollweg — Bildabstand im Median **16,7 ms** (also 60 Bilder je
Sekunde), gleich wie die vorherige Fassung, die nur Transformationen
bewegte. `.handy` steht absolut und trägt `contain: layout paint`, das
Layout bleibt also in diesem Kasten.

Was dadurch **entfallen ist**: die Fläche hinter dem Schirm, die
Mittelfarbe gegen die sichtbare Kante, das Auflösen des Handys und die
Überblendung zum Schlussbild. Der Schirm deckt am Ende alles selbst ab, es
gibt keine zwei Lagen mehr, die zusammenpassen müssten. Nur die eigene
Kopfleiste des Schirms blendet zum Schluss weg — sonst schauten vier Pixel
unter der echten Navigationsleiste hervor und es wären sichtbar zwei.

Der Schlussblock `.unfall-schluss` ist nicht mehr sichtbar, bleibt aber im
Dokument: das Handy ist `aria-hidden` (seine Knöpfe tragen `tabindex="-1"`),
also bekommen Vorleseprogramme Nummer und Anfrage über diesen Block — und
wer Bewegung abbestellt hat, sieht ihn als Schlussbild.

Die Wagenwege sind auf die **Fahrzeugmitte** bezogen, nicht auf die linke
Kante: `left: 50 %` setzt die linke Kante in die Bildmitte, und genau
dieser Denkfehler hatte den Gegner am Handy aus dem Bild geschoben.
`-96 %` heißt jetzt „rechte Kante an der Bildmitte".

Der Scrollweg ist mit dem Aussteigen von 320vh auf **460vh** gewachsen
(am Handy 400vh). Wer `prefers-reduced-motion` gesetzt hat, bekommt kein
Sticky und keinen Scrollweg, sondern das Schlussbild mit allen vier Sätzen
untereinander; Figur und Seitenfläche sind dort ausgeblendet.

## Texte

Die Inhalte stammen aus Nurettins eigenem Entwurf (E-Mail vom 18.08.),
seine Platzhalter für Telefon und E-Mail sind mit den echten Daten gefüllt.

Zwei Formulierungen daraus stehen bewusst so da und sollten vor dem
Livegang noch einmal von ihm bestätigt werden:

- **„Meisterhafter Blick"** als Überschrift bei „Über mich". Gemeint ist
  der geschulte Blick, nicht ein Meistertitel — er ist B. Eng., kein
  Handwerksmeister. Missverständlich ist es trotzdem.
- **„Vom Premium-Hersteller zum unabhängigen Gutachter"** ist die
  Anriss-Überschrift, auf Bilals ausdrückliche Entscheidung. Der Hinweis
  bleibt hier stehen, damit ihn niemand später sucht: Das „vom … zum"
  liest sich wie ein abgeschlossener Wechsel, die Tätigkeit beim
  Hersteller läuft aber weiter. Im Abschnitt darunter steht es richtig
  („Vom Blaumann … bis zum Qualitätsingenieur"), und die Unterzeile
  nennt ihn „freier Kfz-Sachverständiger" — der Widerspruch ist damit
  entschärft, aber nicht ganz weg.

## Vor dem Livegang

- [ ] **Impressum**: USt-IdNr. (§ 27a UStG) und Berufshaftpflichtversicherung ergänzen
- [ ] **Domain und E-Mail** stehen noch auf `ing-nuri.de` (canonical, og:url,
      JSON-LD, Formular, Footer) — bei neuer Domain überall nachziehen
- [ ] **Öffnungszeiten**: im JSON-LD stehen Mo–Fr 8–18 Uhr. Entweder bestätigen
      oder streichen
- [ ] **„24h Rückmeldung“** mit der hauptberuflichen Tätigkeit abgleichen — ein
      Versprechen, das nicht hält, kostet mehr Vertrauen als es bringt
- [ ] **`robots.txt` entfernen**, sobald die Seite unter eigener Domain läuft

## Geprüft

Chromium, 320 / 360 / 390 / 414 / 768 / 1024 / 1280 / 1440 px: keine JS-Fehler,
kein horizontaler Überlauf,
keine doppelten IDs, keine toten Sprungziele, saubere Überschriften-Reihenfolge,
alle Bilder mit Alt-Text und festen Maßen, alle Formularfelder beschriftet,
`main`-Landmarke und Sprungmarke vorhanden, gültiges JSON-LD. Alle geprüften
Textrollen erreichen WCAG AA — die im Anriss gegen die tatsächlich gerenderten
Hintergrundpixel gemessen, nicht gegen eine angenommene Farbe.

## Verworfene Entwürfe

Zwei weitere Fassungen (Tiefschwarz und Prüfblau, beide im selben reduzierten
Aufbau) wurden verworfen. Sie liegen samt Bau-System in der Git-Historie:

```
git log --oneline --diff-filter=D -- index-tuev.html
git checkout <commit>^ -- index.html index-tuev.html src/
```
