from tkinter import Misc
from tkinter.ttk import Scrollbar as ttkScrollbar

from ttkbootstrap.typing import StyleColor as Color
from ttkbootstrap.typing import ScrollbarOptions as ScrollOpts
from ttkbootstrap.styledwidget import StyledWidgetMixin

try:
    from typing import Unpack, Literal
except ImportError:
    from typing_extensions import Unpack, Literal


ScrollbarVariant = Literal["default", "round"]


class Scrollbar(StyledWidgetMixin, ttkScrollbar):
    """
    A styled ttkbootstrap-compatible Scrollbar that supports `color` and
    `variant` options for customizing appearance.

    Variants:
        - "default": rectangular thumb
        - "round": circular/thumbed design

    Example:
        Scrollbar(root, orient="vertical", color="primary", variant="round")
    """

    def __init__(
        self,
        master: Misc | None = None,
        color: Color = None,
        variant: ScrollbarVariant = "default",
        **kwargs: Unpack[ScrollOpts],
    ):
        """
        Initialize a styled Scrollbar.

        Parameters:
            master (Misc | None): The parent container.
            color (Color, optional): A ttkbootstrap color token.
            variant (ScrollbarVariant): Scrollbar style variant.
            **kwargs (ScrollOpts): Additional ttk.Scrollbar options.
        """
        self._color = color
        self._variant = variant
        super().__init__(master, **kwargs)
        self._init_style(kwargs, color=color, variant=variant)
