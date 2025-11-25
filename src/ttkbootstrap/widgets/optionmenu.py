from __future__ import annotations

from tkinter import ttk
from typing import Any, TypedDict, TYPE_CHECKING
from typing_extensions import Unpack
from ._internal.wrapper_base import TTKWrapperBase
from .mixins import SignalMixin

if TYPE_CHECKING:
    from ttkbootstrap.signals import Signal


class OptionMenuKwargs(TypedDict, total=False):
    # Standard ttk.OptionMenu keyword options (positional args handled separately)
    signal: Signal[Any]
    style: str
    class_: str
    cursor: str
    name: str

    # ttkbootstrap-specific extensions
    bootstyle: str
    surface_color: str
    style_options: dict[str, Any]


class OptionMenu(SignalMixin, TTKWrapperBase, ttk.OptionMenu):
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
            signal: Reactive Signal linked to the variable (auto-synced with the variable
                passed as the first positional argument).
            style: Explicit ttk style name (overrides bootstyle).
            bootstyle: ttkbootstrap style tokens.
            surface_color: Optional surface token; otherwise inherited.
            style_options: Optional dict forwarded to the style builder.
        """
        super().__init__(master, *om_args, **kwargs)
