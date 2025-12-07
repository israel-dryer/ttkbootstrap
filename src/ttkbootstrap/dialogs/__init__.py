"""Dialog widgets for ttkbootstrap applications.

This package exposes Bootstrap-styled dialogs for common interactions:

- MessageBox/MessageDialog: info/warning/error/question prompts
- QueryBox/QueryDialog: collect input (string, number, date, item, color, font)
- ColorChooser/ColorChooserDialog: color picker with tabs and dropper
- ColorDropperDialog: pick a color from the screen with zoom preview
- DateDialog: calendar date picker
- FontDialog: font selection
- FilterDialog: multi-select filter dialog with search

Example:

    import ttkbootstrap as ttk
    from ttkbootstrap.dialogs import MessageBox, QueryBox

    root = ttk.Window()
    MessageBox.ok("Operation completed successfully!")
    answer = MessageBox.yesno("Do you want to continue?")
    name = QueryBox.get_string("Enter your name:")
    root.mainloop()
"""
from .colorchooser import (
    ColorChooser,
    ColorChooserDialog,
)
from .colordropper import (
    ColorDropperDialog,
)
from .dialog import Dialog, DialogButton
from .filterdialog import FilterDialog
from .formdialog import FormDialog
from .message import MessageDialog, MessageBox
from .query import QueryDialog, QueryBox
from .datedialog import DateDialog
from .fontdialog import FontDialog

__all__ = [
    # Base / core dialogs
    "Dialog",
    "DialogButton",
    "FilterDialog",
    "FormDialog",
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
