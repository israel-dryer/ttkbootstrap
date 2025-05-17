from tkinter import Misc
from tkinter.ttk import LabelFrame as ttkLabelFrame

from ttkbootstrap.ttk_types import StyleColor as Color
from ttkbootstrap.ttk_types import LabelFrameOptions as LabelFrameOpts
from ttkbootstrap.styledwidget import StyledWidgetMixin

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack


class LabelFrame(StyledWidgetMixin, ttkLabelFrame):
    """A themed labelframe widget with support for background color styling.

    This widget extends the standard `ttk.LabelFrame` by applying a themed
    background color using ttkbootstrap's style system. The color affects both
    the main frame and the label header area, allowing for consistent visual
    grouping of widgets under a labeled section.

    This is useful for organizing related widgets with a visually distinct header.

    Example:
        >>> from ttkbootstrap.widgets import LabelFrame
        >>> lf = LabelFrame(root, text="Settings", color="secondary", padding=10)
        >>> lf.pack(fill="both", expand=True)

    Args:
        master (Misc | None): The parent container widget.
        color (Color): The background color theme (e.g., "secondary", "primary", "light").
        **kwargs (LabelFrameOpts): Additional options accepted by `ttk.LabelFrame`.
    """

    def __init__(
        self,
        master: Misc | None = None,
        color: Color = "default",
        **kwargs: Unpack[LabelFrameOpts],
    ):
        """Initialize the themed LabelFrame widget.

        Args:
            master (Misc | None): The parent container.
            color (Color): A ttkbootstrap color token (e.g., "primary", "light", "default").
            **kwargs (LabelFrameOpts): Additional options passed to `ttk.LabelFrame`.
        """
        self._color = color
        self._variant = None  # No variant support
        super().__init__(master, **kwargs)
        self._init_style(kwargs, color=color, variant="")
