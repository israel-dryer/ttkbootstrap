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
from tkinter import (
    Menu, Text, Canvas, Tk, Variable, StringVar, IntVar, BooleanVar, DoubleVar,
    PhotoImage
)
from tkinter.ttk import (Button, Checkbutton, Combobox, Entry, Frame, Label, Labelframe, Menubutton, Notebook,
                         OptionMenu, Panedwindow, Progressbar, Radiobutton, Scale, Scrollbar, Separator, Sizegrip,
                         Spinbox, Treeview)

from ttkbootstrap import widgets as _widgets
from ttkbootstrap.style import Bootstyle, Style
from ttkbootstrap.widgets import DateEntry, Floodgauge, FloodgaugeLegacy, LabeledScale, M, Meter
from ttkbootstrap.window import Toplevel, Window

Bootstyle.setup_ttkbootstrap_api()

__all__ = [
    # Tk exports
    Tk, Menu, Text, Canvas, Variable, StringVar, IntVar, BooleanVar, DoubleVar,
    PhotoImage,

    # TTk exports
    Button, Checkbutton, Combobox, Entry, Frame, Labelframe,
    Label, Menubutton, Notebook, Panedwindow, Progressbar, Radiobutton,
    Scale, Scrollbar, Separator, Sizegrip, Spinbox,
    Treeview, OptionMenu,

    # TTkBootstrap exports
    Bootstyle,
    Style,
    Toplevel,
    Window,
    DateEntry,
    Floodgauge,
    FloodgaugeLegacy,
    LabeledScale,
    Meter,
    M
]
