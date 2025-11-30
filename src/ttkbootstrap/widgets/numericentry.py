"""Numeric entry field widget with spin buttons.

Provides a specialized entry field for numeric input with increment/decrement
buttons and keyboard/mouse wheel support.
"""

from typing_extensions import Unpack

from ttkbootstrap.widgets.button import Button
from ttkbootstrap.widgets.field import Field, FieldOptions
from ttkbootstrap.widgets.mixins import configure_delegate


class NumericEntry(Field):
    """A numeric entry field widget with increment/decrement spin buttons.

    NumericEntry extends the Field widget to provide specialized numeric input
    with built-in spin buttons for incrementing and decrementing values. The
    widget includes bounds validation, keyboard stepping (Up/Down arrows), mouse
    wheel support, and optional value wrapping.

    Features:
        - Increment/decrement spin buttons (plus/minus icons)
        - Keyboard stepping with Up/Down arrow keys
        - Mouse wheel support for adjusting values
        - Min/max bounds validation
        - Optional value wrapping at boundaries
        - Locale-aware number formatting
        - All Field features (label, validation, messages, etc.)

    Events (forwarded from NumberEntryPart):
        <<Increment>>: Fired when increment is requested (before step occurs)
        <<Decrement>>: Fired when decrement is requested (before step occurs)
        <<Changed>>: Fired when value changes after commit
        <<Input>>: Fired on each keystroke
        <<Valid>>: Fired when validation passes
        <<Invalid>>: Fired when validation fails

    Example:
        ```python
        import ttkbootstrap as ttk
        from ttkbootstrap.widgets.numericentry import NumericEntry

        root = ttk.Window()

        # Basic numeric entry with spin buttons
        age = NumericEntry(
            root,
            label="Age",
            value=25,
            minvalue=0,
            maxvalue=120,
            message="Enter your age"
        )
        age.pack(padx=20, pady=10, fill='x')

        # Currency entry with formatting
        price = NumericEntry(
            root,
            label="Price",
            value=99.99,
            minvalue=0,
            maxvalue=10000,
            increment=0.01,
            value_format='$#,##0.00'
        )
        price.pack(padx=20, pady=10, fill='x')

        # Percentage with wrapping
        percent = NumericEntry(
            root,
            label="Percentage",
            value=50,
            minvalue=0,
            maxvalue=100,
            increment=5,
            wrap=True
        )
        percent.pack(padx=20, pady=10, fill='x')

        # Without spin buttons
        quantity = NumericEntry(
            root,
            label="Quantity",
            value=1,
            show_spin_buttons=False
        )
        quantity.pack(padx=20, pady=10, fill='x')

        # Bind to increment event
        def on_increment(event):
            print("Value incremented")

        age.on_increment(on_increment)

        root.mainloop()
        ```

    Inherited Properties:
        entry_widget: Access to the underlying NumberEntryPart widget
        label_widget: Access to the label widget
        message_widget: Access to the message label widget
        addons: Dictionary of inserted addon widgets
        variable: Tkinter Variable linked to entry text
        signal: Signal object for reactive updates
    """

    def __init__(
            self,
            master=None,
            value: int | float = 0,
            label: str = None,
            message: str = None,
            show_spin_buttons: bool = True,
            minvalue: int | float = 0,
            maxvalue: int | float = 100,
            increment: int | float = 1,
            **kwargs: Unpack[FieldOptions]
    ):
        """Initialize a NumericEntry widget.

        Creates a numeric entry field with optional label, validation, bounds
        constraints, and increment/decrement spin buttons. The widget supports
        keyboard stepping (Up/Down arrows), mouse wheel interaction, and optional
        value wrapping at boundaries.

        Args:
            master: Parent widget. If None, uses the default root window.
            value: Initial numeric value to display. Can be integer or float.
                Default is 0.
            label: Optional label text to display above the entry field.
                If required=True, an asterisk (*) is automatically appended.
            message: Optional message text to display below the entry field.
                Used for hints or help text. Replaced by validation errors when
                validation fails.
            show_spin_buttons: If True, displays increment/decrement buttons
                (plus and minus icons) to the right of the entry. If False,
                hides the spin buttons. Default is True.
            minvalue: Minimum allowed value (inclusive). Values below this will
                be clamped or wrapped depending on the wrap setting. Default is 0.
            maxvalue: Maximum allowed value (inclusive). Values above this will
                be clamped or wrapped depending on the wrap setting. Default is 100.
            increment: Step size for increment/decrement operations. Default is 1.
            **kwargs: Additional keyword arguments from FieldOptions:
                wrap: If True, values wrap around at min/max boundaries. If False,
                    values are clamped at boundaries. Default is False.
                value_format: Number format specification for IntlFormatter.
                    Examples: 'decimal', 'percent', 'currency', '#,##0.00'
                locale: Locale identifier for number formatting (e.g., 'en_US')
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
        """
        super().__init__(
            master, value=value, label=label, message=message, minvalue=minvalue, maxvalue=maxvalue, kind="numeric",
            increment=increment, **kwargs)

        self._show_spin_buttons = show_spin_buttons

        # passthrough methods
        self.on_increment = self.entry_widget.on_increment
        self.off_increment = self.entry_widget.off_increment
        self.on_decrement = self.entry_widget.on_decrement
        self.off_decrement = self.entry_widget.off_decrement
        self.step = self.entry_widget.step

        # pack info
        self._increment_pack_info = {}
        self._decrement_pack_info = {}

        # buttons
        self.insert_addon(
            Button, position="after", name="increment", icon="plus", command=self.increment, icon_only=True)
        self.insert_addon(
            Button, position="after", name="decrement", icon="dash", command=self.decrement, icon_only=True)
        self._config_show_spin_buttons(show_spin_buttons)

    @property
    def increment_widget(self):
        """Get the increment spin button widget."""
        return self.addons['increment']

    @property
    def decrement_widget(self):
        """Get the decrement spin button widget."""
        return self.addons['decrement']

    def increment(self):
        """Increment the numeric value by one step."""
        self.entry_widget.event_generate("<<Increment>>")

    def decrement(self):
        """Decrement the numeric value by one step."""
        self.entry_widget.event_generate("<<Decrement>>")

    @configure_delegate('show_spin_buttons')
    def _config_show_spin_buttons(self, value: bool = None):
        """Get or set the visibility of spin buttons."""
        if value is None:
            return self._show_spin_buttons
        else:
            self._show_spin_buttons = value
            if value:
                if not self.increment_widget.winfo_ismapped():
                    self.increment_widget.pack(**self._increment_pack_info)
                if not self.decrement_widget.winfo_ismapped():
                    self.decrement_widget.pack(**self._decrement_pack_info)
            else:
                self._increment_pack_info = self.increment_widget.pack_info()
                self._decrement_pack_info = self.decrement_widget.pack_info()
                self.increment_widget.pack_forget()
                self.decrement_widget.pack_forget()
        return None
