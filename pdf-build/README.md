# Chapter One sample PDF — rebuild scripts

The sample PDF (`../the-traveling-jessie-barstow-chapter-one.pdf`) is 9 pages:

| page | what it is                                    |
|------|-----------------------------------------------|
| 1    | full-bleed cover                              |
| 2    | title page / colophon                         |
| 3–8  | Chapter One, cream stock, page numbers        |
| 9    | closing CTA ("Keep Traveling with Jessie")    |

These scripts rebuild **pages 2 and 9 only** and splice them back into the existing
PDF, so the cover and the chapter text are carried over untouched, byte for byte.
That is deliberate: it is how copy changes (retailers, order vs preorder, the
domain) get made without any risk of the chapter repaginating.

    python3 render.py    # fits type sizes + letter-spacing against the current PDF
    python3 final.py     # builds the two pages and writes rebuilt.pdf

`render.py` measures the existing pages with `pdftotext -bbox-layout` and solves for
the font size, letter-spacing and top offset that reproduce each line's bounding box
to within ~0.05pt, so the rebuild lands on the original's typography instead of
guessing at it. `spec.py` holds those target boxes and the reverse-engineered design.

Needs: `playwright` (chromium), `pypdf`, `Pillow`, `fontTools`, poppler-utils, and
network access for the Google Fonts TTFs — fetch the css2 URL with **no custom
User-Agent** or you get woff2 subsets back instead of TTFs.

## Design facts worth keeping

* Trim is **6.5in x 9in** (468 x 648pt) for the full-bleed pages, matched to the
  cover art's 3470x4801 aspect so page 1 crops nothing. Do not switch to Letter.
* Pages are authored as **624 x 863 CSS px** (96dpi) with `@page{margin:0}` and an
  absolutely positioned body — the absolute position is what stops a 1-2px overflow
  spawning a blank page.
* Chromium does **not** paint a `body` background into the print canvas here; the
  background is a real `.bg` div instead.
* Palette: cream `#FAF5EA`, ink `#241F19`, soft ink `#5B5145`, page-2 gold `#A97614`;
  navy `#14344E`→`#0B1825`, gold `#E9B949`, gold-soft `#F4D58D`, teal `#54C9D1`,
  body `#DBE6EC`, muted `#9FB3BF`, dim `#6F8794`.
* The order button is a 288x47px rounded rect (radius 6) at 168,671 with a
  `#F2CF80`→`#D39E31` left-to-right gradient.
* Fonts: Cinzel (display), EB Garamond (body), Cormorant Garamond Italic (pull
  quotes). The ✦ comes from DejaVu Sans as a system fallback.

## Verifying a rebuild

Render both files and diff them page by page — pages 1 and 3–8 must come out
pixel-identical, and only the lines you meant to change should differ:

    pdftoppm -png -r 150 old.pdf old && pdftoppm -png -r 150 rebuilt.pdf new
