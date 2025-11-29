"""DateDialog implementation (calendar popup)."""

import calendar
import tkinter
from datetime import date, datetime
from typing import Any, Callable, Optional, Tuple

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs.dialog import Dialog
from ttkbootstrap.localization import MessageCatalog


class DateDialog:
    """Dialog that displays a calendar for selecting dates.

    Navigation:
      - Left-click chevrons: change by month.
      - Right-click chevrons: change by year.
      - Click title: reset to start date.
      - Click day: select and close.
      - Close button: cancel.

    Events:
      - ``<<DialogResult>>`` fires when the dialog produces a result with
        ``event.data`` set to ``{"result": <date>, "confirmed": True}``.

    Example:
      >>> dialog = DateDialog(master=root, title="Select Date")
      >>> dialog.on_result(lambda d: print(d))
      >>> dialog.show()
      >>> print(dialog.result)
    """

    def __init__(
            self,
            master: Optional[tkinter.Misc] = None,
            title: str = " ",
            initial_date: Optional[date] = None,
            first_weekday: int = 6,
            bootstyle: str = PRIMARY,
    ) -> None:
        """Create a date selection dialog.

        Args:
            master: Parent widget; positions dialog relative to it when set.
            title: Dialog window title text.
            initial_date: Initial date shown; defaults to ``date.today()``.
            first_weekday: First weekday index (0=Monday, 6=Sunday).
            bootstyle: Calendar color theme (e.g., ``primary``, ``secondary``).
        """
        self._master = master
        self._first_weekday = first_weekday
        self._initial_date = initial_date or datetime.today().date()
        self._bootstyle = bootstyle or PRIMARY
        self._date_selected = self._initial_date  # Internal selected date storage
        self._date = self._initial_date  # Current display date
        self._calendar = calendar.Calendar(firstweekday=first_weekday)

        self._title_var = ttk.StringVar()
        self._date_var = ttk.IntVar(value=self._initial_date.day)
        self._locked_size: Optional[Tuple[int, int]] = None

        # References for dynamic calendar updates
        self.frm_dates: Optional[ttk.Frame] = None
        self.frm_calendar: Optional[ttk.Frame] = None

        # Create Dialog with no traditional buttons (calendar dates are the buttons)
        self._dialog = Dialog(
            master=master,
            title=title,
            content_builder=self._create_content,
            buttons=[],  # No footer buttons
            footer_builder=None,
        )

    def _create_content(self, master: tkinter.Widget) -> None:
        """Create the calendar dialog content.

        Args:
            master: The content frame provided by Dialog.
        """
        # Main calendar container
        self.frm_calendar = ttk.Frame(master, padding=0)
        self.frm_calendar.pack(fill=BOTH, expand=YES)

        # Navigation header
        self._create_header()

        # Weekday header
        self._create_weekday_header()

        # Calendar grid
        self._draw_calendar()

    def _create_header(self) -> None:
        """Create navigation header with month/year controls."""
        frm_title = ttk.Frame(self.frm_calendar, bootstyle=self._bootstyle, padding=(3, 3))
        frm_title.pack(fill=X)

        # Previous month button with chevron icon
        self.prev_period = ttk.Button(
            master=frm_title,
            icon="chevron-double-left",
            bootstyle=f"{self._bootstyle}",
            style_options={"icon_only": True},
            command=self._on_prev_month
        )
        self.prev_period.pack(side=LEFT)
        self.prev_period.bind("<Button-3>", self._on_prev_year, "+")

        # Month/year title
        self._set_title()
        title_label = ttk.Label(
            master=frm_title,
            textvariable=self._title_var,
            anchor=CENTER,
            font="-weight bold",
        )
        title_label.pack(side=LEFT, fill=X, expand=YES)
        title_label.bind("<Button-1>", self._on_reset_date)

        # Next month button with chevron icon
        self.next_period = ttk.Button(
            master=frm_title,
            icon="chevron-double-right",
            bootstyle=f"{self._bootstyle}",
            style_options={"icon_only": True},
            command=self._on_next_month
        )
        self.next_period.pack(side=LEFT)
        self.next_period.bind("<Button-3>", self._on_next_year, "+")

    def _create_weekday_header(self) -> None:
        """Create the weekday header row."""
        frm_header = ttk.Frame(self.frm_calendar, bootstyle=SECONDARY)
        frm_header.pack(fill=X)

        for col in self._header_columns():
            ttk.Label(
                master=frm_header,
                text=col,
                anchor=CENTER,
                padding=5,
            ).pack(side=LEFT, fill=X, expand=YES)

    def _draw_calendar(self) -> None:
        """Draw the calendar grid with date buttons."""
        self._current_month_days()
        # Only show a selected radio when the chosen date is in the visible month
        if (
                self._date.year == self._date_selected.year
                and self._date.month == self._date_selected.month
        ):
            self._date_var.set(self._date_selected.day)
        else:
            self._date_var.set(0)

        # Create or recreate the dates frame
        if self.frm_dates:
            self.frm_dates.destroy()

        self.frm_dates = ttk.Frame(self.frm_calendar)
        self.frm_dates.pack(fill=BOTH, expand=YES)

        for row, weekday_list in enumerate(self._month_days):
            for col, day in enumerate(weekday_list):
                self.frm_dates.columnconfigure(col, weight=1)
                if day == 0:
                    # Days from adjacent months
                    ttk.Label(
                        master=self.frm_dates,
                        text=self._month_dates[row][col].day,
                        anchor=CENTER,
                        padding=5,
                        bootstyle=SECONDARY,
                    ).grid(row=row, column=col, sticky=NSEW)
                else:
                    day_style = self._bootstyle + '-toolbutton'

                    def selected(x=row, y=col):
                        self._on_date_selected(x, y)

                    btn = ttk.Radiobutton(
                        master=self.frm_dates,
                        variable=self._date_var,
                        value=day,
                        text=day,
                        takefocus=True,
                        bootstyle=day_style,
                        padding=5,
                        command=selected,
                    )
                    btn.grid(row=row, column=col, sticky=NSEW)

        # Lock dialog size after first render to avoid resize flicker on navigation
        self._lock_dialog_size()

    def _set_title(self) -> None:
        _title_date_month = MessageCatalog.translate(f'{self._date.strftime("%B")}')
        _title_date_year = f'{self._date.strftime("%Y")}'
        _title_date = f'{_title_date_month} {_title_date_year}'
        self._title_var.set(value=_title_date.capitalize())

    def _current_month_days(self) -> None:
        """Fetch day numbers and dates for current month."""
        self._month_days = self._calendar.monthdayscalendar(year=self._date.year, month=self._date.month)
        self._month_dates = self._calendar.monthdatescalendar(year=self._date.year, month=self._date.month)

    def _header_columns(self) -> list[str]:
        """Create weekday headers based on `first_weekday`."""
        weekdays = [
            MessageCatalog.translate("Mo"),
            MessageCatalog.translate("Tu"),
            MessageCatalog.translate("We"),
            MessageCatalog.translate("Th"),
            MessageCatalog.translate("Fr"),
            MessageCatalog.translate("Sa"),
            MessageCatalog.translate("Su"),
        ]
        header = weekdays[self._first_weekday:] + weekdays[: self._first_weekday]
        return header

    def _on_date_selected(self, row: int, col: int) -> None:
        """Callback for selecting a date."""
        self._date_selected = self._month_dates[row][col]
        self._dialog.result = self._date_selected
        self._emit_result(self._date_selected, confirmed=True)
        if self._dialog.toplevel:
            # Defer destroy so virtual events have a chance to propagate
            self._dialog.toplevel.after_idle(self._dialog.toplevel.destroy)

    def _refresh_calendar(self) -> None:
        """Update title and redraw the calendar after navigation."""
        self._set_title()
        self._draw_calendar()

    def _on_next_month(self) -> None:
        """Navigate to next month (internal callback)."""
        year, month = self._next_month(self._date.year, self._date.month)
        self._date = datetime(year=year, month=month, day=1).date()
        self._refresh_calendar()

    def _on_next_year(self, *_: Any) -> None:
        """Navigate to next year (internal callback)."""
        year = self._date.year + 1
        month = self._date.month
        self._date = datetime(year=year, month=month, day=1).date()
        self._refresh_calendar()

    def _on_prev_month(self) -> None:
        """Navigate to previous month (internal callback)."""
        year, month = self._prev_month(self._date.year, self._date.month)
        self._date = datetime(year=year, month=month, day=1).date()
        self._refresh_calendar()

    def _on_prev_year(self, *_: Any) -> None:
        """Navigate to previous year (internal callback)."""
        year = self._date.year - 1
        month = self._date.month
        self._date = datetime(year=year, month=month, day=1).date()
        self._refresh_calendar()

    def _on_reset_date(self, *_: Any) -> None:
        """Reset calendar to start date (internal callback)."""
        self._date = self._initial_date
        self._refresh_calendar()

    def show(self, position: Optional[Tuple[int, int]] = None) -> None:
        """Display the dialog and block until closed.

        Args:
            position: Optional ``(x, y)`` coordinates. If omitted, positions at
                the parent's bottom-right when available, otherwise centers.
        """
        # Custom positioning: bottom-right of parent if no explicit position
        # Reset the cached size so UI changes (fonts/DPI/theme) recalc geometry
        self._locked_size = None

        if position is None and self._master:
            try:
                x = self._master.winfo_rootx() + self._master.winfo_width()
                y = self._master.winfo_rooty() + self._master.winfo_height()
                position = (x, y)
            except Exception:
                # If parent info not available, let Dialog center it
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

        def handler(event):
            callback(getattr(event, "data", None))

        return target.bind("<<DialogResult>>", handler, add="+")

    def off_result(self, funcid: str):
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
            # Fallback: emit without data if Tk cannot marshal the payload
            try:
                target.event_generate("<<DialogResult>>")
            except Exception:
                pass

    def _lock_dialog_size(self) -> None:
        """Freeze dialog size after first layout to prevent flashing."""
        if self._locked_size or not self._dialog.toplevel:
            return

        self._dialog.toplevel.update_idletasks()
        width = self._dialog.toplevel.winfo_width()
        height = self._dialog.toplevel.winfo_height()
        if width and height:
            self._dialog.toplevel.geometry(f"{width}x{height}")
            self._dialog.toplevel.minsize(width, height)
            self._locked_size = (width, height)

    @staticmethod
    def _next_month(year: int, month: int) -> Tuple[int, int]:
        """Calculate next month."""
        if month == 12:
            return year + 1, 1
        else:
            return year, month + 1

    @staticmethod
    def _prev_month(year: int, month: int) -> Tuple[int, int]:
        """Calculate previous month."""
        if month == 1:
            return year - 1, 12
        else:
            return year, month - 1
