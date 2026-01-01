"""NavigationViewGroup widget for grouping navigation items."""

from __future__ import annotations

from tkinter import TclError, Toplevel, Variable
from typing import Any, TYPE_CHECKING

from ttkbootstrap.widgets.primitives.frame import Frame
from ttkbootstrap.widgets.primitives.label import Label
from ttkbootstrap.widgets.composites.expander import Expander
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

        super().__init__(master, **kwargs)

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
        self._expander: Expander | None = None
        self._content_frame: Frame | None = None
        self._compact_button: CompositeFrame | None = None
        self._popup: Toplevel | None = None

        # Track selection variable for highlighting
        self._trace_id: str | None = None
        if variable:
            self._trace_id = variable.trace_add('write', self._on_selection_changed)

        # Build internal structure
        self._build_widget()

    def _build_widget(self):
        """Build the internal widget structure."""
        # Create expander for expanded mode
        self._expander = Expander(
            self,
            title=self._text,
            icon=self._icon,
            expanded=self._is_expanded,
            collapsible=True,
            highlight=True,  # Shows selected when expanded
            padding=0,
        )
        self._expander.pack(fill='x')

        # Get content frame for items
        self._content_frame = self._expander.add()

        # Bind expander events
        self._expander.on_toggle(self._on_expander_toggle)

        # Create compact mode button (hidden initially)
        self._compact_button = CompositeFrame(
            self,
            padding=8,
            takefocus=True,
        )
        # Don't pack yet - only shown in compact mode

        # Icon for compact button
        if self._icon:
            self._compact_icon = Label(
                self._compact_button,
                icon=self._icon,
                icon_only=True,
                takefocus=False,
            )
            self._compact_button.register_composite(self._compact_icon)
            self._compact_icon.pack(expand=True)
            # Bind click on icon too
            self._compact_icon.bind('<Button-1>', self._on_compact_click, add='+')

        # Bind compact button click
        self._compact_button.bind('<Button-1>', self._on_compact_click, add='+')
        self._compact_button.bind('<Return>', self._on_compact_click, add='+')
        self._compact_button.bind('<space>', self._on_compact_click, add='+')

    def _on_expander_toggle(self, event):
        """Forward expander toggle events."""
        expanded = event.data.get('expanded', False)
        self._is_expanded = expanded
        if expanded:
            self.event_generate('<<GroupExpanding>>', data={'key': self._key})
        else:
            self.event_generate('<<GroupCollapsed>>', data={'key': self._key})

    def _on_selection_changed(self, *args):
        """Handle selection variable changes to update group highlight."""
        self._update_selection_state()

    def _update_selection_state(self):
        """Update visual state based on whether any child is selected."""
        is_any_selected = self._is_any_child_selected()

        # In expanded mode, update expander highlight
        if not self._compact:
            # The expander's highlight is tied to its expanded state
            # For groups, we want highlight when any child is selected OR when expanded
            # This is handled by the selection state on items
            pass

        # In compact mode, update the button's selected state
        if self._compact and self._compact_button:
            self._compact_button.set_selected(is_any_selected)

    def _is_any_child_selected(self) -> bool:
        """Check if any child item is currently selected."""
        if not self._variable:
            return False
        current = self._variable.get()
        return current in self._items

    def _on_compact_click(self, event=None):
        """Handle click in compact mode - show popup."""
        self._compact_button.focus_set()
        self._show_popup()

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
        header = Label(popup_frame, text=self._text, font='label', color='secondary')
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

        # Position popup to the right of the compact button
        self._popup.update_idletasks()

        # Get button position
        btn_x = self._compact_button.winfo_rootx()
        btn_y = self._compact_button.winfo_rooty()
        btn_width = self._compact_button.winfo_width()

        # Position popup to the right of button
        popup_x = btn_x + btn_width + 4
        popup_y = btn_y

        # Ensure popup stays on screen
        screen_width = self._popup.winfo_screenwidth()
        popup_width = self._popup.winfo_reqwidth()
        if popup_x + popup_width > screen_width:
            # Show to the left instead
            popup_x = btn_x - popup_width - 4

        self._popup.geometry(f'+{popup_x}+{popup_y}')
        self._popup.deiconify()

        # Bind to close on click outside or focus loss
        self._popup.bind('<FocusOut>', self._on_popup_focus_out, add='+')
        self._popup.bind('<Escape>', lambda e: self._hide_popup(), add='+')

    def _setup_popup_close_bindings(self):
        """Set up bindings to close popup when clicking elsewhere."""
        if not self._popup or not self._popup.winfo_exists():
            return

        def check_click(event):
            if not self._popup or not self._popup.winfo_exists():
                return
            # Check if click was outside popup
            try:
                x, y = event.x_root, event.y_root
                px = self._popup.winfo_rootx()
                py = self._popup.winfo_rooty()
                pw = self._popup.winfo_width()
                ph = self._popup.winfo_height()

                if not (px <= x <= px + pw and py <= y <= py + ph):
                    self._hide_popup()
            except TclError:
                pass

        # Bind to root window
        root = self.winfo_toplevel()
        self._click_bind_id = root.bind('<Button-1>', check_click, add='+')

    def _on_popup_focus_out(self, event):
        """Handle popup losing focus."""
        # Delay to allow click events to process
        if self._popup and self._popup.winfo_exists():
            self._popup.after(100, self._check_popup_focus)

    def _check_popup_focus(self):
        """Check if popup should be closed."""
        if not self._popup or not self._popup.winfo_exists():
            return
        try:
            focus = self._popup.focus_get()
            if focus is None or not str(focus).startswith(str(self._popup)):
                self._hide_popup()
        except TclError:
            pass

    def _hide_popup(self):
        """Hide and destroy the popup."""
        if self._popup:
            try:
                # Remove click binding from root
                root = self.winfo_toplevel()
                if hasattr(self, '_click_bind_id'):
                    root.unbind('<Button-1>', self._click_bind_id)
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

        if compact:
            # Hide expander, show compact button
            self._expander.pack_forget()
            self._compact_button.pack(fill='x')
            self._update_selection_state()
        else:
            # Hide compact button, show expander
            self._hide_popup()
            self._compact_button.pack_forget()
            self._expander.pack(fill='x')

    def expand(self) -> None:
        """Expand to show items (expanded mode only)."""
        if not self._compact:
            self._expander.expand()

    def collapse(self) -> None:
        """Collapse to hide items (expanded mode only)."""
        if not self._compact:
            self._expander.collapse()

    def toggle(self) -> None:
        """Toggle expansion state (expanded mode only)."""
        if not self._compact:
            self._expander.toggle()

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
        return self._expander.cget('expanded')

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
        if self._expander:
            self._expander.configure(title=value)
        return None

    @configure_delegate('icon')
    def _delegate_icon(self, value: str | dict = None):
        """Configure the group icon."""
        if value is None:
            return self._icon
        self._icon = value
        if self._expander:
            self._expander.configure(icon=value)
        if hasattr(self, '_compact_icon'):
            self._compact_icon.configure(icon=value)
        return None

    # --- Cleanup ---

    def destroy(self):
        """Clean up resources."""
        self._hide_popup()
        if self._variable and self._trace_id:
            try:
                self._variable.trace_remove('write', self._trace_id)
            except Exception:
                pass
        super().destroy()