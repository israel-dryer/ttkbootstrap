from __future__ import annotations

from tkinter import ttk
from typing import Any, TypedDict, Unpack

from .._internal.wrapper_base import TTKWrapperBase


class SizegripKwargs(TypedDict, total=False):
    # Standard ttk.Sizegrip options
    style: str
    class_: str
    cursor: str
    name: str

    # ttkbootstrap-specific extensions
    bootstyle: str
    surface_color: str
    style_options: dict[str, Any]


class Sizegrip(TTKWrapperBase, ttk.Sizegrip):
    """ttkbootstrap wrapper for `ttk.Sizegrip` with bootstyle support."""

    _ttk_base = ttk.Sizegrip

    def __init__(self, master=None, **kwargs: Unpack[SizegripKwargs]) -> None:
        """Create a themed ttkbootstrap Sizegrip.

        Keyword Args:
            style: Explicit ttk style name (overrides bootstyle).
            bootstyle: ttkbootstrap style tokens.
            surface_color: Optional surface token; otherwise inherited.
            style_options: Optional dict forwarded to the style builder.
        """
        super().__init__(master, **kwargs)

