"""Headless tests for theme-aware widget icons (apply_icon + icon=/icon_size=).

Covers the parts checkable without a display:
- apply_icon gives the widget a derived, image-bearing style,
- inverting styles (outline) render on-accent when active (foreground-follow),
- a theme switch re-renders the glyph (the <<ThemeChanged>> bind),
- the states= per-state glyph override,
- clearing restores the base style; unsupported widgets raise,
- the mixin icon=/icon_size= sugar composes with bootstyle and re-derives,
- content-hashed derived styles dedupe across identical widgets,
- apply_icon is re-exported, and the datepicker carets use the path.
"""
import pytest

import ttkbootstrap as ttk
from ttkbootstrap import apply_icon
from ttkbootstrap.style import apply_icon as apply_icon_style


def _img(style, style_name, state=None):
    return style.lookup(style_name, "image", state=state)


# --------------------------------------------------------------------------
# apply_icon primitive
# --------------------------------------------------------------------------

def test_apply_icon_sets_derived_image_style(root):
    b = ttk.Button(root, text="Settings", bootstyle="primary")
    derived = apply_icon(b, "gear-fill", size=16)
    assert b.cget("style") == derived
    assert derived.startswith("Icon")
    assert derived.endswith("primary.TButton")
    assert _img(root.style, derived)  # image configured
    assert str(root.style.lookup(derived, "compound")) == "left"  # text kept


def test_apply_icon_outline_inverts_when_active(root):
    b = ttk.Button(root, bootstyle="primary-outline")
    derived = apply_icon(b, "funnel-fill", size=16)
    rest = _img(root.style, derived)
    pressed = _img(root.style, derived, state=["pressed", "!disabled"])
    # rest follows the accent fg; pressed follows the on-accent fg -> different image
    assert rest != pressed


def test_apply_icon_rerenders_on_theme_change(root):
    # a bare button follows colors.fg, which flips between light and dark themes
    b = ttk.Button(root, text="x")
    apply_icon(b, "gear-fill", size=16)
    before = _img(root.style, b.cget("style"))
    root.style.theme_use("bootstrap-dark")
    root.update()  # process <<ThemeChanged>>
    after = _img(root.style, b.cget("style"))
    assert before != after


def test_apply_icon_states_glyph_override(root):
    b = ttk.Checkbutton(root, text="Fav", bootstyle="warning")
    derived = apply_icon(b, "star", size=16, states={"selected": "star-fill"})
    rest = _img(root.style, derived)
    selected = _img(root.style, derived, state=["selected"])
    assert rest != selected


def test_apply_icon_none_restores_base(root):
    b = ttk.Button(root, bootstyle="primary")
    apply_icon(b, "gear-fill")
    assert b.cget("style").startswith("Icon")
    assert apply_icon(b, None) is None
    assert b.cget("style") == "primary.TButton"
    assert getattr(b, "_tb_icon", None) is None


def test_apply_icon_unsupported_widget_raises(root):
    with pytest.raises(TypeError):
        apply_icon(ttk.Entry(root), "gear-fill")


def test_apply_icon_dedupes_identical_configs(root):
    a = ttk.Button(root, bootstyle="primary")
    b = ttk.Button(root, bootstyle="primary")
    sa = apply_icon(a, "gear-fill", size=16)
    sb = apply_icon(b, "gear-fill", size=16)
    assert sa == sb  # same (base, glyph, size) -> one content-hashed style


# --------------------------------------------------------------------------
# mixin sugar
# --------------------------------------------------------------------------

def test_icon_kwarg_on_constructor(root):
    b = ttk.Button(root, text="Save", bootstyle="primary", icon="floppy", icon_size=18)
    assert b.cget("style").startswith("Icon")
    assert b._tb_icon["name"] == "floppy"
    assert b._tb_icon["size"] == 18
    assert _img(root.style, b.cget("style"))


def test_bootstyle_change_rederives_icon(root):
    b = ttk.Button(root, bootstyle="primary", icon="floppy")
    b.configure(bootstyle="danger")
    style_name = b.cget("style")
    assert style_name.endswith("danger.TButton")
    assert _img(root.style, style_name)  # icon carried onto the new base


def test_configure_icon_change_and_clear(root):
    b = ttk.Button(root, bootstyle="primary", icon="floppy")
    b.configure(icon="trash")
    assert b._tb_icon["name"] == "trash"
    b.configure(icon_size=24)
    assert b._tb_icon["size"] == 24
    b.configure(icon=None)
    assert b.cget("style") == "primary.TButton"
    assert getattr(b, "_tb_icon", None) is None


# --------------------------------------------------------------------------
# re-exports + first-party dogfood
# --------------------------------------------------------------------------

def test_apply_icon_reexports():
    assert apply_icon is apply_icon_style
    assert "apply_icon" in ttk.__all__


def test_datepicker_carets_use_apply_icon(root):
    # autoshow=False builds the widget tree (incl. _update_widget_bootstyle) in
    # __init__ without the modal show()/wait_window, so this stays headless.
    from ttkbootstrap.dialogs.datepicker import DatePickerDialog
    dp = DatePickerDialog(parent=root, autoshow=False)
    try:
        assert dp.prev_period.cget("style").startswith("Icon")
        assert dp.next_period.cget("style").startswith("Icon")
        assert getattr(dp.prev_period, "_tb_icon", None)
    finally:
        dp.root.destroy()


# --------------------------------------------------------------------------
# icon_only: square, same height as a normal button; explicit overrides win
# --------------------------------------------------------------------------

def test_icon_only_is_square_and_matches_normal_height(root):
    normal = ttk.Button(root, text="Normal")
    normal.pack()
    only = ttk.Button(root, icon="gear-fill", icon_only=True)
    only.pack()
    root.update_idletasks()
    w, h = only.winfo_reqwidth(), only.winfo_reqheight()
    assert abs(w - h) <= 1                                  # square (exact)
    assert abs(h - normal.winfo_reqheight()) <= 1           # same height (exact)
    # compound is image-only (text hidden)
    assert str(root.style.lookup(only.cget("style"), "compound")) == "image"


def test_icon_only_is_always_square_but_size_override_changes_the_control(root):
    # Icon-only uses a fixed default (size, padding) pair, so the default is a
    # square ~a normal button's height; it stays square at any size, but an
    # explicit icon_size deliberately changes the control's size (not forced).
    for size in (12, 16, 20, 24):
        b = ttk.Button(root, icon="gear-fill", icon_only=True, icon_size=size)
        b.pack()
        root.update_idletasks()
        w, h = b.winfo_reqwidth(), b.winfo_reqheight()
        assert abs(w - h) <= 1, f"size={size} not square: {w}x{h}"
    small = ttk.Button(root, icon="gear-fill", icon_only=True, icon_size=12)
    big = ttk.Button(root, icon="gear-fill", icon_only=True, icon_size=24)
    small.pack()
    big.pack()
    root.update_idletasks()
    assert big.winfo_reqheight() > small.winfo_reqheight()  # size is not forced


def test_icon_only_explicit_padding_wins(root):
    # A widget `padding=` (instance option) overrides the icon_only style padding.
    b = ttk.Button(root, icon="gear-fill", icon_only=True, padding=(12, 2))
    b.pack()
    root.update_idletasks()
    assert b.cget("padding") == (12, 2)


def test_icon_only_via_configure_toggles(root):
    normal = ttk.Button(root, text="N")
    normal.pack()
    root.update_idletasks()
    H = normal.winfo_reqheight()
    b = ttk.Button(root, icon="gear-fill", text="Settings")
    b.pack()
    root.update_idletasks()
    wide = b.winfo_reqwidth()
    b.configure(icon_only=True)
    root.update_idletasks()
    assert abs(b.winfo_reqwidth() - b.winfo_reqheight()) <= 3   # now square
    assert abs(b.winfo_reqheight() - H) <= 2
    b.configure(icon="bell-fill")                               # icon_only persists
    root.update_idletasks()
    assert abs(b.winfo_reqwidth() - b.winfo_reqheight()) <= 3
    b.configure(icon_only=False)                               # back to icon+text
    root.update_idletasks()
    assert b.winfo_reqwidth() > b.winfo_reqheight()


def test_icon_only_recomputes_on_theme_change(root):
    b = ttk.Button(root, icon="gear-fill", icon_only=True)
    b.pack()
    root.update_idletasks()
    before = (b.winfo_reqwidth(), b.winfo_reqheight())
    root.style.theme_use("bootstrap-dark")
    root.update()
    after = (b.winfo_reqwidth(), b.winfo_reqheight())
    assert abs(after[0] - after[1]) <= 3           # still square after switch
    assert abs(before[1] - after[1]) <= 2          # height stable


def test_icon_only_without_icon_warns(root):
    with pytest.warns(UserWarning, match="icon_only"):
        ttk.Button(root, icon_only=True, text="x")
