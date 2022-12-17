import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap import utility


class ToolTip:
    """A semi-transparent tooltip popup window that shows text when the
    mouse is hovering over the widget and closes when the mouse is no
    longer hovering over the widget. Clicking a mouse button will also
    close the tooltip.

    ![](../assets/tooltip/tooltip.gif)

    Examples:

        ```python
        import ttkbootstrap as ttk
        from ttkbootstrap.constants import *
        from ttkbootstrap.tooltip import ToolTip

        app = ttk.Window()
        b1 = ttk.Button(app, text="default tooltip")
        b1.pack()
        b2 = ttk.Button(app, text="styled tooltip")
        b2.pack()

        # default tooltip
        ToolTip(b1, text="This is the default style")

        # styled tooltip
        ToolTip(b2, text="This is dangerous", bootstyle=(DANGER, INVERSE))

        app.mainloop()
        ```    
    """

    def __init__(
        self,
        widget,
        text="widget info",
        bootstyle=None,
        wraplength=None,
        delay=250,    # milliseconds
        **kwargs,
    ):
        """
        Parameters:

            widget (Widget):
                The tooltip window will position over this widget when
                hovering.

            text (str):
                The text to display in the tooltip window.

            bootstyle (str):
                The style to apply to the tooltip label. You can use
                any of the standard ttkbootstrap label styles.

            wraplength (int):
                The width of the tooltip window in screenunits before the
                text is wrapped to the next line. By default, this will be
                a scaled factor of 300.

            **kwargs (Dict):
                Other keyword arguments passed to the `Toplevel` window.
        """
        self.widget = widget
        self.text = text
        self.bootstyle = bootstyle
        self.wraplength = wraplength or utility.scale_size(self.widget, 300)
        self.toplevel = None
        self.delay = delay
        self.id = None

        # set keyword arguments
        kwargs["overrideredirect"] = True
        kwargs["master"] = self.widget
        if "alpha" not in kwargs:
            kwargs["alpha"] = 0.95
        self.toplevel_kwargs = kwargs

        # create default tooltip style
        ttk.Style().configure(
            style="tooltip.TLabel",
            background="#fffddd",
            foreground="#333",
            bordercolor="#888",
            borderwidth=1,
            darkcolor="#fffddd",
            lightcolor="#fffddd",
            relief=RAISED,
        )

        # event binding
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<Motion>", self.move_tip)
        self.widget.bind("<ButtonPress>", self.leave)

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hide_tip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.delay, self.show_tip)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def show_tip(self, *_):
        """Create a show the tooltip window"""
        if self.toplevel:
            return
        x = self.widget.winfo_pointerx() + 25
        y = self.widget.winfo_pointery() + 10

        self.toplevel = ttk.Toplevel(position=(x, y), **self.toplevel_kwargs)
        lbl = ttk.Label(
            master=self.toplevel,
            text=self.text,
            justify=LEFT,
            wraplength=self.wraplength,
            padding=10,
        )
        lbl.pack(fill=BOTH, expand=YES)
        if self.bootstyle:
            lbl.configure(bootstyle=self.bootstyle)
        else:
            lbl.configure(style="tooltip.TLabel")

    def move_tip(self, *_):
        """Move the tooltip window to the current mouse position within the
        widget.
        """
        if self.toplevel:
            x = self.widget.winfo_pointerx() + 25
            y = self.widget.winfo_pointery() + 10
            self.toplevel.geometry(f"+{x}+{y}")

    def hide_tip(self, *_):
        """Destroy the tooltip window."""
        if self.toplevel:
            self.toplevel.destroy()
            self.toplevel = None


if __name__ == "__main__":

    app = ttk.Window()

    b1 = ttk.Button(app, text="default tooltip")
    b1.pack(side=LEFT, padx=20, pady=20, fill=X, expand=YES)

    l1 = ttk.Label(app, text="styled tooltip")
    l1.pack(side=LEFT, padx=20, pady=20, fill=X, expand=YES)

    ToolTip(
        b1,
        text="This is the default tooltip style",
    )
    ToolTip(
        l1,
        text="Do not touch this label unless you are sure you want to do something dangerous.",
        bootstyle="danger-inverse",
    )

    app.mainloop()
