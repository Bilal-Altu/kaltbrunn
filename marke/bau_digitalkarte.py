#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Die digitale Visitenkarte – ein Bild zum Verschicken, plus eine vCard.

Nurettin hat nachgelegt: gemeint war keine Logodatei, sondern eine
"digitale Visitenkarte", die man im Chat weiterschickt. Seine Beispiele
sind Bilder: Leistungen, Nummer, Webadresse, QR-Code.

Deshalb entstehen hier zwei Dinge, und das zweite ist das wichtigere:

  1. Ein BILD, quadratisch fuer den Chat und hochkant fuer den Status.
     Das ist das, was er gemeint hat.
  2. Eine VCARD (.vcf). Das ist, was eine digitale Visitenkarte
     eigentlich ist: einmal antippen, und der Kontakt steht im
     Adressbuch – mit Nummer, Mail, Webseite und Anschrift. Ein Bild
     kann man nur ansehen, eine vCard speichert sich selbst.

Gesetzt wird in HTML und mit Chromium ausgegeben. Das ist hier richtig
und nicht faul: das Ziel ist ein Bild fuer WhatsApp, kein Druck. Alle
Teile kommen trotzdem aus denselben Quellen wie alles andere – die
Zeichen aus marke/logo/, die Symbole aus marke/symbole/, die Schrift aus
index.html, der QR-Code aus bau_karte_nuri.

Die Leistungen stehen so auf der Seite. Wer sie hier aendert, ohne sie
dort zu aendern, erzeugt zwei Wahrheiten – deshalb werden sie aus
index.html gelesen und nicht abgetippt.

    python3 bau_digitalkarte.py
"""
import io
import os
import re
import subprocess

import bau_logo as L
import bau_karte_nuri as K

HIER = os.path.dirname(os.path.abspath(__file__))
AUS = os.path.join(HIER, 'logo')
SEITE = os.path.join(HIER, os.pardir, 'index.html')
CHROM = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'
NODE_PW = '/opt/node22/lib/node_modules/playwright'

GRUEN = '#25d366'

# Zwei Fassungen, dunkel und hell. Der Unterschied ist nicht nur die
# Grundfarbe: auf Dunkel muss das Blau heller stehen (#003da5 kommt auf
# #171d29 nur auf Kontrast 1,78 und ist dort praktisch unsichtbar), und
# auf Hell faellt die weisse Kachel unter dem QR-Code weg, weil sie auf
# weissem Grund nichts mehr abgrenzt. Alle Werte gegen ihren Grund
# nachgemessen, nichts darunter liegt unter 4,5.
TOENE = {
    'dunkel': dict(grund='#171d29', zeichen='karte-bild-web-dunkel',
                   stark='#ffffff', blau='#4d8bf5', satz='#e6e8ec',
                   matt='#9ca2aa', strich='#ffffff', strich_kraft='0.16',
                   kachel='#ffffff', kachel_text='#171d29', kachel_rund=True),
    'hell':   dict(grund='#ffffff', zeichen='karte-bild-web-hell',
                   stark='#15171a', blau='#003da5', satz='#15171a',
                   matt='#5d6470', strich='#15171a', strich_kraft='0.14',
                   kachel='transparent', kachel_text='#15171a',
                   kachel_rund=False),
}

NAME = 'Nurettin Sogukcesme'
ROLLE = 'Maschinenbau-Ing. – Fahrzeugtechnik (B. Eng.)'
CLAIM = 'Kfz-Gutachten mit Sachverstand'

FORMATE = [('quadrat', 1080, 1080), ('status', 1080, 1920)]


def leistungen():
    """Die Ueberschriften aus dem Abschnitt Leistungen der Seite."""
    s = io.open(SEITE, encoding='utf-8').read()
    teil = re.search(r'id="leistungen".*?</section>', s, re.S)
    if not teil:
        raise SystemExit('Abschnitt "leistungen" nicht in index.html gefunden')
    namen = [re.sub(r'<[^>]+>', '', h).strip()
             for h in re.findall(r'<h3[^>]*>(.*?)</h3>', teil.group(0), re.S)]
    namen = [n.replace('&amp;', '&') for n in namen]
    if not namen:
        raise SystemExit('Keine Leistungen in index.html gefunden')
    return namen


def schrift():
    s = io.open(SEITE, encoding='utf-8').read()
    m = re.search(r"@font-face\{font-family:'([^']+)'.*?(base64,[A-Za-z0-9+/=]+)\)",
                  s, re.S)
    if not m:
        raise SystemExit('Keine eingebettete Schrift in index.html gefunden')
    return m.group(1), m.group(2)


def sinnbild(name, farbe, kante):
    roh = io.open(os.path.join(HIER, 'symbole', 'lucide-%s.svg' % name),
                  encoding='utf-8').read()
    return ('<svg viewBox="0 0 24 24" width="%d" height="%d" fill="none" '
            'stroke="%s" stroke-width="2" stroke-linecap="round" '
            'stroke-linejoin="round">%s</svg>'
            % (kante, kante, farbe, K.inhalt(roh)))


def wa_punkt(kante):
    """Das WhatsApp-Zeichen als gruener Kreis mit weisser Kurve.

    Vorher stand hier nur ein gruener Punkt. Gruen allein ist kein
    Zeichen – man erkennt WhatsApp an der Sprechblase, nicht an der
    Farbe.
    """
    roh = io.open(os.path.join(HIER, 'whatsapp.svg'), encoding='utf-8').read()
    kurve = re.search(r'<path[^>]*\bd="([^"]+)"', roh).group(1)
    return ('<svg class="wa" viewBox="0 0 24 24" width="%d" height="%d">'
            '<circle cx="12" cy="12" r="12" fill="%s"/>'
            '<g transform="translate(4.8,4.8) scale(0.6)">'
            '<path d="%s" fill="#ffffff"/></g></svg>'
            % (kante, kante, GRUEN, kurve))


def zeichen(name, hoehe_px):
    svg = io.open(os.path.join(AUS, name + '.svg'), encoding='utf-8').read()
    vb = L.viewbox(svg)
    rand = (L.RAND * 0.7 if name.startswith('karte-marke') else L.RAND)
    s = hoehe_px / (vb[3] - 2 * rand)
    return ('<svg viewBox="%.2f %.2f %.2f %.2f" width="%.1f" height="%.1f">%s</svg>'
            % (rand, rand, vb[2] - 2 * rand, vb[3] - 2 * rand,
               (vb[2] - 2 * rand) * s, hoehe_px, L.inneres(svg)))


def qr(kante_px):
    """Derselbe gestaltete Code wie auf der Visitenkarte."""
    pfad, _, _ = K.qr_marke(kante_px, kante_px, kante_px)
    return ('<svg viewBox="0 0 %d %d" width="%d" height="%d">%s</svg>'
            % (kante_px, kante_px, kante_px, kante_px, pfad))


def seite(breite, hoehe, hoch, ton):
    familie, daten = schrift()
    # Skaliert wird ueber die BREITE, nicht ueber die Hoehe. Beide Formate
    # sind 1080 breit; haengt die Schrift an der Hoehe, wird sie im
    # Hochformat 1,78-mal so gross und laeuft seitlich heraus. Genau das
    # ist passiert. Die zusaetzliche Hoehe wird zu Luft, nicht zu Schrift.
    e = breite / 1080.0
    # Im Hochformat darf die Schrift etwas groesser stehen – aber ueber
    # einen eigenen Faktor, nicht ueber die Hoehe. 1,28 ist der Wert, bei
    # dem die laengste Zeile (die Anschrift) noch in die Breite passt;
    # nachgerechnet, nicht geraten.
    schrift_e = e * (1.28 if hoch else 1.0)
    posten = ''.join(
        '<li>%s<span>%s</span></li>' % (sinnbild('check', ton['blau'], int(26 * schrift_e)), n)
        for n in leistungen())
    # Die Anschrift steht auf zwei Zeilen, nicht in einer langen. In einer
    # Zeile bricht sie neben dem QR-Code irgendwo um – "64646" oben,
    # "Heppenheim" unten. Wo umbrochen wird, entscheidet dann der
    # Zeilenfall und nicht die Anschrift.
    kontakt = ''.join(
        '<li>%s<span%s>%s</span>%s</li>'
        % (sinnbild(z, ton['blau'], int(30 * schrift_e)), ' class="stark"' if b else '',
           text, (wa_punkt(int(30 * schrift_e)) if w else ''))
        for z, text, b, w in ([('smartphone', K.TELEFON, True, True),
                               ('mail', K.MAIL, False, False),
                               ('globe', K.WEB, False, False)]
                              # Die Anschrift nur im Hochformat. Im Quadrat
                              # ist der Platz nach dem Zeichen mit Wagen
                              # weg, und sie ist die Angabe, die am
                              # wenigsten fehlt: wer anruft oder schreibt,
                              # braucht sie nicht, und in der vCard steht
                              # sie ohnehin.
                              + ([('house', '%s<br>%s' % (K.STRASSE, K.ORT),
                                   False, False)] if hoch else [])))
    css = """
      *{margin:0;padding:0;box-sizing:border-box}
      @font-face{font-family:'%(fam)s';font-style:normal;font-weight:300 900;
                 src:url(data:font/woff2;%(daten)s) format('woff2')}
      body{width:%(b)dpx;height:%(h)dpx;background:%(grund)s;color:%(stark)s;
           font-family:'%(fam)s',system-ui,sans-serif;overflow:hidden;
           display:flex;flex-direction:column;
           padding:%(rand).1fpx %(seit).1fpx;gap:%(spalt).1fpx}
      .band{align-self:flex-start}
      .wer{display:flex;flex-direction:column;gap:%(mini).1fpx}
      .name{font-size:%(gross).1fpx;font-weight:800;letter-spacing:-0.02em;line-height:1.05}
      .rolle{font-size:%(klein).1fpx;font-weight:500;color:%(blau)s}
      .claim{font-size:%(mittel).1fpx;font-weight:600;color:%(stark)s;line-height:1.2}
      hr{border:0;height:2px;background:%(strich)s;opacity:%(kraft)s;flex:none}
      ul{list-style:none;display:flex;flex-direction:column;gap:%(luft).1fpx}
      /* Die Leistungen fangen den uebrigen Platz auf. Sonst steht das
         Loch zwischen ihnen und dem Kontaktblock, und das sieht aus, als
         haette jemand vergessen, etwas hineinzuschreiben. */
      .leistungen{flex:1;justify-content:center}
      li{display:flex;align-items:center;gap:%(mini).1fpx;
         font-size:%(klein).1fpx;color:%(matt)s;line-height:1.3}
      li svg{flex:none}
      .leistungen li{font-weight:500;color:%(satz)s}
      .kontakt li .stark{font-weight:700;color:%(stark)s}
      .wa{margin-left:%(mini2).1fpx;flex:none}
      .fuss{display:flex;align-items:center;
            gap:%(spalt).1fpx;justify-content:space-between}
      .code{background:%(kachel)s;border-radius:%(rund).1fpx;padding:%(pad).1fpx;
            display:flex;flex-direction:column;align-items:center;gap:%(mini2).1fpx}
      .code small{font-size:%(winz).1fpx;font-weight:700;color:%(kachel_text)s;
                  letter-spacing:0.04em}
    """ % dict(fam=familie, daten=daten, b=breite, h=hoehe,
               grund=ton['grund'], stark=ton['stark'], blau=ton['blau'],
               satz=ton['satz'], matt=ton['matt'], strich=ton['strich'],
               kraft=ton['strich_kraft'], kachel=ton['kachel'],
               kachel_text=ton['kachel_text'],
               gruen=GRUEN,
               rand=(110 if hoch else 68) * e, seit=72 * e,
               spalt=(50 if hoch else 18) * e, luft=(32 if hoch else 15) * e,
               mini=18 * schrift_e, mini2=10 * schrift_e,
               gross=(52 if hoch else 46) * schrift_e, mittel=(40 if hoch else 36) * schrift_e,
               klein=28 * schrift_e, winz=19 * schrift_e,
               wa=24 * e, rund=(22 if ton['kachel_rund'] else 0) * schrift_e,
               pad=(22 if ton['kachel_rund'] else 0) * schrift_e)

    leib = ('<div class="band">%s</div>'
            '<div class="wer"><div class="name">%s</div>'
            '<div class="rolle">%s</div></div>'
            '<div class="claim">%s</div><hr>'
            '<ul class="leistungen">%s</ul><hr>'
            '<div class="fuss"><ul class="kontakt">%s</ul>'
            '<div class="code">%s<small>WHATSAPP</small></div></div>'
            % (zeichen(ton['zeichen'],
                       (200 if hoch else 152) * schrift_e),
               NAME, ROLLE, CLAIM, posten, kontakt,
               qr(int(212 * schrift_e))))
    return ('<!doctype html><html lang="de"><head><meta charset="utf-8">'
            '<title>Ingenieurbüro Kaltbrunn</title><style>%s</style></head>'
            '<body>%s</body></html>' % (css, leib))


def ausgeben():
    auftrag = []
    for tonname, ton in TOENE.items():
        for name, b, h in FORMATE:
            marke = '%s-%s' % (name, tonname)
            quelle = os.path.join(AUS, '.digital-%s.html' % marke)
            io.open(quelle, 'w', encoding='utf-8').write(seite(b, h, h > b, ton))
            auftrag.append([quelle,
                            os.path.join(AUS, 'Digitale-Visitenkarte-%s.png'
                                         % marke), b, h])
    skript = """
const { chromium } = require('%s');
const auftrag = %s;
(async()=>{
  const b = await chromium.launch({executablePath:'%s'});
  for (const [q, z, br, ho] of auftrag) {
    const p = await b.newPage({viewport:{width:br,height:ho}});
    await p.goto('file://' + q);
    await p.evaluate(()=>document.fonts.ready);
    await p.waitForTimeout(350);
    await p.screenshot({path:z});
    await p.close();
  }
  await b.close();
})();
""" % (NODE_PW, repr(auftrag).replace("'", '"'), CHROM)
    lauf = os.path.join(AUS, '.digital.js')
    io.open(lauf, 'w', encoding='utf-8').write(skript)
    subprocess.run(['node', lauf], check=True)
    os.remove(lauf)
    for q, _, _, _ in auftrag:
        os.remove(q)
    return [z for _, z, _, _ in auftrag]


def vcard():
    """Die eigentliche digitale Visitenkarte: einmal antippen, gespeichert.

    vCard 3.0, nicht 4.0 – 3.0 verstehen iOS, Android und Outlook ohne
    Ausnahme, bei 4.0 faellt je nach Geraet die Haelfte unter den Tisch.
    Zeilenende ist CRLF, so steht es in RFC 6350.
    """
    vor, nach = NAME.split(' ', 1)[1], NAME.split(' ', 1)[0]
    zeilen = [
        'BEGIN:VCARD', 'VERSION:3.0',
        'N:%s;%s;;;' % (vor, nach),
        'FN:%s' % NAME,
        'ORG:Ingenieurbüro Kaltbrunn',
        'TITLE:Maschinenbau-Ing. – Fahrzeugtechnik (B. Eng.)',
        'TEL;TYPE=CELL,VOICE:%s' % K.TELEFON,
        'EMAIL;TYPE=INTERNET,WORK:%s' % K.MAIL,
        'URL:https://%s' % K.WEB,
        'ADR;TYPE=WORK:;;%s;%s;;%s;Deutschland'
        % (K.STRASSE, K.ORT.split(' ', 1)[1], K.ORT.split(' ', 1)[0]),
        'NOTE:Kfz-Gutachten mit Sachverstand. WhatsApp: %s' % K.WHATSAPP,
        'END:VCARD',
    ]
    ziel = os.path.join(AUS, 'Nurettin-Sogukcesme.vcf')
    io.open(ziel, 'w', encoding='utf-8', newline='').write(
        '\r\n'.join(zeilen) + '\r\n')
    return ziel


if __name__ == '__main__':
    for z in ausgeben():
        print('  marke/logo/%-38s %6.1f KB' % (os.path.basename(z),
                                               os.path.getsize(z) / 1024))
    z = vcard()
    print('  marke/logo/%-38s %6.1f KB' % (os.path.basename(z),
                                           os.path.getsize(z) / 1024))
