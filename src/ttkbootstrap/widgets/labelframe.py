from tkinter import Misc
from tkinter.ttk import LabelFrame as ttkLabelFrame

from ttkbootstrap.typing import StyleColor as Color
from ttkbootstrap.typing import LabelFrameOptions as LabelFrameOpts
from ttkbootstrap.styledwidget import StyledWidgetMixin

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack


class LabelFrame(StyledWidgetMixin, ttkLabelFrame):
    """
    A styled ttkbootstrap-compatible LabelFrame that supports a `color`
    parameter for themed background styling of the container and label.

    Example:
        LabelFrame(root, text="Section", color="secondary", padding=10)
    """

    def __init__(
        self,
        master: Misc | None = None,
        color: Color = "default",
        **kwargs: Unpack[LabelFrameOpts],
    ):
        """
        Initialize a styled LabelFrame.

        Parameters:
            master (Misc | None): The parent container.
            color (Color): A ttkbootstrap color token (e.g., "primary", "default").
            **kwargs (LabelFrameOpts): Additional standard ttk.LabelFrame options.
        """
        self._color = color
        self._variant = None  # No variant support
        super().__init__(master, **kwargs)
        self._init_style(kwargs, color=color, variant="")
