#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Baut referenzen.html aus index.html.

Kopf, Schrift, Navigation, Fußzeile und Skripte werden übernommen, damit
die beiden Seiten nicht auseinanderlaufen. Neu ist nur der Inhalt zwischen
<main> und </main> sowie ein Block Bildergalerie-CSS.

    python3 bau_referenzen.py

Die Fotos liegen als Dateien unter fotos/ und werden ganz normal verlinkt,
nicht als Data-URI eingebettet: eigene Adresse, kein Fremdanbieter, also
DSGVO-seitig unbedenklich – und der Browser lädt sie erst, wenn sie
gebraucht werden.
"""
import io
import os
import re
import sys

HIER = os.path.dirname(os.path.abspath(__file__))
QUELLE = os.path.join(HIER, 'index.html')
ZIEL = os.path.join(HIER, 'referenzen.html')

# ── Die Fälle ─────────────────────────────────────────────────────────────
# datei, Fahrzeug, Schadenbild, Aufnahme, ausfuehrlich
FAELLE = [
    ('01-bmw-x1-streifschaden.webp', 'BMW X1',
     'Streifschaden über beide Türen', 'Februar 2026',
     'Langgezogener Streifschaden über hintere Tür, Schweller und Seitenwand. '
     'Der Maßstab im Bild hält die Höhe über der Fahrbahn fest – daraus lässt '
     'sich später ableiten, welches Fahrzeug den Schaden verursacht haben kann.'),
    ('02-toyota-corolla-heck-links.webp', 'Toyota Corolla Hybrid',
     'Heck links eingedrückt', 'Januar 2025',
     'Stoßfänger gerissen, Seitenwand eingedrückt, Radlauf verformt. '
     'Sichtbar sind auch die Folgen für die dahinterliegenden Halter – bei '
     'solchen Schäden entscheidet die verdeckte Struktur über die Reparaturkosten.'),
    ('03-toyota-corolla-heck-detail.webp', 'Toyota Corolla Hybrid',
     'Heckstoßfänger, Detailaufnahme', 'August 2024',
     'Detail derselben Schadenart aus einem anderen Fall: Stoßfänger großflächig '
     'eingedrückt und aufgerissen. Kunststoff federt zurück – ohne Aufnahme im '
     'unbelasteten Zustand lässt sich die Tiefe später nicht mehr belegen.'),
    ('04-mercedes-e-front-links.webp', 'Mercedes-Benz E-Klasse',
     'Front links, Vermessung vor Ort', 'Juli 2025',
     'Aufnahme der Fahrzeugecke mit Maßstab, direkt am Unfallort in der Engstelle. '
     'Die Höhe über der Fahrbahn ist festgehalten, bevor das Fahrzeug bewegt wird – '
     'danach lässt sie sich nicht mehr sauber ermitteln.'),
    ('05-bmw-lack-detail.webp', 'BMW',
     'Delle im Reflexionsstreifen', 'Mai 2025',
     'Eine flache Delle sieht man auf dunklem Lack mit bloßem Auge kaum. Im '
     'gespiegelten Streifenmuster verzieht sie sich zum Wirbel und ist damit '
     'belegt – dieselbe Technik, mit der in der Fertigung Oberflächen geprüft werden.'),
    ('06-audi-a5-front.webp', 'Audi A5',
     'Front, Aufnahme mit Maßstab', 'Juli 2024',
     'Dokumentation der Fahrzeugfront mit Maßstab. Auch ohne sichtbare '
     'Verformung gehört die Aufnahme dazu: Sie belegt den Zustand zum '
     'Zeitpunkt der Besichtigung.'),
    ('07-audi-a6-heck-rechts.webp', 'Audi A6',
     'Heck rechts, Streif- und Druckschaden', 'Juni 2024',
     'Streifspuren über Stoßfänger und Seitenwand mit leichter Verformung. '
     'Helle Lackierungen zeigen Fremdlackantrag besonders deutlich – ein '
     'Hinweis auf das verursachende Fahrzeug.'),
]


def fehler(text):
    sys.stderr.write('FEHLER: %s\n' % text)
    sys.exit(1)


def main():
    s = io.open(QUELLE, encoding='utf-8').read()

    # ── Kopf umschreiben ──────────────────────────────────────────────────
    titel = 'Referenzen – Ingenieurbüro Kaltbrunn | Kfz-Gutachten Heppenheim'
    beschr = ('Aufnahmen aus meiner Gutachtertätigkeit: Unfall- und Lackschäden an '
              'PKW im Kreis Bergstraße, dokumentiert mit Maßstab und in '
              'gerichtsverwertbarer Form.')
    s = re.sub(r'<title>.*?</title>', '<title>%s</title>' % titel, s, count=1)
    s = re.sub(r'<meta name="description" content="[^"]*"/>',
               '<meta name="description" content="%s"/>' % beschr, s, count=1)
    s = s.replace('<link rel="canonical" href="https://www.ing-nuri.de/"/>',
                  '<link rel="canonical" href="https://www.ing-nuri.de/referenzen.html"/>')
    s = s.replace('<meta property="og:url" content="https://www.ing-nuri.de/"/>',
                  '<meta property="og:url" content="https://www.ing-nuri.de/referenzen.html"/>')
    s = re.sub(r'<meta property="og:title" content="[^"]*"/>',
               '<meta property="og:title" content="Referenzen – Ingenieurbüro Kaltbrunn"/>', s, count=1)
    s = re.sub(r'<meta property="og:description" content="[^"]*"/>',
               '<meta property="og:description" content="%s"/>' % beschr, s, count=1)

    # ── Galerie-CSS ans Ende des Stilblocks ───────────────────────────────
    if '  </style>' not in s:
        fehler('Stilblock nicht gefunden')
    s = s.replace('  </style>', GALERIE_CSS + '  </style>', 1)

    # ── Inhalt austauschen ────────────────────────────────────────────────
    m = re.search(r'<main id="main">.*?</main>', s, re.S)
    if not m:
        fehler('<main> nicht gefunden')
    s = s.replace(m.group(0), '<main id="main">\n' + galerie_markup() + '\n</main>')

    # ── Verweise: auf dieser Seite gibt es die Sprungziele nicht ──────────
    for ziel in ('leistungen', 'ueber', 'warum', 'kontakt', 'impressum', 'datenschutz'):
        s = s.replace('href="#%s"' % ziel, 'href="index.html#%s"' % ziel)
    s = s.replace('href="#hero" class="nav-logo"', 'href="index.html" class="nav-logo"')
    s = s.replace('<a href="index.html#kontakt" class="mobile-menu-cta">',
                  '<a href="index.html#kontakt" class="mobile-menu-cta">')
    # der eigene Eintrag zeigt nicht auf sich selbst
    s = s.replace('<li><a href="referenzen.html">Referenzen</a></li>',
                  '<li><a href="referenzen.html" aria-current="page">Referenzen</a></li>')
    s = s.replace('  <a href="referenzen.html">Referenzen</a>\n',
                  '  <a href="referenzen.html" aria-current="page">Referenzen</a>\n')

    # ── JSON-LD: nur noch eine schlanke Seitenauszeichnung ────────────────
    m = re.search(r'<script type="application/ld\+json">.*?</script>', s, re.S)
    if not m:
        fehler('JSON-LD nicht gefunden')
    s = s.replace(m.group(0), JSONLD.strip())

    # ── Skript: das Kontaktformular gibt es hier nicht, die Lupe schon ────
    m = re.search(r'  // Kontaktformular → öffnet vorausgefüllte.*?\n  \}\n', s, re.S)
    if m:
        s = s.replace(m.group(0), '')
    s = s.replace('</body>', LIGHTBOX_JS + '</body>', 1)

    io.open(ZIEL, 'w', encoding='utf-8').write(s)
    print('referenzen.html geschrieben, %d KB, %d Fälle'
          % (len(s.encode('utf-8')) // 1024, len(FAELLE)))


def galerie_markup():
    teile = ['''<section id="ref-kopf">
  <div class="hero-grid"></div>
  <div class="ref-kopf-inner">
    <div class="ref-kopf-text">
    <div class="hero-eyebrow">Aus der Praxis</div>
    <h1>Schäden, die ich<br><span>begutachtet habe.</span></h1>
    <p>Ein Gutachten steht und fällt mit der Aufnahme vor Ort. Diese Bilder zeigen,
       wie ich dokumentiere: mit Maßstab, aus mehreren Abständen und immer so,
       dass sich der Zustand später nachvollziehen lässt – auch von jemandem,
       der nicht dabei war.</p>
    </div>
    <figure class="ref-kopf-bild">
      <img src="fotos/03-toyota-corolla-heck-detail-klein.webp" alt="Eingedrückter und aufgerissener Heckstoßfänger eines Toyota Corolla" width="800" height="600" decoding="async"/>
    </figure>
  </div>
</section>

<section id="referenzen">
  <div class="reveal"><div class="section-label">Referenzen</div></div>
  <h2 class="section-title reveal delay-1">Aufnahmen aus meinen Gutachten</h2>
  <p class="section-intro reveal delay-2">Alle Bilder stammen aus abgeschlossenen Aufträgen.
     Kennzeichen sind unkenntlich gemacht, Namen und Anschriften der Auftraggeber nenne ich
     nicht. Zum Vergrößern anklicken.</p>
  <div class="ref-grid">''']

    for i, (datei, fahrzeug, schaden, datum, text) in enumerate(FAELLE, 1):
        alt = '%s, %s, aufgenommen %s' % (fahrzeug, schaden.lower(), datum)
        teile.append('''    <figure class="ref-karte reveal delay-%d">
      <button class="ref-bild" type="button" data-gross="fotos/%s" data-text="%s – %s">
        <img src="fotos/%s" alt="%s" width="800" height="600" loading="lazy" decoding="async"/>
        <span class="ref-lupe" aria-hidden="true">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5M11 8v6M8 11h6"/></svg>
        </span>
      </button>
      <figcaption>
        <div class="ref-kopfzeile"><strong>%s</strong><span>%s</span></div>
        <div class="ref-schaden">%s</div>
        <p>%s</p>
      </figcaption>
    </figure>''' % (((i - 1) % 4) + 1, datei, fahrzeug.replace('"', ''),
                    schaden.replace('"', ''), datei.replace('.webp', '-klein.webp'),
                    alt, fahrzeug, datum, schaden, text))

    teile.append('''  </div>

  <aside class="ref-hinweis reveal">
    <h3>Warum so viele Bilder?</h3>
    <p>Eine Versicherung, die kürzen will, sucht die Lücke in der Dokumentation.
       Was nicht fotografiert ist, hat es im Streitfall nicht gegeben – deshalb
       lieber dreißig Aufnahmen zu viel als eine zu wenig. Der Maßstab im Bild
       ist kein Schmuck: Er hält die Höhe über der Fahrbahn fest und ist oft das
       Einzige, womit sich eine Schadendarstellung der Gegenseite widerlegen lässt.</p>
    <a class="btn-primary" href="index.html#kontakt">Gutachten anfragen</a>
  </aside>
</section>

<div class="lupe" id="lupe" role="dialog" aria-modal="true" aria-label="Bild vergrößert" hidden>
  <button class="lupe-zu" id="lupe-zu" type="button" aria-label="Schließen">&times;</button>
  <img id="lupe-bild" alt=""/>
  <p class="lupe-text" id="lupe-text"></p>
</div>''')
    return '\n'.join(teile)


GALERIE_CSS = '''
    /* ══ REFERENZEN ══════════════════════════════════════════════════════ */
    #ref-kopf {
      background:
        radial-gradient(75% 70% at 68% 20%, rgba(255,255,255,0.12), rgba(255,255,255,0) 62%),
        radial-gradient(58% 60% at 6% 100%, rgba(255,186,140,0.16), rgba(255,186,140,0) 68%),
        linear-gradient(135deg, var(--blue-dark) 0%, var(--blue) 62%, var(--blue-mid) 100%);
      margin-top: 68px; padding: 74px 5% 66px;
      position: relative; overflow: hidden;
    }
    .ref-kopf-inner {
      position: relative; z-index: 4; max-width: 1240px; margin: 0 auto;
      display: grid; grid-template-columns: minmax(0, 1.1fr) minmax(0, 0.9fr);
      gap: 40px; align-items: center;
    }
    /* Eine echte Aufnahme statt der gezeichneten Marke – auf einer Seite,
       die von Fotos handelt, ist eine Zeichnung im Kopf das falsche Signal. */
    .ref-kopf-bild {
      margin: 0; border-radius: 20px; overflow: hidden;
      box-shadow: 0 26px 64px rgba(0,10,40,0.42);
      border: 1px solid rgba(255,255,255,0.18);
      animation: fade-up 1s 0.25s cubic-bezier(.22,1,.36,1) both;
    }
    .ref-kopf-bild img {
      display: block; width: 100%; height: auto;
      aspect-ratio: 4 / 3; object-fit: cover;
    }
    @media (max-width: 860px) {
      .ref-kopf-inner { grid-template-columns: 1fr; gap: 26px; }
      .ref-kopf-bild { border-radius: 16px; }
    }
    .ref-kopf-inner h1 {
      font-family: var(--font-condensed);
      font-size: clamp(2.3rem, 4.6vw, 3.4rem); font-weight: 900;
      color: var(--white); line-height: 1.08; margin-bottom: 18px;
      letter-spacing: -0.028em;
      animation: fade-up 0.9s 0.1s cubic-bezier(.22,1,.36,1) both;
    }
    .ref-kopf-inner h1 span { color: rgba(255,255,255,0.5); font-weight: 300; }
    .ref-kopf-inner p {
      color: rgba(255,255,255,0.95); font-size: 1.02rem; line-height: 1.72; max-width: 620px;
      animation: fade-up 0.9s 0.2s cubic-bezier(.22,1,.36,1) both;
    }

    #referenzen { background: var(--gray-light); }
    .ref-grid {
      display: grid; grid-template-columns: repeat(auto-fill, minmax(330px, 1fr));
      gap: 24px;
    }
    .ref-karte {
      background: var(--white); border: 1px solid var(--gray-mid);
      border-radius: 18px; overflow: hidden; margin: 0;
      box-shadow: 0 2px 12px rgba(0,61,165,0.05);
      transition: transform 0.45s cubic-bezier(.16,1,.3,1), box-shadow 0.45s cubic-bezier(.16,1,.3,1);
    }
    .ref-karte:hover { transform: translateY(-3px); box-shadow: 0 16px 40px rgba(0,42,115,0.13); }
    .ref-bild {
      display: block; width: 100%; padding: 0; border: 0; cursor: zoom-in;
      background: var(--blue-pale); position: relative; line-height: 0;
    }
    .ref-bild img {
      display: block; width: 100%; height: auto; aspect-ratio: 4 / 3; object-fit: cover;
      transition: transform 0.6s cubic-bezier(.16,1,.3,1);
    }
    .ref-karte:hover .ref-bild img { transform: scale(1.035); }
    .ref-lupe {
      position: absolute; right: 12px; bottom: 12px;
      width: 38px; height: 38px; border-radius: 50%;
      background: rgba(0,20,60,0.62); color: var(--white);
      display: grid; place-items: center;
      opacity: 0; transform: translateY(6px);
      transition: opacity 0.3s, transform 0.3s;
      backdrop-filter: blur(6px); -webkit-backdrop-filter: blur(6px);
    }
    .ref-lupe svg { width: 19px; height: 19px; }
    .ref-karte:hover .ref-lupe, .ref-bild:focus-visible .ref-lupe { opacity: 1; transform: translateY(0); }
    .ref-karte figcaption { padding: 20px 22px 22px; }
    .ref-kopfzeile {
      display: flex; align-items: baseline; justify-content: space-between;
      gap: 12px; flex-wrap: wrap; margin-bottom: 4px;
    }
    .ref-kopfzeile strong { font-size: 1rem; font-weight: 700; color: var(--blue-dark); }
    .ref-kopfzeile span { font-size: 0.8rem; color: var(--gray-text); flex-shrink: 0; }
    .ref-schaden {
      font-size: 0.86rem; font-weight: 600; color: var(--flamme-tief); margin-bottom: 10px;
    }
    .ref-karte figcaption p { font-size: 0.88rem; color: var(--gray-text); line-height: 1.65; }

    .ref-hinweis {
      margin-top: 40px; padding: 34px 32px;
      background: var(--blue-dark); border-radius: 20px;
      max-width: 720px;
    }
    .ref-hinweis h3 { font-size: 1.15rem; font-weight: 700; color: var(--white); margin-bottom: 12px; }
    .ref-hinweis p { font-size: 0.94rem; line-height: 1.72; color: rgba(255,255,255,0.82); margin-bottom: 22px; }
    .ref-hinweis .btn-primary { box-shadow: none; }

    /* Lupe: Bild groß, ohne Fremdbibliothek */
    .lupe {
      position: fixed; inset: 0; z-index: 200;
      background: rgba(0,8,28,0.92);
      display: flex; flex-direction: column; align-items: center; justify-content: center;
      gap: 16px; padding: 5vh 4vw;
      opacity: 0; transition: opacity 0.25s;
    }
    .lupe[hidden] { display: none; }
    .lupe.auf { opacity: 1; }
    .lupe img { max-width: 100%; max-height: 82vh; border-radius: 10px; box-shadow: 0 30px 80px rgba(0,0,0,0.5); }
    .lupe-text { color: rgba(255,255,255,0.85); font-size: 0.92rem; text-align: center; }
    .lupe-zu {
      position: absolute; top: 18px; right: 20px;
      width: 44px; height: 44px; border-radius: 50%;
      background: rgba(255,255,255,0.12); border: 1px solid rgba(255,255,255,0.25);
      color: var(--white); font-size: 1.7rem; line-height: 1; cursor: pointer;
      transition: background 0.2s;
    }
    .lupe-zu:hover { background: rgba(255,255,255,0.24); }

    @media (max-width: 900px) { #ref-kopf { padding: 52px 6% 48px; } }
    @media (max-width: 600px) {
      #ref-kopf { padding: 38px 6% 40px; }
      .ref-grid { grid-template-columns: 1fr; gap: 18px; }
      .ref-karte figcaption { padding: 17px 18px 19px; }
      .ref-hinweis { padding: 26px 22px; }
      .ref-hinweis .btn-primary { display: block; text-align: center; }
      .ref-lupe { opacity: 1; transform: none; }
    }
'''

JSONLD = '''
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "CollectionPage",
  "name": "Referenzen – Ingenieurbüro Kaltbrunn",
  "description": "Aufnahmen aus abgeschlossenen Kfz-Gutachten im Kreis Bergstraße.",
  "url": "https://www.ing-nuri.de/referenzen.html",
  "isPartOf": { "@type": "WebSite", "name": "Ingenieurbüro Kaltbrunn", "url": "https://www.ing-nuri.de/" },
  "about": { "@type": "ProfessionalService", "name": "Ingenieurbüro Kaltbrunn" },
  "breadcrumb": {
    "@type": "BreadcrumbList",
    "itemListElement": [
      { "@type": "ListItem", "position": 1, "name": "Start", "item": "https://www.ing-nuri.de/" },
      { "@type": "ListItem", "position": 2, "name": "Referenzen", "item": "https://www.ing-nuri.de/referenzen.html" }
    ]
  }
}
</script>
'''

LIGHTBOX_JS = '''<script>
  // Lupe – ohne Fremdbibliothek, mit Tastatur bedienbar
  (function () {
    const lupe  = document.getElementById('lupe');
    const bild  = document.getElementById('lupe-bild');
    const text  = document.getElementById('lupe-text');
    const zu    = document.getElementById('lupe-zu');
    let zuletzt = null;

    function auf(knopf) {
      zuletzt = knopf;
      bild.src = knopf.dataset.gross;
      bild.alt = knopf.querySelector('img').alt;
      text.textContent = knopf.dataset.text || '';
      lupe.hidden = false;
      requestAnimationFrame(() => lupe.classList.add('auf'));
      document.body.style.overflow = 'hidden';
      zu.focus();
    }
    function schliessen() {
      lupe.classList.remove('auf');
      document.body.style.overflow = '';
      setTimeout(() => { lupe.hidden = true; bild.removeAttribute('src'); }, 250);
      if (zuletzt) zuletzt.focus();
    }
    document.querySelectorAll('.ref-bild').forEach(k => k.addEventListener('click', () => auf(k)));
    zu.addEventListener('click', schliessen);
    lupe.addEventListener('click', e => { if (e.target === lupe || e.target === bild) schliessen(); });
    document.addEventListener('keydown', e => { if (e.key === 'Escape' && !lupe.hidden) schliessen(); });
  })();
</script>
'''

if __name__ == '__main__':
    main()
