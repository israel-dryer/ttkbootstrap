"""Public image-construction toolkit for ttkbootstrap styles.

`Assets(style)` is the ergonomic, key-safe front door to the engine's
content-addressed image cache (`Style._get_or_create_image`). The shape recipes
(`circle`/`rect`/`rounded_rect`) and the general `image()` escape hatch each
render an asset *and* derive its cache key from the same inputs, so a key can
never drift from the pixels it names -- the purity hazard PR 2's whole audit
existed to manage.

The renderer ports bootstack's snap-at-the-source pipeline: even-pixel-snap the
final size, adaptive supersample (3x/2x/1x by size), LANCZOS downscale, then an
UnsharpMask to restore edge crispness. The result is crisper, DPI-stable assets
-- callers pass only the logical (already DPI-scaled) size; the oversample factor
and the snap are internal and adaptive.
"""
from PIL import Image, ImageDraw, ImageFilter, ImageTk
from PIL.Image import Resampling


def _wh(size):
    """Normalize `size` (int -> square, or `(w, h)`) to an int `(w, h)` tuple."""
    if isinstance(size, (int, float)):
        return (int(size), int(size))
    return (int(size[0]), int(size[1]))


def _even(n):
    """Snap a pixel length up to the next even integer.

    bootstack's fractional-DPI fix: an even final size avoids the half-pixel
    LANCZOS blur seen at 125%/150% scaling. Applied to the anti-aliased recipes
    only -- `rect` has no edges to blur and keeps its exact size.
    """
    return n if n % 2 == 0 else n + 1


def _oversample(w, h):
    """Adaptive supersample factor by the larger dimension (bootstack: 3/2/1)."""
    longest = max(w, h)
    if longest < 32:
        return 3
    elif longest < 64:
        return 2
    return 1


def _render(size, draw_fn):
    """Render `draw_fn` onto an oversampled canvas, then snap-downscale + sharpen.

    `size` is the even-snapped final `(w, h)`. `draw_fn(draw, w, h)` draws onto an
    `ImageDraw.Draw` over the oversampled `(w, h)` canvas (final size x the
    adaptive factor), so any coordinates are expressed relative to the canvas it
    is handed. After the LANCZOS downscale an UnsharpMask restores edge
    crispness. Returns a `PhotoImage`.
    """
    w, h = size
    factor = _oversample(w, h)
    cw, ch = w * factor, h * factor
    img = Image.new("RGBA", (cw, ch))
    draw_fn(ImageDraw.Draw(img), cw, ch)
    if factor > 1:
        img = img.resize((w, h), Resampling.LANCZOS)
        img = img.filter(ImageFilter.UnsharpMask(radius=0.6, percent=60, threshold=0))
    return ImageTk.PhotoImage(img)


class Assets:
    """Key-safe image construction over the engine's content-addressed cache.

    `Assets(style)` wraps `Style._get_or_create_image`: each method renders an
    asset *and* derives its cache key from the same render inputs, so the key
    cannot drift from the pixels (the purity hazard PR 2's audit existed to
    manage). Builders reach a shared instance via `self.assets`; public users
    construct `Assets(Style.get_instance())`.

    Sizes are the final widget pixel size (already DPI-scaled by the caller, e.g.
    via `scale_size`); the anti-aliased recipes even-pixel-snap and supersample
    internally, so two logical sizes that snap equal share one image. Every
    method returns the Tcl image name (the `_get_or_create_image` contract), and
    the resolved colors are *in* the key, so cross-theme-identical assets dedupe.
    """

    def __init__(self, style):
        self.style = style

    def circle(self, fill, size, *, outline=None, width=0):
        """A filled (optionally outlined) circle. `width` is in final pixels."""
        size = _wh(size)
        size = (_even(size[0]), _even(size[1]))
        key = ("circle", fill, size, outline, width)

        def factory():
            def draw(d, w, h):
                ow = round(width * w / size[0]) if width else 0
                d.ellipse((0, 0, w - 1, h - 1), fill=fill, outline=outline, width=ow)
            return _render(size, draw)

        return self.style._get_or_create_image(key, factory)

    def rounded_rect(self, fill, size, radius, *, outline=None, width=0):
        """A rounded rectangle. `radius` and `width` are in final pixels."""
        size = _wh(size)
        size = (_even(size[0]), _even(size[1]))
        key = ("rounded_rect", fill, size, radius, outline, width)

        def factory():
            def draw(d, w, h):
                factor = w / size[0]
                r = round(radius * factor)
                ow = round(width * factor) if width else 0
                d.rounded_rectangle((0, 0, w - 1, h - 1), radius=r, fill=fill,
                                    outline=outline, width=ow)
            return _render(size, draw)

        return self.style._get_or_create_image(key, factory)

    def rect(self, fill, size):
        """A solid axis-aligned rectangle (no anti-aliasing, no size snap)."""
        size = _wh(size)
        key = ("rect", fill, size)
        return self.style._get_or_create_image(
            key, lambda: ImageTk.PhotoImage(Image.new("RGB", size, fill)))

    def image(self, size, draw_fn, *key_parts):
        """Escape hatch for custom composite draws (concentric circles, glyphs).

        `draw_fn(draw, w, h)` draws onto the oversampled `(w, h)` canvas, so the
        old hand-fit canvas constants become `w`-relative expressions. The key is
        `(draw_fn.__qualname__, snapped_size, *key_parts)` -- list in `key_parts`
        every color/value the draw closes over; they sit *beside* the draw so the
        key cannot silently drift from it, and the `__qualname__` keeps two
        different draws from colliding on equal `key_parts`.
        """
        size = _wh(size)
        size = (_even(size[0]), _even(size[1]))
        key = (draw_fn.__qualname__, size, *key_parts)
        return self.style._get_or_create_image(key, lambda: _render(size, draw_fn))
