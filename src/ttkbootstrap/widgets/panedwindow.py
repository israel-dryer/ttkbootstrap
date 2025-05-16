from tkinter import Misc
from tkinter.ttk import PanedWindow as ttkPanedWindow

from ttkbootstrap.typing import StyleColor as Color
from ttkbootstrap.typing import PanedWindowOptions as PanedOpts
from ttkbootstrap.styledwidget import StyledWidgetMixin

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack


class PanedWindow(StyledWidgetMixin, ttkPanedWindow):
    """
    A themed paned window widget with support for sash and background color styling.

    This widget extends the standard `ttk.PanedWindow` by applying a background
    style to both the container and the sash using the provided `color`. It allows
    you to divide the layout into resizable panes with a consistent themed appearance.

    Ideal for building adjustable layouts where visual styling is desired for
    the sash and background regions.

    Example:
        PanedWindow(root, orient="horizontal", color="light")

    Parameters:
        master (Misc | None): The parent container widget.
        color (Color): The background color theme (e.g., "light", "secondary").
        **kwargs (PanedWindowOpts): Additional options accepted by `ttk.PanedWindow`.
    """

    def __init__(
        self,
        master: Misc | None = None,
        color: Color = "default",
        **kwargs: Unpack[PanedOpts],
    ):
        """
        Initialize a styled PanedWindow.

        Parameters:
            master (Misc | None): The parent container.
            color (Color): A ttkbootstrap color token (e.g., "light", "primary").
            **kwargs (PanedOpts): Additional standard ttk.PanedWindow options.
        """
        self._color = color
        self._variant = None  # No variant support
        super().__init__(master, **kwargs)
        self._init_style(kwargs, color=color, variant="")
