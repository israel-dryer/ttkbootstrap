from __future__ import annotations

from tkinter import ttk
from typing import Any, Literal, TypedDict
from typing_extensions import Unpack
from ._internal.wrapper_base import TTKWrapperBase


class TreeviewKwargs(TypedDict, total=False):
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


class Treeview(TTKWrapperBase, ttk.Treeview):
    """ttkbootstrap wrapper for `ttk.Treeview` with bootstyle support."""

    _ttk_base = ttk.Treeview

    def __init__(self, master=None, **kwargs: Unpack[TreeviewKwargs]) -> None:
        """Create a themed ttkbootstrap Treeview.

        Keyword Args:
            columns: Sequence of column identifiers.
            displaycolumns: Subset and order of columns to display.
            show: Which parts to display (e.g., 'tree', 'headings').
            height: Number of rows to display.
            padding: Extra padding around the widget.
            selectmode: Selection mode.
            style: Explicit ttk style name (overrides bootstyle).
            bootstyle: ttkbootstrap style tokens.
            surface_color: Optional surface token; otherwise inherited.
            style_options: Optional dict forwarded to the style builder.
        """
        super().__init__(master, **kwargs)

