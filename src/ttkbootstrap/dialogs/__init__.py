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
from ttkbootstrap.dialogs.dialogs import *