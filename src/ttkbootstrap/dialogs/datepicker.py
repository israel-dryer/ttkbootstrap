import calendar
import locale
from datetime import datetime
from tkinter import FLAT, BOTH, YES, X, CENTER, NSEW, LEFT

import ttkbootstrap as ttk
from ttkbootstrap.constants import PRIMARY, SECONDARY, INVERSE
from ttkbootstrap.localization import MessageCatalog


class DatePickerDialog:
    """
    A modal calendar dialog for selecting dates.

    This dialog opens as a floating `Toplevel` window that allows the user to
    navigate through months and years using arrow buttons and select a specific
    day. Once a date is selected, the dialog closes and the `date_selected`
    attribute holds the selected `datetime.date`.

    Features:
    ---------
    - Displays the current date or a specified `startdate`
    - Navigate months with left/right chevrons
        • Left-click chevron → +/-1 month
        • Right-click chevron → +/-1 year
    - Click the month-year label to reset to the `startdate`
    - Localized weekday labels using `MessageCatalog`
    - Fully themed with `bootstyle` (primary, secondary, etc.)
    - Calendar starts on a configurable weekday (`firstweekday`)
    - Automatically closes after selection

    Notes:
    ------
    - This widget grabs all input focus until it is closed.
    - If no parent is given, the window centers over the main window.
    - If a parent is given, the calendar appears to the bottom-right of it.
    """

    def __init__(
            self,
            parent=None,
            title=" ",
            firstweekday=6,
            startdate=None,
            bootstyle=PRIMARY,
    ):
        """
        Initialize a new DatePickerDialog.

        This creates a modal calendar widget that allows the user to select a date.
        The selected date will be available via the `.date_selected` attribute.

        Parameters:
            parent (Widget, optional):
                The widget relative to which the calendar will appear. If `None`,
                the dialog appears near the top-left corner of the screen.

            title (str, optional):
                The window title. Default is a blank space.

            firstweekday (int, optional):
                Index of the first day of the week (0 = Monday, 6 = Sunday).
                Default is `6` (Sunday-first calendar).

            startdate (datetime.date, optional):
                The date to initially display and select. Defaults to today’s date.

            bootstyle (str, optional):
                The ttkbootstrap style to apply for coloring (e.g., 'primary',
                'secondary', 'info', etc.). Affects header, navigation, and
                selection styling.
        """
        # Safe locale setup for weekday/month names
        try:
            locale.setlocale(locale.LC_TIME, "")
        except locale.Error:
            pass  # Continue with default C locale

        self.parent = parent
        self.firstweekday = firstweekday
        self.startdate = startdate or datetime.today().date()
        self.bootstyle = bootstyle or PRIMARY

        self.date_selected = self.startdate
        self.date = self.startdate
        self.calendar = calendar.Calendar(firstweekday=self.firstweekday)

        self.titlevar = ttk.StringVar()
        self.datevar = ttk.IntVar()

        self.root = ttk.Toplevel(
            title=title,
            transient=self.parent,
            resizable=(False, False),
            topmost=True,
            minsize=(226, 1),
            iconify=True,
        )

        self._setup_calendar()
        self.root.grab_set()
        self.root.wait_window()

    def _setup_calendar(self):
        """Create the layout and visual elements for the calendar dialog."""
        self.frm_calendar = ttk.Frame(master=self.root, padding=0, borderwidth=0, relief=FLAT)
        self.frm_calendar.pack(fill=BOTH, expand=YES)
        self.frm_title = ttk.Frame(self.frm_calendar, padding=(3, 3))
        self.frm_title.pack(fill=X)
        self.frm_header = ttk.Frame(self.frm_calendar, bootstyle=SECONDARY)
        self.frm_header.pack(fill=X)

        self.root.withdraw()
        self.frm_calendar.update_idletasks()
        self._draw_titlebar()
        self._draw_calendar()
        self._set_window_position()
        self.root.deiconify()

    def _update_widget_bootstyle(self):
        """Apply the current `bootstyle` to key calendar components."""
        self.frm_title.configure(bootstyle=self.bootstyle)
        self.title.configure(bootstyle=f"{self.bootstyle}-inverse")
        self.prev_period.configure(style=f"Chevron.{self.bootstyle}.TButton")
        self.next_period.configure(style=f"Chevron.{self.bootstyle}.TButton")

    def _draw_calendar(self):
        """Render the grid of date buttons for the currently displayed month."""
        self._update_widget_bootstyle()
        self._set_title()
        self._current_month_days()

        self.frm_dates = ttk.Frame(self.frm_calendar)
        self.frm_dates.pack(fill=BOTH, expand=YES)

        for row, weekday_list in enumerate(self.monthdays):
            for col, day in enumerate(weekday_list):
                self.frm_dates.columnconfigure(col, weight=1)
                if day == 0:
                    # Display overflow days from previous/next month in muted style
                    ttk.Label(
                        master=self.frm_dates,
                        text=self.monthdates[row][col].day,
                        anchor=CENTER,
                        padding=5,
                        bootstyle=SECONDARY,
                    ).grid(row=row, column=col, sticky=NSEW)
                else:
                    is_selected = (
                            day == self.date_selected.day and
                            self.date.month == self.date_selected.month and
                            self.date.year == self.date_selected.year
                    )
                    day_style = "secondary-toolbutton" if is_selected else f"{self.bootstyle}-calendar"

                    def selected(x=row, y=col):
                        self._on_date_selected(x, y)

                    ttk.Radiobutton(
                        master=self.frm_dates,
                        variable=self.datevar,
                        value=day,
                        text=day,
                        bootstyle=day_style,
                        padding=5,
                        command=selected,
                    ).grid(row=row, column=col, sticky=NSEW)

    def _draw_titlebar(self):
        """
        Create the top navigation area of the calendar.

        Includes:
        - Month navigation chevrons (±1 month with left-click, ±1 year with right-click)
        - Month/year label that resets the view on click
        - Weekday column headers
        """
        self.prev_period = ttk.Button(master=self.frm_title, text="«", command=self.on_prev_month)
        self.prev_period.pack(side=LEFT)

        self.title = ttk.Label(
            master=self.frm_title,
            textvariable=self.titlevar,
            anchor=CENTER,
            font="-weight bold",
        )
        self.title.pack(side=LEFT, fill=X, expand=YES)

        self.next_period = ttk.Button(master=self.frm_title, text="»", command=self.on_next_month)
        self.next_period.pack(side=LEFT)

        self.prev_period.bind("<Button-3>", self.on_prev_year, "+")
        self.next_period.bind("<Button-3>", self.on_next_year, "+")
        self.title.bind("<Button-1>", self.on_reset_date)

        for col in self._header_columns():
            ttk.Label(
                master=self.frm_header,
                text=col,
                anchor=CENTER,
                padding=5,
                bootstyle=(SECONDARY, INVERSE),
            ).pack(side=LEFT, fill=X, expand=YES)

    def _set_title(self):
        """Update the title label with the current month and year."""
        self.titlevar.set(self.date.strftime("%B %Y").capitalize())

    def _current_month_days(self):
        """
        Compute and store the day matrix for the current month.

        - `self.monthdays`: grid of integers representing days
        - `self.monthdates`: grid of datetime.date objects
        """
        self.monthdays = self.calendar.monthdayscalendar(self.date.year, self.date.month)
        self.monthdates = self.calendar.monthdatescalendar(self.date.year, self.date.month)

    def _header_columns(self):
        """
        Generate weekday labels in the correct order based on `firstweekday`.

        Returns:
            List[str]: Translated weekday abbreviations in display order.
        """
        weekdays = [
            MessageCatalog.translate("Mo"),
            MessageCatalog.translate("Tu"),
            MessageCatalog.translate("We"),
            MessageCatalog.translate("Th"),
            MessageCatalog.translate("Fr"),
            MessageCatalog.translate("Sa"),
            MessageCatalog.translate("Su"),
        ]
        return weekdays[self.firstweekday:] + weekdays[:self.firstweekday]

    def _on_date_selected(self, row, col):
        """
        Handle selection of a calendar date and close the dialog.

        Args:
            row (int): Row index in the calendar grid.
            col (int): Column index in the calendar grid.
        """
        self.date_selected = self.monthdates[row][col]
        self.root.destroy()

    def _set_window_position(self):
        """
        Position the window either:
        - To the bottom-right of the parent widget, or
        - Centered on the screen if no parent is provided.
        """
        if self.parent:
            xpos = self.parent.winfo_rootx() + self.parent.winfo_width()
            ypos = self.parent.winfo_rooty() + self.parent.winfo_height()
        else:
            xpos = self.root.master.winfo_rootx()
            ypos = self.root.master.winfo_rooty()
        self.root.geometry(f"+{xpos}+{ypos}")

    def _selection_callback(func):
        """Decorator to redraw the calendar after changing the month/year."""

        def inner(self, *args):
            func(self, *args)
            self.frm_dates.destroy()
            self._draw_calendar()

        return inner

    @_selection_callback
    def on_next_month(self):
        """Advance the calendar to the next month."""
        year, month = self._nextmonth(self.date.year, self.date.month)
        self.date = datetime(year=year, month=month, day=1).date()

    @_selection_callback
    def on_prev_month(self):
        """Move the calendar to the previous month."""
        year, month = self._prevmonth(self.date.year, self.date.month)
        self.date = datetime(year=year, month=month, day=1).date()

    @_selection_callback
    def on_next_year(self, *_):
        """Advance the calendar to the same month next year."""
        self.date = datetime(year=self.date.year + 1, month=self.date.month, day=1).date()

    @_selection_callback
    def on_prev_year(self, *_):
        """Move the calendar to the same month in the previous year."""
        self.date = datetime(year=self.date.year - 1, month=self.date.month, day=1).date()

    @_selection_callback
    def on_reset_date(self, *_):
        """Reset the calendar view to the original `startdate`."""
        self.date = self.startdate

    @staticmethod
    def _nextmonth(year, month):
        """
        Return the year and month of the following month.

        Returns:
            Tuple[int, int]: (year, month)
        """
        return (year + 1, 1) if month == 12 else (year, month + 1)

    @staticmethod
    def _prevmonth(year, month):
        """
        Return the year and month of the preceding month.

        Returns:
            Tuple[int, int]: (year, month)
        """
        return (year - 1, 12) if month == 1 else (year, month - 1)
