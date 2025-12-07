from __future__ import annotations

from tkinter import ttk
from typing import Any, Literal, TypedDict, TYPE_CHECKING
from typing_extensions import Unpack
from ._internal.wrapper_base import TTKWrapperBase
from .mixins import IconMixin, TextSignalMixin

if TYPE_CHECKING:
    from ttkbootstrap.signals import Signal


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
    state: Literal['normal', 'active', 'disabled', 'readonly'] | str
    takefocus: Any
    style: str
    class_: str
    cursor: str
    name: str
    textvariable: Any
    textsignal: Signal[str]

    # ttkbootstrap-specific extensions
    bootstyle: str
    surface_color: str
    style_options: dict[str, Any]


class Label(TextSignalMixin, IconMixin, TTKWrapperBase, ttk.Label):
    """ttkbootstrap wrapper for `ttk.Label` with bootstyle and icon support."""

    _ttk_base = ttk.Label

    def __init__(self, master=None, **kwargs: Unpack[LabelKwargs]) -> None:
        """Create a themed ttkbootstrap Label.

        Keyword Args:
            text: Text to display in the label.
            textvariable: Tk variable linked to the label text.
            textsignal: Reactive Signal linked to the label text (auto-synced with textvariable).
            image: Image to display.
            icon: Theme-aware icon spec handled by the style system.
            icon_only: If True, removes the additional padding reserved for label text.
            compound: Placement of the image relative to text.
            anchor: Alignment of the label's content within its area.
            justify: How to justify multiple lines of text.
            padding: Extra space around the label content.
            width: Width of the label in characters.
            wraplength: Maximum width before wrapping text.
            font: Font for text.
            foreground: Text color.
            background: Background color.
            relief: Border style.
            state: Widget state.
            takefocus: Whether the widget participates in focus traversal.
            style: Explicit ttk style name (overrides bootstyle).
            bootstyle: ttkbootstrap style tokens (e.g., 'secondary', 'info').
            surface_color: Optional surface token; otherwise inherited.
            style_options: Optional dict forwarded to the style builder.
        """
        kwargs.update(style_options=self._capture_style_options(['icon_only', 'icon'], kwargs))
        super().__init__(master, **kwargs)
