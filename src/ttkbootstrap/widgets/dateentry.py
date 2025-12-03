"""Date entry field widget with calendar picker button.

Provides a specialized entry field for date input with locale-aware formatting
and an optional calendar picker button.
"""

from datetime import date, datetime
from typing import TYPE_CHECKING

from typing_extensions import Unpack

from ttkbootstrap.widgets.button import Button
from ttkbootstrap.widgets.field import Field, FieldOptions
from ttkbootstrap.widgets.mixins import configure_delegate

if TYPE_CHECKING:
    from ttkbootstrap.dialogs.datedialog import DateDialog


class DateEntry(Field):
    """A date entry field widget with calendar picker button.

    DateEntry extends the Field widget to provide specialized date input with
    locale-aware formatting and an optional calendar picker button. The widget
    supports various date format presets and custom ICU date format patterns,
    and can accept input as strings, date objects, or datetime objects.

    Features:
        - Locale-aware date formatting
        - Multiple date format presets (longDate, shortDate, etc.)
        - Custom ICU date format patterns
        - Calendar picker button with icon
        - Accepts date, datetime, or string input
        - Automatic parsing and formatting on commit
        - All Field features (label, validation, messages, etc.)

    Date Format Presets:
        - longDate: Full date (e.g., "January 15, 2025")
        - shortDate: Short date (e.g., "1/15/25")
        - monthAndDate: Month and day (e.g., "January 15")
        - monthAndYear: Month and year (e.g., "January 2025")
        - quarterAndYear: Quarter and year (e.g., "Q1 2025")
        - day: Day of month (e.g., "15")
        - dayOfWeek: Day name (e.g., "Wednesday")
        - month: Month name (e.g., "January")
        - quarter: Quarter (e.g., "Q1")
        - year: Year (e.g., "2025")
        - longTime: Long time format (e.g., "3:30:45 PM PST")
        - shortTime: Short time format (e.g., "3:30 PM")
        - longDateLongTime: Full date and time
        - shortDateShortTime: Short date and time
        - Custom: Any ICU date format pattern (e.g., "yyyy-MM-dd")

    Events (inherited from Field):
        <<Changed>>: Fired when date value changes after commit
        <<Input>>: Fired on each keystroke
        <<Valid>>: Fired when validation passes
        <<Invalid>>: Fired when validation fails

    Example:
        ```python
        import ttkbootstrap as ttk
        from ttkbootstrap.widgets.dateentry import DateEntry
        from datetime import date

        root = ttk.Window()

        # Basic date entry with short date format
        date_entry = DateEntry(
            root,
            label="Birth Date",
            value=date(1990, 1, 15),
            value_format="shortDate",
            message="Enter your birth date"
        )
        date_entry.pack(padx=20, pady=10, fill='x')

        # Long date format
        date_entry2 = DateEntry(
            root,
            label="Event Date",
            value_format="longDate",
            locale="en_US"
        )
        date_entry2.pack(padx=20, pady=10, fill='x')

        # Custom date format (ISO 8601)
        date_entry3 = DateEntry(
            root,
            label="ISO Date",
            value="2025-01-15",
            value_format="yyyy-MM-dd"
        )
        date_entry3.pack(padx=20, pady=10, fill='x')

        # Month and year only
        date_entry4 = DateEntry(
            root,
            label="Expiry Date",
            value_format="monthAndYear"
        )
        date_entry4.pack(padx=20, pady=10, fill='x')

        # Without picker button
        date_entry5 = DateEntry(
            root,
            label="Date",
            show_picker_button=False
        )
        date_entry5.pack(padx=20, pady=10, fill='x')

        # Get date value
        def on_submit():
            value = date_entry.value()
            print(f"Selected date: {value}")

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

    Note:
        The calendar picker button is currently a placeholder. The date picker
        dialog implementation is planned for a future release. The button can
        be hidden using show_picker_button=False.
    """

    def __init__(
            self,
            master=None,
            value: str | date | datetime = None,
            value_format: str = "longDate",
            label: str = None,
            message: str = None,
            show_picker_button=True,
            picker_title: str = "Select new date",
            picker_first_weekday: int = 6,
            **kwargs: Unpack[FieldOptions]
    ):
        """Initialize a DateEntry widget.

        Creates a date entry field with locale-aware formatting and an optional
        calendar picker button. The widget accepts date input as strings, date
        objects, or datetime objects, and formats them according to the specified
        value_format pattern.

        Args:
            master: Parent widget. If None, uses the default root window.
            value: Initial date value to display. Can be a date object, datetime
                object, or string representation. Default is None (empty field).
            value_format: Date format pattern to use for parsing and displaying
                dates. Can be a preset format name or custom ICU date pattern.
                Default is "shortDate". Common presets:
                - "shortDate": Short numeric date (e.g., "1/15/25")
                - "longDate": Full date (e.g., "January 15, 2025")
                - "yyyy-MM-dd": ISO 8601 format
                - "monthAndYear": Month and year only
                See class documentation for complete list of format presets.
            label: Optional label text to display above the entry field.
                If required=True, an asterisk (*) is automatically appended.
            message: Optional message text to display below the entry field.
                Used for hints or help text. Replaced by validation errors when
                validation fails.
        show_picker_button: If True, displays the calendar picker button
            to the right of the entry. If False, hides the button. Default
            is True.
        picker_title: Title text for the calendar picker dialog (when
            implemented). Default is "Select new date".
        picker_first_weekday: First day of the week to display in the
            calendar picker. 0=Monday, 6=Sunday. Default is 6 (Sunday).
            **kwargs: Additional keyword arguments from FieldOptions:
                locale: Locale identifier for date formatting (e.g., 'en_US')
                required: If True, field cannot be empty
                bootstyle: The accent color of the focus ring and active border
                allow_blank: Allow empty input
                cursor: Cursor style when hovering
                exportselection: Export selection to clipboard
                font: Font for text display
                foreground: Text color
                initial_focus: If True, widget receives focus on creation
                justify: Text alignment
                show_message: If True, displays message area
                padding: Padding around entry widget
                take_focus: If True, widget accepts Tab focus
                textvariable: Tkinter Variable to link with text
                textsignal: Signal object for reactive updates
                width: Width in characters
                xscrollcommand: Callback for horizontal scrolling

        Note:
            The widget uses the IntlFormatter for locale-aware date formatting.
            The value is parsed and formatted automatically when the user commits
            input (on FocusOut or Return key). Invalid date strings that cannot
            be parsed will revert to the previous valid value.
        """
        kwargs.setdefault('bootstyle', 'primary')
        super().__init__(master=master, value=value, value_format=value_format, label=label, message=message, **kwargs)

        # configuration
        self._show_picker_button = show_picker_button
        self._picker_title = picker_title
        self._picker_first_weekday = picker_first_weekday

        self._button_pack = {}

        self.insert_addon(
            Button,
            position="after",
            name="date-picker",
            icon="calendar-week",
            icon_only=True,
            command=self._show_date_picker
        )

        self._delegate_show_picker_button(self._show_picker_button)

    @property
    def date_picker_button(self):
        """Get the calendar picker button widget."""
        return self.addons.get('date-picker')

    @configure_delegate('show_picker_button')
    def _delegate_show_picker_button(self, value: bool = None):
        """Get or set the visibility of the calendar picker button."""
        if value is None:
            return self._show_picker_button
        else:
            if value:
                if not self.date_picker_button.winfo_ismapped():
                    self.date_picker_button.pack(**self._button_pack)
            else:
                self._button_pack = self.date_picker_button.pack_info()
                self.date_picker_button.pack_forget()
        return None

    def _show_date_picker(self):
        """Open the calendar picker dialog.

        Opens a DateDialog seeded with the current value (if valid), updates
        the entry when a date is picked, and leaves the field unchanged on
        cancel.
        """
        from ttkbootstrap.dialogs.datedialog import DateDialog

        # Prevent multiple dialogs: reuse existing if still open
        existing = getattr(self, "_active_date_dialog", None)
        top = getattr(getattr(existing, "_dialog", None), "toplevel", None) if existing else None
        try:
            exists = bool(top and top.winfo_exists())
        except Exception:
            exists = False

        if exists:
            try:
                top.lift()
                top.focus_force()
            except Exception:
                pass
            return
        self._active_date_dialog = None

        current_value = self.value
        if isinstance(current_value, datetime):
            current_value = current_value.date()
        if not isinstance(current_value, date):
            current_value = date.today()

        position = self._picker_position()

        dialog = DateDialog(
            master=self.winfo_toplevel(),
            title=self._picker_title,
            first_weekday=self._picker_first_weekday,
            initial_date=current_value,
            bootstyle=self._bootstyle,
            hide_window_chrome=True,
            close_on_click_outside=True,
        )

        self._active_date_dialog = dialog

        def _on_result(payload):
            self.value = payload.data['result']

        dialog.on_result(lambda x: _on_result(x))
        dialog.show(position=position)

        top = getattr(getattr(dialog, "_dialog", None), "toplevel", None)
        cleared = False
        try:
            if top and top.winfo_exists():
                def _clear(_=None):
                    self._active_date_dialog = None
                top.bind("<Destroy>", _clear, add="+")
                cleared = True
        except Exception:
            cleared = False
        if not cleared:
            self._active_date_dialog = None

        # Fallback: ensure value is applied after modal dialog closes.
        selected = dialog.result
        if isinstance(selected, datetime):
            selected = selected.date()
        if isinstance(selected, date):
            self.value = selected

    def _picker_position(self):
        """Choose a dialog position beneath the entry mirroring SelectBox spacing."""
        try:
            self.update_idletasks()
            x = self.winfo_rootx() + 4
            y = self.winfo_rooty() + self.winfo_height() + 6
            return x, y
        except Exception:
            pass

        try:
            top = self.winfo_toplevel()
            top.update_idletasks()
            x = top.winfo_rootx() + top.winfo_width() // 2
            y = top.winfo_rooty() + top.winfo_height() // 2
            return x, y
        except Exception:
            return None
