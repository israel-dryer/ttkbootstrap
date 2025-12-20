"""ListView widget for displaying large lists with virtual scrolling."""

from tkinter import TclError
from typing import Protocol, Any, Callable, Literal, runtime_checkable

from ttkbootstrap.widgets.primitives.frame import Frame
from ttkbootstrap.widgets.primitives.scrollbar import Scrollbar
from ttkbootstrap.widgets.composites.listitem import ListItem

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

    def unselect_record(self, record_id: Any) -> None:
        """Unselect a record.

        Args:
            record_id: Record identifier to unselect.
        """
        ...

    def unselect_all(self) -> None:
        """Unselect all records."""
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

    def set_data(self, data: list) -> 'MemoryDataSource':
        """Set the data and return self for chaining.

        Args:
            data: List of dicts or primitive values to convert to records.

        Returns:
            This instance for chaining.
        """
        self._data = []
        for i, item in enumerate(data or []):
            if isinstance(item, dict):
                if 'id' not in item:
                    item['id'] = i
                self._data.append(item)
            else:
                # Convert primitives to dict
                self._data.append({'id': i, 'value': str(item)})

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

    def unselect_record(self, record_id: Any) -> None:
        """Unselect a record.

        Args:
            record_id: Record identifier to unselect.
        """
        self._selected_ids.discard(record_id)

    def unselect_all(self) -> None:
        """Unselect all records."""
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
        self._data = [r for r in self._data if r.get('id') != record_id]
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
        self._data.append(data)
        return new_id

    def update_record(self, record_id: Any, data: dict) -> bool:
        """Update a record.

        Args:
            record_id: Record identifier to update.
            data: Record data to merge into the existing record.

        Returns:
            True if the record was updated.
        """
        for record in self._data:
            if record.get('id') == record_id:
                record.update(data)
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

        source_index = None
        for i, record in enumerate(self._data):
            if record.get('id') == record_id:
                source_index = i
                break

        if source_index is None:
            return False

        clamped_target = max(0, min(target_index, len(self._data) - 1))
        if source_index == clamped_target:
            return False

        record = self._data.pop(source_index)
        if clamped_target > source_index:
            clamped_target -= 1
        self._data.insert(clamped_target, record)
        return True


class ListView(Frame):
    """A virtual scrolling list widget for efficiently displaying large datasets.

    ListView uses virtual scrolling to render only visible items, allowing it to
    handle thousands of records efficiently. It supports multiple selection modes,
    item deletion, drag and drop, and custom styling.

    The widget works with either a simple list/dict data or a custom DataSource
    implementation for more complex scenarios (database, API, etc.).

    Virtual events:
        <<SelectionChanged>>: Fired when selection state changes.
        <<ItemDeleted>>: Fired when an item is deleted.
        <<ItemDeleteFailed>>: Fired when item deletion fails.
        <<ItemInserted>>: Fired when a new item is inserted.
        <<ItemUpdated>>: Fired when an item is updated.
        <<ItemClick>>: Fired when an item is clicked.
        <<ItemDragStart>>: Fired when a drag begins.
        <<ItemDragging>>: Fired when an item is being dragged.
        <<ItemDragEnd>>: Fired when a drag ends.

    Examples:
        >>> # Simple usage with a list
        >>> data = [
        ...     {'id': 1, 'title': 'Item 1', 'text': 'Description 1'},
        ...     {'id': 2, 'title': 'Item 2', 'text': 'Description 2'},
        ... ]
        >>> listview = ListView(
        ...     parent,
        ...     items=data,
        ...     selection_mode='multi',
        ...     show_selection_controls=True,
        ...     enable_deleting=True
        ... )
        >>> listview.pack(fill='both', expand=True)
        >>>
        >>> # Get selected items
        >>> selected_ids = listview.get_selected()
        >>>
        >>> # Listen for selection changes
        >>> listview.bind('<<SelectionChanged>>', on_selection_changed)

        >>> # Example with a custom data source
        >>> class DatabaseSource:
        ...     def total_count(self): return db.count()
        ...     def get_page_from_index(self, start, count): return db.query(start, count)
        ...     # ... implement other protocol methods
        >>>
        >>> listview = ListView(parent, datasource=DatabaseSource())
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
        show_separator: bool = True,
        enable_focus_state: bool = True,
        focus_color: str = None,
        selection_background: str = 'primary',
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
            enable_deleting: Show delete button on items.
            enable_dragging: Show drag handle on items.
            show_separator: Show separator line between items.
            enable_focus_state: Allow items to receive focus.
            focus_color: Color for the focus indicator.
            selection_background: Background color for selected items.
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
        self._enable_focus_state = enable_focus_state
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
        self._visible_rows = VISIBLE_ROWS
        self._row_height = ROW_HEIGHT
        self._page_size = VISIBLE_ROWS + OVERSCAN_ROWS
        self._rows: list[ListItem] = []
        self._focused_record_id = None
        self._drag_state: dict | None = None
        self._drag_indicator: Frame | None = None
        self._drag_scroll_counter = 0

        # Row factory
        self._row_factory = row_factory or self._default_row_factory

        # Create container frame for list items
        self._container = Frame(self, bootstyle='list')
        self._container.pack(side='left', fill='both', expand=True)

        # Create scrollbar
        self._scrollbar = Scrollbar(self, orient='vertical', command=self._on_scroll)
        self._scrollbar.pack(side='right', fill='y')

        # Create row pool
        self._ensure_row_pool(self._page_size)

        # Bind events
        self.bind('<Configure>', self._on_resize, add='+')
        self.bind('<MouseWheel>', self._on_mousewheel, add='+')

        # Bind ListItem events
        self._container.bind('<<ItemSelecting>>', self._on_item_selecting, add='+')
        self._container.bind('<<ItemDeleting>>', self._on_item_deleting, add='+')
        self._container.bind('<<ItemFocused>>', self._on_item_focused, add='+')
        self._container.bind('<<ItemClick>>', self._on_item_click, add='+')
        self._container.bind('<<ItemDragStart>>', self._on_item_drag_start, add='+')
        self._container.bind('<<ItemDragging>>', self._on_item_dragging, add='+')
        self._container.bind('<<ItemDragEnd>>', self._on_item_drag_end, add='+')

        # Initial update
        self.after(10, self._remeasure_and_relayout)

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
            row = self._row_factory(
                self._container,
                selection_mode=self._selection_mode,
                show_selection_controls=self._show_selection_controls,
                show_chevron=self._show_chevron,
                enable_deleting=self._enable_deleting,
                enable_dragging=self._enable_dragging,
                show_separator=self._show_separator,
                enable_focus_state=self._enable_focus_state,
                focus_color=self._focus_color,
                selection_background=self._selection_background
            )
            row.pack(fill='x')
            self._rows.append(row)

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
        """Update visible rows with current data."""
        self._clamp_indices()
        page_data = self._datasource.get_page_from_index(self._start_index, self._page_size)

        for i, row in enumerate(self._rows):
            if i < len(page_data):
                record = page_data[i].copy()
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
                record['item_index'] = self._start_index + i

                row.update_data(record)
            else:
                row.update_data(EMPTY)

        # Update scrollbar
        total = max(1, self._datasource.total_count())
        first = self._start_index / total
        last = min(1.0, (self._start_index + self._visible_rows) / total)
        self._scrollbar.set(first, last)

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
            step = self._visible_rows if unit == 'pages' else 1
            self._start_index += amount * step

        self._clamp_indices()
        self._update_rows()

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

    def _on_item_selecting(self, event):
        """Handle item selection event from `ListItem`.

        Args:
            event: Event with `data` for the item being selected.
        """
        record_id = event.data.get('id')
        if record_id is not None and record_id != '__empty__':
            if self._selection_mode == 'single':
                self._datasource.unselect_all()
                self._datasource.select_record(record_id)
            elif self._selection_mode == 'multi':
                if self._datasource.is_selected(record_id):
                    self._datasource.unselect_record(record_id)
                else:
                    self._datasource.select_record(record_id)

            self._update_rows()
            self.event_generate('<<SelectionChanged>>')

    def _on_item_deleting(self, event):
        """Handle item delete event from `ListItem`.

        Args:
            event: Event with `data` for the item being deleted.
        """
        record_id = event.data.get('id')
        if record_id is not None and record_id != '__empty__':
            try:
                self._datasource.delete_record(record_id)
                self._update_rows()
                self.event_generate('<<ItemDeleted>>')
            except Exception as e:
                self.event_generate('<<ItemDeleteFailed>>')

    def _on_item_focused(self, event):
        """Handle item focus event from `ListItem`.

        Args:
            event: Event with `data` for the item being focused.
        """
        record_id = event.data.get('id')
        if record_id is not None and record_id != '__empty__':
            self._focused_record_id = record_id
            self._update_rows()

    def _on_item_click(self, event):
        """Handle item click event from `ListItem`.

        Args:
            event: Event with `data` for the clicked item.
        """
        self.event_generate('<<ItemClick>>', data=event.data)

    def _on_item_drag_start(self, event):
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

    def _on_item_dragging(self, event):
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
        self.event_generate('<<ItemDragging>>', data=payload)

    def _on_item_drag_end(self, event):
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

        Example:
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
            self.event_generate('<<SelectionChanged>>')

    def clear_selection(self):
        """Clear all item selections.

        Deselects all items and generates a <<SelectionChanged>> event.
        """
        self._datasource.unselect_all()
        self._update_rows()
        self.event_generate('<<SelectionChanged>>')

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

        Example:
            >>> listview.insert_item({
            ...     'title': 'New Item',
            ...     'text': 'Description'
            ... })
        """
        self._datasource.create_record(data)
        self._update_rows()
        self.event_generate('<<ItemInserted>>')

    def update_item(self, record_id: Any, data: dict):
        """Update an existing item's data.

        Args:
            record_id: The ID of the record to update.
            data: Dictionary of fields to update. Will be merged with
                existing record data.

        Note:
            Generates a <<ItemUpdated>> event if the update succeeds.

        Example:
            >>> listview.update_item(42, {'title': 'Updated Title'})
        """
        if self._datasource.update_record(record_id, data):
            self._update_rows()
            self.event_generate('<<ItemUpdated>>')

    def delete_item(self, record_id: Any):
        """Delete an item from the list.

        Args:
            record_id: The ID of the record to delete.

        Note:
            Generates a <<ItemDeleted>> event after deletion.

        Example:
            >>> listview.delete_item(42)
        """
        self._datasource.delete_record(record_id)
        self._update_rows()
        self.event_generate('<<ItemDeleted>>')

    def get_datasource(self) -> DataSourceProtocol:
        """Get the underlying datasource.

        Returns:
            The DataSource instance managing the list's data.

        Example:
            >>> ds = listview.get_datasource()
            >>> count = ds.total_count()
        """
        return self._datasource

    def on_item_selected(self, callback):
        """Bind a callback to item selection events.

        Args:
            callback: Function to call when an item is selected. The callback
                receives an event object with a 'data' attribute containing
                the item's record.

        Example:
            >>> def on_select(event):
            ...     print(f"Selected: {event.data}")
            >>> listview.on_item_selected(on_select)
        """
        self._container.bind('<<ItemSelected>>', callback, add='+')
        self._container.bind('<<ItemSelecting>>', callback, add='+')
