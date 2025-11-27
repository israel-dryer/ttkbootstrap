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
        <<Increment>>: Fired when value is incremented
            event.data = {"value": numeric_value}

        <<Decrement>>: Fired when value is decremented
            event.data = {"value": numeric_value}

        Plus all events from TextEntryPart:
            <<Input>>, <<Changed>>, <Return>

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
            value: Union[int, float, str] = 0,
            value_format: str = None,
            minvalue: Union[int, float] = 0,
            maxvalue: Union[int, float] = 100,
            increment: Union[int, float] = 1,
            wrap: bool = False,
            initial_focus: bool = False,
            allow_blank: bool = True,
            locale: str = None,
            **kwargs
    ):
        """Initialize a NumberEntryPart widget.

        Args:
            master: Parent widget
            value: Initial numeric value (int, float, or string representation)
            value_format: Number format specification for IntlFormatter.
                Examples: 'decimal', 'percent', 'currency', '#,##0.00', etc.
            minvalue: Minimum allowed value (inclusive)
            maxvalue: Maximum allowed value (inclusive)
            increment: Step size for increment/decrement operations
            wrap: If True, values wrap around at min/max boundaries.
                If False, values are clamped at boundaries.
            initial_focus: If True, widget receives focus on creation
            allow_blank: If True, empty input is allowed (sets value to None)
            locale: Locale identifier for number formatting (e.g., 'en_US')
            **kwargs: Additional keyword arguments passed to TextEntryPart

        Example:
            ```python
            # Integer entry from 0-100 with step of 5
            entry1 = NumberEntryPart(
                root,
                value=50,
                minvalue=0,
                maxvalue=100,
                increment=5
            )

            # Decimal entry with 2 decimal places
            entry2 = NumberEntryPart(
                root,
                value=3.14,
                minvalue=0.0,
                maxvalue=10.0,
                increment=0.01,
                value_format='#,##0.00'
            )

            # Wrapping entry (like a clock)
            entry3 = NumberEntryPart(
                root,
                value=0,
                minvalue=0,
                maxvalue=23,
                increment=1,
                wrap=True
            )
            ```
        """
        # Store numeric configuration
        self._minvalue = minvalue
        self._maxvalue = maxvalue
        self._increment = increment
        self._wrap = wrap

        # Determine numeric type (float if any parameter is float)
        self._num_type = float if any(
            isinstance(x, float) or (isinstance(x, (int, float)) and float(x) != int(x))
            for x in (minvalue, maxvalue, increment, value if not isinstance(value, str) else 0)
        ) else int

        # Initialize base TextEntryPart
        # Convert initial value to appropriate type
        if isinstance(value, str):
            initial_value = value
        else:
            initial_value = self._num_type(value)

        super().__init__(
            master=master,
            value=initial_value,
            value_format=value_format,
            initial_focus=initial_focus,
            allow_blank=allow_blank,
            locale=locale,
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
        self.bind('<Up>', self._handle_up_key)
        self.bind('<Down>', self._handle_down_key)

        # Bind mouse wheel (Windows/macOS)
        self.bind('<MouseWheel>', self._handle_mouse_wheel)

        # Bind mouse wheel (Linux/X11)
        self.bind('<Button-4>', self._handle_wheel_up)
        self.bind('<Button-5>', self._handle_wheel_down)

    def _handle_up_key(self, event):
        """Handle Up arrow key press - increment value."""
        self.step(+1)
        return 'break'  # Prevent default behavior

    def _handle_down_key(self, event):
        """Handle Down arrow key press - decrement value."""
        self.step(-1)
        return 'break'  # Prevent default behavior

    def _handle_mouse_wheel(self, event):
        """Handle mouse wheel on Windows/macOS."""
        try:
            delta = int(event.delta)
        except (AttributeError, ValueError):
            delta = 0

        if delta != 0:
            self.step(+1 if delta > 0 else -1)
        return 'break'

    def _handle_wheel_up(self, event):
        """Handle mouse wheel up on Linux/X11."""
        self.step(+1)
        return 'break'

    def _handle_wheel_down(self, event):
        """Handle mouse wheel down on Linux/X11."""
        self.step(-1)
        return 'break'

    def _apply_bounds(self, x: float) -> float:
        """Apply min/max bounds with optional wrapping.

        Args:
            x: Input value to constrain

        Returns:
            Value constrained to [min_value, max_value] range
        """
        lo, hi = float(self._minvalue), float(self._maxvalue)

        if not self._wrap:
            # Clamp to bounds
            return min(max(x, lo), hi)

        # Wrap around bounds
        if hi <= lo:
            return lo

        span = hi - lo
        # Normalize with wrap (handle large jumps gracefully)
        while x < lo:
            x += span
        while x > hi:
            x -= span
        return x

    def step(self, n: int = 1):
        """Increment or decrement value by n steps.

        Updates the internal value, applies bounds/wrapping, formats
        the display, and emits appropriate events.

        Args:
            n: Number of steps to increment (positive) or decrement (negative)

        Returns:
            Self for method chaining

        Example:
            ```python
            entry.step(1)   # Increment by one step
            entry.step(-2)  # Decrement by two steps
            entry.step(5)   # Increment by five steps
            ```
        """
        # Get current value (default to min if None)
        current = self._value
        if current is None:
            base = float(self._minvalue)
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

        # Emit increment/decrement event
        event_name = '<<Increment>>' if n > 0 else '<<Decrement>>'
        self.event_generate(event_name, data={"value": self._value})

        # Emit changed event if value actually changed
        if self._value != prev_value:
            self._prev_changed_value = self._value
            self.event_generate(
                '<<Changed>>', data={
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
        """Bind callback to <<Increment>> event.

        Args:
            callback: Function receiving event.data = {"value": numeric_value}

        Returns:
            Binding identifier
        """
        return self.bind('<<Increment>>', callback)

    def off_increment(self, funcid: str):
        """Remove callback from <<Increment>> event."""
        self.unbind('<<Increment>>', funcid)

    def on_decrement(self, callback):
        """Bind callback to <<Decrement>> event.

        Args:
            callback: Function receiving event.data = {"value": numeric_value}

        Returns:
            Binding identifier
        """
        return self.bind('<<Decrement>>', callback)

    def off_decrement(self, funcid: str):
        """Remove callback from <<Decrement>> event."""
        self.unbind('<<Decrement>>', funcid)

    # Configuration delegation for min_value, max_value, increment, and wrap
    @configure_delegate('minvalue')
    def _delegate_minvalue(self, value: Union[int, float]):
        """Set the minimum allowed value and re-validate current value.

        Can be accessed via:
            widget.configure(minvalue=10)
            widget['minvalue'] = 10
            widget.cget('minvalue')
        """
        self._minvalue = value
        if self._value is not None:
            self._value = self._apply_bounds(float(self._value))
            self._normalize_display_from_value()

    @configure_delegate('maxvalue')
    def _delegate_maxvalue(self, value: Union[int, float]):
        """Set the maximum allowed value and re-validate current value.

        Can be accessed via:
            widget.configure(maxvalue=100)
            widget['maxvalue'] = 100
            widget.cget('maxvalue')
        """
        self._maxvalue = value
        if self._value is not None:
            self._value = self._apply_bounds(float(self._value))
            self._normalize_display_from_value()

    @configure_delegate('increment')
    def _delegate_increment(self, value: Union[int, float]):
        """Set the step increment value.

        Can be accessed via:
            widget.configure(increment=5)
            widget['increment'] = 5
            widget.cget('increment')
        """
        self._increment = value

    @configure_delegate('wrap')
    def _delegate_wrap(self, value: bool):
        """Set the wrap setting.

        Can be accessed via:
            widget.configure(wrap=True)
            widget['wrap'] = True
            widget.cget('wrap')
        """
        self._wrap = bool(value)
