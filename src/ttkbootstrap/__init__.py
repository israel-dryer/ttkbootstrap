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
from tkinter import (BooleanVar, Canvas as _tkCanvas, DoubleVar, Frame as _tkFrame, IntVar, Menu as _tkMenu, PhotoImage,
                     StringVar, Text as _tkText, Tk as _tkTk, Variable)

# Re-export tk widgets with original names BEFORE importing submodules
# This prevents circular import issues when submodules try to import these
Tk = _tkTk
Menu = _tkMenu
Text = _tkText
Canvas = _tkCanvas
TkFrame = _tkFrame  # Exported as TkFrame to avoid conflict with ttk.Frame

from ttkbootstrap.appconfig import AppConfig, use_icon_provider
# Use the new Bootstyle implementation with constructor/configure overrides
from ttkbootstrap.style.bootstyle import Bootstyle
# Export the new Style implementation and a convenience accessor
from ttkbootstrap.style.style import Style, use_style
from ttkbootstrap.window import Toplevel, Window
from ttkbootstrap.menu import MenuManager, create_menu

# Export subclass-based ttk wrappers FIRST to avoid circular imports
from ttkbootstrap.widgets.button import Button as Button
from ttkbootstrap.widgets.label import Label as Label
from ttkbootstrap.widgets.menubutton import Menubutton as Menubutton
from ttkbootstrap.widgets.checkbutton import Checkbutton as Checkbutton
from ttkbootstrap.widgets.radiobutton import Radiobutton as Radiobutton
from ttkbootstrap.widgets.combobox import Combobox as Combobox
from ttkbootstrap.widgets.entry import Entry as Entry
from ttkbootstrap.widgets.frame import Frame as Frame
from ttkbootstrap.widgets.notebook import Notebook as Notebook
from ttkbootstrap.widgets.labelframe import Labelframe as Labelframe
from ttkbootstrap.widgets.panedwindow import Panedwindow as Panedwindow
from ttkbootstrap.widgets.progressbar import Progressbar as Progressbar
from ttkbootstrap.widgets.scale import Scale as Scale
from ttkbootstrap.widgets.scrollbar import Scrollbar as Scrollbar
from ttkbootstrap.widgets.separator import Separator as Separator
from ttkbootstrap.widgets.sizegrip import Sizegrip as Sizegrip
from ttkbootstrap.widgets.spinbox import Spinbox as Spinbox
from ttkbootstrap.widgets.treeview import Treeview as Treeview
from ttkbootstrap.widgets.scrollview import ScrollView as ScrollView
from ttkbootstrap.widgets.scrolledtext import ScrolledText as ScrolledText
from ttkbootstrap.widgets.optionmenu import OptionMenu as OptionMenu

# Import custom widgets (after basic widgets to avoid circular imports)
from ttkbootstrap.widgets.dateentry import DateEntry
from ttkbootstrap.widgets.floodgauge import FloodGauge
from ttkbootstrap.widgets.labeledscale import LabeledScale
from ttkbootstrap.widgets.meter import Meter
from ttkbootstrap.widgets.toast import Toast
from ttkbootstrap.widgets.tooltip import ToolTip
from ttkbootstrap.widgets.field import Field as Field
from ttkbootstrap.widgets.textentry import TextEntry as TextEntry
from ttkbootstrap.widgets.passwordentry import PasswordEntry as PasswordEntry
from ttkbootstrap.widgets.numericentry import NumericEntry as NumericEntry
from ttkbootstrap.widgets.pathentry import PathEntry as PathEntry

# Import constants from widgets
from ttkbootstrap.widgets import M, TTK_WIDGETS, TK_WIDGETS


# Patch Tk widgets for autostyle
from ttkbootstrap.style.tk_patch import install_tk_autostyle
install_tk_autostyle()

# Install enhanced event system
from ttkbootstrap.events import install_enhanced_events
install_enhanced_events()

# Note: Type annotations for widgets are now in the actual widget classes
# (widgets/button.py, widgets/label.py, etc.) - no TYPE_CHECKING stubs needed

__all__ = [
    # Tk exports
    'Tk', 'Menu', 'Text', 'Canvas', 'TkFrame', 'Variable', 'StringVar', 'IntVar', 'BooleanVar', 'DoubleVar',
    'PhotoImage',

    # TTK exports
    'Button', 'Checkbutton', 'Combobox', 'Entry', 'Frame', 'Labelframe',
    'Label', 'Menubutton', 'Notebook', 'Panedwindow', 'Progressbar', 'Radiobutton',
    'Scale', 'Scrollbar', 'Separator', 'Sizegrip', 'Spinbox',
    'Treeview', 'OptionMenu',

    # TTkBootstrap exports
    'AppConfig',
    'Bootstyle',
    'Style',
    'Toplevel',
    'Window',
    'DateEntry',
    'Field',
    'FloodGauge',
    'LabeledScale',
    'Meter',
    'PasswordEntry',
    'PathEntry',
    'Toast',
    'ToolTip',
    'TextEntry',
    'ScrollView',
    'ScrolledText',
    'MenuManager',
    'NumericEntry',
    'create_menu',
    'M',
    'TTK_WIDGETS',
    'TK_WIDGETS',
    'use_style',
    'use_icon_provider',
]