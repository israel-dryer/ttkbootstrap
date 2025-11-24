from __future__ import annotations

from tkinter import ttk
from typing import Any, TypedDict
from typing_extensions import Unpack
from ._internal.wrapper_base import TTKWrapperBase


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

    def __init__(self, master=None, **kwargs: Unpack[ScrollbarKwargs]) -> None:
        """Create a themed ttkbootstrap Scrollbar.

        Keyword Args:
            orient: Orientation of the scrollbar.
            command: Scroll command callback.
            takefocus: Whether the widget participates in focus traversal.
            style: Explicit ttk style name (overrides bootstyle).
            bootstyle: ttkbootstrap style tokens (e.g., 'primary', 'danger-square').
            surface_color: Optional surface token; otherwise inherited.
            style_options: Optional dict forwarded to the style builder.
        """
        super().__init__(master, **kwargs)

