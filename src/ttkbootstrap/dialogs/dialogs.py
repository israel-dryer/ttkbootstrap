"""Backwards-compatibility shim for `ttkbootstrap.dialogs.dialogs`.

Deprecated: import from `ttkbootstrap.dialogs` (package) or specific
submodules instead, e.g. `ttkbootstrap.dialogs.message`.
"""
import warnings

warnings.warn(
    "ttkbootstrap.dialogs.dialogs is deprecated; import from ttkbootstrap.dialogs or specific submodules",
    DeprecationWarning,
    stacklevel=2,
)

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
