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
    A themed Treeview widget for displaying tabular or hierarchical data.

    This widget extends the standard `ttk.Treeview` with dynamic theming
    support using the `color` parameter. The color affects the row selection
    and header styling, making it ideal for use in structured views like
    file explorers, data tables, or nested trees.

    Example:
        >>> from ttkbootstrap import Window
        >>> from ttkbootstrap.widgets import Treeview
        >>> tv = Treeview(root, columns=["Name", "Age"], show="headings", color="info")
        >>> tv.heading("Name", text="Name")
        >>> tv.heading("Age", text="Age")
        >>> tv.insert("", "end", values=["Alice", 30])
        >>> tv.pack(fill="both", expand=True)

    Parameters:
        master (Misc | None): The parent container widget.
        color (Color, optional): The highlight color theme (e.g., "info", "primary").
        **kwargs (TreeOpts): Additional options accepted by `ttk.Treeview`.
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
