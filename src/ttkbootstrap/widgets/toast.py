from tkinter import font

from ttkbootstrap.ttk_types import StyleColor
from ttkbootstrap.widgets.frame import Frame
from ttkbootstrap.widgets.label import Label
from ttkbootstrap.window import Toplevel
from ttkbootstrap.utility import scale_size

DEFAULT_ICON_WIN32 = "\ue154"
DEFAULT_ICON = "\u25f0"


class ToastNotification:
    """
    A semi-transparent popup window for temporary alerts or messages.

    This widget creates a floating `Toplevel` window that displays a brief
    message, optionally accompanied by an icon and heading. It can be dismissed
    manually or automatically after a specified duration.

    Features:
    ---------
    - Transparent, borderless popup window
    - Optional alert sound on display
    - Optional duration-based auto-dismiss
    - Fully themed using ttkbootstrap color and style
    - OS-specific positioning and font fallback
    - Click-to-dismiss behavior

    Parameters:
    -----------
    title (str):
        The title text displayed in bold at the top of the toast.

    message (str):
        The message content displayed below the title.

    duration (int, optional):
        The number of milliseconds to display the toast. If None,
        the toast must be dismissed manually.

    color (StyleColor, optional):
        A ttkbootstrap color keyword (e.g., "primary", "success")
        used to style the background and text.

    alert (bool, optional):
        If True, an audible bell is played when the toast is shown.

    icon (str, optional):
        A Unicode character to display as the icon. Default is OS-specific.
        Use an empty string "" to hide the icon.

    iconfont (str | Font, optional):
        A named font or `tkinter.font.Font` instance used for the icon.
        Font family is chosen automatically by default.

    position (tuple[int, int, str], optional):
        The position of the toast on screen. Format: (x_offset, y_offset, anchor),
        where anchor is one of: "n", "ne", "e", "se", "s", "sw", "w", "nw".
        If None, OS-specific defaults apply.

    **kwargs:
        Additional keyword arguments passed to the underlying `Toplevel`.

    Example:
    --------
    ```python
    from ttkbootstrap.toast import ToastNotification

    toast = ToastNotification(
        title="Success!",
        message="Your file has been uploaded successfully.",
        duration=3000,
        color="success",
        alert=True
    )
    toast.show_toast()
    ```
    """

    def __init__(
        self,
        title,
        message,
        duration=None,
        color: StyleColor = "light",
        alert=False,
        icon=None,
        iconfont=None,
        position=None,
        **kwargs,
    ):
        self.message = message
        self.title = title
        self.duration = duration
        self.color = color
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

    def show_toast(self, *_):
        """Create and show the toast window."""
        self.toplevel = Toplevel(**self.kwargs)
        self._setup(self.toplevel)

        self.container = Frame(self.toplevel, self.color)
        self.container.pack(fill="both", expand=1)

        Label(
            self.container,
            text=self.icon,
            font=self.iconfont,
            color=self.color,
            variant="inverse",
            anchor="nw",
        ).grid(row=0, column=0, rowspan=2, sticky="nsew", padx=(5, 0))

        Label(
            self.container,
            text=self.title,
            font=self.titlefont,
            color=self.color,
            variant="inverse",
            anchor="nw",
        ).grid(row=0, column=1, sticky="nsew", padx=10, pady=(5, 0))

        Label(
            self.container,
            text=self.message,
            wraplength=scale_size(self.toplevel, 300),
            color=self.color,
            variant="inverse",
            anchor="nw",
        ).grid(row=1, column=1, sticky="nsew", padx=10, pady=(0, 5))

        self.toplevel.bind("<ButtonPress>", self.hide_toast)

        if self.alert:
            self.toplevel.bell()

        if self.duration:
            self.toplevel.after(self.duration, self.hide_toast)

    def hide_toast(self, *_):
        """Destroy and close the toast window with fade-out effect."""
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

    def _setup(self, window: Toplevel):
        winsys = window.tk.call("tk", "windowingsystem")

        self.toplevel.configure(relief="raised")

        if "minsize" not in self.kwargs:
            w, h = scale_size(self.toplevel, [300, 75])
            self.toplevel.minsize(w, h)

        _font = font.nametofont("TkDefaultFont")
        self.titlefont = font.Font(
            family=_font["family"],
            size=_font["size"] + 1,
            weight="bold",
        )

        self.iconfont = font.Font(size=30, weight="bold")
        if winsys == "win32":
            self.iconfont["family"] = "Segoe UI Symbol"
            self.icon = DEFAULT_ICON_WIN32 if self.icon is None else self.icon
            if self.position is None:
                x, y = scale_size(self.toplevel, [5, 50])
                self.position = (x, y, "se")
        elif winsys == "x11":
            self.iconfont["family"] = "FreeSerif"
            self.icon = DEFAULT_ICON if self.icon is None else self.icon
            if self.position is None:
                x, y = scale_size(self.toplevel, [0, 0])
                self.position = (x, y, "se")
        else:
            self.iconfont["family"] = "Apple Symbols"
            self.toplevel.update_idletasks()
            self.icon = DEFAULT_ICON if self.icon is None else self.icon
            if self.position is None:
                x, y = scale_size(self.toplevel, [50, 50])
                self.position = (x, y, "ne")

        self.set_geometry()

    def set_geometry(self):
        """Set the position and anchor geometry of the toast on screen."""
        self.toplevel.update_idletasks()
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
