from __future__ import annotations

from tkinter import StringVar
from typing import Any, Callable, Literal, TYPE_CHECKING

from typing_extensions import TypedDict, Unpack

from ttkbootstrap.widgets.primitives.radiobutton import RadioButton
from ttkbootstrap.widgets.primitives.label import Label
from ttkbootstrap.widgets.mixins.configure_mixin import configure_delegate
from ttkbootstrap.widgets.primitives import Frame
from ttkbootstrap.widgets.types import Master

if TYPE_CHECKING:
    from ttkbootstrap.core.signals import Signal
    import tkinter as tk


class RadioGroupKwargs(TypedDict, total=False):
    variable: Any
    signal: Signal[Any]
    value: str
    orient: Literal['horizontal', 'vertical']
    color: str
    text: str
    labelanchor: Literal['n', 's', 'e', 'w', 'ne', 'nw', 'se', 'sw']
    state: Literal['normal', 'disabled']
    show_border: bool
    surface_color: str
    style_options: dict[str, Any]
    # Frame options
    padding: Any
    width: int
    height: int


class RadioGroup(Frame):
    """A group of radio buttons with automatic state tracking and optional label.

    The RadioGroup widget provides a convenient way to create groups of radio
    buttons with automatic state management. It supports both horizontal and
    vertical orientations, and can display an optional label in various positions.

    Attributes:
        variable (Variable): The underlying tk.Variable for the selected value.
        signal (Signal): Signal for reactive programming and change subscriptions.
    """

    def __init__(self, master: Master = None, **kwargs: Unpack[RadioGroupKwargs]):
        """Initialize the RadioGroup.

        Args:
            master: Parent widget. If None, uses the default root window.

        Other Parameters:
            orient (str): Layout orientation - 'horizontal' (default) or 'vertical'.
            color (str): Color token for styling (e.g., 'primary', 'success', 'danger').
                Defaults to 'primary'.
            bootstyle (str): DEPRECATED - Use `color` instead.
            text (str): Optional label text to display.
            labelanchor (str): Label position - 'n' (top, default), 's' (bottom),
                'e' (right), 'w' (left), or combinations like 'nw', 'ne', etc.
            variable (Variable): Optional tk.StringVar for controlling the selected value.
            signal (Signal): Optional Signal instance for reactive programming.
            value (str): Initial selected value.
            state (str): Initial state for all buttons - 'normal' (default) or 'disabled'.
            show_border (bool): If True, draws a border around the group.
            surface_color (str): Optional surface token; otherwise inherited.
            style_options (dict): Additional style options passed to child buttons.
            padding (int | tuple): Frame padding. Defaults to 1.
            width (int): Requested width in pixels.
            height (int): Requested height in pixels.
        """
        # Extract RadioGroup-specific options before super().__init__
        self._orientation = kwargs.pop('orient', 'horizontal')
        # Support both 'color' and legacy 'bootstyle'
        self._color = kwargs.pop('color', None) or kwargs.pop('bootstyle', 'primary')
        self._labeltext = kwargs.pop('text', None)
        self._labelanchor = kwargs.pop('labelanchor', 'n')
        self._state = kwargs.pop('state', 'normal')

        # Handle signal/variable/value
        initial_value = kwargs.pop('value', None)
        style_options = kwargs.pop('style_options', {})

        # Initialize internal state
        self._buttons: dict[str, RadioButton] = {}
        self._label: Label | None = None
        self._button_container: Frame | None = None

        # Extract signal/variable before Frame init
        signal_value = kwargs.pop('signal', None)
        variable_value = kwargs.pop('variable', None)

        # Handle padding default
        if 'padding' not in kwargs:
            kwargs['padding'] = 1

        # Call super().__init__() - just Frame now
        super().__init__(master, style_options=style_options, **kwargs)

        # Handle variable/signal setup manually
        if signal_value is not None:
            # Signal provided - extract its variable
            self._signal = signal_value
            self._variable = signal_value.var
        elif variable_value is not None:
            # Variable provided - wrap in Signal
            from ttkbootstrap.core.signals import Signal
            self._variable = variable_value
            self._signal = Signal.from_variable(variable_value)
            # Set initial value if provided
            if initial_value is not None:
                self._variable.set(initial_value)
        else:
            # Neither provided - create internal variable
            from ttkbootstrap.core.signals import Signal
            internal_var = StringVar(value=initial_value or '')
            self._variable = internal_var
            self._signal = Signal.from_variable(internal_var)

        # Build the UI
        self._build_ui()

    def _build_ui(self):
        """Construct the widget layout."""
        # Create button container
        self._button_container = Frame(self)

        # Create label if text provided
        if self._labeltext:
            self._label = Label(self, text=self._labeltext)

        # Position based on labelanchor
        self._update_layout()

    def _update_layout(self):
        """Update grid layout based on labelanchor."""
        # Clear existing layout
        for widget in self.winfo_children():
            widget.grid_forget()

        # Determine anchor direction from labelanchor
        # n/s = top/bottom, e/w = right/left
        anchor = self._labelanchor.lower()

        # Normalize compound anchors to primary direction
        # Priority: n > s > w > e (vertical placement preferred over horizontal)
        if 'n' in anchor:
            primary = 'n'
        elif 's' in anchor:
            primary = 's'
        elif 'w' in anchor:
            primary = 'w'
        elif 'e' in anchor:
            primary = 'e'
        else:
            # Default to north
            primary = 'n'

        # Layout based on primary anchor
        if primary == 'n':
            # Label on top
            if self._label:
                self._label.grid(row=0, column=0, sticky='w', pady=(0, 4))
            self._button_container.grid(row=1, column=0, sticky='ew')
            self.grid_columnconfigure(0, weight=1)
        elif primary == 's':
            # Label on bottom
            self._button_container.grid(row=0, column=0, sticky='ew')
            if self._label:
                self._label.grid(row=1, column=0, sticky='w', pady=(4, 0))
            self.grid_columnconfigure(0, weight=1)
        elif primary == 'w':
            # Label on left
            if self._label:
                self._label.grid(row=0, column=0, sticky='w', padx=(0, 8))
            self._button_container.grid(row=0, column=1, sticky='ew')
            self.grid_columnconfigure(1, weight=1)
        else:  # 'e'
            # Label on right
            self._button_container.grid(row=0, column=0, sticky='ew')
            if self._label:
                self._label.grid(row=0, column=1, sticky='w', padx=(8, 0))
            self.grid_columnconfigure(0, weight=1)

    @property
    def variable(self) -> 'tk.Variable':
        """Get the underlying tk.Variable."""
        return self._variable

    @variable.setter
    def variable(self, value: 'tk.Variable') -> None:
        """Set the variable."""
        from ttkbootstrap.core.signals import Signal
        self._variable = value
        self._signal = Signal.from_variable(value)
        # Update all buttons to use new variable
        for button in self._buttons.values():
            button.configure(variable=value)

    @property
    def signal(self) -> 'Signal[Any]':
        """Get the signal."""
        return self._signal

    @signal.setter
    def signal(self, value: 'Signal[Any]') -> None:
        """Set the signal."""
        self._signal = value
        self._variable = value.var
        # Update all buttons to use new variable
        for button in self._buttons.values():
            button.configure(variable=value.var)

    def add(self, text: str = None, value: Any = None, key: str | None = None, **kwargs: Any) -> RadioButton:
        """Add a radio button to the group.

        Args:
            text: Text to display on the button.
            value: Value this button represents (required).
            key: Unique identifier. Defaults to value.
            **kwargs: Additional arguments passed to RadioButton.

        Returns:
            The created RadioButton widget.

        Raises:
            ValueError: If value is None or if a button with the same key already exists.
        """
        if value is None:
            raise ValueError("The 'value' argument is required.")

        key = key or value
        if key in self._buttons:
            raise ValueError(f"A button with the key '{key}' already exists.")

        btn_kwargs = kwargs.copy()
        # Use color for button styling
        if 'color' not in btn_kwargs and 'bootstyle' not in btn_kwargs:
            btn_kwargs['color'] = self._color
        # Apply current state if not explicitly provided
        if 'state' not in btn_kwargs:
            btn_kwargs['state'] = self._state

        button = RadioButton(
            self._button_container,
            text=text,
            value=value,
            variable=self.variable,
            **btn_kwargs
        )

        if self._orientation == 'horizontal':
            button.pack(side='left', padx=2)
        else:  # vertical
            button.pack(side='top', anchor='w', pady=2)

        self._buttons[key] = button
        return button

    def get(self) -> str:
        """Return the currently selected value."""
        return self.variable.get()

    def set(self, value: str) -> None:
        """Set the selected value.

        Args:
            value: The value to select (must match a button's value).

        Raises:
            TypeError: If value is not a string.
            ValueError: If value doesn't exist in the group.
        """
        if not isinstance(value, str):
            raise TypeError(f"RadioGroup requires a string value, got {type(value).__name__}")

        # Allow empty string (deselection)
        if value and value not in self._buttons:
            valid_values = list(self._buttons.keys())
            raise ValueError(
                f"Value '{value}' not found in group. "
                f"Valid values: {valid_values}"
            )

        self.variable.set(value)

    @property
    def value(self) -> str:
        """Get or set the selected value."""
        return self.get()

    @value.setter
    def value(self, value: str) -> None:
        self.set(value)

    def remove(self, key: str):
        """Remove a button by its key.

        Args:
            key: The key of the button to remove.

        Raises:
            KeyError: If no button with the given key exists.
        """
        if key not in self._buttons:
            raise KeyError(f"No button with key '{key}'")
        button = self._buttons.pop(key)
        button.destroy()

    def buttons(self) -> tuple[RadioButton, ...]:
        """Get all button widgets in the group.

        Returns:
            A tuple of all RadioButton instances in the group.
        """
        return tuple(self._buttons.values())

    def get_button(self, key: str) -> RadioButton:
        """Get a button by its key.

        Args:
            key: The key of the button to retrieve.

        Returns:
            The RadioButton instance.

        Raises:
            KeyError: If no button with the given key exists.
        """
        if key not in self._buttons:
            raise KeyError(f"No button with key '{key}'")
        return self._buttons[key]

    def configure_button(self, key: str, **kwargs: Any):
        """Configure a specific button by its key.

        Args:
            key: The key of the button to configure.
            **kwargs: Configuration options to apply to the button.
        """
        button = self.get_button(key)
        button.configure(**kwargs)

    def on_changed(self, callback: Callable) -> Any:
        """Subscribe to value changes. Callback receives ``new_value: str`` directly."""
        return self._signal.subscribe(callback)

    def off_changed(self, subscription_id: Any) -> None:
        """Unsubscribe from value changes."""
        self._signal.unsubscribe(subscription_id)

    @configure_delegate('color')
    def _delegate_color(self, value=None):
        """Get or set the color. Updates all buttons when changed."""
        if value is None:
            return self._color

        self._color = value
        # Update all buttons with new color
        for button in self._buttons.values():
            button.configure(color=value)

    @configure_delegate('orient')
    def _delegate_orient(self, value=None):
        """Get or set orientation ('horizontal' or 'vertical'). Repacks buttons when changed."""
        if value is None:
            return self._orientation

        if value not in ('horizontal', 'vertical'):
            raise ValueError("orient must be 'horizontal' or 'vertical'")

        self._orientation = value

        # Repack all buttons in new orientation
        for button in self._buttons.values():
            button.pack_forget()
            if self._orientation == 'horizontal':
                button.pack(side='left', padx=2)
            else:
                button.pack(side='top', anchor='w', pady=2)

    @configure_delegate('labelanchor')
    def _delegate_labelanchor(self, value=None):
        """Get or set label anchor position. Updates layout when changed."""
        if value is None:
            return self._labelanchor

        valid_anchors = ('n', 's', 'e', 'w', 'ne', 'nw', 'se', 'sw')
        if value not in valid_anchors:
            raise ValueError(f"labelanchor must be one of {valid_anchors}")

        self._labelanchor = value
        self._update_layout()

    @configure_delegate('text')
    def _delegate_text(self, value=None):
        """Get or set label text. Creates or removes label as needed."""
        if value is None:
            return self._labeltext if self._labeltext else ''

        self._labeltext = value
        if value and not self._label:
            # Create label if it doesn't exist
            self._label = Label(self, text=value)
            self._update_layout()
        elif self._label:
            if value:
                self._label.configure(text=value)
            else:
                # Remove label if text is empty
                self._label.destroy()
                self._label = None
                self._update_layout()

    @configure_delegate('value')
    def _delegate_value(self, value=None):
        """Get or set the selected value."""
        if value is None:
            return self.get()
        self.set(value)

    @configure_delegate('state')
    def _delegate_state(self, value=None):
        """Get or set state for all buttons ('normal' or 'disabled')."""
        if value is None:
            return self._state

        if value not in ('normal', 'disabled'):
            raise ValueError("state must be 'normal' or 'disabled'")

        self._state = value
        # Update all buttons with new state
        for button in self._buttons.values():
            button.configure(state=value)

    def keys(self) -> tuple[str, ...]:
        """Get all button keys.

        Returns:
            A tuple of all button keys in the group.
        """
        return tuple(self._buttons.keys())

    def values(self) -> tuple[str, ...]:
        """Get all possible values.

        Returns:
            A tuple of all values that can be selected.
        """
        return tuple(self._buttons.keys())

    def __len__(self) -> int:
        """Return the number of buttons in the group."""
        return len(self._buttons)

    def __contains__(self, key: str) -> bool:
        """Check if a button with the given key exists in the group."""
        return key in self._buttons
