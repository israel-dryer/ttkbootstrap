import importlib as _importlib
from typing import TYPE_CHECKING

from tkinter import (
    BooleanVar,
    Canvas as _tkCanvas,
    DoubleVar,
    Frame as _tkFrame,
    IntVar,
    Menu as _tkMenu,
    PhotoImage,
    StringVar,
    Text as _tkText,
    Tk as _tkTk,
    Variable,
)

# Re-export tk widgets with original names before importing submodules
Tk = _tkTk
Menu = _tkMenu
Text = _tkText
Canvas = _tkCanvas
TkFrame = _tkFrame  # Exported as TkFrame to avoid conflict with ttk.Frame
# Eagerly import BootstrapIcon to prevent circular import during style bootstrapping
from ttkbootstrap_icons_bs import BootstrapIcon  # noqa: E402

# Constants are available via ttkbootstrap.constants module
# (see constants.py which re-exports from core.constants)

if TYPE_CHECKING:
    from ttkbootstrap.api.menu import MenuManager, create_menu
    from ttkbootstrap.api.app import App, App as Window, Toplevel, AppSettings, get_app_settings, get_current_app
    from ttkbootstrap.api.style import (
        Bootstyle,
        Style,
        get_style,
        get_style_builder,
        get_theme,
        get_theme_provider,
        set_theme,
        toggle_theme,
        get_theme_color,
        get_themes,
    )
    from ttkbootstrap.api.widgets import (
        Button,
        CheckButton,
        Combobox,
        ContextMenu,
        ContextMenuItem,
        DateEntry,
        DatePicker,
        DropdownButton,
        Entry,
        Field,
        FieldOptions,
        FloodGauge,
        Form,
        Frame,
        Label,
        LabelFrame,
        LabeledScale,
        MenuButton,
        Meter,
        Notebook,
        NumericEntry,
        OptionMenu,
        PageStack,
        PanedWindow,
        PasswordEntry,
        PathEntry,
        Progressbar,
        RadioButton,
        RadioGroup,
        Scale,
        Scrollbar,
        ScrolledText,
        ScrollView,
        SelectBox,
        Separator,
        SpinnerEntry,
        SizeGrip,
        Spinbox,
        TableView,
        TextEntry,
        TimeEntry,
        Toast,
        ToggleGroup,
        ToolTip,
        TreeView,
        TK_WIDGETS,
        TTK_WIDGETS,
    )
    from ttkbootstrap.api.localization import MessageCatalog, L, LV,IntlFormatter
    from ttkbootstrap_icons_bs import BootstrapIcon

_DEPRECATED_ALIASES = {
    "Checkbutton": "CheckButton",
    "Radiobutton": "RadioButton",
    "Labelframe": "LabelFrame",
    "Panedwindow": "PanedWindow",
    "Treeview": "TreeView",
    "Tableview": "TableView"
}

_TK_EXPORTS = [
    "Tk",
    "Menu",
    "Text",
    "Canvas",
    "TkFrame",
    "Variable",
    "StringVar",
    "IntVar",
    "BooleanVar",
    "DoubleVar",
    "PhotoImage",
]

# Single source of truth: module-to-exports mapping
# Organized by category for clarity
_TTK_PRIMITIVES = [
    "Button", "CheckButton", "Combobox", "Entry", "Frame", "Label",
    "LabelFrame", "MenuButton", "Notebook", "OptionMenu", "PanedWindow",
    "Progressbar", "RadioButton", "Scale", "Scrollbar", "Separator",
    "SizeGrip", "Spinbox", "TreeView",
]

_MODULE_EXPORTS = {
    "ttkbootstrap.api.app": [
        "App", "Toplevel", "Window", "AppSettings", "get_app_settings", "get_current_app",
    ],
    "ttkbootstrap.api.style": [
        "BootstrapIcon", "Bootstyle", "Style",
        "get_style", "get_style_builder", "get_theme",
        "get_theme_provider", "set_theme", "get_theme_color",
        "toggle_theme", "get_themes"
    ],
    "ttkbootstrap.api.menu": [
        "MenuManager", "create_menu",
    ],
    "ttkbootstrap.api.widgets": [
        *_TTK_PRIMITIVES,
        "Badge",
        "CheckToggle",
        "RadioToggle",
        "ContextMenu", "ContextMenuItem", "DateEntry", "DatePicker",
        "DropdownButton", "Field", "FieldOptions", "FloodGauge", "Form",
        "LabeledScale", "Meter", "NumericEntry", "PageStack",
        "PasswordEntry", "PathEntry", "RadioGroup", "ScrolledText", "ScrollView", "SpinnerEntry",
        "SelectBox", "TableView", "TextEntry", "TimeEntry", "Toast", "ToggleGroup",
        "ToolTip", "TK_WIDGETS", "TTK_WIDGETS",
    ],
    "ttkbootstrap.api.localization": [
        "MessageCatalog", "L", "LV", "IntlFormatter"
    ],
    "ttkbootstrap.core.signals": [
        "Signal",
    ],
}

# Auto-generate lazy exports and categorized export lists
_LAZY_EXPORTS = {}
_TTK_EXPORTS = _TTK_PRIMITIVES.copy()
_TTKBOOTSTRAP_EXPORTS = []

for module, exports in _MODULE_EXPORTS.items():
    for name in exports:
        _LAZY_EXPORTS[name] = module
        if name not in _TTK_EXPORTS:  # Already added TTK primitives
            _TTKBOOTSTRAP_EXPORTS.append(name)

__all__ = [*_TK_EXPORTS, *_TTK_EXPORTS, *_TTKBOOTSTRAP_EXPORTS, *_DEPRECATED_ALIASES]

import warnings as _warnings


def __getattr__(name):
    """Lazily import top-level attributes to avoid circular imports and speed import."""
    # Deprecated aliases
    if name in _DEPRECATED_ALIASES:
        new_name = _DEPRECATED_ALIASES[name]
        _warnings.warn(
            f"ttkbootstrap.{name} is deprecated and will be removed in a future version; "
            f"use {new_name} instead.",
            DeprecationWarning,
            stacklevel=2,
        )

        # Look up the canonical class lazily
        module = _importlib.import_module(_LAZY_EXPORTS[new_name])
        value = getattr(module, new_name)

        # Cache the alias so subsequent access is just a dict lookup
        globals()[name] = value
        return value

    # Lazy exports
    if name in _LAZY_EXPORTS:
        module = _importlib.import_module(_LAZY_EXPORTS[name])
        value = getattr(module, name)
        globals()[name] = value
        return value

    raise AttributeError(f"module 'ttkbootstrap' has no attribute '{name}'")


def __dir__():
    return sorted(set(__all__ + list(globals().keys())))


# Patch Tk widgets for autostyle and install enhanced events on import
from ttkbootstrap.runtime.tk_patch import install_tk_autostyle
from ttkbootstrap.runtime.events import install_enhanced_events

install_tk_autostyle()
install_enhanced_events()
