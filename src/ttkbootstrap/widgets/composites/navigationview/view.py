"""NavigationView widget - a sidebar navigation container."""

from __future__ import annotations

from tkinter import Variable
from typing import Any, Literal, TYPE_CHECKING

from ttkbootstrap.widgets.primitives.frame import Frame
from ttkbootstrap.widgets.primitives.button import Button
from ttkbootstrap.widgets.primitives.label import Label
from ttkbootstrap.widgets.primitives.separator import Separator
from ttkbootstrap.widgets.composites.scrollview import ScrollView
from ttkbootstrap.widgets.composites.toolbar import Toolbar
from ttkbootstrap.widgets.composites.navigationview.item import NavigationViewItem
from ttkbootstrap.widgets.composites.navigationview.group import NavigationViewGroup
from ttkbootstrap.widgets.composites.navigationview.header import NavigationViewHeader
from ttkbootstrap.widgets.composites.navigationview.separator import NavigationViewSeparator
from ttkbootstrap.widgets.mixins import configure_delegate
from ttkbootstrap.widgets.types import Master
from ttkbootstrap.core.signals import Signal


DisplayMode = Literal['expanded', 'compact', 'minimal']


class NavigationView(Frame):
    """A sidebar navigation container with header, scrollable items, and footer.

    NavigationView provides a complete navigation solution with:
    - Pane header with optional title and menu button
    - Scrollable navigation items area
    - Groups for organizing related items (expand/collapse in expanded mode,
      popup flyout in compact mode)
    - Footer section for settings and other fixed items
    - Display modes: expanded (full), compact (icons only), minimal (hidden)

    The pane manages a shared selection variable/signal that all items use
    for radio-group behavior.

    !!! note "Events"
        - ``<<PaneToggled>>``: Fired when pane is opened/closed.
          ``event.data = {'is_open': bool}``
        - ``<<DisplayModeChanged>>``: Fired when display mode changes.
          ``event.data = {'mode': str}``
        - ``<<SelectionChanged>>``: Fired when selected item changes.
          ``event.data = {'key': str}``
        - ``<<BackRequested>>``: Fired when back button is clicked.

    Example:
        ```python
        nav = NavigationView(root, title='My App')

        # Add root-level items
        nav.add_item('home', text='Home', icon='house')
        nav.add_item('docs', text='Documents', icon='file-earmark-text')

        # Add a group with items
        nav.add_group('files', text='Files', icon='folder')
        nav.add_item('local', text='Local', icon='hdd', group='files')
        nav.add_item('cloud', text='Cloud', icon='cloud', group='files')

        # Add section header
        nav.add_header('Favorites')
        nav.add_item('photos', text='Photos', icon='image')

        # Add footer item
        nav.add_footer_item('settings', text='Settings', icon='gear')

        # Bind to selection
        nav.on_selection_changed(lambda e: print(f"Selected: {e.data['key']}"))
        ```
    """

    # Default pane widths
    PANE_WIDTH_EXPANDED = 280
    PANE_WIDTH_COMPACT = 56

    def __init__(
        self,
        master: Master = None,
        title: str = '',
        show_header: bool = True,
        show_back_button: bool = False,
        show_menu_button: bool = True,
        display_mode: DisplayMode = 'expanded',
        is_pane_open: bool = True,
        pane_width: int = None,
        signal: 'Signal[str]' = None,
        variable: Variable = None,
        **kwargs: Any
    ):
        """Initialize a NavigationView.

        Args:
            master (Master | None): Parent widget.
            title (str): Title displayed in the pane header.
            show_header (bool): Show internal header with toolbar. Default True.
                Set to False when using an external toolbar.
            show_back_button (bool): Show back button in header. Default False.
            show_menu_button (bool): Show hamburger menu button. Default True.
            display_mode (DisplayMode): Initial display mode. Default 'expanded'.
            is_pane_open (bool): Initial pane state. Default True.
            pane_width (int | None): Custom pane width. Uses default based on mode.
            signal (Signal | None): Reactive signal for selection state.
            variable (Variable | None): Tk variable for selection state.
            **kwargs: Additional arguments passed to Frame.
        """
        super().__init__(master, **kwargs)

        self._title = title
        self._show_header = show_header
        self._show_back_button = show_back_button
        self._show_menu_button = show_menu_button
        self._display_mode = display_mode
        self._is_pane_open = is_pane_open
        self._pane_width = pane_width

        # Selection state - create signal if neither provided
        if signal is not None:
            self._signal = signal
        elif variable is not None:
            self._signal = None
            self._variable = variable
        else:
            # Create internal signal for selection
            self._signal = Signal('')

        # Get the variable for items (from signal or direct)
        self._selection_var = self._signal._var if self._signal else variable

        # Track variable changes
        if self._selection_var:
            self._selection_var.trace_add('write', self._on_selection_changed)

        # Item and group tracking
        self._items: dict[str, NavigationViewItem] = {}  # All items by key
        self._groups: dict[str, NavigationViewGroup] = {}  # Groups by key
        self._footer_items: dict[str, NavigationViewItem] = {}
        self._headers: list[NavigationViewHeader] = []
        self._separators: list[NavigationViewSeparator] = []

        # Track all content widgets in order for proper re-packing
        self._content_widgets: list = []
        self._footer_order: list[str] = []

        # Widget references
        self._pane_frame: Frame | None = None
        self._header_frame: Frame | None = None
        self._content_scroll: ScrollView | None = None
        self._content_frame: Frame | None = None
        self._footer_frame: Frame | None = None
        self._menu_button: Button | None = None
        self._back_button: Button | None = None
        self._title_label: Label | None = None

        # Build the widget
        self._build_widget()

    def _build_widget(self):
        """Build the internal widget structure."""
        # Pane container
        pane_width = self._pane_width or self.PANE_WIDTH_EXPANDED
        self._pane_frame = Frame(self, width=pane_width, padding=4)
        self._pane_frame.pack(side='left', fill='y')
        self._pane_frame.pack_propagate(False)  # Fixed width

        # Header section (optional - can be disabled when using external toolbar)
        self._toolbar = None
        if self._show_header:
            self._build_header()
            # Separator after header
            Separator(self._pane_frame, orient='horizontal').pack(fill='x', pady=(0, 4))

        # Scrollable content area (vertical only, scrollbar on hover)
        self._content_scroll = ScrollView(
            self._pane_frame,
            direction='vertical',
            show_scrollbar='on-hover',
        )
        self._content_scroll.pack(fill='both', expand=True)
        self._content_frame = self._content_scroll.add()

        # Configure grid column to expand
        self._content_frame.columnconfigure(0, weight=1)

        # Stretch content to fill width when canvas resizes
        def on_canvas_resize(event):
            self._content_scroll.canvas.itemconfigure(
                self._content_scroll._window_id,
                width=event.width
            )
        self._content_scroll.canvas.bind('<Configure>', on_canvas_resize, add='+')

        # Footer section
        self._footer_frame = Frame(self._pane_frame)
        self._footer_frame.pack(side='bottom', fill='x')

        # Separator before footer (shown when footer has items)
        self._footer_separator = Separator(self._pane_frame, orient='horizontal')

        # Apply initial display mode
        self._apply_display_mode()

    def _build_header(self):
        """Build the pane header using Toolbar."""
        # Create toolbar for header
        self._toolbar = Toolbar(self._pane_frame, padding=(4, 4))
        self._toolbar.pack(fill='x')

        # Back button (optional)
        if self._show_back_button:
            self._back_button = self._toolbar.add_button(
                icon={'name': 'arrow-left', 'size': 16},
                command=self._on_back_clicked,
            )

        # Menu button (hamburger)
        if self._show_menu_button:
            self._menu_button = self._toolbar.add_button(
                icon={'name': 'list', 'size': 16},
                command=self.toggle_pane,
            )

        # Title
        if self._title:
            self._title_label = self._toolbar.add_label(
                text=self._title,
                font='heading-md',
            )

    def _apply_display_mode(self):
        """Apply the current display mode to the pane."""
        is_compact = self._display_mode == 'compact'

        if self._display_mode == 'expanded':
            width = self._pane_width or self.PANE_WIDTH_EXPANDED
            self._pane_frame.configure(width=width)
            if self._is_pane_open:
                self._pane_frame.pack(side='left', fill='y')
            else:
                self._pane_frame.pack_forget()
        elif self._display_mode == 'compact':
            self._pane_frame.configure(width=self.PANE_WIDTH_COMPACT)
            self._pane_frame.pack(side='left', fill='y')
        elif self._display_mode == 'minimal':
            if self._is_pane_open:
                width = self._pane_width or self.PANE_WIDTH_EXPANDED
                self._pane_frame.configure(width=width)
                self._pane_frame.pack(side='left', fill='y')
            else:
                self._pane_frame.pack_forget()

        # Hide section headers in compact mode
        for header in self._headers:
            if is_compact:
                header.grid_remove()
            else:
                header.grid()

        # Hide only the title in compact mode (keep back and menu buttons visible)
        if self._title_label:
            if is_compact:
                self._title_label.pack_forget()
            else:
                self._title_label.pack(side='left', fill='x', expand=True)

        # Set compact mode on all items and groups
        for item in self._items.values():
            # Only set compact on root items (not in groups)
            if not self._get_item_group(item.key):
                item.set_compact(is_compact)

        for group in self._groups.values():
            group.set_compact(is_compact)

        for item in self._footer_items.values():
            item.set_compact(is_compact)

    def _get_item_group(self, key: str) -> str | None:
        """Get the group key for an item, or None if at root."""
        for group_key, group in self._groups.items():
            if key in group._items:
                return group_key
        return None

    def _on_selection_changed(self, *args):
        """Handle selection variable changes."""
        if self._selection_var:
            key = self._selection_var.get()
            self.event_generate('<<SelectionChanged>>', data={'key': key})

    def _on_back_clicked(self):
        """Handle back button click."""
        self.event_generate('<<BackRequested>>')

    # --- Public API: Groups ---

    def add_group(
        self,
        key: str,
        text: str = '',
        icon: str | dict = None,
        is_expanded: bool = False,
        **kwargs
    ) -> NavigationViewGroup:
        """Add a navigation group to the pane.

        Groups contain related items and can be expanded/collapsed in expanded
        mode. In compact mode, clicking a group shows a popup with its items.

        Args:
            key (str): Unique identifier for the group.
            text (str): Display text.
            icon (str | dict | None): Icon name or configuration.
            is_expanded (bool): Initial expansion state. Default False.
            **kwargs: Additional arguments passed to NavigationViewGroup.

        Returns:
            NavigationViewGroup: The created group.

        Raises:
            ValueError: If a group or item with the given key already exists.
        """
        if key in self._groups or key in self._items or key in self._footer_items:
            raise ValueError(f"Key '{key}' already exists")

        group = NavigationViewGroup(
            self._content_frame,
            key=key,
            text=text,
            icon=icon,
            variable=self._selection_var,
            is_expanded=is_expanded,
            **kwargs
        )
        row = len(self._content_widgets)
        group.grid(row=row, column=0, sticky='ew')

        self._groups[key] = group
        self._content_widgets.append(group)

        # Apply current display mode
        if self._display_mode == 'compact':
            group.set_compact(True)

        return group

    # --- Public API: Items ---

    def add_item(
        self,
        key: str,
        text: str = '',
        icon: str | dict = None,
        group: str = None,
        **kwargs
    ) -> NavigationViewItem:
        """Add a navigation item to the pane.

        Args:
            key (str): Unique identifier for the item.
            text (str): Display text.
            icon (str | dict | None): Icon name or configuration.
            group (str | None): Key of the group to add this item to.
                If None, item is added at root level.
            **kwargs: Additional arguments passed to NavigationViewItem.

        Returns:
            NavigationViewItem: The created item.

        Raises:
            ValueError: If an item with the given key already exists.
            ValueError: If the specified group does not exist.
        """
        if key in self._items or key in self._groups or key in self._footer_items:
            raise ValueError(f"Key '{key}' already exists")

        if group is not None:
            # Add to a group
            if group not in self._groups:
                raise ValueError(f"Group '{group}' does not exist")

            target_group = self._groups[group]
            item = NavigationViewItem(
                target_group.content_frame,
                key=key,
                text=text,
                icon=icon,
                variable=self._selection_var,
                **kwargs
            )
            item.pack(fill='x', padx=(16, 0))  # indent on left only

            # Register with group
            target_group._add_item(item)
        else:
            # Add at root level
            item = NavigationViewItem(
                self._content_frame,
                key=key,
                text=text,
                icon=icon,
                variable=self._selection_var,
                **kwargs
            )
            row = len(self._content_widgets)
            item.grid(row=row, column=0, sticky='ew')
            self._content_widgets.append(item)

            # Apply current display mode
            if self._display_mode == 'compact':
                item.set_compact(True)

        self._items[key] = item
        return item

    def add_header(self, text: str, **kwargs) -> NavigationViewHeader:
        """Add a section header to the pane.

        Headers are hidden in compact display mode.

        Args:
            text (str): Header text.
            **kwargs: Additional arguments passed to NavigationViewHeader.

        Returns:
            NavigationViewHeader: The created header.
        """
        header = NavigationViewHeader(self._content_frame, text=text, **kwargs)
        self._headers.append(header)

        row = len(self._content_widgets)
        header.grid(row=row, column=0, sticky='ew')
        self._content_widgets.append(header)

        # Hide if in compact mode
        if self._display_mode == 'compact':
            header.grid_remove()

        return header

    def add_separator(self, **kwargs) -> NavigationViewSeparator:
        """Add a separator to the pane.

        Args:
            **kwargs: Additional arguments passed to NavigationViewSeparator.

        Returns:
            NavigationViewSeparator: The created separator.
        """
        sep = NavigationViewSeparator(self._content_frame, **kwargs)
        row = len(self._content_widgets)
        sep.grid(row=row, column=0, sticky='ew')
        self._content_widgets.append(sep)
        self._separators.append(sep)
        return sep

    def add_footer_item(
        self,
        key: str,
        text: str = '',
        icon: str | dict = None,
        **kwargs
    ) -> NavigationViewItem:
        """Add a navigation item to the footer section.

        Args:
            key (str): Unique identifier for the item.
            text (str): Display text.
            icon (str | dict | None): Icon name or configuration.
            **kwargs: Additional arguments passed to NavigationViewItem.

        Returns:
            NavigationViewItem: The created item.

        Raises:
            ValueError: If an item with the given key already exists.
        """
        if key in self._items or key in self._groups or key in self._footer_items:
            raise ValueError(f"Key '{key}' already exists")

        # Show footer separator if this is the first footer item
        if not self._footer_items:
            self._footer_separator.pack(fill='x', pady=4)

        item = NavigationViewItem(
            self._footer_frame,
            key=key,
            text=text,
            icon=icon,
            variable=self._selection_var,
            **kwargs
        )
        item.pack(fill='x')

        self._footer_items[key] = item
        self._footer_order.append(key)

        # Apply current display mode
        if self._display_mode == 'compact':
            item.set_compact(True)

        return item

    def node(self, key: str) -> NavigationViewItem:
        """Get an item by key.

        Args:
            key (str): The item key.

        Returns:
            NavigationViewItem: The item.

        Raises:
            KeyError: If no item with the given key exists.
        """
        if key in self._items:
            return self._items[key]
        if key in self._footer_items:
            return self._footer_items[key]
        raise KeyError(f"No item with key '{key}'")

    def nodes(self) -> tuple[NavigationViewItem, ...]:
        """Get all items (excluding footer items).

        Returns:
            A tuple of all NavigationViewItem instances.
        """
        return tuple(self._items.values())

    def node_keys(self) -> tuple[str, ...]:
        """Get all item keys (excluding footer items).

        Returns:
            A tuple of all item keys.
        """
        return tuple(self._items.keys())

    def group(self, key: str) -> NavigationViewGroup:
        """Get a group by key.

        Args:
            key (str): The group key.

        Returns:
            NavigationViewGroup: The group.

        Raises:
            KeyError: If no group with the given key exists.
        """
        if key not in self._groups:
            raise KeyError(f"No group with key '{key}'")
        return self._groups[key]

    def groups(self) -> tuple[NavigationViewGroup, ...]:
        """Get all groups.

        Returns:
            A tuple of all NavigationViewGroup instances.
        """
        return tuple(self._groups.values())

    def configure_node(self, key: str, option: str = None, **kwargs: Any):
        """Configure a specific item by its key.

        Args:
            key: The key of the item to configure.
            option: If provided, return the value of this option.
            **kwargs: Configuration options to apply to the item.

        Returns:
            If option is provided, returns the value of that option.
        """
        item = self.node(key)
        if option is not None:
            return item.cget(option)
        item.configure(**kwargs)

    def remove_item(self, key: str) -> None:
        """Remove an item by key.

        Args:
            key (str): The item key to remove.
        """
        if key in self._items:
            item = self._items.pop(key)

            # Remove from group if in one
            group_key = self._get_item_group(key)
            if group_key:
                self._groups[group_key]._remove_item(key)

            # Remove from content widgets if at root
            if item in self._content_widgets:
                self._content_widgets.remove(item)

            item.destroy()

        elif key in self._footer_items:
            item = self._footer_items.pop(key)
            self._footer_order.remove(key)
            item.destroy()
            # Hide footer separator if no more footer items
            if not self._footer_items:
                self._footer_separator.pack_forget()

    def remove_group(self, key: str) -> None:
        """Remove a group and all its items.

        Args:
            key (str): The group key to remove.
        """
        if key not in self._groups:
            return

        group = self._groups.pop(key)

        # Remove all items in the group
        for item_key in list(group._items.keys()):
            if item_key in self._items:
                del self._items[item_key]

        # Remove from content widgets
        if group in self._content_widgets:
            self._content_widgets.remove(group)

        group.destroy()

    def select(self, key: str) -> None:
        """Select an item by key.

        Args:
            key (str): The item key to select.
        """
        if self._selection_var:
            self._selection_var.set(key)

    # --- Public API: Pane Control ---

    def toggle_pane(self) -> None:
        """Toggle the pane between expanded and compact modes.

        In minimal mode, this toggles visibility instead.
        """
        if self._display_mode == 'minimal':
            # In minimal mode, toggle visibility
            self._is_pane_open = not self._is_pane_open
            self._apply_display_mode()
            self.event_generate('<<PaneToggled>>', data={'is_open': self._is_pane_open})
        else:
            # Toggle between expanded and compact
            new_mode = 'compact' if self._display_mode == 'expanded' else 'expanded'
            self.set_display_mode(new_mode)

    def open_pane(self) -> None:
        """Open the pane."""
        if not self._is_pane_open:
            self._is_pane_open = True
            self._apply_display_mode()
            self.event_generate('<<PaneToggled>>', data={'is_open': True})

    def close_pane(self) -> None:
        """Close the pane."""
        if self._is_pane_open:
            self._is_pane_open = False
            self._apply_display_mode()
            self.event_generate('<<PaneToggled>>', data={'is_open': False})

    def set_display_mode(self, mode: DisplayMode) -> None:
        """Set the display mode.

        Args:
            mode (DisplayMode): 'expanded', 'compact', or 'minimal'.
        """
        if mode != self._display_mode:
            self._display_mode = mode
            self._apply_display_mode()
            self.event_generate('<<DisplayModeChanged>>', data={'mode': mode})

    # --- Properties ---

    @property
    def is_pane_open(self) -> bool:
        """Check if the pane is open."""
        return self._is_pane_open

    @property
    def display_mode(self) -> DisplayMode:
        """Get the current display mode."""
        return self._display_mode

    @property
    def selected_key(self) -> str | None:
        """Get the currently selected item key."""
        if self._selection_var:
            return self._selection_var.get() or None
        return None

    def footer_nodes(self) -> tuple[NavigationViewItem, ...]:
        """Get all footer items in order.

        Returns:
            A tuple of all footer NavigationViewItem instances.
        """
        return tuple(self._footer_items[key] for key in self._footer_order)

    def footer_node_keys(self) -> tuple[str, ...]:
        """Get all footer item keys in order.

        Returns:
            A tuple of all footer item keys.
        """
        return tuple(self._footer_order)

    @property
    def signal(self) -> 'Signal[str] | None':
        """Get the selection signal."""
        return self._signal

    @property
    def variable(self) -> Variable | None:
        """Get the selection variable."""
        return self._selection_var

    # --- Configuration Delegates ---

    @configure_delegate('title')
    def _delegate_title(self, value: str = None):
        """Configure the pane title."""
        if value is None:
            return self._title
        self._title = value
        if self._title_label:
            self._title_label.configure(text=value)
        return None

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

    def on_back_requested(self, callback) -> str:
        """Bind to ``<<BackRequested>>``.

        Args:
            callback: Function to call when back button is clicked.

        Returns:
            str: Binding identifier.
        """
        return self.bind('<<BackRequested>>', callback, add='+')

    def off_back_requested(self, bind_id: str = None) -> None:
        """Unbind from ``<<BackRequested>>``."""
        self.unbind('<<BackRequested>>', bind_id)

    def on_pane_toggled(self, callback) -> str:
        """Bind to ``<<PaneToggled>>``.

        Args:
            callback: Function to call when pane is toggled.

        Returns:
            str: Binding identifier.
        """
        return self.bind('<<PaneToggled>>', callback, add='+')

    def off_pane_toggled(self, bind_id: str = None) -> None:
        """Unbind from ``<<PaneToggled>>``."""
        self.unbind('<<PaneToggled>>', bind_id)