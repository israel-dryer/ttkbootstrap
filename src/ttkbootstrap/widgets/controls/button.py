from __future__ import annotations

from tkinter import ttk
from typing import Any, Callable, Literal, Optional, TypedDict
from typing_extensions import Unpack

from .._internal.wrapper_base import TTKWrapperBase
from ..mixins.icon_mixin import IconMixin


class ButtonKwargs(TypedDict, total=False):
    # Standard ttk.Button options
    text: Any
    command: Optional[Callable[[], Any]]
    image: Any
    icon: Any
    compound: Literal['text', 'image', 'top', 'bottom', 'left', 'right', 'center', 'none'] | str
    padding: Any
    width: int
    underline: int
    state: Literal['normal', 'active', 'disabled', 'readonly'] | str
    takefocus: Any
    style: str
    class_: str
    cursor: str
    default: Any
    name: str
    textvariable: Any

    # ttkbootstrap-specific extensions
    bootstyle: str
    surface_color: str
    style_options: dict[str, Any]


class Button(IconMixin, TTKWrapperBase, ttk.Button):
    """TTK Bootstrap Button

    ttkbootstrap wrapper for `ttk.Button` with bootstyle and icon support.
    """
    _ttk_base = ttk.Button

    def __init__(self, master=None, **kwargs: Unpack[ButtonKwargs]) -> None:
        """Create a themed ttkbootstrap Button.

        Keyword Args:
            text: Text to display on the button.
            command: Callable invoked when the button is pressed.
            image: Image to display on the button.
            icon: Optional icon spec integrated via the style system. Preferred
                over `image` for theme-aware iconography when supported.
            compound: Placement of the image relative to text (e.g., 'left').
            padding: Extra space around the button content.
            width: Width of the button in characters.
            underline: Index of the character to underline in `text`.
            state: Widget state (e.g., 'normal', 'disabled').
            takefocus: Whether the widget accepts focus during traversal.
            style: Explicit ttk style name to apply (overrides bootstyle).
            bootstyle: ttkbootstrap style tokens, e.g. 'primary', 'danger-outline'.
                Prefer this over `style` to participate in theme updates.
            surface_color: Optional surface token to use for this button; if not
                provided, the surface color is inherited from the parent.
            style_options: Optional dict forwarded to the style builder. Useful
                for widget-specific options (e.g., {'icon': ...}).
        """
        super().__init__(master, **kwargs)  # type: ignore[arg-type]


