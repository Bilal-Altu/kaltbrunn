# Ingenieurbüro Kaltbrunn — Website

Kfz-Gutachten mit Sachverstand · Heppenheim, Kreis Bergstraße

Drei Fassungen derselben Seite, damit die Gestaltung am fertigen Objekt
entschieden wird und nicht am Einzelbild.

| Datei | Fassung | Marke |
|---|---|---|
| `index.html` | Tiefschwarz, reduziert | **4b** „Die stille Wortmarke“ — kein Signet, Gewichtskontrast |
| `index-tuev.html` | Prüfblau | **4a** „Das Winkelzeichen“ — rechter Winkel mit Punkt |
| `index-klassisch.html` | Ursprungsentwurf, Kräftigblau | **4c** „Das Prüfsiegel“ — Ring mit IK und Punkt |

Jede Fassung ist **eine einzige Datei ohne jede externe Verbindung**. Schriften,
Bilder und Skripte stecken als Data-URI darin: keine Google Fonts, keine Cookies,
kein Tracking. Damit entfällt der DSGVO-Klassiker „IP-Adresse an Google
übertragen“ — und die Seite lädt in einem einzigen Request.

| | index | blau | klassisch |
|---|---|---|---|
| Größe | 352 KB | 355 KB | 291 KB |
| Requests | 1 | 1 | 1 |
| externe Verbindungen | 0 | 0 | 0 |

## Vorschau

Der Pages-Workflow veröffentlicht bei jedem Push auf `main` alle drei:

* `/` — Tiefschwarz
* `/blau/` — Prüfblau
* `/klassisch/` — Ursprungsentwurf

`robots.txt` sperrt diese Adresse für Suchmaschinen, damit sie der späteren
echten Domain keine doppelten Inhalte macht. Vor dem Livegang unter eigener
Domain muss die Datei weg.

Lokal genügt ein Doppelklick auf die HTML-Datei — mangels relativer Pfade
verhält sie sich genauso wie über einen Server. Wer trotzdem einen will:

```
python -m http.server 4599
```

## Bearbeiten

`index.html` und `index-tuev.html` werden **gebaut**, nicht von Hand bearbeitet —
sie enthalten lange Base64-Blöcke. Quellen liegen in `src/`:

```
cd src
python3 build.py ../index.html            # Tiefschwarz
python3 build.py ../index-tuev.html tuev  # Prüfblau
```

| Datei | Inhalt |
|---|---|
| `src/part1_head.html` | Meta-Tags und das komplette CSS |
| `src/part2_body.html` | Markup aller Abschnitte inkl. Impressum und Datenschutz |
| `src/part3_script.html` | JSON-LD (LocalBusiness, Person, FAQ) und das JavaScript |
| `src/theme-tuev.css` | Farbvariante: überschreibt ausschließlich Farb-Token |
| `src/brand-*-nav.html`, `src/brand-*-foot.html` | Marke je Fassung |
| `src/*.woff2` | Schibsted Grotesk + Instrument Serif, latin (SIL OFL) |
| `src/*.webp` | Porträt freigestellt, Porträtausschnitt, Wappen Heppenheim |

Ein anderer Blauton ist eine Änderung an zwei Zeilen (`--brand`, `--brand-deep`
in `theme-tuev.css`). Eine weitere Farbfassung ist eine neue `theme-<name>.css`
plus ein Eintrag in `BRANDS` in `build.py`.

`index-klassisch.html` steht bewusst außerhalb des Build-Systems: eigener
Aufbau, eigene Schriften (Roboto), eine einzelne Datei, die direkt bearbeitet
wird.

## Vor dem Livegang

- [ ] **Impressum**: USt-IdNr. (§ 27a UStG) und Berufshaftpflichtversicherung
      ergänzen — Platzhalter-Kommentar steht in `src/part2_body.html`
- [ ] **Domain und E-Mail** stehen noch auf `ing-nuri.de` (canonical, og:url,
      JSON-LD, Formular, Footer) — bei neuer Domain überall nachziehen
- [ ] **Öffnungszeiten**: sichtbar stehen keine mehr auf der Seite, im JSON-LD
      aber weiterhin Mo–Fr 8–18 Uhr. Entweder bestätigen oder dort streichen
- [ ] **„Besichtigung meist innerhalb von 24 Stunden“** (Anriss und Fragen) mit
      der hauptberuflichen Tätigkeit abgleichen — ein Versprechen, das nicht
      hält, kostet mehr Vertrauen als es bringt
- [ ] **`robots.txt` entfernen**, sobald die Seite unter eigener Domain läuft
- [ ] Der **Arbeitgeber** ist bewusst nicht namentlich genannt, sondern als
      „Nutzfahrzeughersteller“ umschrieben

## Geprüft

Chromium, 360 / 390 / 820 / 1280 / 1440 px: keine JS-Fehler, kein horizontaler
Überlauf, keine doppelten IDs, keine toten Sprungziele, saubere
Überschriften-Reihenfolge, alle Bilder mit Alt-Text und festen Maßen,
alle Formularfelder beschriftet, `main`-Landmarke und Sprungmarke vorhanden,
gültiges JSON-LD. Alle geprüften Textrollen erreichen WCAG AA.
