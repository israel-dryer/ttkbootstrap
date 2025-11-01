"""DatePickerDialog implementation (calendar popup)."""

import calendar
import locale
import tkinter
from datetime import date, datetime
from typing import Any, List, Optional, Tuple

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.localization import MessageCatalog
from ttkbootstrap.utility import center_on_parent


class DatePickerDialog:
    """A dialog that displays a calendar popup and returns the
    selected date as a datetime object.

    The current date is displayed by default unless the `startdate`
    parameter is provided.

    The month can be changed by clicking the chevrons to the left
    and right of the month-year title.

    Left-click the arrow to move the calendar by one month.
    Right-click the arrow to move the calendar by one year.
    Right-click the title to reset the calendar to the start date.

    The starting weekday can be changed with the `firstweekday`
    parameter for geographies that do not start the calendar on
    Sunday, which is the default.

    The widget grabs focus and all screen events until released.
    If you want to cancel a date selection, click the 'X' button
    at the top-right corner of the widget.

    The bootstyle api may be used to change the style of the widget.
    The available colors include -> primary, secondary, success,
    info, warning, danger, light, dark.
    """

    def __init__(
            self,
            parent: Optional[tkinter.Misc] = None,
            title: str = " ",
            firstweekday: int = 6,
            startdate: Optional[date] = None,
            bootstyle: str = PRIMARY,
    ) -> None:
        """Create a date picker dialog with a calendar popup.

        The dialog displays a calendar that allows the user to select a date.
        The selected date can be accessed via the `date_selected` attribute
        after the dialog is closed. The dialog is modal and grabs focus until
        dismissed.

        Parameters:

            parent (Widget):
                Parent widget. If provided, the dialog will be positioned
                relative to it. Otherwise, it will be centered on screen.

            title (str):
                The dialog window title (default=' ').

            firstweekday (int):
                First day of the week (0=Monday, 6=Sunday). Adjust this for
                different geographical conventions (default=6).

            startdate (date):
                Initial date to display in the calendar. If None, uses today's
                date. The calendar will open to the month containing this date.

            bootstyle (str):
                The color theme for the calendar (primary, secondary, success,
                info, warning, danger, light, dark) (default=PRIMARY).

        Interaction:
            - Left-click month arrows: Move calendar by one month
            - Right-click month arrows: Move calendar by one year
            - Right-click title: Reset to start date
            - Click date: Select date and close dialog
            - Click X button: Cancel selection and close dialog
        """
        # Safe locale setup
        try:
            locale.setlocale(locale.LC_TIME, "")
        except locale.Error:
            pass

        self.parent = parent
        self.root = ttk.Toplevel(
            title=title,
            transient=self.parent,
            resizable=(False, False),
            topmost=True,
            minsize=(226, 1),
            iconify=True,
        )
        self.firstweekday = firstweekday
        self.startdate = startdate or datetime.today().date()
        self.bootstyle = bootstyle or PRIMARY

        self.date_selected = self.startdate
        self.date = startdate or self.date_selected
        self.calendar = calendar.Calendar(firstweekday=firstweekday)

        self.titlevar = ttk.StringVar()
        self.datevar = ttk.IntVar()

        self._setup_calendar()
        self.root.grab_set()
        self.root.wait_window()

    def _setup_calendar(self) -> None:
        """Setup the calendar widget"""
        # create the widget containers
        self.frm_calendar = ttk.Frame(master=self.root, padding=0, borderwidth=0, relief=FLAT)
        self.frm_calendar.pack(fill=BOTH, expand=YES)
        self.frm_title = ttk.Frame(self.frm_calendar, padding=(3, 3))
        self.frm_title.pack(fill=X)
        self.frm_header = ttk.Frame(self.frm_calendar, bootstyle=SECONDARY)
        self.frm_header.pack(fill=X)

        # setup the toplevel widget
        self.root.withdraw()  # reset the iconify state
        self.frm_calendar.update_idletasks()  # actualize geometry

        # create visual components
        self._draw_titlebar()
        self._draw_calendar()

        # make toplevel visible
        self.root.update_idletasks()
        self.root.deiconify()
        self._set_window_position()

    def _update_widget_bootstyle(self) -> None:
        self.frm_title.configure(bootstyle=self.bootstyle)
        self.title.configure(bootstyle=f"{self.bootstyle}-inverse")
        self.prev_period.configure(style=f"Chevron.{self.bootstyle}.TButton")
        self.next_period.configure(style=f"Chevron.{self.bootstyle}.TButton")

    def _draw_calendar(self) -> None:
        self._update_widget_bootstyle()
        self._set_title()
        self._current_month_days()
        self.frm_dates = ttk.Frame(self.frm_calendar)
        self.frm_dates.pack(fill=BOTH, expand=YES)

        for row, weekday_list in enumerate(self.monthdays):
            for col, day in enumerate(weekday_list):
                self.frm_dates.columnconfigure(col, weight=1)
                if day == 0:
                    ttk.Label(
                        master=self.frm_dates,
                        text=self.monthdates[row][col].day,
                        anchor=CENTER,
                        padding=5,
                        bootstyle=SECONDARY,
                    ).grid(row=row, column=col, sticky=NSEW)
                else:
                    if all(
                            [
                                day == self.date_selected.day,
                                self.date.month == self.date_selected.month,
                                self.date.year == self.date_selected.year,
                            ]
                    ):
                        day_style = "secondary-toolbutton"
                    else:
                        day_style = f"{self.bootstyle}-calendar"

                    def selected(x=row, y=col):
                        self._on_date_selected(x, y)

                    btn = ttk.Radiobutton(
                        master=self.frm_dates,
                        variable=self.datevar,
                        value=day,
                        text=day,
                        takefocus=True,
                        bootstyle=day_style,
                        padding=5,
                        command=selected,
                    )
                    btn.grid(row=row, column=col, sticky=NSEW)

    def _draw_titlebar(self) -> None:
        """Draw the calendar title bar and navigation controls."""
        # create and pack the title and action buttons
        self.prev_period = ttk.Button(master=self.frm_title, text="◀", command=self.on_prev_month)
        self.prev_period.pack(side=LEFT)

        self.title = ttk.Label(
            master=self.frm_title,
            textvariable=self.titlevar,
            anchor=CENTER,
            font="-weight bold",
        )
        self.title.pack(side=LEFT, fill=X, expand=YES)

        self.next_period = ttk.Button(master=self.frm_title, text="▶", command=self.on_next_month)
        self.next_period.pack(side=LEFT)

        # bind "year" callbacks to action buttons
        self.prev_period.bind("<Button-3>", self.on_prev_year, "+")
        self.next_period.bind("<Button-3>", self.on_next_year, "+")
        self.title.bind("<Button-1>", self.on_reset_date)

        # create and pack days of the week header
        for col in self._header_columns():
            ttk.Label(
                master=self.frm_header,
                text=col,
                anchor=CENTER,
                padding=5,
                bootstyle=(SECONDARY, INVERSE),
            ).pack(side=LEFT, fill=X, expand=YES)

    def _set_title(self) -> None:
        _titledate_month = MessageCatalog.translate(f'{self.date.strftime("%B")}')
        _titledate_year = f'{self.date.strftime("%Y")}'
        _titledate = f'{_titledate_month} {_titledate_year}'
        self.titlevar.set(value=_titledate.capitalize())

    def _current_month_days(self) -> None:
        """Fetch day numbers and dates for current month."""
        self.monthdays = self.calendar.monthdayscalendar(year=self.date.year, month=self.date.month)
        self.monthdates = self.calendar.monthdatescalendar(year=self.date.year, month=self.date.month)

    def _header_columns(self) -> List[str]:
        """Create weekday headers based on `firstweekday`."""
        weekdays = [
            MessageCatalog.translate("Mo"),
            MessageCatalog.translate("Tu"),
            MessageCatalog.translate("We"),
            MessageCatalog.translate("Th"),
            MessageCatalog.translate("Fr"),
            MessageCatalog.translate("Sa"),
            MessageCatalog.translate("Su"),
        ]
        header = weekdays[self.firstweekday:] + weekdays[: self.firstweekday]
        return header

    def _on_date_selected(self, row: int, col: int) -> None:
        """Callback for selecting a date."""
        self.date_selected = self.monthdates[row][col]
        self.root.destroy()

    def _selection_callback(func):
        """Calls the decorated `func` and redraws the calendar."""

        def inner(self, *args):
            func(self, *args)
            self.frm_dates.destroy()
            self._draw_calendar()

        return inner

    @_selection_callback
    def on_next_month(self) -> None:
        year, month = self._nextmonth(self.date.year, self.date.month)
        self.date = datetime(year=year, month=month, day=1).date()

    @_selection_callback
    def on_next_year(self, *_: Any) -> None:
        year = self.date.year + 1
        month = self.date.month
        self.date = datetime(year=year, month=month, day=1).date()

    @_selection_callback
    def on_prev_month(self) -> None:
        year, month = self._prevmonth(self.date.year, self.date.month)
        self.date = datetime(year=year, month=month, day=1).date()

    @_selection_callback
    def on_prev_year(self, *_: Any) -> None:
        year = self.date.year - 1
        month = self.date.month
        self.date = datetime(year=year, month=month, day=1).date()

    @_selection_callback
    def on_reset_date(self, *_: Any) -> None:
        self.date = self.startdate

    def _set_window_position(self) -> None:
        """Move window to bottom-right of parent, else center on master."""
        if self.parent:
            xpos = self.parent.winfo_rootx() + self.parent.winfo_width()
            ypos = self.parent.winfo_rooty() + self.parent.winfo_height()
            self.root.geometry(f"+{xpos}+{ypos}")
        else:
            center_on_parent(self.root, self.parent)

    @staticmethod
    def _nextmonth(year: int, month: int) -> Tuple[int, int]:
        if month == 12:
            return year + 1, 1
        else:
            return year, month + 1

    @staticmethod
    def _prevmonth(year: int, month: int) -> Tuple[int, int]:
        if month == 1:
            return year - 1, 12
        else:
            return year, month - 1
