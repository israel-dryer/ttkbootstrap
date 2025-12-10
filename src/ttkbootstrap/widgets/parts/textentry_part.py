from tkinter import Event, TclError
from typing import Any, Callable

from ttkbootstrap.runtime.app import get_app_settings
from ttkbootstrap.core.localization import IntlFormatter
from ttkbootstrap.widgets.primitives.entry import Entry
from ttkbootstrap.widgets.mixins import ValidationMixin
from ttkbootstrap.widgets.mixins.configure_mixin import configure_delegate


class TextEntryPart(ValidationMixin, Entry):
    """Internationalization-aware entry widget with deferred parsing and formatting.

    This widget separates user input (display text) from the committed/parsed value,
    providing a clean pattern for handling formatted data entry. Parsing and formatting
    only occur when the user commits the value via <FocusOut> or <Return>.

    Features:
        - Deferred parsing: Parse only on commit, not during typing
        - International formatting: Locale-aware number, date, and currency formatting
        - Three-tier event system:
            - <<Input>>: Fires on every keystroke with raw text
            - <<Changed>>: Fires when committed value changes (FocusOut/Return)
            - <Return>: Fires on Enter key with current value and text
        - Validation support via ValidationMixin
        - Automatic text normalization after parsing

    Events:
        <<Input>>: Triggered on each keystroke
            event.data = {"text": str}

        <<Changed>>: Triggered when value changes after commit
            event.data = {"value": Any, "prev_value": Any, "text": str}

        <Return>: Triggered on Enter key press
            event.data = {"value": Any, "text": str}

    Example:
        ```python
        import ttkbootstrap as ttk
        from ttkbootstrap.widgets.parts import TextEntryPart

        root = ttk.Window()

        # Currency entry with formatting
        entry = TextEntryPart(
            root,
            value='1234.56',
            value_format='¤#,##0.00',
            locale='en_US'
        )
        entry.pack()

        def on_changed(event):
            print(f"Value changed: {event.data['value']}")

        entry.on_changed(on_changed)
        root.mainloop()
        ```
    """

    def __init__(
            self,
            master=None,
            *,
            value='',
            value_format=None,
            initial_focus: bool = False,
            allow_blank: bool = True,
            locale: str = None,
            **kwargs
    ):
        """Initialize a TextEntryPart widget with internationalization support.

        Creates an entry widget that separates display text from the parsed value.
        The widget defers parsing and formatting until the user commits the value
        by pressing Enter or moving focus away from the widget.

        Args:
            master: Parent widget. If None, uses the default root window.
            value: Initial value to display and parse. Can be a string or any value
                that can be formatted using value_format. Default is empty string.
            value_format: ICU format pattern for parsing and formatting the value.
                Common patterns:
                    - Numbers: '#,##0.00' (decimal with thousands separator)
                    - Currency: '¤#,##0.00' (currency symbol with amount)
                    - Dates: 'yyyy-MM-dd' (ISO date format)
                    - Percent: '#,##0.00%' (percentage)
                If None, value is treated as plain text (no parsing/formatting).
            initial_focus: If True, widget receives focus when created. Useful for
                dialogs or forms where this field should be active immediately.
                Default is False.
            allow_blank: If True, empty input is parsed as None. If False, empty
                input preserves the previous value (rejects blank). Default is True.
            locale: Locale identifier for formatting (e.g., 'en_US', 'de_DE', 'fr_FR').
                Affects decimal separators, currency symbols, date formats, etc.
                If None, uses the system default locale. Default is None.
            **kwargs: Additional keyword arguments passed to the Entry base class.
                Common options include: width, textvariable, font, bootstyle, etc.

        Example:
            ```python
            # Simple text entry (no formatting)
            entry1 = TextEntryPart(root, value='Hello')

            # Currency entry with US formatting
            entry2 = TextEntryPart(
                root,
                value='1234.56',
                value_format='¤#,##0.00',
                locale='en_US'
            )

            # Percentage entry with auto-focus
            entry3 = TextEntryPart(
                root,
                value='0.15',
                value_format='#,##0.00%',
                initial_focus=True
            )

            # Number entry that allows blank values
            entry4 = TextEntryPart(
                root,
                value='100',
                value_format='#,##0.00',
                allow_blank=True
            )
            ```

        Note:
            The widget automatically subscribes to text changes and sets up
            event handlers for <FocusIn>, <FocusOut>, and <Return>. These
            handlers manage value commits and trigger <<Changed>> events.
        """
        kwargs.update(bootstyle='field-input')
        super().__init__(master, **kwargs)

        # configuration
        self._value_format = value_format
        self._locale = locale or get_app_settings().locale
        self._allow_blank = allow_blank
        self._on_input_fid = None

        self._fmt = IntlFormatter(locale=locale)

        # set the initial display value
        # Convert to string if it's a number
        if isinstance(value, (int, float)):
            initial_display = str(value)
        else:
            initial_display = value or self.textsignal.get() or ''

        # Parse initial value if format is specified
        if value_format is not None:
            initial_value = self._parse_or_none(initial_display)
        else:
            initial_value = initial_display or ''

        self._value = initial_value
        self._prev_changed_value = initial_value

        # normalize initial display if we already have a parsed value
        if self._value is not None:
            formatted_text = self._format_value(self._value)
            self.textsignal.set(formatted_text)
        else:
            self.textsignal.set('')

        # track last text emitted for CHANGE
        self._prev_change_text = self.textsignal.get()

        # subscribe to text changes
        self._on_input_fid = self.textsignal.subscribe(self._handle_change)

        # Commit on focus out / enter;
        self.bind('<FocusIn>', self._store_prev_value, add=True)
        self.bind('<FocusOut>', self._handle_focus_out, add=True)
        self.bind('<Return>', self._handle_return, add=True)

        # set initial focus
        if initial_focus:
            self.focus()

    def _store_prev_value(self, _: Any):
        """Store current value on focus-in to detect changes later."""
        self._prev_changed_value = self._value

    def _handle_focus_out(self, _):
        """Commit value and check for changes when focus leaves the widget."""
        self.commit()
        self._check_if_changed()

    def _handle_return(self, _):
        """Commit value and check for changes when Return key is pressed."""
        self.commit()
        self._check_if_changed()

    def _handle_change(self, event):
        """Emit <<Input>> event on every text change without parsing."""
        text = self.textsignal.get()
        if text == self._prev_change_text:
            return

        self._prev_change_text = text
        self.event_generate('<<Input>>', data={"text": text})

    def _check_if_changed(self):
        """Emit <<Changed>> event if parsed value changed since focus-in."""
        if self._value != self._prev_changed_value:
            data = {
                "value": self._value,
                "prev_value": self._prev_changed_value,
                "text": self.textsignal.get()
            }
            self.event_generate('<<Changed>>', data={"value": self._value})
            self._prev_changed_value = self._value

    def _parse_or_none(self, s: str):
        """Parse string using value_format, returning None on empty/invalid input."""
        # If a non-string is passed (e.g., datetime/date), assume it's already parsed.
        if not isinstance(s, str):
            return s
        s2 = (s or '').strip()
        if not s2:
            return None
        try:
            if self._value_format is None:
                return s2
            return self._fmt.parse(s2, self._value_format)
        except ValueError:
            return None

    def _format_value(self, value: Any) -> str:
        """Format a value for display using value_format.

        Args:
            value: The value to format (can be string, int, float, etc.)

        Returns:
            Formatted string representation of the value
        """
        if value is None:
            return ''

        # If no format specified, just convert to string
        if self._value_format is None:
            return str(value)

        # IntlFormatter.format() expects numeric values, not strings
        # So pass the value directly (it will be a number from parse())
        try:
            return self._fmt.format(value, self._value_format)
        except (ValueError, TypeError):
            # If formatting fails, return string representation
            return str(value)

    def on_input(self, callback: Callable[[Any], Any]) -> str:
        """Bind callback to <<Input>> event (fires on every keystroke).

        Args:
            callback: Function receiving event.data = {"text": str}

        Returns:
            Binding identifier for use with off_input()
        """
        return self.bind('<<Input>>', callback, add=True)

    def off_input(self, funcid: str = None):
        """Remove callback from <<Input>> event."""
        self.unbind('<<Input>>', funcid)

    def on_enter(self, callback: Callable[[Any], Any]) -> str:
        """Bind callback to <Return> event.

        Args:
            callback: Function receiving event.data = {"value": Any, "text": str}

        Returns:
            Binding identifier for use with off_enter()

        Note:
            Use on_changed() if you only care about Return when value changed.
        """

        def enrich_callback(event: Event) -> None:
            data = {"value": self._value, "text": self.textsignal.get()}
            event.data = data
            return callback(event)

        return self.bind('<Return>', enrich_callback, add=True)

    def off_enter(self, funcid: str):
        """Remove callback from <Return> event."""
        self.unbind('<Return>', funcid)

    def on_changed(self, callback: Callable[[Any], Any]) -> str:
        """Bind callback to <<Changed>> event (fires when value changes on commit).

        Args:
            callback: Function receiving event.data = {"value": Any, "prev_value": Any, "text": str}

        Returns:
            Binding identifier for use with off_changed()
        """
        return self.bind("<<Changed>>", callback)

    def off_changed(self, funcid: str):
        """Remove callback from <<Changed>> event."""
        self.unbind('<<Changed>>', funcid)

    def value(self, value=None):
        """Get or set the parsed/committed value.

        Args:
            value: If provided, sets the display text and internal value with formatting

        Returns:
            Current parsed value if no argument provided, None otherwise
        """
        if value is None:
            return self._value
        else:
            # Store the value and format it for display
            if isinstance(value, (int, float)):
                value_str = str(value)
            else:
                value_str = str(value) if value is not None else ''

            # Parse the value if format is specified
            if self._value_format is not None and value_str:
                self._value = self._parse_or_none(value_str)
            else:
                self._value = value_str if value_str else None

            # Format and display
            formatted_text = self._format_value(self._value)
            self.textsignal.set(formatted_text)
            return None

    def text(self, value=None):
        """Get or set the raw display text without committing.

        Args:
            value: If provided, sets the display text without parsing

        Returns:
            Current display text if no argument provided, None otherwise
        """
        if value is None:
            return self.textsignal.get()
        else:
            self.textsignal.set(value)
            return None

    def commit(self):
        """Parse display text, update value, and normalize display (called on FocusOut/Return)."""
        s = self.get().strip()

        # parse once
        if s == '':
            self._value = None if self._allow_blank else self._value
        else:
            try:
                self._value = s if self._value_format is None else self._fmt.parse(s, self._value_format)
            except ValueError:
                # keep prior value on parse failure
                return

        # Format the value for display
        new_text = self._format_value(self._value)

        if new_text != self.textsignal.get():
            # temporarily silence CHANGE while normalizing text
            fid = getattr(self, '_on_input_fid', None)
            if fid:
                try:
                    self.textsignal.unsubscribe(fid)
                except TclError:
                    pass
            self.textsignal.set(new_text)
            if fid:
                self._on_input_fid = self.textsignal.subscribe(self._handle_change)

    @configure_delegate('text')
    def _delegate_text(self, value=None):
        if value is not None:
            return self.text()
        else:
            return self.text(value)

    @configure_delegate('value')
    def _delegate_value(self, value=None):
        if value is not None:
            return self.value()
        else:
            return self.value(value)

    @configure_delegate('value_format')
    def _delegate_value_format(self, value: str):
        """Get or set the value format pattern and reformat display.

        Can be accessed via:
            widget.configure(value_format='#,##0.00')
            widget['value_format'] = '#,##0.00'
            widget.cget('value_format')
        """
        if value is None:
            return self._value_format

        self._value_format = value
        # Reformat current value with new format
        if self._value is not None:
            formatted_text = self._format_value(self._value)
            self.textsignal.set(formatted_text)

    @configure_delegate('allow_blank')
    def _delegate_allow_blank(self, value: bool):
        """Get or set whether blank input is allowed.

        Can be accessed via:
            widget.configure(allow_blank=True)
            widget['allow_blank'] = True
            widget.cget('allow_blank')
        """
        if value is None:
            return self._allow_blank

        self._allow_blank = bool(value)

    @configure_delegate('locale')
    def _delegate_locale(self, value: str):
        """Get or set the locale and recreate formatter.

        Can be accessed via:
            widget.configure(locale='en_US')
            widget['locale'] = 'de_DE'
            widget.cget('locale')
        """
        if value is None:
            return self._locale

        self._locale = value
        self._fmt = IntlFormatter(locale=value)
        # Reformat current value with new locale
        if self._value is not None:
            formatted_text = self._format_value(self._value)
            self.textsignal.set(formatted_text)

    def destroy(self):
        """Clean up signal subscriptions and destroy the widget."""
        if self._on_input_fid:
            try:
                self.textsignal.unsubscribe(self._on_input_fid)
            except TclError:
                pass
            self._on_input_fid = None
            super().destroy()
