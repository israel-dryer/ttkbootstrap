from __future__ import annotations

import tkinter
from typing import Any, Optional, Tuple

from ttkbootstrap.runtime.base_window import BaseWindow


class Toplevel(BaseWindow, tkinter.Toplevel):
    """A class that wraps the tkinter.Toplevel class in order to
    provide a more convenient api with additional bells and whistles.
    For more information on how to use the inherited `Toplevel`
    methods, see the [tcl/tk documentation](https://tcl.tk/man/tcl8.6/TkCmd/toplevel.htm)
    and the [Python documentation](https://docs.python.org/3/library/tkinter.html#tkinter.Toplevel).

    Examples:
        >>> app = Toplevel(title="My Toplevel")
        >>> app.mainloop()
    """

    def __init__(
            self,
            title: str = "ttkbootstrap",
            icon: tkinter.PhotoImage | None = None,
            size: Optional[Tuple[int, int]] = None,
            position: Optional[Tuple[int, int]] = None,
            minsize: Optional[Tuple[int, int]] = None,
            maxsize: Optional[Tuple[int, int]] = None,
            resizable: Optional[Tuple[bool, bool]] = None,
            transient: Optional[tkinter.Misc] = None,
            overrideredirect: bool = False,
            windowtype: Optional[str] = None,
            topmost: bool = False,
            toolwindow: bool = False,
            alpha: float = 1.0,
            **kwargs: Any,
    ) -> None:
        """Initialize a Toplevel window.

        Args:
            title: The title that appears on the application titlebar.
            icon: A PhotoImage or file path used for the titlebar icon.
                If None, the default ttkbootstrap.png icon is used.
                Internally this is passed to the `Toplevel.iconphoto` method.
            size: The width and height of the application window.
                Internally, this argument is passed to the `Toplevel.geometry` method.
            position: The horizontal and vertical position of the window on
                the screen relative to the top-left coordinate.
                Internally this is passed to the `Toplevel.geometry` method.
            minsize: Specifies the minimum permissible dimensions for the
                window. Internally, this argument is passed to the
                `Toplevel.minsize` method.
            maxsize: Specifies the maximum permissible dimensions for the
                window. Internally, this argument is passed to the
                `Toplevel.maxsize` method.
            resizable: Specifies whether the user may interactively resize the
                toplevel window. Must pass in two arguments that specify
                this flag for horizontal and vertical dimensions.
                This can be adjusted after the window is created by using
                the `Toplevel.resizable` method.
            transient: Instructs the window manager that this widget is
                transient with regard to the widget master. Internally
                this is passed to the `Toplevel.transient` method.
            overrideredirect: Instructs the window manager to ignore this widget if
                True. Internally, this argument is processed as
                `Toplevel.overrideredirect(1)`.
            windowtype: On X11, requests that the window should be interpreted by
                the window manager as being of the specified type. Internally,
                this is passed to the `Toplevel.attributes('-type', windowtype)`.
            topmost: Specifies whether this is a topmost window (displays above all
                other windows). Internally, this processed by the window as
                `Toplevel.attributes('-topmost', 1)`.
            toolwindow: On Windows, specifies a toolwindow style. Internally, this is
                processed as `Toplevel.attributes('-toolwindow', 1)`.
            alpha: On Windows, specifies the alpha transparency level of the
                toplevel. Where not supported, alpha remains at 1.0. Internally,
                this is processed as `Toplevel.attributes('-alpha', alpha)`.
            **kwargs: Other optional keyword arguments.
        """
        # Extract iconify kwarg if present
        iconify = kwargs.pop('iconify', None)

        # Initialize Toplevel
        tkinter.Toplevel.__init__(self, **kwargs)

        # Setup window system info
        self.winsys: str = self.tk.call('tk', 'windowingsystem')

        # Setup icon (use default ttkbootstrap.png if no icon provided)
        self._setup_icon(icon, default_icon_enabled=True)

        # Setup window using BaseWindow
        self._setup_window(
            title=title,
            size=size,
            position=position,
            minsize=minsize,
            maxsize=maxsize,
            resizable=resizable,
            transient=transient,
            overrideredirect=overrideredirect,
            alpha=alpha
        )

        # Handle iconify
        if iconify:
            self.iconify()

        # Toplevel-specific window attributes
        if windowtype is not None and self.winsys == 'x11':
            self.attributes("-type", windowtype)

        if topmost:
            self.attributes("-topmost", 1)

        if toolwindow and self.winsys == 'win32':
            self.attributes("-toolwindow", 1)
