"""Style-construction toolkit tests (2.0 Workstream I / PR 5).

Covers the public helpers in `ttkbootstrap.style.assets` / `.layout`:

- the shape recipes derive a complete, color-bearing cache key (so identical
  inputs dedupe and a single differing color is a different image);
- the even-pixel snap (an odd logical size and the next even one resolve to the
  same image, and the rendered image is even-sized) -- bootstack's fractional-DPI
  fix; `rect` is exempt and keeps its exact size;
- the `image` escape hatch keys on its declared `*key_parts`;
- `El` lowers to ttk's nested `(name, opts)` tuple form;
- `statespec` validates the state grammar (and raises on a typo);
- `StyleName` performs the DEFAULT/""->PRIMARY, `.TS->.S`, color-prefix dance.

The new public names import warning-free from both `ttkbootstrap` and
`ttkbootstrap.style`.
"""
import pytest

import ttkbootstrap as ttk
from ttkbootstrap.constants import PRIMARY
from ttkbootstrap.style import (
    Assets, El, layout, register_style, image_element, statespec, state_map,
    StyleName,
)


def _cached_image(style, name):
    """The cached PhotoImage whose Tcl name is `name` (or None)."""
    for _key, (cached_name, image) in style._image_cache.items():
        if cached_name == name:
            return image
    return None


# --------------------------------------------------------------------------- #
# Pure helpers (no Tk root required)
# --------------------------------------------------------------------------- #
def test_statespec_splits_and_validates():
    assert statespec("disabled selected") == ("disabled", "selected")
    assert statespec("!selected") == ("!selected",)
    assert statespec("hover !disabled") == ("hover", "!disabled")
    assert statespec("") == ()


def test_statespec_raises_on_typo():
    with pytest.raises(ValueError):
        statespec("diabled")
    with pytest.raises(ValueError):
        statespec("!notastate")
    with pytest.raises(ValueError):
        statespec("disabled seelcted")


def test_el_lowers_to_ttk_tuple():
    tree = El("Radiobutton.padding", sticky="nsew", children=[
        El("X.indicator", side="left", sticky=""),
        El("Radiobutton.focus", side="left", sticky="", children=[
            El("Radiobutton.label", sticky="nsew")])])
    assert tree.spec() == (
        "Radiobutton.padding",
        {"sticky": "nsew", "children": [
            ("X.indicator", {"side": "left", "sticky": ""}),
            ("Radiobutton.focus", {"side": "left", "sticky": "", "children": [
                ("Radiobutton.label", {"sticky": "nsew"})]})]})


def test_el_expand_and_border_options():
    assert El("a", expand=1).spec() == ("a", {"expand": 1})
    assert El("a", border=4).spec() == ("a", {"border": 4})
    assert El("a").spec() == ("a", {})


def test_stylename_default_to_primary():
    sn = StyleName("TRadiobutton")
    assert sn.colorname == PRIMARY
    assert sn.ttkstyle == sn.ttk_style
    assert sn.ttk_style == "TRadiobutton"
    assert sn.element == "Radiobutton"

    empty = StyleName("TRadiobutton", "")
    assert empty.colorname == PRIMARY
    assert empty.ttk_style == "TRadiobutton"


def test_stylename_color_and_orient():
    sn = StyleName("TScale", "info", orient="Horizontal")
    assert sn.colorname == "info"
    assert sn.ttk_style == "info.Horizontal.TScale"
    assert sn.element == "info.Horizontal.Scale"  # .TS -> .S

    default = StyleName("TScale", orient="Horizontal")
    assert default.ttk_style == "Horizontal.TScale"
    assert default.element == "Horizontal.Scale"


# --------------------------------------------------------------------------- #
# Recipes against the live image cache (need a root)
# --------------------------------------------------------------------------- #
def test_circle_key_completeness(root):
    a = Assets(root.style)
    n1 = a.circle("#ff0000", 16)
    n2 = a.circle("#ff0000", 16)
    n3 = a.circle("#00ff00", 16)
    assert n1 == n2          # identical inputs -> cache hit -> same image name
    assert n1 != n3          # one differing color -> different key -> different name


def test_circle_outline_and_width_in_key(root):
    a = Assets(root.style)
    plain = a.circle("#ff0000", 16)
    outlined = a.circle("#ff0000", 16, outline="#000000", width=2)
    assert plain != outlined


def test_even_size_snap(root):
    a = Assets(root.style)
    odd = a.circle("#123456", 15)
    even = a.circle("#123456", 16)
    assert odd == even       # 15 snaps up to 16 -> same image/key
    img = _cached_image(root.style, odd)
    assert (img.width(), img.height()) == (16, 16)  # rendered size is even


def test_rect_keeps_exact_size(root):
    a = Assets(root.style)
    name = a.rect("#abcdef", (40, 5))
    img = _cached_image(root.style, name)
    # solid fill has no edges to blur, so it is exempt from the even snap
    assert (img.width(), img.height()) == (40, 5)


def test_image_escape_hatch_keys_on_parts(root):
    a = Assets(root.style)

    def draw(d, w, h):
        d.ellipse((0, 0, w - 1, h - 1), fill="#111111")

    n1 = a.image(16, draw, "#111111")
    n2 = a.image(16, draw, "#111111")
    n3 = a.image(16, draw, "#222222")
    assert n1 == n2          # same qualname + key parts -> dedup
    assert n1 != n3          # differing key part -> different image


# --------------------------------------------------------------------------- #
# Element / map wrappers against a real style
# --------------------------------------------------------------------------- #
def test_image_element_validates_states(root):
    a = Assets(root.style)
    img = a.circle("#ffffff", 16)
    with pytest.raises(ValueError):
        image_element(root.style, "Bad.indicator", default=img,
                      states={"diabled": img})


def test_state_map_validates_states(root):
    with pytest.raises(ValueError):
        state_map(root.style, "TButton", foreground={"diabled": "#000000"})


def test_layout_applies_el_tree(root):
    # building a radiobutton exercises image_element + state_map + layout end to
    # end; the style must register and round-trip through ttk's layout query.
    rb = ttk.Radiobutton(root, bootstyle="success")
    rb.pack()
    root.update_idletasks()
    spec = root.style.layout("success.TRadiobutton")
    assert spec  # a non-empty, applied layout


# --------------------------------------------------------------------------- #
# Public style registration (the PR-6a finding: a hand-built style applied via
# style="..." is silently re-resolved to its base unless registered)
# --------------------------------------------------------------------------- #
def test_register_style_marks_style_known(root):
    style = root.style
    name = "Custom.TButton"
    assert not style.style_exists_in_theme(name)
    register_style(style, name)
    assert style.style_exists_in_theme(name)


def test_layout_auto_registers(root):
    # layout() is the terminal step of a hand-built style; it should register the
    # name itself so style="..." resolves with no extra call.
    style = root.style
    name = "Auto.TButton"
    assert not style.style_exists_in_theme(name)
    layout(style, name, El("Button.padding", sticky="nsew", children=[
        El("Button.label", sticky="nsew")]))
    assert style.style_exists_in_theme(name)


def test_registered_style_is_honored_via_style_kwarg(root):
    # The finding end-to-end: BootMixin honors style="X" only for a registered
    # style, else it re-resolves to the base. A toolkit-built style whose terminal
    # step is layout() must therefore survive on the widget unchanged.
    style = root.style
    name = "Fancy.TButton"
    layout(style, name, El("Button.padding", sticky="nsew", children=[
        El("Button.label", sticky="nsew")]))
    btn = ttk.Button(root, style=name)
    btn.pack()
    root.update_idletasks()
    assert btn.cget("style") == name
