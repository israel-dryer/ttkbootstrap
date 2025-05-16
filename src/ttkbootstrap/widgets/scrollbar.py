from tkinter import Misc
from tkinter.ttk import Scrollbar as ttkScrollbar

from ttkbootstrap.ttk_types import StyleColor as Color
from ttkbootstrap.ttk_types import ScrollbarOptions as ScrollOpts
from ttkbootstrap.styledwidget import StyledWidgetMixin

try:
    from typing import Unpack, Literal
except ImportError:
    from typing_extensions import Unpack, Literal


ScrollbarVariant = Literal["default", "round"]


class Scrollbar(StyledWidgetMixin, ttkScrollbar):
    """
    A themed scrollbar widget with support for color and variant styling.

    This widget extends the standard `ttk.Scrollbar` by applying custom styles
    based on the provided `color` and `variant`. The `color` affects the thumb
    and track appearance, while the `variant` determines the shape of the thumb.

    Supported variants:
        - "default": Standard rectangular thumb
        - "round": Rounded thumb design

    Useful for customizing scroll appearance to better match modern or
    stylistically themed interfaces.

    Example:
        Scrollbar(root, orient="vertical", color="primary", variant="round")

    Parameters:
        master (Misc | None): The parent container widget.
        color (Color): The scrollbar color theme (e.g., "primary", "secondary").
        variant (str): Either "default" or "round".
        **kwargs (ScrollbarOpts): Additional options accepted by `ttk.Scrollbar`.
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
