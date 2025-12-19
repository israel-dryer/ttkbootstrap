"""ListView widget for displaying large lists efficiently using virtual scrolling."""

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
    """Protocol for data sources used by ListView."""

    def total_count(self) -> int:
        """Return total number of records."""
        ...

    def get_page_from_index(self, start: int, count: int) -> list[dict]:
        """Get a page of records starting at index."""
        ...

    def is_selected(self, record_id: Any) -> bool:
        """Check if record is selected."""
        ...

    def select_record(self, record_id: Any) -> None:
        """Select a record."""
        ...

    def unselect_record(self, record_id: Any) -> None:
        """Unselect a record."""
        ...

    def unselect_all(self) -> None:
        """Unselect all records."""
        ...

    def get_selected(self) -> list[Any]:
        """Get all selected record IDs."""
        ...

    def delete_record(self, record_id: Any) -> None:
        """Delete a record."""
        ...

    def create_record(self, data: dict) -> Any:
        """Create a new record, return its ID."""
        ...

    def update_record(self, record_id: Any, data: dict) -> bool:
        """Update a record, return success."""
        ...

    def reload(self) -> None:
        """Reload data from source."""
        ...


class MemoryDataSource:
    """Simple in-memory data source implementation for ListView."""

    def __init__(self):
        self._data: list[dict] = []
        self._selected_ids: set = set()

    def set_data(self, data: list) -> 'MemoryDataSource':
        """Set the data and return self for chaining."""
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
        """Return total number of records."""
        return len(self._data)

    def get_page_from_index(self, start: int, count: int) -> list[dict]:
        """Get a page of records starting at index."""
        end = min(start + count, len(self._data))
        return self._data[start:end]

    def is_selected(self, record_id: Any) -> bool:
        """Check if record is selected."""
        return record_id in self._selected_ids

    def select_record(self, record_id: Any) -> None:
        """Select a record."""
        self._selected_ids.add(record_id)

    def unselect_record(self, record_id: Any) -> None:
        """Unselect a record."""
        self._selected_ids.discard(record_id)

    def unselect_all(self) -> None:
        """Unselect all records."""
        self._selected_ids.clear()

    def get_selected(self) -> list[Any]:
        """Get all selected record IDs."""
        return list(self._selected_ids)

    def delete_record(self, record_id: Any) -> None:
        """Delete a record."""
        self._data = [r for r in self._data if r.get('id') != record_id]
        self._selected_ids.discard(record_id)

    def create_record(self, data: dict) -> Any:
        """Create a new record, return its ID."""
        max_id = max((r.get('id', 0) for r in self._data), default=0)
        new_id = max_id + 1 if isinstance(max_id, int) else len(self._data)
        data['id'] = new_id
        self._data.append(data)
        return new_id

    def update_record(self, record_id: Any, data: dict) -> bool:
        """Update a record, return success."""
        for record in self._data:
            if record.get('id') == record_id:
                record.update(data)
                return True
        return False

    def reload(self) -> None:
        """Reload data from source (no-op for memory source)."""
        pass


class ListView(Frame):
    """
    A virtual scrolling list widget that efficiently displays large datasets
    by only rendering visible items.

    Example:
        data = [
            {'id': 1, 'title': 'Item 1', 'text': 'Description 1'},
            {'id': 2, 'title': 'Item 2', 'text': 'Description 2'},
        ]

        listview = ListView(
            parent,
            items=data,
            selection_mode='multi',
            show_selection_controls=True
        )
        listview.pack(fill='both', expand=True)
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
        """
        Initialize a ListView widget.

        Args:
            master: Parent widget
            items: List of items or dicts to display (alternative to datasource)
            datasource: DataSource implementation for data access
            row_factory: Callable to create custom ListItem widgets
            selection_mode: Selection mode ('none', 'single', 'multi')
            show_selection_controls: Show checkboxes/radio buttons for selection
            show_chevron: Show chevron indicators on items
            enable_deleting: Show delete button on items
            enable_dragging: Show drag handle on items
            show_separator: Show separator line between items
            enable_focus_state: Allow items to receive focus
            focus_color: Color for focus indicator
            selection_background: Background color for selected items
            **kwargs: Additional keyword arguments for Frame
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
        self.bind_all('<MouseWheel>', self._on_mousewheel, add='+')

        # Bind ListItem events
        self._container.bind('<<ItemSelecting>>', self._on_item_selecting, add='+')
        self._container.bind('<<ItemDeleting>>', self._on_item_deleting, add='+')
        self._container.bind('<<ItemFocused>>', self._on_item_focused, add='+')
        self._container.bind('<<ItemClick>>', self._on_item_click, add='+')

        # Initial update
        self.after(10, self._remeasure_and_relayout)

    @staticmethod
    def _default_row_factory(master, **kwargs):
        """Default factory creates a ListItem."""
        return ListItem(master, **kwargs)

    def _ensure_row_pool(self, needed: int):
        """Create/destroy ListItem widgets to match needed size."""
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
        """Ensure start_index is within valid range."""
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
        """Handle scrollbar movement."""
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
        """Handle mouse wheel scrolling."""
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
        """Handle widget resize - recalculate visible rows."""
        if event.widget == self:
            self.after_idle(self._remeasure_and_relayout)

    def _remeasure_and_relayout(self):
        """Measure real row height, then recompute visible/page sizes and repaint."""
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
        """Handle item selection event from ListItem."""
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
        """Handle item delete event from ListItem."""
        record_id = event.data.get('id')
        if record_id is not None and record_id != '__empty__':
            try:
                self._datasource.delete_record(record_id)
                self._update_rows()
                self.event_generate('<<ItemDeleted>>')
            except Exception as e:
                self.event_generate('<<ItemDeleteFailed>>')

    def _on_item_focused(self, event):
        """Handle item focus event from ListItem."""
        record_id = event.data.get('id')
        if record_id is not None and record_id != '__empty__':
            self._focused_record_id = record_id
            self._update_rows()

    def _on_item_click(self, event):
        """Handle item click event from ListItem."""
        self.event_generate('<<ItemClick>>', data=event.data)

    # Public API

    def reload(self):
        """Reload data from datasource."""
        self._datasource.reload()
        self._update_rows()

    def get_selected(self) -> list:
        """Get list of selected record IDs."""
        return self._datasource.get_selected()

    def select_all(self):
        """Select all items (only in multi mode)."""
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
        """Clear all selections."""
        self._datasource.unselect_all()
        self._update_rows()
        self.event_generate('<<SelectionChanged>>')

    def scroll_to_top(self):
        """Scroll to the beginning of the list."""
        self._start_index = 0
        self._update_rows()

    def scroll_to_bottom(self):
        """Scroll to the end of the list."""
        total = self._datasource.total_count()
        self._start_index = max(0, total - self._visible_rows)
        self._update_rows()

    def insert_item(self, data: dict):
        """Insert a new item."""
        self._datasource.create_record(data)
        self._update_rows()
        self.event_generate('<<ItemInserted>>')

    def update_item(self, record_id: Any, data: dict):
        """Update an existing item."""
        if self._datasource.update_record(record_id, data):
            self._update_rows()
            self.event_generate('<<ItemUpdated>>')

    def delete_item(self, record_id: Any):
        """Delete an item by ID."""
        self._datasource.delete_record(record_id)
        self._update_rows()
        self.event_generate('<<ItemDeleted>>')

    def get_datasource(self) -> DataSourceProtocol:
        """Get the underlying datasource."""
        return self._datasource

    def on_item_selected(self, callback):
        self._container.bind('<<ItemSelected>>', callback, add='+')
        self._container.bind('<<ItemSelecting>>', callback, add='+')