from __future__ import annotations

from tkinter import ttk
from typing import Any, Literal, Optional, TypedDict
from typing_extensions import Unpack
from ._internal.wrapper_base import TTKWrapperBase


class EntryKwargs(TypedDict, total=False):
    # Standard ttk.Entry options
    textvariable: Any
    show: Any
    width: int
    exportselection: bool
    justify: Any
    validate: Any
    validatecommand: Any
    invalidcommand: Any
    xscrollcommand: Any
    font: Any
    foreground: str
    background: str
    state: Literal['normal', 'disabled', 'readonly'] | str
    takefocus: Any
    style: str
    class_: str
    cursor: str
    name: str

    # ttkbootstrap-specific extensions
    bootstyle: str
    surface_color: str
    style_options: dict[str, Any]


class Entry(TTKWrapperBase, ttk.Entry):
    """ttkbootstrap wrapper for `ttk.Entry` with bootstyle support."""

    _ttk_base = ttk.Entry

    def __init__(self, master=None, **kwargs: Unpack[EntryKwargs]) -> None:
        """Create a themed ttkbootstrap Entry.

        Keyword Args:
            textvariable: Tk variable linked to the entry text.
            show: Substitute character for masked input.
            width: Width in characters.
            exportselection: Whether selection is exported to X clipboard.
            justify: Text alignment inside the entry.
            validate: Validation mode.
            validatecommand: Validation callback.
            invalidcommand: Callback executed on validation failure.
            xscrollcommand: Horizontal scroll callback.
            font: Font for the entry text.
            foreground: Text color.
            background: Background color.
            state: Widget state.
            takefocus: Whether the widget participates in focus traversal.
            style: Explicit ttk style name (overrides bootstyle).
            bootstyle: ttkbootstrap style tokens (e.g., 'primary').
            surface_color: Optional surface token; otherwise inherited.
            style_options: Optional dict forwarded to the style builder.
        """
        super().__init__(master, **kwargs)

