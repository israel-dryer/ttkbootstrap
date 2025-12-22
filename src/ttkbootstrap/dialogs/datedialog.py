"""Dialog wrapper around the Calendar widget.

Exposes a chrome-less, popover-capable date picker dialog that can close on
outside clicks and forwards Calendar options (disabled dates, bounds, etc.).
"""

from __future__ import annotations

import tkinter
from datetime import date, datetime
from types import SimpleNamespace
from typing import Any, Callable, Iterable, Literal, Optional, Tuple, Union
from tkinter import Widget

from ttkbootstrap.widgets.primitives import Frame
from ttkbootstrap.constants import BOTH, PRIMARY, YES
from ttkbootstrap.dialogs.dialog import Dialog
from ttkbootstrap.runtime.window_utilities import AnchorPoint
from ttkbootstrap.widgets.composites.calendar import Calendar

ttk = SimpleNamespace(Frame=Frame)

__all__ = ["DateDialog"]


class _ChromeDialog(Dialog):
    """Dialog that can optionally hide window chrome via override-redirect."""

    def __init__(self, *args: Any, hide_window_chrome: bool = False, **kwargs: Any) -> None:
        self._hide_window_chrome = hide_window_chrome
        self._suppress_focus_out = False
        self._outside_click_binding: str | None = None
        super().__init__(*args, **kwargs)

    def _create_toplevel(self):
        super()._create_toplevel()
        if self._hide_window_chrome and self._toplevel:
            try:
                self._toplevel.overrideredirect(True)
            except Exception:
                pass

    def show(
            self,
            position: Optional[Tuple[int, int]] = None,
            modal: Optional[bool] = None,
            *,
            anchor_to: Optional[Union[Widget, Literal["screen", "cursor", "parent"]]] = None,
            anchor_point: AnchorPoint = 'center',
            window_point: AnchorPoint = 'center',
            offset: Tuple[int, int] = (0, 0),
            auto_flip: Union[bool, Literal['vertical', 'horizontal']] = False
    ):
        """Override show to position before deiconify, avoiding placement flash.

        Args:
            position: Optional (x, y) coordinates to position the dialog.
            modal: Override the mode's default modality.
            anchor_to: Positioning target (Widget, "screen", "cursor", "parent", or None).
            anchor_point: Point on the anchor target (n, s, e, w, ne, nw, se, sw, center).
            window_point: Point on the dialog window (n, s, e, w, ne, nw, se, sw, center).
            offset: Additional (x, y) offset in pixels from the anchor position.
            auto_flip: Smart positioning to keep window on screen.
        """
        if modal is None:
            modal = (self._mode == "modal")

        self.result = None
        self._create_toplevel()
        if self._hide_window_chrome and self._toplevel:
            self._toplevel.withdraw()

        self._build_content()
        self._build_footer()

        self._position_dialog(
            position=position,
            anchor_to=anchor_to,
            anchor_point=anchor_point,
            window_point=window_point,
            offset=offset,
            auto_flip=auto_flip
        )

        if self._hide_window_chrome and self._toplevel:
            self._toplevel.deiconify()
            try:
                self._toplevel.lift()
                self._toplevel.focus_force()
            except Exception:
                pass

        if self._alert:
            self._toplevel.bell()

        if self._mode == "popover":
            self._suppress_focus_out = True
            self._toplevel.bind("<FocusOut>", self._on_focus_out, add="+")
            try:
                self._toplevel.after(50, lambda: setattr(self, "_suppress_focus_out", False))
            except Exception:
                self._suppress_focus_out = False
            self._bind_outside_click()

        if modal:
            self._toplevel.transient(self._master)
            if self._mode == "modal":
                self._toplevel.grab_set()
            self._master.wait_window(self._toplevel)

    def _on_focus_out(self, event: tkinter.Event):
        if self._suppress_focus_out:
            return
        return super()._on_focus_out(event)

    def _bind_outside_click(self) -> None:
        """Close popover when clicking outside the toplevel."""
        if not self._toplevel:
            return

        def handler(event: tkinter.Event) -> None:
            widget = getattr(event, "widget", None)
            if widget is None:
                return

            # Walk up the widget hierarchy to check if any parent is the toplevel
            current = widget
            toplevel_str = str(self._toplevel)
            while current:
                current_str = str(current)
                if current_str == toplevel_str or current_str.startswith(toplevel_str + "."):
                    return
                try:
                    current = current.master
                except AttributeError:
                    break

            # Schedule destroy for after current event processing completes
            # This allows button commands inside the dialog to execute first
            try:
                if self._toplevel.winfo_exists():
                    self._toplevel.after_idle(lambda: self._destroy_if_exists())
            except Exception:
                pass

        try:
            self._outside_click_binding = self._toplevel.bind_all("<ButtonPress-1>", handler, add="+")
            self._toplevel.bind("<Destroy>", lambda e: self._unbind_outside_click(), add="+")
        except Exception:
            self._outside_click_binding = None

    def _destroy_if_exists(self) -> None:
        """Destroy the toplevel if it still exists."""
        try:
            if self._toplevel and self._toplevel.winfo_exists():
                self._toplevel.destroy()
        except Exception:
            pass

    def _unbind_outside_click(self) -> None:
        if self._toplevel and self._outside_click_binding:
            try:
                self._toplevel.unbind_all("<ButtonPress-1>", self._outside_click_binding)
            except Exception:
                pass
        self._outside_click_binding = None


class _DialogCalendar(Calendar):
    """Calendar variant that records why a selection event fired."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._last_trigger_reason: str | None = None

    def _on_reset_date(self, *args: Any) -> None:
        self._last_trigger_reason = "reset"
        super()._on_reset_date(*args)

    def _on_date_selected_by_date(self, target: date) -> None:
        self._last_trigger_reason = "select"
        super()._on_date_selected_by_date(target)


class DateDialog:
    """Modal dialog that displays a :class:`~ttkbootstrap.widgets.Calendar`."""

    def __init__(
            self,
            master: Optional[tkinter.Misc] = None,
            title: str = " ",
            initial_date: Optional[date] = None,
            first_weekday: int = 6,
            bootstyle: str = PRIMARY,
            disabled_dates: Optional[Iterable[date | datetime | str]] = None,
            min_date: Optional[date | datetime | str] = None,
            max_date: Optional[date | datetime | str] = None,
            show_outside_days: Optional[bool] = None,
            show_week_numbers: bool = False,
            hide_window_chrome: bool = False,
            close_on_click_outside: bool = False,
    ) -> None:
        """Create a date selection dialog.

        Args:
            master: Parent widget; positions dialog relative to it when set.
            title: Dialog window title text.
            initial_date: Initial date shown; defaults to ``date.today()``.
            first_weekday: First weekday index (0=Monday, 6=Sunday).
            bootstyle: Calendar color theme (e.g., ``primary``, ``secondary``).
            disabled_dates: Iterable of dates to disable selection.
            min_date: Lower bound for selectable dates.
            max_date: Upper bound for selectable dates.
            show_outside_days: Whether to show outside-month days. Defaults to
                the Calendar behavior (True for single month).
            show_week_numbers: Display ISO week numbers beside each row.
            hide_window_chrome: When True, displays the dialog with no window
                decorations using override-redirect.
            close_on_click_outside: When True, closes the dialog when focus
                moves outside (popover mode).
        """
        self._master = master
        self._first_weekday = first_weekday
        self._initial_date = initial_date or datetime.today().date()
        self._bootstyle = bootstyle or PRIMARY
        self._disabled_dates = disabled_dates
        self._min_date = min_date
        self._max_date = max_date
        self._show_outside_days = show_outside_days
        self._show_week_numbers = show_week_numbers
        self._hide_window_chrome = hide_window_chrome
        self._close_on_click_outside = close_on_click_outside

        self._picker: Optional[_DialogCalendar] = None

        self._dialog = _ChromeDialog(
            master=master,
            title=title,
            content_builder=self._create_content,
            buttons=[],
            footer_builder=None,
            hide_window_chrome=self._hide_window_chrome,
            mode="popover" if self._close_on_click_outside else "modal",
        )

    def _create_content(self, master: tkinter.Widget) -> None:
        """Build the Calendar content inside the dialog."""
        container = ttk.Frame(master, padding=2, show_border=True)
        container.pack(fill=BOTH, expand=YES)

        self._picker = _DialogCalendar(
            master=container,
            start_date=self._initial_date,
            first_weekday=self._first_weekday,
            bootstyle=self._bootstyle,
            disabled_dates=self._disabled_dates,
            min_date=self._min_date,
            max_date=self._max_date,
            show_outside_days=self._show_outside_days,
            show_week_numbers=self._show_week_numbers,
            padding=0,
        )
        self._picker.pack(fill=BOTH, expand=YES)
        self._picker.on_date_selected(self._on_date_selected)

    def _on_date_selected(self, event: tkinter.Event) -> None:
        """Handle <<DateSelect>> from the embedded Calendar."""
        if not self._picker:
            return
        trigger_reason = getattr(self._picker, "_last_trigger_reason", None)
        if trigger_reason != "select":
            return

        payload = getattr(event, "data", None)
        selected = None
        if isinstance(payload, dict):
            selected = payload.get("date") or payload.get("result")

        selected = selected or getattr(self._picker, "date", None)
        if selected is None:
            return

        self._dialog.result = selected
        self._emit_result(selected, confirmed=True)
        if self._dialog.toplevel:
            self._dialog.toplevel.after_idle(self._dialog.toplevel.destroy)

    def show(
            self,
            position: Optional[Tuple[int, int]] = None,
            modal: Optional[bool] = None,
            *,
            anchor_to: Optional[Union[Widget, Literal["screen", "cursor", "parent"]]] = None,
            anchor_point: AnchorPoint = 'center',
            window_point: AnchorPoint = 'center',
            offset: Tuple[int, int] = (0, 0),
            auto_flip: Union[bool, Literal['vertical', 'horizontal']] = False
    ) -> None:
        """Display the dialog and block until closed.

        Args:
            position: Optional (x, y) coordinates to position the dialog.
                If provided, takes precedence over anchor-based positioning.
                If omitted and anchor_to is not provided, positions at the parent's
                bottom-right when available, otherwise centers.
            modal: Override the mode's default modality.
                If None, uses True for modal mode dialogs.
            anchor_to: Positioning target. Can be:
                - Widget: Anchor to a specific widget
                - "screen": Anchor to screen edges/corners
                - "cursor": Anchor to mouse cursor location
                - "parent": Anchor to parent window (same as widget)
                - None: Uses default positioning behavior
            anchor_point: Point on the anchor target (n, s, e, w, ne, nw, se, sw, center).
                Default 'center'.
            window_point: Point on the dialog window (n, s, e, w, ne, nw, se, sw, center).
                Default 'center'.
            offset: Additional (x, y) offset in pixels from the anchor position.
            auto_flip: Smart positioning to keep window on screen.
                - False: No flipping (default)
                - True: Flip both vertically and horizontally as needed
                - 'vertical': Only flip up/down
                - 'horizontal': Only flip left/right
        """
        # Default positioning: bottom-right of parent if no positioning options provided
        if position is None and anchor_to is None and self._master:
            try:
                x = self._master.winfo_rootx() + self._master.winfo_width()
                y = self._master.winfo_rooty() + self._master.winfo_height()
                position = (x, y)
            except Exception:
                pass

        # Default modal to True if not specified
        if modal is None:
            modal = True

        self._dialog.show(
            position=position,
            modal=modal,
            anchor_to=anchor_to,
            anchor_point=anchor_point,
            window_point=window_point,
            offset=offset,
            auto_flip=auto_flip
        )

    @property
    def result(self) -> Optional[date]:
        """The selected date, or None if cancelled."""
        return self._dialog.result

    def on_result(self, callback: Callable[[date], None]) -> Optional[str]:
        """Bind a callback fired when a result is produced.

        The callback receives ``event.data["result"]`` (a ``datetime.date``).

        Args:
            callback: Callable that receives the selected ``datetime.date``.

        Returns:
            The Tk binding identifier, which can be used with ``off_result``.
        """
        target = self._dialog.toplevel or self._master
        if target is None:
            return None

        def handler(event: tkinter.Event) -> None:
            callback(getattr(event, "data", None))

        return target.bind("<<DialogResult>>", handler, add="+")

    def off_result(self, funcid: str) -> None:
        """Unbind a previously bound ``on_result`` callback.

        Args:
            funcid: Binding identifier returned by ``on_result``.
        """
        target = self._dialog.toplevel or self._master
        if target is None:
            return
        target.unbind("<<DialogResult>>", funcid)

    def _emit_result(self, value: date, confirmed: bool) -> None:
        """Emit a virtual Tk event with the dialog result."""
        target = self._dialog.toplevel or self._master
        if not target:
            return
        payload = {"result": value, "confirmed": confirmed}
        try:
            target.event_generate("<<DialogResult>>", data=payload)
        except Exception:
            try:
                target.event_generate("<<DialogResult>>")
            except Exception:
                pass
