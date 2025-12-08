from __future__ import annotations

from tkinter import ttk
from typing import Any, Literal, Optional, TypedDict, TYPE_CHECKING
from typing_extensions import Unpack
from ._internal.wrapper_base import TTKWrapperBase
from .mixins.icon_mixin import IconMixin
from .mixins import TextSignalMixin

if TYPE_CHECKING:
    from ttkbootstrap.core.signals import Signal


class MenubuttonKwargs(TypedDict, total=False):
    # Standard ttk.Menubutton options
    text: Any
    image: Any
    icon: Any
    icon_only: bool
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
    textsignal: Signal[Any]

    # ttkbootstrap-specific extensions
    bootstyle: str
    surface_color: str
    style_options: dict[str, Any]


class Menubutton(TextSignalMixin, IconMixin, TTKWrapperBase, ttk.Menubutton):
    """ttkbootstrap wrapper for `ttk.Menubutton` with bootstyle and icon support."""

    _ttk_base = ttk.Menubutton

    def __init__(self, master=None, **kwargs: Unpack[MenubuttonKwargs]) -> None:
        """Create a themed ttkbootstrap Menubutton.

        Keyword Args:
            text: Text to display in the menubutton.
            image: Image to display.
            icon: Theme-aware icon spec handled by the style system.
            icon_only: If True, removes the additional padding reserved for label text.
            compound: Placement of the image relative to text.
            direction: Direction for the menu to appear.
            menu: Associated tk.Menu instance.
            padding: Extra space around the content.
            state: Widget state.
            takefocus: Whether the widget participates in focus traversal.
            textvariable: Tk variable linked to the text.
            textsignal: Reactive Signal linked to the text (auto-synced with textvariable).
            style: Explicit ttk style name (overrides bootstyle).
            bootstyle: ttkbootstrap style tokens (e.g., 'primary', 'ghost').
            surface_color: Optional surface token; otherwise inherited.
            style_options: Optional dict forwarded to the style builder.
        """
        kwargs.update(style_options=self._capture_style_options(['icon_only', 'icon'], kwargs))
        super().__init__(master, **kwargs)

        # Ensure the menubutton receives focus when clicked so focus styling is visible.
        self.bind("<Button-1>", lambda _: self.focus_set(), add="+")

