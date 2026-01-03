from __future__ import annotations

from tkinter import ttk
from typing import Any, Literal, TypedDict, TYPE_CHECKING
from typing_extensions import Unpack

from ttkbootstrap.core.mixins.ttk_state import TtkStateMixin
from ttkbootstrap.core.mixins.widget import WidgetCapabilitiesMixin
from ttkbootstrap.widgets.internal.wrapper_base import TTKWrapperBase
from ttkbootstrap.widgets.types import Master
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
    bootstyle: str  # DEPRECATED: Use accent and variant instead
    accent: str
    surface_color: str
    style_options: dict[str, Any]


class Spinbox(TextSignalMixin, TTKWrapperBase, WidgetCapabilitiesMixin, TtkStateMixin, ttk.Spinbox):
    """ttkbootstrap wrapper for `ttk.Spinbox` with bootstyle support."""

    _ttk_base = ttk.Spinbox

    def __init__(self, master: Master = None, **kwargs: Unpack[SpinboxKwargs]) -> None:
        """Create a themed ttkbootstrap Spinbox.

        Args:
            master: Parent widget. If None, uses the default root window.

        Other Parameters:
            from_ (float): Minimum value.
            to (float): Maximum value.
            increment (float): Step size between values.
            values (list): Sequence of values to cycle through.
            wrap (bool): Whether to wrap between min/max.
            command (Callable): Callback when the value changes.
            textvariable (Variable): Tk variable linked to the entry text.
            textsignal (Signal): Reactive Signal linked to the text (auto-synced with textvariable).
            format (str): Display format string.
            width (int): Widget width in characters.
            state (str): Widget state.
            takefocus (bool): Whether the widget participates in focus traversal.
            style (str): Explicit ttk style name (overrides accent/variant).
            accent (str): Accent token for styling, e.g. 'primary', 'danger', 'success'.
            bootstyle (str): DEPRECATED - Use `accent` instead.
            surface_color (str): Optional surface token; otherwise inherited.
            style_options (dict): Optional dict forwarded to the style builder.
        """
        super().__init__(master, **kwargs)


