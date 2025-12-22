"""Time entry field widget with dropdown list of time intervals.

Provides a specialized entry field for time input with a searchable dropdown
list of time values at specified intervals.
"""

import datetime
from typing import Union

from typing_extensions import Unpack

from ttkbootstrap.runtime.app import get_app_settings
from ttkbootstrap.core.localization import IntlFormatter
from ttkbootstrap.widgets.composites.field import FieldOptions
from ttkbootstrap.widgets.primitives.selectbox import SelectBox


class TimeEntry(SelectBox):
    """Time entry field with dropdown list of time intervals.

    TimeEntry extends SelectBox to provide specialized time input with
    locale-aware formatting and a searchable dropdown of time intervals.
    The widget supports various time format presets and custom time patterns,
    and can accept input as time objects or strings.

    Features:
        - Auto-populates dropdown with time intervals
        - Searchable time selection (type to filter)
        - Custom time format support (12-hour, 24-hour, etc.)
        - Configurable time range (min/max)
        - Clock icon button
        - Allows custom time input
        - Locale-aware time formatting
        - All SelectBox features (search, validation, etc.)

    Time Format Presets:
        - shortTime: Short time format (e.g., "3:30 PM")
        - longTime: Long time with seconds (e.g., "3:30:45 PM PST")
        - mediumTime: Medium time format (e.g., "3:30:45 PM")
        - Custom: Any ICU date format pattern (e.g., "HH:mm", "h:mm a")

    Events (inherited from Field):
        <<Change>>: Fired when time value changes after commit
        <<Input>>: Fired on each keystroke
        <<Valid>>: Fired when validation passes
        <<Invalid>>: Fired when validation fails

    Examples:
        ```python
        import ttkbootstrap as ttk
        from ttkbootstrap.widgets.composites.timeentry import TimeEntry
        from datetime import time

        root = ttk.Window()

        # Basic time entry with 30-minute intervals
        te = TimeEntry(
            root,
            label="Appointment Time",
            interval=30
        )
        te.pack(padx=20, pady=10, fill='x')

        # 24-hour format with custom range
        te2 = TimeEntry(
            root,
            label="Business Hours",
            value_format="HH:mm",
            interval=15,
            min_time=time(9, 0),
            max_time=time(17, 0)
        )
        te2.pack(padx=20, pady=10, fill='x')

        # Get the time value
        def on_submit():
            print(f"Selected time: {te.value}")

        ttk.Button(root, text="Submit", command=on_submit).pack(pady=10)

        root.mainloop()
        ```

    Inherited Properties:
        entry_widget: Access to the underlying TextEntryPart widget
        label_widget: Access to the label widget
        message_widget: Access to the message label widget
        addons: Dictionary of inserted addon widgets
        variable: Tkinter Variable linked to entry text
        signal: Signal object for reactive updates
    """

    def __init__(
            self,
            master=None,
            value: Union[datetime.time, str] = None,
            value_format: str = 'shortTime',
            interval: int = 30,
            min_time: Union[datetime.time, str] = None,
            max_time: Union[datetime.time, str] = None,
            label: str = None,
            message: str = None,
            **kwargs: Unpack[FieldOptions]
    ):
        """Initialize a TimeEntry widget.

        Creates a time entry field with locale-aware formatting and a searchable
        dropdown of time intervals. The widget accepts time input as time objects
        or strings, and formats them according to the specified value_format pattern.

        Args:
            master: Parent widget. If None, uses the default root window.
            value: Initial time value to display. Can be a time object or string.
                Default is current time.
            value_format: Time format pattern for parsing and displaying times.
                Default is "shortTime" (e.g., "3:30 PM"). Common formats:
                - "shortTime": Short time (e.g., "3:30 PM")
                - "longTime": Long time with seconds (e.g., "3:30:45 PM PST")
                - "mediumTime": Medium time (e.g., "3:30:45 PM")
                - "HH:mm": 24-hour format (e.g., "15:30")
                - "h:mm a": 12-hour format (e.g., "3:30 PM")
                See class documentation for complete list of format presets.
            interval: Time interval in minutes for dropdown items (e.g., 15, 30, 60).
                Default is 30 minutes.
            min_time: Minimum time value for the dropdown list. Can be a time object
                or string (e.g., "09:00" or "9:00 AM"). Default is midnight (00:00).
            max_time: Maximum time value for the dropdown list. Can be a time object
                or string (e.g., "17:00" or "5:00 PM"). Default is 11:59 PM (23:59).
            label: Optional label text to display above the entry field.
                If required=True, an asterisk (*) is automatically appended.
            message: Optional message text to display below the entry field.
                Used for hints or help text. Replaced by validation errors when
                validation fails.
            **kwargs: Additional keyword arguments from FieldOptions:
                locale: Locale identifier for time formatting (e.g., 'en_US')
                required: If True, field cannot be empty
                bootstyle: The accent color of the focus ring and active border
                allow_blank: Allow empty input
                width: Width in characters
                textvariable: Tkinter Variable to link with text
                textsignal: Signal object for reactive updates

        Note:
            The widget uses IntlFormatter for locale-aware time formatting.
            The dropdown is searchable - type to filter time values.
            Custom time values can be entered directly in the field.
        """
        self._interval = interval
        self._value_format = value_format
        self._locale = kwargs.get('locale') or get_app_settings().locale

        # Parse and store time range
        self._min_time = self._parse_time(min_time) if min_time else datetime.time(0, 0)
        self._max_time = self._parse_time(max_time) if max_time else datetime.time(23, 59)

        # Default to current time if not provided
        if value is None:
            value = datetime.datetime.now().time()

        # Generate time intervals for dropdown
        items = self._generate_time_intervals()

        # Initialize SelectBox with time-specific configuration
        super().__init__(
            master=master,
            value=value,
            value_format=value_format,
            items=items,
            allow_custom_values=True,
            search_enabled=True,
            dropdown_button_icon='clock',
            message=message,
            label=label,
            **kwargs
        )

    def _parse_time(self, time_value: Union[datetime.time, str]) -> datetime.time:
        """Parse time value from various input formats.

        Args:
            time_value: Time value as time object or string

        Returns:
            Parsed time object, or midnight (00:00) if parsing fails
        """
        if isinstance(time_value, datetime.time):
            return time_value

        if isinstance(time_value, str):
            # Try 24-hour format (HH:MM)
            try:
                dt = datetime.datetime.strptime(time_value, '%H:%M')
                return dt.time()
            except ValueError:
                pass

            # Try 12-hour format (h:MM AM/PM)
            try:
                dt = datetime.datetime.strptime(time_value, '%I:%M %p')
                return dt.time()
            except ValueError:
                pass

        # Fallback to midnight
        return datetime.time(0, 0)

    def _generate_time_intervals(self) -> list[str]:
        """Generate list of formatted time strings at specified intervals.

        Creates a list of time values from min_time to max_time at the specified
        interval, formatted according to value_format. Uses IntlFormatter for
        consistent locale-aware formatting with Field.

        Returns:
            List of formatted time strings
        """
        times = []
        formatter = IntlFormatter(locale=self._locale)

        # Convert time objects to datetime for iteration
        current = datetime.datetime.combine(datetime.date.today(), self._min_time)
        end = datetime.datetime.combine(datetime.date.today(), self._max_time)

        # Handle midnight crossing (e.g., min_time=22:00, max_time=02:00)
        if end < current:
            end += datetime.timedelta(days=1)

        # Generate intervals
        while current <= end:
            # Format using IntlFormatter (consistent with TextEntryPart)
            # Note: Pass datetime (not time) as IntlFormatter expects it for Babel
            try:
                formatted_time = formatter.format(current, self._value_format)
            except (ValueError, TypeError):
                # Fallback to 24-hour format if formatting fails
                formatted_time = current.strftime('%H:%M')

            times.append(formatted_time)
            current += datetime.timedelta(minutes=self._interval)

        return times

