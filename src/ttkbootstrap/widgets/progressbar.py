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
    """
    A themed progress bar widget with support for color and variant styling.

    This widget extends the standard `ttk.Progressbar` by applying dynamic styles
    based on the provided `color` and `variant` parameters. The `color` determines
    the fill color, while the `variant` controls the visual style of the bar.

    Supported variants:
        - "default": Solid fill style
        - "striped": Animated striped fill pattern (typically used with indeterminate mode)

    Suitable for both determinate and indeterminate progress displays, with
    customizable appearance to match themed applications.

    Example:
        Progressbar(root, length=200, color="success", variant="striped", mode="indeterminate")

    Parameters:
        master (Misc | None): The parent container widget.
        color (Color): The fill color theme (e.g., "success", "info").
        variant (str): Either "default" or "striped".
        **kwargs (ProgressbarOpts): Additional options accepted by `ttk.Progressbar`.
    """

    def __init__(
        self,
        master: Misc | None = None,
        color: Color = None,
        variant: ProgressbarVariant = "default",
        **kwargs: Unpack[PbarOpts],
    ):
        """
        Initialize a styled Progressbar.

        Parameters:
            master (Misc | None): The parent container.
            color (Color, optional): A ttkbootstrap color token (e.g., "info").
            variant (ProgressbarVariant): "default" or "striped".
            **kwargs (PbarOpts): Additional standard ttk.Progressbar options.
        """
        self._color = color
        self._variant = variant
        super().__init__(master, **kwargs)
        self._init_style(kwargs, color=color, variant=variant)
