import sys as _sys
from ttkbootstrap.core import constants as _constants_module
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

constants = _constants_module
_sys.modules[__name__ + ".constants"] = _constants_module

if TYPE_CHECKING:
    from ttkbootstrap.api.menu import MenuManager, create_menu
    from ttkbootstrap.api.window import Toplevel, Window
    from ttkbootstrap.api.style import (
        AppConfig,
        Bootstyle,
        Style,
        get_style,
        get_style_builder,
        get_active_theme,
        get_theme_provider,
        set_active_theme,
        get_theme_color,
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
        Scale,
        Scrollbar,
        ScrolledText,
        ScrollView,
        SelectBox,
        Separator,
        SizeGrip,
        Spinbox,
        TableView,
        TextEntry,
        TimeEntry,
        Toast,
        ToolTip,
        TreeView,
        TK_WIDGETS,
        TTK_WIDGETS,
    )
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

_TTK_EXPORTS = [
    "Button",
    "CheckButton",
    "Combobox",
    "Entry",
    "Frame",
    "LabelFrame",
    "Label",
    "MenuButton",
    "Notebook",
    "PanedWindow",
    "Progressbar",
    "RadioButton",
    "Scale",
    "Scrollbar",
    "Separator",
    "SizeGrip",
    "Spinbox",
    "TreeView",
    "OptionMenu",
]

_TTKBOOTSTRAP_EXPORTS = [
    "BootstrapIcon",
    "AppConfig",
    "Bootstyle",
    "ContextMenu",
    "ContextMenuItem",
    "Style",
    "Toplevel",
    "Window",
    "DateEntry",
    "DatePicker",
    "DropdownButton",
    "Field",
    "FieldOptions",
    "FloodGauge",
    "LabeledScale",
    "Meter",
    "Form",
    "TableView",
    "PageStack",
    "PasswordEntry",
    "PathEntry",
    "Toast",
    "ToolTip",
    "TextEntry",
    "TimeEntry",
    "ScrollView",
    "ScrolledText",
    "SelectBox",
    "MenuManager",
    "NumericEntry",
    "create_menu",
    "TTK_WIDGETS",
    "TK_WIDGETS",
    "get_style",
    "get_style_builder",
    "get_active_theme",
    "get_theme_provider",
    "set_active_theme",
    "get_theme_color"
]

_LAZY_EXPORTS = {
    "AppConfig": "ttkbootstrap.api.style",
    "BootstrapIcon": "ttkbootstrap.api.style",
    "Bootstyle": "ttkbootstrap.api.style",
    "Style": "ttkbootstrap.api.style",
    "get_style": "ttkbootstrap.api.style",
    "get_style_builder": "ttkbootstrap.api.style",
    "get_active_theme": "ttkbootstrap.api.style",
    "get_theme_provider": "ttkbootstrap.api.style",
    "set_active_theme": "ttkbootstrap.api.style",
    "get_theme_color": "ttkbootstrap.api.style",
    "MenuManager": "ttkbootstrap.api.menu",
    "create_menu": "ttkbootstrap.api.menu",
    "Toplevel": "ttkbootstrap.api.window",
    "Window": "ttkbootstrap.api.window",
}

for _name in (*_TTKBOOTSTRAP_EXPORTS, *_TTK_EXPORTS):
    if _name not in _LAZY_EXPORTS:
        _LAZY_EXPORTS[_name] = "ttkbootstrap.api.widgets"

__all__ = [*_TK_EXPORTS, *_TTK_EXPORTS, *_TTKBOOTSTRAP_EXPORTS, *_DEPRECATED_ALIASES, "constants"]

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
