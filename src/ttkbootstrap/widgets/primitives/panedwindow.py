from __future__ import annotations

from tkinter import ttk
from typing import Any, TypedDict
from typing_extensions import Unpack
from ttkbootstrap.widgets._internal.wrapper_base import TTKWrapperBase


class PanedwindowKwargs(TypedDict, total=False):
    # Standard ttk.Panedwindow options
    orient: Any
    padding: Any
    width: int
    height: int
    style: str
    class_: str
    cursor: str
    name: str

    # ttkbootstrap-specific extensions
    bootstyle: str
    surface_color: str
    style_options: dict[str, Any]


class Panedwindow(TTKWrapperBase, ttk.Panedwindow):
    """ttkbootstrap wrapper for `ttk.Panedwindow` with bootstyle support."""

    _ttk_base = ttk.Panedwindow

    def __init__(self, master=None, **kwargs: Unpack[PanedwindowKwargs]) -> None:
        """Create a themed ttkbootstrap Panedwindow.

        Keyword Args:
            orient: Orientation of panes ('horizontal' or 'vertical').
            padding: Extra internal padding.
            width: Requested width in pixels.
            height: Requested height in pixels.
            style: Explicit ttk style name (overrides bootstyle).
            bootstyle: ttkbootstrap style tokens.
            surface_color: Optional surface token; otherwise inherited.
            style_options: Optional dict forwarded to the style builder.
        """
        super().__init__(master, **kwargs)


