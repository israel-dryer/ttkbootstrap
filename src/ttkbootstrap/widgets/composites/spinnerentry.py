"""Spinner entry field widget.

Provides a specialized entry field with a built-in spinbox for selecting
values from a list or numeric range.
"""

from typing import List, Union

from typing_extensions import Unpack

from ttkbootstrap.widgets.composites.field import Field, FieldOptions
from ttkbootstrap.widgets.mixins import configure_delegate
from ttkbootstrap.widgets.types import Master


class SpinnerEntry(Field):
    """A spinner entry field widget with built-in spin controls.

    SpinnerEntry extends the Field widget to provide a spinbox input that can
    handle both predefined text values and numeric ranges. The widget includes
    built-in up/down arrow buttons and supports keyboard/mouse wheel interaction.

    !!! note "Events"

        - ``<<Change>>``  : Fired when value changes after commit.
        - ``<<Input>>``   : Fired on each keystroke.
        - ``<<Valid>>``   : Fired when validation passes.
        - ``<<Invalid>>`` : Fired when validation fails.

    Attributes:
        entry_widget (SpinnerEntryPart): The underlying spinbox entry widget.
        label_widget (Label): The label widget above the entry.
        message_widget (Label): The message label widget below the entry.
        addons (dict[str, Widget]): Dictionary of inserted addon widgets by name.
        variable (Variable): Tkinter Variable linked to entry text.
        signal (Signal): Signal object for reactive updates.
    """

    def __init__(
            self,
            master: Master = None,
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
            wrap: If True, values wrap around at boundaries. Default is False.

        Other Parameters:
            value_format (str): ICU format pattern for parsing/formatting.
            locale (str): Locale identifier for formatting (e.g., 'en_US').
            required (bool): If True, field cannot be empty.
            color (str): Color token for the focus ring and active border.
            bootstyle (str): DEPRECATED - Use `color` instead.
            allow_blank (bool): If True, empty input is allowed.
            cursor (str): Cursor style when hovering.
            font (str): Font for text display.
            foreground (str): Text color.
            initial_focus (bool): If True, widget receives focus on creation.
            justify (str): Text alignment.
            show_message (bool): If True, displays message area.
            padding (str): Padding around entry widget.
            take_focus (bool): If True, widget accepts Tab focus.
            textvariable (Variable): Tkinter Variable to link with text.
            textsignal (Signal): Signal object for reactive updates.
            width (int): Width in characters.

        Note:
            Use either 'values' (for text mode) OR 'minvalue/maxvalue' (for numeric mode),
            not both. If both are provided, 'values' takes precedence.
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
