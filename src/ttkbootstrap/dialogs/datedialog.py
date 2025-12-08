"""Dialog wrapper around the DatePicker widget.

Exposes a chrome-less, popover-capable date picker dialog that can close on
outside clicks and forwards DatePicker options (disabled dates, bounds, etc.).
"""

from __future__ import annotations

import tkinter
from datetime import date, datetime
from types import SimpleNamespace
from typing import Any, Callable, Iterable, Optional

from ttkbootstrap.widgets.primitives import Frame
from ttkbootstrap.constants import BOTH, PRIMARY, YES
from ttkbootstrap.dialogs.dialog import Dialog
from ttkbootstrap.widgets.composites.datepicker import DatePicker

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

    def show(self, position: Optional[tuple[int, int]] = None, modal: Optional[bool] = None):
        """Override show to position before deiconify, avoiding placement flash."""
        if modal is None:
            modal = (self._mode == "modal")

        self.result = None
        self._create_toplevel()
        if self._hide_window_chrome and self._toplevel:
            self._toplevel.withdraw()

        self._build_content()
        self._build_footer()

        self._position_dialog(position)

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
            if str(widget).startswith(str(self._toplevel)):
                return
            try:
                if self._toplevel.winfo_exists():
                    self._toplevel.destroy()
            except Exception:
                pass

        try:
            self._outside_click_binding = self._toplevel.bind_all("<ButtonPress-1>", handler, add="+")
            self._toplevel.bind("<Destroy>", lambda e: self._unbind_outside_click(), add="+")
        except Exception:
            self._outside_click_binding = None

    def _unbind_outside_click(self) -> None:
        if self._toplevel and self._outside_click_binding:
            try:
                self._toplevel.unbind_all("<ButtonPress-1>", self._outside_click_binding)
            except Exception:
                pass
        self._outside_click_binding = None


class _DialogDatePicker(DatePicker):
    """DatePicker variant that records why a selection event fired."""

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
    """Modal dialog that displays a :class:`~ttkbootstrap.widgets.DatePicker`."""

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
                the DatePicker behavior (True for single month).
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

        self._picker: Optional[_DialogDatePicker] = None

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
        """Build the DatePicker content inside the dialog."""
        container = ttk.Frame(master, padding=2, show_border=True)
        container.pack(fill=BOTH, expand=YES)

        self._picker = _DialogDatePicker(
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
        """Handle <<DateSelected>> from the embedded DatePicker."""
        if not self._picker:
            return
        if getattr(self._picker, "_last_trigger_reason", None) != "select":
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

    def show(self, position: Optional[tuple[int, int]] = None) -> None:
        """Display the dialog and block until closed.

        Args:
            position: Optional ``(x, y)`` coordinates. If omitted, positions at
                the parent's bottom-right when available, otherwise centers.
        """
        if position is None and self._master:
            try:
                x = self._master.winfo_rootx() + self._master.winfo_width()
                y = self._master.winfo_rooty() + self._master.winfo_height()
                position = (x, y)
            except Exception:
                pass

        self._dialog.show(position=position, modal=True)

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
