"""Verify the vectorized recolor_element_image matches the old per-pixel loop.

Runs the old per-pixel algorithm and the new PIL-vectorized path against the
same inputs and compares the output images channel-by-channel. Reports the
worst absolute delta per channel for each test case.

Expected: max delta of 0 or 1 across all opaque pixels (rounding ties may
differ by 1 LSB on a few pixels — acceptable). For fully-transparent pixels,
the new path retains the LUT-computed RGB instead of zeroing it; this is
visually invisible (alpha=0) but means raw RGB bytes can differ. We mask
those pixels out of the comparison.
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageOps

from ttkbootstrap.style.utility import (
    ELEMENTS_DIR,
    color_to_rgb,
    recolor_element_image,
)


def recolor_old(
    img: Image.Image,
    white_color: str,
    black_color: str = "#ffffff",
    magenta_color: str | None = None,
    transparent_color: str | None = None,
) -> Image.Image:
    """Original per-pixel loop, lifted from utility.py before the rewrite."""
    gray = ImageOps.grayscale(img)
    fg_rgb = color_to_rgb(white_color)
    bg_rgb = color_to_rgb(black_color)
    mag_rgb = color_to_rgb(magenta_color) if magenta_color else None
    trans_rgb = color_to_rgb(transparent_color) if transparent_color else None

    result = Image.new("RGBA", img.size)
    src_pixels = img.load()
    dst_pixels = result.load()

    for y in range(img.height):
        for x in range(img.width):
            r_src, g_src, b_src, a = src_pixels[x, y]
            if a == 0:
                if trans_rgb:
                    dst_pixels[x, y] = (*trans_rgb, 255)
                else:
                    dst_pixels[x, y] = (0, 0, 0, 0)
                continue
            alpha_frac = a / 255.0
            if mag_rgb and (r_src, g_src, b_src) == (255, 0, 255):
                r, g, b = mag_rgb
            else:
                lum = gray.getpixel((x, y)) / 255.0
                r = round(bg_rgb[0] + (fg_rgb[0] - bg_rgb[0]) * lum)
                g = round(bg_rgb[1] + (fg_rgb[1] - bg_rgb[1]) * lum)
                b = round(bg_rgb[2] + (fg_rgb[2] - bg_rgb[2]) * lum)
            if trans_rgb:
                r_final = round(trans_rgb[0] * (1 - alpha_frac) + r * alpha_frac)
                g_final = round(trans_rgb[1] * (1 - alpha_frac) + g * alpha_frac)
                b_final = round(trans_rgb[2] * (1 - alpha_frac) + b * alpha_frac)
                dst_pixels[x, y] = (r_final, g_final, b_final, 255)
            else:
                dst_pixels[x, y] = (r, g, b, a)
    return result


def recolor_new_raw(
    img: Image.Image,
    white_color: str,
    black_color: str = "#ffffff",
    magenta_color: str | None = None,
    transparent_color: str | None = None,
) -> Image.Image:
    """Reproduces the new PIL-vectorized path WITHOUT scale or PhotoImage wrap.

    Mirrors src/ttkbootstrap/style/utility.py exactly so we compare like to
    like. (Calling recolor_element_image directly returns a PhotoImage tied
    to a Tk root, which isn't what we want for a byte comparison.)
    """
    from PIL import ImageChops

    gray = ImageOps.grayscale(img)
    fg_rgb = color_to_rgb(white_color)
    bg_rgb = color_to_rgb(black_color)
    mag_rgb = color_to_rgb(magenta_color) if magenta_color else None
    trans_rgb = color_to_rgb(transparent_color) if transparent_color else None

    def _channel_lut(bg_c: int, fg_c: int) -> list[int]:
        return [round(bg_c + (fg_c - bg_c) * i / 255.0) for i in range(256)]

    r_chan = gray.point(_channel_lut(bg_rgb[0], fg_rgb[0]))
    g_chan = gray.point(_channel_lut(bg_rgb[1], fg_rgb[1]))
    b_chan = gray.point(_channel_lut(bg_rgb[2], fg_rgb[2]))

    r_src, g_src, b_src, alpha = img.split()
    result = Image.merge("RGBA", (r_chan, g_chan, b_chan, alpha))

    if mag_rgb:
        r_eq = r_src.point([255 if i == 255 else 0 for i in range(256)])
        g_eq = g_src.point([255 if i == 0 else 0 for i in range(256)])
        b_eq = b_src.point([255 if i == 255 else 0 for i in range(256)])
        mag_mask = ImageChops.multiply(ImageChops.multiply(r_eq, g_eq), b_eq)
        mag_solid = Image.new("RGBA", img.size, (*mag_rgb, 255))
        composited = Image.composite(mag_solid, result, mag_mask)
        nr, ng, nb, _ = composited.split()
        result = Image.merge("RGBA", (nr, ng, nb, alpha))

    if trans_rgb:
        backing = Image.new("RGBA", img.size, (*trans_rgb, 255))
        result = Image.alpha_composite(backing, result)

    return result


def compare(old: Image.Image, new: Image.Image) -> tuple[int, int, int, int]:
    """Return (max_dr, max_dg, max_db, max_da) over all pixels where alpha>0
    in either image. Fully-transparent-in-both pixels are skipped — the new
    path leaves LUT colors there but they're invisible.
    """
    assert old.size == new.size and old.mode == new.mode == "RGBA"
    op = old.load()
    np_ = new.load()
    max_d = [0, 0, 0, 0]
    for y in range(old.height):
        for x in range(old.width):
            o = op[x, y]
            n = np_[x, y]
            if o[3] == 0 and n[3] == 0:
                continue
            for i in range(4):
                d = abs(o[i] - n[i])
                if d > max_d[i]:
                    max_d[i] = d
    return tuple(max_d)


CASES = [
    # (manifest_key_or_filename, white, black, magenta, transparent, label)
    ("button-default.png", "#3b82f6", "#1e40af", None, None, "button: solid recolor"),
    ("input-default.png", "#ffffff", "#cbd5e0", None, "#f8fafc", "input: with transparent flatten"),
    ("checkbox-checked.png", "#ffffff", "#3b82f6", "#10b981", None, "checkbox: with magenta"),
    ("switch-on.png", "#ffffff", "#3b82f6", None, None, "switch: alpha edges"),
    ("slider-handle.png", "#ffffff", "#3b82f6", None, "#f8fafc", "slider: transparent + handle alpha"),
    ("badge-pill.png", "#ffffff", "#dc2626", "#facc15", "#ffffff", "badge: magenta + transparent"),
]


def main():
    print(f"{'case':<45} {'dR':>4} {'dG':>4} {'dB':>4} {'dA':>4}  status")
    print("-" * 80)
    all_ok = True
    for filename, white, black, mag, trans, label in CASES:
        path = Path(ELEMENTS_DIR) / filename
        if not path.exists():
            print(f"{label:<45} SKIP (file not found: {filename})")
            continue
        img = Image.open(path).convert("RGBA")
        old = recolor_old(img, white, black, mag, trans)
        new = recolor_new_raw(img, white, black, mag, trans)
        dr, dg, db, da = compare(old, new)
        ok = max(dr, dg, db, da) <= 1
        status = "OK" if ok else "FAIL"
        if not ok:
            all_ok = False
        print(f"{label:<45} {dr:>4} {dg:>4} {db:>4} {da:>4}  {status}")
    print("-" * 80)
    print("PASS" if all_ok else "FAIL — investigate")


if __name__ == "__main__":
    main()