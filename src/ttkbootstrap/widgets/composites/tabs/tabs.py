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
            self._tab_bar.add(self._add_button)
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
            self._tab_bar.add(self._add_button, fill='x')

    def _destroy_add_button(self):
        """Remove the add button widget."""
        if self._add_button is not None:
            self._tab_bar.remove(self._add_button)
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

    @property
    def managed_widgets(self) -> list[tk.Widget]:
        """Return list of managed tab widgets in order (excludes add button)."""
        widgets = self._tab_bar.managed_widgets
        if self._add_button is not None and self._add_button in widgets:
            return [w for w in widgets if w is not self._add_button]
        return widgets

    def add_tab(
        self,
        text: str = "",
        icon: str | dict = None,
        value: Any = None,
        closable: Union[bool, Literal['hover']] = None,
        close_command: Callable = None,
        command: Callable = None,
        **kwargs
    ) -> TabItem:
        """Add a new tab to the tab bar.

        This is a convenience method that creates a TabItem with the
        container's default settings and adds it to the tab bar.

        Args:
            text: Text to display on the tab.
            icon: Icon to display on the tab.
            value: Value associated with this tab for selection tracking.
            closable: Close button visibility (True, False, or 'hover').
                If None, uses the widget's `enable_closing` setting.
            close_command: Callback when close button is clicked.
            command: Callback when tab is selected.
            **kwargs: Additional arguments passed to TabItem.

        Returns:
            The created TabItem widget.
        """
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
            add_btn_index = self._tab_bar.index_of(self._add_button)
            self._tab_bar.insert(add_btn_index, tab, **pack_opts)
        else:
            self._tab_bar.add(tab, **pack_opts)

        # Auto-select first tab (check for 1 if no add button, 2 if add button exists)
        tab_count = len(self._tab_bar) - (1 if self._add_button else 0)
        if tab_count == 1 and value is not None:
            self._variable.set(value)

        return tab

    def add(self, widget: tk.Widget, **options: Any) -> tk.Widget:
        """Add a widget (typically TabItem) to the tab bar.

        Args:
            widget: The widget to add.
            **options: Pack options. Defaults to fill='x'.

        Returns:
            The widget.
        """
        # Default fill='x' for tabs
        if 'fill' not in options:
            options['fill'] = 'x'

        # Apply stretch behavior for horizontal orientation
        if self._tab_width == 'stretch' and self._orient == 'horizontal':
            if 'expand' not in options:
                options['expand'] = True

        # Insert before add button if it exists, otherwise append
        if self._add_button is not None:
            add_btn_index = self._tab_bar.index_of(self._add_button)
            return self._tab_bar.insert(add_btn_index, widget, **options)

        return self._tab_bar.add(widget, **options)

    def remove(self, widget: tk.Widget) -> None:
        """Remove a widget from the tab bar.

        Args:
            widget: The widget to remove.
        """
        self._tab_bar.remove(widget)

    @property
    def orient(self) -> str:
        """Get the orientation of the tab bar."""
        return self._orient

    @property
    def variant(self) -> str:
        """Get the visual variant of the tab bar."""
        return self._variant

    @property
    def variable(self) -> tk.Variable:
        """Get the underlying tk.Variable for tab selection."""
        return self._variable

    @property
    def signal(self) -> 'Signal[Any]':
        """Get the Signal for tab selection."""
        return self._signal

    @property
    def show_divider(self) -> bool:
        """Get whether the divider is shown."""
        return self._show_divider

    @show_divider.setter
    def show_divider(self, value: bool):
        """Set whether the divider is shown."""
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
