"""ListView widget for displaying large lists with virtual scrolling."""

from tkinter import TclError
from typing import Protocol, Any, Callable, Literal, runtime_checkable

from ttkbootstrap.widgets.composites.listitem import ListItem
from ttkbootstrap.widgets.primitives.frame import Frame
from ttkbootstrap.widgets.primitives.scrollbar import Scrollbar
from ttkbootstrap.widgets.mixins import configure_delegate

# Constants
VISIBLE_ROWS = 20
ROW_HEIGHT = 40
OVERSCAN_ROWS = 2
EMPTY = {"__empty__": True, "id": "__empty__"}


@runtime_checkable
class DataSourceProtocol(Protocol):
    """Protocol for data sources used by ListView.

    Implementations provide paging, selection, and CRUD operations for records.
    """

    def total_count(self) -> int:
        """Return total number of records.

        Returns:
            Total record count.
        """
        ...

    def get_page_from_index(self, start: int, count: int) -> list[dict]:
        """Get a page of records starting at an index.

        Args:
            start: Zero-based index for the first record.
            count: Maximum number of records to return.

        Returns:
            List of record dictionaries.
        """
        ...

    def is_selected(self, record_id: Any) -> bool:
        """Check if a record is selected.

        Args:
            record_id: Record identifier to check.

        Returns:
            True if the record is selected.
        """
        ...

    def select_record(self, record_id: Any) -> None:
        """Select a record.

        Args:
            record_id: Record identifier to select.
        """
        ...

    def deselect_record(self, record_id: Any) -> None:
        """Deselect a record.

        Args:
            record_id: Record identifier to deselect.
        """
        ...

    def deselect_all(self) -> None:
        """Deselect all records."""
        ...

    def get_selected(self) -> list[Any]:
        """Get all selected record IDs.

        Returns:
            List of selected record identifiers.
        """
        ...

    def delete_record(self, record_id: Any) -> None:
        """Delete a record.

        Args:
            record_id: Record identifier to delete.
        """
        ...

    def create_record(self, data: dict) -> Any:
        """Create a new record and return its ID.

        Args:
            data: Record data to insert.

        Returns:
            The new record identifier.
        """
        ...

    def update_record(self, record_id: Any, data: dict) -> bool:
        """Update a record.

        Args:
            record_id: Record identifier to update.
            data: Record data to merge into the existing record.

        Returns:
            True if the record was updated.
        """
        ...

    def reload(self) -> None:
        """Reload data from the data source."""
        ...

    def move_record(self, record_id: Any, target_index: int) -> bool:
        """Move a record to a new position.

        Args:
            record_id: Record identifier to move.
            target_index: Zero-based index to move the record to.

        Returns:
            True if the record was moved.
        """
        ...


class MemoryDataSource:
    """In-memory data source implementation for ListView.

    Stores records in a list and tracks selected record IDs.
    """

    def __init__(self):
        """Initialize an empty data source."""
        self._data: list[dict] = []
        self._selected_ids: set = set()
        self._id_index: dict[Any, int] = {}  # Maps record ID to index for O(1) lookups

    def set_data(self, data: list) -> 'MemoryDataSource':
        """Set the data and return self for chaining.

        Args:
            data: List of dicts or primitive values to convert to records.

        Returns:
            This instance for chaining.
        """
        self._data = []
        self._id_index = {}
        for i, item in enumerate(data or []):
            if isinstance(item, dict):
                if 'id' not in item:
                    item['id'] = i
                self._data.append(item)
                self._id_index[item['id']] = i
            else:
                # Convert primitives to dict
                record = {'id': i, 'value': str(item)}
                self._data.append(record)
                self._id_index[i] = i

        return self

    def total_count(self) -> int:
        """Return total number of records.

        Returns:
            Total record count.
        """
        return len(self._data)

    def get_page_from_index(self, start: int, count: int) -> list[dict]:
        """Get a page of records starting at an index.

        Args:
            start: Zero-based index for the first record.
            count: Maximum number of records to return.

        Returns:
            List of record dictionaries.
        """
        end = min(start + count, len(self._data))
        return self._data[start:end]

    def is_selected(self, record_id: Any) -> bool:
        """Check if a record is selected.

        Args:
            record_id: Record identifier to check.

        Returns:
            True if the record is selected.
        """
        return record_id in self._selected_ids

    def select_record(self, record_id: Any) -> None:
        """Select a record.

        Args:
            record_id: Record identifier to select.
        """
        self._selected_ids.add(record_id)

    def deselect_record(self, record_id: Any) -> None:
        """Deselect a record.

        Args:
            record_id: Record identifier to deselect.
        """
        self._selected_ids.discard(record_id)

    def deselect_all(self) -> None:
        """Deselect all records."""
        self._selected_ids.clear()

    def get_selected(self) -> list[Any]:
        """Get all selected record IDs.

        Returns:
            List of selected record identifiers.
        """
        return list(self._selected_ids)

    def delete_record(self, record_id: Any) -> None:
        """Delete a record.

        Args:
            record_id: Record identifier to delete.
        """
        # Use index for O(1) lookup
        index = self._id_index.get(record_id)
        if index is not None:
            # Remove from data
            del self._data[index]
            # Remove from index
            del self._id_index[record_id]
            # Rebuild index for all records after the deleted one
            for i in range(index, len(self._data)):
                self._id_index[self._data[i]['id']] = i
        self._selected_ids.discard(record_id)

    def create_record(self, data: dict) -> Any:
        """Create a new record and return its ID.

        Args:
            data: Record data to insert.

        Returns:
            The new record identifier.
        """
        max_id = max((r.get('id', 0) for r in self._data), default=0)
        new_id = max_id + 1 if isinstance(max_id, int) else len(self._data)
        data['id'] = new_id
        new_index = len(self._data)
        self._data.append(data)
        self._id_index[new_id] = new_index
        return new_id

    def update_record(self, record_id: Any, data: dict) -> bool:
        """Update a record.

        Args:
            record_id: Record identifier to update.
            data: Record data to merge into the existing record.

        Returns:
            True if the record was updated.
        """
        # Use index for O(1) lookup
        index = self._id_index.get(record_id)
        if index is not None:
            self._data[index].update(data)
            return True
        return False

    def reload(self) -> None:
        """Reload data from source.

        This is a no-op for the in-memory data source.
        """
        pass

    def move_record(self, record_id: Any, target_index: int) -> bool:
        """Move a record to a new position.

        Args:
            record_id: Record identifier to move.
            target_index: Zero-based index to move the record to.

        Returns:
            True if the record was moved.
        """
        if not self._data:
            return False

        # Use index for O(1) lookup
        source_index = self._id_index.get(record_id)
        if source_index is None:
            return False

        clamped_target = max(0, min(target_index, len(self._data) - 1))
        if source_index == clamped_target:
            return False

        # Move the record
        record = self._data.pop(source_index)
        if clamped_target > source_index:
            clamped_target -= 1
        self._data.insert(clamped_target, record)

        # Rebuild index for affected range
        start = min(source_index, clamped_target)
        end = max(source_index, clamped_target) + 1
        for i in range(start, end):
            self._id_index[self._data[i]['id']] = i

        return True


class ListView(Frame):
    """A virtual scrolling list widget for efficiently displaying large datasets.

    ListView uses virtual scrolling to render only visible items, allowing it to
    handle thousands of records efficiently. It supports multiple selection modes,
    item deletion, drag and drop, and custom styling.

    The widget works with either a simple list/dict data or a custom DataSource
    implementation for more complex scenarios (database, API, etc.).

    Events:
        ``<<SelectionChange>>``: Fired when selection state changes.
        ``<<ItemDelete>>``: Fired when an item is deleted.
        ``<<ItemDeleteFail>>``: Fired when item deletion fails.
        ``<<ItemInsert>>``: Fired when a new item is inserted.
        ``<<ItemUpdate>>``: Fired when an item is updated.
        ``<<ItemClick>>``: Fired when an item is clicked.
        ``<<ItemDragStart>>``: Fired when a drag begins.
        ``<<ItemDrag>>``: Fired when an item is being dragged.
        ``<<ItemDragEnd>>``: Fired when a drag ends.
    """

    def __init__(
            self,
            master=None,
            items: list = None,
            datasource: DataSourceProtocol = None,
            row_factory: Callable = None,
            selection_mode: Literal['none', 'single', 'multi'] = 'none',
            show_selection_controls: bool = False,
            show_chevron: bool = False,
            enable_deleting: bool = False,
            enable_dragging: bool = False,
            alternating_row_color: str = 'background[+1]',
            alternating_row_mode: Literal['odd', 'even', 'none'] = 'even',
            show_separator: bool = True,
            show_scrollbar: bool = True,
            enable_focus_state: bool = True,
            enable_hover_state: bool = True,
            focus_color: str = None,
            selection_background: str = 'primary',
            select_by_click: bool = None,
            **kwargs
    ):
        """Initialize a ListView widget.

        Args:
            master: Parent widget.
            items: List of items or dicts to display (alternative to `datasource`).
            datasource: DataSource implementation for data access.
            row_factory: Callable that creates custom `ListItem` widgets.
            selection_mode: Selection mode (`none`, `single`, `multi`).
            show_selection_controls: Show checkboxes/radio buttons for selection.
            show_chevron: Show chevron indicators on items.
            enable_deleting: Show delete button on items; and allow deleting items.
            enable_dragging: Show drag handle on items; allow row dragging.
            alternating_row_mode: Whether and when to show alternating row colors.
            alternating_row_color: The alternating row color.
            show_separator: Show separator line between items.
            show_scrollbar: Show the vertical scrollbar. When False, scrolling relies
                on mousewheel only. Defaults to True.
            enable_focus_state: Allow items to receive focus.
            enable_hover_state: Show active state on hover.
            focus_color: Color for the focus indicator.
            selection_background: Background color for selected items.
            select_by_click: Whether clicking an item selects it. Defaults to True when
                selection_mode is 'single' or 'multi', False otherwise. Can be explicitly
                set to override the default behavior.
            **kwargs: Additional keyword arguments forwarded to `Frame`.
        """
        super().__init__(master, bootstyle='list', **kwargs)

        # Configuration
        self._selection_mode = selection_mode
        self._show_selection_controls = show_selection_controls
        self._show_chevron = show_chevron
        self._enable_deleting = enable_deleting
        self._enable_dragging = enable_dragging
        self._show_separator = show_separator
        self._show_scrollbar = show_scrollbar
        self._select_by_click = select_by_click
        self._enable_focus_state = enable_focus_state
        self._enable_hover_state = enable_hover_state
        self._alternating_row_mode = alternating_row_mode
        self._alternating_row_color = alternating_row_color
        self._focus_color = focus_color
        self._selection_background = selection_background


        # Data source
        if datasource:
            self._datasource = datasource
        elif items:
            self._datasource = MemoryDataSource().set_data(items)
        else:
            self._datasource = MemoryDataSource().set_data([])

        # Virtual scrolling state
        self._start_index = 0
        self._prev_start_index = 0
        self._visible_rows = VISIBLE_ROWS
        self._row_height = ROW_HEIGHT
        self._page_size = VISIBLE_ROWS + OVERSCAN_ROWS
        self._rows: list[ListItem] = []
        self._focused_record_id = None
        self._drag_state: dict | None = None
        self._drag_indicator: Frame | None = None
        self._drag_scroll_counter = 0
        self._mousewheel_bound_widgets: set = set()  # Track bound widgets to avoid cycles

        # Row factory
        self._row_factory = row_factory or self._default_row_factory

        # Create container frame for list items
        self._container = Frame(self, bootstyle='list')
        self._container.pack(side='left', fill='both', expand=True)

        # Create scrollbar
        self._scrollbar = Scrollbar(self, orient='vertical', command=self._on_scroll)
        if self._show_scrollbar:
            self._scrollbar.pack(side='right', fill='y')

        # Create row pool
        self._ensure_row_pool(self._page_size)

        # Bind events
        self.bind('<Configure>', self._on_resize, add='+')
        self.bind('<MouseWheel>', self._on_mousewheel, add='+')
        self._container.bind('<MouseWheel>', self._on_mousewheel, add='+')

        # Bind ListItem events
        self._container.bind('<<ItemSelecting>>', self._on_item_selecting, add='+')
        self._container.bind('<<ItemDeleting>>', self._on_item_deleting, add='+')
        self._container.bind('<<ItemFocus>>', self._on_item_focused, add='+')
        self._container.bind('<<ItemClick>>', self._on_item_click, add='+')
        self._container.bind('<<ItemDragStart>>', self._on_item_drag_start, add='+')
        self._container.bind('<<ItemDrag>>', self._on_item_dragging, add='+')
        self._container.bind('<<ItemDragEnd>>', self._on_item_drag_end, add='+')

        # Initial update
        self.after(10, self._remeasure_and_relayout)

    @configure_delegate('selection_mode')
    def _delegate_selection_mode(self, value=None):
        """Get or set the selection mode.

        Args:
            value: If provided, sets the selection mode to 'none', 'single', or 'multi'.
                If None, returns the current selection mode.

        Returns:
            Current selection mode when called without arguments.
        """
        if value is None:
            return self._selection_mode
        else:
            self._selection_mode = value
            # Recreate row pool to apply new selection mode
            self._ensure_row_pool(self._page_size)
            self._update_rows()
        return None

    @configure_delegate('show_scrollbar')
    def _delegate_show_scrollbar(self, value=None):
        """Get or set scrollbar visibility.

        Args:
            value: If provided, sets scrollbar visibility (True/False).
                If None, returns current visibility state.

        Returns:
            Current show_scrollbar value when called without arguments.
        """
        if value is None:
            return self._show_scrollbar
        else:
            old_value = self._show_scrollbar
            self._show_scrollbar = bool(value)
            if old_value != self._show_scrollbar:
                if self._show_scrollbar:
                    self._scrollbar.pack(side='right', fill='y')
                else:
                    self._scrollbar.pack_forget()
        return None

    @configure_delegate('alternating_row_mode')
    def _delegate_alternating_row_mode(self, value=None):
        """Get or set alternating row mode.

        Args:
            value: If provided, sets mode to 'odd', 'even', or 'none'.
                If None, returns the current mode.

        Returns:
            Current alternating_row_mode when called without arguments.
        """
        if value is None:
            return self._alternating_row_mode
        else:
            self._alternating_row_mode = value
            # Reapply surface colors to all rows
            for i, row in enumerate(self._rows):
                self._apply_widget_surface(row, i)
        return None

    @configure_delegate('alternating_row_color')
    def _delegate_alternating_row_color(self, value=None):
        """Get or set alternating row color.

        Args:
            value: If provided, sets the alternating row color.
                If None, returns the current color.

        Returns:
            Current alternating_row_color when called without arguments.
        """
        if value is None:
            return self._alternating_row_color
        else:
            self._alternating_row_color = value
            # Reapply surface colors to all rows
            for i, row in enumerate(self._rows):
                self._apply_widget_surface(row, i)
        return None

    @staticmethod
    def _default_row_factory(master, **kwargs):
        """Create a default `ListItem`.

        Args:
            master: Parent widget.
            **kwargs: Keyword arguments for `ListItem`.

        Returns:
            A new `ListItem` instance.
        """
        return ListItem(master, **kwargs)

    def _ensure_row_pool(self, needed: int):
        """Create/destroy `ListItem` widgets to match pool size.

        Args:
            needed: Desired number of row widgets.
        """
        while len(self._rows) < needed:
            # Build kwargs for row factory
            row_kwargs = dict(
                selection_mode=self._selection_mode,
                show_selection_controls=self._show_selection_controls,
                show_chevron=self._show_chevron,
                enable_deleting=self._enable_deleting,
                enable_dragging=self._enable_dragging,
                show_separator=self._show_separator,
                enable_focus_state=self._enable_focus_state,
                enable_hover_state=self._enable_hover_state,
                focus_color=self._focus_color,
                selection_background=self._selection_background
            )

            # Only pass select_by_click if explicitly set
            if self._select_by_click is not None:
                row_kwargs['select_by_click'] = self._select_by_click

            row = self._row_factory(self._container, **row_kwargs)
            row.pack(fill='x')
            self._rows.append(row)

            # Apply surface color once based on widget position
            widget_index = len(self._rows) - 1
            self._apply_widget_surface(row, widget_index)

        while len(self._rows) > needed:
            row = self._rows.pop()
            row.pack_forget()
            try:
                row.destroy()
            except TclError:
                pass

    def _clamp_indices(self):
        """Ensure `self._start_index` is within valid range."""
        total = self._datasource.total_count()
        max_start = max(0, total - self._visible_rows)
        self._start_index = max(0, min(self._start_index, max_start))

    def _update_rows(self):
        """Update visible rows with current data using row recycling for efficiency."""
        self._clamp_indices()

        # Calculate scroll distance to determine if we can use recycling
        scroll_distance = self._start_index - self._prev_start_index
        can_recycle = abs(scroll_distance) <= 3 and scroll_distance != 0

        if can_recycle:
            # Use row recycling for small scrolls
            self._recycle_rows(scroll_distance)
        else:
            # Full update for large scrolls or initial render
            self._full_update_rows()

        # Remember current position for next scroll
        self._prev_start_index = self._start_index

        # Update scrollbar
        total = max(1, self._datasource.total_count())
        first = self._start_index / total
        last = min(1.0, (self._start_index + self._visible_rows) / total)
        self._scrollbar.set(first, last)

    def _recycle_rows(self, scroll_distance: int):
        """Recycle rows by moving them from one end to the other.

        Args:
            scroll_distance: Positive for scrolling down, negative for scrolling up.
        """
        if scroll_distance > 0:
            # Scrolling down: move top rows to bottom
            for _ in range(scroll_distance):
                if not self._rows:
                    break

                # Remove top row
                top_row = self._rows.pop(0)

                # Calculate new data index
                data_index = self._start_index + len(self._rows)

                # Update data BEFORE moving widget to prevent focus tracking widget
                self._update_single_row(top_row, data_index)

                # Move to bottom
                top_row.pack_forget()
                top_row.pack(side='top', fill='x')
                self._rows.append(top_row)

        elif scroll_distance < 0:
            # Scrolling up: move bottom rows to top
            for _ in range(abs(scroll_distance)):
                if not self._rows:
                    break

                # Remove bottom row
                bottom_row = self._rows.pop()

                # Calculate new data index
                data_index = self._start_index

                # Update data BEFORE moving widget to prevent focus tracking widget
                self._update_single_row(bottom_row, data_index)

                # Move to top
                bottom_row.pack_forget()
                if self._rows:
                    bottom_row.pack(side='top', fill='x', before=self._rows[0])
                else:
                    bottom_row.pack(side='top', fill='x')
                self._rows.insert(0, bottom_row)

    def _full_update_rows(self):
        """Perform a full update of all visible rows."""
        page_data = self._datasource.get_page_from_index(self._start_index, self._page_size)

        for i, row in enumerate(self._rows):
            data_index = self._start_index + i
            if i < len(page_data):
                self._update_single_row(row, data_index, page_data[i])
            else:
                row.update_data(EMPTY)

    def _update_single_row(self, row: ListItem, data_index: int, record: dict = None):
        """Update a single row widget with data at the given index.

        Args:
            row: The ListItem widget to update.
            data_index: The data index to fetch and display.
            record: Optional pre-fetched record data. If None, will fetch from datasource.
        """
        if record is None:
            # Fetch the record from datasource
            page_data = self._datasource.get_page_from_index(data_index, 1)
            if not page_data:
                row.update_data(EMPTY)
                # Bind mousewheel after update to ensure all child widgets exist
                self._bind_mousewheel_recursive(row)
                return
            record = page_data[0]

        record = record.copy()
        record_id = record.get('id')

        # Add selection state
        if record_id is not None:
            try:
                record['selected'] = self._datasource.is_selected(record_id)
            except Exception:
                record['selected'] = False
            record['focused'] = (record_id == self._focused_record_id)
        else:
            record['selected'] = False
            record['focused'] = False

        # Add index
        record['item_index'] = data_index

        # Update the row
        row.update_data(record)

        # Bind mousewheel after update to ensure all child widgets exist
        self._bind_mousewheel_recursive(row)

    def _on_scroll(self, *args):
        """Handle scrollbar movement.

        Args:
            *args: Tkinter scrollbar arguments.
        """
        if args[0] == 'moveto':
            fraction = float(args[1])
            total = self._datasource.total_count()
            max_start = max(0, total - self._visible_rows)
            self._start_index = int(round(fraction * max_start))
        elif args[0] == 'scroll':
            amount = int(args[1])
            unit = args[2]
            # Use smaller step size for smoother scrolling
            step = max(1, self._visible_rows // 2) if unit == 'pages' else 1
            self._start_index += amount * step

        self._clamp_indices()
        self._update_rows()

    def _bind_mousewheel_recursive(self, widget):
        """Recursively bind mousewheel event to a widget and all its children.

        Only binds if the widget hasn't been bound already to avoid duplicate bindings.

        Args:
            widget: The widget to bind mousewheel event to.
        """
        # Use widget string representation as identifier
        widget_id = str(widget)

        # Only bind if we haven't already bound this widget
        if widget_id not in self._mousewheel_bound_widgets:
            widget.bind('<MouseWheel>', self._on_mousewheel, add='+')
            self._mousewheel_bound_widgets.add(widget_id)

        try:
            for child in widget.winfo_children():
                self._bind_mousewheel_recursive(child)
        except Exception:
            pass

    def _on_mousewheel(self, event):
        """Handle mouse wheel scrolling.

        Args:
            event: Tkinter mouse wheel event.
        """
        # Check if mouse is over this widget
        widget_under_mouse = self.winfo_containing(event.x_root, event.y_root)
        if widget_under_mouse is None:
            return

        # Check if the widget under mouse is a child of this ListView
        current = widget_under_mouse
        is_child = False
        while current is not None:
            if current == self:
                is_child = True
                break
            try:
                current = current.master
            except AttributeError:
                break

        if not is_child:
            return

        delta = -1 if event.delta > 0 else 1
        self._start_index += delta
        self._clamp_indices()
        self._update_rows()

    def _on_resize(self, event):
        """Handle widget resize and recalculate visible rows.

        Args:
            event: Tkinter configure event.
        """
        if event.widget == self:
            self.after_idle(self._remeasure_and_relayout)

    def _remeasure_and_relayout(self):
        """Measure row height, then recompute sizes and repaint."""
        if not self._rows:
            return

        # Measure actual widget height
        rh = self._rows[0].winfo_height()
        if rh <= 1:
            rh = self._rows[0].winfo_reqheight()

        if rh and rh != self._row_height:
            self._row_height = rh

        # Calculate how many rows fit
        container_height = self._container.winfo_height()
        if container_height > 0:
            visible = max(1, container_height // max(1, self._row_height))
            page_size = visible + OVERSCAN_ROWS

            if visible != self._visible_rows or page_size != self._page_size:
                self._visible_rows = visible
                self._page_size = page_size
                self._ensure_row_pool(self._page_size)

        self._clamp_indices()
        self._update_rows()

    def _on_item_selecting(self, event: Any):
        """Handle item selection event from `ListItem`.

        Args:
            event: Event with `data` for the item being selected.
        """
        record_id = event.data.get('id')
        if record_id is not None and record_id != '__empty__':
            if self._selection_mode == 'single':
                self._datasource.deselect_all()
                self._datasource.select_record(record_id)
            elif self._selection_mode == 'multi':
                if self._datasource.is_selected(record_id):
                    self._datasource.deselect_record(record_id)
                else:
                    self._datasource.select_record(record_id)

            self._update_rows()
            self.event_generate('<<SelectionChange>>')

    def _on_item_deleting(self, event: Any):
        """Handle item delete event from `ListItem`.

        Args:
            event: Event with `data` for the item being deleted.
        """
        record_id = event.data.get('id')
        if record_id is not None and record_id != '__empty__':
            try:
                self._datasource.delete_record(record_id)
                self._update_rows()
                self.event_generate('<<ItemDelete>>')
            except Exception as e:
                self.event_generate('<<ItemDeleteFail>>')

    def _on_item_focused(self, event: Any):
        """Handle item focus event from `ListItem`.

        Args:
            event: Event with `data` for the item being focused.
        """
        record_id = event.data.get('id')
        if record_id is not None and record_id != '__empty__':
            self._focused_record_id = record_id
            self._update_rows()

    def _on_item_click(self, event: Any):
        """Handle item click event from `ListItem`.

        Args:
            event: Event with `data` for the clicked item.
        """
        # Fetch fresh state from datasource to ensure accurate selection/focus state
        record_id = event.data.get('id')
        if record_id is not None and record_id != '__empty__':
            item_index = event.data.get('item_index')
            if item_index is not None:
                page_data = self._datasource.get_page_from_index(item_index, 1)
                if page_data:
                    record = page_data[0].copy()
                    record['selected'] = self._datasource.is_selected(record_id)
                    record['focused'] = (record_id == self._focused_record_id)
                    record['item_index'] = item_index
                    self.event_generate('<<ItemClick>>', data=record)
                    return

        # Fallback to original data if we can't fetch fresh state
        self.event_generate('<<ItemClick>>', data=event.data)

    def _apply_widget_surface(self, row: ListItem, widget_index: int) -> None:
        """Apply surface color to a row widget based on its position in the pool.

        This is called once when a widget is created. The color is based on the
        widget's position (not the data index), creating a stable alternating
        pattern during scrolling without needing to recalculate colors.

        Args:
            row: The ListItem widget to color.
            widget_index: The position of this widget in the row pool (0-based).
        """
        base_surface = getattr(self, "_surface_color", "background")
        if self._alternating_row_mode == 'none':
            surface = base_surface
        else:
            is_even = (widget_index % 2) == 0
            match = is_even if self._alternating_row_mode == 'even' else not is_even
            surface = self._alternating_row_color if match else base_surface

        if hasattr(row, "set_surface_color"):
            row.set_surface_color(surface)

    def _on_item_drag_start(self, event: Any):
        """Handle item drag start event from `ListItem`.

        Args:
            event: Event with `data` for the dragged item.
        """
        record_id = event.data.get('id')
        source_index = event.data.get('source_index')
        if record_id is None or record_id == '__empty__' or source_index is None:
            return

        self._drag_state = dict(
            record_id=record_id,
            source_index=source_index,
            target_index=source_index,
            record_data=dict(event.data),
        )
        self._drag_scroll_counter = 0
        self._show_drag_indicator()
        self._update_drag_indicator_position(source_index)
        self.event_generate('<<ItemDragStart>>', data=event.data)

    def _on_item_dragging(self, event: Any):
        """Handle item dragging event from `ListItem`.

        Args:
            event: Event with `data` for the dragged item.
        """
        if not self._drag_state:
            return

        y_current = event.data.get('y_current')
        target_index = self._get_drop_index(y_current)
        self._drag_state['target_index'] = target_index
        self._auto_scroll_for_drag(y_current)
        self._update_drag_indicator_position(target_index)
        payload = dict(self._drag_state.get('record_data', {}))
        payload.update(
            dict(
                source_index=self._drag_state.get('source_index'),
                target_index=target_index,
                y_current=y_current,
            )
        )
        self.event_generate('<<ItemDrag>>', data=payload)

    def _on_item_drag_end(self, event: Any):
        """Handle item drag end event from `ListItem`.

        Args:
            event: Event with `data` for the dragged item.
        """
        if not self._drag_state:
            return

        self._hide_drag_indicator()

        record_id = self._drag_state.get('record_id')
        target_index = self._drag_state.get('target_index')
        moved = self._move_record(record_id, target_index)
        if moved:
            self._update_rows()

        payload = dict(self._drag_state.get('record_data', {}))
        payload.update(
            dict(
                source_index=self._drag_state.get('source_index'),
                target_index=target_index,
                y_end=event.data.get('y_end'),
                y_start=event.data.get('y_start'),
            )
        )
        payload['target_index'] = target_index
        payload['moved'] = moved
        self.event_generate('<<ItemDragEnd>>', data=payload)
        self._drag_state = None

    def _get_drop_index(self, y_root: int | None) -> int:
        """Calculate the drop index for a drag operation.

        Args:
            y_root: Screen Y coordinate.

        Returns:
            Zero-based index for the drop position.
        """
        total = self._datasource.total_count()
        if total <= 0:
            return 0

        if y_root is None:
            return max(0, min(self._start_index, total - 1))

        container_top = self._container.winfo_rooty()
        container_height = self._container.winfo_height()
        if container_height <= 0:
            return max(0, min(self._start_index, total - 1))

        y_local = y_root - container_top
        y_local = max(0, min(y_local, container_height - 1))
        offset = int(y_local // max(1, self._row_height))
        target = self._start_index + offset
        return max(0, min(target, total - 1))

    def _auto_scroll_for_drag(self, y_root: int | None) -> None:
        """Auto-scroll while dragging near the list edges.

        Args:
            y_root: Screen Y coordinate.
        """
        if y_root is None:
            return

        container_top = self._container.winfo_rooty()
        container_height = self._container.winfo_height()
        if container_height <= 0:
            return

        scroll_zone_height = max(10, int(container_height * 0.2))
        container_bottom = container_top + container_height
        self._drag_scroll_counter += 1
        should_scroll = self._drag_scroll_counter % 8 == 0
        if should_scroll:
            if y_root < container_top + scroll_zone_height:
                self._start_index -= 1
            elif y_root > container_bottom - scroll_zone_height:
                self._start_index += 1
            else:
                return
        else:
            return

        self._clamp_indices()
        self._update_rows()

    def _move_record(self, record_id: Any, target_index: int | None) -> bool:
        """Move a record in the data source if supported.

        Args:
            record_id: Record identifier to move.
            target_index: Target index to move the record to.

        Returns:
            True if the record was moved.
        """
        if record_id is None or target_index is None:
            return False

        mover = getattr(self._datasource, 'move_record', None)
        if callable(mover):
            return bool(mover(record_id, target_index))

        # Fallback for simple in-memory lists
        try:
            total = self._datasource.total_count()
            all_records = self._datasource.get_page_from_index(0, total)
            source_index = None
            for i, record in enumerate(all_records):
                if record.get('id') == record_id:
                    source_index = i
                    break
            if source_index is None:
                return False
            clamped_target = max(0, min(target_index, len(all_records) - 1))
            if source_index == clamped_target:
                return False
            record = all_records.pop(source_index)
            if clamped_target > source_index:
                clamped_target -= 1
            all_records.insert(clamped_target, record)
            setter = getattr(self._datasource, 'set_data', None)
            if callable(setter):
                setter(all_records)
                return True
        except Exception:
            return False

        return False

    def _show_drag_indicator(self) -> None:
        """Create and show the drag drop indicator line."""
        if self._drag_indicator is None:
            self._drag_indicator = Frame(self._container, bootstyle=self._selection_background)

    def _update_drag_indicator_position(self, target_index: int) -> None:
        """Update the drag indicator to show drop location."""
        if self._drag_indicator is None:
            return

        try:
            visual_index = target_index - self._start_index
            if 0 <= visual_index < len(self._rows):
                y_pos = visual_index * max(1, self._row_height)
                self._drag_indicator.place(
                    x=0,
                    y=y_pos,
                    width=self._container.winfo_width(),
                    height=3,
                )
                self._drag_indicator.lift()
            else:
                self._drag_indicator.place_forget()
        except Exception:
            pass

    def _hide_drag_indicator(self) -> None:
        """Hide and destroy the drag indicator."""
        if self._drag_indicator is not None:
            try:
                self._drag_indicator.place_forget()
                self._drag_indicator.destroy()
            except Exception:
                pass
            self._drag_indicator = None

    # Public API

    def reload(self):
        """Reload data from the datasource and refresh the display.

        Calls the datasource's `reload()` method and updates all visible rows
        with the refreshed data. Useful when the underlying data has changed
        externally.
        """
        self._datasource.reload()
        self._update_rows()

    def get_selected(self) -> list:
        """Get list of selected record IDs.

        Returns:
            List of record IDs that are currently selected. Empty list if
            no items are selected.

        Examples:
            >>> selected = listview.get_selected()
            >>> print(f"Selected {len(selected)} items")
        """
        return self._datasource.get_selected()

    def select_all(self):
        """Select all items in the list.

        Only works when selection_mode is 'multi'. Generates a
        <<SelectionChanged>> event after completion.

        Note:
            For large datasets, this may be slow as it loads all records.
        """
        if self._selection_mode == 'multi':
            total = self._datasource.total_count()
            all_records = self._datasource.get_page_from_index(0, total)
            for record in all_records:
                record_id = record.get('id')
                if record_id:
                    self._datasource.select_record(record_id)
            self._update_rows()
            self.event_generate('<<SelectionChange>>')

    def clear_selection(self):
        """Clear all item selections.

        Deselects all items and generates a <<SelectionChange>> event.
        """
        self._datasource.deselect_all()
        self._update_rows()
        self.event_generate('<<SelectionChange>>')

    def scroll_to_top(self):
        """Scroll to the beginning of the list.

        Instantly scrolls to show the first item in the list.
        """
        self._start_index = 0
        self._update_rows()

    def scroll_to_bottom(self):
        """Scroll to the end of the list.

        Instantly scrolls to show the last items in the list.
        """
        total = self._datasource.total_count()
        self._start_index = max(0, total - self._visible_rows)
        self._update_rows()

    def insert_item(self, data: dict):
        """Insert a new item into the list.

        Args:
            data: Dictionary containing the item data. An 'id' will be
                auto-generated if not provided.

        Note:
            Generates a <<ItemInserted>> event after the item is added.

        Examples:
            >>> listview.insert_item({
            ...     'title': 'New Item',
            ...     'text': 'Description'
            ... })
        """
        self._datasource.create_record(data)
        self._update_rows()
        self.event_generate('<<ItemInsert>>')

    def update_item(self, record_id: Any, data: dict):
        """Update an existing item's data.

        Args:
            record_id: The ID of the record to update.
            data: Dictionary of fields to update. Will be merged with
                existing record data.

        Note:
            Generates a <<ItemUpdated>> event if the update succeeds.

        Examples:
            >>> listview.update_item(42, {'title': 'Updated Title'})
        """
        if self._datasource.update_record(record_id, data):
            self._update_rows()
            self.event_generate('<<ItemUpdate>>')

    def delete_item(self, record_id: Any):
        """Delete an item from the list.

        Args:
            record_id: The ID of the record to delete.

        Note:
            Generates a <<ItemDeleted>> event after deletion.

        Examples:
            >>> listview.delete_item(42)
        """
        self._datasource.delete_record(record_id)
        self._update_rows()
        self.event_generate('<<ItemDelete>>')

    def get_datasource(self) -> DataSourceProtocol:
        """Get the underlying datasource.

        Returns:
            The DataSource instance managing the list's data.

        Examples:
            >>> ds = listview.get_datasource()
            >>> count = ds.total_count()
        """
        return self._datasource

    # Event handler API

    def on_selection_change(self, callback: Callable):
        """Bind a callback to selection change events.

        Args:
            callback: Function to call when selection state changes.
                The callback receives an event object.

        Returns:
            Binding identifier that can be passed to off_selection_change().

        Examples:
            >>> def on_change(event):
            ...     selected = listview.get_selected()
            ...     print(f"Selection changed: {len(selected)} items")
            >>> listview.on_selection_change(on_change)
        """
        return self.bind('<<SelectionChange>>', callback, add='+')

    def off_selection_change(self, func_id: str):
        """Unbind a selection change event handler.

        Args:
            func_id: Binding identifier returned from on_selection_change().
        """
        self.unbind('<<SelectionChange>>', func_id)

    def on_item_delete(self, callback: Callable):
        """Bind a callback to item deletion events.

        Args:
            callback: Function to call when an item is deleted.
                The callback receives an event object.

        Returns:
            Binding identifier that can be passed to off_item_delete().

        Examples:
            >>> def on_delete(event):
            ...     print("Item deleted")
            >>> listview.on_item_delete(on_delete)
        """
        return self.bind('<<ItemDelete>>', callback, add='+')

    def off_item_delete(self, func_id: str):
        """Unbind an item deletion event handler.

        Args:
            func_id: Binding identifier returned from on_item_delete().
        """
        self.unbind('<<ItemDelete>>', func_id)

    def on_item_delete_fail(self, callback: Callable):
        """Bind a callback to failed item deletion events.

        Args:
            callback: Function to call when item deletion fails.
                The callback receives an event object.

        Returns:
            Binding identifier that can be passed to off_item_delete_fail().

        Examples:
            >>> def on_fail(event):
            ...     print("Delete failed")
            >>> listview.on_item_delete_fail(on_fail)
        """
        return self.bind('<<ItemDeleteFail>>', callback, add='+')

    def off_item_delete_fail(self, func_id: str):
        """Unbind a failed item deletion event handler.

        Args:
            func_id: Binding identifier returned from on_item_delete_fail().
        """
        self.unbind('<<ItemDeleteFail>>', func_id)

    def on_item_insert(self, callback: Callable):
        """Bind a callback to item insertion events.

        Args:
            callback: Function to call when an item is inserted.
                The callback receives an event object.

        Returns:
            Binding identifier that can be passed to off_item_insert().

        Examples:
            >>> def on_insert(event):
            ...     print("Item inserted")
            >>> listview.on_item_insert(on_insert)
        """
        return self.bind('<<ItemInsert>>', callback, add='+')

    def off_item_insert(self, func_id: str):
        """Unbind an item insertion event handler.

        Args:
            func_id: Binding identifier returned from on_item_insert().
        """
        self.unbind('<<ItemInsert>>', func_id)

    def on_item_update(self, callback: Callable):
        """Bind a callback to item update events.

        Args:
            callback: Function to call when an item is updated.
                The callback receives an event object.

        Returns:
            Binding identifier that can be passed to off_item_update().

        Examples:
            >>> def on_update(event):
            ...     print("Item updated")
            >>> listview.on_item_update(on_update)
        """
        return self.bind('<<ItemUpdate>>', callback, add='+')

    def off_item_update(self, func_id: str):
        """Unbind an item update event handler.

        Args:
            func_id: Binding identifier returned from on_item_update().
        """
        self.unbind('<<ItemUpdate>>', func_id)

    def on_item_click(self, callback: Callable):
        """Bind a callback to item click events.

        Args:
            callback: Function to call when an item is clicked.
                The callback receives an event object with a 'data'
                attribute containing the clicked item's record.

        Returns:
            Binding identifier that can be passed to off_item_click().

        Examples:
            >>> def on_click(event):
            ...     print(f"Clicked: {event.data}")
            >>> listview.on_item_click(on_click)
        """
        return self.bind('<<ItemClick>>', callback, add='+')

    def off_item_click(self, func_id: str):
        """Unbind an item click event handler.

        Args:
            func_id: Binding identifier returned from on_item_click().
        """
        self.unbind('<<ItemClick>>', func_id)

    def on_item_drag_start(self, callback: Callable):
        """Bind a callback to drag start events.

        Args:
            callback: Function to call when a drag operation begins.
                The callback receives an event object with a 'data'
                attribute containing the dragged item's record.

        Returns:
            Binding identifier that can be passed to off_item_drag_start().

        Examples:
            >>> def on_drag_start(event):
            ...     print(f"Drag started: {event.data}")
            >>> listview.on_item_drag_start(on_drag_start)
        """
        return self.bind('<<ItemDragStart>>', callback, add='+')

    def off_item_drag_start(self, func_id: str):
        """Unbind a drag start event handler.

        Args:
            func_id: Binding identifier returned from on_item_drag_start().
        """
        self.unbind('<<ItemDragStart>>', func_id)

    def on_item_drag(self, callback: Callable):
        """Bind a callback to item dragging events.

        Args:
            callback: Function to call during drag operations.
                The callback receives an event object with a 'data'
                attribute containing drag state including source_index,
                target_index, and current position.

        Returns:
            Binding identifier that can be passed to off_item_drag().

        Examples:
            >>> def on_drag(event):
            ...     data = event.data
            ...     print(f"Dragging from {data['source_index']} to {data['target_index']}")
            >>> listview.on_item_drag(on_drag)
        """
        return self.bind('<<ItemDrag>>', callback, add='+')

    def off_item_drag(self, func_id: str):
        """Unbind an item dragging event handler.

        Args:
            func_id: Binding identifier returned from on_item_drag().
        """
        self.unbind('<<ItemDrag>>', func_id)

    def on_item_drag_end(self, callback: Callable):
        """Bind a callback to drag end events.

        Args:
            callback: Function to call when a drag operation ends.
                The callback receives an event object with a 'data'
                attribute containing the final drag state including
                whether the item was moved.

        Returns:
            Binding identifier that can be passed to off_item_drag_end().

        Examples:
            >>> def on_drag_end(event):
            ...     if event.data['moved']:
            ...         print(f"Item moved to index {event.data['target_index']}")
            >>> listview.on_item_drag_end(on_drag_end)
        """
        return self.bind('<<ItemDragEnd>>', callback, add='+')

    def off_item_drag_end(self, func_id: str):
        """Unbind a drag end event handler.

        Args:
            func_id: Binding identifier returned from on_item_drag_end().
        """
        self.unbind('<<ItemDragEnd>>', func_id)
