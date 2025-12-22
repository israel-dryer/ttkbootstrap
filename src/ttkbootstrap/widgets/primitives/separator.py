from __future__ import annotations

from tkinter import ttk
from typing import Any, TypedDict
from typing_extensions import Unpack
from ttkbootstrap.widgets._internal.wrapper_base import TTKWrapperBase


class SeparatorKwargs(TypedDict, total=False):
    # Standard ttk.Separator options
    orient: Any
    style: str
    class_: str
    cursor: str
    name: str

    # ttkbootstrap-specific extensions
    bootstyle: str
    surface_color: str
    style_options: dict[str, Any]


class Separator(TTKWrapperBase, ttk.Separator):
    """ttkbootstrap wrapper for `ttk.Separator` with bootstyle support."""

    _ttk_base = ttk.Separator

    def __init__(self, master=None, **kwargs: Unpack[SeparatorKwargs]) -> None:
        """Create a themed ttkbootstrap Separator.

        Args:
            master: Parent widget. If None, uses the default root window.

        Other Parameters:
            orient (str): Orientation of the separator ('horizontal' or 'vertical').
            style (str): Explicit ttk style name (overrides bootstyle).
            bootstyle (str): ttkbootstrap style tokens.
            surface_color (str): Optional surface token; otherwise inherited.
            style_options (dict): Optional dict forwarded to the style builder.
        """
        super().__init__(master, **kwargs)


