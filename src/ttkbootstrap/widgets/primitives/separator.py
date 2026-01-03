from __future__ import annotations

from tkinter import ttk
from typing import Any, TypedDict
from typing_extensions import Unpack

from ttkbootstrap.core.mixins.ttk_state import TtkStateMixin
from ttkbootstrap.core.mixins.widget import WidgetCapabilitiesMixin
from ttkbootstrap.widgets.internal.wrapper_base import TTKWrapperBase
from ttkbootstrap.widgets.types import Master


class SeparatorKwargs(TypedDict, total=False):
    # Standard ttk.Separator options
    orient: Any
    style: str
    class_: str
    cursor: str
    name: str

    # ttkbootstrap-specific extensions
    bootstyle: str  # DEPRECATED: Use accent and variant instead
    accent: str
    surface: str
    style_options: dict[str, Any]


class Separator(TTKWrapperBase, WidgetCapabilitiesMixin, TtkStateMixin, ttk.Separator):
    """ttkbootstrap wrapper for `ttk.Separator` with bootstyle support."""

    _ttk_base = ttk.Separator

    def __init__(self, master: Master = None, **kwargs: Unpack[SeparatorKwargs]) -> None:
        """Create a themed ttkbootstrap Separator.

        Args:
            master: Parent widget. If None, uses the default root window.

        Other Parameters:
            orient (str): Orientation of the separator ('horizontal' or 'vertical').
            style (str): Explicit ttk style name (overrides accent/variant).
            accent (str): Accent token for styling, e.g. 'primary', 'secondary'.
            bootstyle (str): DEPRECATED - Use `accent` and `variant` instead.
                Combined style tokens.
            surface (str): Optional surface token; otherwise inherited.
            style_options (dict): Optional dict forwarded to the style builder.
        """
        super().__init__(master, **kwargs)


