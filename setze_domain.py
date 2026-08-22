#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Setzt Domain und E-Mail-Adresse an allen Stellen der Seite.

Die Domain steht an 16 Stellen in index.html: siebenmal als reine
Adresse (canonical, og:url, viermal als @id/url im JSON-LD) und neunmal
als Teil der E-Mail (Kontaktzeile, Impressum, Datenschutz, Fußzeile,
JSON-LD und das mailto des Formularskripts – teils zweimal pro Zeile,
einmal im href und einmal im sichtbaren Text). Von Hand ist das eine
Suchaktion, bei der zuverlässig eine Stelle liegen bleibt; deshalb
dieses Skript.

    python3 setze_domain.py neue-domain.de
    python3 setze_domain.py neue-domain.de info@neue-domain.de

Ohne zweites Argument wird der lokale Teil der E-Mail behalten
(info@alt.de → info@neu.de). Danach einmal

    python3 bau_referenzen.py

laufen lassen, damit die Referenzseite nachzieht.

Das Skript zählt vorher, wie viele Stellen es erwartet, und bricht ab,
wenn es weniger findet – lieber gar nicht als halb umgestellt.
"""
import io
import os
import re
import sys

HIER = os.path.dirname(os.path.abspath(__file__))
ZIEL = os.path.join(HIER, 'index.html')


def domain_und_mail(text):
    """Liest die aktuell gesetzte Domain und E-Mail aus der Datei."""
    m = re.search(r'<link rel="canonical" href="https://(?:www\.)?([^/"]+)/', text)
    if not m:
        raise SystemExit('canonical nicht gefunden – ist das die richtige Datei?')
    p = re.search(r'mailto:([^"?@]+)@([^"?]+)', text)
    if not p:
        raise SystemExit('mailto nicht gefunden')
    return m.group(1), p.group(1), p.group(2)


def setzen(neu_domain, neu_mail=None):
    s = io.open(ZIEL, encoding='utf-8').read()
    alt_domain, mail_lokal, alt_mail_domain = domain_und_mail(s)

    if neu_mail:
        if '@' not in neu_mail:
            raise SystemExit('zweite Angabe muss eine E-Mail-Adresse sein')
        neu_lokal, neu_mail_domain = neu_mail.split('@', 1)
    else:
        neu_lokal, neu_mail_domain = mail_lokal, neu_domain

    vorher_domain = s.count(alt_domain)
    vorher_mail = s.count('%s@%s' % (mail_lokal, alt_mail_domain))
    if vorher_domain < 16:
        raise SystemExit('nur %d Domain-Stellen gefunden, erwartet mindestens 16 – '
                         'Abbruch, damit nichts halb umgestellt wird' % vorher_domain)

    s = s.replace('%s@%s' % (mail_lokal, alt_mail_domain),
                  '%s@%s' % (neu_lokal, neu_mail_domain))
    s = s.replace(alt_domain, neu_domain)

    if alt_domain in s:
        raise SystemExit('nach dem Ersetzen steht die alte Domain noch drin')
    io.open(ZIEL, 'w', encoding='utf-8').write(s)
    return alt_domain, neu_domain, vorher_domain, vorher_mail


if __name__ == '__main__':
    if not 2 <= len(sys.argv) <= 3:
        raise SystemExit(__doc__)
    alt, neu, n_dom, n_mail = setzen(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
    print('%s → %s: %d Domain-Stellen, %d E-Mail-Stellen ersetzt.'
          % (alt, neu, n_dom, n_mail))
    print('Jetzt noch: python3 bau_referenzen.py')
