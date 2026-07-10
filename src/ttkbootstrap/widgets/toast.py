"""Toast notification popup for ttkbootstrap.

A semi-transparent popup window for temporary alerts, anchored to a screen
corner with non-overlapping stacking of concurrent toasts, an optional
auto-close duration, a theme-aware icon, and a fade-out animation.
"""
import tkinter
from tkinter import font
from typing import Any, Optional

from ttkbootstrap.constants import *
from ttkbootstrap.style._compat import warn_deprecated

#: The valid ``position`` anchors (compass points).
_VALID_ANCHORS = {"n", "e", "s", "w", "nw", "ne", "sw", "se"}

#: Default notification glyph (a Bootstrap-Icons name). Rendered by the built-in
#: font engine so it is theme-matched and recolorable.
_DEFAULT_ICON = "bell-fill"


class _ToastStack:
    """Keeps concurrent toasts from overlapping.

    Toasts are grouped by their resolved anchor corner. Each toast is offset
    along the anchor's vertical axis by the cumulative height of the toasts
    ahead of it in that corner (plus a gap), so they stack away from the
    anchored edge -- downward for a top anchor, upward for a bottom anchor.
    Dismissing a toast removes it from its corner and reflows the rest so the
    stack closes the gap.
    """

    _GAP = 10  # logical px between stacked toasts

    def __init__(self) -> None:
        self._corners: dict = {}  # anchor(str) -> [ToastNotification, ...]

    def add(self, toast: "ToastNotification") -> None:
        self._corners.setdefault(toast._anchor, []).append(toast)

    def remove(self, toast: "ToastNotification") -> None:
        lst = self._corners.get(toast._anchor)
        if lst and toast in lst:
            lst.remove(toast)
            self._reflow(toast._anchor)

    def offset_for(self, toast: "ToastNotification") -> int:
        """Along-axis pixel offset for ``toast`` from the toasts ahead of it."""
        lst = self._corners.get(toast._anchor, [])
        offset = 0
        for other in lst:
            if other is toast:
                break
            offset += other._height + toast._scaled_gap()
        return offset

    def _reflow(self, anchor: str) -> None:
        for toast in list(self._corners.get(anchor, [])):
            toast._reposition()


#: Process-wide stack manager (one screen, shared corners).
_TOAST_STACK = _ToastStack()


class ToastNotification:
    """A semi-transparent popup window for temporary alerts or messages.
    You may choose to display the toast for a specified period of time,
    otherwise you must click the toast to close it.

    Concurrent toasts anchored to the same corner stack without overlapping and
    reflow when one is dismissed. ``show_toast()`` returns the toast so it can be
    dismissed programmatically with :meth:`hide`.

    Examples:

        ```python
        import ttkbootstrap as ttk

        app = ttk.App()

        toast = ttk.ToastNotification(
            title="ttkbootstrap toast message",
            message="This is a toast message",
            duration=3000,
        )
        handle = toast.show_toast()
        # handle.hide()   # dismiss early

        app.mainloop()
        ```
    """

    def __init__(
            self,
            title: str,
            message: str,
            *,
            duration: Optional[int] = None,
            bootstyle: str = LIGHT,
            alert: bool = False,
            icon: Optional[str] = None,
            position: Optional[tuple] = None,
            **kwargs: Any,
    ) -> None:
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
                Style keywords used to update the label style. One of the
                accepted color keywords.

            alert (bool):
                Indicates whether to ring the display bell when the toast is
                shown.

            icon (str):
                A Bootstrap-Icons glyph name (e.g. ``"bell-fill"``,
                ``"info-circle-fill"``) to show in the top-left corner. Rendered
                from the built-in icon font, so it follows the theme. Defaults
                to a bell glyph; pass an empty string to remove the icon.

            position (tuple[int, int, str]):
                A tuple ``(x, y, anchor)`` controlling the toast position.
                Default is OS specific. ``x``/``y`` are the offset of the
                toplevel relative to ``anchor``. Acceptable anchors: n, e, s, w,
                nw, ne, sw, se (e.g. ``ne`` is the top-right corner). For
                example: ``(100, 100, 'ne')``.

            **kwargs (Dict):
                Other keyword arguments passed to the `Toplevel` window.
        """
        # `iconfont`/`icon_font` are dead in 2.0 -- icons render from the
        # built-in Bootstrap-Icons font. Accept-and-warn so old calls don't blow
        # up on the unexpected keyword.
        for legacy in ("iconfont", "icon_font"):
            if legacy in kwargs:
                kwargs.pop(legacy)
                warn_deprecated(
                    f"the {legacy!r} ToastNotification option",
                    "the built-in Bootstrap-Icons font (icons render automatically)",
                )

        self.title = title
        self.message = message
        self.duration = duration
        self.bootstyle = bootstyle
        self.alert = alert
        self.icon = _DEFAULT_ICON if icon is None else icon
        self.position = position
        self.kwargs = dict(kwargs)  # copy -- we mutate this, not the caller's

        self.toplevel = None
        self.container = None
        self.title_font = None

        # lifecycle bookkeeping
        self._anchor: Optional[str] = None
        self._height: int = 0
        self._duration_id: Optional[str] = None
        self._fade_id: Optional[str] = None
        self._hidden = False

        # internal Toplevel options (snake_case -- avoid the compat shim's
        # DeprecationWarning that the old ``overrideredirect`` spelling tripped).
        if "override_redirect" not in self.kwargs:
            self.kwargs["override_redirect"] = True
        if "alpha" not in self.kwargs:
            self.kwargs["alpha"] = 0.95

        if position is not None:
            self._validate_position(position)

    # -- validation ---------------------------------------------------------- #
    @staticmethod
    def _validate_position(position: tuple) -> None:
        if len(position) != 3:
            raise ValueError(
                f"position must be a (x, y, anchor) tuple, got: {position!r}"
            )
        anchor = str(position[2]).lower()
        if anchor not in _VALID_ANCHORS:
            raise ValueError(
                f"Invalid position anchor: {position[2]!r} "
                f"(expected one of {sorted(_VALID_ANCHORS)})"
            )

    # -- show / hide --------------------------------------------------------- #
    def show_toast(self, *_: Any) -> "ToastNotification":
        """Create, place, and show the toast; returns ``self`` (a dismiss handle)."""
        from tkinter import _default_root

        from ttkbootstrap import Frame, Label, Toplevel, apply_icon, utils

        self._hidden = False

        # On aqua a borderless popup should be a 'tooltip' window type (parity
        # with the tooltip); set it at construction, so probe the windowing
        # system from the existing root before creating the Toplevel.
        if _default_root is not None and "window_type" not in self.kwargs:
            if utils.windowing_system(_default_root) == "aqua":
                self.kwargs["window_type"] = "tooltip"

        self.toplevel = Toplevel(**self.kwargs)
        self.toplevel.withdraw()
        self._setup(self.toplevel)

        self.container = Frame(self.toplevel, bootstyle=self.bootstyle)
        self.container.pack(fill=BOTH, expand=YES)

        icon_lbl = Label(
            self.container,
            bootstyle=f"{self.bootstyle}-inverse",
            anchor=NW,
        )
        icon_lbl.grid(row=0, column=0, rowspan=2, sticky=NSEW, padx=(5, 0))
        if self.icon:
            # Theme-aware glyph: follows the (inverse) label foreground and
            # re-renders on a theme switch.
            apply_icon(icon_lbl, self.icon, size=24)

        Label(
            self.container,
            text=self.title,
            font=self.title_font,
            bootstyle=f"{self.bootstyle}-inverse",
            anchor=NW,
        ).grid(row=0, column=1, sticky=NSEW, padx=10, pady=(5, 0))
        Label(
            self.container,
            text=self.message,
            wraplength=utils.scale_size(self.toplevel, 300),
            bootstyle=f"{self.bootstyle}-inverse",
            anchor=NW,
        ).grid(row=1, column=1, sticky=NSEW, padx=10, pady=(0, 5))

        self.toplevel.bind("<ButtonPress>", self.hide)

        # measure the on-screen height (valid even while withdrawn) BEFORE
        # placing, so the stack offset is correct and there is no reposition
        # flash. The toast is floored to its `minsize`, so the height it actually
        # occupies is the larger of the requested and minimum heights; using
        # reqheight alone undershoots and the stacked toasts overlap.
        self.toplevel.update_idletasks()
        self._height = max(
            self.toplevel.winfo_reqheight(), self.toplevel.minsize()[1]
        )

        _TOAST_STACK.add(self)
        self._reposition()
        self.toplevel.deiconify()

        if self.alert:
            self.toplevel.bell()
        if self.duration:
            self._duration_id = self.toplevel.after(self.duration, self.hide)
        return self

    def hide(self, *_: Any) -> None:
        """Dismiss the toast (idempotent, safe if never shown).

        Removes the toast from its corner stack (reflowing the rest so they
        close the gap), then fades out and destroys the window.
        """
        if self._hidden:
            return
        self._hidden = True

        if self._duration_id is not None:
            self._cancel(self._duration_id)
            self._duration_id = None

        # reflow the siblings first so they slide up while this one fades
        _TOAST_STACK.remove(self)

        if self.toplevel is None:
            return
        self._fade_out()

    #: Back-compat alias for :meth:`hide`.
    def hide_toast(self, *_: Any) -> None:
        self.hide()

    def _fade_out(self) -> None:
        if self.toplevel is None:
            return
        try:
            if not self.toplevel.winfo_exists():
                return self._finalize()
            alpha = float(self.toplevel.attributes("-alpha"))
            if alpha <= 0.1:
                self._finalize()
            else:
                self.toplevel.attributes("-alpha", alpha - 0.1)
                self._fade_id = self.toplevel.after(25, self._fade_out)
        except tkinter.TclError:
            self._finalize()

    def _finalize(self) -> None:
        """Cancel the fade timer and destroy the window; drop the handles."""
        if self._fade_id is not None:
            self._cancel(self._fade_id)
            self._fade_id = None
        if self.toplevel is not None:
            try:
                self.toplevel.destroy()
            except tkinter.TclError:
                pass
        self.toplevel = None
        self.container = None

    def _cancel(self, after_id: str) -> None:
        try:
            if self.toplevel is not None:
                self.toplevel.after_cancel(after_id)
        except (tkinter.TclError, ValueError):
            pass

    # -- setup / geometry ---------------------------------------------------- #
    def _setup(self, window) -> None:
        from ttkbootstrap import utils

        winsys = utils.windowing_system(window)
        self.toplevel.configure(relief=RAISED)

        if "minsize" not in self.kwargs:
            w, h = utils.scale_size(self.toplevel, [300, 75])
            self.toplevel.minsize(w, h)

        # heading font
        _font = font.nametofont("TkDefaultFont")
        self.title_font = font.Font(
            family=_font["family"],
            size=_font["size"] + 1,
            weight="bold",
        )

        # default position by windowing system
        if self.position is None:
            if winsys == "win32":
                x, y = utils.scale_size(self.toplevel, [5, 50])
                self.position = (x, y, SE)
            elif winsys == "x11":
                x, y = utils.scale_size(self.toplevel, [0, 0])
                self.position = (x, y, SE)
            else:  # aqua (window_type='tooltip' was set at construction)
                x, y = utils.scale_size(self.toplevel, [50, 50])
                self.position = (x, y, NE)

        self._anchor = str(self.position[-1]).lower()

    def _scaled_gap(self) -> int:
        from ttkbootstrap import utils
        try:
            return utils.scale_size(self.toplevel, _ToastStack._GAP)
        except Exception:
            return _ToastStack._GAP

    def _reposition(self) -> None:
        """Place the toast at its anchored position plus its stack offset."""
        if self.toplevel is None:
            return
        try:
            offset = _TOAST_STACK.offset_for(self)
            self.toplevel.geometry(self._compute_geometry(offset))
        except tkinter.TclError:
            pass

    def _compute_geometry(self, offset: int) -> str:
        tl = self.toplevel
        tl.update_idletasks()  # actualize the requested geometry
        anchor = self._anchor
        x_anchor = "+" if "w" in anchor else "-"
        y_anchor = "+" if "n" in anchor else "-"

        screen_w = tl.winfo_screenwidth() // 2
        screen_h = tl.winfo_screenheight() // 2
        top_w = tl.winfo_reqwidth() // 2
        top_h = tl.winfo_reqheight() // 2

        if "e" not in anchor and "w" not in anchor:
            xpos = screen_w - top_w
        else:
            xpos = self.position[0]
        if "n" not in anchor and "s" not in anchor:
            ypos = screen_h - top_h
        else:
            ypos = self.position[1]

        # the stack offset moves the toast away from its anchored edge
        ypos += offset
        return f"{x_anchor}{xpos}{y_anchor}{ypos}"