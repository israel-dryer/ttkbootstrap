from tkinter import Misc
from tkinter.ttk import Frame as ttkFrame

from ttkbootstrap.typing import StyleColor as Color
from ttkbootstrap.typing import FrameOptions as FrameOpts
from ttkbootstrap.styledwidget import StyledWidgetMixin

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack


class Frame(StyledWidgetMixin, ttkFrame):
    """
    A styled ttkbootstrap-compatible Frame that supports a `color` parameter
    for background style theming.

    This widget wraps tkinter.ttk.Frame and applies ttkbootstrap styles
    dynamically. `color="default"` will apply the base container background.

    Example:
        Frame(root, color="light", padding=10)
    """

    def __init__(
        self,
        master: Misc | None = None,
        color: Color = "default",
        **kwargs: Unpack[FrameOpts],
    ):
        """
        Initialize a styled Frame.

        Parameters:
            master (Misc | None): The parent container.
            color (Color): A ttkbootstrap background color token (e.g., "light", "primary", "default").
            **kwargs (FrameOpts): Additional standard ttk.Frame options.
        """
        self._color = color
        self._variant = None  # Frame has no variant support
        super().__init__(master, **kwargs)
        self._init_style(kwargs, color=color, variant="")
