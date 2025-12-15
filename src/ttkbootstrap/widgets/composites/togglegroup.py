from __future__ import annotations
from tkinter import StringVar
from typing import Any, Literal, TYPE_CHECKING
from typing_extensions import TypedDict, Unpack

from ttkbootstrap.widgets.primitives import Frame
from ttkbootstrap.widgets.primitives.checktoggle import CheckToggle
from ttkbootstrap.widgets.primitives.radiotoggle import RadioToggle
from ttkbootstrap.core.variables import SetVar

if TYPE_CHECKING:
    from ttkbootstrap.core.signals import Signal
    import tkinter as tk

class ToggleGroupKwargs(TypedDict, total=False):
    mode: Literal['single', 'multi']
    variable: Any
    signal: Signal[Any]
    value: str | set[str]
    orientation: Literal['horizontal', 'vertical']
    bootstyle: str
    show_border: bool
    surface_color: str
    style_options: dict[str, Any]
    # Frame options
    padding: Any
    width: int
    height: int

class ToggleGroup(Frame):
    """A group of toggle buttons with single or multi-selection support."""

    def __init__(self, master: Any = None, **kwargs: Unpack[ToggleGroupKwargs]):
        """
        Initialize the ToggleGroup.

        Args:
            master (Any): The parent widget.
            **kwargs: Keyword arguments for configuration.
        """
        # Extract ToggleGroup-specific options before super().__init__
        self._mode = kwargs.pop('mode', 'single')
        self._orientation = kwargs.pop('orientation', 'horizontal')
        self._bootstyle = kwargs.pop('bootstyle', 'Toolbutton')
        show_border = kwargs.pop('show_border', False)

        # Handle signal/variable/value similar to CheckButton pattern
        signal_provided = 'signal' in kwargs
        variable_provided = 'variable' in kwargs
        initial_value = kwargs.pop('value', None)

        # Add border configuration to kwargs
        if show_border:
            kwargs['borderwidth'] = 1
            kwargs['relief'] = 'solid'

        # Initialize internal state
        self._buttons: dict[str, CheckToggle | RadioToggle] = {}

        # Extract signal/variable before Frame init
        signal_value = kwargs.pop('signal', None)
        variable_value = kwargs.pop('variable', None)

        # Call super().__init__() - just Frame now
        super().__init__(master, **kwargs)

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


    def add(self, text=None, value=None, key=None, **kwargs) -> CheckToggle | RadioToggle:
        """
        Creates and adds a new toggle button to the group.

        Args:
            text (str, optional): The text to display on the button.
            value (Any, optional): The value this button represents. Required.
            key (str, optional): A unique identifier for the button. Defaults to the value.
            **kwargs: Additional keyword arguments passed to the CheckToggle or RadioToggle.

        Returns:
            CheckToggle | RadioToggle: The created button widget.
        """
        if value is None:
            raise ValueError("The 'value' argument is required.")
        
        key = key or value
        if key in self._buttons:
            raise ValueError(f"A button with the key '{key}' already exists.")

        btn_kwargs = kwargs.copy()
        if self._bootstyle:
            btn_kwargs.setdefault('bootstyle', self._bootstyle)

        if self._mode == 'single':
            button = RadioToggle(self, text=text, value=value, variable=self.variable, **btn_kwargs)
        else: # multi
            button = CheckToggle(self, text=text, **btn_kwargs)

            # Set initial state based on current SetVar value
            current_set = self.variable.get()
            button.variable.set(value in current_set)

            # Bind command to update SetVar
            original_command = btn_kwargs.get('command')
            def toggle_command():
                self._on_multi_toggle(value)
                if original_command:
                    original_command()
            button.configure(command=toggle_command)

        if self._orientation == 'horizontal':
            button.pack(side='left', padx=1, pady=1)
        else:  # vertical
            button.pack(side='top', fill='x', padx=1, pady=1)

        self._buttons[key] = button
        return button

    def _on_multi_toggle(self, value: str):
        """Callback to update the SetVar when a CheckToggle is clicked."""
        current_set = self.get()
        if value in current_set:
            current_set.remove(value)
        else:
            current_set.add(value)
        self.set(current_set)

    def get(self) -> str | set[str]:
        """Returns the current value from the underlying variable."""
        return self.variable.get()

    def set(self, value: str | set[str]):
        """Sets the underlying variable to a new value."""
        self.variable.set(value)

        # For multi mode, update CheckToggle states to match new value
        if self._mode == 'multi' and isinstance(value, set):
            for key, button in self._buttons.items():
                button.variable.set(key in value)

    def remove(self, key: str):
        """Removes a button by its key and destroys the widget."""
        if key in self._buttons:
            button = self._buttons.pop(key)
            button.destroy()

    def clear(self):
        """Removes all buttons from the group."""
        for key in list(self._buttons.keys()):
            self.remove(key)

    def buttons(self) -> tuple[CheckToggle | RadioToggle, ...]:
        """Returns a tuple of all button widgets in the group."""
        return tuple(self._buttons.values())

    def get_button(self, key: str) -> CheckToggle | RadioToggle:
        """Returns the button widget corresponding to the given key.

        Args:
            key: The button key.

        Returns:
            The button widget.

        Raises:
            KeyError: If key doesn't exist.
        """
        if key not in self._buttons:
            raise KeyError(f"No button with key '{key}'")
        return self._buttons[key]

    def configure_button(self, key: str, **kwargs):
        """Configures a specific button in the group.

        Args:
            key (str): The key of the button to configure.
            **kwargs: Keyword arguments to pass to the button's configure method.

        Raises:
            KeyError: If key doesn't exist.
        """
        button = self.get_button(key)
        button.configure(**kwargs)
