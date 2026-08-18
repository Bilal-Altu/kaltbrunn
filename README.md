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

Marke: das eingedrückte Auto mit den Aufprallstrahlen, im Navigationskopf
klein und im Anriss groß — frei stehend, ohne Stempelring.

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

## Texte

Die Inhalte stammen aus Nurettins eigenem Entwurf (E-Mail vom 18.08.),
seine Platzhalter für Telefon und E-Mail sind mit den echten Daten gefüllt.

Zwei Formulierungen daraus stehen bewusst so da und sollten vor dem
Livegang noch einmal von ihm bestätigt werden:

- **„Meisterhafter Blick"** als Überschrift bei „Über mich". Gemeint ist
  der geschulte Blick, nicht ein Meistertitel — er ist B. Eng., kein
  Handwerksmeister. Missverständlich ist es trotzdem.
- **„Vom Blaumann … bis zum Qualitätsingenieur"** beschreibt den Weg;
  die Tätigkeit beim Hersteller läuft weiter. Seine ursprüngliche
  Alternativ-Überschrift („Vom Premium-Hersteller **zum** unabhängigen
  Gutachter") hätte einen Wechsel behauptet, den es nicht gibt — die ist
  deshalb nicht übernommen.

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
