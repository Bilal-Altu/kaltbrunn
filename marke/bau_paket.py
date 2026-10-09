#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Packt die Visitenkarte so zusammen, dass man sie weiterschicken kann.

Das Problem, das dieses Skript loest, ist kein technisches:

  * SVG ist ein Web-Format. Wer eine SVG doppelklickt, bekommt den
    Browser zu sehen – das sieht aus, als sei eine Webseite daraus
    geworden. Ist es nicht, die Datei ist in Ordnung, der Browser ist nur
    das Programm, das SVG anzeigen kann.
  * WhatsApp kennt SVG nicht. Je nach Geraet wird die Datei abgelehnt,
    umbenannt oder als Text verschickt. Per E-Mail geht sie durch.
  * Nurettin braucht die SVG gar nicht. Fuer ihn ist das PDF richtig: es
    oeffnet sich auf jedem Geraet und ist dieselbe Zeichnung.

Deshalb liegt im Paket beides, dazu zwei PNG zum schnellen Anschauen und
ein LIESMICH, das in zwei Saetzen sagt, welche Datei wofuer ist. Das ZIP
kann man am Stueck weiterleiten, ohne dass unterwegs etwas umgewandelt
wird.

    python3 bau_paket.py
"""
import io
import os
import subprocess
import zipfile

import bau_karte_nuri as K

HIER = os.path.dirname(os.path.abspath(__file__))
LOGO = os.path.join(HIER, 'logo')
ZIEL = os.path.join(LOGO, 'Visitenkarte-Kaltbrunn.zip')

# (Datei im Ordner, Name im ZIP)
STUECKE = [
    ('Visitenkarte-Nuri-Druck.pdf', 'Visitenkarte-Druck.pdf'),
    ('Visitenkarte-Nuri-Vorderseite.svg', 'Vektor/Vorderseite.svg'),
    ('Visitenkarte-Nuri-Rueckseite.svg', 'Vektor/Rueckseite.svg'),
]

LIESMICH = """Visitenkarte Ingenieurbüro Kaltbrunn
====================================

Welche Datei wofür:

  Visitenkarte-Druck.pdf
      Die Datei für die Druckerei. Zwei Seiten, 91 x 61 mm.
      Das sind 85 x 55 mm Endformat plus 3 mm Anschnitt ringsum.
      Zum Anschauen reicht sie auch - sie öffnet sich auf jedem Gerät.

  Vorschau/Vorderseite.png, Vorschau/Rueckseite.png
      Nur zum Anschauen, zum Beispiel am Telefon. Nicht zum Drucken.

  Vektor/Vorderseite.svg, Vektor/Rueckseite.svg
      Dieselbe Zeichnung als Vektordatei, falls die Druckerei oder ein
      Werbetechniker einzelne Teile herauslösen will.
      SVG ist ein Web-Format: wer sie doppelklickt, bekommt den Browser
      zu sehen. Das ist richtig so, die Datei ist in Ordnung.

Für den Druck:

  Die Dateien sind RGB. Die Druckerei wandelt nach FOGRA51
  (PSO Coated v3) bei gestrichenem Papier, FOGRA52 bei ungestrichenem.

  Farben als Referenz:
      Marke          #003DA5
      Marke tief     #002A73
      Text           #15171A
      Text gedämpft  #5D6470
      WhatsApp-Grün  #25D366   (nur das Zeichen im QR-Code)

  Es ist keine Schrift im Dokument, alles ist in Kurven umgewandelt.
  Es ist auch kein Bild im Dokument, auch der QR-Code nicht.

Vor dem Druck bitte bestätigen:

  Die Karte steht auf ing-kaltbrunn.de. Solange die Domain nicht
  endgültig ist, nicht drucken - ein falscher Aufdruck kostet die ganze
  Auflage, nicht eine Datei.

Der QR-Code führt auf das WhatsApp-Unternehmenskonto.
"""


def vorschau():
    """Zwei PNG, 300 dpi, zum Anschauen am Telefon."""
    skript = """
const { chromium } = require('%s');
(async()=>{
  const b = await chromium.launch({executablePath:'%s'});
  for (const [q, z] of %s) {
    const p = await b.newPage({viewport:{width:400,height:300},
                               deviceScaleFactor:%f});
    await p.goto('file://' + q);
    await p.waitForTimeout(250);
    await (await p.$('svg')).screenshot({path: z});
    await p.close();
  }
  await b.close();
})();
""" % (K.NODE_PW if hasattr(K, 'NODE_PW') else '/opt/node22/lib/node_modules/playwright',
       '/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
       str([[os.path.join(LOGO, 'Visitenkarte-Nuri-%s.svg' % a),
             os.path.join(LOGO, '.vorschau-%s.png' % b)]
            for a, b in (('Vorderseite', 'vorn'), ('Rueckseite', 'hinten'))]),
       300.0 / 96.0)
    lauf = os.path.join(LOGO, '.vorschau.js')
    io.open(lauf, 'w', encoding='utf-8').write(skript)
    subprocess.run(['node', lauf], check=True)
    os.remove(lauf)
    return [(os.path.join(LOGO, '.vorschau-vorn.png'), 'Vorschau/Vorderseite.png'),
            (os.path.join(LOGO, '.vorschau-hinten.png'), 'Vorschau/Rueckseite.png')]


if __name__ == '__main__':
    bilder = vorschau()
    with zipfile.ZipFile(ZIEL, 'w', zipfile.ZIP_DEFLATED) as z:
        for datei, name in STUECKE:
            z.write(os.path.join(LOGO, datei), name)
        for datei, name in bilder:
            z.write(datei, name)
        # Windows liest .txt nur mit CRLF sauber.
        z.writestr('LIESMICH.txt', LIESMICH.replace('\n', '\r\n'))
    for datei, _ in bilder:
        os.remove(datei)
    print('  marke/logo/%s  %.1f KB' % (os.path.basename(ZIEL),
                                        os.path.getsize(ZIEL) / 1024))
    with zipfile.ZipFile(ZIEL) as z:
        for i in z.infolist():
            print('    %-30s %7.1f KB' % (i.filename, i.file_size / 1024))
