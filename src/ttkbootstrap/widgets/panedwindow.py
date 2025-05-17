from tkinter import Misc
from tkinter.ttk import PanedWindow as ttkPanedWindow

from ttkbootstrap.ttk_types import StyleColor as Color
from ttkbootstrap.ttk_types import PanedWindowOptions as PanedOpts
from ttkbootstrap.styledwidget import StyledWidgetMixin

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack


class PanedWindow(StyledWidgetMixin, ttkPanedWindow):
    """A themed paned window widget with background and sash color styling.

    This widget extends the standard `ttk.PanedWindow` by applying a themed
    background to the container and sash using the provided `color`. It allows
    you to create adjustable, resizable layouts with a visually consistent style.

    Typically used for split-pane layouts in editors, dashboards, and file explorers.

    Example:
        >>> from ttkbootstrap.widgets import PanedWindow
        >>> pw = PanedWindow(root, orient="horizontal", color="light")
        >>> pw.pack(fill="both", expand=True)

    Args:
        master (Misc | None): The parent container widget.
        color (Color): The background color theme (e.g., "light", "secondary").
        **kwargs (PanedOpts): Additional options accepted by `ttk.PanedWindow`.
    """

    def __init__(
        self,
        master: Misc | None = None,
        color: Color = "default",
        **kwargs: Unpack[PanedOpts],
    ):
        """Initialize a themed PanedWindow widget.

        Args:
            master (Misc | None): The parent container.
            color (Color): A ttkbootstrap color token (e.g., "light", "primary").
            **kwargs (PanedOpts): Additional configuration options passed to `ttk.PanedWindow`.
        """
        self._color = color
        self._variant = None  # No variant support
        super().__init__(master, **kwargs)
        self._init_style(kwargs, color=color, variant="")
