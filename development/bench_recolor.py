"""Benchmark old vs new recolor_element_image.

Times both implementations on a representative spread of element images.
Reports per-call time and aggregate (matching realistic theme-build call
volume of ~50 recolors).
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).parent))

from ttkbootstrap.style.utility import ELEMENTS_DIR  # noqa: E402
from verify_recolor_equivalence import recolor_old, recolor_new_raw  # noqa: E402


SAMPLES = [
    "button-default.png",
    "button-compact.png",
    "input-default.png",
    "input-compact.png",
    "checkbox-checked.png",
    "switch-on.png",
    "slider-handle.png",
    "badge-pill.png",
    "border.png",
]

COLORS = ("#3b82f6", "#1e40af")  # primary blue, dark


def time_fn(fn, repeats: int = 3) -> float:
    """Return min wall time over `repeats` runs."""
    best = float("inf")
    for _ in range(repeats):
        t0 = time.perf_counter()
        fn()
        dt = time.perf_counter() - t0
        if dt < best:
            best = dt
    return best


def main():
    images = []
    for name in SAMPLES:
        path = Path(ELEMENTS_DIR) / name
        if path.exists():
            images.append((name, Image.open(path).convert("RGBA")))
    if not images:
        print("no images found")
        return

    white, black = COLORS

    print(f"{'image':<32} {'pixels':>8} {'old (ms)':>10} {'new (ms)':>10} {'speedup':>8}")
    print("-" * 72)
    total_old = 0.0
    total_new = 0.0
    total_pixels = 0
    for name, img in images:
        pixels = img.width * img.height
        total_pixels += pixels
        t_old = time_fn(lambda: recolor_old(img, white, black))
        t_new = time_fn(lambda: recolor_new_raw(img, white, black))
        total_old += t_old
        total_new += t_new
        speedup = t_old / t_new if t_new > 0 else float("inf")
        print(f"{name:<32} {pixels:>8} {t_old*1000:>10.2f} {t_new*1000:>10.4f} {speedup:>7.1f}x")

    print("-" * 72)
    speedup = total_old / total_new if total_new > 0 else float("inf")
    print(f"{'TOTAL (one pass per image)':<32} {total_pixels:>8} "
          f"{total_old*1000:>10.2f} {total_new*1000:>10.4f} {speedup:>7.1f}x")

    # Realistic theme build hits ~50 recolor calls. Project that.
    print()
    avg_old = total_old / len(images)
    avg_new = total_new / len(images)
    print(f"Projected for 50 recolor calls per theme switch (cold cache):")
    print(f"  old impl: {avg_old * 50 * 1000:>8.1f} ms")
    print(f"  new impl: {avg_new * 50 * 1000:>8.1f} ms")
    print(f"  saved:    {(avg_old - avg_new) * 50 * 1000:>8.1f} ms")


if __name__ == "__main__":
    main()