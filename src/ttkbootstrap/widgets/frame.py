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
    """
    A themed frame widget with support for background color styling.

    This widget extends the standard `ttk.Frame` by applying a background
    style based on the provided `color`. It allows for consistent visual theming
    of container elements across your application. The `"default"` color uses
    the base theme's standard background color for frames.

    It behaves identically to `ttk.Frame`, supporting layout, nesting,
    and padding, while allowing for custom appearance through dynamic styling.

    Example:
        Frame(root, color="light", padding=10)

    Parameters:
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
