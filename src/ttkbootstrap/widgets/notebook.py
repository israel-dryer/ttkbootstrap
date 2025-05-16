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
    """
     A themed notebook widget with support for tab color styling.

     This widget extends the standard `ttk.Notebook` by applying a dynamic style
     based on the provided `color` parameter. The color affects the tab background,
     active state, and indicator to create a cohesive visual theme across tabs.

     Useful for multi-tabbed interfaces where visual emphasis or categorization
     is desired through color differentiation.

     Example:
         Notebook(root, color="primary")

     Parameters:
         master (Misc | None): The parent container widget.
         color (Color): The tab color theme (e.g., "primary", "info").
         **kwargs (NotebookOpts): Additional options accepted by `ttk.Notebook`.
     """

    def __init__(
        self,
        master: Misc | None = None,
        color: Color = "default",
        **kwargs: Unpack[NotebookOpts],
    ):
        """
        Initialize a styled Notebook.

        Parameters:
            master (Misc | None): The parent container.
            color (Color): A ttkbootstrap color token (e.g., "primary", "default").
            **kwargs (NotebookOpts): Additional standard ttk.Notebook options.
        """
        self._color = color
        self._variant = None  # Notebook does not support variants
        super().__init__(master, **kwargs)
        self._init_style(kwargs, color=color, variant="")
