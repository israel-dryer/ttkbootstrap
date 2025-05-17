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
    """A themed scrollbar widget with color and variant styling.

    This widget extends `ttk.Scrollbar` and applies ttkbootstrap styling
    via the `color` and `variant` options. The `color` defines the scrollbar's
    visual theme, while the `variant` controls the thumb's shape.

    Supported variants:
        - "default": Rectangular thumb
        - "round": Rounded thumb ends

    Ideal for interfaces where scroll aesthetics should match a modern or
    visually cohesive theme.

    Example:
        >>> from ttkbootstrap.widgets import Scrollbar
        >>> sb = Scrollbar(root, orient="vertical", color="primary", variant="round")
        >>> sb.pack(side="right", fill="y")

    Args:
        master (Misc | None): The parent container widget.
        color (Color): The scrollbar color theme (e.g., "primary", "secondary").
        variant (ScrollbarVariant): Scrollbar thumb shape: "default" or "round".
        **kwargs (ScrollOpts): Additional keyword options passed to `ttk.Scrollbar`.
    """

    def __init__(
        self,
        master: Misc | None = None,
        color: Color = None,
        variant: ScrollbarVariant = "default",
        **kwargs: Unpack[ScrollOpts],
    ):
        """Initialize the themed Scrollbar widget.

        Args:
            master (Misc | None): The parent container.
            color (Color, optional): A ttkbootstrap color token (e.g., "info", "warning").
            variant (ScrollbarVariant): Thumb variant: "default" or "round".
            **kwargs (ScrollOpts): Additional configuration options passed to `ttk.Scrollbar`.
        """
        self._color = color
        self._variant = variant
        super().__init__(master, **kwargs)
        self._init_style(kwargs, color=color, variant=variant)
