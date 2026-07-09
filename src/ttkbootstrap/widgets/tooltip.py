"""Tooltip popup for ttkbootstrap.

A semi-transparent tooltip that shows text on hover and hides on leave or click.
Supports a configurable delay, mouse-following or widget-anchored positioning,
text wrapping/justification, an optional image, and live reconfiguration.
"""
import tkinter
from tkinter import Event, Misc
from typing import Any, Literal, Optional

import ttkbootstrap as ttk
from ttkbootstrap import utility
from ttkbootstrap.constants import *
from ttkbootstrap.internal.positioning import ensure_on_screen

_POSITION_TOKENS = {"top", "bottom", "left", "right", "center"}


class ToolTip:
    """A semi-transparent tooltip popup window that shows text when the
    mouse is hovering over the widget and closes when the mouse is no
    longer hovering over the widget. Clicking a mouse button will also
    close the tooltip.

    The tooltip releases itself automatically when its target widget is
    destroyed; call :meth:`destroy` to remove it explicitly. Its options can be
    changed after construction with :meth:`configure` / :meth:`cget` (or item
    access), and a currently-visible popup is reconfigured in place.

    Examples:

        ```python
        import ttkbootstrap as ttk
        from ttkbootstrap.constants import *

        app = ttk.Window()
        b1 = ttk.Button(app, text="default tooltip")
        b1.pack()

        tip = ttk.ToolTip(b1, text="This is the default style")
        tip.configure(text="Updated text")   # live reconfigure

        app.mainloop()
        ```
    """

    #: Options that :meth:`configure`/:meth:`cget` understand.
    _OPTIONS = (
        "text", "bootstyle", "position", "delay",
        "wraplength", "justify", "image", "padding",
    )

    def __init__(
            self,
            widget: Misc,
            *,
            text: str = "widget info",
            padding: int = 10,
            justify: Literal["left", "center", "right"] = "left",
            bootstyle: Optional[str] = None,
            wraplength: Optional[int] = None,
            delay: int = 250,  # milliseconds
            image: Any = None,
            position: Optional[str] = None,
            **kwargs: Any,
    ) -> None:
        """
        Parameters:

            widget (Widget):
                The tooltip window will position over this widget when
                hovering.

            text (str):
                The text to display in the tooltip window.

            padding (int):
                The padding between the text and the border of the tooltip
                (default=10).

            justify ('left', 'center', 'right'):
                How to justify multi-line tooltip text (default='left').

            bootstyle (str):
                The style to apply to the tooltip label. You can use
                any of the standard ttkbootstrap label styles.

            wraplength (int):
                The width of the tooltip window in screen units before the
                text is wrapped to the next line. By default, this will be
                a scaled factor of 300.

            delay (int):
                The delay in milliseconds before the tooltip appears on hover
                (default=250).

            image (PhotoImage):
                An optional image shown below the text in the tooltip.

            position (str):
                If provided, sets the position of the tooltip relative to the
                widget. Valid options include combinations of "left", "right",
                "top", "bottom", and "center" separated by a space, e.g.
                "top left" or "bottom right". If not provided, the tooltip is
                offset from the mouse pointer.

            **kwargs (Dict):
                Other keyword arguments passed to the `Toplevel` window.
        """
        self.widget = widget
        self.text = text
        self.padding = padding
        self.justify = justify
        self.image = image
        self.bootstyle = bootstyle
        self.wraplength = wraplength or utility.scale_size(self.widget, 300)
        self.toplevel = None
        self.delay = delay
        self.position = position.lower() if position else None
        self.id = None

        self._validate_position(self.position)

        # Toplevel options -- copy the caller's dict before mutating it.
        kwargs = dict(kwargs)
        kwargs["override_redirect"] = True
        kwargs["master"] = self.widget
        kwargs["window_type"] = "tooltip"
        if "alpha" not in kwargs:
            kwargs["alpha"] = 0.95
        self.toplevel_kwargs = kwargs

        # the live popup label, held so a visible tooltip can be reconfigured
        self._label: Optional[ttk.Label] = None

        # event binding -- add="+" so a second ToolTip (or the user's own
        # handlers) are not silently clobbered; keep the funcids to unbind them
        # in destroy().
        self._funcids: dict = {}
        for seq, handler in (
            ("<Enter>", self.enter),
            ("<Leave>", self.leave),
            ("<Motion>", self.move_tip),
            ("<ButtonPress>", self.leave),
        ):
            self._funcids[seq] = self.widget.bind(seq, handler, add="+")
        # release ourselves when the target widget is destroyed
        self._destroy_funcid = self.widget.bind(
            "<Destroy>", self._on_widget_destroy, add="+"
        )

    # -- validation ---------------------------------------------------------- #
    @staticmethod
    def _validate_position(position: Optional[str]) -> None:
        if position and not all(p in _POSITION_TOKENS for p in position.split()):
            raise ValueError(f"Invalid position string: '{position}'")

    # -- scheduling ---------------------------------------------------------- #
    def enter(self, event: Optional[Event] = None) -> None:
        self.schedule()

    def leave(self, event: Optional[Event] = None) -> None:
        self.unschedule()
        self.hide_tip()

    def schedule(self) -> None:
        self.unschedule()
        self.id = self.widget.after(self.delay, self.show_tip)

    def unschedule(self) -> None:
        _id = self.id
        self.id = None
        if _id:
            try:
                self.widget.after_cancel(_id)
            except (ValueError, tkinter.TclError):
                pass

    # -- show / hide --------------------------------------------------------- #
    def show_tip(self, *_: Any) -> None:
        """Create and show the tooltip window."""
        if self.toplevel:
            return
        # An orphaned timer can fire after the widget is gone -- no-op then.
        try:
            if not self.widget.winfo_exists():
                return
        except tkinter.TclError:
            return

        # Create the tooltip window at a temporary position
        self.toplevel = ttk.window.Toplevel(position=(0, 0), **self.toplevel_kwargs)
        self.toplevel.withdraw()

        self._label = ttk.Label(
            master=self.toplevel,
            text=self.text,
            image=self.image,
            compound='bottom',
            justify=self.justify,
            wraplength=self.wraplength,
            padding=self.padding,
        )
        self._label.pack(fill=BOTH, expand=YES)
        self._apply_label_style()

        # Wait until size is known, then position
        self.toplevel.update_idletasks()
        self._place()
        self.toplevel.deiconify()

    def move_tip(self, *_: Any) -> None:
        """Move the tooltip window to track the pointer/anchor."""
        if self.toplevel:
            self._place()

    def hide_tip(self, *_: Any) -> None:
        """Destroy the tooltip window (the target widget stays)."""
        if self.toplevel:
            try:
                self.toplevel.destroy()
            except tkinter.TclError:
                pass
            self.toplevel = None
            self._label = None

    # -- lifecycle ----------------------------------------------------------- #
    def _on_widget_destroy(self, event: Event) -> None:
        # Ignore the <Destroy> of child widgets bubbling up.
        if event.widget is self.widget:
            self.destroy()

    def destroy(self) -> None:
        """Release the tooltip: cancel timers, drop the popup, unbind handlers.

        Idempotent and safe to call from the target widget's ``<Destroy>``.
        """
        self.unschedule()
        self.hide_tip()
        for seq, funcid in list(self._funcids.items()):
            try:
                self.widget.unbind(seq, funcid)
            except tkinter.TclError:
                pass
        self._funcids.clear()
        if self._destroy_funcid is not None:
            try:
                self.widget.unbind("<Destroy>", self._destroy_funcid)
            except tkinter.TclError:
                pass
            self._destroy_funcid = None

    # -- configure / cget ---------------------------------------------------- #
    def configure(self, cnf: Any = None, **kwargs: Any) -> Any:
        """Query or set tooltip options.

        With a single option name and no keyword arguments, returns that
        option's value (like :meth:`cget`). Otherwise applies the given
        options; a currently-visible popup is reconfigured in place.
        """
        if cnf is not None and not kwargs and isinstance(cnf, str):
            return self.cget(cnf)
        if isinstance(cnf, dict):
            kwargs = {**cnf, **kwargs}
        for key, value in kwargs.items():
            if key not in self._OPTIONS:
                raise ValueError(f"unknown tooltip option: {key!r}")
            if key == "position":
                value = value.lower() if value else None
                self._validate_position(value)
            setattr(self, key, value)
        if kwargs:
            self._reconfigure_live()
        return None

    config = configure

    def cget(self, key: str) -> Any:
        """Return the value of a tooltip option."""
        if key not in self._OPTIONS:
            raise ValueError(f"unknown tooltip option: {key!r}")
        return getattr(self, key)

    def __getitem__(self, key: str) -> Any:
        return self.cget(key)

    def __setitem__(self, key: str, value: Any) -> None:
        self.configure(**{key: value})

    # -- placement / styling helpers ----------------------------------------- #
    def _apply_label_style(self) -> None:
        if self._label is None:
            return
        if self.bootstyle:
            self._label.configure(bootstyle=self.bootstyle)
        else:
            self._label.configure(style="tooltip.TLabel")

    def _reconfigure_live(self) -> None:
        """Push option changes onto a visible popup (no-op when hidden)."""
        if not self.toplevel or self._label is None:
            return
        try:
            self._label.configure(
                text=self.text,
                image=self.image,
                justify=self.justify,
                wraplength=self.wraplength,
                padding=self.padding,
            )
            self._apply_label_style()
            self.toplevel.update_idletasks()
            self._place()
        except tkinter.TclError:
            pass

    def _place(self) -> None:
        """Position the popup, clamped to the monitor it lands on."""
        if not self.toplevel:
            return
        if self.position:
            x, y = self._calculate_position()
        else:
            x = self.widget.winfo_pointerx() + 25
            y = self.widget.winfo_pointery() + 10
        # A tooltip has no titlebar; clamp so it stays fully on-screen.
        x, y = ensure_on_screen(self.toplevel, x, y, padding=8, titlebar_height=0)
        self.toplevel.geometry(f"+{x}+{y}")

    def _calculate_position(self) -> tuple[int, int]:
        w = self.widget
        self.toplevel.update_idletasks()
        tip_w = self.toplevel.winfo_reqwidth()
        tip_h = self.toplevel.winfo_reqheight()

        widget_x = w.winfo_rootx()
        widget_y = w.winfo_rooty()
        widget_w = w.winfo_width()
        widget_h = w.winfo_height()

        horiz = "center"
        vert = "bottom"
        for token in self.position.split():
            if token in ("top", "bottom", "center"):
                vert = token
            if token in ("left", "right", "center"):
                horiz = token

        # Vertical positioning
        if vert == "top":
            y = widget_y - tip_h - 4
        elif vert == "bottom":
            y = widget_y + widget_h + 4
        else:  # center
            y = widget_y + (widget_h // 2) - (tip_h // 2)

        # Horizontal positioning
        if horiz == "left":
            x = widget_x - tip_w - 4
        elif horiz == "right":
            x = widget_x + widget_w + 4
        else:  # center
            x = widget_x + (widget_w // 2) - (tip_w // 2)

        return x, y