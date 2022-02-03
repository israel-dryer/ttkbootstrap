"""
    This module contains various custom scrolling widgets, including 
    `ScrolledText` and `ScrolledFrame`.
"""
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import Pack, Place, Grid


class ScrolledText(ttk.Frame):
    """A text widget with optional vertical and horizontal scrollbars.
    Setting `autohide=True` will cause the scrollbars to hide when the
    mouse is not over the widget. The vertical scrollbar is on by
    default, but can be turned off. The horizontal scrollbar can be
    enabled by setting `vbar=True`.
    
    This widget is identical in configuration to the `Text` widget other
    than the scrolling frame. https://tcl.tk/man/tcl8.6/TkCmd/text.htm

    ![scrolled text](../../../assets/scrolled/scrolledtext.gif)  

    Examples:

        ```python
        import ttkbootstrap as ttk
        from ttkbootstrap.constants import *
        from ttkbootstrap.scrolled import ScrolledText

        app = ttk.Window()

        # scrolled text with autohide vertical scrollbar
        st = ScrolledText(app, padding=5, height=10, autohide=True)
        st.pack(fill=BOTH, expand=YES)

        # add text
        st.insert(END, 'Insert your text here.')

        app.mainloop()        
        ```
    """

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
        self._text = ttk.Text(self, padx=50, **kwargs)
        self._hbar = None
        self._vbar = None

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
            self._vbar.place(relx=1.0, relheight=1.0, anchor=NE)
            self._text.configure(yscrollcommand=self._vbar.set)

        if hbar:
            self._hbar = ttk.Scrollbar(
                master=self,
                bootstyle=bootstyle,
                command=self._text.xview,
                orient=HORIZONTAL,
            )
            self._hbar.place(rely=1.0, relwidth=1.0, anchor=SW)
            self._text.configure(xscrollcommand=self._hbar.set, wrap="none")

        self._text.pack(side=LEFT, fill=BOTH, expand=YES)

        # position scrollbars
        if self._hbar:
            self.update_idletasks()
            self._text_width = self.winfo_reqwidth()
            self._scroll_width = self.winfo_reqwidth()

        self.bind("<Configure>", self._on_configure)

        if autohide:
            self.autohide_scrollbar()
            self.hide_scrollbars()

    def _on_configure(self, *_):
        """Callback for when the configure method is used"""
        if self._hbar:
            self.update_idletasks()
            text_width = self.winfo_width()
            vbar_width = self._vbar.winfo_width()
            relx = (text_width - vbar_width) / text_width
            self._hbar.place(rely=1.0, relwidth=relx)

    def hide_scrollbars(self, *_):
        """Hide the scrollbars."""
        try:
            self._vbar.lower(self._text)
        except:
            pass
        try:
            self._hbar.lower(self._text)
        except:
            pass

    def show_scrollbars(self, *_):
        """Show the scrollbars."""
        try:
            self._vbar.lift(self._text)
        except:
            pass
        try:
            self._hbar.lift(self._text)
        except:
            pass

    def autohide_scrollbar(self, *_):
        """Show the scrollbars when the mouse enters the widget frame,
        and hide when it leaves the frame."""
        self.bind("<Enter>", self.show_scrollbars)
        self.bind("<Leave>", self.hide_scrollbars)


class ScrolledFrame(ttk.Frame):
    """A widget container with a vertical scrollbar.

    The scrollbar has an autohide feature that can be turned on by
    setting `autohide=True`.

    There is unfortunately not a clean way to implement this megawidget
    in tkinter. A common implementation is to reference an internal
    frame as the master for objects to be packed, placed, etc... I've
    chosen to expose the internal container foremost, so that you can
    use this `ScrolledFrame` just as you would a normal frame. This
    is more natural. However, there are cases when you need to have
    the actual parent container, and for that reason, you can access
    this parent container object via `ScrolledFrame.container`.
    Specifically, you will need this object when adding a
    `ScrolledFrame` to a `Notebook` or `Panedwindow`. For example,
    `mynotebook.add(myscrolledframe.container)`.

    Examples:

        ```python
        import ttkbootstrap as ttk
        from ttkbootstrap.constants import *
        from ttkbootstrap.scrolled import ScrolledFrame

        app = ttk.Window()

        sf = ScrolledFrame(app, autohide=True)
        sf.pack(fill=BOTH, expand=YES, padx=10, pady=10)

        # add a large number of checkbuttons into the scrolled frame
        for x in range(20):
            ttk.Checkbutton(sf, text=f"Checkbutton {x}").pack(anchor=W)

        app.mainloop()        
        ```
"""
    def __init__(
        self,
        master=None,
        padding=2,
        bootstyle=DEFAULT,
        autohide=False,
        height=None,
        width=None,
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

            autohide (bool):
                When **True**, the scrollbars will hide when the mouse
                is not within the frame bbox.

            height (int):
                The height of the frame in screen units.

            width (int):
                The widget of the frame in screen units.

            **kwargs (Dict[str, Any]):
                Other keyword arguments.
        """
        self.container = ttk.Frame(
            master=master, 
            relief=FLAT, 
            borderwidth=0
        )
        self._canvas = ttk.Canvas(
            self.container,
            relief=FLAT,
            borderwidth=0,
            highlightthickness=0,
            height=height,
            width=width,
        )
        self._canvas.pack(fill=BOTH, expand=YES)
        self._vbar = ttk.Scrollbar(
            master=self.container,
            bootstyle=bootstyle,
            command=self._canvas.yview,
            orient=VERTICAL,
        )
        self._vbar.place(relx=1.0, relheight=1.0, anchor=NE)
        self._canvas.configure(yscrollcommand=self._vbar.set)

        super().__init__(
            master=self._canvas, 
            padding=padding, 
            bootstyle=bootstyle, 
            **kwargs
        )
        self._winsys = self.tk.call('tk', 'windowingsystem')
        self._wid = self._canvas.create_window((0, 0), anchor=NW, window=self)

        # delegate text methods to frame
        _methods = vars(Pack).keys() | vars(Grid).keys() | vars(Place).keys()
        for method in _methods:
            if any(["pack" in method, "grid" in method, "place" in method]):
                setattr(self, method, getattr(self.container, method))

        self.container.bind("<Configure>", self._on_configure, "+")
        self.container.bind("<Map>", self._on_map, "+")
        self.container.bind("<Enter>", self._enable_scrolling, "+")
        self.container.bind("<Leave>", self._disable_scrolling, "+")
        self.refresh_geometry()
        
        if autohide:
            self.autohide_scrollbar()
            self.hide_scrollbars()  

    def _on_configure(self, _):
        """Callback for when container is configured"""
        self.update_idletasks()
        height = max([self.winfo_height(), self.winfo_reqheight()])
        if self.container.winfo_ismapped():
            width = self.container.winfo_width()
            cheight = self.container.winfo_height()
        else:
            width = self.container.winfo_reqwidth()
            cheight = self.container.winfo_reqheight()
        height = cheight if height == 1 else height
        self._canvas.config(scrollregion=self._canvas.bbox(ALL))
        self._canvas.itemconfig(self._wid, width=width, height=height)

    def _on_map(self, _):
        """Callback for when the widget is mapped"""
        self.refresh_geometry()

    def refresh_geometry(self):
        """Force the frame to refresh its height based on the frame 
        contents. This is necessary if you've added widgets to the frame 
        after the screen has already been drawn.
        """
        self._on_configure(None)

    def hide_scrollbars(self, *_):
        """Hide the scrollbars."""
        try:
            self._vbar.lower(self._canvas)
        except:
            pass
        try:
            self._hbar.lower(self._canvas)
        except:
            pass

    def show_scrollbars(self, *_):
        """Show the scrollbars."""
        try:
            self._vbar.lift(self._canvas)
        except:
            pass
        try:
            self._hbar.lift(self._canvas)
        except:
            pass

    def autohide_scrollbar(self, *_):
        """Show the scrollbars when the mouse enters the widget frame,
        and hide when it leaves the frame."""
        self.container.bind("<Enter>", self.show_scrollbars)
        self.container.bind("<Leave>", self.hide_scrollbars)

    def _on_mousewheel(self, event):
        if self._winsys.lower() == 'win32':
            delta = -int(event.delta / 120)
        elif self._winsys.lower() == 'aqua':
            delta = -event.delta
        elif event.num == 4:
            delta = -1
        elif event.num == 5:
            delta = 1
        self._canvas.yview_scroll(delta, UNITS)

    def _enable_scrolling(self, *_):
        """Enable mousewheel scrolling on the frame and all of its
        children."""
        children = self.winfo_children()
        for widget in [self, *children]:
            if self._winsys.lower() == 'x11':
                widget.bind("<Button-4>", self._on_mousewheel, "+")
                widget.bind("<Button-5>", self._on_mousewheel, "+")
            else:
                widget.bind("<MouseWheel>", self._on_mousewheel, "+")

    def _disable_scrolling(self, *_):
        """Disabled mousewheel scrolling on the frame and all of its
        children."""
        children = self.winfo_children()
        for widget in [self, *children]:
            if self._winsys.lower() == 'x11':
                widget.unbind("<Button-4>")
                widget.unbind("<Button-5>")
            else:
                widget.unbind("<MouseWheel>")


