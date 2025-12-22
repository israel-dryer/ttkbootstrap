from tkinter import Event, TclError
from typing import Any, Callable

from ttkbootstrap.core.localization import MessageCatalog, IntlFormatter
from ttkbootstrap.widgets.primitives.entry import Entry
from ttkbootstrap.widgets.mixins import ValidationMixin
from ttkbootstrap.widgets.mixins.configure_mixin import configure_delegate


class TextEntryPart(ValidationMixin, Entry):
    """Internationalization-aware entry widget with deferred parsing and formatting.

    This widget separates user input (display text) from the committed/parsed value,
    providing a clean pattern for handling formatted data entry. Parsing and formatting
    only occur when the user commits the value via ``<FocusOut>`` or ``<Return>``.

    !!! note "Events"

        - ``<<Input>>``: Triggered on each keystroke.
          Provides ``event.data`` with keys: ``text``.

        - ``<<Change>>``: Triggered when value changes after commit.
          Provides ``event.data`` with keys: ``value``, ``prev_value``, ``text``.

        - **<Return>**: Triggered on Enter key press.
          Provides ``event.data`` with keys: ``value``, ``text``.
    """

    def __init__(
            self,
            master=None,
            *,
            value='',
            value_format=None,
            initial_focus: bool = False,
            allow_blank: bool = True,
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
            value_format (str): ICU format pattern for parsing and formatting the value.
                Common patterns: ``'#,##0.00'`` (decimal), ``'¤#,##0.00'`` (currency),
                ``'yyyy-MM-dd'`` (date), ``'#,##0.00%'`` (percent).
                If None, value is treated as plain text (no parsing/formatting).
            initial_focus (bool): If True, widget receives focus when created.
            allow_blank (bool): If True, empty input is parsed as None. If False, empty
                input preserves the previous value.
            **kwargs: Additional keyword arguments passed to the Entry base class.

        Note:
            The widget automatically subscribes to text changes and sets up
            event handlers for ``<FocusIn>``, ``<FocusOut>``, and ``<Return>``.
        """
        kwargs.update(bootstyle='field-input')
        super().__init__(master, **kwargs)

        # configuration
        self._value_format = value_format
        self._allow_blank = allow_blank
        self._on_input_fid = None
        self._fmt = IntlFormatter(locale=MessageCatalog.locale())

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
        self.winfo_toplevel().bind('<<LocaleChanged>>', self._on_locale_changed, add='+')

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
        """Emit <<Change>> event if parsed value changed since focus-in."""
        if self._value != self._prev_changed_value:
            data = {
                "value": self._value,
                "prev_value": self._prev_changed_value,
                "text": self.textsignal.get()
            }
            self.event_generate('<<Change>>', data={"value": self._value})
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
        """Bind callback to <<Change>> event (fires when value changes on commit).

        Args:
            callback: Function receiving event.data = {"value": Any, "prev_value": Any, "text": str}

        Returns:
            Binding identifier for use with off_changed()
        """
        return self.bind("<<Change>>", callback)

    def off_changed(self, funcid: str):
        """Remove callback from <<Change>> event."""
        self.unbind('<<Change>>', funcid)

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

    def _on_locale_changed(self, event=None):
        """Respond to global changes in locale by updating formatter and text"""
        self._fmt = IntlFormatter(locale=MessageCatalog.locale())

        # reformat current value with new locale + same value_format
        if self._value is not None:
            formatted_text = self._format_value(self._value)
            self.textsignal.set(formatted_text)

    @configure_delegate('text')
    def _delegate_text(self, value=None):
        if value is None:
            return self.text()
        else:
            return self.text(value)

    @configure_delegate('value')
    def _delegate_value(self, value=None):
        if value is None:
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

    def destroy(self):
        """Clean up signal subscriptions and destroy the widget."""
        if self._on_input_fid:
            try:
                self.textsignal.unsubscribe(self._on_input_fid)
            except Exception:
                pass  # Ignore all errors during cleanup
            self._on_input_fid = None
        super().destroy()
