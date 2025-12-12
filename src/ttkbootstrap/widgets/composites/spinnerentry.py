"""Spinner entry field widget.

Provides a specialized entry field with a built-in spinbox for selecting
values from a list or numeric range.
"""

from typing import List, Union
from typing_extensions import Unpack

from ttkbootstrap.widgets.composites.field import Field, FieldOptions
from ttkbootstrap.widgets.mixins import configure_delegate


class SpinnerEntry(Field):
    """A spinner entry field widget with built-in spin controls.

    SpinnerEntry extends the Field widget to provide a spinbox input that can
    handle both predefined text values and numeric ranges. The widget includes
    built-in up/down arrow buttons and supports keyboard/mouse wheel interaction.

    Features:
        - Built-in spinner controls (up/down arrows)
        - Text values mode: Cycle through predefined list
        - Numeric range mode: Select from min to max with increment
        - Keyboard support (Up/Down arrows)
        - Mouse wheel support for adjusting values
        - Optional value wrapping at boundaries
        - Locale-aware number formatting
        - All Field features (label, validation, messages, etc.)

    Events (forwarded from SpinnerEntryPart):
        <<Changed>>: Fired when value changes after commit
        <<Input>>: Fired on each keystroke
        <<Valid>>: Fired when validation passes
        <<Invalid>>: Fired when validation fails

    Example:
        ```python
        import ttkbootstrap as ttk
        from ttkbootstrap.widgets.composites.spinnerentry import SpinnerEntry

        root = ttk.Window()

        # Text spinner with predefined values
        size = SpinnerEntry(
            root,
            label="T-Shirt Size",
            values=['XS', 'S', 'M', 'L', 'XL', 'XXL'],
            value='M',
            message="Select your size"
        )
        size.pack(padx=20, pady=10, fill='x')

        # Numeric spinner with range
        quantity = SpinnerEntry(
            root,
            label="Quantity",
            value=1,
            minvalue=1,
            maxvalue=100,
            increment=1,
            message="Enter quantity"
        )
        quantity.pack(padx=20, pady=10, fill='x')

        # Spinner with wrapping
        priority = SpinnerEntry(
            root,
            label="Priority",
            values=['Low', 'Medium', 'High'],
            value='Medium',
            wrap=True
        )
        priority.pack(padx=20, pady=10, fill='x')

        # Currency spinner with formatting
        price = SpinnerEntry(
            root,
            label="Price",
            value=99.99,
            minvalue=0,
            maxvalue=1000,
            increment=10,
            value_format='¤#,##0.00'
        )
        price.pack(padx=20, pady=10, fill='x')

        # Get the value
        def on_submit():
            print(f"Size: {size.value}")
            print(f"Quantity: {quantity.value}")
            print(f"Priority: {priority.value}")
            print(f"Price: {price.value}")

        ttk.Button(root, text="Submit", command=on_submit).pack(pady=10)

        root.mainloop()
        ```

    Inherited Properties:
        entry_widget: Access to the underlying SpinnerEntryPart widget
        label_widget: Access to the label widget
        message_widget: Access to the message label widget
        addons: Dictionary of inserted addon widgets
        variable: Tkinter Variable linked to entry text
        signal: Signal object for reactive updates
    """

    def __init__(
            self,
            master=None,
            value: Union[int, float, str] = '',
            label: str = None,
            message: str = None,
            values: List[str] = None,
            minvalue: Union[int, float] = None,
            maxvalue: Union[int, float] = None,
            increment: Union[int, float] = 1,
            wrap: bool = False,
            **kwargs: Unpack[FieldOptions]
    ):
        """Initialize a SpinnerEntry widget.

        Creates a spinner entry field with optional label, validation, and either
        a predefined list of values or a numeric range. The widget includes built-in
        up/down arrows for cycling through values or adjusting numbers.

        Args:
            master: Parent widget. If None, uses the default root window.
            value: Initial value to display. Can be string, integer, or float
                depending on whether using text values or numeric range.
                Default is empty string.
            label: Optional label text to display above the entry field.
                If required=True, an asterisk (*) is automatically appended.
            message: Optional message text to display below the entry field.
                Used for hints or help text. Replaced by validation errors when
                validation fails.
            values: List of valid string values for the spinner. If provided,
                the spinner cycles through these values. Mutually exclusive with
                minvalue/maxvalue/increment. Example: ['Low', 'Medium', 'High']
            minvalue: Minimum numeric value (inclusive). Only used for numeric spinners.
                If provided along with 'maxvalue', creates a numeric range spinner.
            maxvalue: Maximum numeric value (inclusive). Only used for numeric spinners.
                If provided along with 'minvalue', creates a numeric range spinner.
            increment: Step size for increment/decrement in numeric mode.
                Default is 1. Only applies when using minvalue/maxvalue.
            wrap: If True, values wrap around at boundaries (cycle back to start
                after reaching end). If False, stops at min/max boundaries.
                Default is False.
            **kwargs: Additional keyword arguments from FieldOptions:
                value_format: ICU format pattern for parsing/formatting
                    (e.g., '¤#,##0.00' for currency, '#,##0.00' for decimal)
                locale: Locale identifier for formatting (e.g., 'en_US')
                required: If True, field cannot be empty
                bootstyle: The accent color of the focus ring and active border
                allow_blank: If True, empty input is allowed (sets value to None)
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
            Use either 'values' (for text mode) OR 'minvalue/maxvalue' (for numeric mode),
            not both. If both are provided, 'values' takes precedence.

        Example:
            ```python
            # Text mode
            spinner1 = SpinnerEntry(
                root,
                values=['Small', 'Medium', 'Large'],
                value='Medium'
            )

            # Numeric mode
            spinner2 = SpinnerEntry(
                root,
                minvalue=0,
                maxvalue=100,
                increment=5,
                value=50
            )
            ```
        """
        # Build kwargs for Field initialization
        # Map minvalue/maxvalue to from_/to for the underlying Spinbox
        field_kwargs = {
            'values': values,
            'from_': minvalue,
            'to': maxvalue,
            'increment': increment,
            'wrap': wrap,
        }
        field_kwargs.update(kwargs)

        super().__init__(
            master,
            value=value,
            label=label,
            message=message,
            kind="spinbox",
            **field_kwargs
        )

        # Store configuration
        self._values = values
        self._minvalue = minvalue
        self._maxvalue = maxvalue
        self._increment = increment
        self._wrap = wrap

    @property
    def values(self) -> List[str]:
        """Get the list of valid values (text mode only)."""
        return self._values

    @configure_delegate('values')
    def _delegate_values(self, value: List[str] = None):
        """Get or set the list of valid values.

        Can be accessed via:
            widget.configure(values=['A', 'B', 'C'])
            widget['values'] = ['A', 'B', 'C']
            widget.cget('values')
        """
        if value is None:
            return self._values

        self._values = value
        # Update the underlying spinbox
        try:
            self.entry_widget.configure(values=value)
        except Exception:
            pass
        return None

    @configure_delegate('minvalue')
    def _delegate_minvalue(self, value: Union[int, float] = None):
        """Get or set the minimum value (numeric mode).

        Can be accessed via:
            widget.configure(minvalue=0)
            widget['minvalue'] = 0
            widget.cget('minvalue')
        """
        if value is None:
            return self._minvalue

        self._minvalue = value
        # Update the underlying spinbox (uses from_)
        try:
            self.entry_widget.configure(from_=value)
        except Exception:
            pass
        return None

    @configure_delegate('maxvalue')
    def _delegate_maxvalue(self, value: Union[int, float] = None):
        """Get or set the maximum value (numeric mode).

        Can be accessed via:
            widget.configure(maxvalue=100)
            widget['maxvalue'] = 100
            widget.cget('maxvalue')
        """
        if value is None:
            return self._maxvalue

        self._maxvalue = value
        # Update the underlying spinbox (uses to)
        try:
            self.entry_widget.configure(to=value)
        except Exception:
            pass
        return None

    @configure_delegate('increment')
    def _delegate_increment(self, value: Union[int, float] = None):
        """Get or set the increment step size (numeric mode).

        Can be accessed via:
            widget.configure(increment=5)
            widget['increment'] = 5
            widget.cget('increment')
        """
        if value is None:
            return self._increment

        self._increment = value
        # Update the underlying spinbox
        try:
            self.entry_widget.configure(increment=value)
        except Exception:
            pass
        return None

    @configure_delegate('wrap')
    def _delegate_wrap(self, value: bool = None):
        """Get or set the wrap setting.

        Can be accessed via:
            widget.configure(wrap=True)
            widget['wrap'] = True
            widget.cget('wrap')
        """
        if value is None:
            return self._wrap

        self._wrap = bool(value)
        # Update the underlying spinbox
        try:
            self.entry_widget.configure(wrap=value)
        except Exception:
            pass
        return None