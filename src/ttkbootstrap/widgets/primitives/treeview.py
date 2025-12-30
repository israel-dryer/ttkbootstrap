from __future__ import annotations

from tkinter import ttk
from typing import Any, Literal, TypedDict
from typing_extensions import Unpack

from ttkbootstrap.core.mixins.ttk_state import TtkStateMixin
from ttkbootstrap.core.mixins.widget import WidgetCapabilitiesMixin
from ttkbootstrap.widgets.internal.wrapper_base import TTKWrapperBase
from ttkbootstrap.widgets.types import Master


class TreeViewKwargs(TypedDict, total=False):
    # Standard ttk.Treeview options
    columns: Any
    displaycolumns: Any
    show: Literal['tree', 'headings', '']
    height: int
    padding: Any
    selectmode: Literal['browse','extended','none'] | str
    style: str
    class_: str
    cursor: str
    name: str

    # ttkbootstrap-specific extensions
    surface_color: str
    border_color: str
    show_border: bool
    select_background: str
    header_background: str
    style_options: dict[str, Any]


class TreeView(TTKWrapperBase, WidgetCapabilitiesMixin, TtkStateMixin, ttk.Treeview):
    """ttkbootstrap wrapper for `ttk.Treeview` with bootstyle support."""

    _ttk_base = ttk.Treeview

    def __init__(self, master: Master = None, **kwargs: Unpack[TreeViewKwargs]) -> None:
        """Create a themed ttkbootstrap Treeview.

        Args:
            master: Parent widget. If None, uses the default root window.

        Other Parameters:
            columns (list): Sequence of column identifiers.
            displaycolumns (list | str): Subset and order of columns to display.
            show (str): Which parts to display (e.g., 'tree', 'headings').
            height (int): Number of rows to display.
            padding (int | tuple): Extra padding around the widget.
            selectmode (str): Selection mode ('browse', 'extended', 'none').
            style (str): Explicit ttk style name.
            surface_color (str): Optional surface token; otherwise inherited.
            border_color (str): The color of the border around the table.
            show_border (bool): Whether to show a border around the table.
            open_icon (str | dict): The icon used for open state.
            close_icon (str | dict): The icon used for close state.
            select_background (str): A semantic color token used to set selection background color.
            header_background (str): A semantic color token used to set the header background color.
            style_options (dict): Optional dict forwarded to the style builder.
        """
        kwargs.update(style_options=self._capture_style_options([
            'border_color',
            'show_border',
            'open_icon',
            'close_icon',
            'select_background',
            'header_background'
        ],
            kwargs))
        super().__init__(master, **kwargs)


