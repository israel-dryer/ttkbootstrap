from tkinter import Misc
from tkinter.ttk import Notebook as ttkNotebook

from ttkbootstrap.typing import StyleColor as Color
from ttkbootstrap.typing import NotebookOptions as NotebookOpts
from ttkbootstrap.styledwidget import StyledWidgetMixin

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack


class Notebook(StyledWidgetMixin, ttkNotebook):
    """
    A styled ttkbootstrap-compatible Notebook that supports a `color` parameter
    for applying dynamic themed tab styling.

    Example:
        Notebook(root, color="primary")
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
