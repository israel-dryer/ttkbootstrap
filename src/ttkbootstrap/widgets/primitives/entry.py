from __future__ import annotations

from tkinter import ttk
from typing import Any, Literal, Optional, TypedDict, TYPE_CHECKING
from typing_extensions import Unpack

from ttkbootstrap.core.mixins.ttk_state import TtkStateMixin
from ttkbootstrap.core.mixins.widget import WidgetCapabilitiesMixin
from ttkbootstrap.widgets.internal.wrapper_base import TTKWrapperBase
from ttkbootstrap.widgets.types import Master
from ..mixins import TextSignalMixin

if TYPE_CHECKING:
    from ttkbootstrap.core.signals import Signal


class EntryKwargs(TypedDict, total=False):
    # Standard ttk.Entry options
    textvariable: Any
    textsignal: Signal[str]
    show: Any
    width: int
    exportselection: bool
    justify: Any
    validate: Any
    validatecommand: Any
    invalidcommand: Any
    xscrollcommand: Any
    font: Any
    foreground: str
    background: str
    state: Literal['normal', 'disabled', 'readonly'] | str
    takefocus: Any
    style: str
    class_: str
    cursor: str
    name: str

    # ttkbootstrap-specific extensions
    bootstyle: str  # DEPRECATED: Use color and variant instead
    color: str
    variant: str
    surface_color: str
    style_options: dict[str, Any]


class Entry(TextSignalMixin, TTKWrapperBase, WidgetCapabilitiesMixin, TtkStateMixin, ttk.Entry):
    """ttkbootstrap wrapper for `ttk.Entry` with bootstyle support."""

    _ttk_base = ttk.Entry

    def __init__(self, master: Master = None, **kwargs: Unpack[EntryKwargs]) -> None:
        """Create a themed ttkbootstrap Entry.

        Args:
            master: Parent widget. If None, uses the default root window.

        Other Parameters:
            textvariable (Variable): Tk variable linked to the entry text.
            textsignal (Signal[str]): Reactive Signal linked to the entry text (auto-synced with textvariable).
            show (str): Substitute character for masked input.
            width (int): Width in characters.
            exportselection (bool): Whether selection is exported to X clipboard.
            justify (str): Text alignment inside the entry.
            validate (str): Validation mode.
            validatecommand (Callable): Validation callback.
            invalidcommand (Callable): Callback executed on validation failure.
            xscrollcommand (Callable): Horizontal scroll callback.
            font (str | Font): Font for the entry text.
            foreground (str): Text color.
            background (str): Background color.
            state (str): Widget state.
            takefocus (bool): Whether the widget participates in focus traversal.
            style (str): Explicit ttk style name (overrides color/variant).
            color (str): Color token for styling, e.g. 'primary', 'danger', 'success'.
            variant (str): Style variant, e.g. 'default'.
            bootstyle (str): DEPRECATED - Use `color` and `variant` instead.
                Combined style tokens (e.g., 'primary').
            surface_color (str): Optional surface token; otherwise inherited.
            style_options (dict): Optional dict forwarded to the style builder.
        """
        super().__init__(master, **kwargs)


