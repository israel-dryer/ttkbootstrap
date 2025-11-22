"""Public widget exports for ttkbootstrap.

Re-exports ttk wrapper widgets and custom widgets under a stable namespace.
Prefer importing from `ttkbootstrap` or `ttkbootstrap.widgets` rather than
submodules.
"""
import tkinter as tk
from tkinter import ttk

# Import widgets from individual modules
from ttkbootstrap.widgets.custom.dateentry import DateEntry
from ttkbootstrap.widgets.custom.floodgauge import FloodGauge
from ttkbootstrap.widgets.custom.labeledscale import LabeledScale
from ttkbootstrap.widgets.custom.meter import Meter
from ttkbootstrap.widgets.custom.toast import Toast
from ttkbootstrap.widgets.custom.tooltip import ToolTip

# Wrapper widgets (ttk)
from ttkbootstrap.widgets.controls.button import Button
from ttkbootstrap.widgets.display.label import Label
from ttkbootstrap.widgets.controls.menubutton import Menubutton
from ttkbootstrap.widgets.controls.checkbutton import Checkbutton
from ttkbootstrap.widgets.controls.radiobutton import Radiobutton
from ttkbootstrap.widgets.controls.combobox import Combobox
from ttkbootstrap.widgets.controls.entry import Entry
from ttkbootstrap.widgets.containers.frame import Frame
from ttkbootstrap.widgets.containers.notebook import Notebook
from ttkbootstrap.widgets.containers.labelframe import Labelframe
from ttkbootstrap.widgets.containers.panedwindow import Panedwindow
from ttkbootstrap.widgets.display.progressbar import Progressbar
from ttkbootstrap.widgets.controls.scale import Scale
from ttkbootstrap.widgets.display.scrollbar import Scrollbar
from ttkbootstrap.widgets.display.separator import Separator
from ttkbootstrap.widgets.display.sizegrip import Sizegrip
from ttkbootstrap.widgets.controls.spinbox import Spinbox
from ttkbootstrap.widgets.dataview.treeview import Treeview
from ttkbootstrap.widgets.controls.optionmenu import OptionMenu

# Constants from original widgets.py
M = 3  # meter image scale, higher number increases resolution

TTK_WIDGETS = (
    ttk.Button,
    ttk.Checkbutton,
    ttk.Combobox,
    ttk.Entry,
    ttk.Frame,
    ttk.Labelframe,
    ttk.Label,
    ttk.Menubutton,
    ttk.Notebook,
    ttk.Panedwindow,
    ttk.Progressbar,
    ttk.Radiobutton,
    ttk.Scale,
    ttk.Scrollbar,
    ttk.Separator,
    ttk.Sizegrip,
    ttk.Spinbox,
    ttk.Treeview,
    ttk.OptionMenu,
)

TK_WIDGETS = (
    tk.Tk,
    tk.Toplevel,
    tk.Button,
    tk.Label,
    tk.Text,
    tk.Frame,
    tk.Checkbutton,
    tk.Radiobutton,
    tk.Entry,
    tk.Scale,
    tk.Listbox,
    tk.Menu,
    tk.Menubutton,
    tk.LabelFrame,
    tk.Canvas,
    tk.OptionMenu,
    tk.Spinbox,
)

# Export all widgets for backwards compatibility
__all__ = [
    # ttk wrapper widgets
    'Button',
    'Label',
    'Menubutton',
    'Checkbutton',
    'Radiobutton',
    'Combobox',
    'Entry',
    'Frame',
    'Notebook',
    'Labelframe',
    'Panedwindow',
    'Progressbar',
    'Scale',
    'Scrollbar',
    'Separator',
    'Sizegrip',
    'Spinbox',
    'Treeview',
    'OptionMenu',

    'DateEntry',
    'FloodGauge',
    'Meter',
    'LabeledScale',
    'Toast',
    'ToolTip',
    'M',
    'TTK_WIDGETS',
    'TK_WIDGETS',
]
