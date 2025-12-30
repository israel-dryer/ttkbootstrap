from __future__ import annotations

from tkinter import ttk
from typing import Any, Literal, TypedDict

from typing_extensions import Unpack

from ttkbootstrap.core.mixins.ttk_state import TtkStateMixin
from ttkbootstrap.core.mixins.widget import WidgetCapabilitiesMixin
from ttkbootstrap.widgets.internal.wrapper_base import TTKWrapperBase
from ttkbootstrap.widgets.mixins import LocalizationMixin
from ttkbootstrap.widgets.types import Master


class LabelFrameKwargs(TypedDict, total=False):
    # Standard ttk.Labelframe options
    text: Any
    labelanchor: Any
    padding: Any
    relief: Any
    borderwidth: Any
    width: int
    height: int
    style: str
    class_: str
    cursor: str
    name: str

    # ttkbootstrap-specific extensions
    bootstyle: str  # DEPRECATED: Use color and variant instead
    color: str
    surface_color: str
    style_options: dict[str, Any]
    localize: bool | Literal['auto']


class LabelFrame(LocalizationMixin, TTKWrapperBase, WidgetCapabilitiesMixin, TtkStateMixin, ttk.LabelFrame):
    """ttkbootstrap wrapper for `ttk.Labelframe` with bootstyle support."""

    _ttk_base = ttk.Labelframe

    def __init__(self, master: Master = None, **kwargs: Unpack[LabelFrameKwargs]) -> None:
        """Create a themed ttkbootstrap Labelframe.

        Args:
            master: Parent widget. If None, uses the default root window.

        Other Parameters:
            text (str): Text for the embedded label.
            labelanchor (str): Position of the label relative to the frame.
            padding (int | tuple): Extra internal padding.
            relief (str): Border style.
            borderwidth (int): Border width.
            width (int): Requested width in pixels.
            height (int): Requested height in pixels.
            style (str): Explicit ttk style name (overrides color/variant).
            color (str): Color token for styling, e.g. 'primary', 'secondary'.
            bootstyle (str): DEPRECATED - Use `color` instead.
            surface_color (str): Optional surface token; otherwise inherited.
            style_options (dict): Optional dict forwarded to the style builder.
            localize (bool | Literal['auto']): Determines the widget's localization mode.
        """
        super().__init__(master, **kwargs)
