from __future__ import annotations

from tkinter import ttk
from typing import Any, Literal, Optional, TypedDict
from typing_extensions import Unpack
from .._internal.wrapper_base import TTKWrapperBase


class ComboboxKwargs(TypedDict, total=False):
    # Standard ttk.Combobox options
    values: Any
    textvariable: Any
    state: Literal['normal', 'readonly', 'disabled'] | str
    width: int
    height: int
    postcommand: Any
    justify: Any
    exportselection: bool
    xscrollcommand: Any
    font: Any
    foreground: str
    background: str
    style: str
    class_: str
    cursor: str
    name: str

    # ttkbootstrap-specific extensions
    bootstyle: str
    surface_color: str
    style_options: dict[str, Any]


class Combobox(TTKWrapperBase, ttk.Combobox):
    """ttkbootstrap wrapper for `ttk.Combobox` with bootstyle support."""

    _ttk_base = ttk.Combobox

    def __init__(self, master=None, **kwargs: Unpack[ComboboxKwargs]) -> None:
        """Create a themed ttkbootstrap Combobox.

        Keyword Args:
            values: Sequence of values to display.
            textvariable: Tk variable linked to the selected value.
            state: Widget state; 'readonly' restricts to list items.
            width: Width in characters.
            height: Maximum rows shown in the drop-down list.
            postcommand: Callback executed before showing the drop-down.
            justify: Text justification within the entry field.
            exportselection: Whether selection is exported to X clipboard.
            xscrollcommand: Scroll callback for horizontal scrolling.
            font: Font for the entry field.
            foreground: Text color.
            background: Background color for the entry field.
            style: Explicit ttk style name (overrides bootstyle).
            bootstyle: ttkbootstrap style tokens (e.g., 'primary').
            surface_color: Optional surface token; otherwise inherited.
            style_options: Optional dict forwarded to the style builder.
        """
        super().__init__(master, **kwargs)

