"""NavigationViewItem widget for selectable navigation items."""

from __future__ import annotations

from tkinter import Variable
from typing import Any, TYPE_CHECKING

from ttkbootstrap.widgets.primitives.frame import Frame
from ttkbootstrap.widgets.primitives.radiotoggle import RadioToggle
from ttkbootstrap.widgets.mixins import configure_delegate
from ttkbootstrap.widgets.types import Master

if TYPE_CHECKING:
    from ttkbootstrap.core.signals import Signal


class NavigationViewItem(Frame):
    """A selectable navigation item with icon and text.

    NavigationViewItem provides a clickable item for navigation menus.
    Items can exist at the root level or within a NavigationViewGroup.
    Selection is managed via a shared variable for radio-group behavior.

    Uses RadioToggle internally for consistent styling and built-in
    selection state management.

    Virtual events:
        ``<<ItemInvoked>>``: Fired when the item is clicked.
            event.data = {'key': str}

    Example:
        ```python
        # Items are created via NavigationView.add_item()
        nav.add_item('home', text='Home', icon='house')
        nav.add_item('local', text='Local', icon='hdd', group='files')
        ```
    """

    def __init__(
        self,
        master: Master = None,
        key: str = '',
        text: str = '',
        icon: str | dict = None,
        signal: 'Signal[Any]' = None,
        variable: Variable = None,
        is_enabled: bool = True,
        **kwargs: Any
    ):
        """Initialize a NavigationViewItem.

        Args:
            master (Master | None): Parent widget.
            key (str): Unique identifier for this item (used as selection value).
            text (str): Display text for the item.
            icon (str | dict | None): Icon name or configuration dict.
            signal (Signal | None): Reactive signal for selection state (preferred).
            variable (Variable | None): Shared variable for radio group selection.
            is_enabled (bool): Whether the item is interactive. Default True.
            **kwargs: Additional arguments passed to Frame.
        """
        if not key:
            raise ValueError("NavigationViewItem requires a non-empty 'key'")

        super().__init__(master, **kwargs)

        self._key = key
        self._text = text
        self._icon = icon
        self._signal = signal
        self._variable = variable
        self._is_enabled = is_enabled

        # Compact mode state
        self._compact = False

        # Widget references - two toggles: one full, one compact (icon only)
        self._toggle_full: RadioToggle | None = None
        self._toggle_compact: RadioToggle | None = None

        # Build internal structure
        self._build_widget()

        # Apply initial state
        if not is_enabled:
            self._toggle_full.state(['disabled'])
            self._toggle_compact.state(['disabled'])

    def _build_widget(self):
        """Build the internal widget structure."""
        # Full mode toggle (icon + text)
        self._toggle_full = RadioToggle(
            self,
            text=self._text,
            icon=self._icon,
            compound='left',
            variable=self._variable,
            value=self._key,
            anchor='w',
            bootstyle='primary-ghost',
            command=self._on_invoked,
        )
        self._toggle_full.pack(fill='x')

        # Compact mode toggle (icon only)
        self._toggle_compact = RadioToggle(
            self,
            icon=self._icon,
            icon_only=True,
            variable=self._variable,
            value=self._key,
            bootstyle='primary-ghost',
            command=self._on_invoked,
        )
        # Don't pack yet - only shown in compact mode

    def _on_invoked(self):
        """Handle toggle selection."""
        # Fire invoked event
        self.event_generate('<<ItemInvoked>>', data={'key': self._key})

    # --- Public API ---

    def select(self) -> None:
        """Select this item (set the variable to this item's key)."""
        if self._variable is not None:
            self._variable.set(self._key)

    def set_enabled(self, enabled: bool) -> None:
        """Set the enabled state.

        Args:
            enabled (bool): True to enable, False to disable.
        """
        self._is_enabled = enabled
        state = ['!disabled'] if enabled else ['disabled']
        if self._toggle_full:
            self._toggle_full.state(state)
        if self._toggle_compact:
            self._toggle_compact.state(state)

    def set_compact(self, compact: bool) -> None:
        """Set compact mode (icon only, no text).

        Args:
            compact (bool): True for compact mode, False for full display.
        """
        if self._compact == compact:
            return

        self._compact = compact

        if compact:
            # Switch to compact toggle
            self._toggle_full.pack_forget()
            self._toggle_compact.pack(fill='x')
        else:
            # Switch to full toggle
            self._toggle_compact.pack_forget()
            self._toggle_full.pack(fill='x')

    # --- Properties ---

    @property
    def key(self) -> str:
        """Get the item's unique key."""
        return self._key

    @property
    def is_selected(self) -> bool:
        """Check if this item is currently selected."""
        if self._variable is not None:
            return self._variable.get() == self._key
        return False

    @property
    def is_enabled(self) -> bool:
        """Check if this item is enabled."""
        return self._is_enabled

    @property
    def signal(self) -> 'Signal[Any] | None':
        """Get the signal for selection state."""
        return self._signal

    @property
    def variable(self) -> Variable | None:
        """Get the variable for selection state."""
        return self._variable

    # --- Configuration Delegates ---

    @configure_delegate('text')
    def _delegate_text(self, value: str = None):
        """Configure the item text."""
        if value is None:
            return self._text
        self._text = value
        if self._toggle_full:
            self._toggle_full.configure(text=value)
        return None

    @configure_delegate('icon')
    def _delegate_icon(self, value: str | dict = None):
        """Configure the item icon."""
        if value is None:
            return self._icon
        self._icon = value
        if self._toggle_full:
            self._toggle_full.configure(icon=value)
        if self._toggle_compact:
            self._toggle_compact.configure(icon=value)
        return None

    # --- Event Binding Helpers ---

    def on_invoked(self, callback) -> str:
        """Bind to ``<<ItemInvoked>>``.

        Args:
            callback: Function to call when item is invoked.

        Returns:
            str: Binding identifier for use with off_invoked().
        """
        return self.bind('<<ItemInvoked>>', callback, add='+')

    def off_invoked(self, bind_id: str = None) -> None:
        """Unbind from ``<<ItemInvoked>>``.

        Args:
            bind_id (str | None): Binding identifier from on_invoked().
        """
        self.unbind('<<ItemInvoked>>', bind_id)