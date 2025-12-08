from __future__ import annotations

from tkinter import ttk
from typing import Any, TypedDict, TYPE_CHECKING
from typing_extensions import Unpack
from ._internal.wrapper_base import TTKWrapperBase
from .mixins import SignalMixin

if TYPE_CHECKING:
    from ttkbootstrap.core.signals import Signal


class ScaleKwargs(TypedDict, total=False):
    # Standard ttk.Scale options
    from_: float
    to: float
    value: float
    variable: Any
    signal: Signal[Any]
    orient: Any
    length: Any
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


class Scale(SignalMixin, TTKWrapperBase, ttk.Scale):
    """ttkbootstrap wrapper for `ttk.Scale` with bootstyle support."""

    _ttk_base = ttk.Scale

    def __init__(self, master=None, **kwargs: Unpack[ScaleKwargs]) -> None:
        """Create a themed ttkbootstrap Scale.

        Keyword Args:
            from_: Minimum value.
            to: Maximum value.
            value: Initial value.
            variable: Tk variable linked to the value.
            signal: Reactive Signal linked to the value (auto-synced with variable).
            orient: Orientation of the scale.
            length: Scale length.
            command: Callback on value change.
            takefocus: Whether the widget participates in focus traversal.
            style: Explicit ttk style name (overrides bootstyle).
            bootstyle: ttkbootstrap style tokens (e.g., 'primary').
            surface_color: Optional surface token; otherwise inherited.
            style_options: Optional dict forwarded to the style builder.
        """
        super().__init__(master, **kwargs)

