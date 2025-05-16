from tkinter import Text
from tkinter.ttk import Frame
from typing import Literal

from ttkbootstrap.widgets import Scrollbar


class ScrolledText(Frame):
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
        color=None,
        variant: Literal['default', 'round'] = "default",
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
        self._text = Text(self, padx=50, **kwargs)
        self._hbar = None
        self._vbar = None

        # delegate text methods to frame
        for method in vars(Text).keys():
            if any(["pack" in method, "grid" in method, "place" in method]):
                pass
            else:
                setattr(self, method, getattr(self._text, method))

        # setup scrollbars
        if vbar:
            self._vbar = Scrollbar(
                master=self,
                color=color,
                variant=variant,
                command=self._text.yview,
                orient="vertical",
            )
            self._vbar.place(relx=1.0, relheight=1.0, anchor="ne")
            self._text.configure(yscrollcommand=self._vbar.set)

        if hbar:
            self._hbar = Scrollbar(
                master=self,
                color=color,
                variant=variant,
                command=self._text.xview,
                orient="horizontal",
            )
            self._hbar.place(rely=1.0, relwidth=1.0, anchor="sw")
            self._text.configure(xscrollcommand=self._hbar.set, wrap="none")

        self._text.pack(side="left", fill="both", expand=1)

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

    @property
    def text(self):
        """Returns the internal text object"""
        return self._text

    @property
    def hbar(self):
        """Returns the internal horizontal scrollbar"""
        return self._hbar

    @property
    def vbar(self):
        """Returns the internal vertical scrollbar"""
        return self._vbar

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
