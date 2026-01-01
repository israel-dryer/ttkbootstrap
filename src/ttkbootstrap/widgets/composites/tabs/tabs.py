"""Tabs widget - a tab bar container for TabItem widgets."""
from __future__ import annotations

__all__ = ['Tabs']

import tkinter as tk
from tkinter import Variable
from typing import Any, Callable, Literal, TYPE_CHECKING, Union

from ttkbootstrap.widgets.primitives.packframe import PackFrame
from ttkbootstrap.widgets.primitives.frame import Frame
from ttkbootstrap.widgets.primitives.separator import Separator
from ttkbootstrap.widgets.primitives.button import Button
from ttkbootstrap.widgets.composites.tabs.tabitem import TabItem
from ttkbootstrap.widgets.mixins.configure_mixin import configure_delegate
from ttkbootstrap.widgets.types import Master

if TYPE_CHECKING:
    from ttkbootstrap.core.signals import Signal


class Tabs(Frame):
    """A container widget for grouping TabItem widgets.

    Tabs provides a tab bar with optional divider. It manages the layout,
    orientation, and styling of child TabItems.

    !!! note "Events"
        - ``<<TabSelect>>``: Fired when a tab is selected (bubbled from TabItem).
        - ``<<TabClose>>``: Fired when a tab's close button is clicked (bubbled from TabItem).
        - ``<<TabAdd>>``: Fired when the add button is clicked (if enable_adding=True).

    Attributes:
        orient (str): The orientation of the tab bar ('horizontal' or 'vertical').
        variant (str): The visual style variant ('pill' or 'bar').
    """

    def __init__(
        self,
        master: Master = None,
        orient: Literal['horizontal', 'vertical'] = 'horizontal',
        variant: Literal['pill', 'bar'] = 'bar',
        show_divider: bool = None,
        compound: Literal['left', 'right', 'top', 'bottom', 'center', 'none'] = 'left',
        tab_width: Union[None, int, Literal['stretch']] = None,
        tab_padding: tuple = (12, 8),
        tab_anchor: str = None,
        enable_closing: Union[bool, Literal['hover']] = False,
        enable_adding: bool = False,
        variable: Variable = None,
        signal: 'Signal[Any]' = None,
        color: str = None,
        **kwargs
    ):
        """Create a Tabs widget.

        Args:
            master: Parent widget. If None, uses the default root window.
            orient: Orientation of the tab bar. 'horizontal' places tabs in a row,
                'vertical' places tabs in a column. Default is 'horizontal'.
            variant: Visual style variant ('pill' or 'bar').
                Default is 'bar'.
            show_divider: Whether to show a divider line. If None (default),
                automatically set to True for 'bar' variant, False for others.
            compound: How to position icon relative to text in tabs.
                Passed to all TabItems. Default is 'left'.
            tab_width: Width of tabs. None for auto-sizing, an integer for
                fixed character width, or 'stretch' to expand tabs to fill
                available space (horizontal only). Default is None.
            tab_padding: Padding for all tabs as (horizontal, vertical).
                Default is (12, 8).
            tab_anchor: Anchor for tab text/icon alignment. If None, defaults
                to 'w' for vertical orientation, 'center' for horizontal.
            enable_closing: Default close button visibility for all tabs.
                True=always visible, False=hidden, 'hover'=visible on hover.
                Can be overridden per-tab via `closable` in add_tab().
            enable_adding: If True, shows an "add" button. In horizontal
                orientation, shows a plus icon on the right. In vertical
                orientation, shows "New Tab" at the bottom. Fires `<<TabAdd>>`
                event when clicked.
            variable: Tk variable for tracking selected tab value.
            signal: Reactive Signal for tracking selected tab value.
            color: Color token for styling tabs.
            **kwargs: Additional arguments passed to Frame.
        """
        super().__init__(master=master, **kwargs)

        self._orient = orient
        self._variant = variant
        self._compound = compound
        self._tab_width = tab_width
        self._tab_padding = tab_padding
        self._enable_closing = enable_closing
        self._enable_adding = enable_adding
        self._color = color

        # Handle variable/signal setup
        if signal is not None:
            # Signal provided - extract its variable
            self._signal = signal
            self._variable = signal.var
        elif variable is not None:
            # Variable provided - wrap in Signal
            from ttkbootstrap.core.signals import Signal
            self._variable = variable
            self._signal = Signal.from_variable(variable)
        else:
            # Neither provided - create internal variable and signal
            from ttkbootstrap.core.signals import Signal
            self._variable = tk.StringVar()
            self._signal = Signal.from_variable(self._variable)

        # Default anchor based on orientation
        if tab_anchor is None:
            self._tab_anchor = 'w' if orient == 'vertical' else 'center'
        else:
            self._tab_anchor = tab_anchor

        # Determine show_divider default based on variant
        if show_divider is None:
            self._show_divider = variant == 'bar'
        else:
            self._show_divider = show_divider

        # Set direction based on orient
        direction = 'horizontal' if orient == 'horizontal' else 'vertical'

        # Gap between tabs
        gap = 0

        # Internal divider widget
        self._divider: Separator | None = None

        # Internal add button
        self._add_button: Button | None = None

        # Create internal PackFrame for tabs
        self._tab_bar = PackFrame(
            self,
            direction=direction,
            gap=gap,
        )

        # Layout tab bar and divider
        if orient == 'horizontal':
            self._tab_bar.pack(side='top', fill='x')
            if self._show_divider:
                self._divider = Separator(self, orient='horizontal')
                self._divider.pack(side='top', fill='x')
        else:
            self._tab_bar.pack(side='left', fill='y')
            if self._show_divider:
                self._divider = Separator(self, orient='vertical')
                self._divider.pack(side='left', fill='y')

        # Create add button if enabled (must be after tab_bar is created)
        if enable_adding:
            self._create_add_button()

        # Tab tracking by key
        self._tabs: dict[str, TabItem] = {}
        self._tab_order: list[str] = []
        self._counter = 0  # For auto-generating keys

    def _create_divider(self):
        """Create the divider separator widget."""
        if self._divider is not None:
            return
        if self._orient == 'horizontal':
            self._divider = Separator(self, orient='horizontal')
            self._divider.pack(side='top', fill='x')
        else:
            self._divider = Separator(self, orient='vertical')
            self._divider.pack(side='left', fill='y')

    def _destroy_divider(self):
        """Remove the divider widget."""
        if self._divider is not None:
            self._divider.pack_forget()
            self._divider.destroy()
            self._divider = None

    def _create_add_button(self):
        """Create the add button widget."""
        if self._add_button is not None:
            return

        if self._orient == 'horizontal':
            # Plus icon only
            self._add_button = Button(
                self._tab_bar,
                icon='plus',
                icon_only=True,
                variant='ghost',
                command=self._on_add_click,
            )
            self._add_button.pack()
        else:
            # "New Tab" with plus icon
            self._add_button = Button(
                self._tab_bar,
                text='New',
                icon='plus',
                variant='ghost',
                padding=2,
                command=self._on_add_click,
                anchor='w',
            )
            self._add_button.pack(fill='x')

    def _destroy_add_button(self):
        """Remove the add button widget."""
        if self._add_button is not None:
            self._add_button.pack_forget()
            self._add_button.destroy()
            self._add_button = None

    def _on_add_click(self):
        """Handle add button click."""
        self.event_generate('<<TabAdd>>')

    def on_tab_added(self, callback: Callable) -> str:
        """Bind to ``<<TabAdd>>`` event.

        Args:
            callback: Function to call when add button is clicked.

        Returns:
            Binding identifier for use with off_tab_added().
        """
        return self.bind('<<TabAdd>>', callback, add='+')

    def off_tab_added(self, bind_id: str | None = None) -> None:
        """Unbind from <<TabAdd>> event."""
        self.unbind('<<TabAdd>>', bind_id)

    def add(
        self,
        text: str = "",
        *,
        key: str = None,
        icon: str | dict = None,
        value: Any = None,
        closable: Union[bool, Literal['hover']] = None,
        close_command: Callable = None,
        command: Callable = None,
        **kwargs
    ) -> TabItem:
        """Add a new tab to the tab bar.

        Args:
            text: Text to display on the tab.
            key: Unique identifier for the tab. Auto-generated if not provided.
            icon: Icon to display on the tab.
            value: Value associated with this tab for selection tracking.
                If None, defaults to the key.
            closable: Close button visibility (True, False, or 'hover').
                If None, uses the widget's `enable_closing` setting.
            close_command: Callback when close button is clicked.
            command: Callback when tab is selected.
            **kwargs: Additional arguments passed to TabItem.

        Returns:
            The created TabItem widget.

        Raises:
            ValueError: If a tab with the same key already exists.
        """
        # Auto-generate key if not provided
        if key is None:
            key = f"tab_{self._counter}"
            self._counter += 1

        if key in self._tabs:
            raise ValueError(f"A tab with the key '{key}' already exists.")

        # Default value to key if not specified
        if value is None:
            value = key

        # Use widget-level default if not specified
        if closable is None:
            closable = self._enable_closing

        # Apply container defaults
        tab_kwargs = {
            'compound': self._compound,
            'variant': self._variant,
            'orient': self._orient,
            'padding': self._tab_padding,
            'anchor': self._tab_anchor,
        }

        # Apply tab_width if specified (not 'stretch')
        if self._tab_width is not None and self._tab_width != 'stretch':
            tab_kwargs['width'] = self._tab_width

        # Apply color if specified
        if self._color is not None:
            tab_kwargs['color'] = self._color

        # Pass signal to TabItem for selection sync
        tab_kwargs['signal'] = self._signal

        # User kwargs override defaults
        tab_kwargs.update(kwargs)

        tab = TabItem(
            self._tab_bar,
            text=text,
            icon=icon,
            value=value,
            closable=closable,
            close_command=close_command,
            command=command,
            **tab_kwargs
        )

        # Determine pack options
        pack_opts = {'fill': 'x'}
        if self._tab_width == 'stretch' and self._orient == 'horizontal':
            pack_opts['expand'] = True

        # Insert before add button if it exists, otherwise append
        if self._add_button is not None:
            tab.pack(before=self._add_button, **pack_opts)
        else:
            tab.pack(**pack_opts)

        # Track tab by key
        self._tabs[key] = tab
        self._tab_order.append(key)

        # Auto-select first tab
        if len(self._tabs) == 1:
            self._variable.set(value)

        return tab

    def remove(self, key: str) -> None:
        """Remove a tab by its key.

        Args:
            key: The key of the tab to remove.

        Raises:
            KeyError: If no tab with the given key exists.
        """
        if key not in self._tabs:
            raise KeyError(f"No tab with key '{key}'")

        tab = self._tabs.pop(key)
        self._tab_order.remove(key)
        tab.pack_forget()
        tab.destroy()

    def item(self, key: str) -> TabItem:
        """Get a tab by its key.

        Args:
            key: The key of the tab to retrieve.

        Returns:
            The TabItem instance.

        Raises:
            KeyError: If no tab with the given key exists.
        """
        if key not in self._tabs:
            raise KeyError(f"No tab with key '{key}'")
        return self._tabs[key]

    def items(self) -> tuple[TabItem, ...]:
        """Get all tab widgets in order.

        Returns:
            A tuple of all TabItem instances in the order they were added.
        """
        return tuple(self._tabs[key] for key in self._tab_order)

    def keys(self) -> tuple[str, ...]:
        """Get all tab keys in order.

        Returns:
            A tuple of all tab keys in the order they were added.
        """
        return tuple(self._tab_order)

    def configure_item(self, key: str, option: str = None, **kwargs: Any):
        """Configure a specific tab by its key.

        Args:
            key: The key of the tab to configure.
            option: If provided, return the value of this option.
            **kwargs: Configuration options to apply to the tab.

        Returns:
            If option is provided, returns the value of that option.
        """
        tab = self.item(key)
        if option is not None:
            return tab.cget(option)
        tab.configure(**kwargs)

    @configure_delegate('orient')
    def _delegate_orient(self, value=None):
        """Get orientation (read-only after creation)."""
        if value is None:
            return self._orient
        raise ValueError("orient cannot be changed after creation")

    @configure_delegate('variant')
    def _delegate_variant(self, value=None):
        """Get variant (read-only after creation)."""
        if value is None:
            return self._variant
        raise ValueError("variant cannot be changed after creation")

    @property
    def variable(self) -> tk.Variable:
        """Get the underlying tk.Variable for tab selection."""
        return self._variable

    @property
    def signal(self) -> 'Signal[Any]':
        """Get the Signal for tab selection."""
        return self._signal

    @configure_delegate('show_divider')
    def _delegate_show_divider(self, value=None):
        """Get or set whether the divider is shown."""
        if value is None:
            return self._show_divider
        if value != self._show_divider:
            self._show_divider = value
            if value:
                self._create_divider()
            else:
                self._destroy_divider()

    def get(self) -> str:
        """Return the currently selected tab value."""
        return self._variable.get()

    def set(self, value: str) -> None:
        """Set the selected tab value."""
        self._variable.set(value)

    @property
    def value(self) -> str:
        """Get or set the selected tab value."""
        return self.get()

    @value.setter
    def value(self, value: str) -> None:
        self.set(value)

    @configure_delegate('value')
    def _delegate_value(self, value=None):
        """Get or set the value via configure."""
        if value is None:
            return self.get()
        self.set(value)

    def on_tab_changed(self, callback: Callable) -> Any:
        """Subscribe to tab selection changes.

        Args:
            callback: Function called with the new selected value.

        Returns:
            Subscription ID for use with off_tab_changed().
        """
        return self._signal.subscribe(callback)

    def off_tab_changed(self, bind_id: Any) -> None:
        """Unsubscribe from tab selection changes."""
        self._signal.unsubscribe(bind_id)
