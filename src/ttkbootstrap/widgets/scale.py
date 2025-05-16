from tkinter import Misc
from tkinter.ttk import Scale as ttkScale

from ttkbootstrap.typing import StyleColor as Color
from ttkbootstrap.typing import ScaleOptions as ScaleOpts
from ttkbootstrap.styledwidget import StyledWidgetMixin

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack


class Scale(StyledWidgetMixin, ttkScale):
    """
    A styled ttkbootstrap-compatible Scale widget that supports a `color`
    parameter for dynamic style generation.

    This widget allows users to select a numerical value by dragging a slider.

    Example:
        Scale(root, from_=0, to=100, color="primary", orient="horizontal")
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
