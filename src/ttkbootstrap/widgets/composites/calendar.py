"""Inline calendar widget supporting single and range date selection."""
from __future__ import annotations

import calendar
import tkinter
from datetime import date, datetime, timedelta
from types import SimpleNamespace
from tkinter import StringVar
from typing import Any, Callable, Iterable, Literal, Optional

from babel import dates
from ttkbootstrap.widgets.primitives import Button, CheckButton, Frame, Label, Separator
from ttkbootstrap.widgets.types import Master
from ttkbootstrap.constants import BOTH, CENTER, LEFT, NSEW, PRIMARY, X, Y, YES
from ttkbootstrap.core.localization import MessageCatalog
from ttkbootstrap.widgets.mixins import configure_delegate

ttk = SimpleNamespace(
    Button=Button,
    Checkbutton=CheckButton,
    Frame=Frame,
    Label=Label,
    Separator=Separator,
    StringVar=StringVar,
)

_WEEKDAY_TOKENS = (
    "day.mo",
    "day.tu",
    "day.we",
    "day.th",
    "day.fr",
    "day.sa",
    "day.su",
)

_MONTH_TOKENS = (
    None,
    "month.january",
    "month.february",
    "month.march",
    "month.april",
    "month.may",
    "month.june",
    "month.july",
    "month.august",
    "month.september",
    "month.october",
    "month.november",
    "month.december",
)


def _localized_month_name(month_index: int) -> str:
    if 1 <= month_index < len(_MONTH_TOKENS):
        token = _MONTH_TOKENS[month_index]
        if token:
            return MessageCatalog.translate(token)
    return calendar.month_name[month_index] if 1 <= month_index <= 12 else ""


def _format_month_year(month_date: date) -> str:
    """Format month/year in the current locale via Babel, falling back to English."""
    locale_code = MessageCatalog.locale().replace("_", "-")
    try:
        return dates.format_skeleton("yMMMM", month_date, locale=locale_code)
    except Exception:
        month_name = _localized_month_name(month_date.month)
        return f"{month_name} {month_date.year}"


class Calendar(ttk.Frame):
    """Inline calendar widget for selecting dates.

    Supports single or range selection modes with optional disabled dates
    and min/max bounds. Displays one month in single mode or two months
    in range mode.

    Events:
        - ``<<DateSelect>>``: Fired on selection. ``event.data = {'date': date, 'range': tuple[date, date | None]}``
    """

    def __init__(
            self,
            master: Master = None,
            *,
            start_date: date | datetime | str | None = None,
            end_date: date | datetime | str | None = None,
            disabled_dates: Iterable[date | datetime | str] | None = None,
            selection_mode: Literal['single', 'range'] = "single",
            max_date: date | datetime | str | None = None,
            min_date: date | datetime | str | None = None,
            show_outside_days: bool | None = None,
            show_week_numbers: bool = False,
            first_weekday: int = 6,
            bootstyle: str = PRIMARY,
            padding: int | tuple[int, int] | tuple[int, int, int, int] | str | None = None,
    ) -> None:
        """Initialize a Calendar widget.

        Args:
            master: Parent widget. If None, uses the default root window.
            start_date (date | datetime | str): Initial selected date or range start.
                Accepts date, datetime, or ISO format string.
            end_date (date | datetime | str): End date for range selection. Only used
                when ``selection_mode='range'``.
            disabled_dates (Iterable): Collection of dates that cannot be selected.
            selection_mode (str): Selection mode - ``'single'`` for single date or
                ``'range'`` for date range selection.
            max_date (date | datetime | str): Maximum selectable date. Dates after
                this are disabled.
            min_date (date | datetime | str): Minimum selectable date. Dates before
                this are disabled.
            show_outside_days (bool): Whether to show days from adjacent months.
                Defaults to True for single mode, False for range mode.
            show_week_numbers (bool): Whether to display ISO week numbers in the
                leftmost column.
            first_weekday (int): First day of the week. 0=Monday, 6=Sunday.
            bootstyle (str): The accent color for selected dates and highlights.
            padding (int | tuple | str): Padding around the widget.
        """
        super().__init__(master, padding=padding)

        self._selection_mode = selection_mode
        # Derive visible months from selection mode: single->1, range->2
        self._display_months = 2 if selection_mode == "range" else 1
        # Default outside-day visibility: True for single, False for range if not provided
        if show_outside_days is None:
            self._show_outside_days = selection_mode != "range"
        else:
            self._show_outside_days = bool(show_outside_days)
        self._show_week_numbers = show_week_numbers

        self._first_weekday = first_weekday
        self._bootstyle = bootstyle or PRIMARY
        self._calendar = calendar.Calendar(firstweekday=first_weekday)

        initial = self._coerce_date(start_date) or date.today()
        self._initial_date = initial
        self._display_date = date(initial.year, initial.month, 1)

        self._range_start: date | None = self._coerce_date(start_date)
        self._range_end: date | None = self._coerce_date(end_date)
        if self._range_start and self._range_end and self._range_end < self._range_start:
            self._range_start, self._range_end = self._range_end, self._range_start

        self._selected_date: date = self._range_end or self._range_start or initial

        self._disabled_dates = {
            d for d in (self._coerce_date(x) for x in (disabled_dates or [])) if d is not None
        }
        self._max_date = self._coerce_date(max_date)
        self._min_date = self._coerce_date(min_date)

        self._title_var = ttk.StringVar()
        self._locked_size: Optional[tuple[int, int]] = None

        self._header_frame: ttk.Frame | None = None
        self._months_frame: ttk.Frame | None = None
        self._month_frames: list[ttk.Frame] = []
        self._month_separators: list[ttk.Separator] = []
        self._month_views: list[dict[str, Any]] = []

        self._build_ui()
        self.bind("<<LocaleChanged>>", lambda *_: self._refresh_calendar(), add="+")

    # --- public API --------------------------------------------------
    @configure_delegate("date")
    def _delegate_date(self, value: date | datetime | str | None = None) -> Optional[date]:
        """Get or set the current selected date."""
        if value is None:
            return self._selected_date
        new_date = self._coerce_date(value) or date.today()
        self._selected_date = new_date
        self._range_start = new_date
        self._range_end = None
        self._display_date = date(new_date.year, new_date.month, 1)
        self._refresh_calendar()
        return None

    def on_date_selected(self, callback: Callable) -> str:
        """Bind to ``<<DateSelect>>``. Callback receives ``event.data = {'date': date, 'range': tuple[date, date | None]}``."""
        return self.bind("<<DateSelect>>", callback, add=True)

    def off_date_selected(self, bind_id: str | None = None) -> None:
        """Unbind from ``<<DateSelect>>``."""
        return self.unbind("<<DateSelect>>", bind_id)

    # --- UI construction --------------------------------------------
    def _build_ui(self) -> None:
        # Single-month header only for non-range mode
        if self._selection_mode != "range":
            self._create_header()
            if not hasattr(self, "_header_separator"):
                self._header_separator = ttk.Separator(self)
                self._header_separator.pack(fill=X)
        self._draw_calendar()

    def _create_header(self) -> None:
        self._header_frame = ttk.Frame(self, padding=6)
        self._header_frame.pack(fill=X)

        for col in range(5):
            self._header_frame.columnconfigure(col, weight=1 if col == 2 else 0)

        self._prev_year_btn = ttk.Button(
            master=self._header_frame,
            icon={"name": "chevron-double-left", "size": 20},
            icon_only=True,
            bootstyle="secondary-label",
            command=self._on_prev_year,
        )
        self._prev_year_btn.grid(row=0, column=0, padx=(0, 2))
        self._prev_year_btn.bind("<Button-3>", self._on_prev_year, "+")

        self._prev_month_btn = ttk.Button(
            master=self._header_frame,
            icon={"name": "chevron-left", "size": 20},
            bootstyle="secondary-label",
            icon_only=True,
            command=self._on_prev_month,
        )
        self._prev_month_btn.grid(row=0, column=1, padx=(0, 6))

        self._set_title()
        title_label = ttk.Label(
            master=self._header_frame,
            textvariable=self._title_var,
            anchor=CENTER,
            bootstyle="secondary",
            font="label",
        )
        title_label.grid(row=0, column=2, sticky="ew")
        title_label.bind("<Button-1>", self._on_reset_date)

        self._next_month_btn = ttk.Button(
            master=self._header_frame,
            icon={"name": "chevron-right", "size": 20},
            bootstyle="secondary-label",
            icon_only=True,
            command=self._on_next_month,
        )
        self._next_month_btn.grid(row=0, column=3, padx=(6, 0))

        self._next_year_btn = ttk.Button(
            master=self._header_frame,
            icon={"name": "chevron-double-right", "size": 20},
            icon_only=True,
            bootstyle="secondary-label",
            command=self._on_next_year,
        )
        self._next_year_btn.grid(row=0, column=4, padx=(2, 0))
        self._next_year_btn.bind("<Button-3>", self._on_next_year, "+")

        # Preserve column widths so hiding buttons won't shift the title
        self._header_frame.update_idletasks()
        col_sizes = [
            self._prev_year_btn.winfo_reqwidth(),
            self._prev_month_btn.winfo_reqwidth(),
            title_label.winfo_reqwidth(),
            self._next_month_btn.winfo_reqwidth(),
            self._next_year_btn.winfo_reqwidth(),
        ]
        for idx, size in enumerate(col_sizes):
            self._header_frame.columnconfigure(idx, minsize=size)

    # --- drawing ------------------------------------------------------
    def _draw_calendar(self) -> None:
        if self._months_frame is None:
            self._months_frame = ttk.Frame(self)
            self._months_frame.pack(fill=BOTH, expand=YES)

        if self._display_months == 1:
            self._set_title()

        current = self._display_date
        for idx in range(self._display_months):
            if idx >= len(self._month_frames):
                frame = ttk.Frame(self._months_frame, padding=0)
                self._month_frames.append(frame)
                self._month_views.append({})
                frame.pack(side=LEFT, fill=BOTH, expand=YES, padx=0, pady=0)
            month_frame = self._month_frames[idx]
            view = self._month_views[idx]
            view["frame"] = month_frame
            month_frame.pack_configure(side=LEFT, fill=BOTH, expand=YES, padx=0, pady=0)
            self._draw_month(month_frame, current, view, idx)
            current = self._add_months(current, 1)

            # Insert vertical separators between months for multi-month display
            if idx < self._display_months - 1:
                if len(self._month_separators) <= idx:
                    sep = ttk.Separator(self._months_frame, orient="vertical")
                    self._month_separators.append(sep)
                sep = self._month_separators[idx]
                sep.pack(side=LEFT, fill=Y, padx=0)

        # Hide unused frames
        for extra in self._month_frames[self._display_months:]:
            extra.pack_forget()
        for sep in self._month_separators[self._display_months - 1:]:
            sep.pack_forget()

        self.after_idle(self._lock_size)

    def _draw_month(self, parent: ttk.Frame, month_date: date, view: dict[str, Any], idx: int) -> None:
        # Per-month header when in range mode
        if self._selection_mode == "range":
            header = view.get("header_frame")
            title_var = view.get("title_var")
            if header is None:
                header = ttk.Frame(parent, padding=6)
                header.pack(fill=X)
                for col in range(5):
                    header.columnconfigure(col, weight=1 if col == 2 else 0)
                view["header_frame"] = header
                title_var = ttk.StringVar()
                view["title_var"] = title_var
                # Separator between header and weekday row for this month
                sep = ttk.Separator(parent)
                sep.pack(fill=X)
                view["header_separator"] = sep

                prev_year = ttk.Button(
                    master=header,
                    icon={"name": "chevron-double-left", "size": 20},
                    icon_only=True,
                    bootstyle="secondary-label",
                    command=self._on_prev_year,
                )
                prev_year.grid(row=0, column=0, padx=(0, 2))
                view["prev_year_btn"] = prev_year

                prev_month = ttk.Button(
                    master=header,
                    icon={"name": "chevron-left", "size": 20},
                    bootstyle="secondary-label",
                    icon_only=True,
                    command=self._on_prev_month,
                )
                prev_month.grid(row=0, column=1, padx=(0, 6))
                view["prev_month_btn"] = prev_month

                title_label = ttk.Label(
                    master=header,
                    textvariable=title_var,
                    anchor=CENTER,
                    bootstyle="secondary",
                    font="label",
                )
                title_label.grid(row=0, column=2, sticky="ew")

                next_month = ttk.Button(
                    master=header,
                    icon={"name": "chevron-right", "size": 20},
                    bootstyle="secondary-label",
                    icon_only=True,
                    command=self._on_next_month,
                )
                next_month.grid(row=0, column=3, padx=(6, 0))
                view["next_month_btn"] = next_month

                next_year = ttk.Button(
                    master=header,
                    icon={"name": "chevron-double-right", "size": 20},
                    icon_only=True,
                    bootstyle="secondary-label",
                    command=self._on_next_year,
                )
                next_year.grid(row=0, column=4, padx=(2, 0))
                view["next_year_btn"] = next_year

                # Capture sizes and create spacers to hold column widths when buttons are hidden
                header.update_idletasks()
                col_sizes = [
                    prev_year.winfo_reqwidth(),
                    prev_month.winfo_reqwidth(),
                    title_label.winfo_reqwidth(),
                    next_month.winfo_reqwidth(),
                    next_year.winfo_reqwidth(),
                ]
                spacers = [
                    ttk.Frame(header, width=col_sizes[0], height=1),
                    ttk.Frame(header, width=col_sizes[1], height=1),
                    None,
                    ttk.Frame(header, width=col_sizes[3], height=1),
                    ttk.Frame(header, width=col_sizes[4], height=1),
                ]
                view["col_spacers"] = spacers
                for c_idx, size in enumerate(col_sizes):
                    header.columnconfigure(c_idx, minsize=size)

            # Update title text
            if title_var is None:
                title_var = ttk.StringVar()
                view["title_var"] = title_var
            title_var.set(_format_month_year(month_date))

            # Show/hide nav buttons depending on column
            prev_year = view.get("prev_year_btn")
            prev_month = view.get("prev_month_btn")
            next_month = view.get("next_month_btn")
            next_year = view.get("next_year_btn")
            spacers = view.get("col_spacers", [None] * 5)
            spacer_left_year, spacer_left_month, _, spacer_right_month, spacer_right_year = spacers

            def _grid_left():
                if prev_year:
                    prev_year.grid(row=0, column=0, padx=(0, 2))
                if prev_month:
                    prev_month.grid(row=0, column=1, padx=(0, 6))
                if spacer_right_month:
                    spacer_right_month.grid(row=0, column=3, padx=(6, 0))
                if spacer_right_year:
                    spacer_right_year.grid(row=0, column=4, padx=(2, 0))
                if next_month:
                    next_month.grid_remove()
                if next_year:
                    next_year.grid_remove()
                if spacer_left_year:
                    spacer_left_year.grid_remove()
                if spacer_left_month:
                    spacer_left_month.grid_remove()

            def _grid_right():
                if spacer_left_year:
                    spacer_left_year.grid(row=0, column=0, padx=(0, 2))
                if spacer_left_month:
                    spacer_left_month.grid(row=0, column=1, padx=(0, 6))
                if next_month:
                    next_month.grid(row=0, column=3, padx=(6, 0))
                if next_year:
                    next_year.grid(row=0, column=4, padx=(2, 0))
                if prev_year:
                    prev_year.grid_remove()
                if prev_month:
                    prev_month.grid_remove()
                if spacer_right_month:
                    spacer_right_month.grid_remove()
                if spacer_right_year:
                    spacer_right_year.grid_remove()

            # Ensure layout is stable each draw
            if idx == 0:
                _grid_left()
            else:
                _grid_right()
        else:
            # Ensure any per-month header is hidden when not in range nav mode
            header = view.get("header_frame")
            if header:
                header.pack_forget()

        # Weekday header per month
        weekdays_frame: ttk.Frame | None = view.get("weekdays")
        if weekdays_frame is None:
            weekdays_frame = ttk.Frame(parent)
            weekdays_frame.pack(fill=X)
            view["weekdays"] = weekdays_frame
        else:
            for child in weekdays_frame.winfo_children():
                child.destroy()

        if self._show_week_numbers:
            ttk.Label(weekdays_frame, text="#", anchor=CENTER, padding=5, surface_color="background[+1]").pack(
                side=LEFT, fill=X, expand=YES)
        for col in self._header_columns():
            ttk.Label(
                master=weekdays_frame,
                text=col,
                anchor=CENTER,
                padding=5,
                bootstyle="secondary",
                font="body[bold]",
            ).pack(side=LEFT, fill=X, expand=YES)

        # Grid reused
        grid: ttk.Frame | None = view.get("grid")
        if grid is None:
            grid = ttk.Frame(parent)
            grid.pack(fill=BOTH, expand=YES)
            view["grid"] = grid
            cells: list[list[ttk.Checkbutton]] = []
            cell_vars: list[list[tkinter.BooleanVar]] = []
            week_labels: list[ttk.Label] = []
            for r in range(6):
                if self._show_week_numbers:
                    wl = ttk.Label(grid, anchor=CENTER, padding=5, surface_color="background[+1]")
                    wl.grid(row=r, column=0, sticky=NSEW)
                    week_labels.append(wl)
                row_cells: list[ttk.Checkbutton] = []
                row_vars: list[tkinter.BooleanVar] = []
                for c in range(7):
                    col_offset = 1 if self._show_week_numbers else 0
                    grid.columnconfigure(c + col_offset, weight=1)
                    var = tkinter.BooleanVar(value=False)
                    btn = ttk.Checkbutton(
                        grid,
                        padding=2,
                        bootstyle=f"{self._bootstyle}-calendar_day-toolbutton",
                        variable=var,
                        onvalue=True,
                        offvalue=False,
                        takefocus=True,
                    )
                    btn.grid(row=r, column=c + col_offset, sticky=NSEW)
                    row_cells.append(btn)
                    row_vars.append(var)
                cells.append(row_cells)
                cell_vars.append(row_vars)
            view["cells"] = cells
            view["cell_vars"] = cell_vars
            view["week_labels"] = week_labels
        else:
            cells = view["cells"]
            cell_vars = view.get("cell_vars", [])
            week_labels = view.get("week_labels", [])

        # Compute 42 sequential days starting at first cell of month view
        month_dates = self._calendar.monthdatescalendar(year=month_date.year, month=month_date.month)
        start = month_dates[0][0]
        days = [start + timedelta(days=i) for i in range(42)]

        # Update week numbers; hide rows with no in-month days
        if self._show_week_numbers:
            for r, wl in enumerate(week_labels):
                row_days = days[r * 7:(r + 1) * 7]
                in_month = any(d.month == month_date.month for d in row_days)
                if in_month:
                    wl.configure(text=str(row_days[0].isocalendar()[1]))
                    wl.grid(row=r, column=0, sticky=NSEW)
                else:
                    if self._show_outside_days:
                        off_only = all(d.month != month_date.month for d in row_days)
                    else:
                        off_only = True
                    if off_only:
                        wl.grid_remove()
                    else:
                        wl.configure(text=str(row_days[0].isocalendar()[1]))
                        wl.grid(row=r, column=0, sticky=NSEW)

        # Track which rows should be visible
        row_visible = [False] * 6

        # Update cells without recreating
        for idx, d in enumerate(days):
            r, c = divmod(idx, 7)
            btn = cells[r][c]
            var = cell_vars[r][c]
            in_month = d.month == month_date.month

            # Mark row visible if it has an in-month day or we are showing outside days
            if in_month or self._show_outside_days:
                row_visible[r] = True

            if not self._show_outside_days and not in_month:
                btn.configure(
                    text="",
                    command=lambda d=d: None,
                    bootstyle="text-toolbutton",
                    takefocus=False,
                )
                btn.state(["disabled"])
                var.set(False)
                continue

            disabled = self._is_disabled(d)
            style = self._style_for_date(d, in_month, disabled)
            is_selected = self._is_selected(d)
            btn.configure(
                text=d.day,
                bootstyle=style,
                command=(lambda d=d: self._on_date_selected_by_date(d)),
                takefocus=not disabled,
            )
            var.set(is_selected)
            if disabled or not in_month:
                btn.state(["disabled"])
            else:
                btn.state(["!disabled"])

        # Hide or show rows (including week numbers) based on visibility
        col_offset = 1 if self._show_week_numbers else 0
        for r in range(6):
            if row_visible[r]:
                for c in range(7):
                    cells[r][c].grid(row=r, column=c + col_offset, sticky=NSEW)
                if self._show_week_numbers and r < len(week_labels):
                    week_labels[r].grid(row=r, column=0, sticky=NSEW)
            else:
                for c in range(7):
                    cells[r][c].grid_remove()
                if self._show_week_numbers and r < len(week_labels):
                    week_labels[r].grid_remove()

    # --- selection/navigation ----------------------------------------
    def _refresh_calendar(self) -> None:
        self._draw_calendar()

    def _on_next_month(self, *_args) -> None:
        candidate = self._add_months(self._display_date, 1)
        if self._is_month_allowed(candidate):
            self._display_date = candidate
            self._refresh_calendar()

    def _on_prev_month(self, *_args) -> None:
        candidate = self._add_months(self._display_date, -1)
        if self._is_month_allowed(candidate):
            self._display_date = candidate
            self._refresh_calendar()

    def _on_next_year(self, *_args) -> None:
        candidate = date(self._display_date.year + 1, self._display_date.month, 1)
        if self._is_month_allowed(candidate):
            self._display_date = candidate
            self._refresh_calendar()

    def _on_prev_year(self, *_args) -> None:
        candidate = date(self._display_date.year - 1, self._display_date.month, 1)
        if self._is_month_allowed(candidate):
            self._display_date = candidate
            self._refresh_calendar()

    def _on_reset_date(self, *_args) -> None:
        self._display_date = date(self._initial_date.year, self._initial_date.month, 1)
        self._selected_date = self._initial_date
        self._range_start = self._initial_date
        self._range_end = None
        self._refresh_calendar()
        self.event_generate(
            "<<DateSelect>>", data={"date": self._selected_date, "range": (self._range_start, self._range_end)})

    def _on_date_selected_by_date(self, target: date) -> None:
        if self._is_disabled(target):
            return
        if self._selection_mode == "range":
            if self._range_start is None or self._range_end is not None:
                self._range_start = target
                self._range_end = None
            else:
                if target < self._range_start:
                    self._range_start, target = target, self._range_start
                self._range_end = target
            self._selected_date = target
        else:
            self._selected_date = target
            self._range_start = target
            self._range_end = None

        self._draw_calendar()
        self.event_generate(
            "<<DateSelect>>", data={"date": self._selected_date, "range": (self._range_start, self._range_end)})

    # --- helpers ------------------------------------------------------
    def _lock_size(self) -> None:
        if self._locked_size is None:
            self.update_idletasks()
            self._locked_size = (self.winfo_width(), self.winfo_height())
            try:
                self.minsize(*self._locked_size)
            except Exception:
                pass

    def _header_columns(self) -> list[str]:
        localized_weekdays = [MessageCatalog.translate(token) for token in _WEEKDAY_TOKENS]
        return localized_weekdays[self._first_weekday:] + localized_weekdays[: self._first_weekday]

    def _is_disabled(self, d: date) -> bool:
        if d in self._disabled_dates:
            return True
        if self._min_date and d < self._min_date:
            return True
        if self._max_date and d > self._max_date:
            return True
        return False

    def _style_for_date(self, d: date, in_month: bool, disabled: bool) -> str:
        if disabled or not in_month:
            return "text-toolbutton"
        if self._selection_mode == "range" and self._range_start:
            end = self._range_end
            start = self._range_start
            if end and start:
                if start <= d <= end:
                    if start < d < end:
                        return f"{self._bootstyle}[subtle]-calendar_range-toolbutton"
                    return f"{self._bootstyle}-calendar_date-toolbutton"
        return f"{self._bootstyle}-calendar_day-toolbutton"

    def _is_selected(self, d: date) -> bool:
        if self._selection_mode == "range":
            if not self._range_start:
                return False
            if self._range_end:
                return self._range_start <= d <= self._range_end
            return d == self._range_start
        return d == self._selected_date

    def _is_month_allowed(self, candidate: date) -> bool:
        if self._min_date and candidate < self._min_date.replace(day=1):
            return False
        if self._max_date and candidate > self._max_date.replace(day=1):
            return False
        return True

    def _set_title(self) -> None:
        self._title_var.set(_format_month_year(self._display_date))

    @staticmethod
    def _add_months(d: date, n: int) -> date:
        year = d.year + (d.month - 1 + n) // 12
        month = (d.month - 1 + n) % 12 + 1
        return date(year, month, 1)

    @staticmethod
    def _coerce_date(value: date | datetime | str | None) -> date | None:
        if value is None:
            return None
        if isinstance(value, date) and not isinstance(value, datetime):
            return value
        if isinstance(value, datetime):
            return value.date()
        if isinstance(value, str):
            for fmt in ("%Y-%m-%d", "%m/%d/%Y"):
                try:
                    return datetime.strptime(value, fmt).date()
                except Exception:
                    continue
            try:
                return datetime.fromisoformat(value).date()
            except Exception:
                return None
        return None


__all__ = ["Calendar"]
