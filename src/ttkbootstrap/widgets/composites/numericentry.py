"""Numeric entry field widget with spin buttons.

Provides a specialized entry field for numeric input with increment/decrement
buttons and keyboard/mouse wheel support.
"""

from typing import Any
from tkinter import TclError
from typing_extensions import Unpack

from ttkbootstrap.widgets.primitives.button import Button
from ttkbootstrap.widgets.composites.field import Field, FieldOptions
from ttkbootstrap.widgets.mixins import configure_delegate
from ttkbootstrap.widgets.types import Master


class NumericEntry(Field):
    """A numeric entry field widget with increment/decrement spin buttons.

    Extends Field to provide numeric input with spin buttons, bounds validation,
    keyboard stepping (Up/Down arrows), mouse wheel support, and optional wrapping.

    !!! note "Events"

        - ``<<Increment>>``: Fired when increment is requested (before step occurs).
        - ``<<Decrement>>``: Fired when decrement is requested (before step occurs).
        - ``<<Change>>``: Fired when value changes after commit.
        - ``<<Input>>``: Fired on each keystroke.
        - ``<<Valid>>``: Fired when validation passes.
        - ``<<Invalid>>``: Fired when validation fails.

    Attributes:
        entry_widget (NumberEntryPart): The underlying entry widget.
        label_widget (Label): The label widget.
        message_widget (Label): The message label widget.
        addons (dict[str, Widget]): Dictionary of inserted addon widgets by name.
        variable (Variable): Tkinter Variable linked to entry text.
        signal (Signal): Signal object for reactive updates.
    """

    def __init__(
            self,
            master: Master = None,
            value: int | float = 0,
            label: str = None,
            message: str = None,
            show_spin_buttons: bool = True,
            minvalue: int | float | None = None,
            maxvalue: int | float | None = None,
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
            value (int | float): Initial numeric value to display.
            label (str): Optional label text to display above the entry field.
                If ``required=True``, an asterisk (*) is automatically appended.
            message (str): Optional message text to display below the entry field.
                Used for hints or help text. Replaced by validation errors when
                validation fails.
            show_spin_buttons (bool): If True, displays increment/decrement buttons
                (plus and minus icons) to the right of the entry.
            minvalue (int | float): Minimum allowed value (inclusive). Values below
                this will be clamped or wrapped depending on the wrap setting.
            maxvalue (int | float): Maximum allowed value (inclusive). Values above
                this will be clamped or wrapped depending on the wrap setting.
            increment (int | float): Step size for increment/decrement operations.

        Other Parameters:
            wrap (bool): If True, values wrap around at min/max boundaries.
            value_format (str): Number format specification for IntlFormatter.
                Examples: ``'decimal'``, ``'percent'``, ``'currency'``, ``'#,##0.00'``.
            locale (str): Locale identifier for number formatting (e.g., ``'en_US'``).
            required (bool): If True, field cannot be empty.
            accent (str): Accent token for the focus ring and active border.
            bootstyle (str): DEPRECATED - Use `accent` instead.
            allow_blank (bool): If True, empty input is allowed (sets value to None).
            cursor (str): Cursor style when hovering.
            exportselection (bool): Export selection to clipboard.
            font (str): Font for text display.
            foreground (str): Text color.
            initial_focus (bool): If True, widget receives focus on creation.
            justify (str): Text alignment (``'left'``, ``'center'``, ``'right'``).
            show_message (bool): If True, displays message area.
            padding (int | tuple): Padding around entry widget.
            takefocus (bool): If True, widget accepts Tab focus.
            textvariable (Variable): Tkinter Variable to link with text.
            textsignal (Signal): Signal object for reactive updates.
            width (int): Width in characters.
            xscrollcommand (Callable): Callback for horizontal scrolling.
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
            Button, position="after", name="decrement", icon="dash", command=self.decrement, icon_only=True)
        self.insert_addon(
            Button, position="after", name="increment", icon="plus", command=self.increment, icon_only=True)
        self._delegate_show_spin_buttons(show_spin_buttons)

        self.entry_widget.bind('<<StateChanged>>', self._on_entry_state_changed, add=True)
        self._update_spin_button_states()

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
        if not self._entry_is_interactive():
            return
        self.entry_widget.event_generate("<<Increment>>")

    def decrement(self):
        """Decrement the numeric value by one step."""
        if not self._entry_is_interactive():
            return
        self.entry_widget.event_generate("<<Decrement>>")

    def _entry_is_interactive(self) -> bool:
        """Return True if the entry widget is not disabled or readonly."""
        state = self.entry_widget.state()
        return 'disabled' not in state and 'readonly' not in state

    def _on_entry_state_changed(self, _: Any = None):
        """Sync spin buttons whenever the entry state mutates."""
        self._update_spin_button_states()

    def _update_spin_button_states(self):
        """Enable or disable spin buttons based on entry interactivity."""
        state_value = 'disabled' if not self._entry_is_interactive() else '!disabled'
        for control in (self.increment_widget, self.decrement_widget):
            try:
                control.configure(state=state_value)
            except TclError:
                pass

    @configure_delegate('show_spin_buttons')
    def _delegate_show_spin_buttons(self, value: bool = None):
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
