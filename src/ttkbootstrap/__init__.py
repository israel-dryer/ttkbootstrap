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

# Typing-time augmentation so local type checkers see `bootstyle`
# in constructors and `configure(...)` for ttk widgets imported from
# `ttkbootstrap` during development within this repo.
from typing import TYPE_CHECKING, Any, Optional, Tuple, Union

if TYPE_CHECKING:
    from tkinter import ttk as _ttk

    BootstyleArg = Union[str, Tuple[str, ...]]

    class _BootstyleMixin:
        def __init__(self, *args: Any, bootstyle: Optional[BootstyleArg] = ..., **kwargs: Any) -> None: ...
        def configure(self, *args: Any, bootstyle: Optional[BootstyleArg] = ..., **kwargs: Any) -> Any: ...

    class Button(_BootstyleMixin, Button): ...
    class Checkbutton(_BootstyleMixin, Checkbutton): ...
    class Combobox(_BootstyleMixin, Combobox): ...
    class Entry(_BootstyleMixin, Entry): ...
    class Frame(_BootstyleMixin, Frame): ...
    class Labelframe(_BootstyleMixin, Labelframe): ...
    class Label(_BootstyleMixin, Label): ...
    class Menubutton(_BootstyleMixin, Menubutton): ...
    class Notebook(_BootstyleMixin, Notebook): ...
    class Panedwindow(_BootstyleMixin, Panedwindow): ...
    class Progressbar(_BootstyleMixin, Progressbar): ...
    class Radiobutton(_BootstyleMixin, Radiobutton): ...
    class Scale(_BootstyleMixin, Scale): ...
    class Scrollbar(_BootstyleMixin, Scrollbar): ...
    class Separator(_BootstyleMixin, Separator): ...
    class Sizegrip(_BootstyleMixin, Sizegrip): ...
    class Spinbox(_BootstyleMixin, Spinbox): ...
    class Treeview(_BootstyleMixin, Treeview): ...
    class OptionMenu(_BootstyleMixin, OptionMenu): ...

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
