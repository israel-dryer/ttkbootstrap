"""DateEntry widget for ttkbootstrap.

This module provides the DateEntry widget, which combines an Entry field
with a calendar button to allow users to select dates from a popup calendar.

Example:
    ```python
    import ttkbootstrap as ttk
    from datetime import datetime

    root = ttk.Window()

    # Create a date entry widget
    date_entry = ttk.DateEntry(root, firstweekday=0, startdate=datetime.now())
    date_entry.pack(padx=10, pady=10)

    # Get the selected date
    selected_date = date_entry.get_date()

    # Handle date selection events
    def on_date_selected(event):
        print(f"Selected date: {date_entry.get_date()}")

    date_entry.bind("<<DateEntrySelected>>", on_date_selected)

    root.mainloop()
    ```
"""
from datetime import date, datetime
from tkinter import Misc
from typing import Any, Optional, Union

from ttkbootstrap import Button, Entry, Frame
from ttkbootstrap.constants import END, LEFT, X, YES
from ttkbootstrap.dialogs import Querybox


class DateEntry(Frame):
    """A date entry widget combines an Entry field and a Button for date selection.

    When the button is pressed, a calendar popup is displayed allowing the user
    to select a date. The selected date is inserted into the entry field.

    The <<DateEntrySelected>> event is generated when a date is selected from
    the calendar popup.

    Features:
        - Configurable date format using strftime format strings
        - Customizable starting weekday (0=Monday, 6=Sunday)
        - Style customization via bootstyle parameter
        - Date validation with optional exception raising
        - Access to entry and button widgets via instance attributes

    The date chooser popup will use the date in the entry field as the initial
    focus date if it matches the specified dateformat. By default, the format
    is locale-specific ("%x").

    The bootstyle parameter can be used to change the widget colors. Available
    options include: primary, secondary, success, info, warning, danger, light, dark.

    Widget Attributes:
        entry (ttk.Entry): The entry field displaying the selected date
        button (ttk.Button): The button that opens the calendar popup

    ![](../../assets/widgets/date-entry.png)
    """

    def __init__(
            self,
            master: Optional[Misc] = None,
            dateformat: str = r"%x",
            firstweekday: int = 6,
            startdate: Optional[Union[datetime, date]] = None,
            bootstyle: str = "",
            popup_title: str = 'Select new date',
            raise_exception: bool = False,
            **kwargs: Any,
    ) -> None:
        """
        Parameters:

            master (Widget, optional):
                The parent widget.

            dateformat (str, optional):
                The format string used to render the text in the entry widget.
                Defaults to "%x" (locale's appropriate date representation).
                For more information on acceptable formats, see https://strftime.org/

            firstweekday (int, optional):
                Specifies the first day of the week. 0=Monday, 1=Tuesday,
                etc...

            startdate (datetime, optional):
                The date that is in focus when the widget is displayed. Default is
                current date.

            bootstyle (str, optional):
                A style keyword used to set the focus color of the entry
                and the background color of the date button. Available
                options include -> primary, secondary, success, info,
                warning, danger, dark, light.

            popup_title (str, optional):
                Title for PopUp window (Default: `Select new date`)

            raise_exception (bool, optional):
                If a `ValueError` should be raised, if the user enters an invalid date string. If this is set to `False`,
                faulty date strings will be ignored. Only a warning on the terminal/console will be printed. (Default: `False`)

            **kwargs (dict[str, Any], optional):
                Other keyword arguments passed to the frame containing the
                entry and date button.
        """

        self.__enabled = True  # User/Programmer should NOT be able to change this, therefore double underscores
        self.__dateformat = self._validate_dateformat(
            dateformat)  # User/Programmer should NOT be able to change this, therefore double underscores
        self._firstweekday = firstweekday

        self._startdate = startdate or datetime.today()
        self._bootstyle = bootstyle
        self._popup_title = popup_title
        self._raise_exception = raise_exception
        super().__init__(master, **kwargs)

        # add visual components
        entry_kwargs = {
            "bootstyle": self._bootstyle,
        }
        if "width" in kwargs:
            entry_kwargs["width"] = kwargs.pop("width")

        # Build date Widget button (this shows the date in the wanted format)
        self.entry = Entry(self, **entry_kwargs)
        self.entry.pack(side=LEFT, fill=X, expand=YES)

        # Build datepicker button & place it right to the date widget
        self.button = Button(
            master=self,
            command=self._on_date_ask,
            bootstyle=f"{self._bootstyle}-date",
        )
        self.button.pack(side=LEFT)

        # Initialize this widget
        self.set_date(self._startdate)

    def __getitem__(self, key: str) -> Any:
        return self.configure(cnf=key)

    def __setitem__(self, key: str, value: Any) -> None:
        self.configure(cnf=None, **{key: value})

    def _configure_set(self, **kwargs: Any) -> None:
        """Override configure method to allow for setting custom DateEntry parameters.

        Handles special configuration options like 'state', 'dateformat', 'firstweekday',
        'startdate', 'bootstyle', and 'width'.
        """

        if "state" in kwargs:
            state = kwargs.pop("state")
            if state in ["readonly", "invalid"]:
                self.entry.configure(state=state)
            elif state in ("disabled", "normal"):
                self.entry.configure(state=state)
                self.button.configure(state=state)
            else:
                kwargs[state] = state
        if "dateformat" in kwargs:
            self.__dateformat = kwargs.pop("dateformat")
        if "firstweekday" in kwargs:
            self._firstweekday = kwargs.pop("firstweekday")
        if "startdate" in kwargs:
            self._startdate = kwargs.pop("startdate")
        if "bootstyle" in kwargs:
            self._bootstyle = kwargs.pop("bootstyle")
            self.entry.configure(bootstyle=self._bootstyle)
            self.button.configure(bootstyle=[self._bootstyle, "date"])
        if "width" in kwargs:
            width = kwargs.pop("width")
            self.entry.configure(width=width)

        super(Frame, self).configure(**kwargs)

    def _configure_get(self, cnf: str) -> Any:
        """Override the configure get method.

        Returns configuration values for DateEntry-specific options.
        """
        if cnf == "state":
            entrystate = self.entry.cget("state")
            buttonstate = self.button.cget("state")
            return {"Entry": entrystate, "Button": buttonstate}
        if cnf == "dateformat":
            return self.__dateformat
        if cnf == "firstweekday":
            return self._firstweekday
        if cnf == "startdate":
            return self._startdate
        if cnf == "bootstyle":
            return self._bootstyle
        else:
            return super(Frame, self).configure(cnf=cnf)

    def configure(self, cnf: Optional[str] = None, **kwargs: Any) -> Any:
        """Configure the options for this widget.

        Parameters:

            cnf (dict[str, Any], optional):
                A dictionary of configuration options.

            **kwargs:
                Optional keyword arguments.
        """
        if cnf is not None:
            return self._configure_get(cnf)
        else:
            return self._configure_set(**kwargs)

    @property
    def enabled(self) -> bool:
        """Check if the date picker is enabled.

        Returns:
            bool: True if the widget is enabled and can accept user input,
                  False otherwise.
        """
        return self.__enabled

    @property
    def dateformat(self) -> str:
        """Get the date format string.

        Returns:
            str: The strftime format string used to convert between
                 strings and datetime objects.
        """
        return self.__dateformat

    def get_date(self) -> datetime:
        """Get the currently selected date.

        Returns:
            datetime: The currently selected date as a datetime object.
        """
        return self.configure(cnf='startdate')

    @staticmethod
    def _validate_dateformat(dateformat: str) -> str:
        """Validate that a date format string is appropriate for dates.

        Checks that the format string contains sufficient information to
        represent a complete date (year, month, and day).

        Parameters:
            dateformat (str): The strftime format string to validate.

        Returns:
            str: The validated format string.

        Raises:
            ValueError: If the format string cannot be used to represent
                       a complete date.

        See Also:
            https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior
        """
        has_year: bool = any(y in dateformat for y in ('%Y', '%y', '%G'))
        has_month: bool = any(m in dateformat for m in ('%m', '%B', '%b'))
        has_day: bool = any(d in dateformat for d in ('%d',))
        is_full_format: bool = any(f in dateformat for f in ('%x', '%c'))

        if has_year and has_month and has_day:
            return dateformat

        if is_full_format:
            return dateformat

        # Special case: (day of the year & year)
        if '%j' in dateformat and has_year:
            return dateformat

        # Special case: (week day & week number & year)
        has_week_number: bool = any(w in dateformat for w in ('%U', '%W', '%V'))
        has_week_day: bool = any(w in dateformat for w in ('%a', '%A', '%w'))
        if has_week_number and has_week_day and has_year:
            return dateformat

        raise ValueError(
            f'Given formatting string ("{dateformat}"), cannot be used to validate a given strings for dates or display a given datetime object as a date!')

    @staticmethod
    def _clean_datetime(new_date: Union[datetime, date]) -> datetime:
        """Strip time components from a datetime object.

        Since this is a date picker, removes hours, minutes, seconds, and
        microseconds, keeping only the date components (year, month, day).

        Parameters:
            new_date (datetime | date): The date or datetime to clean.

        Returns:
            datetime: A datetime object with only date components (time set to 00:00:00).
        """
        if isinstance(new_date, datetime):
            return datetime(new_date.year, new_date.month, new_date.day, tzinfo=new_date.tzinfo)
        else:
            return datetime(new_date.year, new_date.month, new_date.day)

    def set_date(self, new_date: Union[datetime, date]) -> None:
        """Set the currently selected date.

        Updates the entry field and internal state with the new date.
        Time components (hours, minutes, seconds, microseconds) are ignored
        and will be stripped from datetime objects.

        Parameters:
            new_date (datetime | date): The new date to set.
        """

        _date: datetime = self._clean_datetime(new_date)
        if self.__enabled:
            self.configure(startdate=_date)
            self.entry.delete(first=0, last=END)
            self.entry.insert(END, new_date.strftime(self.__dateformat))
        else:
            self.enable()
            self.configure(startdate=_date)
            self.entry.delete(first=0, last=END)
            self.entry.insert(END, new_date.strftime(self.__dateformat))
            self.disable()

    def disable(self) -> None:
        """Disable the date picker.

        Disables both the entry field and calendar button, preventing user interaction.
        """
        self.__enabled = False
        self.entry.state(['disabled'])
        self.button.state(['disabled'])

    def enable(self) -> None:
        """Enable the date picker.

        Enables both the entry field and calendar button, allowing user interaction.
        """
        self.__enabled = True
        self.entry.state(['!disabled'])
        self.button.state(['!disabled'])

    def _on_date_ask(self) -> None:
        """Handle the calendar button click event.

        Opens the date selection popup and updates the entry field with the
        selected date. Generates the <<DateEntrySelected>> event when a date
        is chosen.

        Raises:
            ValueError: If raise_exception is True and the entry text doesn't
                       match the configured date format.
        """
        from warnings import warn

        currently_selected_date: str = self.entry.get() or datetime.today().strftime(self.__dateformat)
        try:
            self._startdate: datetime = datetime.strptime(currently_selected_date, self.__dateformat)
        except ValueError as exc:
            warn(f"Date entry text does not match with date format: {self.__dateformat}\n")
            if self._raise_exception:
                raise exc
            return
        old_date = datetime.strptime(currently_selected_date, self.__dateformat)

        # get the new date and insert into the entry
        new_date = Querybox.get_date(
            parent=self.entry,
            title=self._popup_title,
            startdate=old_date,
            firstweekday=self._firstweekday,
            bootstyle=self._bootstyle,
        )
        self.set_date(new_date)
        self.event_generate("<<DateEntrySelected>>")
