"""Regression tests for button-family follow-ups (2.0).

- the bare ``toggle`` bootstyle must build (it resolves to a ``Toggle`` style that
  the default toggle recipe previously never created -> "Layout Toggle not found")
- DateEntry's button carries the same hairline border as the other buttons
"""
import ttkbootstrap as ttk


def _lookup(app, style, option):
    return str(app.tk.call("ttk::style", "lookup", style, f"-{option}")).lower()


def test_bare_toggle_bootstyle_builds(root):
    """`bootstyle="toggle"` resolves to a real, laid-out `Toggle` style."""
    style = root.style
    cb = ttk.Checkbutton(root, text="t", bootstyle="toggle")
    root.update_idletasks()
    assert cb.cget("style") == "Toggle"
    assert style.style_exists_in_theme("Toggle")


def test_toggle_variants_all_build(root):
    """The default toggle and the explicit round/square variants all resolve."""
    for bootstyle, expected in (
        ("toggle", "Toggle"),
        ("round-toggle", "Round.Toggle"),
        ("square-toggle", "Square.Toggle"),
        ("primary-toggle", "primary.Toggle"),
    ):
        cb = ttk.Checkbutton(root, text=bootstyle, bootstyle=bootstyle)
        root.update_idletasks()
        assert cb.cget("style") == expected
        assert root.style.style_exists_in_theme(expected)


def test_ghost_button_is_transparent_with_accent_text(root):
    """A colored ghost button is borderless, surface-filled, accent-texted, and
    washes subtly on hover."""
    style = root.style
    ttk.Button(root, bootstyle="primary-ghost")
    root.update_idletasks()
    st = "primary.Ghost.TButton"
    # flat relief => no visible border (borderwidth is kept at 1 only to match the
    # solid/outline size; nothing is drawn)
    assert _lookup(root, st, "relief") == "flat"
    assert _lookup(root, st, "foreground") == str(style.colors.primary).lower()
    assert _lookup(root, st, "background") == str(style.colors.bg).lower()
    # hover wash is a subtle tint of the accent, distinct from both fg and surface
    hover = {tuple(i[:-1]): str(i[-1]).lower() for i in style.map(st, "background")}
    wash = hover[("hover", "!disabled")]
    assert wash not in (str(style.colors.bg).lower(), str(style.colors.primary).lower())


def test_ghost_is_a_canonical_bootstyle():
    import typing
    from ttkbootstrap.constants import BootStyle
    canonical = set(typing.get_args(BootStyle))
    assert "ghost" in canonical
    assert "primary ghost" in canonical


def test_dateentry_button_uses_icon_button_style(root):
    """DateEntry's button is a normal (icon-bearing) button, not a bespoke
    ``Date.TButton`` style -- the dedicated date-button recipe was removed once
    the button switched to the icon engine."""
    de = ttk.DateEntry(root)
    root.update_idletasks()
    # It resolves to an icon-derived variant of the bootstyle's TButton...
    assert de.button.cget("style").endswith(".TButton")
    # ...and the dead bespoke style is gone.
    assert not root.style.style_exists_in_theme("Date.TButton")
