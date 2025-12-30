from __future__ import annotations

from tkinter import ttk
from typing import Any, Callable, Literal, Optional, TYPE_CHECKING, TypedDict

from typing_extensions import Unpack

from ttkbootstrap.core.mixins.ttk_state import TtkStateMixin
from ttkbootstrap.core.mixins.widget import WidgetCapabilitiesMixin
from ttkbootstrap.widgets.internal.wrapper_base import TTKWrapperBase
from ttkbootstrap.widgets.mixins import IconMixin, LocalizationMixin, SignalMixin, TextSignalMixin
from ttkbootstrap.widgets.types import Master

if TYPE_CHECKING:
    from ttkbootstrap.core.signals import Signal


class RadioButtonKwargs(TypedDict, total=False):
    # Standard ttk.Radiobutton options
    text: Any
    command: Optional[Callable[[], Any]]
    image: Any
    icon: Any
    icon_only: bool
    compound: Literal['text', 'image', 'top', 'bottom', 'left', 'right', 'center', 'none'] | str
    variable: Any
    signal: Signal[Any]
    value: Any
    padding: Any
    anchor: str
    width: int
    underline: int
    state: Literal['normal', 'active', 'disabled', 'readonly'] | str
    takefocus: Any
    style: str
    class_: str
    cursor: str
    name: str
    textvariable: Any
    textsignal: Signal[str]

    # ttkbootstrap-specific extensions
    bootstyle: str  # DEPRECATED: Use color and variant instead
    color: str
    variant: str
    surface_color: str
    style_options: dict[str, Any]
    localize: bool | Literal['auto']


class RadioButton(LocalizationMixin, SignalMixin, TextSignalMixin, IconMixin, TTKWrapperBase, WidgetCapabilitiesMixin, TtkStateMixin, ttk.Radiobutton):
    """ttkbootstrap wrapper for `ttk.Radiobutton` with bootstyle and icon support."""

    _ttk_base = ttk.Radiobutton

    def __init__(self, master: Master = None, **kwargs: Unpack[RadioButtonKwargs]) -> None:
        """Create a themed ttkbootstrap Radiobutton.

        Args:
            master: Parent widget. If None, uses the default root window.

        Other Parameters:
            text (str): Text to display.
            textvariable (Variable): Tk variable linked to the text.
            textsignal (Signal[str]): Reactive Signal linked to the text (auto-synced with textvariable).
            command (Callable): Callable invoked when the value is selected.
            image (PhotoImage): Image to display.
            icon (str | dict): Theme-aware icon spec handled by the style system.
            icon_only (bool): Removes the additional padding added for label.
            compound (str): Placement of the image relative to text.
            variable (Variable): Linked Tk variable that receives the selected value.
            signal (Signal): Reactive Signal that receives the selected value (auto-synced with variable).
            value (Any): The value assigned to `variable` when this radio is selected.
            padding (int | tuple): Extra space around the content.
            anchor (str): Determines how the content is aligned in the container. Combination of 'n', 's', 'e', 'w', or 'center' (default).
            width (int): Width of the control in characters.
            underline (int): Index of character to underline in `text`.
            state (str): Widget state.
            takefocus (bool): Whether the widget participates in focus traversal.
            style (str): Explicit ttk style name (overrides color/variant).
            color (str): Color token for styling, e.g. 'primary', 'success', 'danger'.
            variant (str): Style variant, e.g. 'default'.
            bootstyle (str): DEPRECATED - Use `color` and `variant` instead.
                Combined style tokens (e.g., 'primary', 'success').
            surface_color (str): Optional surface token; otherwise inherited.
            style_options (dict): Optional dict forwarded to the style builder.
            localize (bool | Literal['auto']): Determines the widget's localization mode.
        """
        kwargs.update(style_options=self._capture_style_options(['icon_only', 'icon', 'anchor'], kwargs))
        super().__init__(master, **kwargs)
