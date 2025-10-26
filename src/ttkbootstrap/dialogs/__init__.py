"""Dialog widgets for ttkbootstrap applications.

This module provides Bootstrap-styled dialog windows for common user interactions
like messages, questions, file selection, and color picking.

Dialogs:
    - Messagebox: Display informational messages (info, warning, error, question)
    - Querybox: Get user input (text, integer, float, selection)
    - Colorchooser: Select colors using various methods
    - FontDialog: Select and configure fonts

All dialogs support Bootstrap styling and theming.

Example:
    ```python
    import ttkbootstrap as ttk
    from ttkbootstrap.dialogs import Messagebox, Querybox

    root = ttk.Window()

    # Show message
    Messagebox.ok("Operation completed successfully!")

    # Ask question
    result = Messagebox.yesno("Do you want to continue?")

    # Get user input
    name = Querybox.get_string("Enter your name:")

    root.mainloop()
    ```
"""
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
