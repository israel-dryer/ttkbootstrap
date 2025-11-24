from __future__ import annotations

from tkinter import ttk
from typing import Any, TypedDict
from typing_extensions import Unpack
from ._internal.wrapper_base import TTKWrapperBase


class OptionMenuKwargs(TypedDict, total=False):
    # Standard ttk.OptionMenu keyword options (positional args handled separately)
    style: str
    class_: str
    cursor: str
    name: str

    # ttkbootstrap-specific extensions
    bootstyle: str
    surface_color: str
    style_options: dict[str, Any]


class OptionMenu(TTKWrapperBase, ttk.OptionMenu):
    """ttkbootstrap wrapper for `ttk.OptionMenu` with bootstyle support.

    Note:
        ttk.OptionMenu requires positional arguments `(variable, default, *values)` in
        addition to keyword configuration. This wrapper preserves that signature.
    """

    _ttk_base = ttk.OptionMenu

    def __init__(self, master=None, *om_args: Any, **kwargs: Unpack[OptionMenuKwargs]) -> None:
        """Create a themed ttkbootstrap OptionMenu.

        Positional Args:
            *om_args: `(variable, default, *values)` as required by ttk.OptionMenu.

        Keyword Args:
            style: Explicit ttk style name (overrides bootstyle).
            bootstyle: ttkbootstrap style tokens.
            surface_color: Optional surface token; otherwise inherited.
            style_options: Optional dict forwarded to the style builder.
        """
        super().__init__(master, *om_args, **kwargs)
