"""SideNav widget - a simple vertical navigation container."""

from __future__ import annotations

from tkinter import Variable
from typing import Any, TYPE_CHECKING

from ttkbootstrap.widgets.primitives.frame import Frame
from ttkbootstrap.widgets.primitives.radiotoggle import RadioToggle
from ttkbootstrap.widgets.primitives.label import Label
from ttkbootstrap.widgets.primitives.separator import Separator
from ttkbootstrap.widgets.types import Master
from ttkbootstrap.core.capabilities.signals import create_signal, normalize_signal

if TYPE_CHECKING:
    from ttkbootstrap.core.signals import Signal


class SideNav(Frame):
    """A simple vertical navigation container with selectable items.

    SideNav provides a straightforward navigation component using RadioToggle
    buttons. Items can display icons, text, or both. Use multiple SideNavs
    side-by-side for multi-level navigation (e.g., icon-only + list view).

    Virtual events:
        ``<<SelectionChanged>>``: Fired when selected item changes.
            event.data = {'key': str}

    Example:
        ```python
        # Simple navigation
        nav = SideNav(root)
        nav.add_item('home', text='Home', icon='house')
        nav.add_item('docs', text='Documents', icon='file-earmark-text')
        nav.add_separator()
        nav.add_item('settings', text='Settings', icon='gear')

        # Icon-only navigation
        icon_nav = SideNav(root, icon_only=True)
        icon_nav.add_item('home', icon='house')
        icon_nav.add_item('search', icon='search')
        ```
    """

    def __init__(
        self,
        master: Master = None,
        icon_only: bool = False,
        signal: 'Signal[str]' = None,
        variable: Variable = None,
        item_color: str = 'ghost',
        **kwargs: Any
    ):
        """Initialize a SideNav.

        Args:
            master (Master | None): Parent widget.
            icon_only (bool): Show only icons, no text. Default False.
            signal (Signal | None): Reactive signal for selection state.
            variable (Variable | None): Tk variable for selection state.
            item_color (str): Color for navigation items. Default 'ghost'.
            **kwargs: Additional arguments passed to Frame (including color
                for container background).
        """
        kwargs.setdefault('padding', 4)
        super().__init__(master, **kwargs)

        self._icon_only = icon_only
        self._item_color = item_color

        # Selection state - create signal if neither provided
        if signal is not None:
            self._signal = signal
            binding = normalize_signal(signal)
            self._variable = binding.variable if binding else None
        elif variable is not None:
            self._signal = None
            self._variable = variable
        else:
            # Create internal signal for selection
            self._signal = create_signal('')
            binding = normalize_signal(self._signal)
            self._variable = binding.variable if binding else None

        # Track variable changes
        if self._variable:
            self._variable.trace_add('write', self._on_variable_changed)

        # Item tracking
        self._items: dict[str, RadioToggle] = {}
        self._item_order: list[str] = []

    def _on_variable_changed(self, *args):
        """Handle selection variable changes."""
        if self._variable:
            key = self._variable.get()
            self.event_generate('<<SelectionChanged>>', data={'key': key})

    # --- Public API ---

    def add_item(
        self,
        key: str,
        text: str = '',
        icon: str | dict = None,
        **kwargs
    ) -> RadioToggle:
        """Add a navigation item.

        Args:
            key (str): Unique identifier for the item.
            text (str): Display text (ignored if icon_only=True).
            icon (str | dict | None): Icon name or configuration.
            **kwargs: Additional arguments passed to RadioToggle.

        Returns:
            RadioToggle: The created navigation item.

        Raises:
            ValueError: If an item with the given key already exists.
        """
        if key in self._items:
            raise ValueError(f"Item with key '{key}' already exists")

        # Configure item based on icon_only mode
        if self._icon_only:
            item = RadioToggle(
                self,
                icon=icon,
                icon_only=True,
                variable=self._variable,
                value=key,
                color=self._item_color,
                **kwargs
            )
        else:
            item = RadioToggle(
                self,
                text=text,
                icon=icon,
                compound='left' if icon else None,
                variable=self._variable,
                value=key,
                color=self._item_color,
                padding=(12, 8),
                anchor='w',
                **kwargs
            )

        item.pack(fill='x', pady=1)

        self._items[key] = item
        self._item_order.append(key)

        return item

    def add_header(self, text: str, **kwargs) -> Label:
        """Add a section header.

        Args:
            text (str): Header text.
            **kwargs: Additional arguments passed to Label.

        Returns:
            Label: The created header label.
        """
        # Skip headers in icon-only mode
        if self._icon_only:
            return None

        header = Label(
            self,
            text=text,
            font='label',
            color='secondary',
            padding=(8, 12, 8, 4),
            **kwargs
        )
        header.pack(fill='x')
        return header

    def add_separator(self, **kwargs) -> Separator:
        """Add a visual separator.

        Args:
            **kwargs: Additional arguments passed to Separator.

        Returns:
            Separator: The created separator.
        """
        sep = Separator(self, orient='horizontal', **kwargs)
        sep.pack(fill='x', pady=8)
        return sep

    def get_item(self, key: str) -> RadioToggle | None:
        """Get an item by key.

        Args:
            key (str): The item key.

        Returns:
            RadioToggle | None: The item, or None if not found.
        """
        return self._items.get(key)

    def remove_item(self, key: str) -> None:
        """Remove an item by key.

        Args:
            key (str): The item key to remove.
        """
        if key in self._items:
            item = self._items.pop(key)
            self._item_order.remove(key)
            item.destroy()

    def select(self, key: str) -> None:
        """Select an item by key.

        Args:
            key (str): The item key to select.
        """
        if self._variable and key in self._items:
            self._variable.set(key)

    # --- Properties ---

    @property
    def selected_key(self) -> str | None:
        """Get the currently selected item key."""
        if self._variable:
            value = self._variable.get()
            return value if value else None
        return None

    @property
    def items(self) -> list[RadioToggle]:
        """Get all items in order."""
        return [self._items[key] for key in self._item_order]

    @property
    def signal(self) -> 'Signal[str] | None':
        """Get the selection signal."""
        return self._signal

    @property
    def variable(self) -> Variable | None:
        """Get the selection variable."""
        return self._variable

    @property
    def icon_only(self) -> bool:
        """Check if in icon-only mode."""
        return self._icon_only

    # --- Event Binding Helpers ---

    def on_selection_changed(self, callback) -> str:
        """Bind to ``<<SelectionChanged>>``.

        Args:
            callback: Function to call when selection changes.

        Returns:
            str: Binding identifier.
        """
        return self.bind('<<SelectionChanged>>', callback, add='+')

    def off_selection_changed(self, bind_id: str = None) -> None:
        """Unbind from ``<<SelectionChanged>>``."""
        self.unbind('<<SelectionChanged>>', bind_id)
