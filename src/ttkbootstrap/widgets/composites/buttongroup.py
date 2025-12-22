from __future__ import annotations

from typing import Any, Callable, Literal, TYPE_CHECKING

from typing_extensions import TypedDict, Unpack

from ttkbootstrap import Button
from ttkbootstrap.widgets.mixins.configure_mixin import configure_delegate
from ttkbootstrap.widgets.primitives import Frame
from ttkbootstrap.widgets.primitives.checkbutton import CheckButton
from ttkbootstrap.widgets.primitives.checktoggle import CheckToggle
from ttkbootstrap.widgets.primitives.radiobutton import RadioButton
from ttkbootstrap.widgets.primitives.radiotoggle import RadioToggle

if TYPE_CHECKING:
    import tkinter as tk


class ButtonGroupKwargs(TypedDict, total=False):
    orient: Literal['horizontal', 'vertical']
    bootstyle: str
    state: Literal['normal', 'disabled']
    show_border: bool
    surface_color: str
    style_options: dict[str, Any]
    # Frame options
    padding: Any
    width: int
    height: int


class ButtonGroup(Frame):
    """A group of buttons with automatic positioning and styling.

    ButtonGroup provides visual grouping of buttons (or other widgets) without
    state tracking. Perfect for toolbars, action button groups, or any scenario
    where you want buttons visually connected but don't need to track which is
    selected.
    """

    def __init__(self, master: Any = None, **kwargs: Unpack[ButtonGroupKwargs]):
        """Initialize the ButtonGroup.

        Args:
            master: Parent widget. If None, uses the default root window.

        Other Parameters:
            orient (str): Layout orientation - 'horizontal' (default) or 'vertical'.
            bootstyle (str): The color/variant style (e.g., 'primary', 'success', 'danger').
                Defaults to 'primary'.
            state (str): Initial state for all buttons - 'normal' (default) or 'disabled'.
            show_border (bool): If True, draws a border around the group.
            surface_color (str): Optional surface token; otherwise inherited.
            style_options (dict): Additional style options passed to child widgets.
            padding (int | tuple): Frame padding. Defaults to 1.
            width (int): Requested width in pixels.
            height (int): Requested height in pixels.
        """
        # Extract ButtonGroup-specific options
        self._orientation = kwargs.pop('orient', 'horizontal')
        self._bootstyle = kwargs.pop('bootstyle', 'primary')
        self._state = kwargs.pop('state', 'normal')

        style_options = kwargs.pop('style_options', {})

        # Initialize internal state
        self._widgets: dict[str, tk.Widget] = {}
        self._counter = 0  # For auto-generating keys

        # Handle padding default
        if 'padding' not in kwargs:
            kwargs['padding'] = 1

        super().__init__(master, style_options=style_options, **kwargs)

    def add(
        self,
        text: str = None,
        *,
        key: str = None,
        widget_type: type = None,
        command: Callable[[], Any] = None,
        **kwargs
    ) -> 'tk.Widget':
        """Add a widget to the group.

        Args:
            text: Text to display on the widget.
            key: Unique identifier. Auto-generated if not provided.
            widget_type: Widget class to instantiate (defaults to Button).
            command: Callback for button press.
            **kwargs: Additional arguments passed to the widget constructor.

        Returns:
            The created widget instance.

        Raises:
            ValueError: If a widget with the same key already exists.
        """
        # Auto-generate key if not provided
        if key is None:
            key = f"widget_{self._counter}"
            self._counter += 1

        if key in self._widgets:
            raise ValueError(f"A widget with the key '{key}' already exists.")

        # Default to Button if no widget type specified
        if widget_type is None:
            widget_type = Button
        elif not callable(widget_type):
            raise TypeError(f"widget_type must be a class or callable, got {type(widget_type).__name__}")

        widget_kwargs = kwargs.copy()

        # Apply buttongroup bootstyle for visual grouping
        if 'bootstyle' not in widget_kwargs:
            widget_kwargs['bootstyle'] = f'{self._bootstyle}-buttongroup'
        else:
            # User provided custom bootstyle - append buttongroup
            custom_style = widget_kwargs.pop('bootstyle')
            widget_kwargs['bootstyle'] = f"{custom_style}-buttongroup"

        # Apply positioning via style_options
        existing_style_opts = widget_kwargs.get('style_options', {}).copy()
        existing_style_opts['orient'] = self._orientation
        existing_style_opts.setdefault('position', 'before')

        # Set active_state for non-radio/check button types
        _radio_check_types = (CheckButton, CheckToggle, RadioButton, RadioToggle)
        if isinstance(widget_type, type) and not issubclass(widget_type, _radio_check_types):
            existing_style_opts.setdefault('active_state', True)

        widget_kwargs['style_options'] = existing_style_opts

        # Apply state if not explicitly provided
        if 'state' not in widget_kwargs:
            widget_kwargs['state'] = self._state

        # Build constructor arguments
        ctor_args = {'text': text} if text is not None else {}
        if command is not None:
            ctor_args['command'] = command
        ctor_args.update(widget_kwargs)

        # Create the widget
        widget = widget_type(self, **ctor_args)

        # Pack based on orientation
        if self._orientation == 'horizontal':
            widget.pack(side='left')
        else:  # vertical
            widget.pack(side='top', fill='x')

        self._widgets[key] = widget
        self._update_widget_positions()
        return widget

    def _update_widget_positions(self):
        """Update widget styles based on their position in the group.

        Note: Relies on dictionary insertion order (Python 3.7+) to maintain
        widget order based on when they were added.
        """
        widget_list = list(self._widgets.values())
        num_widgets = len(widget_list)

        if num_widgets == 0:
            return

        base_style = self._bootstyle

        for idx, widget in enumerate(widget_list):
            if num_widgets == 1:
                position = 'before'
            elif idx == 0:
                position = 'before'
            elif idx == num_widgets - 1:
                position = 'after'
            else:
                position = 'center'

            # Update position if widget supports configure_style_options
            if hasattr(widget, 'configure_style_options'):
                current_position = widget.configure_style_options('position')
                if current_position != position:
                    widget.configure_style_options(position=position)
                    new_bootstyle = f'{base_style}-buttongroup'
                    widget.configure(bootstyle=new_bootstyle)

    def remove(self, key: str):
        """Remove a widget by its key.

        Args:
            key: The key of the widget to remove.

        Raises:
            KeyError: If no widget with the given key exists.
        """
        if key not in self._widgets:
            raise KeyError(f"No widget with key '{key}'")
        widget = self._widgets.pop(key)
        widget.destroy()
        self._update_widget_positions()

    def clear(self):
        """Remove all widgets from the group."""
        for key in list(self._widgets.keys()):
            self.remove(key)

    def get_widget(self, key: str) -> 'tk.Widget':
        """Get a widget by its key.

        Args:
            key: The key of the widget to retrieve.

        Returns:
            The widget instance.

        Raises:
            KeyError: If no widget with the given key exists.
        """
        if key not in self._widgets:
            raise KeyError(f"No widget with key '{key}'")
        return self._widgets[key]

    def configure_widget(self, key: str, **kwargs):
        """Configure a specific widget by its key.

        Args:
            key: The key of the widget to configure.
            **kwargs: Configuration options to apply to the widget.

        Examples:
            group.configure_widget("save_btn", state='disabled')
        """
        widget = self.get_widget(key)
        widget.configure(**kwargs)

    def widgets(self) -> tuple['tk.Widget', ...]:
        """Get all widgets in the group.

        Returns:
            A tuple of all widget instances in the group.
        """
        return tuple(self._widgets.values())

    def keys(self) -> tuple[str, ...]:
        """Get all widget keys.

        Returns:
            A tuple of all widget keys in the group.
        """
        return tuple(self._widgets.keys())

    def __len__(self) -> int:
        """Return the number of widgets in the group.

        Examples:
            >>> count = len(button_group)
        """
        return len(self._widgets)

    def __contains__(self, key: str) -> bool:
        """Check if a widget with the given key exists in the group.

        Examples:
            >>> if 'save' in button_group:
            ...     print('Save button exists')
        """
        return key in self._widgets

    def __iter__(self):
        """Iterate over the widgets in the group.

        Examples:
            >>> for widget in button_group:
            ...     widget.configure(state='disabled')
        """
        return iter(self._widgets.values())

    @configure_delegate('bootstyle')
    def _delegate_bootstyle(self, value=None):
        """Get or set the bootstyle. Updates all widgets when changed."""
        if value is None:
            return self._bootstyle

        self._bootstyle = value

        # Reconfigure all widgets with the new bootstyle
        for widget in self._widgets.values():
            if hasattr(widget, 'configure'):
                new_bootstyle = f'{self._bootstyle}-buttongroup'
                widget.configure(bootstyle=new_bootstyle)

        self._update_widget_positions()

    @configure_delegate('orient')
    def _delegate_orient(self, value=None):
        """Get or set orientation ('horizontal' or 'vertical'). Repacks widgets when changed."""
        if value is None:
            return self._orientation

        if value not in ('horizontal', 'vertical'):
            raise ValueError("orient must be 'horizontal' or 'vertical'")

        self._orientation = value

        # Repack all widgets
        for widget in self._widgets.values():
            widget.pack_forget()
            if hasattr(widget, 'configure_style_options'):
                widget.configure_style_options(orient=value)
                # Reconfigure bootstyle to trigger style rebuild with new orientation
                current_bootstyle = f'{self._bootstyle}-buttongroup'
                widget.configure(bootstyle=current_bootstyle)

            if self._orientation == 'horizontal':
                widget.pack(side='left')
            else:
                widget.pack(side='top', fill='x')

        self._update_widget_positions()

    @configure_delegate('state')
    def _delegate_state(self, value=None):
        """Get or set state for all widgets ('normal' or 'disabled')."""
        if value is None:
            return self._state

        if value not in ('normal', 'disabled'):
            raise ValueError("state must be 'normal' or 'disabled'")

        self._state = value
        # Update all widgets with new state
        for widget in self._widgets.values():
            try:
                widget.configure(state=value)
            except (AttributeError, TypeError):
                # Widget doesn't support state configuration
                pass