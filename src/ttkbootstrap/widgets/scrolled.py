"""Scrolling widgets with optional autohide scrollbars for ttkbootstrap.

This module provides enhanced scrolling widgets that wrap standard tkinter
and ttk widgets with automatic scrollbar management. The scrollbars can be
configured to auto-hide when the mouse is not over the widget.

Classes:
    ScrolledText: Text widget with vertical/horizontal scrollbars
    ScrolledFrame: Frame container with a vertical scrollbar (Canvas viewport)

Features:
    - Optional auto-hide scrollbars (hide when the mouse leaves the widget)
    - Configurable vertical and horizontal scrollbars
    - Seamless delegation of widget methods
    - Bootstrap styling support via the bootstyle parameter

Example:
    ```python
    import ttkbootstrap as ttk
    from ttkbootstrap.constants import *

    app = ttk.Window()

    # Scrolled text with an auto-hide scrollbar
    st = ttk.ScrolledText(app, padding=5, height=10, auto_hide=True)
    st.pack(fill=BOTH, expand=YES)
    st.insert(END, 'Insert your text here.')

    # Scrolled frame for multiple widgets
    sf = ttk.ScrolledFrame(app, auto_hide=True)
    sf.pack(fill=BOTH, expand=YES, padx=10, pady=10)
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
from ttkbootstrap.internal.configure_delegation import ConfigureDelegationMixin
from ttkbootstrap.style._compat import normalize_scrolled_kwargs


class ScrolledText(ConfigureDelegationMixin, ttk.Frame):
    """A text widget with optional vertical and horizontal scrollbars.

    Setting `auto_hide=True` will cause the scrollbars to hide when the
    mouse is not over the widget. The vertical scrollbar is on by
    default, but can be turned off. The horizontal scrollbar can be
    enabled by setting `hbar=True`.

    This widget is identical in configuration to the `Text` widget other
    than the scrolling frame; `configure`/`cget` and unknown method access
    are delegated to the internal `Text`. https://tcl.tk/man/tcl8.6/TkCmd/text.htm

    ![scrolled text](../../../assets/scrolled/scrolledtext.gif)

    Examples:

        ```python
        import ttkbootstrap as ttk
        from ttkbootstrap.constants import *

        app = ttk.Window()

        # scrolled text with an auto-hide vertical scrollbar
        st = ttk.ScrolledText(app, padding=5, height=10, auto_hide=True)
        st.pack(fill=BOTH, expand=YES)
        st.insert(END, 'Insert your text here.')

        app.mainloop()
        ```
    """

    def __init__(
            self,
            master: Optional[tkinter.Misc] = None,
            *,
            padding: int = 2,
            bootstyle: str = DEFAULT,
            auto_hide: bool = False,
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
                scrollbars. Available options include -> primary,
                secondary, success, info, warning, danger, dark, light.

            auto_hide (bool):
                When **True**, the scrollbars hide when the mouse is not
                within the frame.

            vbar (bool):
                A vertical scrollbar is shown when **True** (default).

            hbar (bool):
                A horizontal scrollbar is shown when **True**. Turning
                on this scrollbar will also set `wrap="none"`. This
                scrollbar is _off_ by default.

            **kwargs (dict[str, Any]):
                Other keyword arguments passed to the `Text` widget.
        """
        # Accept the pre-2.0 `autohide` spelling (warn-and-normalize).
        aliases = normalize_scrolled_kwargs(kwargs)
        auto_hide = aliases.get("auto_hide", auto_hide)

        super().__init__(master, padding=padding)

        # a grid layout keeps the text + bars aligned with a stable gutter,
        # which removes the old place()/relwidth math (and its hbar-without-vbar
        # AttributeError).
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self._text: ttk.Text = ttk.Text(self, padx=50, **kwargs)
        self._hbar: Optional[ttk.Scrollbar] = None
        self._vbar: Optional[ttk.Scrollbar] = None
        self._auto_hide = auto_hide

        self._text.grid(row=0, column=0, sticky=NSEW)

        if vbar:
            self._vbar = ttk.Scrollbar(
                master=self,
                bootstyle=bootstyle,
                command=self._text.yview,
                orient=VERTICAL,
            )
            self._vbar.grid(row=0, column=1, sticky=NS)
            self._text.configure(yscrollcommand=self._vbar.set)

        if hbar:
            self._hbar = ttk.Scrollbar(
                master=self,
                bootstyle=bootstyle,
                command=self._text.xview,
                orient=HORIZONTAL,
            )
            self._hbar.grid(row=1, column=0, sticky=EW)
            self._text.configure(xscrollcommand=self._hbar.set, wrap="none")

        if self._auto_hide:
            self._enable_auto_hide()
            self.hide_scrollbars()

    # -- configure/cget delegation ------------------------------------------- #
    def _configure_delegate_target(self):
        """Route non-delegated configure/cget options to the inner Text.

        A ScrolledText is "a Text with scrollbars", so `st.configure(font=...)`
        / `st.cget("wrap")` reach the Text instead of the wrapper Frame.
        """
        return self._text

    def __getattr__(self, name: str) -> Any:
        """Delegate unknown attribute/method access to the internal Text widget.

        Only invoked when normal lookup (including the mixin's methods) fails,
        so `insert`/`get`/`see`/`tag_configure`/... reach the `Text`.
        """
        if name == "_text":
            # Accessed before _text is assigned -- avoid infinite recursion.
            raise AttributeError(name)
        return getattr(self._text, name)

    @property
    def text(self) -> ttk.Text:
        """Return the internal text widget."""
        return self._text

    @property
    def hbar(self) -> Optional[ttk.Scrollbar]:
        """Return the internal horizontal scrollbar, if created."""
        return self._hbar

    @property
    def vbar(self) -> Optional[ttk.Scrollbar]:
        """Return the internal vertical scrollbar, if created."""
        return self._vbar

    @property
    def auto_hide(self) -> bool:
        """Whether the scrollbars hide when the mouse leaves the widget."""
        return self._auto_hide

    def hide_scrollbars(self, *args: Any) -> None:
        """Hide the scrollbars."""
        if self._vbar is not None:
            self._vbar.grid_remove()
        if self._hbar is not None:
            self._hbar.grid_remove()

    def show_scrollbars(self, *args: Any) -> None:
        """Show the scrollbars."""
        if self._vbar is not None:
            self._vbar.grid()
        if self._hbar is not None:
            self._hbar.grid()

    def _enable_auto_hide(self) -> None:
        self.bind("<Enter>", self.show_scrollbars)
        self.bind("<Leave>", self.hide_scrollbars)

    def _disable_auto_hide(self) -> None:
        self.unbind("<Enter>")
        self.unbind("<Leave>")
        self.show_scrollbars()

    def autohide_scrollbar(self, *args: Any) -> None:
        """Toggle the auto-hide behavior.

        When turned on, the scrollbars are shown while the mouse is over the
        widget and hidden when it leaves; when turned off, they stay visible.
        (Unified with `ScrolledFrame.autohide_scrollbar` in 2.0.)
        """
        self._auto_hide = not self._auto_hide
        if self._auto_hide:
            self._enable_auto_hide()
            self.hide_scrollbars()
        else:
            self._disable_auto_hide()


class _ScrollContainer(ttk.Frame):
    """Outer container owning the Canvas + scrollbar for a ScrolledFrame.

    Its `destroy()` sets `_tearing_down` *before* the child cascade runs, so the
    content frame's `destroy()` can tell an ancestor-driven teardown (don't
    re-destroy the container) from a direct `ScrolledFrame.destroy()` call.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self._tearing_down = False
        super().__init__(*args, **kwargs)

    def destroy(self) -> None:
        self._tearing_down = True
        super().destroy()


class ScrolledFrame(ttk.Frame):
    """A widget container with a vertical scrollbar.

    The ScrolledFrame fills the width of its container. The height is
    either set explicitly or determined by the content's contents. Add
    child widgets with the ScrolledFrame itself as the parent:

        `ttk.Checkbutton(myscrolledframe, text="...")`

    When packing it into a Notebook or Panedwindow, add the container
    instead of the content frame, e.g.
    `mynotebook.add(myscrolledframe.container)`.

    The scrollbar has an auto-hide feature turned on with `auto_hide=True`.

    Internally (2.0) the content frame is a child of a Canvas viewport, so
    scroll fractions come from the Canvas and destroying the ScrolledFrame
    tears down the whole assembly (no container leak).

    Examples:

        ```python
        import ttkbootstrap as ttk
        from ttkbootstrap.constants import *

        app = ttk.Window()

        sf = ttk.ScrolledFrame(app, auto_hide=True)
        sf.pack(fill=BOTH, expand=YES, padx=10, pady=10)

        for x in range(20):
            ttk.Checkbutton(sf, text=f"Checkbutton {x}").pack(anchor=W)

        app.mainloop()
        ```"""

    def __init__(
            self,
            master: Optional[tkinter.Misc] = None,
            *,
            padding: int = 2,
            bootstyle: str = DEFAULT,
            auto_hide: bool = False,
            height: int = 200,
            width: int = 300,
            scroll_height: Optional[int] = None,
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
                vertical scrollbar.

            auto_hide (bool):
                When **True**, the scrollbar hides when the mouse is not
                within the frame.

            height (int):
                The height of the viewport in screen units.

            width (int):
                The width of the viewport in screen units.

            scroll_height (int):
                The height of the content frame in screen units. If None,
                the height is determined by the frame contents.

            **kwargs (dict[str, Any]):
                Other keyword arguments passed to the content frame.
        """
        aliases = normalize_scrolled_kwargs(kwargs)
        auto_hide = aliases.get("auto_hide", auto_hide)
        scroll_height = aliases.get("scroll_height", scroll_height)

        self._destroying = False
        self._auto_hide = auto_hide
        # Persistent user intent (default on). Hover applies/removes the wheel
        # tag, but only re-applies it while scrolling is intended -- so
        # disable_scrolling() survives a later hover (regression #1064).
        self._scroll_enabled = True

        # outer container: Canvas viewport + vertical scrollbar in a grid
        self.container: _ScrollContainer = _ScrollContainer(
            master=master,
            relief=FLAT,
            borderwidth=0,
            width=width,
            height=height,
        )
        self.winsys: str = self.container.tk.call("tk", "windowingsystem")
        self.container.propagate(False)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self._canvas: tkinter.Canvas = ttk.Canvas(
            master=self.container,
            highlightthickness=0,
            borderwidth=0,
            width=width,
            height=height,
        )
        self._canvas.grid(row=0, column=0, sticky=NSEW)

        self.vscroll: ttk.Scrollbar = ttk.Scrollbar(
            master=self.container,
            command=self._canvas.yview,
            orient=VERTICAL,
            bootstyle=bootstyle,
        )
        self.vscroll.grid(row=0, column=1, sticky=NS)
        self._canvas.configure(yscrollcommand=self.vscroll.set)

        # content frame lives inside the canvas -> native scroll fractions +
        # native destroy cascade.
        super().__init__(
            master=self._canvas,
            padding=padding,
            bootstyle=bootstyle.replace('round', ''),
            **kwargs,
        )
        self._window_id = self._canvas.create_window(0, 0, anchor=NW, window=self)
        if scroll_height is not None:
            self._canvas.itemconfigure(self._window_id, height=scroll_height)

        # keep the scroll region + content width in sync with the viewport
        self.bind("<Configure>", self._on_content_configure, "+")
        self._canvas.bind("<Configure>", self._on_canvas_configure, "+")

        # per-instance mousewheel bind-tag (enable/disable by toggling the tag
        # in each widget's bindtags -- no O(subtree) rebinding, no clobbering
        # the app's own wheel handlers).
        self._wheel_tag = f"ScrolledFrame_{id(self)}"
        if self.winsys.lower() == "x11":
            self.bind_class(self._wheel_tag, "<Button-4>", self._on_mousewheel, "+")
            self.bind_class(self._wheel_tag, "<Button-5>", self._on_mousewheel, "+")
        else:
            self.bind_class(self._wheel_tag, "<MouseWheel>", self._on_mousewheel, "+")

        # show/enable on enter, hide/disable on leave
        self.container.bind("<Enter>", self._on_enter, "+")
        self.container.bind("<Leave>", self._on_leave, "+")

        if self._auto_hide:
            self.hide_scrollbars()

        # delegate content geometry methods to the container frame so that
        # `sf.pack()/grid()/place()` lay out the whole assembly, while the
        # content frame's own geometry stays reachable as `content_*`.
        _exclude = {
            "grid_columnconfigure", "grid_rowconfigure", "grid_bbox",
            "grid_location", "grid_propagate", "grid_size",
            "grid_slaves", "grid_content",
            "pack_propagate", "pack_slaves", "pack_content",
            "place_slaves", "place_content",
        }
        _methods = vars(Pack).keys() | vars(Grid).keys() | vars(Place).keys()
        for method in _methods:
            if any(["pack" in method, "grid" in method, "place" in method]):
                if method in _exclude:
                    continue
                setattr(self, f"content_{method}", getattr(self, method))
                setattr(self, method, getattr(self.container, method))

    # -- viewport plumbing --------------------------------------------------- #
    def _on_content_configure(self, event: tkinter.Event) -> None:
        """Recompute the scroll region when the content size changes."""
        self._canvas.configure(scrollregion=self._canvas.bbox("all"))

    def _on_canvas_configure(self, event: tkinter.Event) -> None:
        """Pin the content width to the viewport width (vertical scroll)."""
        width = max(1, event.width)
        if width <= 1:
            return
        self._canvas.itemconfigure(self._window_id, width=width)

    # -- view delegation (native canvas fractions; always returns a tuple) --- #
    def yview(self, *args: Any) -> Optional[Tuple[float, float]]:
        """Query or command the vertical view; returns `(first, last)` on query."""
        return self._canvas.yview(*args)

    def xview(self, *args: Any) -> Optional[Tuple[float, float]]:
        """Query or command the horizontal view; returns `(first, last)` on query."""
        return self._canvas.xview(*args)

    def yview_moveto(self, fraction: float) -> None:
        """Scroll so `fraction` (0.0-1.0) of the content is above the viewport."""
        self._canvas.yview_moveto(fraction)

    def yview_scroll(self, number: int, what: str = UNITS) -> None:
        """Scroll vertically by `number` of `what` (units/pages)."""
        self._canvas.yview_scroll(number, what)

    # -- mousewheel bind-tag seam -------------------------------------------- #
    def _tagged_widgets(self):
        """The canvas + the content subtree that should scroll on wheel."""
        stack = [self._canvas, self]
        seen = []
        while stack:
            w = stack.pop()
            seen.append(w)
            stack.extend(w.winfo_children())
        return seen

    def _add_scroll_binding(self) -> None:
        for widget in self._tagged_widgets():
            try:
                tags = list(widget.bindtags())
            except tkinter.TclError:
                continue
            if self._wheel_tag not in tags:
                tags.insert(1, self._wheel_tag)
                widget.bindtags(tuple(tags))

    def _del_scroll_binding(self) -> None:
        for widget in self._tagged_widgets():
            try:
                tags = list(widget.bindtags())
            except tkinter.TclError:
                continue
            if self._wheel_tag in tags:
                tags.remove(self._wheel_tag)
                widget.bindtags(tuple(tags))

    def enable_scrolling(self) -> None:
        """Enable mousewheel scrolling on the frame and all of its children."""
        self._scroll_enabled = True
        self._add_scroll_binding()

    def disable_scrolling(self) -> None:
        """Disable mousewheel scrolling on the frame and all of its children."""
        self._scroll_enabled = False
        self._del_scroll_binding()

    def _on_mousewheel(self, event: tkinter.Event) -> None:
        """Scroll the canvas vertically in response to the mouse wheel."""
        # do nothing when the content already fits (avoids capturing the wheel)
        try:
            first, last = self._canvas.yview()
            if first <= 0.0 and last >= 1.0:
                return
        except tkinter.TclError:
            pass
        if self.winsys.lower() == "win32":
            delta = -int(event.delta / 120)
        elif self.winsys.lower() == "aqua":
            delta = -event.delta
        elif event.num == 4:
            delta = -1
        elif event.num == 5:
            delta = 1
        else:
            delta = 0
        if delta:
            self._canvas.yview_scroll(delta, UNITS)

    # -- scrollbar visibility ------------------------------------------------ #
    @property
    def auto_hide(self) -> bool:
        """Whether the scrollbar hides when the mouse leaves the widget."""
        return self._auto_hide

    @property
    def vbar(self) -> ttk.Scrollbar:
        """The vertical scrollbar."""
        return self.vscroll

    @property
    def hbar(self) -> None:
        """ScrolledFrame has no horizontal scrollbar (vertical scroll only)."""
        return None

    def hide_scrollbars(self) -> None:
        """Hide the scrollbar."""
        self.vscroll.grid_remove()

    def show_scrollbars(self) -> None:
        """Show the scrollbar."""
        self.vscroll.grid()

    def autohide_scrollbar(self) -> None:
        """Toggle the auto-hide behavior.

        When turned on, the scrollbar is shown while the mouse is over the
        widget and hidden when it leaves; when turned off, it stays visible.
        (Unified with `ScrolledText.autohide_scrollbar` in 2.0.)
        """
        self._auto_hide = not self._auto_hide
        if self._auto_hide:
            self.hide_scrollbars()
        else:
            self.show_scrollbars()

    # -- events -------------------------------------------------------------- #
    def _on_enter(self, event: tkinter.Event) -> None:
        """Apply the wheel tag (re-walking for new children) while scrolling is
        intended, and show the bar when auto-hiding.

        Does NOT flip the persistent intent, so a prior ``disable_scrolling()``
        keeps the frame un-scrollable on hover (regression #1064).
        """
        if self._scroll_enabled:
            self._add_scroll_binding()
        if self._auto_hide:
            self.show_scrollbars()

    def _on_leave(self, event: tkinter.Event) -> None:
        """Remove the wheel tag and hide the bar when auto-hiding.

        Leaves the persistent intent untouched (only the current hover's tag is
        removed), so scrolling resumes on the next hover when still enabled.
        """
        self._del_scroll_binding()
        if self._auto_hide:
            self.hide_scrollbars()

    # -- teardown ------------------------------------------------------------ #
    def destroy(self) -> None:
        """Tear down the whole assembly, fixing the historical container leak.

        A direct `sf.destroy()` destroys the outer container (cascading to the
        canvas, content, and scrollbar). When an ancestor is already tearing the
        container down, `_ScrollContainer` has set `_tearing_down` first, so we
        only tear down the content frame and skip re-destroying the container.
        """
        if self._destroying:
            return super().destroy()
        self._destroying = True
        try:
            if self.winsys.lower() == "x11":
                self.unbind_class(self._wheel_tag, "<Button-4>")
                self.unbind_class(self._wheel_tag, "<Button-5>")
            else:
                self.unbind_class(self._wheel_tag, "<MouseWheel>")
        except tkinter.TclError:
            pass

        if not getattr(self.container, "_tearing_down", False):
            # direct destroy: tear down the assembly (re-enters and destroys
            # self via the cascade + the `_destroying` guard above).
            self.container.destroy()
        else:
            # ancestor cascade already handling the container: just tear down self.
            super().destroy()

    # Statically declare dynamically-assigned geometry helpers for type checkers
    content_pack: Callable[..., Any]
    content_grid: Callable[..., Any]
    content_place: Callable[..., Any]