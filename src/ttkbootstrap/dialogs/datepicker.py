import calendar
import locale
from datetime import datetime
from tkinter import IntVar, StringVar
from typing import Callable

from ttkbootstrap.widgets import Frame, Label, ToolRadiobutton, Button, Radiobutton
from ttkbootstrap.window import Toplevel
from ttkbootstrap.localization import MessageCatalog
from ttkbootstrap.ttk_types import StyleColor


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
        • Left-click chevron → ±1 month
        • Right-click chevron → ±1 year
    - Click the month-year label to reset to the `startdate`
    - Localized weekday labels using `MessageCatalog`
    - Calendar starts on a configurable weekday (`firstweekday`)
    - Fully themed using `color`
    - Automatically closes after selection

    Theming:
    --------
    The visual appearance of the dialog can be customized using the `color` parameter.
    This color will be applied to the header background, selected day buttons,
    and navigation controls.

    Available colors include: 'primary', 'secondary', 'success', 'info',
    'warning', 'danger', 'light', 'dark'.

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
        color: StyleColor = "primary",
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
                The default is `6` (Sunday-first calendar).

            startdate (datetime.date, optional):
                The date to initially display and select. Defaults to today’s date.

            color (StyleColor, optional):
                Color for header, navigation, and selection styling.
        """
        # Safe locale setup for weekday/month names
        try:
            locale.setlocale(locale.LC_TIME, "")
        except locale.Error:
            pass  # Continue with default C locale

        self.parent = parent
        self.firstweekday = firstweekday
        self.startdate = startdate or datetime.today().date()
        self.color = color

        self.date_selected = self.startdate
        self.date = self.startdate
        self.calendar = calendar.Calendar(firstweekday=self.firstweekday)

        self.titlevar = StringVar()
        self.datevar = IntVar()

        self.root = Toplevel(
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
        self.frm_calendar = Frame(master=self.root, padding=0, borderwidth=0, relief="flat")
        self.frm_calendar.pack(fill="both", expand=1)
        self.frm_title = Frame(self.frm_calendar, padding=(3, 3))
        self.frm_title.pack(fill="x")
        self.frm_header = Frame(self.frm_calendar, color="secondary")
        self.frm_header.pack(fill="x")

        self.root.withdraw()
        self.frm_calendar.update_idletasks()
        self._draw_titlebar()
        self._draw_calendar()
        self._set_window_position()
        self.root.deiconify()

    def _update_widget_bootstyle(self):
        """Apply the current `bootstyle` to key calendar parts."""
        self.frm_title.configure(color=self.color)
        self.title.configure(color=self.color, variant="inverse")
        self.prev_period.configure(style=f"Chevron.{self.color}.TButton")
        self.next_period.configure(style=f"Chevron.{self.color}.TButton")

    def _draw_calendar(self):
        """Render the grid of date buttons for the currently displayed month."""
        self._update_widget_bootstyle()
        self._set_title()
        self._current_month_days()

        self.frm_dates = Frame(self.frm_calendar)
        self.frm_dates.pack(fill="both", expand=1)

        for row, weekday_list in enumerate(self.monthdays):
            for col, day in enumerate(weekday_list):
                self.frm_dates.columnconfigure(col, weight=1)
                if day == 0:
                    # Display overflow days from previous/next month in muted style
                    Label(
                        master=self.frm_dates,
                        text=str(self.monthdates[row][col].day),
                        anchor="center",
                        padding=5,
                        color="secondary",
                    ).grid(row=row, column=col, sticky="nsew")
                else:
                    is_selected = (
                        day == self.date_selected.day and
                        self.date.month == self.date_selected.month and
                        self.date.year == self.date_selected.year
                    )

                    def selected(x=row, y=col):
                        self._on_date_selected(x, y)

                    if is_selected:
                        ToolRadiobutton(
                            master=self.frm_dates,
                            variable=self.datevar,
                            value=day,
                            text=str(day),
                            color="secondary",
                            command=selected
                        ).grid(row=row, column=col, sticky="nsew")
                    else:
                        CalendarRadio(
                            master=self.frm_dates,
                            variable=self.datevar,
                            value=day,
                            text=str(day),
                            color=self.color,
                            command=selected
                        ).grid(row=row, column=col, sticky="nsew")

    def _draw_titlebar(self):
        """
        Create the top navigation area of the calendar.

        Includes:
        - Month navigation chevrons (±1 month with left-click, ±1 year with right-click)
        - Month/year label that resets the view on click
        - Weekday column headers
        """
        self.prev_period = Button(master=self.frm_title, text="«", command=self.on_prev_month)
        self.prev_period.pack(side="left")

        self.title = Label(
            master=self.frm_title,
            textvariable=self.titlevar,
            anchor="center",
            font="-weight bold",
        )
        self.title.pack(side="left", fill="x", expand=1)

        self.next_period = Button(master=self.frm_title, text="»", command=self.on_next_month)
        self.next_period.pack(side="left")

        self.prev_period.bind("<Button-3>", self.on_prev_year, "+")
        self.next_period.bind("<Button-3>", self.on_next_year, "+")
        self.title.bind("<Button-1>", self.on_reset_date)

        for col in self._header_columns():
            Label(
                master=self.frm_header,
                text=col,
                anchor="center",
                padding=5,
                color="secondary",
                variant="inverse"
            ).pack(side="left", fill="x", expand=1)

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

    @staticmethod
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
        year, month = self._next_month(self.date.year, self.date.month)
        self.date = datetime(year=year, month=month, day=1).date()

    @_selection_callback
    def on_prev_month(self):
        """Move the calendar to the previous month."""
        year, month = self._prev_month(self.date.year, self.date.month)
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
    def _next_month(year, month):
        """
        Return the year and month of the following month.

        Returns:
            Tuple[int, int]: (year, month)
        """
        return (year + 1, 1) if month == 12 else (year, month + 1)

    @staticmethod
    def _prev_month(year, month):
        """
        Return the year and month of the preceding month.

        Returns:
            Tuple[int, int]: (year, month)
        """
        return (year - 1, 12) if month == 1 else (year, month - 1)


class CalendarRadio(Radiobutton):
    """A radiobutton for the calendar widget"""

    def __init__(self, master=None, color: StyleColor = "primary", **kwargs):
        kwargs.update(variant="calendar")
        super().__init__(master, color=color, **kwargs)
