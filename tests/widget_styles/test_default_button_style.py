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
from ttkbootstrap.style.builders.utils import default_button_fill


def _tbutton_background(app):
    return str(app.tk.call("ttk::style", "lookup", "TButton", "-background")).lower()


def test_base_tbutton_themed_without_default_button(root):
    """The base ``TButton`` is themed at load, and follows theme changes,
    even when the app only ever creates a styled button.
    """
    style = root.style
    style.theme_use("sandstone-light")

    # Mirror the bug report: only a styled toolbutton is created.
    ttk.Button(root, text="Browse", style="Outline.Toolbutton")

    assert style.style_exists_in_theme("TButton"), \
        "base TButton should be built at theme load"

    # The base TButton uses the default_button fill (neutral by default), built
    # at load, and it must keep tracking the active theme.
    def expected_default():
        return str(default_button_fill(style._get_builder())).lower()

    assert _tbutton_background(root) == expected_default(), \
        "base TButton should use the default_button (neutral) fill"

    for theme in ("bootstrap-dark", "minty-light", "pydata-light"):
        style.theme_use(theme)
        assert _tbutton_background(root) == expected_default(), \
            f"base TButton did not follow change to {theme}"


def test_bare_button_is_neutral_by_default(root):
    """A bare `ttk.Button()` (no bootstyle) renders neutral, not primary."""
    style = root.style
    style.theme_use("bootstrap-light")
    assert style.default_button == "neutral"
    ttk.Button(root, bootstyle="neutral")  # build neutral.TButton to compare
    root.update_idletasks()
    neutral_bg = str(
        style.tk.call("ttk::style", "lookup", "neutral.TButton", "-background")
    ).lower()
    # the base (no-color) button matches the explicit neutral button...
    assert _tbutton_background(root) == neutral_bg
    # ...and is not the accent
    assert _tbutton_background(root) != str(style.colors.primary).lower()


def test_default_button_setting_opts_out_to_primary(root):
    """`default_button` drives the base fill: 'primary' restores the accent."""
    style = root.style
    builder = style._get_builder()
    before = style.default_button
    try:
        style.default_button = "primary"
        assert str(default_button_fill(builder)).lower() == \
            str(style.colors.primary).lower()
        style.default_button = "neutral"
        assert str(default_button_fill(builder)).lower() != \
            str(style.colors.primary).lower()
    finally:
        style.default_button = before