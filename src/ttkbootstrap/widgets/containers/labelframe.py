from __future__ import annotations

from tkinter import ttk
from typing import Any, TypedDict, Unpack

from .._internal.wrapper_base import TTKWrapperBase


class LabelframeKwargs(TypedDict, total=False):
    # Standard ttk.Labelframe options
    text: Any
    labelanchor: Any
    padding: Any
    relief: Any
    borderwidth: Any
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


class Labelframe(TTKWrapperBase, ttk.Labelframe):
    """ttkbootstrap wrapper for `ttk.Labelframe` with bootstyle support."""

    _ttk_base = ttk.Labelframe

    def __init__(self, master=None, **kwargs: Unpack[LabelframeKwargs]) -> None:
        """Create a themed ttkbootstrap Labelframe.

        Keyword Args:
            text: Text for the embedded label.
            labelanchor: Position of the label relative to the frame.
            padding: Extra internal padding.
            relief: Border style.
            borderwidth: Border width.
            width: Requested width in pixels.
            height: Requested height in pixels.
            style: Explicit ttk style name (overrides bootstyle).
            bootstyle: ttkbootstrap style tokens.
            surface_color: Optional surface token; otherwise inherited.
            style_options: Optional dict forwarded to the style builder.
        """
        super().__init__(master, **kwargs)

