"""NavigationViewGroup widget for grouping navigation items."""

from __future__ import annotations

from tkinter import TclError, Toplevel, Variable
from typing import Any, TYPE_CHECKING

from ttkbootstrap.widgets.primitives.frame import Frame
from ttkbootstrap.widgets.primitives.gridframe import GridFrame
from ttkbootstrap.widgets.primitives.label import Label
from ttkbootstrap.widgets.composites.compositeframe import CompositeFrame
from ttkbootstrap.widgets.composites.list import ListView
from ttkbootstrap.widgets.mixins import configure_delegate
from ttkbootstrap.widgets.types import Master

if TYPE_CHECKING:
    from ttkbootstrap.core.signals import Signal
    from ttkbootstrap.widgets.composites.navigationview.item import NavigationViewItem


class NavigationViewGroup(Frame):
    """A collapsible group of navigation items.

    NavigationViewGroup provides a container for related navigation items.
    In expanded mode, it behaves like an Expander with a chevron toggle.
    In compact mode, clicking the group shows a popup flyout to the right
    containing the group's items.

    Uses a single CompositeFrame container with separate icon, text, and
    chevron labels. In compact mode, text and chevron are hidden and the
    icon is centered.

    The group shows as selected if any of its child items are currently selected.

    !!! note "Events"
        - ``<<GroupExpanding>>``: Fired before the group expands.
          ``event.data = {'key': str}``
        - ``<<GroupCollapsed>>``: Fired after the group collapses.
          ``event.data = {'key': str}``

    Example:
        ```python
        # Groups are created via NavigationView.add_group()
        nav.add_group('files', text='Files', icon='folder')
        nav.add_item('local', text='Local', icon='hdd', group='files')
        nav.add_item('cloud', text='Cloud', icon='cloud', group='files')
        ```
    """

    # Default padding values (same as NavigationViewItem)
    DEFAULT_PADDING_X = 12
    DEFAULT_PADDING_Y = 10
    DEFAULT_ICON_GAP = 10

    def __init__(
        self,
        master: Master = None,
        key: str = '',
        text: str = '',
        icon: str | dict = None,
        signal: 'Signal[Any]' = None,
        variable: Variable = None,
        is_expanded: bool = False,
        **kwargs: Any
    ):
        """Initialize a NavigationViewGroup.

        Args:
            master (Master | None): Parent widget.
            key (str): Unique identifier for this group.
            text (str): Display text for the group.
            icon (str | dict | None): Icon name or configuration dict.
            signal (Signal | None): Reactive signal for selection state.
            variable (Variable | None): Shared variable for selection tracking.
            is_expanded (bool): Initial expansion state. Default False.
            **kwargs: Additional arguments passed to Frame.
        """
        if not key:
            raise ValueError("NavigationViewGroup requires a non-empty 'key'")

        # Extract styling kwargs before super().__init__
        # Must set these AFTER super().__init__ because TTKWrapperBase also sets _accent
        saved_accent = kwargs.pop('accent', 'primary')

        super().__init__(master, **kwargs)

        # Set after super() to avoid being overwritten by TTKWrapperBase
        self._accent = saved_accent

        self._key = key
        self._text = text
        self._icon = icon
        self._signal = signal
        self._variable = variable
        self._is_expanded = is_expanded

        # Track child items (managed by NavigationView)
        self._items: dict[str, 'NavigationViewItem'] = {}
        self._item_order: list[str] = []

        # Compact mode state
        self._compact = False

        # Widget references
        self._container: CompositeFrame | None = None
        self._icon_label: Label | None = None
        self._text_label: Label | None = None
        self._chevron_label: Label | None = None
        self._content_frame: Frame | None = None
        self._popup: Toplevel | None = None
        self._root_click_id: str | None = None

        # Selection state is now managed centrally by NavigationView
        # for better performance (only affected items are updated)
        self._trace_id: str | None = None

        # Build internal structure
        self._build_widget()

    def _build_widget(self):
        """Build the internal widget structure.

        Uses CompositeFrame with NavigationButton styles for the header.
        Child labels are registered for automatic state coordination.
        """
        # Container using NavigationButton.TFrame for selection indicator
        self._container = CompositeFrame(
            self,
            ttk_class='NavigationButton.TFrame',
            accent=self._accent,
            padding=(self.DEFAULT_PADDING_X, self.DEFAULT_PADDING_Y,
                     self.DEFAULT_PADDING_X, self.DEFAULT_PADDING_Y),
            takefocus=True,
        )
        self._container.pack(fill='x')

        # Icon label
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

        # Chevron for expand/collapse indicator
        self._chevron_label = Label(
            self._container,
            icon=self._get_chevron_icon(),
            icon_only=True,
            ttk_class='NavigationButton.TLabel',
            accent=self._accent,
            takefocus=False,
        )
        self._container.register_composite(self._chevron_label)

        # Apply initial layout
        self._apply_layout()

        # Bind click events
        self._bind_events()

        # Content frame for child items
        self._content_frame = GridFrame(
            self,
            columns=1,
            gap=(0, 0),
            sticky_items='ew',
        )
        if self._is_expanded:
            self._content_frame.pack(fill='both', expand=True)

        # Set initial selection state
        self._update_selection_state()

    def _apply_layout(self):
        """Apply the current layout based on compact mode."""
        # Clear current layout
        if self._icon_label:
            self._icon_label.pack_forget()
        self._text_label.pack_forget()
        self._chevron_label.pack_forget()

        if self._compact:
            # Compact mode: icon only, centered
            if self._icon_label:
                self._icon_label.pack(expand=True)
        else:
            # Expanded mode: icon + text + chevron
            if self._icon_label:
                self._icon_label.pack(side='left', padx=(0, self.DEFAULT_ICON_GAP))
            self._text_label.pack(side='left', fill='x', expand=True)
            self._chevron_label.pack(side='right')

    def _bind_events(self):
        """Bind click and keyboard events.

        Binds click to container and all child widgets since Tkinter
        doesn't bubble events from children to parents.
        """
        self._container.bind('<Button-1>', self._on_header_click, add='+')
        if self._icon_label:
            self._icon_label.bind('<Button-1>', self._on_header_click, add='+')
        self._text_label.bind('<Button-1>', self._on_header_click, add='+')
        self._chevron_label.bind('<Button-1>', self._on_header_click, add='+')

        # Keyboard support on focusable container
        self._container.bind('<Return>', self._on_header_click, add='+')
        self._container.bind('<space>', self._on_header_click, add='+')

    def _get_chevron_icon(self) -> dict:
        """Get the appropriate chevron icon for current state."""
        if self._is_expanded:
            return {'name': 'chevron-up', 'size': 16}
        else:
            return {'name': 'chevron-down', 'size': 16}

    def _on_header_click(self, event=None):
        """Handle header click - toggle expand/collapse or show popup."""
        self._container.focus_set()

        if self._compact:
            # In compact mode, show popup
            self._show_popup()
        else:
            # In expanded mode, toggle expand/collapse
            self.toggle()

    def _update_selection_state(self):
        """Update visual state based on whether any child is selected."""
        is_any_selected = self._is_any_child_selected()
        self._container.set_selected(is_any_selected)

    def set_child_selected(self, has_selected_child: bool) -> None:
        """Directly set whether a child is selected.

        This is called by NavigationView for efficient selection updates,
        avoiding the need to iterate through children.

        Args:
            has_selected_child: True if any child item is selected.
        """
        self._container.set_selected(has_selected_child)

    def _is_any_child_selected(self) -> bool:
        """Check if any child item is currently selected."""
        if not self._variable:
            return False
        current = self._variable.get()
        return current in self._items

    def _show_popup(self):
        """Show the popup flyout with group items using ListView."""
        if self._popup and self._popup.winfo_exists():
            self._hide_popup()
            return

        # Create popup window
        self._popup = Toplevel(self)
        self._popup.withdraw()  # Hide initially
        self._popup.overrideredirect(True)  # No window decorations

        # Style the popup
        popup_frame = Frame(self._popup, padding=4, show_border=True)
        popup_frame.pack(fill='both', expand=True)

        # Add header
        header = Label(popup_frame, text=self._text, font='label', accent='secondary')
        header.pack(fill='x', padx=8, pady=(4, 8))

        # Build items data for ListView
        items_data = []
        current_selection = self._variable.get() if self._variable else None
        for key in self._item_order:
            item = self._items[key]
            items_data.append({
                'id': key,
                'text': item.cget('text'),
                'icon': item.cget('icon'),
                'selected': key == current_selection,
            })

        # Create ListView for items
        listview = ListView(
            popup_frame,
            items=items_data,
            selection_mode='single',
            scrollbar_visibility='never',
            show_separator=False,
        )
        listview.pack(fill='both', expand=True)

        # Handle item click
        def on_item_click(event):
            record = event.data
            key = record.get('id')
            if key and key in self._items:
                # Set selection and fire event
                if self._variable:
                    self._variable.set(key)
                self._items[key].event_generate('<<ItemInvoked>>', data={'key': key})
                # Delay popup close to allow event chain to complete
                self.after(1, self._hide_popup)

        listview.on_item_click(on_item_click)

        # Bind to close on Escape
        self._popup.bind('<Escape>', lambda e: self._hide_popup(), add='+')

        # Bind to close on outside click
        self._root_click_id = self.winfo_toplevel().bind('<Button-1>', self._on_root_click, add='+')

        # Position and show after a brief delay to allow full layout
        self._popup.after(10, self._position_and_show_popup)

    def _position_and_show_popup(self):
        """Position and display the popup after layout is complete."""
        if not self._popup or not self._popup.winfo_exists():
            return

        # Force final layout calculation
        self._popup.update_idletasks()

        # Get container position
        btn_x = self._container.winfo_rootx()
        btn_y = self._container.winfo_rooty()
        btn_width = self._container.winfo_width()

        # Position popup to the right of container
        popup_x = btn_x + btn_width + 12
        popup_y = btn_y

        # Ensure popup stays on screen
        screen_width = self._popup.winfo_screenwidth()
        popup_width = self._popup.winfo_reqwidth()
        if popup_x + popup_width > screen_width:
            # Show to the left instead
            popup_x = btn_x - popup_width - 4

        self._popup.geometry(f'+{popup_x}+{popup_y}')
        self._popup.deiconify()

    def _on_root_click(self, event):
        """Handle click on root window - close popup if click is outside."""
        if not self._popup or not self._popup.winfo_exists():
            return

        # Get popup bounds
        popup_x = self._popup.winfo_rootx()
        popup_y = self._popup.winfo_rooty()
        popup_w = self._popup.winfo_width()
        popup_h = self._popup.winfo_height()

        # Check if click is outside popup
        if not (popup_x <= event.x_root <= popup_x + popup_w and
                popup_y <= event.y_root <= popup_y + popup_h):
            self._hide_popup()

    def _hide_popup(self):
        """Hide and destroy the popup."""
        # Unbind root click handler
        if hasattr(self, '_root_click_id') and self._root_click_id:
            try:
                self.winfo_toplevel().unbind('<Button-1>', self._root_click_id)
            except TclError:
                pass
            self._root_click_id = None

        if self._popup:
            try:
                self._popup.destroy()
            except TclError:
                pass
            self._popup = None

    # --- Public API ---

    def set_compact(self, compact: bool) -> None:
        """Set compact mode.

        In compact mode, only the icon is shown and clicking opens a popup
        with the group's items.

        Args:
            compact (bool): True for compact mode, False for full display.
        """
        if self._compact == compact:
            return

        self._compact = compact
        self._hide_popup()
        self._apply_layout()

        if compact:
            # Hide content in compact mode
            self._content_frame.pack_forget()
        else:
            # Restore content if expanded
            if self._is_expanded:
                self._content_frame.pack(fill='both', expand=True)

        self._update_selection_state()

    def expand(self) -> None:
        """Expand to show items (expanded mode only)."""
        if self._compact or self._is_expanded:
            return

        self._is_expanded = True
        self._content_frame.pack(fill='both', expand=True)
        self._chevron_label.configure(icon=self._get_chevron_icon())
        self.event_generate('<<GroupExpanding>>', data={'key': self._key})

    def collapse(self) -> None:
        """Collapse to hide items (expanded mode only)."""
        if self._compact or not self._is_expanded:
            return

        self._is_expanded = False
        self._content_frame.pack_forget()
        self._chevron_label.configure(icon=self._get_chevron_icon())
        self.event_generate('<<GroupCollapsed>>', data={'key': self._key})

    def toggle(self) -> None:
        """Toggle expansion state (expanded mode only)."""
        if self._compact:
            return

        if self._is_expanded:
            self.collapse()
        else:
            self.expand()

    # --- Internal: Item management (called by NavigationView) ---

    def _add_item(self, item: 'NavigationViewItem') -> None:
        """Add an item to this group (internal use by NavigationView)."""
        self._items[item.key] = item
        self._item_order.append(item.key)

    def _remove_item(self, key: str) -> None:
        """Remove an item from this group (internal use by NavigationView)."""
        if key in self._items:
            del self._items[key]
            self._item_order.remove(key)

    # --- Properties ---

    @property
    def key(self) -> str:
        """Get the group's unique key."""
        return self._key

    @property
    def content_frame(self) -> Frame:
        """Get the content frame for adding items."""
        return self._content_frame

    @property
    def is_expanded(self) -> bool:
        """Check if group is currently expanded."""
        return self._is_expanded

    @property
    def has_items(self) -> bool:
        """Check if this group has any items."""
        return len(self._items) > 0

    @property
    def items(self) -> list['NavigationViewItem']:
        """Get all items in order."""
        return [self._items[key] for key in self._item_order]

    @property
    def is_any_selected(self) -> bool:
        """Check if any child item is selected."""
        return self._is_any_child_selected()

    # --- Configuration Delegates ---

    @configure_delegate('text')
    def _delegate_text(self, value: str = None):
        """Configure the group text."""
        if value is None:
            return self._text
        self._text = value
        if self._text_label:
            self._text_label.configure(text=value)
        return None

    @configure_delegate('icon')
    def _delegate_icon(self, value: str | dict = None):
        """Configure the group icon."""
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
            self._icon_label.bind('<Button-1>', self._on_header_click, add='+')
            # Re-apply layout
            self._apply_layout()
        return None

    # --- Cleanup ---

    def destroy(self):
        """Clean up resources."""
        self._hide_popup()
        super().destroy()
