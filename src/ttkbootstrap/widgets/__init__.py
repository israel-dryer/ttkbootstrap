"""
Widgets module for ttkbootstrap.

This module provides custom widgets for ttkbootstrap. All widgets are
re-exported from this module for backwards compatibility.
"""
import tkinter as tk
from tkinter import ttk

# Import widgets from individual modules
from ttkbootstrap.widgets.dateentry import DateEntry
from ttkbootstrap.widgets.floodgauge import Floodgauge, FloodgaugeLegacy
from ttkbootstrap.widgets.meter import Meter
from ttkbootstrap.widgets.labeledscale import LabeledScale

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
    'DateEntry',
    'Floodgauge',
    'FloodgaugeLegacy',
    'Meter',
    'LabeledScale',
    'M',
    'TTK_WIDGETS',
    'TK_WIDGETS',
]