"""Backwards-compatibility shim for ttkbootstrap.dialogs.dialogs.

This module re-exports dialog classes and facades that are now organized
across submodules within `ttkbootstrap.dialogs`.
"""

from .base import Dialog
from .datepicker import DatePickerDialog
from .fontdialog import FontDialog
from .message import MessageDialog, Messagebox
from .query import QueryDialog, Querybox

__all__ = [
    "Dialog",
    "MessageDialog",
    "QueryDialog",
    "DatePickerDialog",
    "FontDialog",
    "Messagebox",
    "Querybox",
]
