from __future__ import annotations

"""
PEP 561 stub augmentations for ttkbootstrap's public API.

These stubs add typing for ttkbootstrap's monkey‑patched ttk widgets so
they accept the named keyword argument `bootstyle` in both the widget
constructor and in `configure(...)` while retaining the base ttk types.

Target: Python 3.9+
"""

from typing import Any, Optional, Tuple, Union

from tkinter import (
    Menu,
    Text,
    Canvas,
    Tk,
    Variable,
    StringVar,
    IntVar,
    BooleanVar,
    DoubleVar,
    PhotoImage,
)
from tkinter import ttk as _ttk

from ttkbootstrap.style import Bootstyle, Style
from ttkbootstrap.window import Toplevel, Window
from ttkbootstrap.widgets import (
    DateEntry,
    Floodgauge,
    FloodgaugeLegacy,
    LabeledScale,
    Meter,
)


# A bootstyle can be a single keyword (e.g. "primary") or a tuple
# of keywords (e.g. ("danger", "inverse"))
BootstyleArg = Union[str, Tuple[str, ...]]


class _BootstyleMixin:
    def __init__(self, *args: Any, bootstyle: Optional[BootstyleArg] = ..., **kwargs: Any) -> None: ...

    def configure(self, *args: Any, bootstyle: Optional[BootstyleArg] = ..., **kwargs: Any) -> Any: ...


class Button(_BootstyleMixin, _ttk.Button): ...
class Checkbutton(_BootstyleMixin, _ttk.Checkbutton): ...
class Combobox(_BootstyleMixin, _ttk.Combobox): ...
class Entry(_BootstyleMixin, _ttk.Entry): ...
class Frame(_BootstyleMixin, _ttk.Frame): ...
class Labelframe(_BootstyleMixin, _ttk.Labelframe): ...
class Label(_BootstyleMixin, _ttk.Label): ...
class Menubutton(_BootstyleMixin, _ttk.Menubutton): ...
class Notebook(_BootstyleMixin, _ttk.Notebook): ...
class Panedwindow(_BootstyleMixin, _ttk.Panedwindow): ...
class Progressbar(_BootstyleMixin, _ttk.Progressbar): ...
class Radiobutton(_BootstyleMixin, _ttk.Radiobutton): ...
class Scale(_BootstyleMixin, _ttk.Scale): ...
class Scrollbar(_BootstyleMixin, _ttk.Scrollbar): ...
class Separator(_BootstyleMixin, _ttk.Separator): ...
class Sizegrip(_BootstyleMixin, _ttk.Sizegrip): ...
class Spinbox(_BootstyleMixin, _ttk.Spinbox): ...
class Treeview(_BootstyleMixin, _ttk.Treeview): ...
class OptionMenu(_BootstyleMixin, _ttk.OptionMenu): ...


# Constant re-exported by the widgets module
M: int

__all__ = [
    # Tk exports
    "Tk",
    "Menu",
    "Text",
    "Canvas",
    "Variable",
    "StringVar",
    "IntVar",
    "BooleanVar",
    "DoubleVar",
    "PhotoImage",

    # TTK exports
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

    # ttkbootstrap
    "Bootstyle",
    "Style",
    "Toplevel",
    "Window",
    "DateEntry",
    "Floodgauge",
    "FloodgaugeLegacy",
    "LabeledScale",
    "Meter",
    "M",
]
