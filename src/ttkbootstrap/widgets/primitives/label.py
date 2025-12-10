from __future__ import annotations

from tkinter import ttk
from typing import Any, Literal, TypedDict, TYPE_CHECKING
from typing_extensions import Unpack
from ttkbootstrap.widgets._internal.wrapper_base import TTKWrapperBase
from ..mixins import IconMixin, TextSignalMixin
from ..mixins.localizable_mixin import LocalizableWidgetMixin

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
    bootstyle: str
    surface_color: str
    style_options: dict[str, Any]


class Label(LocalizableWidgetMixin, TextSignalMixin, IconMixin, TTKWrapperBase, ttk.Label):
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
            localize: If true, translates the text.
            padding: Extra space around the label content.
            width: Width of the label in characters.
            wraplength: Maximum width before wrapping text.
            font: Font for text.
            foreground: Text color.
            value_format: Format specification for the label value.
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

        # catch localization items.
        localize = kwargs.pop('localize', 'auto')
        value_format = kwargs.pop('value_format', None)
        text = kwargs.get('text')
        super().__init__(master, localize=localize, value_format=value_format, **kwargs)
        self.register_localized_field('text', text, value_format=value_format)
