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

if TYPE_CHECKING:
    from ttkbootstrap.appconfig import AppConfig
    from ttkbootstrap_icons_bs import BootstrapIcon
    from ttkbootstrap.menu import MenuManager, create_menu
    from ttkbootstrap.style.bootstyle import Bootstyle
    from ttkbootstrap.style.style import Style, use_style
    from ttkbootstrap.widgets import TK_WIDGETS, TTK_WIDGETS
    from ttkbootstrap.widgets.button import Button
    from ttkbootstrap.widgets.checkbutton import Checkbutton
    from ttkbootstrap.widgets.combobox import Combobox
    from ttkbootstrap.widgets.contextmenu import ContextMenu
    from ttkbootstrap.widgets.dateentry import DateEntry
    from ttkbootstrap.widgets.datepicker import DatePicker
    from ttkbootstrap.widgets.dropdownbutton import DropdownButton
    from ttkbootstrap.widgets.entry import Entry
    from ttkbootstrap.widgets.field import Field
    from ttkbootstrap.widgets.floodgauge import FloodGauge
    from ttkbootstrap.widgets.form import Form
    from ttkbootstrap.widgets.frame import Frame
    from ttkbootstrap.widgets.label import Label
    from ttkbootstrap.widgets.labelframe import Labelframe
    from ttkbootstrap.widgets.labeledscale import LabeledScale
    from ttkbootstrap.widgets.menubutton import Menubutton
    from ttkbootstrap.widgets.meter import Meter
    from ttkbootstrap.widgets.notebook import Notebook
    from ttkbootstrap.widgets.numericentry import NumericEntry
    from ttkbootstrap.widgets.optionmenu import OptionMenu
    from ttkbootstrap.widgets.panedwindow import Panedwindow
    from ttkbootstrap.widgets.passwordentry import PasswordEntry
    from ttkbootstrap.widgets.pathentry import PathEntry
    from ttkbootstrap.widgets.progressbar import Progressbar
    from ttkbootstrap.widgets.radiobutton import Radiobutton
    from ttkbootstrap.widgets.scale import Scale
    from ttkbootstrap.widgets.scrollbar import Scrollbar
    from ttkbootstrap.widgets.scrolledtext import ScrolledText
    from ttkbootstrap.widgets.scrollview import ScrollView
    from ttkbootstrap.widgets.selectbox import SelectBox
    from ttkbootstrap.widgets.separator import Separator
    from ttkbootstrap.widgets.sizegrip import Sizegrip
    from ttkbootstrap.widgets.spinbox import Spinbox
    from ttkbootstrap.widgets.tableview import TableView
    from ttkbootstrap.widgets.textentry import TextEntry
    from ttkbootstrap.widgets.timeentry import TimeEntry
    from ttkbootstrap.widgets.toast import Toast
    from ttkbootstrap.widgets.tooltip import ToolTip
    from ttkbootstrap.widgets.treeview import Treeview
    from ttkbootstrap.window import Toplevel, Window

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
    # Core app/config
    "AppConfig": "ttkbootstrap.appconfig",
    "BootstrapIcon": "ttkbootstrap_icons_bs",
    "Bootstyle": "ttkbootstrap.style.bootstyle",
    "Style": "ttkbootstrap.style.style",
    "use_style": "ttkbootstrap.style.style",
    "MenuManager": "ttkbootstrap.menu",
    "create_menu": "ttkbootstrap.menu",
    "TK_WIDGETS": "ttkbootstrap.widgets",
    "TTK_WIDGETS": "ttkbootstrap.widgets",

    # TTK widgets
    "Button": "ttkbootstrap.widgets.button",
    "Checkbutton": "ttkbootstrap.widgets.checkbutton",
    "Combobox": "ttkbootstrap.widgets.combobox",
    "Entry": "ttkbootstrap.widgets.entry",
    "Frame": "ttkbootstrap.widgets.frame",
    "Labelframe": "ttkbootstrap.widgets.labelframe",
    "Label": "ttkbootstrap.widgets.label",
    "Menubutton": "ttkbootstrap.widgets.menubutton",
    "Notebook": "ttkbootstrap.widgets.notebook",
    "Panedwindow": "ttkbootstrap.widgets.panedwindow",
    "Progressbar": "ttkbootstrap.widgets.progressbar",
    "Radiobutton": "ttkbootstrap.widgets.radiobutton",
    "Scale": "ttkbootstrap.widgets.scale",
    "Scrollbar": "ttkbootstrap.widgets.scrollbar",
    "Separator": "ttkbootstrap.widgets.separator",
    "Sizegrip": "ttkbootstrap.widgets.sizegrip",
    "Spinbox": "ttkbootstrap.widgets.spinbox",
    "Treeview": "ttkbootstrap.widgets.treeview",
    "OptionMenu": "ttkbootstrap.widgets.optionmenu",

    # Composite/extended widgets
    "ScrollView": "ttkbootstrap.widgets.scrollview",
    "ScrolledText": "ttkbootstrap.widgets.scrolledtext",
    "FloodGauge": "ttkbootstrap.widgets.floodgauge",
    "LabeledScale": "ttkbootstrap.widgets.labeledscale",
    "Meter": "ttkbootstrap.widgets.meter",
    "TableView": "ttkbootstrap.widgets.tableview",
    "ContextMenu": "ttkbootstrap.widgets.contextmenu",
    "DateEntry": "ttkbootstrap.widgets.dateentry",
    "DatePicker": "ttkbootstrap.widgets.datepicker",
    "DropdownButton": "ttkbootstrap.widgets.dropdownbutton",
    "Field": "ttkbootstrap.widgets.field",
    "Form": "ttkbootstrap.widgets.form",
    "NumericEntry": "ttkbootstrap.widgets.numericentry",
    "PasswordEntry": "ttkbootstrap.widgets.passwordentry",
    "PathEntry": "ttkbootstrap.widgets.pathentry",
    "SelectBox": "ttkbootstrap.widgets.selectbox",
    "TextEntry": "ttkbootstrap.widgets.textentry",
    "TimeEntry": "ttkbootstrap.widgets.timeentry",
    "Toast": "ttkbootstrap.widgets.toast",
    "ToolTip": "ttkbootstrap.widgets.tooltip",

    # Windows
    "Toplevel": "ttkbootstrap.window",
    "Window": "ttkbootstrap.window",
}

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
from ttkbootstrap.style.tk_patch import install_tk_autostyle
from ttkbootstrap.events import install_enhanced_events

install_tk_autostyle()
install_enhanced_events()
