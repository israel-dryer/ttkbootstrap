from tkinter import font
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap import utility

# https://www.fontspace.com/freeserif-font-f13277

DEFAULT_ICON_WIN32 = "\ue154"
DEFAULT_ICON = "\u25f0"


class ToastNotification:
    """A semi-transparent popup window for temporary alerts or messages.
    You may choose to display the toast for a specified period of time,
    otherwise you must click the toast to close it.

    ![toast notification](../assets/toast/toast.png)
    """

    def __init__(
        self,
        title,
        message,
        duration=None,
        bootstyle=LIGHT,
        alert=False,
        icon=None,
        iconfont=None,
        **kwargs,
    ):
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
                A unicode character to display on the top-left hand
                corner of the toast. The default symbol is OS specific.
                Pass an empty string to remove the symbol.

            iconfont (Union[str, Font]):
                The font used to render the icon. By default, this is
                OS specific. You may need to change the font to enable
                better character or emoji support for the icon you
                want to use. Windows (Segoe UI Symbol),
                Linux (FreeSerif), MacOS (Apple Symbol)

            **kwargs (Dict):
                Other keyword arguments passed to the `Toplevel` window.
        """
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

        if "overrideredirect" not in self.kwargs:
            self.kwargs["overrideredirect"] = True
        if "alpha" not in self.kwargs:
            self.kwargs["alpha"] = 0.95

    def show_toast(self, *_):
        """Create and show the toast window."""

        # build toast
        self.toplevel = ttk.Toplevel(**self.kwargs)
        self._setup(self.toplevel)

        self.container = ttk.Frame(self.toplevel, bootstyle=self.bootstyle)
        self.container.pack(fill=BOTH, expand=YES)
        ttk.Label(
            self.container,
            text=self.icon,
            font=self.iconfont,
            bootstyle=f"{self.bootstyle}-inverse",
            anchor=NW,
        ).grid(row=0, column=0, rowspan=2, sticky=NSEW, padx=(5, 0))
        ttk.Label(
            self.container,
            text=self.title,
            font=self.titlefont,
            bootstyle=f"{self.bootstyle}-inverse",
            anchor=NW,
        ).grid(row=0, column=1, sticky=NSEW, padx=10, pady=(5, 0))
        ttk.Label(
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

    def hide_toast(self, *_):
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

    def _setup(self, window: ttk.Toplevel):
        winsys = window.tk.call("tk", "windowingsystem")

        self.toplevel.configure(relief=RAISED)

        # minsize
        if "minsize" not in self.kwargs:
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
            if "position" not in self.kwargs:
                self.toplevel.geometry("-2-75")

        elif winsys == "x11":
            self.iconfont["family"] = "FreeSerif"
            self.icon = DEFAULT_ICON if self.icon is None else self.icon
            if "position" not in self.kwargs:
                self.toplevel.geometry("-2-75")
        else:
            self.iconfont["family"] = "Apple Symbols"
            self.icon = DEFAULT_ICON if self.icon is None else self.icon
            if "position" not in self.kwargs:
                self.toplevel.update_idletasks()
                self.toplevel.geometry(f"-5+30")


if __name__ == "__main__":

    app = ttk.Window()

    ToastNotification(
        "ttkbootstrap toast message",
        "This is a toast message;",
    ).show_toast()

    app.mainloop()
