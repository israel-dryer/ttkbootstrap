from tkinter import Misc
from tkinter.ttk import Progressbar as ttkProgressbar

from ttkbootstrap.ttk_types import StyleColor as Color
from ttkbootstrap.ttk_types import ProgressbarOptions as PbarOpts
from ttkbootstrap.styledwidget import StyledWidgetMixin

try:
    from typing import Unpack, Literal
except ImportError:
    from typing_extensions import Unpack, Literal

ProgressbarVariant = Literal["default", "striped"]


class Progressbar(StyledWidgetMixin, ttkProgressbar):
    """A themed progress bar with support for color and fill variants.

    This widget extends the standard `ttk.Progressbar` with ttkbootstrap theme
    support, allowing you to customize the bar's appearance using the `color`
    and `variant` parameters.

    Use `mode="determinate"` for measurable progress and `mode="indeterminate"`
    for animated activity indicators.

    Supported variants:
        - "default": Solid fill style
        - "striped": Animated striped fill (commonly used for indeterminate mode)

    Example:
        >>> from ttkbootstrap.widgets import Progressbar
        >>> pb = Progressbar(root, length=200, color="success", variant="striped", mode="indeterminate")
        >>> pb.pack()
        >>> pb.start()

    Args:
        master (Misc | None): The parent container widget.
        color (Color): The fill color theme (e.g., "success", "info").
        variant (ProgressbarVariant): Fill style: "default" or "striped".
        **kwargs (ProgressbarOpts): Additional options accepted by `ttk.Progressbar`.
    """

    def __init__(
        self,
        master: Misc | None = None,
        color: Color = None,
        variant: ProgressbarVariant = "default",
        **kwargs: Unpack[PbarOpts],
    ):
        """Initialize the themed Progressbar widget.

        Args:
            master (Misc | None): The parent container.
            color (Color, optional): A ttkbootstrap color token (e.g., "info", "warning").
            variant (ProgressbarVariant): Either "default" or "striped".
            **kwargs (ProgressbarOpts): Additional keyword arguments for `ttk.Progressbar`.
        """
        self._color = color
        self._variant = variant
        super().__init__(master, **kwargs)
        self._init_style(kwargs, color=color, variant=variant)
