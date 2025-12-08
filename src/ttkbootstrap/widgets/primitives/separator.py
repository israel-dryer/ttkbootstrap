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

        Keyword Args:
            orient: Orientation of the separator.
            style: Explicit ttk style name (overrides bootstyle).
            bootstyle: ttkbootstrap style tokens.
            surface_color: Optional surface token; otherwise inherited.
            style_options: Optional dict forwarded to the style builder.
        """
        super().__init__(master, **kwargs)


