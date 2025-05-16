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
    A themed labelframe widget with support for background color styling.

    This widget extends the standard `ttk.LabelFrame` by applying a
    background style based on the provided `color`. The style affects both
    the container background and the label text area, offering a consistent
    visual theme for grouped sections.

    This is useful for visually organizing related widgets under a labeled
    container with customizable styling.

    Example:
        LabelFrame(root, text="Settings", color="secondary", padding=10)

    Parameters:
        master (Misc | None): The parent container widget.
        color (Color): The background color theme (e.g., "secondary", "light").
        **kwargs (LabelFrameOpts): Additional options accepted by `ttk.LabelFrame`.
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
