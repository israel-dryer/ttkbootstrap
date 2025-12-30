from __future__ import annotations

from tkinter import ttk
from typing import Any, Literal, TYPE_CHECKING, TypedDict

from typing_extensions import Unpack

from ttkbootstrap.core.mixins.ttk_state import TtkStateMixin
from ttkbootstrap.core.mixins.widget import WidgetCapabilitiesMixin
from ttkbootstrap.widgets.internal.wrapper_base import TTKWrapperBase
from ttkbootstrap.widgets.mixins import IconMixin, LocalizationMixin, TextSignalMixin
from ttkbootstrap.widgets.types import Master

if TYPE_CHECKING:
    from ttkbootstrap.core.signals import Signal


class LabelKwargs(TypedDict, total=False):
    # Standard ttk.Label options
    text: Any
    image: Any
    icon: Any
    icon_only: bool
    compound: Literal['text', 'image', 'top', 'bottom', 'left', 'right', 'center', 'none'] | str
    anchor: Any
    justify: Any
    padding: Any
    width: int
    wraplength: Any
    font: Any
    foreground: str
    background: str
    relief: Any
    localize: bool | Literal['auto']
    value_format: dict | str
    state: Literal['normal', 'active', 'disabled', 'readonly'] | str
    takefocus: Any
    format_spec: str | dict
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


class Label(LocalizationMixin, TextSignalMixin, IconMixin, TTKWrapperBase, WidgetCapabilitiesMixin, TtkStateMixin, ttk.Label):
    """ttkbootstrap wrapper for `ttk.Label` with bootstyle and icon support."""

    _ttk_base = ttk.Label

    def __init__(self, master: Master = None, **kwargs: Unpack[LabelKwargs]) -> None:
        """Create a themed ttkbootstrap Label.

        Args:
            master: Parent widget. If None, uses the default root window.

        Other Parameters:
            text (str): Text to display in the label.
            textvariable (Variable): Tk variable linked to the label text.
            textsignal (Signal[str]): Reactive Signal linked to the label text (auto-synced with textvariable).
            image (PhotoImage): Image to display.
            icon (str | dict): Theme-aware icon spec handled by the style system.
            icon_only (bool): If True, removes the additional padding reserved for label text.
            compound (str): Placement of the image relative to text.
            anchor (str): Alignment of the label's content within its area.
            justify (str): How to justify multiple lines of text.
            localize (bool | Literal['auto']): Determines the widget's localization mode.
            value_format (str | dict): Format specification for the label value.
            padding (int | tuple): Extra space around the label content.
            width (int): Width of the label in characters.
            wraplength (int): Maximum width before wrapping text.
            font (str | Font): Font for text.
            foreground (str): Text color.
            background (str): Background color.
            relief (str): Border style.
            state (str): Widget state.
            takefocus (bool): Whether the widget participates in focus traversal.
            style (str): Explicit ttk style name (overrides color/variant).
            color (str): Color token for styling, e.g. 'primary', 'danger', 'success'.
            variant (str): Style variant, e.g. 'default', 'inverse'.
            bootstyle (str): DEPRECATED - Use `color` and `variant` instead.
                Combined style tokens (e.g., 'secondary', 'info').
            surface_color (str): Optional surface token; otherwise inherited.
            style_options (dict): Optional dict forwarded to the style builder.
        """
        kwargs.update(style_options=self._capture_style_options(['icon_only', 'icon'], kwargs))
        super().__init__(master, **kwargs)
