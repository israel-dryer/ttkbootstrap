"""Build the packaged app-icon assets from the top-level source PNGs.

Mirrors bootstack's ``assets/make_ico.py``. The per-size source renders live in
the repo-root ``assets/app_icons/`` (``16x16.png`` .. ``512x512.png``) and are
*not* shipped. This script produces the two runtime assets that ship inside the
package (``src/ttkbootstrap/assets/app_icons/``):

- ``ttkbootstrap.ico`` -- a multi-resolution Windows icon (16..256), used for the
  titlebar/taskbar icon via ``wm_iconbitmap``.
- ``ttkbootstrap.png`` -- the 512px render, used on macOS/Linux via ``iconphoto``.

Run after changing the source PNGs::

    python tools/make_app_ico.py
"""
import shutil
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = ROOT / "assets" / "app_icons"                       # source renders (not shipped)
PKG_DIR = ROOT / "src" / "ttkbootstrap" / "assets" / "app_icons"  # packaged runtime assets

# ``.ico`` entries top out at 256px; the 512 PNG is the macOS/Linux runtime icon.
ICO_SIZES = [16, 24, 32, 48, 64, 128, 256]
PNG_SIZE = 512


def make_ico(src_dir: Path, out_path: Path) -> None:
    imgs = [Image.open(src_dir / f"{s}x{s}.png").convert("RGBA") for s in ICO_SIZES]
    # Pass the largest first -- Pillow skips sizes larger than the base image.
    imgs[-1].save(
        out_path,
        format="ICO",
        bitmap_format="bmp",  # BMP encoding for maximum Windows compatibility
        sizes=[(s, s) for s in ICO_SIZES],
        append_images=imgs[:-1],
    )
    print(f"Saved: {out_path}  ({', '.join(f'{s}x{s}' for s in ICO_SIZES)})")


def copy_runtime_png(src_dir: Path, out_path: Path) -> None:
    shutil.copyfile(src_dir / f"{PNG_SIZE}x{PNG_SIZE}.png", out_path)
    print(f"Saved: {out_path}  ({PNG_SIZE}x{PNG_SIZE})")


if __name__ == "__main__":
    PKG_DIR.mkdir(parents=True, exist_ok=True)
    make_ico(SRC_DIR, PKG_DIR / "ttkbootstrap.ico")
    copy_runtime_png(SRC_DIR, PKG_DIR / "ttkbootstrap.png")