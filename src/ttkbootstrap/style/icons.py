"""Bootstrap Icons glyph rendering for ttkbootstrap styles.

`IconRenderer` rasterizes a single named glyph from the vendored Bootstrap Icons
font (`assets/icons/`) to a PIL image, using a precomputed per-glyph ink box to
fit-and-center it accurately -- the alignment fix ported from the sibling
bootstack project. Pillow's `font.getbbox()` under-reports the ink of full-bleed
icon glyphs, which skews sizing/centering; `icon_metrics.json` instead carries
each glyph's true inked bounds (in em-fractions) measured offline, so the
renderer fits the real ink to the frame with no per-glyph fudge.

The public surface layered on top:

  - `Icon(name, size, color)` -- the atom: render one glyph to a cached Tk image
    usable directly as `image=`. `color` is a bootstyle keyword or a hex,
    resolved once against the active theme.
  - `icon_element(style, name, ...)` -- style-level sugar that maps a glyph per
    ttk widget state and bakes a validated image element (the `Style.map`-aligned
    analog of `image_element`, with the icon as the asset source).

Layering: this module's top-level imports are PIL + stdlib + the two leaf toolkit
modules (`assets`, `layout`); it carries **no module-level engine edge** (the
`Style` singleton is reached function-locally inside `Icon`), so it stays a leaf
and imports standalone. Asset loading is lazy: `import ttkbootstrap` does not read
the font -- `IconRenderer` loads it on first `render`.
"""
import io
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont
from PIL.Image import Resampling

from ttkbootstrap.style.assets import Assets, _wh
from ttkbootstrap.style.layout import statespec, image_element


# The vendored Bootstrap Icons assets ship as package data next to this package
# (see assets/icons/README.md). Resolved relative to this file so it works from
# an installed wheel, not just the src tree.
_ICONS_DIR = Path(__file__).parent.parent / "assets" / "icons"

# A small downward nudge -- icon fonts sit slightly high in their em box; this
# (and the 10% inner pad) match bootstack's tuned render so glyphs optically
# center in a square frame.
_ICON_Y_BIAS = 0.02
_ICON_PAD_FACTOR = 0.10


def _icon_oversample(w, h):
    """Supersample factor for a glyph of size `(w, h)` -- richer than the
    geometric recipes' 3/2/1 (`assets._oversample`).

    Glyph outlines (circle/chevron) carry thin curved strokes; the smoothness of
    those curves is set by the *supersample*, not the sharpen -- a hard sharpen
    just stair-steps them. So push samples high (6x) for the small indicator tier
    and pair it with a gentle UnsharpMask (see `render`): the curves stay smooth
    and the straight strokes stay defined. bootstack stops at 3x + a gentle
    sharpen (soft but smooth); the richer supersample here is what lets the edges
    read crisp without pixelating the rings.
    """
    longest = max(w, h)
    if longest < 32:
        return 6
    elif longest < 64:
        return 3
    return 1


class IconRenderer:
    """Render one Bootstrap Icons glyph to a PIL image (lazy, cached assets).

    Stateless apart from the class-level caches: the font bytes, the
    name->character glyphmap, the per-glyph ink metrics, and one `FreeTypeFont`
    per *computed* font size (the fit size varies by glyph, not the requested
    icon size). Each is loaded/built once on first use and persists for the
    process lifetime -- this is font/glyph data, independent of theme and of the
    Tk root, so `Style.clear_image_cache()` (which drops rendered `PhotoImage`s)
    deliberately does not release it. `render` is pure with respect to
    `(name, size, color)`; the `Assets.icon` facade memoizes its Tk `PhotoImage`
    through the engine's content-addressed image cache.
    """

    _font_bytes = None      # bytes, loaded once
    _glyphmap = None        # dict[name -> single-char str]
    _metrics = None         # dict[name -> [left, top, width, height]] (em fractions)
    _font_cache = {}        # dict[int -> FreeTypeFont]

    @classmethod
    def _load_assets(cls):
        """Lazy-load the font bytes + the name->character glyphmap (once)."""
        if cls._font_bytes is None:
            cls._font_bytes = (_ICONS_DIR / "bootstrap.ttf").read_bytes()
            raw = json.loads(
                (_ICONS_DIR / "glyphmap.json").read_text(encoding="utf-8"))
            cls._glyphmap = {name: chr(cp) for name, cp in raw.items()}
        return cls._font_bytes, cls._glyphmap

    @classmethod
    def _get_metrics(cls):
        """Lazy-load the precomputed normalized ink bounds per glyph (once).

        Maps a glyph name to `[left, top, width, height]` as fractions of the
        font size, measured from the text draw origin (see
        `tools/generate_icon_metrics.py`). A missing/unreadable file degrades to
        an empty map -- the renderer then falls back to `getbbox` measurement.
        """
        if cls._metrics is None:
            try:
                cls._metrics = json.loads(
                    (_ICONS_DIR / "icon_metrics.json").read_text(encoding="utf-8"))
            except (OSError, ValueError):
                cls._metrics = {}
        return cls._metrics

    @classmethod
    def _get_font(cls, size):
        """A `FreeTypeFont` at `size` px, cached (font load is from in-memory bytes)."""
        font = cls._font_cache.get(size)
        if font is None:
            font_bytes, _ = cls._load_assets()
            font = ImageFont.truetype(io.BytesIO(font_bytes), size)
            cls._font_cache[size] = font
        return font

    @classmethod
    def render(cls, name, size, color):
        """Render glyph `name` to an RGBA `Image` of `size`, filled with `color`.

        `size` is the final pixel size -- an int (square) or `(w, h)`; `color` is
        a literal color string (already resolved). The glyph is drawn onto an
        adaptively oversampled canvas, fit-and-centered via its precomputed ink
        box, then LANCZOS-downscaled with an `UnsharpMask` to restore edge
        crispness (bootstack's pipeline, shared with `assets._render`).

        Raises `ValueError` for a name absent from the Bootstrap Icons glyphmap
        (a typo fails loudly rather than rendering a blank image).
        """
        w, h = _wh(size)
        _, glyphmap = cls._load_assets()
        glyph = glyphmap.get(name)
        if glyph is None:
            raise ValueError(
                f"unknown icon name {name!r}; not in the Bootstrap Icons glyphmap "
                f"(assets/icons/glyphmap.json)"
            )

        factor = _icon_oversample(w, h)
        cw, ch = w * factor, h * factor
        pad_w, pad_h = int(cw * _ICON_PAD_FACTOR), int(ch * _ICON_PAD_FACTOR)
        inner_w, inner_h = cw - 2 * pad_w, ch - 2 * pad_h

        img = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        metrics = cls._get_metrics().get(name)
        if metrics:
            # Precomputed normalized ink box (em fractions from the draw origin):
            # fit the true ink to the inner frame and center on it -- accurate for
            # full-bleed glyphs, free of getbbox skew, no per-glyph offset.
            nl, nt, nw, nh = metrics
            font_size = max(1, int(min(
                inner_w / max(nw, 1e-6),
                inner_h / max(nh, 1e-6),
                float(max(cw, ch)),
            )))
            font = cls._get_font(font_size)
            ink_w, ink_h = nw * font_size, nh * font_size
            dx = (cw - ink_w) / 2 - nl * font_size
            dy = (ch - ink_h) / 2 - nt * font_size + ch * _ICON_Y_BIAS
            draw.text((dx, dy), glyph, font=font, fill=color)
        else:
            # Fallback for glyphs absent from icon_metrics.json: measure with
            # getbbox at render time (under-reports full-bleed ink, but always
            # works). Regenerate metrics with tools/generate_icon_metrics.py.
            eff = max(1, min(cw, ch))
            font = cls._get_font(eff)
            ascent, descent = font.getmetrics()
            bbox = font.getbbox(glyph)
            gw, gh = bbox[2] - bbox[0], bbox[3] - bbox[1]
            if gw > inner_w or gh > inner_h:
                scale = min(inner_w / max(gw, 1), inner_h / max(gh, 1)) * 0.95
                eff = max(1, int(eff * scale))
                font = cls._get_font(eff)
                ascent, descent = font.getmetrics()
                bbox = font.getbbox(glyph)
                gw, gh = bbox[2] - bbox[0], bbox[3] - bbox[1]
            full_h = ascent + descent
            dx = pad_w + (inner_w - gw) // 2 - bbox[0]
            dy = pad_h + (inner_h - full_h) // 2 + (ascent - bbox[3]) + int(ch * _ICON_Y_BIAS)
            draw.text((dx, dy), glyph, font=font, fill=color)

        if factor > 1:
            img = img.resize((w, h), Resampling.LANCZOS)
            # Gentle sharpen only: the high supersample above already gives smooth
            # curves, so this just restores a little edge definition without
            # stair-stepping the thin rings. (A harder sharpen pixelated them.)
            img = img.filter(ImageFilter.UnsharpMask(radius=0.5, percent=50, threshold=0))
        return img


# --------------------------------------------------------------------------- #
# Public surface
# --------------------------------------------------------------------------- #
def _resolve_color(style, color):
    """Resolve a color spec to a literal color string.

    A bootstyle keyword ("primary", "fg", ...) resolves against the *active*
    theme; a hex string (or any non-keyword) passes through unchanged. Resolves
    once -- there is no auto-follow on a later theme switch (a re-render is the
    engine's job, or a fresh call).
    """
    if not color:
        return color
    if isinstance(color, str) and color.startswith("#"):
        return color
    resolved = style.colors.get(color)
    return resolved if resolved is not None else color


def Icon(name, size=16, color=None):
    """Render a Bootstrap Icons glyph as a cached Tk image.

    Returns the Tcl image name (a string), usable directly as a widget's
    `image=` -- the engine's content-addressed cache holds a strong reference, so
    the image stays alive and identical `(name, size, color)` calls dedupe.

    ```python
    gear = ttk.Icon("gear-fill", size=20, color="primary")
    ttk.Button(app, text="Settings", image=gear, compound="left").pack()
    ```

    Parameters:

        name (str):
            A Bootstrap Icons glyph name (e.g. "gear-fill", "check-square-fill").
            An unknown name raises `ValueError`.

        size (int | tuple[int, int]):
            The final pixel size (already DPI-scaled by the caller). Snapped to an
            even size internally.

        color (str):
            A bootstyle keyword ("primary", "success", "fg", ...) resolved against
            the active theme, or a hex string passed through. Defaults to the
            theme foreground.
    """
    from ttkbootstrap.style.engine import Style  # back-edge; keeps this a leaf

    style = Style.get_instance()
    color = style.colors.fg if color is None else _resolve_color(style, color)
    return Assets(style).icon(name, size, color)


def _spec_name(spec):
    """The icon name a per-state spec carries, or None if it inherits the default."""
    if isinstance(spec, str):
        return spec
    if isinstance(spec, dict):
        return spec.get("name")
    raise TypeError(
        f"icon spec must be a name string or a {{name?, color?}} dict, got {spec!r}"
    )


def _state_foreground(style, ttkstyle, state_string):
    """The configured foreground for `ttkstyle` in `state_string` (theme fg fallback).

    Image elements are baked bitmaps, not live text, so a spec that omits a color
    materializes it here from the style's already-configured `foreground` map --
    call `icon_element` *after* the `foreground` configure/map.
    """
    tokens = statespec(state_string)  # validates the grammar (loud on a typo)
    # A ttk lookup takes the *active* states, so negated tokens ("!selected") are
    # dropped -- an "off" state resolves against the base (no-state) foreground.
    lookup_state = [t for t in tokens if not t.startswith("!")]
    fg = style.lookup(ttkstyle, "foreground", state=lookup_state or None)
    return fg or style.colors.fg


def icon_element(style, name, *, size, default, states=None, **options):
    """Create a ttk image element whose per-state image is a Bootstrap Icons glyph.

    The `Style.map`-aligned analog of `image_element`, with the icon as the asset
    source: each per-state spec is rendered via `Icon`/`Assets.icon` and assembled
    into one validated, first-match-wins image element. One declarative call
    replaces a `create_*_assets` method plus its `image_element` wiring.

    `name` is the element name and must be `"<ttkstyle>.<element>"` (e.g.
    `"Favorite.TCheckbutton.indicator"`); the foreground a color-less spec follows
    is looked up on the `<ttkstyle>` prefix (`name` minus its last component).

    Per-state spec grammar (`default` and each `states` value):

      - **bare string** -> the icon *name*; its color **follows the foreground**
        configured for that state.
      - **dict `{name?, color?}`** -> `name` omitted = the `default` icon;
        `color` omitted = follows the foreground. `color` is a bootstyle keyword
        or a hex, resolved once against the active theme.

    ```python
    state_map(style, "Favorite.TCheckbutton", foreground={"disabled": "#888"})
    icon_element(style, "Favorite.TCheckbutton.indicator", size=20,
        default={"name": "star-fill", "color": "warning"},  # selected -> accent
        states={"!selected": "star"},                       # off -> follows fg
        border=4, sticky="w")
    ```

    `states` is an ordered dict; ttk matches its specs first-match-wins, so the
    insertion order *is* the match order. `options` (border, sticky, width, ...)
    pass through to `element_create`.
    """
    if "." not in name:
        raise ValueError(
            f"icon_element name must be '<ttkstyle>.<element>' (the foreground is "
            f"looked up on the ttkstyle prefix), got {name!r}")
    ttkstyle = name.rsplit(".", 1)[0]
    assets = Assets(style)

    default_name = _spec_name(default)
    if default_name is None:
        raise ValueError("icon_element 'default' must specify an icon name")

    def resolve(spec, state_string):
        icon_name = _spec_name(spec) or default_name
        color = spec.get("color") if isinstance(spec, dict) else None
        if color is None:
            color = _state_foreground(style, ttkstyle, state_string)
        else:
            color = _resolve_color(style, color)
        return assets.icon(icon_name, size, color)

    default_image = resolve(default, "")
    state_images = None
    if states:
        state_images = {s: resolve(spec, s) for s, spec in states.items()}
    image_element(style, name, default=default_image, states=state_images, **options)
