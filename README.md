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
| Unfall-Sequenz | die gezeichneten Wagen, **nicht** der aus dem Logo | wie gehabt |

Warum im Kopf nur das K: der Wagen wird unter 20 px zu Matsch, das
Monogramm trägt bis 18 px. Nachgeprüft bei 120/64/40/28/18 px auf Weiß und
auf Marineblau.

Warum die Sequenz den gezeichneten Wagen behält: der aus dem Logo ist
frontal-schräg gezeichnet und **vorne bereits eingedrückt**. Zwei davon
zeigen beide zur Kamera statt aufeinander, und ein Wagen, der schon vor dem
Aufprall verbeult ist, erzählt die Sequenz falsch herum.

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
Wagen stoßen zusammen, ein Handy fährt hoch, auf dem Schirm lädt diese
Seite, am Ende steht der Aufruf.

Sie steht **bewusst nicht als Vorspann vor der Seite**. Wer gerade einen
Unfall hatte, will die Nummer sofort — ein Vorspann hätte genau die
Anrufe gekostet, um die es geht. Anriss und Telefonnummer sind ab der
ersten Sekunde da.

Gesteuert wird über fünf Fortschrittswerte, die das Skript beim Scrollen
als CSS-Variablen auf `.unfall-szene` setzt (`--anfahrt`, `--knall`,
`--nach`, `--handy`, `--zoom`). Bewegt werden ausschließlich `transform`
und `opacity`. Die Phasengrenzen stehen im Skript in einer Zeile:

```
--anfahrt  0 – 30 %      --handy  52 – 78 %
--knall   28 – 38 %      --zoom   78 – 100 %
--nach    36 – 52 %
```

Die Wagenwege sind auf die **Fahrzeugmitte** bezogen, nicht auf die linke
Kante: `left: 50 %` setzt die linke Kante in die Bildmitte, und genau
dieser Denkfehler hatte den Gegner am Handy aus dem Bild geschoben.
`-96 %` heißt jetzt „rechte Kante an der Bildmitte".

Wer `prefers-reduced-motion` gesetzt hat, bekommt kein Sticky und keinen
Scrollweg, sondern das Schlussbild mit allen vier Sätzen untereinander.

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
