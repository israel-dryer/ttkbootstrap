"""
ttkbootstrap.dialogs
=====================

A convenience module for importing and accessing all built-in dialog classes
in `ttkbootstrap`. This includes standard dialogs such as message boxes,
query dialogs, color pickers, font pickers, and more.

This module also provides backwards-compatible aliases for earlier versions
of ttkbootstrap, making it easier to upgrade without changing legacy code.

Usage Examples:
---------------

    from ttkbootstrap.dialogs import Messagebox, ColorChooserDialog

    # Show a message dialog
    result = Messagebox.show_info("Operation completed successfully.")

    # Show a color chooser
    color = ColorChooserDialog().show()

Available Dialogs:
------------------

- Dialog               : Base class for custom dialogs
- ColorDropperDialog   : Dropper tool for selecting a color from the screen
- ColorPickerDialog    : Modal dialog for picking a color
- ColorPicker          : Color picker widget (used internally in the dialog)
- DatePickerDialog     : Modal dialog for selecting a date
- FontPickerDialog     : Modal dialog for selecting font families and sizes
- QueryDialog          : Modal dialog for asking the user a question
- Querybox             : Function interface to QueryDialog
- MessageDialog        : Base class for message-style dialogs
- Messagebox           : Function interface to MessageDialog

Backwards-Compatible Aliases:
-----------------------------

- DateChooserDialog    → DatePickerDialog
- ColorChooserDialog   → ColorPickerDialog
- ColorChooser         → ColorPicker
- FontDialog           → FontPickerDialog
"""

from ttkbootstrap.dialogs.dialog import Dialog
from ttkbootstrap.dialogs.colordropper import ColorDropperDialog
from ttkbootstrap.dialogs.colorpicker import ColorPickerDialog, ColorPicker
from ttkbootstrap.dialogs.datepicker import DatePickerDialog
from ttkbootstrap.dialogs.fontpicker import FontPickerDialog
from ttkbootstrap.dialogs.query import QueryDialog, Querybox
from ttkbootstrap.dialogs.message import MessageDialog, Messagebox

# backwards-compatible alias
DateChooserDialog = DatePickerDialog
ColorChooserDialog = ColorPickerDialog
ColorChooser = ColorPicker
FontDialog = FontPickerDialog
