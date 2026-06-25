"""Regression test for issue #1062.

ttkbootstrap builds widget styles lazily, so the base ``TButton`` style
used to be configured only when the app created a *default* ``ttk.Button``.
Native ttk widgets the app never instantiates directly -- such as the
``ttk::button`` widgets inside Tk's file/message dialogs on Linux -- rely
on that base style. An app that created only styled buttons (e.g.
``Outline.Toolbutton``) therefore left ``TButton`` unthemed, and any
linked dialog lost its button coloring.

The base ``TButton`` style must now be themed at theme-load time, even
when the application never creates a plain button, and it must follow
runtime theme changes.

Runnable headlessly with pytest.
"""
import ttkbootstrap as ttk


def _tbutton_background(app):
    return str(app.tk.call("ttk::style", "lookup", "TButton", "-background")).lower()


def test_base_tbutton_themed_without_default_button(root):
    """The base ``TButton`` is themed at load, and follows theme changes,
    even when the app only ever creates a styled button.
    """
    style = root.style
    style.theme_use("sandstone")

    # Mirror the bug report: only a styled toolbutton is created.
    ttk.Button(root, text="Browse", style="Outline.Toolbutton")

    assert style.style_exists_in_theme("TButton"), \
        "base TButton should be built at theme load"
    assert _tbutton_background(root) == str(style.colors.primary).lower(), \
        "base TButton should use the theme's primary color"

    # The base style must keep tracking the active theme.
    for theme in ("superhero", "flatly", "litera"):
        style.theme_use(theme)
        assert _tbutton_background(root) == str(style.colors.primary).lower(), \
            f"base TButton did not follow change to {theme}"