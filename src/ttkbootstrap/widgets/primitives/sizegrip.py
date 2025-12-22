from __future__ import annotations

from tkinter import ttk
from typing import Any, TypedDict
from typing_extensions import Unpack
from ttkbootstrap.widgets._internal.wrapper_base import TTKWrapperBase
from ttkbootstrap.widgets.types import Master


class SizeGripKwargs(TypedDict, total=False):
    # Standard ttk.Sizegrip options
    style: str
    class_: str
    cursor: str
    name: str

    # ttkbootstrap-specific extensions
    bootstyle: str
    surface_color: str
    style_options: dict[str, Any]


class SizeGrip(TTKWrapperBase, ttk.Sizegrip):
    """ttkbootstrap wrapper for `ttk.Sizegrip` with bootstyle support."""

    _ttk_base = ttk.Sizegrip

    def __init__(self, master: Master = None, **kwargs: Unpack[SizeGripKwargs]) -> None:
        """Create a themed ttkbootstrap Sizegrip.

        Args:
            master: Parent widget. If None, uses the default root window.

        Other Parameters:
            style (str): Explicit ttk style name (overrides bootstyle).
            bootstyle (str): ttkbootstrap style tokens.
            surface_color (str): Optional surface token; otherwise inherited.
            style_options (dict): Optional dict forwarded to the style builder.
        """
        super().__init__(master, **kwargs)


