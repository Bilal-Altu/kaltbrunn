# Hier kommen die Originalaufnahmen hin

Die Fotos aus der Kamera unverändert in diesen Ordner legen und so benennen,
dass die Reihenfolge stimmt, in der sie auf der Referenzseite stehen sollen:

```
01.jpg   BMW X1, Streifschaden über beide Türen
02.jpg   Toyota Corolla Hybrid, Heck links eingedrückt
03.jpg   Toyota Corolla Hybrid, Heckstoßfänger im Detail
04.jpg   Mercedes-Benz E-Klasse, Front links mit Maßstab
05.jpg   BMW, Lackschaden in Nahaufnahme
06.jpg   Audi A5, Front mit Maßstab
07.jpg   Audi A6, Heck rechts
```

Sortiert wird nach Dateinamen — deshalb die führende Null. Groß, unbearbeitet
und im Originalformat ist genau richtig, das Verkleinern übernimmt das Skript.

## Hochladen über GitHub, ohne Werkzeug auf dem Rechner

1. <https://github.com/Bilal-Altu/kaltbrunn/tree/main/fotos/original>
2. **Add file → Upload files**, die sieben Bilder hineinziehen
3. **Commit changes** auf `main`

## Danach

```
python3 fotos/aufbereiten.py    # macht daraus 1600-px-WebP für die Seite
python3 bau_referenzen.py       # setzt sie in referenzen.html
```

Beim Veröffentlichen bleibt dieser Ordner außen vor: der Pages-Workflow kopiert
nur `fotos/*.webp`. Die Originale liegen also im Repo, aber nicht auf der
Website — sie wären mit voller Auflösung und allen Kameradaten sonst öffentlich
abrufbar.
