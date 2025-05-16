from tkinter import Misc
from tkinter.ttk import Treeview as ttkTreeview

from ttkbootstrap.ttk_types import StyleColor as Color
from ttkbootstrap.ttk_types import TreeviewOptions as TreeOpts
from ttkbootstrap.styledwidget import StyledWidgetMixin

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack


class Treeview(StyledWidgetMixin, ttkTreeview):
    """
    A themed Treeview widget for displaying tabular data or hierarchical trees
    with optional columns, headings, and row selection.

    Supports theming through a `color` parameter to visually differentiate
    header and row highlights.

    Example:
        Treeview(root, columns=["Name", "Age"], show="headings", color="info")
    """

    def __init__(
        self,
        master: Misc | None = None,
        color: Color = None,
        **kwargs: Unpack[TreeOpts],
    ):
        """
        Initialize a themed Treeview.

        Parameters:
            master (Misc | None): The parent container.
            color (Color, optional): A ttkbootstrap color token.
            **kwargs (TreeOpts): Additional standard ttk.Treeview options.
        """
        self._color = color
        self._variant = None  # Treeview does not use variants
        super().__init__(master, **kwargs)
        self._init_style(kwargs, color=color, variant="")
