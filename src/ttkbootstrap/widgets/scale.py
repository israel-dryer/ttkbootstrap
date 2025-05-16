from tkinter import Misc
from tkinter.ttk import Scale as ttkScale

from ttkbootstrap.ttk_types import StyleColor as Color
from ttkbootstrap.ttk_types import ScaleOptions as ScaleOpts
from ttkbootstrap.styledwidget import StyledWidgetMixin

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack


class Scale(StyledWidgetMixin, ttkScale):
    """
    A themed scale (slider) widget with support for dynamic color styling.

    This widget extends the standard `ttk.Scale` by applying a style based on
    the provided `color`. The color affects the slider trough and thumb,
    allowing for visual consistency with the application’s theme.

    The scale enables users to select a numerical value within a defined range
    by dragging a slider horizontally or vertically.

    Example:
        Scale(root, from_=0, to=100, color="primary", orient="horizontal")

    Parameters:
        master (Misc | None): The parent container widget.
        color (Color): The slider color theme (e.g., "primary", "warning").
        **kwargs (ScaleOpts): Additional options accepted by `ttk.Scale`.
    """

    def __init__(
        self,
        master: Misc | None = None,
        color: Color = None,
        **kwargs: Unpack[ScaleOpts],
    ):
        """
        Initialize a styled Scale widget.

        Parameters:
            master (Misc | None): The parent container.
            color (Color, optional): A ttkbootstrap color token (e.g., "primary").
            **kwargs (ScaleOpts): Additional standard ttk.Scale options.
        """
        self._color = color
        self._variant = None  # Scale does not use variants
        super().__init__(master, **kwargs)
        self._init_style(kwargs, color=color, variant="")
