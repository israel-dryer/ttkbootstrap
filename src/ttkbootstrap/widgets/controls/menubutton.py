from __future__ import annotations

from tkinter import ttk
from typing import Any, Literal, Optional, TypedDict
from typing_extensions import Unpack
from .._internal.wrapper_base import TTKWrapperBase
from ..mixins.icon_mixin import IconMixin


class MenubuttonKwargs(TypedDict, total=False):
    # Standard ttk.Menubutton options
    text: Any
    image: Any
    icon: Any
    compound: Literal['text','image','top','bottom','left','right','center','none'] | str
    direction: Any
    menu: Any
    padding: Any
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


class Menubutton(IconMixin, TTKWrapperBase, ttk.Menubutton):
    """ttkbootstrap wrapper for `ttk.Menubutton` with bootstyle and icon support."""

    _ttk_base = ttk.Menubutton

    def __init__(self, master=None, **kwargs: Unpack[MenubuttonKwargs]) -> None:
        """Create a themed ttkbootstrap Menubutton.

        Keyword Args:
            text: Text to display in the menubutton.
            image: Image to display.
            icon: Theme-aware icon spec handled by the style system.
            compound: Placement of the image relative to text.
            direction: Direction for the menu to appear.
            menu: Associated tk.Menu instance.
            padding: Extra space around the content.
            state: Widget state.
            takefocus: Whether the widget participates in focus traversal.
            style: Explicit ttk style name (overrides bootstyle).
            bootstyle: ttkbootstrap style tokens (e.g., 'primary', 'ghost').
            surface_color: Optional surface token; otherwise inherited.
            style_options: Optional dict forwarded to the style builder.
        """
        super().__init__(master, **kwargs)

