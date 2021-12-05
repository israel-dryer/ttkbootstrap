"""
    This module contains helper functions that show popups with a
    message to the end user with various arrangments of buttons
    and alert options.
"""

from ttkbootstrap.dialogs import MessageDialog


def ok(message, title=None, alert=False, parent=None):
    """Display a modal dialog box with an OK button and and optional
    bell alert. 

    Parameters:

        message (str):
            A message to display in the message box.

        title (str):
            The string displayed as the title of the messagebox. This
            option is ignored on Mac OS X, where platform guidelines
            forbid the use of a title on this kind of dialog.

        alert (bool):
            Specified whether to ring the display bell.

        parent (Union[Window, Toplevel]):
            Makes the window the logical parent of the message box. The
            message box is displayed on top of its parent window.
    """
    sd = MessageDialog(
        title=title,
        message=message,
        parent=parent,
        alert=alert,
        buttons=['OK:primary']
    )
    sd.show()


def okcancel(message, title=None, alert=False, parent=None):
    """Displays a modal dialog box with OK and Cancel buttons and
    return the symbolic name of the button pressed.

    Parameters:

        message (str):
            A message to display in the message box.

        title (str):
            The string displayed as the title of the messagebox. This
            option is ignored on Mac OS X, where platform guidelines
            forbid the use of a title on this kind of dialog.

        alert (bool):
            Specified whether to ring the display bell.

        parent (Union[Window, Toplevel]):
            Makes the window the logical parent of the message box. The
            message box is displayed on top of its parent window.

    Returns:

        Union[str, None]:
            The symbolic name of the button pressed, or None if the
            window is closed without pressing a button.
    """
    sd = MessageDialog(
        title=title,
        message=message,
        parent=parent
    )
    sd.show()
    return sd.result


def yesno(message, title=None, alert=False, parent=None):
    """Display a modal dialog box with YES and NO buttons and return
    the symbolic name of the button pressed.

    Parameters:

        message (str):
            A message to display in the message box.

        title (str):
            The string displayed as the title of the messagebox. This
            option is ignored on Mac OS X, where platform guidelines
            forbid the use of a title on this kind of dialog.

        alert (bool):
            Specified whether to ring the display bell.

        parent (Union[Window, Toplevel]):
            Makes the window the logical parent of the message box. The
            message box is displayed on top of its parent window.

    Returns:

        Union[str, None]:
            The symbolic name of the button pressed, or None if the
            window is closed without pressing a button.
    """
    sd = MessageDialog(
        title=title,
        message=message,
        parent=parent,
        buttons=['No', 'Yes:primary']
    )
    sd.show()
    return sd.result


def yesnocancel(message, title=None, alert=False, parent=None):
    """Display a modal dialog box with YES, NO, and Cancel buttons,
    and return the symbolic name of the button pressed.

    Parameters:

        message (str):
            A message to display in the message box.

        title (str):
            The string displayed as the title of the messagebox. This
            option is ignored on Mac OS X, where platform guidelines
            forbid the use of a title on this kind of dialog.

        alert (bool):
            Specified whether to ring the display bell.

        parent (Union[Window, Toplevel]):
            Makes the window the logical parent of the message box. The
            message box is displayed on top of its parent window.

    Returns:

        Union[str, None]:
            The symbolic name of the button pressed, or None if the
            window is closed without pressing a button.
    """
    sd = MessageDialog(
        title=title,
        message=message,
        parent=parent,
        buttons=['Cancel', 'No', 'Yes:primary']
    )
    sd.show()
    return sd.result


def retrycancel(message, title=None, alert=False, parent=None):
    """Display a modal dialog box with RETRY and Cancel buttons;
    returns the symbolic name of the button pressed.

    Parameters:

        message (str):
            A message to display in the message box.

        title (str):
            The string displayed as the title of the messagebox. This
            option is ignored on Mac OS X, where platform guidelines
            forbid the use of a title on this kind of dialog.

        alert (bool):
            Specified whether to ring the display bell.

        parent (Union[Window, Toplevel]):
            Makes the window the logical parent of the message box. The
            message box is displayed on top of its parent window.

    Returns:

        Union[str, None]:
            The symbolic name of the button pressed, or None if the
            window is closed without pressing a button.
    """
    sd = MessageDialog(
        title=title,
        message=message,
        parent=parent,
        alert=alert,
        buttons=['Cancel', 'Retry:primary']
    )
    sd.show()
    return sd.result
