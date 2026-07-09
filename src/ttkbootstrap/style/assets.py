"""Image-construction toolkit for ttkbootstrap styles.

`Assets(style)` wraps the engine's content-addressed image cache
(`Style._get_or_create_image`). The shape recipes (`circle`/`rect`/
`rounded_rect`), the icon and recolor renderers, and the general `image()`
escape hatch each render an asset *and* derive its cache key from the same
inputs, so a key cannot drift from the pixels it names.

The renderer uses adaptive supersampling, LANCZOS downscaling, and sharpening
while preserving exact root-scaled output dimensions. Callers pass logical UI
sizes.
"""
from PIL import Image, ImageDraw, ImageFilter, ImageTk
from PIL.Image import Resampling

from ttkbootstrap.style.elements import RecolorRenderer, RecolorResult

def _oversample(w, h):
    """Adaptive supersample factor by the larger dimension: 3x below 32px, 2x below 64px, else 1x."""
    longest = max(w, h)
    if longest < 32:
        return 3
    elif longest < 64:
        return 2
    return 1


def _render(size, draw_fn):
    """Render `draw_fn` onto an oversampled canvas, then downscale and sharpen.

    `size` is the exact final physical `(w, h)`. `draw_fn(draw, w, h)` draws onto an
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
    """Image construction over the engine's content-addressed cache.

    `Assets(style)` wraps `Style._get_or_create_image`: each method renders an
    asset *and* derives its cache key from the same render inputs, so the key
    cannot drift from the pixels. Builders reach a shared instance via
    `self.assets`; public users construct `Assets(Style.get_instance())`.

    Sizes are logical UI units converted once by the root-bound scaling service;
    final image dimensions are exact and may be odd. Every
    method returns the Tcl image name (the `_get_or_create_image` contract), and
    the resolved colors are *in* the key, so cross-theme-identical assets dedupe.
    """

    def __init__(self, style):
        self.style = style
        self.scaling = style.scaling

    def circle(self, fill, size, *, outline=None, width=0):
        """A filled circle; `size` and `width` are logical UI units."""
        size = self.scaling.image_size(size)
        width = self.scaling.logical(width, minimum=1 if width > 0 else 0)
        key = ("circle", fill, size, outline, width)

        def factory():
            def draw(d, w, h):
                ow = round(width * w / size[0]) if width else 0
                d.ellipse((0, 0, w - 1, h - 1), fill=fill, outline=outline, width=ow)
            return _render(size, draw)

        return self.style._get_or_create_image(key, factory)

    def rounded_rect(self, fill, size, radius, *, outline=None, width=0):
        """A rounded rectangle with geometry in logical UI units."""
        size = self.scaling.image_size(size)
        radius = self.scaling.logical(radius)
        width = self.scaling.logical(width, minimum=1 if width > 0 else 0)
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
        size = self.scaling.image_size(size)
        key = ("rect", fill, size)
        return self.style._get_or_create_image(
            key, lambda: ImageTk.PhotoImage(Image.new("RGB", size, fill)))

    def icon(self, name, size, color):
        """Render a Bootstrap Icons glyph as a cached widget asset.

        `size` is the logical UI size; `color` is a resolved color
        string. Returns the Tcl image name (the same contract as the shape
        recipes). The key is `("icon", name, physical_size, color)` -- theme
        -independent by construction (the resolved color is *in* the key), so two
        themes that resolve a glyph to the same color share one image.

        `IconRenderer` is imported lazily here so `assets.py` keeps no module
        -level edge to `icons.py` (which imports this module), and the font is
        never read at import time.
        """
        from ttkbootstrap.style.icons import IconRenderer

        size = self.scaling.image_size(size)
        key = ("icon", name, size, color)
        return self.style._get_or_create_image(
            key, lambda: ImageTk.PhotoImage(IconRenderer.render(name, size, color)))

    def recolor(self, name, *, white, black, magenta=None, transform=None):
        """Recolor a manifest-backed ttk element raster and cache the result.

        `white`, `black`, and optional `magenta` are resolved color strings for
        the source template's semantic channels. Source alpha is preserved.
        `transform` may flip the image horizontally (`"flip-x"`) or rotate it
        by 90/180/270 degrees (`"rotate-90"`/`"rotate-180"`/`"rotate-270"`);
        dimensions and border/padding metadata transform with the pixels.

        Returns a `RecolorResult` containing the Tcl image name and scaled
        logical manifest metadata. Source-image dimensions only validate the
        vendored PNG; callers do not pass a size.
        """
        meta = RecolorRenderer.metadata(name, self.scaling, transform)
        size = (meta.width, meta.height)
        key = ("recolor", name, size, white, black, magenta, transform)
        image = self.style._get_or_create_image(
            key,
            lambda: ImageTk.PhotoImage(RecolorRenderer.render(
                name, size, white, black, magenta, transform)),
        )
        return RecolorResult(image=image, meta=meta)

    def image(self, size, draw_fn, *key_parts):
        """Escape hatch for custom composite draws (concentric circles, glyphs).

        `draw_fn(draw, w, h)` draws onto the oversampled `(w, h)` canvas, so the
        old hand-fit canvas constants become `w`-relative expressions. The key is
        `(draw_fn.__qualname__, physical_size, *key_parts)` -- list in `key_parts`
        every color/value the draw closes over; they sit *beside* the draw so the
        key cannot silently drift from it, and the `__qualname__` keeps two
        different draws from colliding on equal `key_parts`.
        """
        size = self.scaling.image_size(size)
        key = (draw_fn.__qualname__, size, *key_parts)
        return self.style._get_or_create_image(key, lambda: _render(size, draw_fn))
