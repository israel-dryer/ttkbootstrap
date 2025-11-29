"""Dialog widgets for ttkbootstrap applications.

This module provides Bootstrap-styled dialog windows for common user interactions
like messages, questions, file selection, and color picking.

Dialogs:
    - Messagebox: Display informational messages (info, warning, error, question)
    - Querybox: Get user input (text, integer, float, selection)
    - Colorchooser: Select colors using various methods
    - DateDialog: Select dates using a calendar
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
from .dialog import Dialog, DialogButton
from .message import MessageDialog, MessageBox
from .query import QueryDialog, QueryBox
from .date import DateDialog
from .fontdialog import FontDialog

__all__ = [
    # Base / core dialogs
    "Dialog",
    "DialogButton",
    "MessageDialog",
    "QueryDialog",
    "DateDialog",
    "FontDialog",
    # Facades
    "MessageBox",
    "QueryBox",
    # Color tools
    "ColorChooser",
    "ColorChooserDialog",
    "ColorDropperDialog",
]
