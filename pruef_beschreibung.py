# -*- coding: utf-8 -*-
import re

LANG = """Ingenieurbüro Kaltbrunn ist das Büro von Nurettin Sogukcesme, freier Kfz-Sachverständiger in Heppenheim. Ich arbeite unabhängig von Versicherungen, im Auftrag von Fahrzeughaltern, Anwälten und Gerichten.

Nach einem Unfall halte ich den Schaden vollständig und neutral fest, ermittle die Ursache und leite die Bewertung nachvollziehbar her. Dazu kommen Wertgutachten für Kauf, Verkauf und Versicherung, technische Analysen bei unklaren Fehlerbildern, Gegengutachten sowie Nutzfahrzeuge und Fuhrparks.

Grundlage: Ausbildung zum Nutzfahrzeug-Mechatroniker, Maschinenbaustudium (B. Eng.), Qualitätsingenieur und Auditor bei einem Premium-Automobilhersteller.

Tätig im Kreis Bergstraße sowie im Rhein-Main- und Rhein-Neckar-Gebiet."""

KURZ = """Ingenieurbüro Kaltbrunn ist das Büro von Nurettin Sogukcesme, freier Kfz-Sachverständiger in Heppenheim. Ich erstelle Schaden- und Wertgutachten für Fahrzeughalter, Anwälte und Gerichte – unabhängig von Versicherungen.

Nach einem Unfall halte ich den Schaden vollständig und neutral fest, ermittle die Ursache und leite die Bewertung nachvollziehbar her. Dazu kommen technische Analysen bei unklaren Fehlerbildern, Gegengutachten sowie Nutzfahrzeuge und Fuhrparks.

Ausbildung zum Nutzfahrzeug-Mechatroniker, Maschinenbaustudium (B. Eng.), Qualitätsingenieur und Auditor bei einem Premium-Automobilhersteller.

Kreis Bergstraße, Rhein-Main- und Rhein-Neckar-Gebiet."""

VERBOTEN = [
    (r'https?://|www\.|\.de\b|\.com\b', 'Link oder Adresse'),
    (r'<[^>]+>', 'HTML'),
    (r'\b\d+\s*%|\bkostenlos\b|\bgratis\b|\bAngebot\b|\bRabatt\b|\bab nur\b|€', 'Preis oder Aktion'),
    (r'\b(beste[rns]?|günstigste[rns]?|Nr\.\s*1)\b', 'Superlativ'),
    (r'[A-ZÄÖÜ]{4,}', 'Versalien'),
    (r'!{2,}|\?{2,}', 'Sonderzeichen gehäuft'),
]

for name, text in (('LANG', LANG), ('KURZ', KURZ)):
    n = len(text)
    n_crlf = len(text.replace('\n', '\r\n'))
    vorschau = text[:250]
    print('=== %s ===' % name)
    print('Zeichen: %d von 750  (%s) · mit CRLF: %d (%s)'
          % (n, 'passt' if n <= 750 else 'ZU LANG',
             n_crlf, 'passt' if n_crlf <= 750 else 'ZU LANG'))
    print('Erste 250 Zeichen (das zeigt Google ohne Aufklappen):')
    print('   ' + vorschau.replace('\n', ' ⏎ ')[:250])
    treffer = []
    for muster, was in VERBOTEN:
        for m in re.finditer(muster, text, re.I if 'Versalien' not in was else 0):
            treffer.append('%s: %r' % (was, m.group(0)))
    print('Regelverstöße:', '; '.join(sorted(set(treffer))) if treffer else 'keine')
    print()
