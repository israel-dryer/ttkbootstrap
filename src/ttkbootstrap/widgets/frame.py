from tkinter import Misc
from tkinter.ttk import Frame as ttkFrame

from ttkbootstrap.ttk_types import StyleColor as Color
from ttkbootstrap.ttk_types import FrameOptions as FrameOpts
from ttkbootstrap.styledwidget import StyledWidgetMixin

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack


class Frame(StyledWidgetMixin, ttkFrame):
    """A themed frame widget with background color styling support.

    This widget extends the standard `ttk.Frame` and applies a background
    style based on the specified `color`. It allows for consistent visual theming
    of containers throughout your application.

    All layout, padding, and nesting behaviors of `ttk.Frame` are preserved.

    Example:
        >>> from ttkbootstrap.widgets import Frame
        >>> frame = Frame(root, color="light", padding=10)
        >>> frame.pack(fill="both", expand=True)

    Args:
        master (Misc | None): The parent container widget.
        color (Color): The background color theme (e.g., "light", "primary", "default").
        **kwargs (FrameOpts): Additional options accepted by `ttk.Frame`.
    """

    def __init__(
        self,
        master: Misc | None = None,
        color: Color = "default",
        **kwargs: Unpack[FrameOpts],
    ):
        """Initialize the themed Frame widget.

        This constructor configures the widget’s style based on the specified color
        and passes additional options to the base `ttk.Frame`.

        Args:
            master (Misc | None): The parent container.
            color (Color): A ttkbootstrap background color token (e.g., "light", "primary", "default").
            **kwargs (FrameOpts): Additional standard `ttk.Frame` options.
        """
        self._color = color
        self._variant = None  # Frame has no variant support
        super().__init__(master, **kwargs)
        self._init_style(kwargs, color=color, variant="")
