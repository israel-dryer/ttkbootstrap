from __future__ import annotations

from tkinter import ttk
from typing import Any, TypedDict, Unpack

from .._internal.wrapper_base import TTKWrapperBase


class NotebookKwargs(TypedDict, total=False):
    # Standard ttk.Notebook options
    padding: Any
    height: int
    width: int
    style: str
    class_: str
    cursor: str
    name: str

    # ttkbootstrap-specific extensions
    bootstyle: str
    surface_color: str
    style_options: dict[str, Any]


class Notebook(TTKWrapperBase, ttk.Notebook):
    """ttkbootstrap wrapper for `ttk.Notebook` with bootstyle support."""

    _ttk_base = ttk.Notebook

    def __init__(self, master=None, **kwargs: Unpack[NotebookKwargs]) -> None:
        """Create a themed ttkbootstrap Notebook.

        Keyword Args:
            padding: Padding around tab area and content area.
            height: Requested height in pixels.
            width: Requested width in pixels.
            style: Explicit ttk style name (overrides bootstyle).
            bootstyle: ttkbootstrap style tokens (e.g., 'primary').
            surface_color: Optional surface token; otherwise inherited.
            style_options: Optional dict forwarded to the style builder.
        """
        super().__init__(master, **kwargs)

