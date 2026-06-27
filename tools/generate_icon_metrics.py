#!/usr/bin/env python
"""Generate normalized ink-bounds metrics for the bundled icon font.

The icon renderer (`ttkbootstrap.style.icons.IconRenderer.render`) needs each
glyph's true *inked* bounding box to size and center it consistently — Pillow's
`font.getbbox()` under-reports the ink for these icon glyphs, which left
full-bleed icons with no padding and nudged some glyphs off-center.

A glyph's ink bbox is color-independent and scales linearly with font size, so
it only needs to be measured once per glyph and stored as fractions of the em.
This tool renders every glyph at a high reference size, measures the actual
inked pixels, and writes the normalized box to `icon_metrics.json` next to the
font. Re-run it whenever `bootstrap.ttf` / `glyphmap.json` change:

    python tools/generate_icon_metrics.py

Each entry is ``name -> [left, top, width, height]`` as fractions of the font
size, measured from the text draw origin (matching how the renderer positions
the glyph).
"""

from __future__ import annotations

import argparse
import io
import json
from pathlib import Path

from PIL import Image as PILImage, ImageDraw, ImageFont

ROOT = Path(__file__).parent.parent
ICONS_DIR = ROOT / "src" / "ttkbootstrap" / "assets" / "icons"
FONT_PATH = ICONS_DIR / "bootstrap.ttf"
GLYPHMAP_PATH = ICONS_DIR / "glyphmap.json"
OUT_PATH = ICONS_DIR / "icon_metrics.json"

# High reference size — large enough that hinting noise is negligible.
REF = 512
# Decimal places to keep per fraction (≈ sub-pixel even at 4K icon sizes).
PRECISION = 5


def measure_glyph(font: ImageFont.FreeTypeFont, glyph: str) -> list[float] | None:
    """Return [left, top, width, height] of the glyph's ink, as em fractions.

    Offsets are relative to the text draw origin, so the renderer can place the
    ink precisely. Returns None for glyphs that render no pixels.
    """
    # Generous canvas so glyphs extending past the em in any direction are
    # still captured; draw origin sits at (REF, REF).
    canvas = PILImage.new("RGBA", (REF * 3, REF * 3), (0, 0, 0, 0))
    ImageDraw.Draw(canvas).text((REF, REF), glyph, font=font, fill="#000000")
    bbox = canvas.getchannel("A").getbbox()
    if bbox is None:
        return None
    left, top, right, bottom = bbox
    return [
        round((left - REF) / REF, PRECISION),
        round((top - REF) / REF, PRECISION),
        round((right - left) / REF, PRECISION),
        round((bottom - top) / REF, PRECISION),
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--ref", type=int, default=REF, help=f"Reference render size in px (default: {REF}).")
    parser.add_argument("--out", type=Path, default=OUT_PATH, help=f"Output path (default: {OUT_PATH}).")
    args = parser.parse_args()

    if not FONT_PATH.exists() or not GLYPHMAP_PATH.exists():
        raise SystemExit(f"Missing icon assets in {ICONS_DIR} (need bootstrap.ttf + glyphmap.json).")

    glyphmap: dict[str, int] = json.loads(GLYPHMAP_PATH.read_text(encoding="utf-8"))
    font = ImageFont.truetype(io.BytesIO(FONT_PATH.read_bytes()), args.ref)

    metrics: dict[str, list[float]] = {}
    empty: list[str] = []
    for name, codepoint in sorted(glyphmap.items()):
        box = measure_glyph(font, chr(codepoint))
        if box is None:
            empty.append(name)
            continue
        metrics[name] = box

    args.out.write_text(json.dumps(metrics, indent=0, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Wrote {len(metrics)} icon metrics to {args.out} (ref={args.ref}px).")
    if empty:
        print(f"Skipped {len(empty)} glyphs with no ink: {', '.join(empty[:10])}{' …' if len(empty) > 10 else ''}")


if __name__ == "__main__":
    main()
