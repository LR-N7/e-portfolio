# E-Portfolio — Louis REEVES

Personal one-page portfolio (single `index.html`, Tailwind via CDN) with a
French / English toggle.

```
index.html                 the whole site
Louis_REEVES.pdf           CV — French version
Louis_REEVES_CV_EN.pdf     CV — English version (generated)
assets/tipe/               TIPE project resources
  TIPE_REEVES.pdf          slide deck (downloadable)
  slides/                  deck exported as images for the in-page viewer
tools/
  build_cv_en.py           builds the English CV from the French layout
  build_slides.py          exports a deck PDF to assets/tipe/slides/*.jpg
  fonts/                   Questrial + Glacial Indifference (CV), Font Awesome Brands
```

## CV in both languages

The hero section has two buttons: **CV Français** (`Louis_REEVES.pdf`) and
**CV Anglais** (`Louis_REEVES_CV_EN.pdf`).

The English CV keeps the exact layout, colours and typefaces of the French one;
only the text is translated. If the French CV changes, update the text in
`tools/build_cv_en.py` and regenerate:

```bash
pip install pymupdf
python3 tools/build_cv_en.py
```

## Project resources

The *Projects* section links to the slide deck of the TIPE project:

* **Voir les diapositives / View the slides** opens an in-page viewer
  (arrow keys, thumbnails, swipe on mobile, click the image for full size).
* **PDF complet / Full PDF** opens the original deck.

Slides are exported with `tools/build_slides.py`; re-run it after replacing
`assets/tipe/TIPE_REEVES.pdf` so the images stay in sync.

The **project website** button is still a "coming soon" placeholder. Paste the
URL in `index.html`:

```js
const TIPE_PROJECT_URL = 'https://…';
```

and the placeholder is swapped for the real link automatically.

## Mobility section

The *Mobility* section (`#mobility`) shows the mobility video, three role models and
three scenarios (plans A / B / C).

To publish the video, drop the file in `assets/video/` and point the `<source>` of the
`#mobility` video element at it.
