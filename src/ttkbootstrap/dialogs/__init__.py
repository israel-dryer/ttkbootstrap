"""Dialog widgets for ttkbootstrap: message boxes, input queries, date picking, color selection, and font selection."""
from .colorchooser import (
    ColorChooser,
    ColorChooserDialog,
)
from .colordropper import (
    ColorDropperDialog,
)
from .base import Dialog
from .message import MessageDialog, Messagebox
from .query import QueryDialog, Querybox
from .datepicker import DatePickerDialog
from .fontdialog import FontDialog

__all__ = [
    # Base / core dialogs
    "Dialog",
    "MessageDialog",
    "QueryDialog",
    "DatePickerDialog",
    "FontDialog",
    # Facades
    "Messagebox",
    "Querybox",
    # Color tools
    "ColorChooser",
    "ColorChooserDialog",
    "ColorDropperDialog",
]
