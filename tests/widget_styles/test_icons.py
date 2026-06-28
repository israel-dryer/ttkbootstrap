"""Icon engine tests (2.0 Workstream I / PR 6a).

Covers the glyph renderer and its public surface in `ttkbootstrap.style.icons`:

- `IconRenderer.render` rasterizes a known glyph to a non-empty RGBA of the
  requested (even-snapped) size, and centers a metrics-present glyph in its frame;
- an unknown glyph name fails loudly (a typo is not a blank image);
- `Assets.icon` / `Icon` derive a complete, color-bearing cache key, so identical
  `(name, size, color)` dedupe to one Tcl image and a single differing color is a
  different image -- the PR 2 content-addressed invariant, with the resolved
  color in the key (theme-independent);
- `Icon`'s `color=` resolves a bootstyle keyword against the active theme;
- `icon_element` bakes a validated per-state image element from the icon specs.

The renderer needs no Tk root (it returns a PIL image); the cache/element tests
take the shared `root` fixture. `import ttkbootstrap` stays warning-free and does
not load the font.
"""
import pytest

import ttkbootstrap as ttk
from ttkbootstrap.style import Assets, Icon, icon_element, IconRenderer


def _cached_image(style, name):
    """The cached PhotoImage whose Tcl name is `name` (or None)."""
    for _key, (cached_name, image) in style._image_cache.items():
        if cached_name == name:
            return image
    return None


# --------------------------------------------------------------------------- #
# Renderer (pure -- no Tk root)
# --------------------------------------------------------------------------- #
def test_render_known_glyph_is_nonempty_rgba_of_even_size():
    img = IconRenderer.render("check-square-fill", (20, 20), "#3498db")
    assert img.mode == "RGBA"
    assert img.size == (20, 20)
    # something was actually drawn (the alpha channel has ink)
    assert img.getchannel("A").getbbox() is not None


def test_render_unknown_glyph_fails_loudly():
    with pytest.raises(ValueError):
        IconRenderer.render("definitely-not-a-real-glyph", 20, "#000000")


def test_metrics_present_glyph_centers_within_tolerance():
    # "square" is a full-bleed glyph with precomputed ink metrics; its ink must
    # land centered in the frame (the fit-and-center fix, not getbbox skew).
    size = 40
    img = IconRenderer.render("square", size, "#000000")
    left, top, right, bottom = img.getchannel("A").getbbox()
    cx, cy = (left + right) / 2, (top + bottom) / 2
    tol = size * 0.06  # ~2px at 40 -- covers the intentional small y-bias
    assert abs(cx - size / 2) <= tol
    assert abs(cy - size / 2) <= tol


def test_import_is_warning_free_and_font_lazy():
    # A fresh interpreter: importing the package (and the icons module) must not
    # warn, and must NOT read the font -- the renderer loads it on first render.
    # Run in a subprocess so the assertion is real (the in-process class caches
    # may already be populated by other tests).
    import subprocess
    import sys

    code = (
        "import warnings; warnings.simplefilter('error')\n"
        "import ttkbootstrap\n"
        "from ttkbootstrap.style.icons import IconRenderer\n"
        "assert IconRenderer._font_bytes is None, 'font loaded at import'\n"
        "print('ok')\n"
    )
    proc = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True)
    assert proc.returncode == 0, proc.stderr
    assert proc.stdout.strip() == "ok"


def test_render_falls_back_without_metrics(monkeypatch):
    # If icon_metrics.json is unavailable, render degrades to getbbox measuring
    # and still produces a non-empty, sized glyph (the safety net, not the path
    # normally taken since the vendored metrics cover the glyphmap).
    monkeypatch.setattr(IconRenderer, "_metrics", {})
    img = IconRenderer.render("square", 24, "#000000")
    assert img.size == (24, 24)
    assert img.getchannel("A").getbbox() is not None


# --------------------------------------------------------------------------- #
# Cache key completeness / Icon atom (need a root)
# --------------------------------------------------------------------------- #
def test_icon_key_completeness(root):
    a = Assets(root.style)
    n1 = a.icon("check-square-fill", 20, "#3498db")
    n2 = a.icon("check-square-fill", 20, "#3498db")
    n3 = a.icon("check-square-fill", 20, "#e74c3c")
    assert n1 == n2          # identical inputs -> cache hit -> same Tcl name
    assert n1 != n3          # one differing color -> different key -> different name


def test_icon_even_snaps_size(root):
    a = Assets(root.style)
    odd = a.icon("square", 15, "#000000")
    even = a.icon("square", 16, "#000000")
    assert odd == even       # 15 snaps up to 16 -> same image/key
    img = _cached_image(root.style, odd)
    assert (img.width(), img.height()) == (16, 16)


def test_icon_atom_resolves_color_keyword(root):
    # Icon("...", color="primary") must resolve the keyword against the active
    # theme and equal a call made with that resolved hex; a different keyword
    # (different color) must produce a different image.
    primary_hex = root.style.colors.primary
    by_keyword = Icon("gear-fill", size=20, color="primary")
    by_hex = Icon("gear-fill", size=20, color=primary_hex)
    by_other = Icon("gear-fill", size=20, color="danger")
    assert by_keyword == by_hex
    assert by_keyword != by_other


# --------------------------------------------------------------------------- #
# icon_element state map (need a root)
# --------------------------------------------------------------------------- #
def test_icon_element_builds_state_map(root):
    style = root.style
    # configure a foreground a color-less spec can follow
    style._build_configure("Fav.TCheckbutton", foreground=style.colors.fg)
    icon_element(style, "Fav.TCheckbutton.indicator", size=20,
                 default={"name": "star-fill", "color": "warning"},
                 states={"!selected": "star"},
                 border=4, sticky="w")
    # the element registered and is usable in a layout (round-trips through ttk)
    layout = [("Fav.TCheckbutton.indicator", {"side": "left"})]
    style.layout("Fav.TCheckbutton", layout)
    assert style.layout("Fav.TCheckbutton")


def test_icon_element_validates_state_grammar(root):
    style = root.style
    with pytest.raises(ValueError):
        icon_element(style, "Bad.TCheckbutton.indicator", size=20,
                     default="square", states={"diabled": "square"})


def test_icon_element_requires_qualified_name(root):
    # name must be '<ttkstyle>.<element>' so the foreground can be looked up on
    # the ttkstyle prefix; a dotless name fails loud instead of silently.
    with pytest.raises(ValueError):
        icon_element(root.style, "indicator", size=20, default="square")
