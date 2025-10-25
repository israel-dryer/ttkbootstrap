"""DateEntry widget for ttkbootstrap."""
import tkinter as tk
from datetime import date, datetime
from tkinter import ttk
from typing import Union

from ttkbootstrap.constants import END
from ttkbootstrap.dialogs import Querybox


class DateEntry(ttk.Frame):
    """A date entry widget combines the `Combobox` and a `Button`
    with a callback attached to the `get_date` function.

    When pressed, a date chooser popup is displayed. The returned
    value is inserted into the combobox.

    The <<DateEntrySelected>> event is generated when a date is
    selected.

    The date chooser popup will use the date in the combobox as the
    date of focus if it is in the format specified by the
    `dateformat` parameter. By default, this format is "%Y-%m-%d".

    The bootstyle api may be used to change the style of the widget.
    The available colors include -> primary, secondary, success,
    info, warning, danger, light, dark.

    The starting weekday on the date chooser popup can be changed
    with the `firstweekday` parameter. By default this value is
    `6`, which represents "Sunday".

    The `Entry` and `Button` widgets are accessible from the
    `DateEntry.Entry` and `DateEntry.Button` properties.

    ![](../../assets/widgets/date-entry.png)
    """

    def __init__(
            self,
            master=None,
            dateformat=r"%x",
            firstweekday=6,
            startdate=None,
            bootstyle="",
            popup_title: str = 'Select new date',
            raise_exception: bool = False,
            **kwargs,
    ):
        """
        Parameters:

            master (Widget, optional):
                The parent widget.

            dateformat (str, optional):
                The format string used to render the text in the entry
                widget. For more information on acceptable formats, see https://strftime.org/

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
        from warnings import warn

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
        self.entry = ttk.Entry(self, **entry_kwargs)
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=tk.YES)

        # Build datepicker button & place it right to the date widget
        self.button = ttk.Button(
            master=self,
            command=self._on_date_ask,
            bootstyle=f"{self._bootstyle}-date",
        )
        self.button.pack(side=tk.LEFT)

        # Initialize this widget
        self.set_date(self._startdate)

    def __getitem__(self, key: str):
        return self.configure(cnf=key)

    def __setitem__(self, key: str, value):
        self.configure(cnf=None, **{key: value})

    def _configure_set(self, **kwargs):
        """Override configure method to allow for setting custom
        DateEntry parameters"""

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

        super(ttk.Frame, self).configure(**kwargs)

    def _configure_get(self, cnf):
        """Override the configure get method"""
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
            return super(ttk.Frame, self).configure(cnf=cnf)

    def configure(self, cnf=None, **kwargs):
        """Configure the options for this widget.

        Parameters:

            cnf (Dict[str, Any], optional):
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
        """
        If ``True`` this date picker is enabled and user can pick a new date, if ``False`` user can't use this picker

        :return: ``True`` if usable, ``False`` otherwise
        """
        return self.__enabled

    @property
    def dateformat(self) -> str:
        """
        Returns date format string, that is used to convert from strings to datetime objects respectively vice versa

        :return: Date format as string
        """
        return self.__dateformat

    def get_date(self) -> datetime:
        """
        Returns currently selected date as datetime object

        :return: Currently selected date
        """
        return self.configure(cnf='startdate')

    @staticmethod
    def _validate_dateformat(dateformat: str) -> str:
        """
        Checks if given dateformat string is appropriate for dates. If not, a `ValueError` will be raised.

        @see https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior

        :param dateformat: Dateformat string
        :return: Given dateformat string
        :raise ValueError: If given dateformat string is not appropriate for dates
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
        """This is a date picker, therefore erase all unnecessary elements: hours, minutes, seconds, ..."""
        if isinstance(new_date, datetime):
            return datetime(new_date.year, new_date.month, new_date.day, tzinfo=new_date.tzinfo)
        else:
            return datetime(new_date.year, new_date.month, new_date.day)

    def set_date(self, new_date: Union[datetime, date]) -> None:
        """
        Sets given date/datetime object as currently selected date.

        (NOTE: Hours, minutes, seconds, milliseconds, microseconds will be ignored)

        :param new_date: New date that will become the currently selected one
        """
        from warnings import warn

        _date: datetime = self._clean_datetime(new_date)
        if self.__enabled:
            self.configure(startdate=_date)
            self.entry.delete(first=0, last=END)
            self.entry.insert(END, new_date.strftime(self.__dateformat))
        else:
            self.enable()
            self.configure(startdate=_date)
            self.entry.delete(first=0, last=END)
            self.entry.insert(tk.END, new_date.strftime(self.__dateformat))
            self.disable()

    def disable(self) -> None:
        """ Disables this date picker """
        self.__enabled = False
        self.entry.state(['disabled'])
        self.button.state(['disabled'])

    def enable(self) -> None:
        """ Enables this date picker """
        self.__enabled = True
        self.entry.state(['!disabled'])
        self.button.state(['!disabled'])

    def _on_date_ask(self):
        """
        Callback for pushing the date button

        :raise ValueError: If entered string does NOT match with currently used date format
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