from __future__ import annotations

from tkinter import ttk
from typing import Any, Literal, TypedDict, TYPE_CHECKING
from typing_extensions import Unpack
from ttkbootstrap.widgets._internal.wrapper_base import TTKWrapperBase
from ..mixins import TextSignalMixin

if TYPE_CHECKING:
    from ttkbootstrap.core.signals import Signal


class SpinboxKwargs(TypedDict, total=False):
    # Standard ttk.Spinbox options
    from_: float
    to: float
    increment: float
    values: Any
    wrap: bool
    command: Any
    textvariable: Any
    textsignal: Signal[Any]
    format: str
    width: int
    state: Literal['normal','disabled','readonly'] | str
    takefocus: Any
    style: str
    class_: str
    cursor: str
    name: str

    # ttkbootstrap-specific extensions
    bootstyle: str
    surface_color: str
    style_options: dict[str, Any]


class Spinbox(TextSignalMixin, TTKWrapperBase, ttk.Spinbox):
    """ttkbootstrap wrapper for `ttk.Spinbox` with bootstyle support."""

    _ttk_base = ttk.Spinbox

    def __init__(self, master=None, **kwargs: Unpack[SpinboxKwargs]) -> None:
        """Create a themed ttkbootstrap Spinbox.

        Keyword Args:
            from_: Minimum value.
            to: Maximum value.
            increment: Step size between values.
            values: Sequence of values to cycle through.
            wrap: Whether to wrap between min/max.
            command: Callback when the value changes.
            textvariable: Tk variable linked to the entry text.
            textsignal: Reactive Signal linked to the text (auto-synced with textvariable).
            format: Display format string.
            width: Widget width in characters.
            state: Widget state.
            takefocus: Whether the widget participates in focus traversal.
            style: Explicit ttk style name (overrides bootstyle).
            bootstyle: ttkbootstrap style tokens.
            surface_color: Optional surface token; otherwise inherited.
            style_options: Optional dict forwarded to the style builder.
        """
        super().__init__(master, **kwargs)


