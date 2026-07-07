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


def test_date_button_has_hairline_border(root):
    """DateEntry's button gets the same fill-derived border as other buttons."""
    style = root.style
    ttk.DateEntry(root)
    root.update_idletasks()
    border = _lookup(root, "Date.TButton", "bordercolor")
    assert border, "date button must have a border"
    # a distinct edge derived from the fill, not the raw fill
    assert border != _lookup(root, "Date.TButton", "background")
    assert _lookup(root, "Date.TButton", "relief") == "raised"
