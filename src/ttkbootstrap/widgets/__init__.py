"""Widgets module for ttkbootstrap.

This module provides custom widgets for ttkbootstrap, extending the standard
tkinter and ttk widget set with enhanced functionality and styling options.

Available Widgets:
    DateEntry: Date picker widget with calendar popup
    Floodgauge: Progress bar with customizable text overlay
    FloodgaugeLegacy: Legacy ttk-based progress bar
    Meter: Radial progress indicator with various display styles
    LabeledScale: Scale widget with automatic value label

Module Constants:
    M (int): Meter image scale factor (3)
    TTK_WIDGETS: Tuple of standard ttk widget classes
    TK_WIDGETS: Tuple of standard tk widget classes

Example:
    ```python
    import ttkbootstrap as ttk
    from datetime import datetime

    root = ttk.Window()

    # Create various custom widgets
    date_entry = ttk.DateEntry(root, firstweekday=0)
    date_entry.pack(padx=10, pady=5)

    floodgauge = ttk.Floodgauge(root, maximum=100, mask="{}% Complete")
    floodgauge.pack(fill='x', padx=10, pady=5)

    meter = ttk.Meter(root, amountused=75, metertype="semi")
    meter.pack(padx=10, pady=5)

    scale = ttk.LabeledScale(root, from_=0, to=100)
    scale.pack(fill='x', padx=10, pady=5)

    root.mainloop()
    ```

Note:
    All widgets in this module maintain backwards compatibility with the
    previous monolithic widgets.py file. Imports from ttkbootstrap.widgets
    will work identically to before the module refactoring.
"""
import tkinter as tk
from tkinter import ttk

# Import widgets from individual modules
from ttkbootstrap.widgets.dateentry import DateEntry
from ttkbootstrap.widgets.floodgauge import Floodgauge, FloodgaugeLegacy
from ttkbootstrap.widgets.labeledscale import LabeledScale
from ttkbootstrap.widgets.meter import Meter
from ttkbootstrap.widgets.toast import ToastNotification
from ttkbootstrap.widgets.tooltip import ToolTip

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
    'ToolTip',
    'ToastNotification',
    'M',
    'TTK_WIDGETS',
    'TK_WIDGETS',
]
