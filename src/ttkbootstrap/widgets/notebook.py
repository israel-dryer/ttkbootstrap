from tkinter import Misc
from tkinter.ttk import Notebook as ttkNotebook

from ttkbootstrap.ttk_types import StyleColor as Color
from ttkbootstrap.ttk_types import NotebookOptions as NotebookOpts
from ttkbootstrap.styledwidget import StyledWidgetMixin

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack


class Notebook(StyledWidgetMixin, ttkNotebook):
    """A themed notebook widget with support for tab color styling.

    This widget extends the standard `ttk.Notebook` and applies a
    ttkbootstrap-compatible style based on the specified `color`.
    The tab color affects the background, indicator, and selected state,
    making it easier to visually differentiate groups of tabs or indicate
    importance.

    Commonly used in multi-tabbed interfaces such as forms, dashboards,
    and configuration panels.

    Example:
        >>> from ttkbootstrap.widgets import Notebook
        >>> nb = Notebook(root, color="primary")
        >>> nb.pack(fill="both", expand=True)
        >>> frame1 = ttk.Frame(nb)
        >>> frame2 = ttk.Frame(nb)
        >>> nb.add(frame1, text="Tab 1")
        >>> nb.add(frame2, text="Tab 2")

    Args:
        master (Misc | None): The parent container widget.
        color (Color): The tab color theme (e.g., "primary", "info", "default").
        **kwargs (NotebookOpts): Additional options accepted by `ttk.Notebook`.
    """

    def __init__(
        self,
        master: Misc | None = None,
        color: Color = "default",
        **kwargs: Unpack[NotebookOpts],
    ):
        """Initialize a themed Notebook widget.

        Args:
            master (Misc | None): The parent container.
            color (Color): A ttkbootstrap color token (e.g., "primary", "default").
            **kwargs (NotebookOpts): Additional standard `ttk.Notebook` options.
        """
        self._color = color
        self._variant = None  # Notebook does not support variants
        super().__init__(master, **kwargs)
        self._init_style(kwargs, color=color, variant="")
