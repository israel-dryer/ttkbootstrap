from __future__ import annotations

from tkinter import ttk
from typing import Any, Literal, TypedDict, TYPE_CHECKING
from typing_extensions import Unpack
from ttkbootstrap.widgets._internal.wrapper_base import TTKWrapperBase
from ..mixins import SignalMixin

if TYPE_CHECKING:
    from ttkbootstrap.core.signals import Signal


class ProgressbarKwargs(TypedDict, total=False):
    # Standard ttk.Progressbar options
    mode: Literal['determinate', 'indeterminate'] | str
    orient: Any
    length: Any
    maximum: float
    value: float
    variable: Any
    signal: Signal[Any]
    phase: int
    style: str
    class_: str
    cursor: str
    name: str

    # ttkbootstrap-specific extensions
    bootstyle: str
    surface_color: str
    style_options: dict[str, Any]


class Progressbar(SignalMixin, TTKWrapperBase, ttk.Progressbar):
    """ttkbootstrap wrapper for `ttk.Progressbar` with bootstyle support."""

    _ttk_base = ttk.Progressbar

    def __init__(self, master=None, **kwargs: Unpack[ProgressbarKwargs]) -> None:
        """Create a themed ttkbootstrap Progressbar.

        Keyword Args:
            mode: Progress mode ('determinate' or 'indeterminate').
            orient: Orientation of the bar.
            length: Requested length of the progress bar.
            maximum: Maximum value.
            value: Current value.
            variable: Tk variable linked to the value.
            signal: Reactive Signal linked to the value (auto-synced with variable).
            phase: Animation phase for indeterminate mode.
            style: Explicit ttk style name (overrides bootstyle).
            bootstyle: ttkbootstrap style tokens (e.g., 'success', 'striped').
            surface_color: Optional surface token; otherwise inherited.
            style_options: Optional dict forwarded to the style builder.
        """
        super().__init__(master, **kwargs)


