"""Platform / windowing-system helpers for ttkbootstrap applications."""


def windowing_system(widget):
    """Return the Tk windowing system for `widget`'s display.

    One of `'win32'` (Windows), `'aqua'` (macOS), or `'x11'` (Linux/Unix).
    Wraps `widget.tk.call('tk', 'windowingsystem')` so platform checks read the
    same everywhere instead of repeating the raw Tcl call.

    Parameters:

        widget (Misc):
            Any widget (or the root) whose interpreter is queried.

    Returns:

        str:
            The windowing system identifier.
    """
    return str(widget.tk.call('tk', 'windowingsystem'))
