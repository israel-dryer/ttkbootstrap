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
    """A themed slider widget with dynamic color styling.

    This widget extends the standard `ttk.Scale` and applies a themed style
    based on the provided `color`. The styling affects the slider thumb and
    trough to match the selected ttkbootstrap theme.

    Ideal for use cases where users must select a continuous numeric value
    (e.g., volume, brightness, thresholds) and where consistent visual theming
    is desired.

    Example:
        >>> from ttkbootstrap.widgets import Scale
        >>> s = Scale(root, from_=0, to=100, color="primary", orient="horizontal")
        >>> s.pack(fill="x")

    Args:
        master (Misc | None): The parent container widget.
        color (Color, optional): A ttkbootstrap color token (e.g., "primary", "warning").
        **kwargs (ScaleOpts): Additional keyword arguments accepted by `ttk.Scale`.
    """

    def __init__(
        self,
        master: Misc | None = None,
        color: Color = None,
        **kwargs: Unpack[ScaleOpts],
    ):
        """Initialize the themed Scale widget.

        Args:
            master (Misc | None): The parent container.
            color (Color, optional): The ttkbootstrap color style applied to the slider.
            **kwargs (ScaleOpts): Additional configuration options for `ttk.Scale`.
        """
        self._color = color
        self._variant = None  # Scale does not use variants
        super().__init__(master, **kwargs)
        self._init_style(kwargs, color=color, variant="")
