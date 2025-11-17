from __future__ import annotations

from tkinter import ttk
from typing import Any, Callable, Literal, Optional, TypedDict
from typing_extensions import Unpack
from .._internal.wrapper_base import TTKWrapperBase
from ..mixins.icon_mixin import IconMixin


class RadiobuttonKwargs(TypedDict, total=False):
    # Standard ttk.Radiobutton options
    text: Any
    command: Optional[Callable[[], Any]]
    image: Any
    icon: Any
    compound: Literal['text','image','top','bottom','left','right','center','none'] | str
    variable: Any
    value: Any
    padding: Any
    width: int
    underline: int
    state: Literal['normal','active','disabled','readonly'] | str
    takefocus: Any
    style: str
    class_: str
    cursor: str
    name: str
    textvariable: Any

    # ttkbootstrap-specific extensions
    bootstyle: str
    surface_color: str
    style_options: dict[str, Any]


class Radiobutton(IconMixin, TTKWrapperBase, ttk.Radiobutton):
    """ttkbootstrap wrapper for `ttk.Radiobutton` with bootstyle and icon support."""

    _ttk_base = ttk.Radiobutton

    def __init__(self, master=None, **kwargs: Unpack[RadiobuttonKwargs]) -> None:
        """Create a themed ttkbootstrap Radiobutton.

        Keyword Args:
            text: Text to display.
            command: Callable invoked when the value is selected.
            image: Image to display.
            icon: Theme-aware icon spec handled by the style system.
            compound: Placement of the image relative to text.
            variable: Linked tk variable that receives the selected value.
            value: The value assigned to `variable` when this radio is selected.
            padding: Extra space around the content.
            width: Width of the control in characters.
            underline: Index of character to underline in `text`.
            state: Widget state.
            takefocus: Whether the widget participates in focus traversal.
            style: Explicit ttk style name (overrides bootstyle).
            bootstyle: ttkbootstrap style tokens (e.g., 'primary', 'success').
            surface_color: Optional surface token; otherwise inherited.
            style_options: Optional dict forwarded to the style builder.
        """
        super().__init__(master, **kwargs)

