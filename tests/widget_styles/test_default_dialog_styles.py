"""Regression test for issue #1224 (companion to #1062 / test_default_button_style).

Tk's native file/directory dialogs on X11 are built from base ttk styles
(``TEntry``, ``TCombobox``, ``TMenubutton``, the scrollbars) the application
may never instantiate. Unbuilt, those styles inherit the theme foreground from
the root style but keep clam's light field/fill -- near-white text on a white
entry field in dark mode. The dialog set must be themed at theme-load time,
with no widget created, and follow runtime theme changes.

Runnable headlessly with pytest.
"""
import ttkbootstrap as ttk

DIALOG_STYLES = (
    "TButton",
    "TEntry",
    "TCombobox",
    "TMenubutton",
    "Vertical.TScrollbar",
    "Horizontal.TScrollbar",
)


def _lookup(app, style_name, option):
    return str(app.tk.call("ttk::style", "lookup", style_name, f"-{option}"))


def test_dialog_base_styles_built_at_theme_load(root):
    """Every base style a native dialog uses is built with no widget created."""
    style = root.style
    style.theme_use("bootstrap-dark")
    for name in DIALOG_STYLES:
        assert style.style_exists_in_theme(name), \
            f"{name} should be built at theme load"


def test_entry_field_readable_in_dark_without_widgets(root):
    """The dark-mode TEntry field is themed, not clam's white (#1224)."""
    style = root.style
    style.theme_use("bootstrap-dark")
    fg = _lookup(root, "TEntry", "foreground")
    field = _lookup(root, "TEntry", "fieldbackground")
    # unbuilt, field is '' (clam falls back to a light default under the
    # near-white dark-theme foreground)
    assert field not in ("", "#ffffff", "white")
    assert field != fg

    # and it keeps tracking the active theme
    style.theme_use("bootstrap-light")
    assert _lookup(root, "TEntry", "fieldbackground") != field