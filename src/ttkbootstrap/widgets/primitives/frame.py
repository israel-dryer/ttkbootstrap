from __future__ import annotations

from tkinter import ttk
from typing import Any, TypedDict

from typing_extensions import Unpack

from ttkbootstrap.widgets._internal.wrapper_base import TTKWrapperBase
from ..mixins import configure_delegate


class FrameKwargs(TypedDict, total=False):
    # Standard ttk.Frame options
    padding: Any
    relief: Any
    borderwidth: Any
    width: int
    height: int
    style: str
    class_: str
    cursor: str
    name: str
    takefocus: bool

    # ttkbootstrap-specific extensions
    bootstyle: str
    surface_color: str
    show_border: bool
    style_options: dict[str, Any]


class Frame(TTKWrapperBase, ttk.Frame):
    """ttkbootstrap wrapper for `ttk.Frame` with bootstyle support."""

    _ttk_base = ttk.Frame

    def __init__(self, master=None, **kwargs: Unpack[FrameKwargs]) -> None:
        """Create a themed ttkbootstrap Frame.

        Keyword Args:
            padding: Extra padding inside the frame.
            relief: Border style.
            borderwidth: Border width.
            width: Requested width in pixels.
            height: Requested height in pixels.
            takefocus: Widget accepts focus during keyboard traversal.
            style: Explicit ttk style name (overrides bootstyle).
            bootstyle: ttkbootstrap style tokens (e.g., 'secondary').
            surface_color: Optional surface token; otherwise inherited.
            show_border: If true, draws a border around the frame.
            style_options: Optional dict forwarded to the style builder.
        """
        kwargs.update(style_options=self._capture_style_options(['show_border'], kwargs))
        super().__init__(master, **kwargs)

    @configure_delegate('show_border')
    def _delegate_show_border(self, value=None):
        if value is not None:
            return self.configure_style_options('show_border')
        else:
            self.configure_style_options(show_border=True)
            return self.rebuild_style()

