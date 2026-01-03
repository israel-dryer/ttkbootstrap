from __future__ import annotations

from tkinter import ttk
from typing import Any, Literal, TypedDict, TYPE_CHECKING
from typing_extensions import Unpack

from ttkbootstrap.core.mixins.ttk_state import TtkStateMixin
from ttkbootstrap.core.mixins.widget import WidgetCapabilitiesMixin
from ttkbootstrap.widgets.internal.wrapper_base import TTKWrapperBase
from ttkbootstrap.widgets.mixins.configure_mixin import configure_delegate
from ttkbootstrap.widgets.types import Master
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
    bootstyle: str  # DEPRECATED: Use accent and variant instead
    accent: str
    variant: str
    surface: str
    style_options: dict[str, Any]


class Progressbar(SignalMixin, TTKWrapperBase, WidgetCapabilitiesMixin, TtkStateMixin, ttk.Progressbar):
    """ttkbootstrap wrapper for `ttk.Progressbar` with bootstyle support."""

    _ttk_base = ttk.Progressbar

    def __init__(self, master: Master = None, **kwargs: Unpack[ProgressbarKwargs]) -> None:
        """Create a themed ttkbootstrap Progressbar.

        Args:
            master: Parent widget. If None, uses the default root window.

        Other Parameters:
            mode (str): Progress mode ('determinate' or 'indeterminate').
            orient (str): Orientation of the bar ('horizontal' or 'vertical').
            length (int): Requested length of the progress bar in pixels.
            maximum (float): Maximum value.
            value (float): Current value.
            variable (Variable): Tk variable linked to the value.
            signal (Signal): Reactive Signal linked to the value (auto-synced with variable).
            phase (int): Animation phase for indeterminate mode.
            style (str): Explicit ttk style name (overrides accent/variant).
            accent (str): Accent token for styling, e.g. 'primary', 'success', 'danger'.
            variant (str): Style variant, e.g. 'default', 'striped'.
            bootstyle (str): DEPRECATED - Use `accent` and `variant` instead.
                Combined style tokens (e.g., 'success', 'striped').
            surface (str): Optional surface token; otherwise inherited.
            style_options (dict): Optional dict forwarded to the style builder.
        """
        super().__init__(master, **kwargs)

    def get(self) -> float:
        """Return the current progress value."""
        return self.cget('value')

    def set(self, value: float) -> None:
        """Set the progress value."""
        self.configure(value=value)

    @property
    def value(self) -> float:
        """Get or set the progress value."""
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


