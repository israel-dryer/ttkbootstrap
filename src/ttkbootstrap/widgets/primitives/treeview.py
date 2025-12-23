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
    show: Any
    height: int
    padding: Any
    selectmode: Literal['browse','extended','none'] | str
    style: str
    class_: str
    cursor: str
    name: str

    # ttkbootstrap-specific extensions
    bootstyle: str
    surface_color: str
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
            style (str): Explicit ttk style name (overrides bootstyle).
            bootstyle (str): ttkbootstrap style tokens.
            surface_color (str): Optional surface token; otherwise inherited.
            style_options (dict): Optional dict forwarded to the style builder.
        """
        super().__init__(master, **kwargs)


