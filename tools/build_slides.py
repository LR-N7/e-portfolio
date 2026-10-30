#!/usr/bin/env python3
"""Turn a slide-deck PDF into web-friendly images for the portfolio.

Every page of the PDF is exported as ``assets/tipe/slides/slide-NN.jpg`` and a
slightly optimised copy of the PDF is written to ``assets/tipe/``.

Usage:
    python3 tools/build_slides.py [deck.pdf]

Defaults to ``assets/tipe/TIPE_REEVES.pdf`` (the copy already in the repo).
Re-run it after replacing the deck so the images stay in sync.

Requires: pymupdf  ->  pip install pymupdf
"""

import pathlib
import sys

import pymupdf

ROOT = pathlib.Path(__file__).resolve().parent.parent
DECK = ROOT / "assets" / "tipe" / "TIPE_REEVES.pdf"
SLIDES_DIR = ROOT / "assets" / "tipe" / "slides"
MAX_WIDTH = 1400          # px, plenty for a full-screen view on retina laptops
QUALITY = 80


def main() -> None:
    src_path = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else DECK

    if src_path.resolve() != DECK.resolve():
        # keep the downloadable copy in the repository
        DECK.parent.mkdir(parents=True, exist_ok=True)
        with pymupdf.open(src_path) as doc:
            doc.save(DECK, garbage=4, deflate=True)

    SLIDES_DIR.mkdir(parents=True, exist_ok=True)
    for old in SLIDES_DIR.glob("slide-*.jpg"):
        old.unlink()

    with pymupdf.open(DECK) as doc:
        for number, page in enumerate(doc, start=1):
            zoom = min(1.0, MAX_WIDTH / page.rect.width)
            pix = page.get_pixmap(matrix=pymupdf.Matrix(zoom, zoom))
            out = SLIDES_DIR / f"slide-{number:02d}.jpg"
            pix.save(str(out), jpg_quality=QUALITY)
            print(f"{out.relative_to(ROOT)}  {pix.width}x{pix.height}")

    print(f"\n{len(list(SLIDES_DIR.glob('slide-*.jpg')))} slides written to "
          f"{SLIDES_DIR.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
