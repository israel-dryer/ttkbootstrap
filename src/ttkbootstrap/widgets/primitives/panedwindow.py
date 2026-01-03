from __future__ import annotations

from tkinter import ttk
from typing import Any, TypedDict
from typing_extensions import Unpack

from ttkbootstrap.core.mixins.ttk_state import TtkStateMixin
from ttkbootstrap.core.mixins.widget import WidgetCapabilitiesMixin
from ttkbootstrap.widgets.internal.wrapper_base import TTKWrapperBase
from ttkbootstrap.widgets.types import Master


class PanedWindowKwargs(TypedDict, total=False):
    # Standard ttk.Panedwindow options
    orient: Any
    padding: Any
    width: int
    height: int
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


class PanedWindow(TTKWrapperBase, WidgetCapabilitiesMixin, TtkStateMixin, ttk.PanedWindow):
    """ttkbootstrap wrapper for `ttk.Panedwindow` with bootstyle support."""

    _ttk_base = ttk.Panedwindow

    def __init__(self, master: Master = None, **kwargs: Unpack[PanedWindowKwargs]) -> None:
        """Create a themed ttkbootstrap Panedwindow.

        Args:
            master: Parent widget. If None, uses the default root window.

        Other Parameters:
            orient (str): Orientation of panes ('horizontal' or 'vertical').
            padding (int | tuple): Extra internal padding.
            width (int): Requested width in pixels.
            height (int): Requested height in pixels.
            style (str): Explicit ttk style name (overrides accent/variant).
            accent (str): Accent token for styling, e.g. 'primary', 'secondary'.
            variant (str): Style variant (if applicable).
            bootstyle (str): DEPRECATED - Use `accent` and `variant` instead.
                Combined style tokens.
            surface (str): Optional surface token; otherwise inherited.
            style_options (dict): Optional dict forwarded to the style builder.
        """
        super().__init__(master, **kwargs)


