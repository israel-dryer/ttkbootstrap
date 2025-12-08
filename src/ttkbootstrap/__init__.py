"""ttkbootstrap - A supercharged theme extension for tkinter.

A modern flat style theme engine for tkinter that enables on-demand styling
of ttk widgets with over a dozen built-in themes inspired by Bootstrap.

This package provides:
    - A comprehensive collection of modern, flat-style themes
    - Custom widgets extending tkinter/ttk functionality
    - Easy-to-use styling API with color keywords
    - Window and Toplevel classes with enhanced functionality
    - Cross-platform compatibility

Example:
    ```python
    import ttkbootstrap as ttk
    from ttkbootstrap.constants import *

    # Create a themed window
    root = ttk.Window(themename="darkly")

    # Create styled widgets
    btn = ttk.Button(root, text="Click Me", bootstyle="success")
    btn.pack(padx=10, pady=10)

    root.mainloop()
    ```

For more information, see: https://ttkbootstrap.readthedocs.io/
"""

import importlib
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

if TYPE_CHECKING:
    from ttkbootstrap.api.menu import MenuManager, create_menu
    from ttkbootstrap.api.window import Toplevel, Window
    from ttkbootstrap.api.style import AppConfig, Bootstyle, Style, use_style
    from ttkbootstrap.api.widgets import (
        Button,
        Checkbutton,
        Combobox,
        ContextMenu,
        DateEntry,
        DatePicker,
        DropdownButton,
        Entry,
        Field,
        FloodGauge,
        Form,
        Frame,
        Label,
        Labelframe,
        LabeledScale,
        Menubutton,
        Meter,
        Notebook,
        NumericEntry,
        OptionMenu,
        Panedwindow,
        PasswordEntry,
        PathEntry,
        Progressbar,
        Radiobutton,
        Scale,
        Scrollbar,
        ScrolledText,
        ScrollView,
        SelectBox,
        Separator,
        Sizegrip,
        Spinbox,
        TableView,
        TextEntry,
        TimeEntry,
        Toast,
        ToolTip,
        Treeview,
        TK_WIDGETS,
        TTK_WIDGETS,
    )
    from ttkbootstrap_icons_bs import BootstrapIcon

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
    "Checkbutton",
    "Combobox",
    "Entry",
    "Frame",
    "Labelframe",
    "Label",
    "Menubutton",
    "Notebook",
    "Panedwindow",
    "Progressbar",
    "Radiobutton",
    "Scale",
    "Scrollbar",
    "Separator",
    "Sizegrip",
    "Spinbox",
    "Treeview",
    "OptionMenu",
]

_TTKBOOTSTRAP_EXPORTS = [
    "BootstrapIcon",
    "AppConfig",
    "Bootstyle",
    "ContextMenu",
    "Style",
    "Toplevel",
    "Window",
    "DateEntry",
    "DatePicker",
    "DropdownButton",
    "Field",
    "FloodGauge",
    "LabeledScale",
    "Meter",
    "Form",
    "TableView",
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
    "use_style",
]

_LAZY_EXPORTS = {
    "AppConfig": "ttkbootstrap.api.style",
    "BootstrapIcon": "ttkbootstrap.api.style",
    "Bootstyle": "ttkbootstrap.api.style",
    "Style": "ttkbootstrap.api.style",
    "use_style": "ttkbootstrap.api.style",
    "MenuManager": "ttkbootstrap.api.menu",
    "create_menu": "ttkbootstrap.api.menu",
    "Toplevel": "ttkbootstrap.api.window",
    "Window": "ttkbootstrap.api.window",
}

for _name in (*_TTKBOOTSTRAP_EXPORTS, *_TTK_EXPORTS):
    if _name not in _LAZY_EXPORTS:
        _LAZY_EXPORTS[_name] = "ttkbootstrap.api.widgets"

__all__ = [*_TK_EXPORTS, *_TTK_EXPORTS, *_TTKBOOTSTRAP_EXPORTS]


def __getattr__(name):
    """Lazily import top-level attributes to avoid circular imports and speed import."""
    if name in _LAZY_EXPORTS:
        module = importlib.import_module(_LAZY_EXPORTS[name])
        value = getattr(module, name)
        globals()[name] = value
        return value
    raise AttributeError(f"module 'ttkbootstrap' has no attribute '{name}'")


def __dir__():
    return sorted(set(__all__ + list(globals().keys())))


# Patch Tk widgets for autostyle and install enhanced events on import
from ttkbootstrap.runtime.tk_patch import install_tk_autostyle
from ttkbootstrap.events import install_enhanced_events

install_tk_autostyle()
install_enhanced_events()
