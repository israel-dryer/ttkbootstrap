"""Numeric entry widget with manual stepping and validation.

This module provides a number entry widget that extends TextEntryPart with
numeric-specific features like min/max bounds, stepping, and keyboard/mouse
wheel support.
"""

from typing import Union

from ttkbootstrap.widgets.mixins.configure_mixin import configure_delegate
from ttkbootstrap.widgets.parts.textentry_part import TextEntryPart


class NumberEntryPart(TextEntryPart):
    """Numeric entry widget with stepping and bounds validation.

    Extends TextEntryPart to provide numeric input with constraints and
    stepping functionality. Supports min/max bounds, increment/decrement
    via keyboard and mouse wheel, and optional wrapping.

    Features:
        - Numeric constraints (min, max)
        - Keyboard stepping (Up/Down arrows)
        - Mouse wheel support
        - Optional value wrapping at boundaries
        - Locale-aware number formatting
        - Virtual events for increment/decrement

    Events:
        <<Increment>>: Fired when an increment is requested (before step occurs).
            Emit this event to programmatically increment the value.
            Can be intercepted to prevent or customize increment behavior.

        <<Decrement>>: Fired when a decrement is requested (before step occurs).
            Emit this event to programmatically decrement the value.
            Can be intercepted to prevent or customize decrement behavior.

        Plus all events from TextEntryPart:
            <<Input>>, <<Change>>, <Return>

    Example:
        ```python
        import ttkbootstrap as ttk
        from ttkbootstrap.widgets.parts import NumberEntryPart

        root = ttk.Window()

        # Basic numeric entry with bounds
        entry = NumberEntryPart(
            root,
            value=50,
            min_value=0,
            max_value=100,
            increment=5,
            value_format='#,##0.00'
        )
        entry.pack()

        # Percentage entry with wrapping
        pct_entry = NumberEntryPart(
            root,
            value=0.5,
            min_value=0.0,
            max_value=1.0,
            increment=0.1,
            wrap=True,
            value_format='percent'
        )
        pct_entry.pack()

        root.mainloop()
        ```
    """

    def __init__(
            self,
            master=None,
            *,
            value: Union[int, float, str] = 0,
            value_format: str = None,
            minvalue: Union[int, float, None] = None,
            maxvalue: Union[int, float, None] = None,
            increment: Union[int, float] = 1,
            wrap: bool = False,
            initial_focus: bool = False,
            allow_blank: bool = True,
            **kwargs
    ):
        """Initialize a NumberEntryPart widget.

        Args:
            master: Parent widget
            value: Initial numeric value (int, float, string, or None)
            value_format: Number format specification for IntlFormatter.
                Examples: 'decimal', 'percent', 'currency', '#,##0.00', etc.
            minvalue: Minimum allowed value (inclusive), or None for no lower bound
            maxvalue: Maximum allowed value (inclusive), or None for no upper bound
            increment: Step size for increment/decrement operations
            wrap: If True, values wrap around at min/max boundaries.
                If False, values are clamped at boundaries.
            initial_focus: If True, widget receives focus on creation
            allow_blank: If True, empty input is allowed (sets value to None)
            locale: Locale identifier for number formatting (e.g., 'en_US')
            **kwargs: Additional keyword arguments passed to TextEntryPart
        """
        # Store numeric configuration
        self._minvalue = minvalue
        self._maxvalue = maxvalue
        self._increment = increment
        self._wrap = wrap

        # Determine numeric type (float if any parameter is float)
        def _has_fractional(x: Union[int, float, None]) -> bool:
            if x is None:
                return False
            if isinstance(x, float):
                return True
            if isinstance(x, (int, float)) and float(x) != int(x):
                return True
            return False

        self._num_type = float if any(
            _has_fractional(x) for x in (
                minvalue, maxvalue, increment,
                value if not isinstance(value, str) else 0
            )
        ) else int

        # Initialize base TextEntryPart
        # Convert initial value to appropriate type
        if isinstance(value, str):
            initial_value = value
        else:
            initial_value = None if value is None else self._num_type(value)

        super().__init__(
            master=master,
            value=initial_value,
            value_format=value_format,
            initial_focus=initial_focus,
            allow_blank=allow_blank,
            **kwargs
        )

        # Apply bounds to initial value
        if self._value is not None:
            self._value = self._apply_bounds(float(self._value))
            if self._num_type is int:
                self._value = int(round(self._value))
            # Update display with bounded value
            formatted_text = self._format_value(self._value)
            self.textsignal.set(formatted_text)
            self._prev_changed_value = self._value

        # Bind keyboard stepping (Up/Down arrows)
        self.bind('<Up>', self._handle_up_key, add=True)
        self.bind('<Down>', self._handle_down_key, add=True)

        # Bind mouse wheel (Windows/macOS)
        self.bind('<MouseWheel>', self._handle_mouse_wheel, add=True)

        # Bind mouse wheel (Linux/X11)
        self.bind('<Button-4>', self._handle_wheel_up, add=True)
        self.bind('<Button-5>', self._handle_wheel_down, add=True)

        # Listen for increment/decrement events to invoke step
        self.bind('<<Increment>>', self._handle_increment_event, add=True)
        self.bind('<<Decrement>>', self._handle_decrement_event, add=True)

    def _handle_up_key(self, event):
        """Handle Up arrow key press - emit increment event."""
        if not self._is_interactive():
            return 'break'
        self.event_generate('<<Increment>>')
        return 'break'  # Prevent default behavior

    def _handle_down_key(self, event):
        """Handle Down arrow key press - emit decrement event."""
        if not self._is_interactive():
            return 'break'
        self.event_generate('<<Decrement>>')
        return 'break'  # Prevent default behavior

    def _handle_mouse_wheel(self, event):
        """Handle mouse wheel on Windows/macOS."""
        if not self._is_interactive():
            return 'break'
        try:
            delta = int(event.delta)
        except (AttributeError, ValueError):
            delta = 0

        if delta != 0:
            if delta > 0:
                self.event_generate('<<Increment>>')
            else:
                self.event_generate('<<Decrement>>')
        return 'break'

    def _handle_wheel_up(self, event):
        """Handle mouse wheel up on Linux/X11."""
        if not self._is_interactive():
            return 'break'
        self.event_generate('<<Increment>>')
        return 'break'

    def _handle_wheel_down(self, event):
        """Handle mouse wheel down on Linux/X11."""
        if not self._is_interactive():
            return 'break'
        self.event_generate('<<Decrement>>')
        return 'break'

    def _handle_increment_event(self, event):
        """Handle <<Increment>> event by stepping up."""
        if not self._is_interactive():
            return 'break'
        self.step(+1)

    def _handle_decrement_event(self, event):
        """Handle <<Decrement>> event by stepping down."""
        if not self._is_interactive():
            return 'break'
        self.step(-1)

    def _apply_bounds(self, x: float) -> float:
        """Apply min/max bounds with optional wrapping."""
        lo = float(self._minvalue) if self._minvalue is not None else None
        hi = float(self._maxvalue) if self._maxvalue is not None else None

        if self._wrap and lo is not None and hi is not None:
            if hi <= lo:
                return lo

            span = hi - lo
            while x < lo:
                x += span
            while x > hi:
                x -= span
            return x

        if lo is not None and x < lo:
            x = lo
        if hi is not None and x > hi:
            x = hi

        return x

    def _is_interactive(self) -> bool:
        """Return True if the widget is not readonly or disabled."""
        current_states = self.state()
        return 'disabled' not in current_states and 'readonly' not in current_states

    def step(self, n: int = 1):
        """Increment or decrement value by n steps."""
        if not self._is_interactive():
            return self
        # Get current value (default to min if None)
        current = self._value
        if current is None:
            base = float(self._minvalue) if self._minvalue is not None else 0.0
        else:
            base = float(current)

        # Calculate new value
        new_value = base + float(self._increment) * float(n)

        # Apply bounds/wrapping
        new_value = self._apply_bounds(new_value)

        # Coerce to desired type
        if self._num_type is float:
            coerced = float(new_value)
        else:
            coerced = int(round(new_value))

        # Store previous value for change detection
        prev_value = self._value

        # Update internal value
        self._value = coerced

        # Update display
        self._normalize_display_from_value()

        # Emit changed event if value actually changed
        if self._value != prev_value:
            self._prev_changed_value = self._value
            self.event_generate(
                '<<Change>>', data={
                    "value": self._value,
                    "prev_value": prev_value,
                    "text": self.textsignal.get()
                })

        return self

    def _normalize_display_from_value(self):
        """Update display text from internal value without triggering input events."""
        # Format the value
        new_text = self._format_value(self._value)

        # Only update if text changed
        if new_text != self.textsignal.get():
            # Temporarily unsubscribe from input signal to avoid spurious events
            fid = getattr(self, '_on_input_fid', None)
            if fid:
                try:
                    self.textsignal.unsubscribe(fid)
                except Exception:
                    pass

            # Update display
            self.textsignal.set(new_text)

            # Re-subscribe to input signal
            if fid:
                self._on_input_fid = self.textsignal.subscribe(self._handle_change)

    def commit(self):
        """Override commit to apply bounds validation after parsing.

        This ensures user-entered values are constrained to valid range.
        """
        # Call parent commit to parse and format
        super().commit()

        # Apply bounds to the parsed value
        if self._value is not None:
            bounded_value = self._apply_bounds(float(self._value))

            # Coerce to appropriate type
            if self._num_type is float:
                self._value = float(bounded_value)
            else:
                self._value = int(round(bounded_value))

            # Update display if value changed due to bounds
            self._normalize_display_from_value()

    def on_increment(self, callback):
        """Bind callback to <<Increment>> event."""
        return self.bind('<<Increment>>', callback, add=True)

    def off_increment(self, funcid: str):
        """Remove callback from <<Increment>> event."""
        self.unbind('<<Increment>>', funcid)

    def on_decrement(self, callback):
        """Bind callback to <<Decrement>> event."""
        return self.bind('<<Decrement>>', callback, add=True)

    def off_decrement(self, funcid: str):
        """Remove callback from <<Decrement>> event."""
        self.unbind('<<Decrement>>', funcid)

    @configure_delegate('minvalue')
    def _delegate_minvalue(self, value: Union[int, float]):
        """Get or set the minimum allowed value and re-validate current value."""
        if value is None:
            return self._minvalue

        self._minvalue = value
        if self._value is not None:
            self._value = self._apply_bounds(float(self._value))
            self._normalize_display_from_value()

    @configure_delegate('maxvalue')
    def _delegate_maxvalue(self, value: Union[int, float]):
        """Get or set the maximum allowed value and re-validate current value."""
        if value is None:
            return self._maxvalue

        self._maxvalue = value
        if self._value is not None:
            self._value = self._apply_bounds(float(self._value))
            self._normalize_display_from_value()

    @configure_delegate('increment')
    def _delegate_increment(self, value: Union[int, float]):
        """Get or set the step increment value."""
        if value is None:
            return self._increment

        self._increment = value

    @configure_delegate('wrap')
    def _delegate_wrap(self, value: bool):
        """Get or set the wrap setting."""
        if value is None:
            return self._wrap

        self._wrap = bool(value)
