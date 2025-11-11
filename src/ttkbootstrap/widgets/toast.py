"""Toast notification popup widgets for ttkbootstrap.

This module provides a semi-transparent toast notification system for displaying
temporary alerts or messages. Toasts appear as popup windows that can be configured
to automatically close after a duration or require user interaction to dismiss.

Classes:
    ToastNotification: Semi-transparent popup for alerts and messages

Features:
    - Configurable display duration or click-to-close behavior
    - Bootstrap styling support (primary, secondary, success, danger, etc.)
    - Customizable icon and font support
    - Flexible positioning (anchored to screen corners)
    - Optional audible alert bell
    - Smooth fade-out animation on close

Example:
    ```python
    import ttkbootstrap as ttk
    from ttkbootstrap.toast import ToastNotification

    app = ttk.Window()

    # Toast with auto-close after 3 seconds
    toast = ToastNotification(
        title="ttkbootstrap toast message",
        message="This is a toast message",
        duration=3000,
        bootstyle="info",
    )
    toast.show_toast()

    # Toast that requires click to close
    toast2 = ToastNotification(
        title="Important Notice",
        message="Click to dismiss this message",
        bootstyle="warning",
        alert=True,  # Ring bell when shown
    )
    toast2.show_toast()

    app.mainloop()
    ```
"""
from tkinter import font
from typing import Any, TYPE_CHECKING, Optional, Union

from ttkbootstrap.constants import *

# https://www.fontspace.com/freeserif-font-f13277

DEFAULT_ICON_WIN32 = "\ue154"
DEFAULT_ICON = "\u25f0"


class ToastNotification:
    """A semi-transparent popup window for temporary alerts or messages.
    You may choose to display the toast for a specified period of time,
    otherwise you must click the toast to close it.

    ![toast notification](../assets/toast/toast.png)

    Examples:

        ```python
        import ttkbootstrap as ttk
        from ttkbootstrap.toast import ToastNotification

        app = ttk.Window()

        toast = ToastNotification(
            title="ttkbootstrap toast message",
            message="This is a toast message",
            duration=3000,
        )
        toast.show_toast()

        app.mainloop()
        ```
    """

    def __init__(
            self,
            title: str,
            message: str,
            duration: Optional[int] = None,
            bootstyle: str = LIGHT,
            alert: bool = False,
            icon: Optional[str] = None,
            iconfont: Optional[Union[font.Font, str]] = None,
            position: Optional[tuple[int, int, str]] = None,
            **kwargs: Any,
    ) -> None:
        """
        Parameters:

            title (str):
                The toast title.

            message (str):
                The toast message.

            duration (int):
                The number of milliseconds to show the toast. If None
                (default), then you must click the toast to close it.

            bootstyle (str):
                Style keywords used to updated the label style. One of
                the accepted color keywords.

            alert (bool):
                Indicates whether to ring the display bell when the
                toast is shown.

            icon (str):
                A UNICODE character to display on the top-left hand
                corner of the toast. The default symbol is OS specific.
                Pass an empty string to remove the symbol.

            iconfont (Union[str, Font]):
                The font used to render the icon. By default, this is
                OS specific. You may need to change the font to enable
                better character or emoji support for the icon you
                want to use. Windows (Segoe UI Symbol),
                Linux (FreeSerif), macOS (Apple Symbol)

            position (tuple[int, int, str]):
                A tuple that controls the position of the toast. Default
                is OS specific. The tuple cooresponds to
                (horizontal, vertical, anchor), where the horizontal and
                vertical elements represent the position of the toplevel
                releative to the anchor, which is "ne" or top-left by
                default. Acceptable anchors include: n, e, s, w, nw, ne,
                sw, se. For example: (100, 100, 'ne').

            **kwargs (Dict):
                Other keyword arguments passed to the `Toplevel` window.
        """
        self.container = None
        self.message = message
        self.title = title
        self.duration = duration
        self.bootstyle = bootstyle
        self.icon = icon
        self.iconfont = iconfont
        self.iconfont = None
        self.titlefont = None
        self.toplevel = None
        self.kwargs = kwargs
        self.alert = alert
        self.position = position

        if "overrideredirect" not in self.kwargs:
            self.kwargs["overrideredirect"] = True
        if "alpha" not in self.kwargs:
            self.kwargs["alpha"] = 0.95

        if position is not None:
            if len(position) != 3:
                self.position = None

    def show_toast(self, *_: Any) -> None:
        """Create and show the toast window."""
        # Late import to avoid circular import during package initialization
        from ttkbootstrap import Frame, Label, Toplevel, utility

        # build toast
        self.toplevel = Toplevel(**self.kwargs)
        self._setup(self.toplevel)

        self.container = Frame(self.toplevel, bootstyle=self.bootstyle)
        self.container.pack(fill=BOTH, expand=YES)
        Label(
            self.container,
            text=self.icon,
            font=self.iconfont,
            bootstyle=f"{self.bootstyle}-inverse",
            anchor=NW,
        ).grid(row=0, column=0, rowspan=2, sticky=NSEW, padx=(5, 0))
        Label(
            self.container,
            text=self.title,
            font=self.titlefont,
            bootstyle=f"{self.bootstyle}-inverse",
            anchor=NW,
        ).grid(row=0, column=1, sticky=NSEW, padx=10, pady=(5, 0))
        Label(
            self.container,
            text=self.message,
            wraplength=utility.scale_size(self.toplevel, 300),
            bootstyle=f"{self.bootstyle}-inverse",
            anchor=NW,
        ).grid(row=1, column=1, sticky=NSEW, padx=10, pady=(0, 5))

        self.toplevel.bind("<ButtonPress>", self.hide_toast)

        # alert toast
        if self.alert:
            self.toplevel.bell()

        # specified duration to close
        if self.duration:
            self.toplevel.after(self.duration, self.hide_toast)

    def hide_toast(self, *_: Any) -> None:
        """Destroy and close the toast window."""
        try:
            alpha = float(self.toplevel.attributes("-alpha"))
            if alpha <= 0.1:
                self.toplevel.destroy()
            else:
                self.toplevel.attributes("-alpha", alpha - 0.1)
                self.toplevel.after(25, self.hide_toast)
        except:
            if self.toplevel:
                self.toplevel.destroy()

    def _setup(self, window) -> None:
        winsys = window.tk.call("tk", "windowingsystem")

        self.toplevel.configure(relief=RAISED)

        # minsize
        if "minsize" not in self.kwargs:
            # Late import to avoid circular import for utility
            from ttkbootstrap import utility
            w, h = utility.scale_size(self.toplevel, [300, 75])
            self.toplevel.minsize(w, h)

        # heading font
        _font = font.nametofont("TkDefaultFont")
        self.titlefont = font.Font(
            family=_font["family"],
            size=_font["size"] + 1,
            weight="bold",
        )
        # symbol font
        self.iconfont = font.Font(size=30, weight="bold")
        if winsys == "win32":
            self.iconfont["family"] = "Segoe UI Symbol"
            self.icon = DEFAULT_ICON_WIN32 if self.icon is None else self.icon
            if self.position is None:
                from ttkbootstrap import utility
                x, y = utility.scale_size(self.toplevel, [5, 50])
                self.position = (x, y, SE)
        elif winsys == "x11":
            self.iconfont["family"] = "FreeSerif"
            self.icon = DEFAULT_ICON if self.icon is None else self.icon
            if self.position is None:
                from ttkbootstrap import utility
                x, y = utility.scale_size(self.toplevel, [0, 0])
                self.position = (x, y, SE)
        else:
            self.iconfont["family"] = "Apple Symbols"
            self.toplevel.update_idletasks()
            self.icon = DEFAULT_ICON if self.icon is None else self.icon
            if self.position is None:
                from ttkbootstrap import utility
                x, y = utility.scale_size(self.toplevel, [50, 50])
                self.position = (x, y, NE)

        self.set_geometry()

    def set_geometry(self) -> None:
        self.toplevel.update_idletasks()  # actualize geometry
        anchor = self.position[-1]
        x_anchor = "-" if "w" not in anchor else "+"
        y_anchor = "-" if "n" not in anchor else "+"
        screen_w = self.toplevel.winfo_screenwidth() // 2
        screen_h = self.toplevel.winfo_screenheight() // 2
        top_w = self.toplevel.winfo_width() // 2
        top_h = self.toplevel.winfo_height() // 2

        if all(["e" not in anchor, "w" not in anchor]):
            xpos = screen_w - top_w
        else:
            xpos = self.position[0]
        if all(["n" not in anchor, "s" not in anchor]):
            ypos = screen_h - top_h
        else:
            ypos = self.position[1]

        self.toplevel.geometry(f"{x_anchor}{xpos}{y_anchor}{ypos}")


if __name__ == "__main__":
    from ttkbootstrap import Window

    app = Window()

    ToastNotification(
        "ttkbootstrap toast message",
        "This is a toast message; you can place a symbol on the top-left that is supported by the selected font. You can either make it appear for a specified period of time, or click to close.",
    ).show_toast()

    app.mainloop()
