from __future__ import annotations

from tkinter import ttk
from typing import Any, Callable, Literal, Optional, TypedDict, TYPE_CHECKING
from typing_extensions import Unpack

from ttkbootstrap.widgets._internal.wrapper_base import TTKWrapperBase
from ttkbootstrap.widgets.mixins import IconMixin, TextSignalMixin, LocalizationMixin
from ttkbootstrap.widgets.types import Master

if TYPE_CHECKING:
    from ttkbootstrap.core.signals import Signal


class ButtonKwargs(TypedDict, total=False):
    # Standard ttk.Button options
    text: Any
    command: Optional[Callable[[], Any]]
    image: Any
    icon: Any
    icon_only: bool
    compound: Literal['text', 'image', 'top', 'bottom', 'left', 'right', 'center', 'none'] | str
    padding: Any
    width: int
    underline: int
    state: Literal['normal', 'active', 'disabled', 'readonly'] | str
    takefocus: Any
    localize: bool | Literal['auto']
    value_format: dict | str
    style: str
    class_: str
    cursor: str
    default: Any
    name: str
    textvariable: Any
    textsignal: Signal[str]

    # ttkbootstrap-specific extensions
    bootstyle: str
    surface_color: str
    style_options: dict[str, Any]


class Button(LocalizationMixin, TextSignalMixin, IconMixin, TTKWrapperBase, ttk.Button):
    """TTK Bootstrap Button

    ttkbootstrap wrapper for `ttk.Button` with bootstyle and icon support.
    """
    _ttk_base = ttk.Button

    def __init__(self, master: Master = None, **kwargs: Unpack[ButtonKwargs]) -> None:
        """Create a themed ttkbootstrap Button.

        Args:
            master: Parent widget. If None, uses the default root window.

        Other Parameters:
            text (str): Text to display on the button.
            textvariable (Variable): Tk variable linked to the button text.
            textsignal (Signal[str]): Reactive Signal linked to the button text (auto-synced with textvariable).
            command (Callable): Callable invoked when the button is pressed.
            image (PhotoImage): Image to display on the button.
            icon (str | dict): Optional icon spec integrated via the style system. Preferred
                over `image` for theme-aware iconography when supported.
            icon_only (bool): If true, removes the extra padding reserved for the text labels.
            compound (str): Placement of the image relative to text (e.g., 'left').
            padding (int | tuple): Extra space around the button content.
            localize (bool | Literal['auto']): Determines the widgets localization mode.
            value_format (str | dict): Format specification for the label value.
            width (int): Width of the button in characters.
            underline (int): Index of the character to underline in `text`.
            state (str): Widget state (e.g., 'normal', 'disabled').
            takefocus (bool): Whether the widget accepts focus during traversal.
            style (str): Explicit ttk style name to apply (overrides bootstyle).
            bootstyle (str): ttkbootstrap style tokens, e.g. 'primary', 'danger-outline'.
                Prefer this over `style` to participate in theme updates.
            surface_color (str): Optional surface token to use for this button; if not
                provided, the surface color is inherited from the parent.
            style_options (dict): Optional dict forwarded to the style builder. Useful
                for widget-specific options (e.g., {'icon': ...}).
        """
        kwargs.update(style_options=self._capture_style_options(['icon_only', 'icon'], kwargs))
        super().__init__(master, **kwargs)
