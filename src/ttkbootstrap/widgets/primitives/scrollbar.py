from __future__ import annotations

from tkinter import ttk
from typing import Any, TypedDict
from typing_extensions import Unpack
from ttkbootstrap.widgets._internal.wrapper_base import TTKWrapperBase
from ttkbootstrap.widgets.types import Master


class ScrollbarKwargs(TypedDict, total=False):
    # Standard ttk.Scrollbar options
    orient: Any
    command: Any
    takefocus: Any
    style: str
    class_: str
    cursor: str
    name: str

    # ttkbootstrap-specific extensions
    bootstyle: str
    surface_color: str
    style_options: dict[str, Any]


class Scrollbar(TTKWrapperBase, ttk.Scrollbar):
    """ttkbootstrap wrapper for `ttk.Scrollbar` with bootstyle support."""

    _ttk_base = ttk.Scrollbar

    def __init__(self, master: Master = None, **kwargs: Unpack[ScrollbarKwargs]) -> None:
        """Create a themed ttkbootstrap Scrollbar.

        Args:
            master: Parent widget. If None, uses the default root window.

        Other Parameters:
            orient (str): Orientation of the scrollbar ('horizontal' or 'vertical').
            command (Callable): Scroll command callback.
            takefocus (bool): Whether the widget participates in focus traversal.
            style (str): Explicit ttk style name (overrides bootstyle).
            bootstyle (str): ttkbootstrap style tokens (e.g., 'primary', 'danger-square').
            surface_color (str): Optional surface token; otherwise inherited.
            style_options (dict): Optional dict forwarded to the style builder.
        """
        super().__init__(master, **kwargs)


