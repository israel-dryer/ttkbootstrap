"""
    This module contains various custom scrolling widgets, including 
    `ScrolledText` and `ScrolledFrame`.
"""

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import Pack, Place, Grid


"""
    # TODO reconfigure autohide implementation
    - Use the place manager to set the scrollbar to (relx=1, relheight=1, anchor=NE)
    - Allow the text to fill 100% of the space
    - Lower the scrollbar to hide, Raise the scrollbar to make visible
    - hide the scrollbar is at 100% of height or width
    - Show the scrollbar when the mousewheel is used, then hide again on button click.
    - ANOTHER option is to have a *hidden* style that is applied whenever the scrollbar is inactive
"""

class ScrolledText(ttk.Frame):
    """A text widget with a vertical scrollbar."""

    def __init__(
        self,
        master=None,
        padding=2,
        bootstyle=DEFAULT,
        autohide=False,
        vbar=True,
        hbar=False,
        **kwargs,
    ):
        """
        Parameters:

            master (Widget):
                The parent widget.

            padding (int):
                The amount of empty space to create on the outside of
                the widget.

            bootstyle (str):
                A style keyword used to set the color and style of the
                vertical scrollbar. Available options include -> primary,
                secondary, success, info, warning, danger, dark, light.

            vbar (bool):
                A vertical scrollbar is shown when **True** (default).

            hbar (bool):
                A horizontal scrollbar is shown when **True**. Turning
                on this scrollbar will also set `wrap="none"`. This
                scrollbar is _off_ by default.

            autohide (bool):
                When **True**, the scrollbars will hide when the mouse
                is not within the frame bbox.

            **kwargs (Dict[str, Any]):
                Other keyword arguments passed to the `Text` widget.
        """
        super().__init__(master, padding=padding)

        # setup text widget
        self._text = ttk.Text(self, **kwargs)

        # delegate text methods to frame
        for method in vars(ttk.Text).keys():
            if any(["pack" in method, "grid" in method, "place" in method]):
                pass
            else:
                setattr(self, method, getattr(self._text, method))

        # setup scrollbars
        if vbar:
            self._vbar = ttk.Scrollbar(
                master=self,
                bootstyle=bootstyle,
                command=self._text.yview,
                orient=VERTICAL,
            )
            self._vbar.pack(side=RIGHT, fill=Y)
            self._text.configure(yscrollcommand=self._vbar.set)

        if hbar:
            self._hbar = ttk.Scrollbar(
                master=self,
                bootstyle=bootstyle,
                command=self._text.xview,
                orient=HORIZONTAL,
            )
            self._hbar.pack(side=BOTTOM, fill=X)
            self._text.configure(xscrollcommand=self._hbar.set, wrap="none")

        self._text.pack(side=LEFT, fill=BOTH, expand=YES)

        if autohide:
            self.autohide_scrollbar()
            self.hide_scrollbars()

    def hide_scrollbars(self, *_):
        """Hide the scrollbars."""
        try:
            self._vbar.pack_forget()
        except:
            pass
        try:
            self._hbar.pack_forget()
        except:
            pass

    def show_scrollbars(self, *_):
        """Show the scrollbars."""
        try:
            self._vbar.pack(side=RIGHT, fill=Y)
        except:
            pass
        try:
            self._hbar.pack(side=BOTTOM, fill=X)
        except:
            pass

    def autohide_scrollbar(self, *_):
        """Show the scrollbars when the mouse enters the widget frame,
        and hide when it leaves the frame."""
        self.bind("<Enter>", self.show_scrollbars)
        self.bind("<Leave>", self.hide_scrollbars)


# TODO refactor <MouseWheel> to include only canvas children

class ScrolledFrame(ttk.Frame):
    """A widget container with a vertical scrollbar.
    
    !!! note "Note on implementation
        There is unfortunately not a clean way to implement this feature
        in tkinter. A common implementation is to reference an internal
        frame as the master for objects to be packed, placed, etc... I've
        chosen to expose the internal container first, so that you can
        use this `ScrolledFrame` just as you would a normal frame. This
        is more natural. However, there are cases when you need to have
        the actual parent container, and for that reason, you can access
        this parent container object via `ScrolledFrame.container`. 
        Specifically, you will need this object when adding a 
        `ScrolledFrame` to a `Notebook` or `Panedwindow`. For example, 
        `mynotebook.add(myscrolledframe.container)`.
    """

    def __init__(
        self,
        master=None,
        padding=2,
        width=None,
        height=None,
        bootstyle=DEFAULT,
    ):
        self.container = ttk.Frame(master, padding=padding, relief=FLAT, borderwidth=0)
        self._canvas = ttk.Canvas(
            master=self.container,
            relief=FLAT,
            borderwidth=0,
            highlightthickness=0,
            height=height,
            width=width,
        )
        self._canvas.pack(side=LEFT, fill=BOTH, expand=YES)
        self._vbar = ttk.Scrollbar(
            master=self.container,
            orient=VERTICAL,
            command=self._canvas.yview,
            bootstyle=bootstyle,
        )
        self._vbar.pack(side=RIGHT, fill=Y)
        self._canvas.configure(yscrollcommand=self._vbar.set)

        super().__init__(self._canvas)
        self._wid = self._canvas.create_window((0, 0), anchor=NW, window=self)

        # delegate geometry methods to outer frame
        for method in (
            vars(Pack).keys() | vars(Place).keys() | vars(Grid).keys()
        ):
            if any(["pack" in method, "grid" in method, "place" in method]):
                setattr(self, method, getattr(self.container, method))

        self._canvas.bind("<Configure>", self._resize_canvas, "+")
        self._canvas.bind("<Enter>", self._enable_scrolling, "+")
        self._canvas.bind("<Leave>", self._disable_scrolling, "+")

    def _resize_canvas(self, *_):
        """Resize the canvas when frame is resized"""
        self.update_idletasks()
        self._canvas.config(scrollregion=self._canvas.bbox(ALL))
        self._canvas.itemconfig(self._wid, width=self._canvas.winfo_width())

    def _on_mousewheel(self, event):
        delta = -int(event.delta / 120)
        self._canvas.yview_scroll(delta, UNITS)

    def _enable_scrolling(self, *_):
        self.bind_all("<MouseWheel>", self._on_mousewheel)

    def _disable_scrolling(self, *_):
        self.unbind_all("<MouseWheel>")


if __name__ == "__main__":

    app = ttk.Window()

    # TEST SCROLLED TEXT
    # st = ScrolledText(app, hbar=True, padding=20)
    # st.pack(fill=BOTH, expand=YES)

    # TEST SCROLLED FRAME
    nb = ttk.Notebook()
    nb.pack()
    sf = ScrolledFrame(app)
    nb.add(sf.container, text="ScrolledFrame", padding=10)
    for x in range(20):
        ttk.Button(sf, text=f"button {x}").pack(anchor=W)

    app.mainloop()
