"""Tests for the thin scrollbar variant (2.0).

A thin scrollbar is a few-pixel flat thumb on a surface-matched track with no
arrows -- for narrow lists/dropdowns (combobox popdown, font dialog). Neutral by
default, or the accent when a color is given. See
`development/2_0_breaking_changes.md`.
"""
import ttkbootstrap as ttk


def _lookup(app, style, option):
    return str(app.tk.call("ttk::style", "lookup", style, f"-{option}")).lower()


def test_thin_scrollbar_builds_arrowless_on_the_surface(root):
    """`bootstyle="thin"` builds a vertical + horizontal arrowless scrollbar
    whose track matches the surface."""
    style = root.style
    ttk.Scrollbar(root, orient="vertical", bootstyle="thin")
    ttk.Scrollbar(root, orient="horizontal", bootstyle="thin")
    root.update_idletasks()
    for st in ("Thin.Vertical.TScrollbar", "Thin.Horizontal.TScrollbar"):
        assert style.style_exists_in_theme(st)
        assert _lookup(root, st, "arrowsize") in ("0", "")
        assert _lookup(root, st, "troughcolor") == str(style.colors.bg).lower()


def test_thin_scrollbar_accepts_a_color(root):
    """A colored thin scrollbar builds its own style."""
    style = root.style
    ttk.Scrollbar(root, orient="vertical", bootstyle="primary-thin")
    root.update_idletasks()
    assert style.style_exists_in_theme("primary.Thin.Vertical.TScrollbar")
