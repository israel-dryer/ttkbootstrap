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
    A styled ttkbootstrap-compatible PanedWindow that supports a `color`
    parameter for background styling of the sash and container.

    This widget allows you to split the interface into resizable panes.

    Example:
        PanedWindow(root, orient="horizontal", color="light")
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
