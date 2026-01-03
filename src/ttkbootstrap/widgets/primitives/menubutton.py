from __future__ import annotations

from tkinter import ttk
from typing import Any, Literal, TYPE_CHECKING, TypedDict

from typing_extensions import Unpack

from ttkbootstrap.core.mixins.ttk_state import TtkStateMixin
from ttkbootstrap.core.mixins.widget import WidgetCapabilitiesMixin
from ttkbootstrap.widgets.internal.wrapper_base import TTKWrapperBase
from ttkbootstrap.widgets.mixins import IconMixin, LocalizationMixin, TextSignalMixin
from ttkbootstrap.widgets.types import Master

if TYPE_CHECKING:
    from ttkbootstrap.core.signals import Signal


class MenuButtonKwargs(TypedDict, total=False):
    # Standard ttk.Menubutton options
    text: Any
    image: Any
    icon: Any
    icon_only: bool
    compound: Literal['text', 'image', 'top', 'bottom', 'left', 'right', 'center', 'none'] | str
    direction: Any
    menu: Any
    padding: Any
    state: Literal['normal', 'active', 'disabled', 'readonly'] | str
    takefocus: Any
    style: str
    class_: str
    cursor: str
    name: str
    textvariable: Any
    textsignal: Signal[Any]

    # ttkbootstrap-specific extensions
    bootstyle: str  # DEPRECATED: Use accent and variant instead
    accent: str
    variant: str
    surface_color: str
    style_options: dict[str, Any]
    localize: bool | Literal['auto']


class MenuButton(LocalizationMixin, TextSignalMixin, IconMixin, TTKWrapperBase, WidgetCapabilitiesMixin, TtkStateMixin, ttk.Menubutton):
    """ttkbootstrap wrapper for `ttk.Menubutton` with bootstyle and icon support."""

    _ttk_base = ttk.Menubutton

    def __init__(self, master: Master = None, **kwargs: Unpack[MenuButtonKwargs]) -> None:
        """Create a themed ttkbootstrap Menubutton.

        Args:
            master: Parent widget. If None, uses the default root window.

        Other Parameters:
            text (str): Text to display in the menubutton.
            image (PhotoImage): Image to display.
            icon (str | dict): Theme-aware icon spec handled by the style system.
            icon_only (bool): If True, removes the additional padding reserved for label text.
            compound (str): Placement of the image relative to text.
            direction (str): Direction for the menu to appear.
            menu (Menu): Associated tk.Menu instance.
            padding (int | tuple): Extra space around the content.
            state (str): Widget state.
            takefocus (bool): Whether the widget participates in focus traversal.
            textvariable (Variable): Tk variable linked to the text.
            textsignal (Signal): Reactive Signal linked to the text (auto-synced with textvariable).
            style (str): Explicit ttk style name (overrides accent/variant).
            accent (str): Accent token for styling, e.g. 'primary', 'danger', 'success'.
            variant (str): Style variant, e.g. 'solid', 'outline', 'ghost'.
            bootstyle (str): DEPRECATED - Use `accent` and `variant` instead.
                Combined style tokens (e.g., 'primary', 'ghost').
            surface_color (str): Optional surface token; otherwise inherited.
            style_options (dict): Optional dict forwarded to the style builder.
            localize (bool | Literal['auto']): Determines the widget's localization mode.
        """
        kwargs.update(style_options=self._capture_style_options(['icon_only', 'icon'], kwargs))
        super().__init__(master, **kwargs)

        # Ensure the menubutton receives focus when clicked so focus styling is visible.
        self.bind("<Button-1>", lambda _: self.focus_set(), add="+")
