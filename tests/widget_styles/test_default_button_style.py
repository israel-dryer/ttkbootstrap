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

Runnable headlessly with pytest, or directly as a script.
"""
import ttkbootstrap as ttk
from ttkbootstrap.style import Style


def _tbutton_background(app):
    return str(app.tk.call("ttk::style", "lookup", "TButton", "-background")).lower()


def test_base_tbutton_themed_without_default_button():
    """The base ``TButton`` is themed at load, and follows theme changes,
    even when the app only ever creates a styled button.

    A single Tk root is used because ttkbootstrap's ``Style`` is a
    singleton; creating multiple roots in one process is unsupported.
    """
    app = ttk.Window(themename="sandstone")
    app.withdraw()
    style = Style.get_instance()
    try:
        # Mirror the bug report: only a styled toolbutton is created.
        ttk.Button(app, text="Browse", style="Outline.Toolbutton")

        assert style.style_exists_in_theme("TButton"), \
            "base TButton should be built at theme load"
        assert _tbutton_background(app) == str(style.colors.primary).lower(), \
            "base TButton should use the theme's primary color"

        # The base style must keep tracking the active theme.
        for theme in ("superhero", "flatly", "litera"):
            style.theme_use(theme)
            assert _tbutton_background(app) == str(style.colors.primary).lower(), \
                f"base TButton did not follow change to {theme}"
    finally:
        app.destroy()


if __name__ == "__main__":
    test_base_tbutton_themed_without_default_button()
    print("All default-button-style regression tests passed.")