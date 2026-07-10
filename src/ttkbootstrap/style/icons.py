"""Bootstrap Icons glyph rendering for ttkbootstrap styles.

`IconRenderer` rasterizes a single named glyph from the vendored Bootstrap Icons
font (`assets/icons/`) to a PIL image, using a precomputed per-glyph ink box to
fit-and-center it accurately. Pillow's `font.getbbox()` under-reports the ink of
full-bleed icon glyphs, which skews sizing/centering; `icon_metrics.json` instead
carries each glyph's true inked bounds (in em-fractions) measured offline, so the
renderer fits the real ink to the frame with no per-glyph fudge.

The public surface layered on top:

  - `Icon(name, size, color)` -- the atom: render one glyph to a cached Tk image
    usable directly as `image=`. `color` is a bootstyle keyword or a hex,
    resolved once against the active theme.
  - `icon_element(style, name, ...)` -- style-level sugar that maps a glyph per
    ttk widget state and bakes a validated image element (the `Style.map`-aligned
    analog of `image_element`, with the icon as the asset source).

Asset loading is lazy: `import ttkbootstrap` does not read the font --
`IconRenderer` loads it on first `render`.
"""
import hashlib
import io
import json
import re
import tkinter as tk
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont
from PIL.Image import Resampling

from ttkbootstrap.style.assets import Assets
from ttkbootstrap.style.layout import statespec, image_element


# The vendored Bootstrap Icons assets ship as package data next to this package
# (see assets/icons/README.md). Resolved relative to this file so it works from
# an installed wheel, not just the src tree.
_ICONS_DIR = Path(__file__).parent.parent / "assets" / "icons"

# A small downward nudge -- icon fonts sit slightly high in their em box; this
# and the small inner pad keep glyphs optically centered in a square frame. The
# pad is kept low (4%): at button-icon sizes (~16px) a larger pad renders the
# glyph at only ~80% of the frame, starving thin strokes of pixels and reading
# blurry -- 4% lets the glyph nearly fill the frame and stay crisp.
_ICON_Y_BIAS = 0.02
_ICON_PAD_FACTOR = 0.04


def _physical_size(size):
    """Normalize an exact physical scalar or pair to `(width, height)`."""
    if isinstance(size, (int, float)):
        return int(size), int(size)
    return int(size[0]), int(size[1])


def _icon_oversample(w, h):
    """Supersample factor for a glyph of size `(w, h)` -- richer than the
    geometric recipes' 3/2/1 (`assets._oversample`).

    Glyph outlines (circle/chevron) carry thin curved strokes; the smoothness of
    those curves is set by the *supersample*, not the sharpen -- a hard sharpen
    just stair-steps them. Samples are pushed high (6x) for the small indicator
    tier and paired with a gentle UnsharpMask (see `render`), keeping curves
    smooth and straight strokes defined without pixelating the rings.
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
        crispness (shared with `assets._render`).

        Raises `ValueError` for a name absent from the Bootstrap Icons glyphmap
        (a typo fails loudly rather than rendering a blank image).
        """
        w, h = _physical_size(size)
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
            # Snap the draw origin to whole pixels (the fallback branch already
            # does via //) so the ink lands on the grid rather than half-pixels,
            # which softens straight strokes on the LANCZOS downscale.
            dx = round((cw - ink_w) / 2 - nl * font_size)
            dy = round((ch - ink_h) / 2 - nt * font_size + ch * _ICON_Y_BIAS)
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
            The logical UI size. It is converted once by the root-bound service;
            final dimensions may be odd.

        color (str | None):
            A bootstyle keyword ("primary", "success", "fg", ...) resolved against
            the active theme, or a hex string passed through. `None` (the
            default) resolves to the theme foreground.
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
    into one validated, first-match-wins image element.

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
    insertion order *is* the match order. Numeric `border`, `padding`, `width`,
    and `height` options are logical UI units and convert with the image frame;
    other options pass through to `element_create`.
    """
    if "." not in name:
        raise ValueError(
            f"icon_element name must be '<ttkstyle>.<element>' (the foreground is "
            f"looked up on the ttkstyle prefix), got {name!r}")
    ttkstyle = name.rsplit(".", 1)[0]
    assets = Assets(style)
    for option in ("border", "padding", "width", "height"):
        value = options.get(option)
        if isinstance(value, (int, float, tuple, list)):
            options[option] = assets.scaling.logical(value, minimum=1)

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


# --------------------------------------------------------------------------- #
# Theme-aware widget icons (apply_icon)
# --------------------------------------------------------------------------- #
# ttk classes whose layout has a label element that renders the style `image`
# option + honors `compound`. apply_icon works on these; anything else silently
# no-ops at the Tcl level, so we class-check and raise instead.
_ICON_WIDGET_CLASSES = frozenset({
    "TButton", "Toolbutton", "TLabel", "TMenubutton",
    "TCheckbutton", "TRadiobutton",
})

#: Default logical glyph size for a normal icon (icon + text).
_ICON_SIZE = 14
#: Default logical glyph size + symmetric padding for an icon-only widget. The
#: pair is chosen once for the expected height: a button is
#: ``content + 2*padding + chrome``, and a normal button (text lineheight ~15,
#: base padding 4, chrome ~6) is ~29 px, so ``size + 2*padding = 23`` lands an
#: icon-only square on that same height. 17 + 2*3 = 23 -> a compact square the
#: height of a normal button, with a glyph a touch larger than the text line.
#: Both are logical units (DPI-scaled). Explicit ``icon_size=`` / ``padding=``
#: override them, and then the control's size changes to match (by design).
_ICON_ONLY_SIZE = 17
_ICON_ONLY_PADDING = 3

# A derived icon style is named "Icon<8 hex>.<base style>"; this strips the
# prefix back to the base so re-applies are idempotent.
_ICON_STYLE_PREFIX = re.compile(r"^Icon[0-9a-f]{8}\.")


def _icon_base_style(widget):
    """The widget's current style with any Icon<hash>. prefix removed.

    Falls back to the widget's ttk class (e.g. ``TButton``) when no style is set.
    """
    current = _ICON_STYLE_PREFIX.sub("", str(widget.cget("style") or ""))
    return current or widget.winfo_class()


def _widget_has_text(widget):
    try:
        return bool(str(widget.cget("text") or ""))
    except tk.TclError:
        return False


def _build_icon_style(style, base, name, size, states, compound, icon_only=False):
    """(Re)configure a derived ``Icon<hash>.<base>`` style and return its name.

    Renders one glyph per state in that state's *base foreground* color (so the
    icon inverts / mutes exactly as the label text does); ``states`` overrides the
    glyph name per state, never its color. The images are set as the derived
    style's ``image`` option + map, which the inherited ``*.label`` element renders
    (the built-in date-button pattern -- no custom element/layout). configure/map
    overwrite, so a theme-change rebuild is just a re-call (idempotent).
    """
    assets = Assets(style)
    states = states or {}

    # icon-only: image-only compound + the fixed symmetric padding chosen (with
    # the default size) so the default control is a square ~a normal button's
    # height. Fixed, not derived: an explicit size/padding just changes the size.
    padding = None
    if icon_only:
        compound = "image"  # ttk compound value; no tkinter constant for it
        padding = assets.scaling.logical(_ICON_ONLY_PADDING)

    key = f"{base}|{name}|{size}|{sorted(states.items())}|{compound}|{padding}"
    digest = hashlib.md5(key.encode("utf-8")).hexdigest()[:8]
    derived = f"Icon{digest}.{base}"

    def render(glyph, state_tokens):
        color = style.lookup(base, "foreground", state=state_tokens or None)
        return assets.icon(glyph, size, color or style.colors.fg)

    rest_image = render(states.get("", name), [])

    image_map = []
    seen = set()
    for entry in style.map(base, "foreground"):
        *tokens, _color = entry
        state_str = " ".join(tokens)
        if not tokens or state_str in seen:
            continue
        seen.add(state_str)
        image_map.append((state_str, render(states.get(state_str, name), tokens)))
    # states= keys the base foreground map doesn't remap still need an image
    for state_str, glyph in states.items():
        if state_str and state_str not in seen:
            seen.add(state_str)
            image_map.append((state_str, render(glyph, state_str.split())))

    config = {"image": rest_image}
    if compound is not None:
        config["compound"] = compound
    if padding is not None:
        config["padding"] = padding
    style.configure(derived, **config)
    if image_map:
        style.map(derived, image=image_map)
    return derived


def _set_icon_style(widget, derived):
    """Set the widget's style to ``derived``, guarding `BootMixin.configure` from
    re-deriving the icon on the resulting style change (which would recurse)."""
    widget._tb_applying_icon = True
    try:
        widget.configure(style=derived)
    finally:
        widget._tb_applying_icon = False


def _rebuild_widget_icon(widget):
    """Re-render a widget's icon for the active theme (``<<ThemeChanged>>``)."""
    spec = getattr(widget, "_tb_icon", None)
    if not spec:
        return
    from ttkbootstrap.style.engine import Style  # back-edge; keeps this a leaf
    style = Style.get_instance()
    if style is None:
        return
    try:
        derived = _build_icon_style(
            style, spec["base"], spec["name"], spec["size"],
            spec["states"], spec["compound"], spec.get("icon_only", False),
        )
        _set_icon_style(widget, derived)
    except tk.TclError:
        pass  # widget torn down mid-switch


def _clear_widget_icon(widget):
    """Remove an applied icon: restore the base style, drop the theme bind."""
    spec = getattr(widget, "_tb_icon", None)
    # Clear the spec *before* restoring the base style: the configure() below
    # routes through BootMixin.configure, whose base-change branch would otherwise
    # see a live _tb_icon and re-derive the icon we are removing.
    widget._tb_icon = None
    if spec is not None:
        base = spec["base"]
        try:
            widget.configure(
                style="" if base == widget.winfo_class() else base)
        except tk.TclError:
            pass
    bindid = getattr(widget, "_tb_icon_bindid", None)
    if bindid is not None:
        try:
            widget.unbind("<<ThemeChanged>>", bindid)
        except tk.TclError:
            pass
        widget._tb_icon_bindid = None
    return None


def apply_icon(widget, name, *, size=None, states=None, compound=None,
               icon_only=False):
    """Put a theme-aware Bootstrap Icons glyph on ``widget``.

    Unlike a bare `Icon(...)` used as ``image=``, this tracks the active theme and
    the widget's states: the glyph color follows the widget's style ``foreground``,
    so it inverts on ``outline``/``toggle`` buttons, mutes when disabled, and
    re-colors on a theme switch. It does so by giving the widget a derived,
    content-hashed style that augments (inherits) its current ``style``/
    ``bootstyle``.

    Parameters:

        widget:
            A ttk ``Button`` (incl. Toolbutton/Outline/link/ghost variants),
            ``Label``, ``Menubutton``, ``Checkbutton``, or ``Radiobutton``. Any
            other class raises ``TypeError`` (it has no image-bearing label
            element; use a per-item image API for Treeview/Notebook).

        name (str | None):
            A Bootstrap Icons glyph name (e.g. ``"gear-fill"``). ``None``/``""``
            removes the icon and restores the base style.

        size (int | tuple[int, int]):
            The logical UI size (converted by the root-bound scaling service).

        states (dict[str, str] | None):
            Optional ``{state_string: glyph_name}`` to show a *different glyph*
            per state (e.g. ``{"selected": "check-square-fill"}``). The color still
            follows the foreground. State strings are ttk state specs
            (``"disabled"``, ``"pressed !disabled"``, ...).

        compound (str | None):
            The ttk ``-compound`` option (icon/text arrangement). Defaults to
            ``LEFT`` when the widget has text, else icon-only. Ignored (forced to
            ``IMAGE``) when ``icon_only`` is set.

        icon_only (bool):
            Render the widget as an icon-only control: hide any text
            (``compound=IMAGE``) and give it a symmetric padding that makes it a
            square the same height as a normal widget. The default glyph is a
            touch larger; an explicit ``size`` (and a widget ``padding=`` option,
            which wins over the style) still take precedence.

    Returns the derived ttk style name, or ``None`` when the icon was cleared.
    """
    from ttkbootstrap.style.engine import Style  # back-edge; keeps this a leaf

    style = Style.get_instance() or Style()

    if not name:
        return _clear_widget_icon(widget)

    if widget.winfo_class() not in _ICON_WIDGET_CLASSES:
        raise TypeError(
            f"apply_icon: {widget.winfo_class()!r} has no image-bearing label "
            f"element. Supported: Button, Label, Menubutton, Checkbutton, "
            f"Radiobutton. (Treeview/Notebook take images via their own per-item "
            f"API, not a widget-level style.)"
        )

    if size is None:
        size = _ICON_ONLY_SIZE if icon_only else _ICON_SIZE
    if not icon_only and compound is None and _widget_has_text(widget):
        compound = tk.LEFT

    base = _icon_base_style(widget)
    derived = _build_icon_style(style, base, name, size, states, compound,
                                icon_only)
    _set_icon_style(widget, derived)

    # remember the spec so a <<ThemeChanged>> (or a bootstyle change that re-calls
    # apply_icon) can rebuild the glyphs for the new theme
    widget._tb_icon = {
        "base": base, "name": name, "size": size,
        "states": states, "compound": compound, "icon_only": icon_only,
    }
    # single bind: replace, never stack, on repeated apply_icon calls
    old = getattr(widget, "_tb_icon_bindid", None)
    if old is not None:
        try:
            widget.unbind("<<ThemeChanged>>", old)
        except tk.TclError:
            pass
    widget._tb_icon_bindid = widget.bind(
        "<<ThemeChanged>>", lambda _e: _rebuild_widget_icon(widget), "+")
    return derived
