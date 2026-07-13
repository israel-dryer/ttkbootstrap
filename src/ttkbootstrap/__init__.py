"""ttkbootstrap - A supercharged theme extension for tkinter.

A modern flat style theme engine for tkinter that enables on-demand styling
of ttk widgets with over a dozen built-in themes inspired by Bootstrap.

This package provides:
    - A comprehensive collection of modern, flat-style themes
    - Custom widgets extending tkinter/ttk functionality
    - Easy-to-use styling API with color keywords
    - App (application root) and Toplevel classes with enhanced functionality
    - Cross-platform compatibility

Examples:
    ```python
    import ttkbootstrap as ttk
    from ttkbootstrap.constants import *

    # Create a themed application root
    root = ttk.App(theme="bootstrap-dark")

    # Create styled widgets
    btn = ttk.Button(root, text="Click Me", bootstyle="success")
    btn.pack(padx=10, pady=10)

    root.mainloop()
    ```

The styling API (the `bootstyle=` keyword on ttk widgets and `autostyle=` on
tk widgets) is delivered through the concrete widget classes exported here:
``ttkbootstrap.Button`` is ``class Button(BootMixin, ttk.Button)`` rather than a
monkey-patched ``tkinter.ttk.Button``. Importing ttkbootstrap therefore no
longer mutates the stock tkinter classes. To opt back into the old global
behavior (so that *vanilla* `tkinter.ttk`/`tkinter` widgets accept
`bootstyle`/`autostyle`), call `enable_global_api()`. To style a one-off widget
of a class you do not control, use `bootify(cls)` or `apply_bootstyle(widget,
bootstyle)`.

For more information, see: https://ttkbootstrap.readthedocs.io/
"""
from tkinter import (
    Menu as _tkMenu, Text as _tkText, Canvas as _tkCanvas, Tk as _tkTk,
    Frame as _tkFrame, LabelFrame as _tkLabelFrame, Label as _tkLabel,
    Listbox as _tkListbox,
    Variable, StringVar, IntVar, BooleanVar, DoubleVar, PhotoImage
)
from tkinter.font import (
    Font, families as font_families, names as font_names, nametofont,
)
from tkinter.ttk import (
    Button as _ttkButton, Checkbutton as _ttkCheckbutton,
    Combobox as _ttkCombobox, Entry as _ttkEntry, Frame as _ttkFrame,
    Label as _ttkLabel, Labelframe as _ttkLabelframe,
    Menubutton as _ttkMenubutton, Notebook as _ttkNotebook,
    OptionMenu as _ttkOptionMenu, Panedwindow as _ttkPanedwindow,
    Progressbar as _ttkProgressbar, Radiobutton as _ttkRadiobutton,
    Scale as _ttkScale, Scrollbar as _ttkScrollbar, Separator as _ttkSeparator,
    Sizegrip as _ttkSizegrip, Spinbox as _ttkSpinbox, Treeview as _ttkTreeview,
)

# The styling primitives. Importing style here only pulls in submodules
# (utils, constants, themes); it does not depend on the widget classes
# defined below, so it is safe this early in package init.
from ttkbootstrap.style import (
    Bootstyle, Style, FluentGeometryMixin, BootMixin, AutoStyleMixin,
    bootify, apply_bootstyle, enable_global_api,
    # Semantic-anchor theme authoring (Workstream E).
    Theme,
    # Style-construction toolkit (Workstream I): the public "build your own
    # style" surface, dogfooded by the builders.
    Assets, El, layout, register_style, image_element, statespec, state_map, StyleName,
    # Icon-rendered assets: glyph atoms + per-state icon element sugar + the
    # theme-aware widget-icon helper (also the icon=/icon_size= mixin kwargs).
    Icon, apply_icon, icon_element,
    # Canonical bootstyle grammar strictness (Workstream D).
    set_bootstyle_strict, is_bootstyle_strict,
)
# Opt-in migration path for the pre-2.0 theme names (Workstream E/F).
from ttkbootstrap.themes.legacy import install_legacy_themes

# Public utilities re-exported at the top level for convenience, so
# `ttk.scale_size(...)` / `ttk.contrast_color(...)` work the same way the widgets
# and dialogs are reachable as `ttk.<Name>`. Their home is the `ttkbootstrap.utils`
# package (2.0); the old `ttkbootstrap.utility` / `ttkbootstrap.colorutils`
# module paths still work as warn-and-forward shims (removed in 3.0).
from ttkbootstrap.utils import (
    enable_high_dpi_awareness,
    scale_size,
    windowing_system,
    color_to_rgb,
    color_to_hex,
    color_to_hsl,
    update_hsl_value,
    contrast_color,
    conform_color_model,
    set_default_button,
    on_theme_change,
    theme_aware,
    remove_theme_change_callback,
    Fonts,
    set_global_family,
)


# --------------------------------------------------------------------------- #
# Concrete ttk widget classes — the blessed `bootstyle` set.
#
# Each is a real subclass `class X(BootMixin, ttk.X)`, so it carries a genuine
# signature/docstring (for IDEs and the docs build) and the `bootstyle` keyword
# is statically visible. These MUST be defined before the widgets/dialogs/window
# submodules are imported below, because those modules import these names from
# `ttkbootstrap` (e.g. `from ttkbootstrap import Frame`).
# --------------------------------------------------------------------------- #
class Button(BootMixin, _ttkButton):
    """ttk Button with ttkbootstrap theming (accepts `bootstyle=`)."""


class Checkbutton(BootMixin, _ttkCheckbutton):
    """ttk Checkbutton with ttkbootstrap theming (accepts `bootstyle=`)."""


class Combobox(BootMixin, _ttkCombobox):
    """ttk Combobox with ttkbootstrap theming (accepts `bootstyle=`)."""


class Entry(BootMixin, _ttkEntry):
    """ttk Entry with ttkbootstrap theming (accepts `bootstyle=`)."""


class Frame(BootMixin, _ttkFrame):
    """ttk Frame with ttkbootstrap theming (accepts `bootstyle=`)."""


class Label(BootMixin, _ttkLabel):
    """ttk Label with ttkbootstrap theming (accepts `bootstyle=`)."""


class Labelframe(BootMixin, _ttkLabelframe):
    """ttk Labelframe with ttkbootstrap theming (accepts `bootstyle=`)."""


class Menubutton(BootMixin, _ttkMenubutton):
    """ttk Menubutton with ttkbootstrap theming (accepts `bootstyle=`)."""


class Notebook(BootMixin, _ttkNotebook):
    """ttk Notebook with ttkbootstrap theming (accepts `bootstyle=`)."""


class Panedwindow(BootMixin, _ttkPanedwindow):
    """ttk Panedwindow with ttkbootstrap theming (accepts `bootstyle=`)."""


class Progressbar(BootMixin, _ttkProgressbar):
    """ttk Progressbar with ttkbootstrap theming (accepts `bootstyle=`)."""


class Radiobutton(BootMixin, _ttkRadiobutton):
    """ttk Radiobutton with ttkbootstrap theming (accepts `bootstyle=`)."""


class Scale(BootMixin, _ttkScale):
    """ttk Scale with ttkbootstrap theming (accepts `bootstyle=`)."""


class Scrollbar(BootMixin, _ttkScrollbar):
    """ttk Scrollbar with ttkbootstrap theming (accepts `bootstyle=`)."""


class Separator(BootMixin, _ttkSeparator):
    """ttk Separator with ttkbootstrap theming (accepts `bootstyle=`)."""


class Sizegrip(BootMixin, _ttkSizegrip):
    """ttk Sizegrip with ttkbootstrap theming (accepts `bootstyle=`)."""


class Spinbox(BootMixin, _ttkSpinbox):
    """ttk Spinbox with ttkbootstrap theming (accepts `bootstyle=`)."""


class Treeview(BootMixin, _ttkTreeview):
    """ttk Treeview with ttkbootstrap theming (accepts `bootstyle=`)."""


class OptionMenu(BootMixin, _ttkOptionMenu):
    """ttk OptionMenu with ttkbootstrap theming (accepts `bootstyle=`)."""
    # OptionMenu manages its own item access through __getitem__/__setitem__
    # (e.g. it sets self['menu'] during construction). Keep tkinter's versions
    # rather than BootMixin's bootstyle-routing accessors.
    __getitem__ = _ttkOptionMenu.__getitem__
    __setitem__ = _ttkOptionMenu.__setitem__


# --------------------------------------------------------------------------- #
# Concrete tk widget classes — the blessed `autostyle` set. These legacy tk
# widgets have no ttk style; AutoStyleMixin paints them with the active theme at
# construction and honors `autostyle=False` to opt out.
# --------------------------------------------------------------------------- #
class Tk(AutoStyleMixin, _tkTk):
    """tk root window with ttkbootstrap theming (accepts `autostyle=`)."""


# Menu is defined in its own module (it carries the macOS application-menu
# helpers, more than a one-line subclass); re-exported here as `ttk.Menu`.
from ttkbootstrap.menu import Menu


class Text(AutoStyleMixin, _tkText):
    """tk Text with ttkbootstrap theming (accepts `autostyle=`)."""


class Canvas(AutoStyleMixin, _tkCanvas):
    """tk Canvas with ttkbootstrap theming (accepts `autostyle=`)."""


class Listbox(AutoStyleMixin, _tkListbox):
    """tk Listbox with ttkbootstrap theming (accepts `autostyle=`)."""


class TkFrame(AutoStyleMixin, _tkFrame):
    """tk Frame with ttkbootstrap theming (accepts `autostyle=`).

    Exported as ``TkFrame`` to avoid colliding with the ttk ``Frame`` above.
    """


class TkLabel(AutoStyleMixin, _tkLabel):
    """tk Label with ttkbootstrap theming (accepts `autostyle=`).

    Exported as ``TkLabel`` to avoid colliding with the ttk ``Label`` above.
    Use it (with ``autostyle=False``) for a label that must show explicit
    colors the theme should not repaint.
    """


class LabelFrame(AutoStyleMixin, _tkLabelFrame):
    """tk LabelFrame with ttkbootstrap theming (accepts `autostyle=`)."""


# Submodules below import the concrete widget classes from this package, so
# they must come after the class definitions above.
from ttkbootstrap import widgets as _widgets
from ttkbootstrap.widgets import (
    DateEntry,
    Floodgauge,
    FloodgaugeLegacy,
    LabeledScale,
    M,
    Meter,
    ScrolledFrame,
    ScrolledText,
    TableColumn,
    TableRow,
    Tableview,
    ToastNotification,
    ToolTip,
)
from ttkbootstrap.window import App, Toplevel, Window

# Dialogs re-exported at top level so the common front doors are reachable as
# ttk.Messagebox / ttk.Querybox, matching how widgets are exposed (2.0). The
# ttkbootstrap.dialogs.* import paths remain valid. Placed after the widget and
# window classes above, since the dialogs build on them at runtime.
from ttkbootstrap.dialogs import (
    ColorChooser,
    ColorChooserDialog,
    ColorDropperDialog,
    DatePickerDialog,
    Dialog,
    FontDialog,
    MessageDialog,
    Messagebox,
    QueryDialog,
    Querybox,
)

# Localization helpers re-exported at the top level (`ttk.L`, `ttk.set_locale`,
# `ttk.LocaleVar`). Imported after `window` above so the localization -> window
# import chain resolves cleanly. The `ttkbootstrap.localization` package remains
# the canonical home / import path.
from ttkbootstrap.localization import L, LocaleVar, set_locale

# Input-validation namespace re-exported at the top level (`ttk.Validation`).
# Imported last so the `validation -> ttkbootstrap` chain sees a fully built
# package; `ttkbootstrap.validation` remains the canonical home / import path.
from ttkbootstrap.validation import Validation, validator, ValidationEvent

# Re-export the stdlib file dialog as `ttk.filedialog`. It is the one standard
# dialog ttkbootstrap does not supersede (native OS chrome), so surfacing the
# module here spares callers a bare `from tkinter import filedialog`; the themed
# wrappers live on `Querybox.get_open_filename`/etc.
from tkinter import filedialog

__all__ = [
    # Tk exports
    "Tk", "Menu", "Text", "Canvas", "Listbox", "TkFrame", "TkLabel", "LabelFrame", "Variable", "StringVar", "IntVar", "BooleanVar",
    "DoubleVar", "PhotoImage",
    "Font", "font_families", "font_names", "nametofont",

    # TTk exports
    "Button", "Checkbutton", "Combobox", "Entry", "Frame", "Labelframe",
    "Label", "Menubutton", "Notebook", "Panedwindow", "Progressbar", "Radiobutton",
    "Scale", "Scrollbar", "Separator", "Sizegrip", "Spinbox",
    "Treeview", "OptionMenu",

    # Styling API
    "Bootstyle",
    "Style",
    "FluentGeometryMixin",
    "BootMixin",
    "AutoStyleMixin",
    "bootify",
    "apply_bootstyle",
    "enable_global_api",
    "Theme",
    "install_legacy_themes",

    # Style-construction toolkit
    "Assets",
    "El",
    "layout",
    "register_style",
    "image_element",
    "statespec",
    "state_map",
    "StyleName",
    "Icon",
    "apply_icon",
    "icon_element",
    "set_bootstyle_strict",
    "is_bootstyle_strict",

    # Public utilities
    "enable_high_dpi_awareness",
    "scale_size",
    "windowing_system",
    "color_to_rgb",
    "color_to_hex",
    "color_to_hsl",
    "update_hsl_value",
    "contrast_color",
    "conform_color_model",
    "set_default_button",
    "on_theme_change",
    "theme_aware",
    "remove_theme_change_callback",
    "Fonts",
    "set_global_family",

    # Localization
    "L",
    "LocaleVar",
    "set_locale",

    # Input validation
    "Validation",
    "validator",
    "ValidationEvent",

    # Stdlib file dialog (native; not superseded)
    "filedialog",

    # Application root + windows
    "App",
    "Toplevel",
    "Window",

    # Custom widgets
    "DateEntry",
    "Floodgauge",
    "FloodgaugeLegacy",
    "LabeledScale",
    "Meter",
    "ScrolledText",
    "ScrolledFrame",
    "Tableview",
    "TableColumn",
    "TableRow",
    "ToolTip",
    "ToastNotification",
    "M",

    # Dialogs
    "Messagebox",
    "Querybox",
    "Dialog",
    "MessageDialog",
    "QueryDialog",
    "DatePickerDialog",
    "FontDialog",
    "ColorChooser",
    "ColorChooserDialog",
    "ColorDropperDialog",
]
