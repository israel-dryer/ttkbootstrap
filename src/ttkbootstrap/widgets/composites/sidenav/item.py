"""SideNavItem widget for selectable navigation items."""

from __future__ import annotations

from tkinter import Variable
from typing import Any, Callable, TYPE_CHECKING

from typing_extensions import TypedDict, Unpack

from ttkbootstrap.widgets.primitives.frame import Frame
from ttkbootstrap.widgets.primitives.label import Label
from ttkbootstrap.widgets.composites.compositeframe import CompositeFrame
from ttkbootstrap.widgets.mixins import configure_delegate
from ttkbootstrap.widgets.types import Master

if TYPE_CHECKING:
    from ttkbootstrap.core.signals import Signal


class SideNavItemKwargs(TypedDict, total=False):
    """Keyword arguments for SideNavItem."""

    key: str
    text: str
    icon: Any
    signal: Any
    variable: Variable
    is_enabled: bool
    indent_level: int
    command: Callable
    padding_x: int
    padding_y: int
    icon_gap: int
    accent: str
    variant: str
    # Frame options
    padding: Any
    width: int
    height: int


class SideNavItem(Frame):
    """A selectable navigation item with icon and text.

    SideNavItem uses a CompositeFrame container with separate icon and
    text label children. This provides synchronized hover/pressed/selected
    states across all elements and precise control over layout.

    The widget supports expanded and compact modes. In compact mode, only the
    icon is displayed and it remains perfectly centered due to symmetrical
    padding. In expanded mode, both icon and text are visible.

    Uses NavigationButton.TFrame for the container (with selection indicator)
    and NavigationButton.TLabel for the icon and text labels.

    !!! note "Events"
        - `<<ItemInvoked>>`: Fired when the item is clicked.
          `event.data = {'key': str}`

    Example:
        ```python
        # Items are typically created via SideNav.add_item()
        nav.add_item('home', text='Home', icon='house')
        nav.add_item('local', text='Local', icon='hdd', group='files')
        ```

    """

    # Default indent width in pixels per indent level
    INDENT_WIDTH = 24

    # Default padding values
    DEFAULT_PADDING_X = 12  # Horizontal padding on left/right edges
    DEFAULT_PADDING_Y = 6   # Vertical padding
    DEFAULT_ICON_GAP = 10   # Gap between icon and text in expanded mode
    COMPACT_PADDING_X = 6   # Reduced horizontal padding in compact mode
    COMPACT_PADDING_Y = 6   # Reduced vertical padding in compact mode

    def __init__(
        self,
        master: Master = None,
        key: str = '',
        text: str = '',
        icon: str | dict = None,
        signal: 'Signal[Any]' = None,
        variable: Variable = None,
        is_enabled: bool = True,
        indent_level: int = 0,
        command: Callable = None,
        padding_x: int = None,
        padding_y: int = None,
        icon_gap: int = None,
        **kwargs: Unpack[SideNavItemKwargs]
    ):
        """Initialize a SideNavItem.

        Args:
            master (Master | None): Parent widget.
            key (str): Unique identifier for this item (used as selection value).
            text (str): Display text for the item.
            icon (str | dict | None): Icon name or configuration dict.
            signal (Signal | None): Reactive signal for selection state (preferred).
            variable (Variable | None): Shared variable for radio group selection.
            is_enabled (bool): Whether the item is interactive. Default True.
            indent_level (int): Nesting level for indentation (0 = root, 1 = child). Default 0.
            command (Callable | None): Callback invoked when item is clicked.
            padding_x (int | None): Horizontal padding on edges. Default is 12.
            padding_y (int | None): Vertical padding. Default is 8.
            icon_gap (int | None): Gap between icon and text. Default is 8.
            **kwargs: Additional arguments passed to Frame.

        """
        if not key:
            raise ValueError("SideNavItem requires a non-empty 'key'")

        # Extract styling kwargs before super().__init__
        # Must set these AFTER super().__init__ because TTKWrapperBase also sets _accent/_variant
        saved_accent = kwargs.pop('accent', 'primary')
        saved_variant = kwargs.pop('variant', None)

        super().__init__(master, **kwargs)

        # Set after super() to avoid being overwritten by TTKWrapperBase
        self._accent = saved_accent
        self._variant = saved_variant

        self._key = key
        self._text = text
        self._icon = icon
        self._signal = signal
        self._variable = variable
        self._is_enabled = is_enabled
        self._indent_level = indent_level
        self._command = command
        self._padding_x = padding_x if padding_x is not None else self.DEFAULT_PADDING_X
        self._padding_y = padding_y if padding_y is not None else self.DEFAULT_PADDING_Y
        self._icon_gap = icon_gap if icon_gap is not None else self.DEFAULT_ICON_GAP

        # Compact mode state
        self._compact = False

        # Widget references
        self._container: CompositeFrame | None = None
        self._icon_label: Label | None = None
        self._text_label: Label | None = None

        # Variable trace
        self._trace_id: str | None = None

        # Build internal structure
        self._build_widget()

        # Set up variable trace for selection state
        self._setup_variable_trace()

        # Apply initial enabled state
        if not is_enabled:
            self._container.set_disabled(True)

    def _build_widget(self):
        """Build the internal widget structure."""
        # Calculate indentation padding for expanded mode
        indent_padding = self._indent_level * self.INDENT_WIDTH
        left_padding = self._padding_x + indent_padding

        # CompositeFrame container with selection indicator
        # Uses NavigationButton.TFrame style which has the nav-button assets
        self._container = CompositeFrame(
            self,
            ttk_class='NavigationButton.TFrame',
            accent=self._accent,
            padding=(left_padding, self._padding_y, self._padding_x, self._padding_y),
            takefocus=True,
        )
        self._container.pack(fill='x')

        # Icon label (optional)
        if self._icon:
            self._icon_label = Label(
                self._container,
                icon=self._icon,
                icon_only=True,
                ttk_class='NavigationButton.TLabel',
                accent=self._accent,
                takefocus=False,
            )
            self._container.register_composite(self._icon_label)

        # Text label
        self._text_label = Label(
            self._container,
            text=self._text,
            anchor='w',
            ttk_class='NavigationButton.TLabel',
            accent=self._accent,
            takefocus=False,
        )
        self._container.register_composite(self._text_label)

        # Apply initial layout
        self._apply_layout()

        # Bind click events - only to container, events bubble up from children
        self._bind_events()

    def _apply_layout(self):
        """Apply the current layout based on compact mode."""
        # Clear current layout
        if self._icon_label:
            self._icon_label.pack_forget()
        self._text_label.pack_forget()

        if self._compact:
            # Compact mode: tighter symmetrical padding, icon centered
            px = self.COMPACT_PADDING_X
            py = self.COMPACT_PADDING_Y
            self._container.configure(padding=(px, py, px, py))
            if self._icon_label:
                self._icon_label.pack(expand=True)
        else:
            # Expanded mode: icon + text, with indent
            indent_padding = self._indent_level * self.INDENT_WIDTH
            left_padding = self._padding_x + indent_padding
            self._container.configure(
                padding=(left_padding, self._padding_y, self._padding_x, self._padding_y)
            )
            if self._icon_label:
                self._icon_label.pack(side='left', padx=(0, self._icon_gap))
            self._text_label.pack(side='left', fill='x', expand=True)

    def _bind_events(self):
        """Bind click and keyboard events.

        Binds click to container and all child widgets since Tkinter
        doesn't bubble events from children to parents.
        """
        self._container.bind('<Button-1>', self._on_click, add='+')
        if self._icon_label:
            self._icon_label.bind('<Button-1>', self._on_click, add='+')
        self._text_label.bind('<Button-1>', self._on_click, add='+')

        # Keyboard support on focusable container
        self._container.bind('<Return>', self._on_click, add='+')
        self._container.bind('<space>', self._on_click, add='+')

    def _setup_variable_trace(self):
        """Set up variable trace for selection state updates.

        Note: For performance, the SideNav now manages selection updates
        centrally rather than each item tracing the variable. This method is
        kept for backwards compatibility but does nothing when used with
        SideNav.
        """
        # Selection state is now managed by SideNav._on_selection_changed()
        # which only updates the affected items rather than all items.
        # Initial state update
        self._update_selection_state()

    def _update_selection_state(self):
        """Update visual state based on selection."""
        if self._variable is not None and self._key:
            selected = self._variable.get() == self._key
            self._container.set_selected(selected)

    def set_selected(self, selected: bool) -> None:
        """Directly set the selection visual state.

        This is called by SideNav for efficient selection updates,
        avoiding the need to query the variable.

        Args:
            selected: True to show as selected, False otherwise.

        """
        self._container.set_selected(selected)

    def _on_click(self, event=None):
        """Handle item click."""
        if not self._is_enabled:
            return

        # Request focus
        self._container.focus_set()

        # Set selection if variable is configured
        if self._variable is not None and self._key:
            self._variable.set(self._key)

        # Fire invoked event
        self.event_generate('<<ItemInvoked>>', data={'key': self._key})

        # Call command if set
        if self._command:
            self._command()

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
        self._container.set_disabled(not enabled)

    def set_compact(self, compact: bool) -> None:
        """Set compact mode (icon only, no text).

        Args:
            compact (bool): True for compact mode, False for full display.

        """
        if self._compact == compact:
            return

        self._compact = compact
        self._apply_layout()
        self._update_selection_state()

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
        if self._text_label:
            self._text_label.configure(text=value)
        return None

    @configure_delegate('icon')
    def _delegate_icon(self, value: str | dict = None):
        """Configure the item icon."""
        if value is None:
            return self._icon
        self._icon = value

        if self._icon_label is not None:
            self._icon_label.configure(icon=value)
        elif value is not None:
            # Create icon label if it doesn't exist
            self._icon_label = Label(
                self._container,
                icon=value,
                icon_only=True,
                ttk_class='NavigationButton.TLabel',
                accent=self._accent,
                takefocus=False,
            )
            self._container.register_composite(self._icon_label)
            self._icon_label.bind('<Button-1>', self._on_click, add='+')
            # Re-apply layout
            self._apply_layout()
        return None

    @configure_delegate('command')
    def _delegate_command(self, value: Callable = None):
        """Configure the command callback."""
        if value is None:
            return self._command
        self._command = value
        return None

    # --- Event Binding Helpers ---

    def on_invoked(self, callback) -> str:
        """Bind to `<<ItemInvoked>>`.

        Args:
            callback: Function to call when item is invoked.

        Returns:
            str: Binding identifier for use with off_invoked().

        """
        return self.bind('<<ItemInvoked>>', callback, add='+')

    def off_invoked(self, bind_id: str = None) -> None:
        """Unbind from `<<ItemInvoked>>`.

        Args:
            bind_id (str | None): Binding identifier from on_invoked().

        """
        self.unbind('<<ItemInvoked>>', bind_id)
