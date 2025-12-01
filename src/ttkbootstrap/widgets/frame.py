from __future__ import annotations

from tkinter import ttk
from typing import Any, TypedDict
from typing_extensions import Unpack
from ._internal.wrapper_base import TTKWrapperBase


class FrameKwargs(TypedDict, total=False):
    # Standard ttk.Frame options
    padding: Any
    relief: Any
    borderwidth: Any
    width: int
    height: int
    style: str
    class_: str
    cursor: str
    name: str
    show_border: bool

    # ttkbootstrap-specific extensions
    bootstyle: str
    surface_color: str
    style_options: dict[str, Any]


class Frame(TTKWrapperBase, ttk.Frame):
    """ttkbootstrap wrapper for `ttk.Frame` with bootstyle support."""

    _ttk_base = ttk.Frame

    def __init__(self, master=None, **kwargs: Unpack[FrameKwargs]) -> None:
        """Create a themed ttkbootstrap Frame.

        Keyword Args:
            padding: Extra padding inside the frame.
            relief: Border style.
            borderwidth: Border width.
            width: Requested width in pixels.
            height: Requested height in pixels.
            style: Explicit ttk style name (overrides bootstyle).
            bootstyle: ttkbootstrap style tokens (e.g., 'secondary').
            surface_color: Optional surface token; otherwise inherited.
            show_border: If true, draws a border around the frame.
            style_options: Optional dict forwarded to the style builder.
        """
        show_border = kwargs.pop('show_border', False)
        style_options = kwargs.pop('style_options', {})
        style_options['show_border'] = show_border
        super().__init__(master, style_options=style_options, **kwargs)

