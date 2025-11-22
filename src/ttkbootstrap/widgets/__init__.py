"""Public widget exports for ttkbootstrap.

Re-exports ttk wrapper widgets and custom widgets under a stable namespace.
Prefer importing from `ttkbootstrap` or `ttkbootstrap.widgets` rather than
submodules.
"""
import tkinter as tk
from tkinter import ttk

# Custom widgets
from ttkbootstrap.widgets.dateentry import DateEntry
from ttkbootstrap.widgets.floodgauge import FloodGauge
from ttkbootstrap.widgets.labeledscale import LabeledScale
from ttkbootstrap.widgets.meter import Meter
from ttkbootstrap.widgets.toast import Toast
from ttkbootstrap.widgets.tooltip import ToolTip

# Wrapper widgets (ttk)
from ttkbootstrap.widgets.button import Button
from ttkbootstrap.widgets.label import Label
from ttkbootstrap.widgets.menubutton import Menubutton
from ttkbootstrap.widgets.checkbutton import Checkbutton
from ttkbootstrap.widgets.radiobutton import Radiobutton
from ttkbootstrap.widgets.combobox import Combobox
from ttkbootstrap.widgets.entry import Entry
from ttkbootstrap.widgets.frame import Frame
from ttkbootstrap.widgets.notebook import Notebook
from ttkbootstrap.widgets.labelframe import Labelframe
from ttkbootstrap.widgets.panedwindow import Panedwindow
from ttkbootstrap.widgets.progressbar import Progressbar
from ttkbootstrap.widgets.scale import Scale
from ttkbootstrap.widgets.scrollbar import Scrollbar
from ttkbootstrap.widgets.separator import Separator
from ttkbootstrap.widgets.sizegrip import Sizegrip
from ttkbootstrap.widgets.spinbox import Spinbox
from ttkbootstrap.widgets.treeview import Treeview
from ttkbootstrap.widgets.optionmenu import OptionMenu

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
