from typing import Literal
from ttkbootstrap.ttk_types import StyleColor
from ttkbootstrap.widgets.frame import Frame
from ttkbootstrap.widgets.scrollbar import Scrollbar
from tkinter import Pack, Grid, Place


class ScrolledFrame(Frame):
    """A themed vertically scrollable frame with an optional autohiding scrollbar.

    This widget behaves like a standard frame but includes a vertical `Scrollbar`
    for navigating its contents when they exceed the visible region. It supports
    automatic scrollbar hiding, mousewheel scrolling, and layout method delegation
    for use in any geometry manager (`pack`, `grid`, or `place`).

    Use `content_pack()`, `content_grid()`, or `content_place()` to lay out widgets
    inside the scrollable region.

    Example:
        >>> from ttkbootstrap.widgets import ScrolledFrame
        >>> sf = ScrolledFrame(root, autohide=True)
        >>> sf.pack(fill="both", expand=True)
        >>> ttk.Label(sf, text="Scrollable content").pack()

    Attributes:
        container (Frame): The outer wrapper that contains the scrollable content.
        vscroll (Scrollbar): The vertical scrollbar instance.
        autohide (bool): Whether the scrollbar is hidden unless hovered.
        winsys (str): The detected windowing system ("win32", "x11", "aqua", etc.).
    """

    def __init__(
        self,
        master=None,
        padding=2,
        color: StyleColor = "default",
        variant: Literal["default", "round"] = "default",
        autohide=False,
        height=200,
        width=300,
        scrollheight=None,
        **kwargs,
    ):
        """Initialize a ScrolledFrame widget.

        Args:
            master (Misc, optional): The parent container.
            padding (int): Padding applied to the inner content frame.
            color (StyleColor): Scrollbar color token (e.g., "primary").
            variant (str): Scrollbar visual variant: "default" or "round".
            autohide (bool): If True, scrollbar only appears when hovered.
            height (int): Height of the outer container frame.
            width (int): Width of the outer container frame.
            scrollheight (int, optional): Height of the scrollable area; if None, auto-determined.
            **kwargs: Additional keyword arguments passed to the inner frame.
        """
        self.container = Frame(master, relief="flat", borderwidth=0, width=width, height=height)
        self.container.bind("<Configure>", lambda _: self.yview())
        self.container.propagate(False)

        super().__init__(self.container, padding=padding, color=color, width=width, height=height, **kwargs)
        self.place(rely=0.0, relwidth=1.0, height=scrollheight)

        self.vscroll = Scrollbar(self.container, command=self.yview, orient="vertical", color=color, variant=variant)
        self.vscroll.pack(side="right", fill="y")

        self.winsys = self.tk.call("tk", "windowingsystem")
        self.autohide = autohide
        if self.autohide:
            self.hide_scrollbars()

        self.container.bind("<Enter>", self._on_enter, "+")
        self.container.bind("<Leave>", self._on_leave, "+")
        self.container.bind("<Map>", self._on_map, "+")
        self.bind("<<MapChild>>", self._on_map_child, "+")

        methods = vars(Pack).keys() | vars(Grid).keys() | vars(Place).keys()
        for method in methods:
            if any(x in method for x in ("pack", "grid", "place")):
                setattr(self, f"content_{method}", getattr(self, method))
                setattr(self, method, getattr(self.container, method))

    def yview(self, *args):
        """Callback for the scrollbar to control vertical position.

        Args:
            *args: Supports standard scrollbar command formats:
                - no args: sync from scrollbar
                - ("moveto", fraction): jump to fraction
                - ("scroll", number, "units"): scroll by step
        """
        if not args:
            first, _ = self.vscroll.get()
            self.yview_moveto(first)
        elif args[0] == "moveto":
            self.yview_moveto(float(args[1]))
        elif args[0] == "scroll":
            self.yview_scroll(int(args[1]), args[2])

    def yview_moveto(self, fraction: float):
        """Scroll to a given vertical position.

        Args:
            fraction (float): Fraction between 0.0 and 1.0.
        """
        base, thumb = self._measures()
        first = max(0.0, min(1 - thumb, fraction))
        self.vscroll.set(first, first + thumb)

    def yview_scroll(self, number: int, _):
        """Scroll the view by a number of steps.

        Args:
            number (int): The number of scroll steps (positive or negative).
            _ (str): Unused parameter from standard scrollbar command.
        """
        first, _ = self.vscroll.get()
        self.yview_moveto(first + number / 100)

    def enable_scrolling(self):
        """Enable mousewheel scrolling for this frame and all descendants."""
        self._add_scroll_binding(self)

    def disable_scrolling(self):
        """Disable mousewheel scrolling for this frame and all descendants."""
        self._del_scroll_binding(self)

    def hide_scrollbars(self):
        """Hide the vertical scrollbar."""
        self.vscroll.pack_forget()

    def show_scrollbars(self):
        """Show the vertical scrollbar."""
        self.vscroll.pack(side="right", fill="y")

    def autohide_scrollbar(self):
        """Toggle the autohide behavior of the scrollbar."""
        self.autohide = not self.autohide

    def destroy(self):
        """Destroy the scrollbar, internal frame, and container."""
        self.vscroll.destroy()
        super().destroy()
        self.container.destroy()

    def _measures(self):
        """Internal: calculate proportions of content height to container height.

        Returns:
            tuple[float, float]: (base height ratio, thumb size)
        """
        outer = self.container.winfo_height()
        inner = max(self.winfo_height(), outer)
        base = inner / outer
        thumb = 1.0 if inner == outer else outer / inner
        return base, thumb

    def _on_map_child(self, _):
        if self.container.winfo_ismapped():
            self.yview()

    def _on_enter(self, _):
        self.enable_scrolling()
        if self.autohide:
            self.show_scrollbars()

    def _on_leave(self, _):
        self.disable_scrolling()
        if self.autohide:
            self.hide_scrollbars()

    def _on_configure(self, _):
        self.yview()

    def _on_map(self, _):
        self.yview()

    def _on_mousewheel(self, event):
        """Internal: Handle platform-specific mousewheel scrolling."""
        if self.winsys == "win32":
            delta = -int(event.delta / 120)
        elif self.winsys == "aqua":
            delta = -event.delta
        elif event.num == 4:
            delta = -10
        elif event.num == 5:
            delta = 10
        else:
            delta = 0
        self.yview_scroll(delta, "units")

    def _add_scroll_binding(self, parent):
        """Internal: Recursively bind mousewheel scrolling to all descendants."""
        children = parent.winfo_children()
        for widget in [parent, *children]:
            bindings = widget.bind()
            if self.winsys == "x11":
                if "<Button-4>" not in bindings:
                    widget.bind("<Button-4>", self._on_mousewheel, "+")
                if "<Button-5>" not in bindings:
                    widget.bind("<Button-5>", self._on_mousewheel, "+")
            else:
                if "<MouseWheel>" not in bindings:
                    widget.bind("<MouseWheel>", self._on_mousewheel, "+")
            if widget.winfo_children() and widget != parent:
                self._add_scroll_binding(widget)

    def _del_scroll_binding(self, parent):
        """Internal: Recursively unbind mousewheel scrolling from all descendants."""
        children = parent.winfo_children()
        for widget in [parent, *children]:
            if self.winsys == "x11":
                widget.unbind("<Button-4>")
                widget.unbind("<Button-5>")
            else:
                widget.unbind("<MouseWheel>")
            if widget.winfo_children() and widget != parent:
                self._del_scroll_binding(widget)
