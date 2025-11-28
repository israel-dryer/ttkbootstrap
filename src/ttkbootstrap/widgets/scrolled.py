"""Scrolling widgets with optional autohide scrollbars for ttkbootstrap.

This module provides enhanced scrolling widgets that wrap standard tkinter
and ttk widgets with automatic scrollbar management. The scrollbars can be
configured to autohide when the mouse is not over the widget.

Classes:
    ScrolledText: Text widget with vertical/horizontal scrollbars
    ScrolledFrame: Frame container with vertical scrollbar

Features:
    - Optional autohide scrollbars (hide when mouse leaves widget)
    - Configurable vertical and horizontal scrollbars
    - Seamless delegation of widget methods
    - Bootstrap styling support via bootstyle parameter

Example:
    ```python
    import ttkbootstrap as ttk
    from ttkbootstrap.constants import *
    from ttkbootstrap.scrolled import ScrolledText, ScrolledFrame

    app = ttk.Window()

    # Scrolled text with autohide scrollbar
    st = ScrolledText(app, padding=5, height=10, autohide=True)
    st.pack(fill=BOTH, expand=YES)
    st.insert(END, 'Insert your text here.')

    # Scrolled frame for multiple widgets
    sf = ScrolledFrame(app, autohide=True)
    sf.pack(fill=BOTH, expand=YES, padx=10, pady=10)

    # Add widgets to scrolled frame
    for x in range(20):
        ttk.Checkbutton(sf, text=f"Checkbutton {x}").pack(anchor=W)

    app.mainloop()
    ```
"""
import tkinter
from tkinter import Grid, Pack, Place
from typing import Any, Callable, Optional, Tuple

import ttkbootstrap as ttk
from ttkbootstrap.constants import *


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
            master: Optional[tkinter.Misc] = None,
            padding: int = 2,
            bootstyle: str = DEFAULT,
            autohide: bool = False,
            vbar: bool = True,
            hbar: bool = False,
            **kwargs: Any,
    ) -> None:
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

            **kwargs (dict[str, Any]):
                Other keyword arguments passed to the `Text` widget.
        """
        super().__init__(master, padding=padding)

        # setup text widget
        self._text: ttk.Text = ttk.Text(self, padx=50, **kwargs)
        self._hbar: Optional[ttk.Scrollbar] = None
        self._vbar: Optional[ttk.Scrollbar] = None

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

    def _on_configure(self, *args: Any) -> None:
        """Callback for when the configure method is used."""
        if self._hbar:
            self.update_idletasks()
            text_width = self.winfo_width()
            vbar_width = self._vbar.winfo_width()
            relx = (text_width - vbar_width) / text_width
            self._hbar.place(rely=1.0, relwidth=relx)

    def __getattr__(self, name: str) -> Any:
        """Delegate unknown attribute access to the internal Text widget.

        This supports static type checkers by indicating that any missing
        attribute on ScrolledText should be treated as Any and forwarded to
        the underlying `ttk.Text` instance.
        """
        return getattr(self._text, name)

    @property
    def text(self) -> ttk.Text:
        """Return the internal text widget.

        Returns:

            ttk.Text: The underlying text widget instance.
        """
        return self._text

    @property
    def hbar(self) -> Optional[ttk.Scrollbar]:
        """Return the internal horizontal scrollbar.

        Returns:

            Optional[ttk.Scrollbar]: The horizontal scrollbar, if created.
        """
        return self._hbar

    @property
    def vbar(self) -> Optional[ttk.Scrollbar]:
        """Return the internal vertical scrollbar.

        Returns:

            Optional[ttk.Scrollbar]: The vertical scrollbar, if created.
        """
        return self._vbar

    def hide_scrollbars(self, *args: Any) -> None:
        """Hide the scrollbars."""
        try:
            self._vbar.lower(self._text)
        except:
            pass
        try:
            self._hbar.lower(self._text)
        except:
            pass

    def show_scrollbars(self, *args: Any) -> None:
        """Show the scrollbars."""
        try:
            self._vbar.lift(self._text)
        except:
            pass
        try:
            self._hbar.lift(self._text)
        except:
            pass

    def autohide_scrollbar(self, *args: Any) -> None:
        """Show the scrollbars when the mouse enters the widget frame,
        and hide when it leaves the frame."""
        self.bind("<Enter>", self.show_scrollbars)
        self.bind("<Leave>", self.hide_scrollbars)


class ScrolledFrame(ttk.Frame):
    """A widget container with a vertical scrollbar.

    The ScrolledFrame fills the width with its container. The height is
    either set explicitly or is determined by the content frame's
    contents.

    This widget behaves mostly like a normal frame other than the
    exceptions stated already. Another exception is when packing it
    into a Notebook or Panedwindow. In this case, you'll need to add
    the container instead of the content frame. For example,
    `mynotebook.add(myscrolledframe.container)`.

    The scrollbar has an autohide feature that can be turned on by
    setting `autohide=True`.

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
        ```"""

    def __init__(
            self,
            master: Optional[tkinter.Misc] = None,
            padding: int = 2,
            bootstyle: str = DEFAULT,
            autohide: bool = False,
            height: int = 200,
            width: int = 300,
            scrollheight: Optional[int] = None,
            **kwargs: Any,
    ) -> None:
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
                The height of the container frame in screen units.

            width (int):
                The width of the container frame in screen units.

            scrollheight (int):
                The height of the content frame in screen units. If None,
                the height is determined by the frame contents.

            **kwargs (dict[str, Any]):
                Other keyword arguments passed to the content frame.
        """
        # content frame container
        self.container: ttk.Frame = ttk.Frame(
            master=master,
            relief=FLAT,
            borderwidth=0,
            width=width,
            height=height,
        )
        self.container.bind("<Configure>", lambda _: self.yview())
        self.container.propagate(False)

        # content frame
        super().__init__(
            master=self.container,
            padding=padding,
            bootstyle=bootstyle.replace('round', ''),
            width=width,
            height=height,
            **kwargs,
        )
        self.place(rely=0.0, relwidth=1.0, height=scrollheight)

        # vertical scrollbar
        self.vscroll: ttk.Scrollbar = ttk.Scrollbar(
            master=self.container,
            command=self.yview,
            orient=VERTICAL,
            bootstyle=bootstyle,
        )
        self.vscroll.pack(side=RIGHT, fill=Y)

        self.winsys: str = self.tk.call("tk", "windowingsystem")

        # setup autohide scrollbar
        self.autohide: bool = autohide
        if self.autohide:
            self.hide_scrollbars()

        # widget event binding
        self.container.bind("<Enter>", self._on_enter, "+")
        self.container.bind("<Leave>", self._on_leave, "+")
        self.container.bind("<Map>", self._on_map, "+")
        self.bind("<<MapChild>>", self._on_map_child, "+")

        # delegate content geometry methods to container frame
        # exclude configuration methods that should apply to content frame
        _exclude = {
            "grid_columnconfigure", "grid_rowconfigure", "grid_bbox",
            "grid_location", "grid_propagate", "grid_size",
            "grid_slaves", "grid_content",  # grid_slaves renamed to grid_content in newer tk
            "pack_propagate", "pack_slaves", "pack_content",
            "place_slaves", "place_content"
        }
        _methods = vars(Pack).keys() | vars(Grid).keys() | vars(Place).keys()
        for method in _methods:
            if any(["pack" in method, "grid" in method, "place" in method]):
                if method in _exclude:
                    # keep these methods pointing to the content frame
                    continue
                # prefix content frame methods with 'content_'
                setattr(self, f"content_{method}", getattr(self, method))
                # overwrite content frame methods from container frame
                setattr(self, method, getattr(self.container, method))

    def yview(self, *args: Any) -> None:
        """Update the vertical position of the content frame within the
        container.

        Parameters:

            *args (list[Any, ...]):
                Optional arguments passed to yview in order to move the
                content frame within the container frame.
        """
        if not args:
            first, _ = self.vscroll.get()
            self.yview_moveto(fraction=first)
        elif args[0] == "moveto":
            self.yview_moveto(fraction=float(args[1]))
        elif args[0] == "scroll":
            self.yview_scroll(number=int(args[1]), what=args[2])
        else:
            return

    def yview_moveto(self, fraction: float) -> None:
        """Update the vertical position of the content frame within the
        container.

        Parameters:

            fraction (float):
                The relative position of the content frame within the
                container.
        """
        base, thumb = self._measures()
        if fraction < 0:
            first = 0.0
        elif (fraction + thumb) > 1:
            first = 1 - thumb
        else:
            first = fraction
        self.vscroll.set(first, first + thumb)
        self.content_place(rely=-first * base)

    def yview_scroll(self, number: int, what: str) -> None:
        """Update the vertical position of the content frame within the
        container.

        Parameters:

            number (int):
                The amount by which the content frame will be moved
                within the container frame by 'what' units.

            what (str):
                The type of units by which the number is to be interpeted.
                This parameter is currently not used and is assumed to be
                'units'.
        """
        first, _ = self.vscroll.get()
        fraction = (number / 100) + first
        self.yview_moveto(fraction)

    def _add_scroll_binding(self, parent: tkinter.Misc) -> None:
        """Recursive adding of scroll binding to all descendants."""
        children = parent.winfo_children()
        for widget in [parent, *children]:
            bindings = widget.bind()
            if self.winsys.lower() == "x11":
                if "<Button-4>" in bindings or "<Button-5>" in bindings:
                    continue
                else:
                    widget.bind("<Button-4>", self._on_mousewheel, "+")
                    widget.bind("<Button-5>", self._on_mousewheel, "+")
            else:
                if "<MouseWheel>" not in bindings:
                    widget.bind("<MouseWheel>", self._on_mousewheel, "+")
            if widget.winfo_children() and widget != parent:
                self._add_scroll_binding(widget)

    def _del_scroll_binding(self, parent: tkinter.Misc) -> None:
        """Recursive removal of scrolling binding for all descendants"""
        children = parent.winfo_children()
        for widget in [parent, *children]:
            if self.winsys.lower() == "x11":
                widget.unbind("<Button-4>")
                widget.unbind("<Button-5>")
            else:
                widget.unbind("<MouseWheel>")
            if widget.winfo_children() and widget != parent:
                self._del_scroll_binding(widget)

    def enable_scrolling(self) -> None:
        """Enable mousewheel scrolling on the frame and all of its
        children."""
        self._add_scroll_binding(self)

    def disable_scrolling(self) -> None:
        """Disable mousewheel scrolling on the frame and all of its
        children."""
        self._del_scroll_binding(self)

    def hide_scrollbars(self) -> None:
        """Hide the scrollbars."""
        self.vscroll.pack_forget()

    def show_scrollbars(self) -> None:
        """Show the scrollbars."""
        self.vscroll.pack(side=RIGHT, fill=Y)

    def autohide_scrollbar(self) -> None:
        """Toggle the autohide funtionality. Show the scrollbars when
        the mouse enters the widget frame, and hide when it leaves the
        frame."""
        self.autohide = not self.autohide

    def destroy(self) -> None:
        super().destroy()

    def _measures(self) -> Tuple[float, float]:
        """Measure the base size of the container and the thumb size
        for use in the yview methods"""
        outer = self.container.winfo_height()
        inner = max([self.winfo_height(), outer])
        base = inner / outer
        if inner == outer:
            thumb = 1.0
        else:
            thumb = outer / inner
        return base, thumb

    def _on_map_child(self, event: tkinter.Event) -> None:
        """Callback for when a widget is mapped to the content frame."""
        if self.container.winfo_ismapped():
            self.yview()

    def _on_enter(self, event: tkinter.Event) -> None:
        """Callback for when the mouse enters the widget."""
        self.enable_scrolling()
        if self.autohide:
            self.show_scrollbars()

    def _on_leave(self, event: tkinter.Event) -> None:
        """Callback for when the mouse leaves the widget."""
        self.disable_scrolling()
        if self.autohide:
            self.hide_scrollbars()

    def _on_configure(self, event: tkinter.Event) -> None:
        """Callback for when the widget is configured"""
        self.yview()

    def _on_map(self, event: tkinter.Event) -> None:
        self.yview()

    def _on_mousewheel(self, event: tkinter.Event) -> None:
        """Callback for when the mouse wheel is scrolled."""
        delta = 0
        if self.winsys.lower() == "win32":
            delta = -int(event.delta / 120)
        elif self.winsys.lower() == "aqua":
            delta = -event.delta
        elif event.num == 4:
            delta = -10
        elif event.num == 5:
            delta = 10
        self.yview_scroll(delta, UNITS)

    # Statically declare dynamically-assigned geometry helpers for type checkers
    content_pack: Callable[..., Any]
    content_grid: Callable[..., Any]
    content_place: Callable[..., Any]
