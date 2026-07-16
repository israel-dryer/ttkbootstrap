"""DateEntry widget for ttkbootstrap.

An Entry field paired with a button that opens a popup calendar for date
selection; the chosen date is written back into the entry.
"""
from datetime import date, datetime
from tkinter import Misc
from typing import Any, Optional, Tuple, Union

from ttkbootstrap import Button, Entry, Frame, apply_icon
from ttkbootstrap.constants import BOTH, END, LEFT, X, YES
from ttkbootstrap.dialogs import Querybox
from ttkbootstrap.internal.configure_delegation import (
    ConfigureDelegationMixin,
    configure_delegate,
)
from ttkbootstrap.style._compat import (
    normalize_dateentry_kwargs,
    normalize_dateentry_option,
    warn_deprecated,
)


class DateEntry(ConfigureDelegationMixin, Frame):
    """A date entry widget combines an Entry field and a Button for date selection.

    When the button is pressed, a calendar popup is displayed allowing the user
    to select a date. The selected date is inserted into the entry field.

    The <<DateEntrySelected>> event is generated when a date is selected from
    the calendar popup.

    Features:
        - Configurable date format using strftime format strings
        - Customizable starting weekday (0=Monday, 6=Sunday)
        - Style customization via bootstyle parameter
        - Typed-text aware: `get_date()` / the `value` property parse the live
          entry text, so manual keyboard edits are honored
        - Blur validation: the entry is flagged `invalid` when its text cannot
          be parsed as a date
        - Access to entry and button widgets via instance attributes

    The date chooser popup will use the date in the entry field as the initial
    focus date if it matches the specified date_format. By default, the format
    is locale-specific ("%x").

    The bootstyle parameter can be used to change the widget colors. Available
    options include: primary, secondary, success, info, warning, danger, light, dark.

    Widget Attributes:
        entry (ttk.Entry): The entry field displaying the selected date
        button (ttk.Button): The button that opens the calendar popup
    """

    # Common fallback formats tried (after the widget's own `date_format`) when
    # coercing the live entry text to a date.
    _FALLBACK_FORMATS = ("%Y-%m-%d", "%m/%d/%Y")

    def __init__(
            self,
            master: Optional[Misc] = None,
            *,
            date_format: str = r"%x",
            first_weekday: int = 6,
            start_date: Optional[Union[datetime, date]] = None,
            bootstyle: str = "primary",
            button_icon: str = "calendar-week",
            show_outside_days: bool = True,
            popup_title: str = 'Select new date',
            raise_exception: bool = False,
            position: Optional[Tuple[int, int]] = None,
            **kwargs: Any,
    ) -> None:
        """
        Parameters:

            master (Widget, optional):
                The parent widget.

            date_format (str, optional):
                The format string used to render the text in the entry widget.
                Defaults to "%x" (locale's appropriate date representation).
                For more information on acceptable formats, see https://strftime.org/

            first_weekday (int, optional):
                Specifies the first day of the week. 0=Monday, 1=Tuesday,
                etc...

            start_date (datetime, optional):
                The date the widget starts on — fills the field at construction
                and is the `get_date()` fallback when the field is empty. The
                displayed date after construction is `value` / `set_date()`.
                Default is the current date.

            bootstyle (str, optional):
                A style keyword used to set the focus color of the entry
                and the background color of the date button. Available
                options include -> primary, secondary, success, info,
                warning, danger, dark, light.

            button_icon (str, optional):
                The icon to use in the button. Defaults to "calendar-week".

            show_outside_days (bool, optional):
                If True (default), the calendar popup shows the leading/trailing
                days of the adjacent months as muted, non-selectable labels. If
                False, those cells are blank (only the current month is shown).

            popup_title (str, optional):
                Window title for the calendar popup. NOTE: the popup is now a
                frameless (borderless) window, so this title is not displayed;
                it is retained for API compatibility. (Default: `Select new date`)

            raise_exception (bool, optional):
                If a `ValueError` should be raised when the user enters an
                invalid date string. If this is set to `False`, faulty date
                strings are ignored (only a warning is printed). (Default: `False`)

            position (tuple[int, int], optional):
                Optional ``(x, y)`` screen coordinates passed through to the
                date-picker popup.

            **kwargs (dict[str, Any], optional):
                Other keyword arguments passed to the frame containing the
                entry and date button. A ``width`` here is applied to the entry
                field (not the frame).
        """
        # Accept the pre-2.0 dateformat/firstweekday/startdate spellings
        # (warn-and-normalize through 2.x; removed in 3.0).
        aliases = normalize_dateentry_kwargs(kwargs)
        date_format = aliases.get("date_format", date_format)
        first_weekday = aliases.get("first_weekday", first_weekday)
        start_date = aliases.get("start_date", start_date)

        self.__enabled = True  # User/Programmer should NOT be able to change this, therefore double underscores
        self.__dateformat = self._validate_dateformat(date_format)
        self._firstweekday = first_weekday
        self._startdate = start_date or datetime.today()
        self._bootstyle = bootstyle
        self._button_icon = button_icon
        self._show_outside_days = show_outside_days
        self._popup_title = popup_title
        self._raise_exception = raise_exception
        self._position = position
        self._picker_open = False  # re-entrancy guard for the popup

        # Kwarg partitioning: `width` belongs to the entry field, everything
        # else to the frame. (Previously `width` was applied to both.)
        entry_width = kwargs.pop("width", None)
        super().__init__(master, **kwargs)

        # Build the date entry (this shows the date in the wanted format)
        entry_kwargs = {"bootstyle": self._bootstyle}
        if entry_width is not None:
            entry_kwargs["width"] = entry_width
        self.entry = Entry(self, **entry_kwargs)

        # Build datepicker button.
        self.button = Button(
            master=self,
            command=self._on_date_ask,
            bootstyle=self._bootstyle,
            icon=self._button_icon,
            icon_only=True,
            padding=2
        )
        # The button is *placed* over the entry's right edge (not packed beside
        # it) so it covers the entry's right border/corner-radius -- the field +
        # button then read as a single control. The entry reserves the button's
        # width on its right via `padx`, minus a few px of deliberate overlap so
        # the button sits on top of that border rather than flush against it.
        self.button.update_idletasks()
        overlap = 3
        reserve = max(0, self.button.winfo_reqwidth() - overlap)
        self.entry.pack(side=LEFT, fill=BOTH, expand=YES, padx=(0, reserve))
        self.button.place(relx=1.0, rely=0, relheight=1.0, anchor="ne")
        self.button.lift()

        # Mark the entry `invalid` on blur when its text is not a valid date.
        self.entry.bind("<FocusOut>", self._on_entry_blur, add="+")

        # Initialize this widget
        self.set_date(self._startdate)

    # -- configure delegates ------------------------------------------------- #
    # One get/set handler per custom option (value=None queries, else sets).
    # The ConfigureDelegationMixin wires these into configure/cget/keys/
    # __getitem__/__setitem__.

    @configure_delegate("date_format")
    def _cfg_date_format(self, value):
        if value is None:
            return self.__dateformat
        # Read the current date with the OLD format before switching, then
        # re-render it with the validated NEW format.
        current = self.get_date()
        self.__dateformat = self._validate_dateformat(value)
        if current is not None:
            self._write_entry(current.strftime(self.__dateformat))

    @configure_delegate("first_weekday")
    def _cfg_first_weekday(self, value):
        if value is None:
            return self._firstweekday
        self._firstweekday = value

    @configure_delegate("show_outside_days")
    def _cfg_show_outside_days(self, value):
        # Applies to the calendar popup the next time it is opened.
        if value is None:
            return self._show_outside_days
        self._show_outside_days = bool(value)

    @configure_delegate("button_icon")
    def _cfg_button_icon(self, value):
        # Re-render the button glyph live (theme/state-aware) via apply_icon,
        # matching the size used at construction.
        if value is None:
            return self._button_icon
        self._button_icon = value
        apply_icon(self.button, value, icon_only=True)

    @configure_delegate("start_date")
    def _cfg_start_date(self, value):
        if value is None:
            return self._startdate
        self._startdate = value

    @configure_delegate("bootstyle")
    def _cfg_bootstyle(self, value):
        if value is None:
            return self._bootstyle
        self._bootstyle = value
        self.entry.configure(bootstyle=self._bootstyle)
        self.button.configure(bootstyle=self._bootstyle)

    @configure_delegate("state")
    def _cfg_state(self, value):
        # Canonical single-string state: query returns the entry's state; a set
        # fans out to entry (+ button, for the shared normal/disabled states).
        if value is None:
            return str(self.entry.cget("state"))
        self.entry.configure(state=value)
        if value in ("disabled", "normal"):
            self.button.configure(state=value)

    @configure_delegate("width")
    def _cfg_width(self, value):
        # `width` is an entry option here, not a frame option (kills the
        # historical double-apply).
        if value is None:
            return self.entry.cget("width")
        self.entry.configure(width=value)

    # -- configure/cget wrappers (accept legacy option spellings) ------------ #
    def configure(self, cnf: Any = None, **kwargs: Any) -> Any:
        """Configure the options for this widget.

        Accepts the legacy ``dateformat``/``firstweekday``/``startdate``
        spellings (with a ``DeprecationWarning``) in addition to the snake_case
        names.
        """
        if kwargs:
            kwargs.update(normalize_dateentry_kwargs(kwargs))
        if isinstance(cnf, dict):
            cnf = dict(cnf)
            cnf.update(normalize_dateentry_kwargs(cnf))
        elif isinstance(cnf, str):
            cnf = normalize_dateentry_option(cnf)
        return super().configure(cnf, **kwargs)

    config = configure

    def cget(self, key: str) -> Any:
        return super().cget(normalize_dateentry_option(key))

    def __setitem__(self, key: str, value: Any) -> None:
        super().__setitem__(normalize_dateentry_option(key), value)

    def __getitem__(self, key: str) -> Any:
        return super().__getitem__(normalize_dateentry_option(key))

    # -- properties ---------------------------------------------------------- #
    @property
    def enabled(self) -> bool:
        """Check if the date picker is enabled.

        Returns:
            bool: True if the widget is enabled and can accept user input,
                  False otherwise.
        """
        return self.__enabled

    # NOTE: `date_format` (like start_date/first_weekday/bootstyle/state/width)
    # is a configure option, not a property -- read/write it via
    # `cget("date_format")` / `configure(date_format=...)` / `de["date_format"]`
    # (the legacy `dateformat` spelling still resolves there, with a warning).
    # Only the canonical `value` handle and the computed `enabled` state are
    # exposed as properties.

    @property
    def dateformat(self) -> str:
        """Deprecated alias for ``cget('date_format')``."""
        warn_deprecated("the 'dateformat' DateEntry attribute", "cget('date_format')")
        return self.__dateformat

    @property
    def value(self) -> Optional[datetime]:
        """The currently selected date (synonym for :meth:`get_date`).

        Reads the live entry text, falling back to the last set date when the
        text is empty or unparseable. Assigning is equivalent to
        :meth:`set_date`.
        """
        return self.get_date()

    @value.setter
    def value(self, new_date: Union[datetime, date]) -> None:
        self.set_date(new_date)

    # -- date access --------------------------------------------------------- #
    def get_date(self) -> Optional[datetime]:
        """Get the currently selected date.

        Parses the **live entry text** so typed keyboard edits are honored. If
        the text is empty or cannot be parsed, the last date set on the widget
        is returned as a fallback.

        Returns:
            datetime: The currently selected date as a datetime object.
        """
        parsed = self._coerce_date(self.entry.get())
        if parsed is not None:
            return parsed
        return self._startdate

    def set_date(self, new_date: Union[datetime, date]) -> None:
        """Set the currently selected date.

        Updates the entry field and internal state with the new date.
        Time components (hours, minutes, seconds, microseconds) are ignored
        and will be stripped from datetime objects.

        Parameters:
            new_date (datetime | date): The new date to set.
        """
        _date: datetime = self._clean_datetime(new_date)
        self._startdate = _date
        self._write_entry(_date.strftime(self.__dateformat))
        # A freshly set date is valid by construction.
        self.entry.state(['!invalid'])

    def _coerce_date(self, text: str) -> Optional[datetime]:
        """Tolerantly parse ``text`` to a ``datetime``, or ``None``.

        Tries the widget's configured ``date_format`` first, then a couple of
        common formats, then ISO-8601. Never raises.
        """
        if not text:
            return None
        for fmt in (self.__dateformat, *self._FALLBACK_FORMATS):
            try:
                return datetime.strptime(text, fmt)
            except (ValueError, TypeError):
                continue
        try:
            return datetime.fromisoformat(text)
        except (ValueError, TypeError):
            return None

    def _write_entry(self, text: str) -> None:
        """Replace the entry text, transparently toggling the disabled state."""
        was_disabled = not self.__enabled
        if was_disabled:
            self.enable()
        self.entry.delete(first=0, last=END)
        self.entry.insert(END, text)
        if was_disabled:
            self.disable()

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

    def _on_entry_blur(self, event: Any = None) -> None:
        """Flag the entry `invalid` when its text is not a parseable date.

        An empty field is treated as valid (no date entered). A non-empty,
        unparseable field is marked `invalid` so the styling reflects it.
        """
        text = self.entry.get()
        if text and self._coerce_date(text) is None:
            self.entry.state(['invalid'])
        else:
            self.entry.state(['!invalid'])

    def _on_date_ask(self) -> None:
        """Handle the calendar button click event.

        Opens the date selection popup and updates the entry field with the
        selected date. Generates the <<DateEntrySelected>> event when a date
        is chosen. Reads the initial focus date from the live entry text.

        Raises:
            ValueError: If raise_exception is True and the entry text doesn't
                       match the configured date format.
        """
        from warnings import warn

        # Re-entrancy guard: ignore a click while the picker is already open.
        if self._picker_open:
            return
        self._picker_open = True
        try:
            text = self.entry.get()
            old_date = self._coerce_date(text)
            if old_date is None:
                if text:
                    warn(f"Date entry text does not match with date format: {self.__dateformat}\n")
                    if self._raise_exception:
                        raise ValueError(
                            f"time data {text!r} does not match format {self.__dateformat!r}"
                        )
                old_date = self._startdate or datetime.today()
            self._startdate = old_date

            # get the new date and insert into the entry
            new_date = Querybox.get_date(
                parent=self.entry,
                title=self._popup_title,
                start_date=old_date,
                first_weekday=self._firstweekday,
                bootstyle=self._bootstyle,
                show_outside_days=self._show_outside_days,
                position=self._position,
            )
            # get_date returns None when the picker is cancelled (2.0); leave
            # the field unchanged rather than resetting it.
            if new_date is not None:
                self.set_date(new_date)
                self.event_generate("<<DateEntrySelected>>")
        finally:
            self._picker_open = False