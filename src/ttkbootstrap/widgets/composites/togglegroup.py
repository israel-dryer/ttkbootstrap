from __future__ import annotations

from tkinter import StringVar
from typing import Any, Callable, Literal, TYPE_CHECKING

from typing_extensions import TypedDict, Unpack

from ttkbootstrap import RadioButton, CheckButton
from ttkbootstrap.core.variables import SetVar
from ttkbootstrap.widgets.mixins.configure_mixin import configure_delegate
from ttkbootstrap.widgets.primitives import Frame

if TYPE_CHECKING:
    from ttkbootstrap.core.signals import Signal
    import tkinter as tk


class ToggleGroupKwargs(TypedDict, total=False):
    mode: Literal['single', 'multi']
    variable: Any
    signal: Signal[Any]
    value: str | set[str]
    orient: Literal['horizontal', 'vertical']
    bootstyle: str
    show_border: bool
    surface_color: str
    style_options: dict[str, Any]
    # Frame options
    padding: Any
    width: int
    height: int


class ToggleGroup(Frame):
    """A group of toggle buttons with single or multi-selection support.

    The ToggleGroup widget provides a convenient way to create groups of toggle
    buttons with automatic position tracking and styling. It supports both single
    selection (radio button behavior) and multi-selection (checkbox behavior).
    """

    def __init__(self, master: Any = None, **kwargs: Unpack[ToggleGroupKwargs]):
        """Initialize the ToggleGroup.

        Args:
            master: Parent widget. If None, uses the default root window.

        Other Parameters:
            mode (str): Selection mode - 'single' for radio button behavior (default),
                or 'multi' for checkbox behavior allowing multiple selections.
            orient (str): Layout orientation - 'horizontal' (default) or 'vertical'.
            bootstyle (str): The color/variant style (e.g., 'primary', 'danger-outline').
                Defaults to 'primary'.
            variable (Variable): Optional tk.Variable for controlling the value. For single mode,
                use StringVar; for multi mode, use SetVar.
            signal (Signal): Optional Signal instance for reactive programming.
            value (str | set): Initial value - string for single mode, set for multi mode.
            show_border (bool): If True, draws a border around the group.
            surface_color (str): Optional surface token; otherwise inherited.
            style_options (dict): Additional style options passed to child buttons.
            padding (int | tuple): Frame padding. Defaults to 1.
            width (int): Requested width in pixels.
            height (int): Requested height in pixels.
        """
        # Extract ToggleGroup-specific options before super().__init__
        self._mode = kwargs.pop('mode', 'single')
        self._orientation = kwargs.pop('orient', 'horizontal')
        self._bootstyle = kwargs.pop('bootstyle', 'primary')

        # Handle signal/variable/value similar to CheckButton pattern
        initial_value = kwargs.pop('value', None)

        style_options = kwargs.pop('style_options', {})

        # Initialize internal state
        self._buttons: dict[str, RadioButton | CheckButton] = {}

        # Extract signal/variable before Frame init
        signal_value = kwargs.pop('signal', None)
        variable_value = kwargs.pop('variable', None)

        # Call super().__init__() - just Frame now
        super().__init__(master, style_options=style_options, padding=1, **kwargs)

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
            if self._mode == 'single':
                internal_var = StringVar(value=initial_value or '')
            else:
                internal_var = SetVar(value=initial_value or set())
            self._variable = internal_var
            self._signal = Signal.from_variable(internal_var)

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

    @property
    def signal(self) -> 'Signal[Any]':
        """Get the signal."""
        return self._signal

    @signal.setter
    def signal(self, value: 'Signal[Any]') -> None:
        """Set the signal."""
        self._signal = value
        self._variable = value.var

    def add(self, text: str = None, value: Any = None, key: str | None = None, **kwargs: Any) -> RadioButton | CheckButton:
        """Add a toggle button to the group.

        Args:
            text: Text to display on the button.
            value: Value this button represents (required).
            key: Unique identifier. Defaults to value.
            **kwargs: Additional arguments passed to RadioButton or CheckButton.

        Returns:
            The created button widget.
        """
        if value is None:
            raise ValueError("The 'value' argument is required.")

        key = key or value
        if key in self._buttons:
            raise ValueError(f"A button with the key '{key}' already exists.")

        btn_kwargs = kwargs.copy()
        # Set the buttongroup variant - position will be updated by _update_button_positions
        # If user provides custom bootstyle, append -buttongroup suffix
        custom_bootstyle = btn_kwargs.pop('bootstyle', self._bootstyle)
        btn_kwargs['bootstyle'] = f'{custom_bootstyle}-buttongroup'
        # Merge orient and initial position into style_options
        existing_style_opts = btn_kwargs.get('style_options', {}).copy()
        existing_style_opts['orient'] = self._orientation
        existing_style_opts.setdefault('position', 'before')  # Default position, will be corrected later
        btn_kwargs['style_options'] = existing_style_opts

        if self._mode == 'single':
            button = RadioButton(self, text=text, value=value, variable=self.variable, **btn_kwargs)
        else:  # multi
            button = CheckButton(self, text=text, **btn_kwargs)

            # Set initial state based on current SetVar value
            current_set = self.variable.get()
            if not isinstance(current_set, set):
                current_set = set()
            button.variable.set(value in current_set)

            # Bind command to update SetVar
            # Pop command to avoid double-calling
            original_command = btn_kwargs.pop('command', None)

            def toggle_command():
                self._on_multi_toggle(value)
                if original_command:
                    original_command()

            button.configure(command=toggle_command)

        if self._orientation == 'horizontal':
            button.pack(side='left')
        else:  # vertical
            button.pack(side='top', fill='x')

        self._buttons[key] = button
        self._update_button_positions()
        return button

    def _update_button_positions(self):
        """Update button bootstyles based on their position in the group.

        Note: Relies on dictionary insertion order (Python 3.7+) to maintain
        button order based on when they were added.
        """
        # List conversion maintains insertion order (Python 3.7+)
        button_list = list(self._buttons.values())
        num_buttons = len(button_list)

        if num_buttons == 0:
            return

        base_style = self._bootstyle

        for idx, button in enumerate(button_list):
            if num_buttons == 1:
                # Single button - use 'before' style for consistent appearance
                position = 'before'
            elif idx == 0:
                # First button
                position = 'before'
            elif idx == num_buttons - 1:
                # Last button
                position = 'after'
            else:
                # Middle button
                position = 'center'

            # Only update if position has changed (performance optimization)
            current_position = button.configure_style_options('position')
            if current_position != position:
                button.configure_style_options(position=position)
                new_bootstyle = f'{base_style}-buttongroup'
                button.configure(bootstyle=new_bootstyle)

    def _on_multi_toggle(self, value: str):
        """Callback to update the SetVar when a CheckToggle is clicked."""
        current_set = self.get()
        if value in current_set:
            current_set.remove(value)
        else:
            current_set.add(value)
        self.set(current_set)

    def get(self) -> str | set[str]:
        """Get the current value (string for single mode, set for multi mode)."""
        return self.variable.get()

    def set(self, value: str | set[str]):
        """Set the value (string for single mode, set for multi mode)."""
        # Validate value type matches mode
        if self._mode == 'single':
            if not isinstance(value, str):
                raise TypeError(f"Single mode requires a string value, got {type(value).__name__}")
        else:  # multi mode
            if not isinstance(value, set):
                raise TypeError(f"Multi mode requires a set value, got {type(value).__name__}")

        self.variable.set(value)

        # For multi mode, update CheckToggle states to match new value
        if self._mode == 'multi':
            for key, button in self._buttons.items():
                button.variable.set(key in value)

    def remove(self, key: str):
        """Remove a button by its key."""
        if key in self._buttons:
            button = self._buttons.pop(key)
            button.destroy()
            self._update_button_positions()

    def clear(self):
        """Remove all buttons from the group."""
        for key in list(self._buttons.keys()):
            self.remove(key)

    def buttons(self) -> tuple[RadioButton | CheckButton, ...]:
        """Get all button widgets in the group."""
        return tuple(self._buttons.values())

    def get_button(self, key: str) -> RadioButton | CheckButton:
        """Get a button by its key."""
        if key not in self._buttons:
            raise KeyError(f"No button with key '{key}'")
        return self._buttons[key]

    def configure_button(self, key: str, **kwargs: Any):
        """Configure a specific button by its key."""
        button = self.get_button(key)
        button.configure(**kwargs)

    def on_changed(self, callback: Callable) -> Any:
        """Subscribe to value changes. Callback receives ``new_value: str | set[str]`` directly (str in 'single' mode, set in 'multi' mode)."""
        return self._signal.subscribe(callback)

    def off_changed(self, subscription_id: Any) -> None:
        """Unsubscribe from value changes."""
        self._signal.unsubscribe(subscription_id)

    @configure_delegate('bootstyle')
    def _delegate_bootstyle(self, value=None):
        """Get or set the bootstyle. Updates all buttons when changed."""
        if value is None:
            return self._bootstyle

        self._bootstyle = value
        # Update all buttons with new bootstyle
        self._update_button_positions()

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
            button.configure_style_options(orient=value)
            if self._orientation == 'horizontal':
                button.pack(side='left')
            else:
                button.pack(side='top', fill='x')

        # Update button styles with new orientation
        self._update_button_positions()
