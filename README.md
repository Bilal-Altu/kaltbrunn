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
| Unfall-Sequenz | die Figur aus `marke/bau_mensch.py`, im selben Strich wie die Wagen | eigene `--mn-*`-Töne |

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

## Schrift

**Rubik**, von Bilal vorgegeben. Variabler Schnitt 300–900, auf die
lateinische Teilmenge beschränkt und als Data-URI eingebettet — die Seite
lädt nichts von Google. Open Font License. **34 KB gegenüber 87 KB** bei
Archivo, `index.html` ist dadurch netto kleiner geworden.

**Was der Wechsel gekostet hat:** Archivo hatte eine *Breitenachse*
(`font-stretch: 84 %` für Schlagzeilen), Rubik hat keine. Die Angabe wäre
wirkungslos und irreführend und ist raus. Damit lief die Schlagzeile
breiter und „zum unabhängigen Gutachter:" brach auf eine vierte Zeile um.
Nachgezogen, an den Umbrüchen gemessen statt geschätzt:

| | vorher (Archivo) | jetzt (Rubik) |
|---|---|---|
| Spalten im Anriss | 1,06 / 0,94 | **1,10 / 0,90** |
| `.hero-content` | max. 620 px | max. **650 px** |
| h1 Schreibtisch | `clamp(1.9rem, 3.5vw, 2.7rem)` | `clamp(1.8rem, 2.9vw, 2.5rem)` |
| h1 Handy | `clamp(1.5rem, 6.4vw, 1.95rem)` | `clamp(1.25rem, 5.5vw, 1.95rem)` |
| Laufweite Schlagzeilen | −0,015 em (bei 84 % Breite) | **−0,021 em** |

Ergebnis nachgemessen bei 1920/1440/1280/1024/430/390/360 px: überall
**drei Zeilen**, wie mit Archivo. Bei 768 und 320 px sind es vier — das
war mit Archivo genauso, dort ist die Spalte schlicht zu schmal.

**Eine Kontrastfolge hatte der Wechsel auch:** die dritte Zeile
(„Präzision für Ihr Recht.") ist am Handy von 25 auf 21,4 px geschrumpft
und fällt damit unter die WCAG-Grenze für großen Text — ab da gilt 4,5
statt 3,0. Bei `rgba(255,255,255,0.5)` waren es 3,42. Jetzt **0,68**, das
sind 4,91 am Handy und 5,17 am Schreibtisch.

**Zwei Zeichen kann Rubik nicht:** `→` (U+2192) und `✓` (U+2713). Die
kommen aus der Systemschrift — bei Archivo war das genauso, beide fehlten
dort ebenfalls. Wer sie zeichensicher haben will, muss sie durch Inline-SVG
ersetzen.

## Tonfall

Die Seite spricht in der **Ich-Form**. Ein Ingenieurbüro mit einer Person
klingt im „wir“ nach Behörde, und genau das war die Rückmeldung. Ebenso
bewusst weg sind: der Rundstempel mit Umlaufschrift, die Eckmarken und der
Maßstab am Blattrand, gesperrte Versalien als Etikettenschrift und die
scharfen Kanten. Dazu ein warmer Akzent (`--flamme`), der aus dem Feuer der
Marke kommt und dem Blau die Amtskühle nimmt.

## Bearbeiten

`index.html` wird direkt bearbeitet — kein Build, kein Werkzeug. Die langen
Base64-Blöcke sind die eingebettete Schrift (Rubik, variabel) und das
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

Zwischen Anriss und Leistungen liegt eine Scroll-Erzählung: zwei
Wagen stoßen zusammen, ein Strichmännchen steigt aus, zieht das Handy aus
der Tasche, ruft diese Seite auf — und der Schirm wächst, bis er die Seite
**ist**.

Sie steht **bewusst nicht als Vorspann vor der Seite**. Wer gerade einen
Unfall hatte, will die Nummer sofort — ein Vorspann hätte genau die
Anrufe gekostet, um die es geht. Anriss und Telefonnummer sind ab der
ersten Sekunde da.

Die Vertrauensleiste, die vorher zwischen Anriss und Sequenz lag
(„Unabhängig & neutral", „Hält vor Gericht stand", „15 Jahre
Automobilindustrie", „Termine oft schon am nächsten Tag"), ist auf
Bilals Wunsch entfernt. Inhaltlich fehlt nichts: die drei Zusagen in der
Anriss-Tafel decken dasselbe ab, und „15 Jahre" steht als Zahl direkt
darunter.

Sie hat aber die Höhe des Anrisses mitgenommen, und die brauchte zwei
Anläufe. Der Anriss stand auf `min-height: 88svh` und zentrierte seinen
Inhalt darin — solange die Leiste darunter lag, schloss die ihn ab; ohne
sie blieben je 136 px leeres Blau, das unten in das ebenfalls blaue
Sequenzbild überging. Der erste Versuch, `min-height: auto`, nahm den
Freiraum weg, ließ den Anriss dafür schon bei 72 % der Fensterhöhe enden —
die Stadt schob sich mit ins Bild und man sah zwei Abschnitte gleichzeitig.

Jetzt **genau eine Bildschirmhöhe**: `calc(100svh - 68px)`, abzüglich der
Navigationsleiste, die `#hero` als `margin-top` trägt. An neun
Fenstergrößen nachgemessen: von der Sequenz ist bei Scrollstand null
überall **0 px** zu sehen.

Der Platz, der dadurch unten bleibt (bei 1920×1080 sind es 293 px),
bekommt eine Aufgabe statt leer zu stehen: `.hero-weiter` sagt, dass es
weitergeht und wohin. **Mobile first** — am Handy passt der Anriss ohnehin
nicht auf einen Schirm, dort gibt es weder Platz noch Grund dafür; der
Hinweis erscheint erst ab 701 px. Die Sequenz hat außerdem eine feine
Linie oben bekommen, die Kante, die vorher die Leiste gezogen hat.

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

### Die Stadt im Hintergrund

Der Hintergrund war leeres Blau. `marke/bau_stadt.py` legt eine
Silhouette dahinter — **ohne nennenswerte Ladezeit**: kein Bild, sondern
zwei Häuserreihen als je *ein* Pfad plus ein dritter für alle Fenster
zusammen, mit ganzzahligen Koordinaten und relativen Befehlen. 3,4 KB roh,
gemessen **+1,6 KB gzip** an der ganzen Seite (188,8 → 190,4 KB).

Zwei Ebenen ergeben Tiefe: hinten niedriger und heller, vorn höher und
dunkler, Fenster nur in der vorderen Reihe. Der Zufall ist mit festem
Startwert angenagelt, damit jeder Lauf dieselbe Stadt ergibt und der
Wächter im Workflow greift.

**Mobile first**: die Grundregel gilt fürs Handy — feste Bandhöhe von
96 px mit `xMidYMax slice`, die Silhouette wird dort seitlich beschnitten
statt flachgedrückt. Ohne das stünden bei 390 px nur 54 px hohe Klötze da
(Maßstab 0,24 statt 0,44). Erst ab 701 px folgt die Höhe dem
Seitenverhältnis der Zeichnung, dann passt sie ohne Beschnitt.

### Die Figur
Sie kommt aus `marke/bau_mensch.py` und ist eine gezeichnete Comic-Figur
im selben Strich wie die Wagen: gefüllte Fläche, weißer Umriss, runde
Ecken. Die Teile überdecken sich absichtlich — das Hemd liegt über den
Oberarmen, der Kopf über dem Hals —, dadurch entstehen aus einfachen
Formen saubere Außenkonturen ohne eine einzige Hilfslinie.

Davor standen dort zwei Fassungen, die beide verworfen sind:

- **Ein Strichmännchen aus sechs CSS-Kästen.** Sah aus wie ein
  Scherenschnitt.
- **Dasselbe mit Gelenken** — Schulter- und Hüftbalken, zweiteilige Arme
  und Beine, Hände, Füße, Knie die nur nach hinten knicken. Technisch
  richtig, beweglich, und trotzdem sah man ihm die Mechanik an. Bilals
  Urteil dazu steht in der Historie (`ff2eb1e`), damit es niemand noch
  einmal baut.

Die Lehre daraus: eine Figur, die sich bewegen können muss, wird aus
Teilen gebaut, die man einzeln drehen kann — und genau das sieht man ihr
an. Die gezeichnete Figur kann weniger und sieht besser aus.

**Der linke Arm liegt in zwei gezeichneten Stellungen vor**, hängend und
mit erhobenem Handy, und die Seite blendet zwischen ihnen um. Ein starres
Glied zu drehen ginge nicht: den Arm gebeugt vors Gesicht bekommt man nur
mit zwei Gelenken — ein gerader Arm, um die Schulter gedreht, landet mit
der Hand bei x = −11 und damit außerhalb des Bildes. Zwei richtig
gezeichnete Haltungen sind ehrlicher als eine falsche bewegliche.

Die Überblendung läuft über ein schmales Band in der Mitte von `--hoch`
(`clamp(0, (hoch − 0.35) / 0.3, 1)`), nicht über den ganzen Hub. Über den
ganzen Hub sah man beide Arme lange halb durchscheinen — genau das
Geisterbild, das die Sequenz vorher unsauber gemacht hat. So dauert der
Wechsel drei Prozent des Scrollwegs und liest sich als Bewegung.

Das Handy taucht vorher in der hängenden Hand auf (`--tasche`) — das ist
der Griff in die Tasche. Gehen ist eine Wippe: `--gang` hebt und senkt die
Figur um 2,2 % und kippt sie um 1,1°. Ein zweiter Beinsatz wäre teurer
gewesen und hätte bei 90 px Höhe niemand gesehen.

**Maße, die nachgemessen sind und nicht geschätzt:**

- Die Figur ist **1,28-mal so hoch wie ein Wagen** (Wagen 1,45 m, Mensch
  1,75 m wären 1,21 — die 1,28 sind Absicht, sonst verschwindet sie neben
  zwei Limousinen).
- Sie steht bei `top: 73 %`, nicht 80. Bei 80 standen die Füße **77 px
  unter der Radlinie** — die Figur war weit vor dem Wagen, ohne dafür
  größer zu sein. Jetzt sind es 14 px: dieselbe Fahrbahn, eine Spur davor.
- Der Ausstiegsweg ist **18,5 vw**. Nachgemessen von 701 bis 2560 px
  bleibt die Figur überall im Bild, linke Kante nirgends unter 34 px.

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
  Übernehmen. **Wer an der Figur etwas ändert, muss neu messen** — jeder
  Umbau hat den Punkt bisher verschoben: der Wechsel des Armwinkels von
  −58° auf −108°, der Wechsel vom rechten auf den linken Arm (74 px
  daneben), der Wechsel auf die gezeichnete Figur (67/77 px daneben). Das
  Messskript setzt die Mitte des Handys in der Hand auf die Mitte des
  großen Handys; zuletzt −36,2 vw / 7,11 vh am Schreibtisch und
  −35,6 vw / 11,26 vh am Handy, Restversatz 0/0 px.
- **Das Handy hält der linke Arm, nicht der rechte.** Die Figur steht bei
  `z-index: 1` hinter den Wagen. Ein gehobener rechter Arm ragt in den
  Umriss des nahen Wagens — Hand und Handy verschwanden dahinter, sobald
  der Arm hochging. Nach links ist der Weg frei.

Der Übergang zur Seite: der Schirm wächst nur gleichmäßig und kann ein
breites Fenster nie ausfüllen. Deshalb liegt dahinter eine Fläche mit
demselben Verlauf, und der Schirm trägt die **Mittelfarbe** dieses
Verlaufs statt eines eigenen — zwei Verläufe verschiedener Größe treffen
sich am Schirmrand immer sichtbar. Gemessen am größten Farbsprung eines
waagerechten Schnitts: 394 bei `--zoom` 0,30 → 3 bei 0,70.

### Warum das Handy in Endgröße gebaut wird

Rückmeldung: „man sieht nichts auf dem Handy und es sieht unscharf aus."
Zwei getrennte Ursachen.

**Unscharf.** Das Handy war 196 px breit gebaut und wurde per `scale()` auf
das Vierfache gezogen — dazu `will-change: transform`, was die Ebene beim
Compositor festschreibt. Der Browser rastert sie dann einmal und zieht die
Bitmap auf. Jetzt ist es umgekehrt: gebaut in Endgröße (`46vh + 28px`),
`will-change` weg, und der Maßstab ist mit `min(1, …)` bei 1,0 gedeckelt —
**hochskaliert wird nie mehr**. Ehrlich dazu: in Chromium (headless) ließ
sich die Unschärfe nicht nachstellen, dort wird bei jeder Stiländerung neu
gerastert. Die Ursache, die den Effekt auf echter Hardware erzeugt, ist
damit trotzdem weg.

**Man sieht nichts.** Auf dem Schirm standen graue Platzhalterbalken. Sobald
das Handy groß wurde, gab es also nichts zu lesen. Jetzt steht der echte
Anriss darauf: Kopfleiste mit Monogramm, „Ihr Unfall. Ihr Recht.",
Unterzeile, Nummer, vier Leistungen, drei Zusagen, Anrufknopf. Die
Schriftgrößen sind für die Endgröße gesetzt und werden mit dem Rest
heruntergerechnet — nicht umgekehrt.

Die Breite folgt aus der Schirmhöhe: sie ist `(Breite − 28) · 17,5/9`, und
`46vh + 28px` ergibt daraus 89 % der Fensterhöhe. Das Handy sitzt 30 px
unter der Bildmitte, weil die Seite oben ihre Navigationsleiste trägt und
der Kopf des Schirms sonst darunter verschwindet. Nachgemessen bei
1440×900 und 1280×700: der Schirm wird 89 % der Fensterhöhe hoch, bei
390×844 sind es 71 % — der Rest ist die Fläche dahinter.

Die Wagenwege sind auf die **Fahrzeugmitte** bezogen, nicht auf die linke
Kante: `left: 50 %` setzt die linke Kante in die Bildmitte, und genau
dieser Denkfehler hatte den Gegner am Handy aus dem Bild geschoben.
`-96 %` heißt jetzt „rechte Kante an der Bildmitte".

Die vier Sätze stehen auf einem **festen Boden**, nicht auf einem
Prozentwert: die Seite trägt oben eine 68 px hohe Navigationsleiste, und
`top: 9 %` unterschreitet die auf kurzen Fenstern (bei 320×650 waren es
59 px). Auf einem iPhone war die erste Zeile halb verdeckt. Jetzt
`clamp(104px, 12%, 190px)` — nachgemessen bleiben bei jeder geprüften
Größe mindestens 36 px Luft unter der Leiste, auch bei den Höhen, die
Safari mit eingeblendeter Adressleiste übrig lässt. Die Reserve ist
absichtlich größer als nötig: iOS verschiebt beim Ein- und Ausblenden der
Leiste kurz den Anzeigebereich, und ein `sticky`-Element rutscht mit —
das lässt sich hier nicht nachstellen, kostet aber Pixel.

### Der Schirm zieht erst spät auf

Zwei Anläufe, ein Ergebnis. Der erste ließ den Schirm **von Anfang an**
zur Seite werden — Breite und Höhe gerechnet statt `scale()`, das
Seitenverhältnis von 9:17,5 durchgehend auf das des Fensters wandernd.
Technisch sauber, aber die Wachstumsphase davor gefiel besser.

Jetzt beides: bis `--zoom` 0,50 wächst das Handy **als Handy** über den
Maßstab, ab dort übernehmen Breite und Höhe und ziehen den Schirm nach
links und rechts auf, bis er bei 0,86 das Fenster deckt.

```
--f    = clamp(0, (--zoom − 0,50) / 0,36, 1)
Breite = w0 + (100 % − w0) · f
Höhe   = h0 + (100 % − h0) · f
```

Der Maßstab erreicht die 1 genau dort, wo `--f` anfängt — danach ändert
sich nur noch der Kasten, hochskaliert wird nie. `--w0` ist nicht geraten,
sondern aus einer Bedingung abgeleitet: der Kasten sitzt mittig (`top:
50 %` ist nötig, damit er am Ende genau das Fenster deckt), die Seite
trägt oben eine 68 px hohe Leiste, also braucht die größte Handy-Größe
oben und unten je 92 px Rand. Rückwärts über `Höhe = (Breite − 28) ·
17,5/9 + 28` aufgelöst ergibt das `(100vh − 212px) / 1,94444 + 28px`.
Eine geratene vh-Zahl ließ bei 1440×700 einen einzigen Pixel übrig.

Nachgemessen an neun Fenstergrößen von 320×650 bis 1920×1080: überall
mindestens 22 px Luft unter der Leiste, und überall füllt der Schirm am
Ende das Fenster.

Der Scrollweg ist mit dem Aussteigen von 320vh auf **460vh** gewachsen
(am Handy 400vh). Wer `prefers-reduced-motion` gesetzt hat, bekommt kein
Sticky und keinen Scrollweg, sondern das Schlussbild mit allen vier Sätzen
untereinander; Figur und Seitenfläche sind dort ausgeblendet.

## Texte

Die Inhalte stammen aus Nurettins eigenem Entwurf, zuletzt Punkt für Punkt
gegen seine Mail abgeglichen; seine Platzhalter (`01XX-XXXXXXX`, `[Ihre
Telefonnummer]`, `[Ihre E-Mail-Adresse]`) sind mit den echten Daten
gefüllt.

### Die Reihenfolge der Abschnitte
Nurettins Entwurf gibt sie vor, und sie ist verbindlich:

| | Abschnitt | auf der Seite |
|---|---|---|
| — | Banner / Hero | `#hero` |
| — | *(die Unfall-Sequenz — Bilals Zusatz, kein Punkt aus der Mail)* | `#unfall` |
| 1 | Die Expertise — „Meisterhafter Blick. Akademische Präzision." | `#ueber` |
| 2 | Ihre Vorteile — „Warum mein Gutachten den Unterschied macht" | `#warum` |
| 3 | Rechtlicher Schutz — „Ihr gutes Recht bei einem Unfallschaden" | `#ihr-recht` |
| 4 | Leistungen & Region — „Meine Leistungen in Ihrer Region" | `#leistungen` |
| 5 | Kontakt — „Schnelle Hilfe im Schadensfall" | `#kontakt` |
| — | *(Impressum und Datenschutz — Pflicht, kein Punkt aus der Mail)* | `#rechtliches` |

**Die Leistungen standen lange an dritter Stelle**, direkt nach der
Sequenz, und damit vor Expertise, Vorteilen und Recht. Beim Abgleich mit
dem Entwurf ist das aufgefallen: sie gehören dorthin, wo Nurettin sie
hingeschrieben hat — nach der Begründung, nicht davor. Erst wer weiß, wer
da begutachtet und warum das zählt, liest die Liste richtig.

Die Navigation folgt derselben Reihenfolge. **Kontakt bekam dabei einen
eigenen Ton** (Blassblau statt Grau): seit die Leistungen nach hinten
gerückt sind, stießen sonst zwei graue Abschnitte aneinander und lasen
sich als ein einziger langer Block.

Was der Abgleich sonst geändert hat:

| Stelle | vorher | jetzt |
|---|---|---|
| Leistungen | 7 Karten | die **4** aus der Mail |
| „Das sollten Sie wissen:" | fehlte | steht vor den drei Recht-Karten |
| Formular | Vorname + Nachname, E-Mail, Telefon, Kennzeichen, Art des Gutachtens, Nachricht | **Name, Telefonnummer, E-Mail-Adresse, Kennzeichen / Fahrzeug, Ihre Nachricht** |
| Anriss | Verlauf | zusätzlich ein **Hintergrundbild** |

**Die drei gestrichenen Leistungen** (Nutzfahrzeuge & Fuhrpark,
Karosservermessung, Wohnmobil & Wohnwagen) standen nicht in der Mail. Das
betrifft besonders *Nutzfahrzeuge*, die Nurettin zuvor per WhatsApp
ausdrücklich verlangt hatte („Hier gerne noch Nutzfahrzeuge aufnehmen") —
die Mail ist laut Bilal der neuere Stand, deshalb ist sie maßgeblich.
Zurückholen ist eine Zeile.

Der Streifen „Ich begutachte: PKW / Wohnwagen & Wohnmobil / Motorrad /
LKW, Bus & Transporter" ist auf Bilals Hinweis als redundant ebenfalls
entfallen — er wiederholte, was die Leistungskarten und der Abschnitt
„Über mich" ohnehin sagen. Den Abstand zum Verweis auf die Referenzen
hält jetzt der Verweis selbst (40 statt 26 px).

**Ein Satz zu viel** stand im Abschnitt „Die Expertise": „Wenn Sie anrufen,
gehe ich selbst ran." Das ist derselbe Inhalt wie der Vorteil „Direkter
Draht" einen Abschnitt weiter — er ist gestrichen. Ebenso stand im
Anriss-Panel „Ingenieur · Kfz-Sachverständiger" direkt über der Pille
„Kfz-Sachverständiger in Heppenheim"; die Zeile nennt jetzt die
Qualifikation statt noch einmal die Rolle.

**Die Auswahlliste „Art des Gutachtens"** ist mit dem Formular entfallen,
sie stand nicht in der Mail. Die Einwilligung zur Datenverarbeitung steht
weiter darunter — die ist keine Inhaltsfrage, sondern Pflicht.

**Das Hintergrundbild** im Anriss ist die Reflexionsprüfung auf dunklem
Lack (`fotos/anriss_hintergrund.py`), beschnitten so, dass drei Dinge
draußen bleiben: der eingebrannte Zeitstempel, das Herstelleremblem und
eine im Lack gespiegelte Person. Darüber liegt derselbe Verlauf wie zuvor,
nur nicht mehr deckend (0,84/0,78/0,80).

**Entrauschen statt weichzeichnen.** Die erste Fassung hat das Bild mit
einem Gauß von 1,4 weichgezeichnet, um es klein zu bekommen — und genau
das sah dann billig aus: die Streifen wurden zu Matsch. Teuer an dem Foto
ist nicht die Struktur, sondern der Lackflitter und das Sensorrauschen.
Beide sind hochfrequent, unkomprimierbar und unter dem blauen Schleier
ohnehin unsichtbar. Ein Medianfilter nimmt genau die weg und lässt die
Kanten stehen:

| Behandlung | Größe | Aussehen |
|---|---|---|
| ohne alles | 226 KB | scharf |
| Gauß 1,4 (erste Fassung) | 43 KB | matschig |
| Median 7 + 3 | **51 KB** | scharf |

**Zwei Ausschnitte, nicht zwei Größen.** Der Anriss ist am Handy hoch und
schmal, das Bild ein breiter Streifen — mit `cover` wurde die kleine
Fassung dort **6,7-fach** hochskaliert. Das war der eigentliche Grund,
warum es am Handy billig aussah, nicht die Kompression. Jetzt gibt es
einen eigenen, fast quadratischen Ausschnitt (800 × 780, 41 KB), der oben
im Anriss liegt und nach unten in den Grundton ausläuft. Nachgemessen:

| | vorher | jetzt |
|---|---|---|
| 1920 × 1080 @1x | 1,33× | 1,33× |
| 1440 × 900 @2x | 2,19× | 2,19× |
| 430 × 932 @3x | 6,49× | **1,61×** |
| 390 × 844 @3x | 6,68× | **1,46×** |

Der Auslauf ist ein Verlauf über dem Foto, der auf demselben
`--blue-dark` endet, das darunter liegt — deshalb sieht man keine Kante.
Seine Höhe steht als `97,5 vw` da: das ist genau die Höhe, die der
Ausschnitt bei voller Breite einnimmt. Wer den Ausschnitt ändert, muss
diese Zahl mitziehen. Am Schreibtisch fällt die Ebene weg (`none`) —
stehen bleibt sie trotzdem, denn Größen und Positionen werden Ebene für
Ebene zugeordnet, eine fehlende Ebene würde alle folgenden verschieben.

Zwei Textrollen brauchten dadurch mehr Grund: die Blase in der Tafel
bekam einen eigenen dunklen Hintergrund, der WhatsApp-Knopf dunkles statt
hellem Glas (gemessen 4,09 → 7,31).

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

**Die Referenzseite baut ihre Verweise jetzt selbst.** Vorher stand in
`bau_referenzen.py` eine Liste von Hand, welche Sprungziele auf die
Startseite umzuleiten sind — `ihr-recht` kam später dazu, stand nie darin,
und der Verweis lief seitdem ins Leere. Jetzt wird abgeleitet: jeder
Sprung, dessen Ziel es auf der Referenzseite nicht gibt, geht auf die
Startseite. Vor dem Schreiben prüft das Skript zusätzlich, dass kein
Sprung ins Leere zeigt, und bricht sonst ab.

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
