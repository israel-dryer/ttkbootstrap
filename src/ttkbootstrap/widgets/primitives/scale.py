from __future__ import annotations

from tkinter import ttk
from typing import Any, TypedDict, TYPE_CHECKING
from typing_extensions import Unpack

from ttkbootstrap.core.mixins.ttk_state import TtkStateMixin
from ttkbootstrap.core.mixins.widget import WidgetCapabilitiesMixin
from ttkbootstrap.widgets.internal.wrapper_base import TTKWrapperBase
from ttkbootstrap.widgets.mixins.configure_mixin import configure_delegate
from ttkbootstrap.widgets.types import Master
from ..mixins import SignalMixin

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
    bootstyle: str  # DEPRECATED: Use accent and variant instead
    accent: str
    surface: str
    style_options: dict[str, Any]


class Scale(SignalMixin, TTKWrapperBase, WidgetCapabilitiesMixin, TtkStateMixin, ttk.Scale):
    """ttkbootstrap wrapper for `ttk.Scale` with bootstyle support."""

    _ttk_base = ttk.Scale

    def __init__(self, master: Master = None, **kwargs: Unpack[ScaleKwargs]) -> None:
        """Create a themed ttkbootstrap Scale.

        Args:
            master: Parent widget. If None, uses the default root window.

        Other Parameters:
            from_ (float): Minimum value.
            to (float): Maximum value.
            value (float): Initial value.
            variable (Variable): Tk variable linked to the value.
            signal (Signal): Reactive Signal linked to the value (auto-synced with variable).
            orient (str): Orientation of the scale ('horizontal' or 'vertical').
            length (int): Scale length in pixels.
            command (Callable): Callback on value change.
            takefocus (bool): Whether the widget participates in focus traversal.
            accent (str): Accent token for styling, e.g. 'primary', 'success', 'danger'.
            bootstyle (str): DEPRECATED - Use `accent` instead.
            surface (str): Optional surface token; otherwise inherited.
            style_options (dict): Optional dict forwarded to the style builder.
        """
        super().__init__(master, **kwargs)

    @property
    def value(self) -> float:
        """Get or set the scale's current value."""
        return self.get()

    @value.setter
    def value(self, value: float) -> None:
        self.set(value)

    @configure_delegate('value')
    def _delegate_value(self, value=None):
        """Get or set the value via configure."""
        if value is None:
            return self.get()
        self.set(value)


