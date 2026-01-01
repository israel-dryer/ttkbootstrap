"""TableView widget backed by an in-memory SQLite datasource.

The datasource performs filtering, sorting, and pagination while the widget
renders the current page in a Treeview with optional grouping, striping, and
context menus.
"""

from __future__ import annotations

import logging
from collections import OrderedDict
from tkinter import font as tkfont

from typing_extensions import Literal

from ttkbootstrap.widgets.types import Master

from ttkbootstrap_icons_bs import BootstrapIcon
from ttkbootstrap.style.style import get_style
from ttkbootstrap.datasource.sqlite_source import SqliteDataSource
from ttkbootstrap.widgets.primitives.button import Button
from ttkbootstrap.widgets.composites.contextmenu import ContextMenu
from ttkbootstrap.widgets.composites.dropdownbutton import DropdownButton
from ttkbootstrap.widgets.primitives.entry import Entry
from ttkbootstrap.widgets.primitives.frame import Frame
from ttkbootstrap.widgets.primitives.label import Label
from ttkbootstrap.widgets.primitives.scrollbar import Scrollbar
from ttkbootstrap.widgets.primitives.selectbox import SelectBox
from ttkbootstrap.widgets.primitives.separator import Separator
from ttkbootstrap.widgets.composites.textentry import TextEntry
from ttkbootstrap.widgets.primitives.treeview import TreeView
from ttkbootstrap.core.localization import MessageCatalog

from .types import (
    EditingOptions,
    SelectionOptions,
    ExportingOptions,
    PagingOptions,
    RowAlternationOptions,
    FilteringOptions,
    SearchOptions,
    parse_selection_mode as _parse_selection_mode,
    normalize_row_alternation_options as _normalize_row_alternation_options,
    normalize_selection_options as _normalize_selection_options,
    normalize_filtering_options as _normalize_filtering_options,
    normalize_editing_options as _normalize_editing_options,
    normalize_exporting_options as _normalize_exporting_options,
    normalize_paging_options as _normalize_paging_options,
    normalize_searchbar_options as _normalize_searchbar_options,
)

logger = logging.getLogger(__name__)

_TABLE_SEARCH_MODE_OPTIONS = [
    ("table.search_mode_equals", "EQUALS"),
    ("table.search_mode_contains", "CONTAINS"),
    ("table.search_mode_starts_with", "STARTS WITH"),
    ("table.search_mode_ends_with", "ENDS WITH"),
    ("table.search_mode_sql", "SQL"),
]


class TableView(Frame):
    """TableView backed by an in-memory SqliteDataSource.

    Provides sortable headers, filtering/search, pagination or virtual scrolling,
    optional grouping, column striping, and configurable exporting/editing.

    !!! note "Events"
        - ``<<SelectionChange>>``: Fired when row selection changes. ``event.data = {'records': list[dict], 'iids': list[str]}``
        - ``<<RowClick>>``: Fired on single row click. ``event.data = {'record': dict, 'iid': str}``
        - ``<<RowDoubleClick>>``: Fired on row double-click. ``event.data = {'record': dict, 'iid': str}``
        - ``<<RowRightClick>>``: Fired on row right-click. ``event.data = {'record': dict, 'iid': str}``
        - ``<<RowInsert>>``: Fired when rows are inserted. ``event.data = {'records': list[dict]}``
        - ``<<RowUpdate>>``: Fired when rows are updated. ``event.data = {'records': list[dict]}``
        - ``<<RowDelete>>``: Fired when rows are deleted. ``event.data = {'records': list[dict]}``
        - ``<<RowMove>>``: Fired when rows are moved/reordered. ``event.data = {'records': list[dict]}``
    """

    def __init__(
            self,
            master: Master = None,
            columns: list[str | dict] | None = None,
            rows: list | None = None,
            datasource: SqliteDataSource | None = None,
            editing: EditingOptions | dict | None = None,
            paging: PagingOptions | dict | None = None,
            exporting: ExportingOptions | dict | None = None,
            filtering: FilteringOptions | dict | None = None,
            selection: SelectionOptions | dict | None = None,
            search: SearchOptions | dict | None = None,
            sorting: Literal['single', 'multiple', 'none'] = 'single',
            row_alternation: RowAlternationOptions | dict | None = None,
            allow_grouping: bool = False,
            show_table_status: bool = True,
            show_column_chooser: bool = False,
            context_menus: Literal["none", "headers", "rows", "all"] = "all",
            column_min_width: int = 40,
            column_auto_width: bool = False,
            **kwargs,
    ):
        """
        Create a TableView backed by an in-memory SqliteDataSource.

        Args:
            master: Parent widget.
            columns: Column definitions (list of strings or dicts with keys like "text", "key", "width", "minwidth").
            rows: Initial data to load (list of dicts or row-like sequences).
            datasource: Custom SqliteDataSource; if omitted, an in-memory source is created.
            editing: EditingOptions or dict to enable adding/updating/deleting and form settings.
            paging: PagingOptions or dict (mode 'standard'|'virtual', page_size, page_index, cache_size, xscroll, yscroll).
            exporting: ExportingOptions or dict (enabled, allow_export_selected, export_all_mode 'page'|'all', formats).
            filtering: FilteringOptions or dict (enabled, header_menu_filtering, row_menu_filtering).
            selection: SelectionOptions or dict (mode 'single'|'multiple'|'none', allow_select_all).
            search: SearchOptions or dict (enabled, mode 'standard'|'advanced', event 'input'|'enter'; default 'enter').
            row_alternation: RowAlternationOptions (enabled flag, color token for striping; disabled when grouped).
            allow_grouping: Allow grouping rows via header context menu.
            sorting: Sorting mode ('single', 'multiple', or 'none' to disable sorting).
            show_table_status: Show filter/sort/group status labels and pager.
            show_column_chooser: Show column chooser button for toggling column visibility.
            context_menus: "none" | "headers" | "rows" | "all" to enable region context menus.
            column_min_width: Global minimum width for columns (overridden by per-column minwidth; default 40).
            column_auto_width: Automatically size columns to widest visible text on each page.
            **kwargs: Any: Passed through to Frame.
        """
        super().__init__(master, **kwargs)

        # configuration
        self._editing = _normalize_editing_options(editing)
        self._paging = _normalize_paging_options(paging)
        self._exporting = _normalize_exporting_options(exporting)
        self._filtering = _normalize_filtering_options(filtering)
        self._selection = _normalize_selection_options(selection)
        self._searchbar = _normalize_searchbar_options(search)
        self._search_mode_map: dict[str, str] = {}
        self._sorting = sorting
        self._show_table_status = show_table_status
        self._show_column_chooser = show_column_chooser
        self._row_alternation = _normalize_row_alternation_options(row_alternation)
        self._allow_grouping = allow_grouping
        self._context_menus = (context_menus or "all").lower()
        self._column_min_width = max(0, column_min_width)
        self._column_auto_width = column_auto_width
        self._datasource = datasource or SqliteDataSource(":memory:", page_size=self._paging['page_size'])

        self._page_cache: OrderedDict[int, list[dict]] = OrderedDict()
        self._column_defs = columns or []
        self._column_keys: list[str] = []
        self._heading_texts: list[str] = []
        self._sort_state: dict[str, bool] = {}  # key -> ascending
        self._current_page = self._paging['page_index']
        self._loading_next = False
        self._heading_fg: str | None = None
        self._icon_sort_up = None
        self._icon_sort_down = None
        self._column_anchors: list[str] = []
        self._column_filters: dict[str, list] = {}  # key -> list of allowed values
        self._column_types: dict[str, str] = {}
        self._alignment_sample: list[dict] | None = None
        self._row_map: dict[str, dict] = {}
        self._row_menu: ContextMenu | None = None
        self._display_columns: list[int] = []
        self._header_menu: ContextMenu | None = None
        self._header_menu_col: int | None = None
        self._cached_total_count: int | None = None
        self._group_by_key: str | None = None
        self._group_parents: dict[str | None, str] = {}
        self._hidden_rows: dict[str, tuple[str, int]] = {}

        self._resolve_column_keys()

        seeded_records: list[dict] | None = None
        if rows:
            try:
                if self._column_keys:
                    # Avoid per-row dict conversion when we already know the column order
                    self._datasource.set_data(rows, column_keys=self._column_keys)
                    seeded_records = None
                else:
                    seeded_records = self._to_records(rows)
                    self._datasource.set_data(seeded_records)
            except Exception:
                # Last-resort fallback to dict conversion if direct load fails
                seeded_records = self._to_records(rows)
                try:
                    self._datasource.set_data(seeded_records)
                except Exception:
                    seeded_records = []

        self._ensure_column_metadata(seeded_records)

        # UI
        self._build_toolbar()
        self._build_tree()
        if self._show_table_status or not self._paging['mode'] == 'virtual':
            self._build_footer()

        # Initial load
        self._load_page(0)

    # ------------------------------------------------------------------ Public API
    def set_data(self, rows: list) -> None:
        """Replace data in the datasource and refresh the grid."""
        if self._column_keys:
            self._datasource.set_data(rows, column_keys=self._column_keys)
            seeded_records = None
        else:
            seeded_records = self._to_records(rows)
            self._datasource.set_data(seeded_records)
        self._ensure_column_metadata(seeded_records)
        self._clear_cache()
        self._load_page(0)

    # ------------------------------------------------------------------ Public event API
    def on_selection_changed(self, callback) -> str:
        """Bind to ``<<SelectionChange>>``. Callback receives ``event.data = {'records': list[dict], 'iids': list[str]}``."""
        return self.bind("<<SelectionChange>>", callback, add=True)

    def off_selection_changed(self, bind_id: str | None = None) -> None:
        """Unbind from ``<<SelectionChange>>``."""
        self.unbind("<<SelectionChange>>", bind_id)

    def on_row_click(self, callback) -> str:
        """Bind to ``<<RowClick>>``. Callback receives ``event.data = {'record': dict, 'iid': str}``."""
        return self.bind("<<RowClick>>", callback, add=True)

    def off_row_click(self, bind_id: str | None = None) -> None:
        """Unbind from ``<<RowClick>>``."""
        self.unbind("<<RowClick>>", bind_id)

    def on_row_double_click(self, callback) -> str:
        """Bind to ``<<RowDoubleClick>>``. Callback receives ``event.data = {'record': dict, 'iid': str}``."""
        return self.bind("<<RowDoubleClick>>", callback, add=True)

    def off_row_double_click(self, bind_id: str | None = None) -> None:
        """Unbind from ``<<RowDoubleClick>>``."""
        self.unbind("<<RowDoubleClick>>", bind_id)

    def on_row_right_click(self, callback) -> str:
        """Bind to ``<<RowRightClick>>``. Callback receives ``event.data = {'record': dict, 'iid': str}``."""
        return self.bind("<<RowRightClick>>", callback, add=True)

    def off_row_right_click(self, bind_id: str | None = None) -> None:
        """Unbind from ``<<RowRightClick>>``."""
        self.unbind("<<RowRightClick>>", bind_id)

    def on_row_deleted(self, callback) -> str:
        """Bind to ``<<RowDelete>>``. Callback receives ``event.data = {'records': list[dict]}``."""
        return self.bind("<<RowDelete>>", callback, add=True)

    def off_row_deleted(self, bind_id: str | None = None) -> None:
        """Unbind from ``<<RowDelete>>``."""
        self.unbind("<<RowDelete>>", bind_id)

    def on_row_inserted(self, callback) -> str:
        """Bind to ``<<RowInsert>>``. Callback receives ``event.data = {'records': list[dict]}``."""
        return self.bind("<<RowInsert>>", callback, add=True)

    def off_row_inserted(self, bind_id: str | None = None) -> None:
        """Unbind from ``<<RowInsert>>``."""
        self.unbind("<<RowInsert>>", bind_id)

    def on_row_updated(self, callback) -> str:
        """Bind to ``<<RowUpdate>>``. Callback receives ``event.data = {'records': list[dict]}``."""
        return self.bind("<<RowUpdate>>", callback, add=True)

    def off_row_updated(self, bind_id: str | None = None) -> None:
        """Unbind from ``<<RowUpdate>>``."""
        self.unbind("<<RowUpdate>>", bind_id)

    def on_row_moved(self, callback) -> str:
        """Bind to ``<<RowMove>>``. Callback receives ``event.data = {'records': list[dict]}``."""
        return self.bind("<<RowMove>>", callback, add=True)

    def off_row_moved(self, bind_id: str | None = None) -> None:
        """Unbind from ``<<RowMove>>``."""
        self.unbind("<<RowMove>>", bind_id)

    # ------------------------------------------------------------------ Public data/selection API
    @property
    def selected_rows(self) -> list[dict]:
        """List of record dicts for the current Treeview selection."""
        rows: list[dict] = []
        for iid in self._tree.selection():
            if iid in self._row_map:
                rows.append(self._row_map[iid])
        return rows

    @property
    def visible_rows(self) -> list[dict]:
        """List of record dicts for rows currently rendered (flat traversal)."""
        rows: list[dict] = []
        queue = list(self._tree.get_children(""))
        while queue:
            iid = queue.pop(0)
            if iid in self._row_map:
                rows.append(self._row_map[iid])
            queue.extend(list(self._tree.get_children(iid)))
        return rows

    # ------------------------------------------------------------------ Public row/column manipulation
    def insert_rows(self, rows: list) -> None:
        """Insert new rows via the datasource and refresh."""
        recs = self._to_records(rows)
        inserted: list[dict] = []
        for rec in recs:
            try:
                new_id = self._datasource.create_record(dict(rec))
                rec = dict(rec)
                if new_id is not None:
                    rec["id"] = new_id
                inserted.append(rec)
            except Exception:
                logger.exception("Failed to insert record")
        if inserted:
            self._clear_cache()
            self._load_page(self._current_page)
            self.event_generate("<<RowInsert>>", data={"records": inserted})

    def update_rows(self, rows: list[dict]) -> None:
        """Update rows by id; each dict must include an 'id' key."""
        updated: list[dict] = []
        for rec in rows:
            rec_id = rec.get("id")
            if rec_id is None:
                continue
            updates = {k: v for k, v in rec.items() if k != "id"}
            try:
                self._datasource.update_record(rec_id, updates)
                updated.append(rec)
            except Exception:
                logger.exception("Failed to update record id=%s", rec_id)
        if updated:
            self._clear_cache()
            self._load_page(self._current_page)
            self.event_generate("<<RowUpdate>>", data={"records": updated})

    def delete_rows(self, rows_or_ids: list) -> None:
        """Delete rows by id or row dicts containing an id key."""
        deleted: list[dict] = []
        for item in rows_or_ids:
            rec_id = None
            rec = {}
            if isinstance(item, dict):
                rec = item
                rec_id = item.get("id")
            else:
                rec_id = item
            if rec_id is None:
                continue
            try:
                self._datasource.delete_record(rec_id)
                if not rec:
                    rec = {"id": rec_id}
                deleted.append(rec)
            except Exception:
                logger.exception("Failed to delete record id=%s", rec_id)
        if deleted:
            self._clear_cache()
            self._load_page(self._current_page)
            self.event_generate("<<RowDelete>>", data={"records": deleted})

    def insert_columns(self, *_args, **_kwargs) -> None:
        """Not currently supported; columns are defined at construction time."""
        raise NotImplementedError("Dynamic column insertion is not supported yet")

    def delete_columns(self, indices: list[int]) -> None:
        """Hide columns at the given indices."""
        self.hide_columns(indices)

    def move_rows(self, iids: list[str], to_index: int) -> None:
        """Move the given rows to a target index in the root list."""
        children = list(self._tree.get_children(""))
        to_index = max(0, min(len(children), to_index))
        for offset, iid in enumerate(iids):
            try:
                self._tree.move(iid, "", to_index + offset)
            except Exception:
                pass
        self._apply_row_alternation()
        moved_recs = [self._row_map.get(i) for i in iids if i in self._row_map]
        if moved_recs:
            self.event_generate("<<RowMove>>", data={"records": moved_recs})

    def move_columns(self, from_index: int, to_index: int) -> None:
        """Reorder a column from one index to another."""
        if from_index < 0 or from_index >= len(self._display_columns):
            return
        to_index = max(0, min(len(self._display_columns) - 1, to_index))
        col_id = self._display_columns.pop(from_index)
        self._display_columns.insert(to_index, col_id)
        self._tree.configure(displaycolumns=self._display_columns)

    def hide_rows(self, iids: list[str]) -> None:
        """Hide rows from view (not removed from datasource)."""
        for iid in iids:
            try:
                parent = self._tree.parent(iid)
                children = list(self._tree.get_children(parent))
                idx = children.index(iid)
                self._hidden_rows[iid] = (parent, idx)
                self._tree.detach(iid)
            except Exception:
                pass

    def unhide_rows(self, iids: list[str] | None = None) -> None:
        """Restore previously hidden rows."""
        targets = iids or list(self._hidden_rows.keys())
        for iid in targets:
            if iid not in self._hidden_rows:
                continue
            parent, idx = self._hidden_rows.pop(iid)
            try:
                self._tree.move(iid, parent, idx)
            except Exception:
                pass
        self._apply_row_alternation()

    def hide_columns(self, indices: list[int]) -> None:
        """Remove columns from the displayed set."""
        for idx in indices:
            if idx in self._display_columns:
                self._display_columns.remove(idx)
        if not self._display_columns and self._heading_texts:
            self._display_columns = list(range(len(self._heading_texts)))
        self._tree.configure(displaycolumns=self._display_columns)

    def unhide_columns(self, indices: list[int]) -> None:
        """Add columns back into the displayed set."""
        changed = False
        for idx in indices:
            if idx not in self._display_columns and 0 <= idx < len(self._heading_texts):
                self._display_columns.append(idx)
                changed = True
        if changed:
            self._display_columns = sorted(self._display_columns)
            self._tree.configure(displaycolumns=self._display_columns)

    def select_rows(self, iids: list[str]) -> None:
        """Select the given row ids."""
        self._tree.selection_set(iids)

    def deselect_rows(self, iids: list[str] | None = None) -> None:
        """Clear selection or remove specific iids from selection."""
        if not iids:
            self._tree.selection_remove(self._tree.selection())
        else:
            self._tree.selection_remove(iids)

    def scroll_to_row(self, iid: str) -> None:
        """Ensure the given row is visible."""
        try:
            self._tree.see(iid)
        except Exception:
            pass

    # ------------------------------------------------------------------ Pagination helpers
    def next_page(self) -> None:
        self._next_page()

    def previous_page(self) -> None:
        self._prev_page()

    def first_page(self) -> None:
        self._first_page()

    def last_page(self) -> None:
        self._last_page()

    def go_to_page(self, index: int) -> None:
        self._load_page(max(0, index))

    # ------------------------------------------------------------------ Filter/Sort/Group API
    def get_filters(self) -> str:
        """Return current SQL where clause string (if any)."""
        try:
            return getattr(self._datasource, "_where", "") or ""
        except Exception:
            return ""

    def set_filters(self, where: str) -> None:
        try:
            self._datasource.set_filter(where or "")
        except Exception:
            return
        self._clear_cache()
        self._load_page(0)
        self._update_status_labels()

    def clear_filters(self) -> None:
        self._clear_filter_cmd()

    def get_sorting(self) -> dict[str, bool]:
        """Return a copy of the current sort state {column_key: ascending}."""
        return dict(self._sort_state)

    def set_sorting(self, key: str, ascending: bool = True) -> None:
        quoted_key = self._quote_col(key)
        order = "ASC" if ascending else "DESC"
        try:
            self._datasource.set_sort(f"{quoted_key} {order}")
        except Exception:
            return
        self._sort_state = {key: ascending}
        self._clear_cache()
        self._update_heading_icons()
        self._load_page(0)
        self._update_status_labels()

    def clear_sorting(self) -> None:
        self._clear_sort()

    def get_grouping(self) -> str | None:
        return self._group_by_key

    def set_grouping(self, key: str | None) -> None:
        if not key:
            self._ungroup_all()
            return
        if key not in self._column_keys:
            return
        self._group_by_key = key
        self._group_parents.clear()
        try:
            quoted_key = self._quote_col(key)
            self._datasource.set_sort(f"{quoted_key} ASC")
        except Exception:
            pass
        self._sort_state = {key: True}
        self._clear_cache()
        self._update_heading_icons()
        self._load_page(0)
        self._update_status_labels()

    def clear_grouping(self) -> None:
        self._ungroup_all()

    # ------------------------------------------------------------------ Group expand/collapse
    def expand_all(self) -> None:
        for iid in self._tree.get_children(""):
            try:
                self._tree.item(iid, open=True)
            except Exception:
                pass

    def collapse_all(self) -> None:
        for iid in self._tree.get_children(""):
            try:
                self._tree.item(iid, open=False)
            except Exception:
                pass

    def expand_group(self, group_value) -> None:
        parent = self._group_parents.get(group_value)
        if parent:
            try:
                self._tree.item(parent, open=True)
            except Exception:
                pass

    def collapse_group(self, group_value) -> None:
        parent = self._group_parents.get(group_value)
        if parent:
            try:
                self._tree.item(parent, open=False)
            except Exception:
                pass

    def select_all(self) -> None:
        """Select all visible rows."""
        self._tree.selection_set(self._tree.get_children(""))

    def deselect_all(self) -> None:
        """Clear the selection."""
        self._tree.selection_remove(self._tree.selection())

    # ------------------------------------------------------------------ UI

    def _resolve_alternating_row_color(self):
        style = get_style()
        color_token = self._row_alternation.get('color', 'background[+1]')

        try:
            background = style.style_builder.color(color_token)
        except Exception:
            background = style.style_builder.color('background')

        try:
            foreground = style.style_builder.on_color(background)
        except Exception:
            foreground = style.style_builder.color('foreground')
        return background, foreground

    def _resolve_column_keys(self) -> None:
        if not self._column_defs:
            return
        for idx, col in enumerate(self._column_defs):
            if isinstance(col, str):
                self._column_keys.append(col)
            elif isinstance(col, dict):
                self._column_keys.append(col.get("key") or col.get("text") or str(idx))
            else:
                self._column_keys.append(str(col))

    def _ensure_column_metadata(self, sample_records: list[dict] | None) -> None:
        """Guarantee we have column keys/defs before the Treeview is built."""
        if self._column_keys:
            return

        inferred: list[str] = []
        if sample_records:
            first = sample_records[0]
            if isinstance(first, dict):
                inferred = list(first.keys())
        if not inferred:
            inferred = getattr(self._datasource, "_columns", []) or []

        inferred = [c for c in inferred if c not in ("id", "selected")]
        if not inferred:
            inferred = ["value"]

        self._column_keys = inferred
        if not self._column_defs:
            self._column_defs = [{"text": c} for c in self._column_keys]

    def _build_toolbar(self) -> None:
        bar = Frame(self, name="toolbar")
        bar.pack(fill="x", pady=(0, 4))

        if self._searchbar['enabled']:
            self._search_entry = TextEntry(bar)
            self._search_entry.insert_addon(Label, 'before', icon="search", icon_only=True)
            self._search_entry.insert_addon(Button, 'after', icon="x-lg", icon_only=True, command=self._clear_search)
            self._search_entry.pack(side="left", fill="x", expand=True, padx=(0, 6))
            trigger = str(self._searchbar.get('event', 'enter')).lower()
            if trigger == 'input':
                self._search_entry.on_input(lambda _e: self._run_search())
            else:
                self._search_entry.on_enter(lambda _e: self._run_search())
                # Clear filter when the box is emptied, but do not search on every keystroke
                self._search_entry.on_input(lambda _e: self._clear_search() if not self._search_entry.get() else None)

            if self._searchbar['mode'] == 'advanced':
                search_items = []
                self._search_mode_map = {}
                for token, code in _TABLE_SEARCH_MODE_OPTIONS:
                    label = MessageCatalog.translate(token)
                    search_items.append(label)
                    self._search_mode_map[label] = code
                default_value = search_items[0] if search_items else "EQUALS"
                self._search_mode = SelectBox(
                    bar,
                    items=search_items,
                    value=default_value,
                    width=14,
                    allow_custom_values=False,
                    search_enabled=False,
                )
                self._search_mode.pack(side="left", padx=(0, 6))

        if self._show_column_chooser:
            self._column_chooser_btn = Button(
                bar,
                icon="layout-three-columns",
                icon_only=True,
                color="foreground",
                variant="ghost",
                command=self._show_column_chooser_dialog,
            )
            self._column_chooser_btn.pack(side="right", padx=(4, 0))

        if self._exporting['enabled']:
            export_items = []
            if self._exporting['export_all_mode'] == 'all':
                export_items.append({"type": "command", "text": "table.export_all", "command": self._export_all})
            if self._exporting["allow_export_selected"]:
                export_items.append({"type": "command", "text": "table.export_selection", "command": self._export_selection})
            if self._exporting['export_all_mode'] == "page":
                export_items.append({"type": "command", "text": "table.export_page", "command": self._export_page})
            if not export_items:
                export_items.append({"type": "command", "text": "table.export_all", "command": self._export_all})
            DropdownButton(
                bar,
                icon="download",
                icon_only=True,
                color="foreground",
                variant="ghost",
                compound="image",
                items=export_items,
                show_dropdown_button=False,
            ).pack(side="right")

        if self._editing['adding']:
            Button(
                bar,
                icon="plus-lg",
                text="table.add_record",
                color="foreground",
                variant="ghost",
                command=self._open_new_record,
            ).pack(side="right", padx=(0, 4))

    def _build_tree(self) -> None:
        frame = Frame(self)
        frame.pack(fill="both", expand=True)

        cols = [self._col_text(c) for c in self._column_defs] or self._column_keys
        tree_container = Frame(frame)
        tree_container.pack(side="left", fill="both", expand=True)
        # Prevent the tree from expanding the container beyond the available viewport
        tree_container.pack_propagate(False)

        self._tree = TreeView(
            tree_container,
            columns=list(range(len(cols))),
            selectmode=_parse_selection_mode(self._selection['mode']),
            show="headings"
        )
        self._tree.pack(side="top", fill="both", expand=True, padx=3)
        self._display_columns = list(range(len(cols)))

        if self._paging['yscroll']:
            self._vsb = Scrollbar(frame, orient="vertical", command=self._tree.yview)
            self._vsb.pack(side="right", fill="y")
            if self._paging['mode'] == "virtual":
                self._tree.configure(yscrollcommand=self._on_scroll)
            else:
                self._tree.configure(yscrollcommand=self._vsb.set)
        else:
            self._vsb = None

        if self._paging['xscroll']:
            self._hsb = Scrollbar(tree_container, orient="horizontal", command=self._tree.xview)
            self._hsb.pack(side="bottom", fill="x")
            self._tree.configure(xscrollcommand=self._hsb.set)
        else:
            self._hsb = None

        self._heading_texts = []
        self._column_anchors = []
        stretch_columns = not self._paging['xscroll']  # allow natural width when xscroll is enabled
        for idx, text in enumerate(cols):
            self._heading_texts.append(text)
            anchor = self._determine_anchor(idx)
            self._column_anchors.append(anchor)
            heading_kwargs = {"text": text, "anchor": anchor}
            # Don't use heading command - we'll handle clicks via Button-1 binding
            self._tree.heading(idx, **heading_kwargs)
            # Apply per-column width overrides, fall back to global defaults
            width = 120
            minwidth = self._column_min_width
            if idx < len(self._column_defs):
                coldef = self._column_defs[idx]
                if isinstance(coldef, dict):
                    width = coldef.get("width", width)
                    minwidth = coldef.get("minwidth", coldef.get("min_width", minwidth))
            self._tree.column(idx, anchor=anchor, width=width, minwidth=minwidth, stretch=stretch_columns)
        self._update_heading_icons()
        self._tree.bind("<Button-1>", self._on_header_click)
        self._tree.bind("<<TreeviewSelect>>", self._on_selection_event)
        self._tree.bind("<ButtonRelease-1>", self._on_row_click_event)
        if self._context_menus != "none":
            self._tree.bind("<Button-3>", self._on_tree_context)
        if self._editing['updating']:
            self._tree.bind("<Double-1>", self._on_row_double_click)
        # Track resize events to rebalance grouped layouts
        self._tree.bind("<Configure>", self._on_tree_configure)

    def _build_footer(self) -> None:
        bar = Frame(self)
        bar.pack(fill="x", pady=(4, 0))
        status_frame = Frame(bar)
        status_frame.pack(side="left", fill="x", expand=True)
        self._filter_label = Label(status_frame, text="", anchor="w", color="secondary")
        self._filter_label.pack(side="left", padx=(0, 4))
        self._sort_label = Label(status_frame, text="", anchor="w", color="secondary")
        self._sort_label.pack(side="left", padx=(8, 4))

        if not self._show_table_status:
            status_frame.pack_forget()
        Frame(bar).pack(side='left', fill='x', expand=True)  # spacer
        info_frame = Frame(bar)
        info_frame.pack(side='left')
        Label(info_frame, text="table.page").pack(side='left')
        self._page_entry = Entry(info_frame, width=6, justify="center")
        self._page_entry.bind("<Return>", self._jump_page)
        self._page_entry.pack(side="left", padx=8)
        self._page_label = Label(info_frame, text="")
        self._page_label.pack(side="left", padx=(0, 8))

        sep = Separator(bar, orient="vertical")
        sep.pack(side="left", fill="y", padx=8)

        btn_frame = Frame(bar)
        btn_frame.pack(side="right")
        Button(btn_frame, icon="chevron-double-left", color="foreground", variant="ghost", icon_only=True, command=self._first_page).pack(
            side="left")
        Button(btn_frame, icon="chevron-left", icon_only=True, color="foreground", variant="ghost", command=self._prev_page).pack(
            side="left")
        Button(btn_frame, icon="chevron-right", icon_only=True, color="foreground", variant="ghost", command=self._next_page).pack(
            side="left")
        Button(btn_frame, icon="chevron-double-right", icon_only=True, color="foreground", variant="ghost", command=self._last_page).pack(
            side="left")

    # ------------------------------------------------------------------ Helpers
    def _col_text(self, col) -> str:
        if isinstance(col, str):
            return col
        if isinstance(col, dict):
            return col.get("text") or col.get("key") or ""
        return str(col)

    def _header_context_enabled(self) -> bool:
        return self._context_menus in ("all", "headers")

    def _row_context_enabled(self) -> bool:
        return self._context_menus in ("all", "rows")

    def _quote_col(self, key: str) -> str:
        """Quote column identifiers for safe SQL usage (handles reserved names)."""
        try:
            quote_fn = getattr(self._datasource, "_quote_identifier", None)
            if callable(quote_fn):
                return quote_fn(key)
        except Exception:
            pass
        text = str(key).replace('"', '""')
        return f'"{text}"'

    def _determine_anchor(self, idx: int) -> str:
        """Pick an anchor for the given column index.

        Priority:
            1) Explicit anchor/align in column definition
            2) Explicit dtype/type hint in column definition (numeric -> right)
            3) Numeric columns -> right
            4) Default -> left
        """
        if idx < len(self._column_defs):
            coldef = self._column_defs[idx]
            if isinstance(coldef, dict):
                anchor = coldef.get("anchor") or coldef.get("align")
                if anchor:
                    return anchor
                # Allow a dtype/type hint on the column definition
                dtype = coldef.get("dtype") or coldef.get("type")
                if dtype:
                    dtype_upper = str(dtype).upper()
                    if any(t in dtype_upper for t in ("INT", "REAL", "NUM", "DECIMAL", "DOUBLE", "FLOAT")):
                        return "e"
                    if "TEXT" in dtype_upper or "STR" in dtype_upper or "CHAR" in dtype_upper:
                        return "w"
        # Infer from type
        key = self._column_keys[idx] if idx < len(self._column_keys) else None
        ctype = self._get_column_type(key) if key else ""
        if ctype and any(t in ctype.upper() for t in ("INT", "REAL", "NUM", "DECIMAL", "DOUBLE", "FLOAT")):
            return "e"
        # Fallback: sample values to detect numeric strings
        if self._is_numeric_sample(idx):
            return "e"
        return "w"

    def _get_column_type(self, key: str | None) -> str:
        if not key:
            return ""
        if key in self._column_types:
            return self._column_types[key]
        # Try PRAGMA table_info
        try:
            cur = self._datasource.conn.execute(f"PRAGMA table_info({self._datasource._table})")
            for cid, name, ctype, *_rest in cur.fetchall():
                if name == key:
                    self._column_types[key] = ctype or ""
                    return self._column_types[key]
        except Exception:
            pass
        return ""

    def _load_alignment_sample(self) -> list[dict]:
        if self._alignment_sample is not None:
            return self._alignment_sample
        try:
            sample = self._datasource.get_page(0)
        except Exception:
            sample = []
        self._alignment_sample = sample or []
        return self._alignment_sample

    def _is_numeric_sample(self, idx: int) -> bool:
        """Check sample values to decide if a column with text storage is numeric-like."""
        key = self._column_keys[idx] if idx < len(self._column_keys) else None
        if not key:
            return False
        sample = self._load_alignment_sample()
        if not sample:
            return False

        def is_num(val) -> bool:
            if val is None or val == "":
                return True
            try:
                float(val)
                return True
            except Exception:
                return False

        seen = 0
        for rec in sample[: min(20, len(sample))]:
            if key not in rec:
                continue
            seen += 1
            if not is_num(rec.get(key)):
                return False
        return seen > 0

    def _to_records(self, rows: list) -> list[dict]:
        records: list[dict] = []
        if not rows:
            return records
        keys = self._column_keys or [str(i) for i in range(len(rows[0]))]
        for rec in rows:
            if isinstance(rec, dict):
                records.append(rec)
            else:
                records.append({k: rec[i] if i < len(rec) else "" for i, k in enumerate(keys)})
        return records

    def _refresh_tree(self, records: list[dict]) -> None:
        self._tree.delete(*self._tree.get_children())
        self._row_map.clear()
        if not self._column_keys and records:
            self._column_keys = list(records[0].keys())
        grouped = bool(self._group_by_key) and self._group_by_key in self._column_keys
        self._apply_group_show_state(grouped)
        if grouped:
            self._render_grouped(records)
        else:
            self._render_flat(records)
        self._apply_row_alternation()

    def _append_tree(self, records: list[dict]) -> None:
        # Grouped mode rebuilds the view instead of appending to keep hierarchy consistent
        if self._group_by_key:
            self._refresh_tree(records)
            return
        stripe = self._row_alternation.get('enabled', False) and not self._group_by_key
        start_idx = len(self._tree.get_children(""))
        for offset, rec in enumerate(records):
            values = [rec.get(k, "") for k in self._column_keys]
            tags = ("altrow",) if stripe and (start_idx + offset) % 2 == 1 else ()
            iid = self._tree.insert("", "end", values=values, tags=tags)
            self._row_map[iid] = rec
        self._apply_row_alternation()

    def _total_pages(self) -> int:
        try:
            # Use cached count to avoid expensive COUNT(*) queries on every navigation
            if self._cached_total_count is None:
                self._cached_total_count = self._datasource.total_count()
            total = self._cached_total_count
            size = getattr(self._datasource, "page_size", self._paging['page_size']) or 1
            return max(1, (total + size - 1) // size)
        except Exception:
            return 1

    # ------------------------------------------------------------------ Paging
    def _load_page(self, page: int, append: bool = False) -> None:
        if not append and page in self._page_cache:
            records = self._page_cache[page]
        else:
            try:
                records = self._datasource.get_page(page)
            except Exception:
                records = []
            if not append:
                self._remember_page(page, records)
        self._current_page = max(0, page)
        try:
            if append:
                self._append_tree(records)
            else:
                self._refresh_tree(records)
            if self._column_auto_width:
                self._auto_size_columns(records if not append else None)
            self._update_page_label()
        finally:
            self._loading_next = False

    def _update_page_label(self) -> None:
        if hasattr(self, "_page_entry"):
            self._page_entry.delete(0, 'end')
            self._page_entry.insert(0, str(self._current_page + 1))
        if hasattr(self, "_page_label"):
            of_text = MessageCatalog.translate("table.of")
            self._page_label.configure(text=f"{of_text} {self._total_pages()}")
        if self._show_table_status:
            self._update_status_labels()

    def _first_page(self) -> None:
        self._load_page(0)

    def _prev_page(self) -> None:
        self._load_page(max(0, self._current_page - 1))

    def _next_page(self) -> None:
        self._load_page(min(self._total_pages() - 1, self._current_page + 1))

    def _last_page(self) -> None:
        self._load_page(self._total_pages() - 1)

    def _jump_page(self, _event=None) -> None:
        try:
            target = int(self._page_entry.get()) - 1
        except Exception:
            return
        target = max(0, min(self._total_pages() - 1, target))
        self._load_page(target)

    def _on_scroll(self, first: float, last: float) -> None:
        """Drive scrollbar and trigger lazy loading when near the bottom."""
        # Grouped mode disables virtual scroll append to avoid breaking hierarchy
        if self._group_by_key:
            self._vsb.set(first, last)
            return
        try:
            first_f = float(first)
            last_f = float(last)
        except Exception:
            self._vsb.set(first, last)
            return

        self._vsb.set(first_f, last_f)
        if (
                self._paging['mode'] == "virtual"
                and last_f >= 0.85  # prefetch a bit earlier for smoother scrolling
                and not self._loading_next
                and hasattr(self._datasource, "has_next_page")
                and self._datasource.has_next_page()
        ):
            # Load next page and keep appending rows
            self._loading_next = True
            self._load_page(self._current_page + 1, append=True)

    # ------------------------------------------------------------------ Search & sort
    def _run_search(self) -> None:
        text = self._search_entry.get()
        if hasattr(self, "_search_mode") and self._search_mode_map:
            display_mode = self._search_mode.get()
            mode = self._search_mode_map.get(display_mode, "CONTAINS")
        else:
            mode = "CONTAINS"
        colnames = self._column_keys
        quoted_cols = [self._quote_col(c) for c in colnames]
        where = ""
        if text and quoted_cols:
            crit = text.replace("'", "''")
            mode_upper = mode.upper().replace(" ", "_")
            if mode_upper == "CONTAINS":
                where = " OR ".join([f"{c} LIKE '%{crit}%'" for c in quoted_cols])
            elif mode_upper == "STARTS_WITH":
                where = " OR ".join([f"{c} LIKE '{crit}%'" for c in quoted_cols])
            elif mode_upper == "ENDS_WITH":
                where = " OR ".join([f"{c} LIKE '%{crit}'" for c in quoted_cols])
            elif mode_upper == "SQL":
                where = text
            else:  # equals
                where = " OR ".join([f"{c} = '{crit}'" for c in quoted_cols])
        try:
            self._datasource.set_filter(where)
        except Exception:
            logger.exception("Failed to apply search filter: %s", where)
        self._clear_cache()
        self._load_page(0)
        self._update_status_labels()

    def _clear_search(self) -> None:
        self._search_entry.delete(0, 'end')
        try:
            self._datasource.set_filter("")
        except Exception:
            pass
        self._clear_cache()
        self._load_page(0)
        self._update_status_labels()

    def _on_sort(self, column_index: int) -> None:
        if column_index >= len(self._column_keys):
            return
        key = self._column_keys[column_index]
        quoted_key = self._quote_col(key)
        asc = not self._sort_state.get(key, True)
        # Clear other sort states to keep single-column sort
        self._sort_state = {key: asc}
        order = "ASC" if asc else "DESC"
        try:
            self._datasource.set_sort(f"{quoted_key} {order}")
        except Exception:
            pass
        self._clear_cache()
        self._update_heading_icons()
        self._load_page(0)
        self._update_status_labels()

    def _update_status_labels(self) -> None:
        # Filter
        filter_txt = ""
        try:
            where = getattr(self._datasource, "_where", "")
            if where:
                filter_txt = MessageCatalog.translate("table.filter_status", where)
        except Exception:
            pass
        # Sort
        sort_txt = ""
        try:
            order = getattr(self._datasource, "_order_by", "")
            if order:
                sort_txt = MessageCatalog.translate("table.sort_status", order)
        except Exception:
            pass
        group_txt = ""
        if self._group_by_key:
            try:
                col_idx = self._column_keys.index(self._group_by_key)
                heading_text = self._heading_texts[col_idx] if col_idx < len(
                    self._heading_texts) else self._group_by_key
            except Exception:
                heading_text = self._group_by_key
            group_txt = MessageCatalog.translate("table.group_status", heading_text)

        if hasattr(self, "_filter_label"):
            self._filter_label.configure(text=filter_txt)
        if hasattr(self, "_sort_label"):
            joined = " | ".join([t for t in (sort_txt, group_txt) if t])
            self._sort_label.configure(text=joined)

    # ------------------------------------------------------------------ Row context menu
    def _ensure_row_menu(self) -> None:
        if not self._row_context_enabled():
            return
        if self._row_menu:
            return
        menu = ContextMenu(master=self, target=self._tree, attach='sw')
        if not self._sorting == 'none':
            menu.add_command(text="table.sort_asc", command=lambda: self._sort_selection(True))
            menu.add_command(text="table.sort_desc", command=lambda: self._sort_selection(False))

        if self._filtering['row_menu_filtering']:
            menu.add_separator()
            menu.add_command(text="table.filter_by_value", command=self._filter_by_value)
            menu.add_command(text="table.hide_select", command=self._hide_selection)
            menu.add_command(text="table.clear_filters", command=self._clear_filter_cmd)

        menu.add_separator()
        menu.add_command(text="table.move_up", command=self._move_row_up)
        menu.add_command(text="table.move_down", command=self._move_row_down)
        menu.add_command(text="table.move_top", command=self._move_row_top)
        menu.add_command(text="table.move_bottom", command=self._move_row_bottom)

        if self._editing['updating'] or self._editing['deleting']:
            menu.add_separator()
            if self._editing['updating']:
                menu.add_command(text="table.edit", icon="pencil", command=self._edit_selected_row)
            if self._editing['deleting']:
                menu.add_command(text="table.delete_row", icon="trash", command=self._delete_selected_row)
        self._row_menu = menu

    def _on_row_context(self, event) -> None:
        if not self._row_context_enabled():
            return
        iid = self._tree.identify_row(event.y)
        col_id = self._tree.identify_column(event.x)
        try:
            col_idx = int(col_id.strip("#")) - 1
        except Exception:
            col_idx = 0
        if iid:
            if iid not in self._tree.selection():
                self._tree.selection_set(iid)
            rec = self._row_map.get(iid, {})
            self.event_generate("<<RowRightClick>>", data={"record": rec, "iid": iid})
        if not self._tree.selection():
            return
        self._row_menu_col = col_idx
        self._ensure_row_menu()
        self._row_menu.show(position=(event.x_root, event.y_root))

    def _on_row_double_click(self, event) -> None:
        region = self._tree.identify_region(event.x, event.y)
        if region == "heading":
            return
        iid = self._tree.identify_row(event.y)
        if not iid:
            return
        rec = self._row_map.get(iid, {})
        self.event_generate("<<RowDoubleClick>>", data={"record": rec, "iid": iid})
        if self._editing['updating']:
            self._open_form_dialog(rec)

    def _open_new_record(self) -> None:
        if not self._editing['adding']:
            return
        self._open_form_dialog(None)

    def _open_form_dialog(self, record: dict | None) -> None:
        from ttkbootstrap.dialogs.formdialog import FormDialog

        try:
            # Ensure geometry info is current so centering uses real widget bounds
            self.update_idletasks()
        except Exception:
            pass
        dialog_master = self.winfo_toplevel() if hasattr(self, "winfo_toplevel") else self

        form_items = self._build_form_items()
        initial_data = dict(record) if record else {}

        form_options = dict(self._editing['form'])
        form_options.setdefault('col_count', 2)
        form_options.setdefault('min_col_width', 260)
        form_options.setdefault('scrollable', True)
        form_options.setdefault('resizable', True)

        # Build buttons: Cancel, Delete (only for existing records), Save
        if record and "id" in record:
            buttons: list[str | dict] = ['Cancel']
            if self._editing['deleting']:
                buttons.append({"text": "Delete", "role": "secondary", "result": "delete"})
            buttons.append("Save")
        else:
            buttons = ["Cancel", "Save"]

        dialog = FormDialog(
            master=dialog_master,
            title="Edit Record" if record else "New Record",
            data=initial_data,
            items=form_items,
            col_count=form_options.get('col_count', 2),
            min_col_width=form_options.get('min_col_width', 260),
            scrollable=form_options.get('scrollable', True),
            buttons=buttons,
            resizable=(True, True) if form_options.get('resizable', True) else (False, False),
        )

        dialog.show(anchor_to="screen")
        result = dialog.result

        if result is None:
            return

        # Handle delete action
        if result == "delete" and record and "id" in record:
            try:
                self._datasource.delete_record(record["id"])
                self._clear_cache()
                self._load_page(self._current_page)
            except Exception:
                logger.exception("Failed to delete record id=%s", record["id"])
            return

        data = result
        new_id = None
        if record and "id" in record:
            rec_id = record["id"]
            updates = dict(data)
            updates.pop("id", None)
            try:
                logger.debug("Updating record id=%s with %s", rec_id, updates)
                self._datasource.update_record(rec_id, updates)
            except Exception:
                logger.exception("Failed to update record id=%s", rec_id)
                return
        else:
            try:
                logger.debug("Creating record %s", data)
                new_id = self._datasource.create_record(dict(data))
                logger.debug("Created record id=%s (total=%s)", new_id, self._datasource.total_count())
            except Exception:
                logger.exception("Failed to create record from %s", data)
                return
        self._clear_cache()
        target_page = self._current_page
        if not record:
            # After creating, compute last page using fresh count so the new row is visible
            located_page = self._find_record_page(new_id) if new_id is not None else None
            target_page = located_page if located_page is not None else max(0, self._total_pages() - 1)
        self._load_page(target_page)
        if new_id is not None:
            self._focus_record(new_id)

    def _build_form_items(self) -> list[dict]:
        items: list[dict] = []
        for idx, key in enumerate(self._column_keys):
            coldef = self._column_defs[idx] if idx < len(self._column_defs) else key
            label = self._col_text(coldef)
            editor_opts = {}
            editor = None
            dtype = None
            readonly = False
            if isinstance(coldef, dict):
                editor_opts = dict(coldef.get("editor_options", {}))
                editor = coldef.get("editor")
                dtype = coldef.get("dtype") or coldef.get("type")
                readonly = bool(coldef.get("readonly", False))
                if coldef.get("required"):
                    editor_opts.setdefault("required", True)
            # Show validation messages to avoid layout jump on first error
            editor_opts.setdefault("show_message", True)
            items.append(
                {
                    "key": key,
                    "label": label,
                    "dtype": dtype,
                    "editor": editor,
                    "editor_options": {**editor_opts},
                    "readonly": readonly,
                    "type": "field",
                }
            )
        return items

    def _filter_by_value(self) -> None:
        selection = self._tree.selection()
        if not selection:
            return
        iid = selection[0]
        col_idx = max(0, min(self._row_menu_col or 0, len(self._column_keys) - 1))
        key = self._column_keys[col_idx]
        quoted_key = self._quote_col(key)
        values = self._tree.item(iid, "values")
        if col_idx >= len(values):
            return
        val = values[col_idx]
        crit = str(val).replace("'", "''")
        where = f"{quoted_key} = '{crit}'"
        try:
            self._datasource.set_filter(where)
        except Exception:
            return
        self._clear_cache()
        self._load_page(0)

    def _sort_selection(self, ascending: bool) -> None:
        selection = self._tree.selection()
        if not selection:
            return
        iid = selection[0]
        col_idx = max(0, min(self._row_menu_col or 0, len(self._column_keys) - 1))
        key = self._column_keys[col_idx]
        quoted_key = self._quote_col(key)
        self._sort_state = {key: ascending}
        order = "ASC" if ascending else "DESC"
        try:
            self._datasource.set_sort(f"{quoted_key} {order}")
        except Exception:
            pass
        self._clear_cache()
        self._update_heading_icons()
        self._load_page(0)

    def _clear_filter_cmd(self) -> None:
        try:
            self._datasource.set_filter("")
        except Exception:
            pass
        self._clear_cache()
        self._load_page(0)
        self._update_status_labels()

    def _move_row_up(self) -> None:
        self._move_row_relative(-1)

    def _move_row_down(self) -> None:
        self._move_row_relative(1)

    def _move_row_top(self) -> None:
        self._move_row_absolute(0)

    def _move_row_bottom(self) -> None:
        children = list(self._tree.get_children())
        if children:
            self._move_row_absolute(len(children) - 1)

    def _move_row_relative(self, delta: int) -> None:
        sel = list(self._tree.selection())
        if not sel:
            return
        target_iid = sel[0]
        children = list(self._tree.get_children())
        try:
            idx = children.index(target_iid)
        except ValueError:
            return
        new_idx = max(0, min(len(children) - 1, idx + delta))
        if new_idx == idx:
            return
        self._tree.move(target_iid, "", new_idx)
        self._apply_row_alternation()
        rec = self._row_map.get(target_iid)
        if rec:
            self.event_generate("<<RowMove>>", data={"records": [rec]})

    def _move_row_absolute(self, new_idx: int) -> None:
        sel = list(self._tree.selection())
        if not sel:
            return
        target_iid = sel[0]
        children = list(self._tree.get_children())
        new_idx = max(0, min(len(children) - 1, new_idx))
        self._tree.move(target_iid, "", new_idx)
        self._apply_row_alternation()
        rec = self._row_map.get(target_iid)
        if rec:
            self.event_generate("<<RowMove>>", data={"records": [rec]})

    def _hide_selection(self) -> None:
        sel = list(self._tree.selection())
        for iid in sel:
            self._tree.delete(iid)
            self._row_map.pop(iid, None)

    def _edit_selected_row(self) -> None:
        """Open the form dialog for the first selected row."""
        sel = list(self._tree.selection())
        if not sel:
            return
        iid = sel[0]
        rec = self._row_map.get(iid, {})
        self._open_form_dialog(rec)

    def _delete_selected_row(self) -> None:
        """Delete the first selected row from the datasource."""
        sel = list(self._tree.selection())
        if not sel:
            return
        iid = sel[0]
        rec = self._row_map.get(iid, {})
        rec_id = rec.get("id")
        if rec_id is not None:
            try:
                self._datasource.delete_record(rec_id)
                self._clear_cache()
                self._load_page(self._current_page)
                self.event_generate("<<RowDelete>>", data={"records": [rec]})
            except Exception:
                logger.exception("Failed to delete record id=%s", rec_id)

    def _delete_selection(self) -> None:
        sel = list(self._tree.selection())
        deleted_records: list[dict] = []
        changed = False
        for iid in sel:
            rec = dict(self._row_map.get(iid) or {})
            if rec:
                deleted_records.append(rec)
            rec_id = rec.get("id")
            if rec_id is not None:
                try:
                    self._datasource.delete_record(rec_id)
                    changed = True
                except Exception:
                    pass
            self._row_map.pop(iid, None)
        if changed:
            self._clear_cache()
            self._load_page(self._current_page)
            if deleted_records:
                self.event_generate("<<RowDelete>>", data={"records": deleted_records})

    # ------------------------------------------------------------------ Cache helpers
    def _clear_cache(self) -> None:
        if self._page_cache:
            self._page_cache.clear()
        # Invalidate total count cache when data/filter/sort changes
        self._cached_total_count = None

    def _load_heading_icons(self) -> None:
        """Load and cache heading icons (sort arrows) sized to match the heading color."""
        try:
            fg = self._get_heading_fg()
            if fg == self._heading_fg and self._icon_sort_up:
                return
            self._heading_fg = fg
            self._icon_sort_up = BootstrapIcon("sort-up", 20, fg)
            self._icon_sort_down = BootstrapIcon("sort-down", 20, fg)
        except Exception:
            self._icon_sort_up = None
            self._icon_sort_down = None

    def _get_heading_fg(self) -> str:
        """Resolve a heading foreground color with light-biased fallbacks."""
        style = get_style()
        ttk_style = self._tree.cget('style')
        # Try configured value first
        return style.configure(f"{ttk_style}.Heading", 'foreground')

    def _update_heading_icons(self) -> None:
        """Apply sort direction icons to headings."""
        if not self._heading_texts:
            return
        self._load_heading_icons()
        for idx, text in enumerate(self._heading_texts):
            image = ""
            if idx < len(self._column_keys):
                key = self._column_keys[idx]
                state = self._sort_state.get(key)
                if state is True:
                    image = self._icon_sort_up if self._icon_sort_up else ""
                elif state is False:
                    image = self._icon_sort_down if self._icon_sort_down else ""
            self._tree.heading(idx, text=text, image=image)

    def _remember_page(self, page: int, records: list[dict]) -> None:
        if self._paging['cache_size'] <= 0:
            return
        # Move/update LRU cache
        if page in self._page_cache:
            self._page_cache.pop(page)
        self._page_cache[page] = records
        if len(self._page_cache) > self._paging['cache_size']:
            self._page_cache.popitem(last=False)

    def _focus_record(self, record_id) -> None:
        """Select and scroll to a record by id if it's on the current page."""
        try:
            rid = str(record_id)
            for iid, rec in self._row_map.items():
                if str(rec.get("id")) == rid:
                    self._tree.selection_set(iid)
                    self._tree.see(iid)
                    break
        except Exception:
            pass

    def _find_record_page(self, record_id) -> int | None:
        """Locate the page index containing the given record id, if available."""
        try:
            rid = str(record_id)
            total_pages = self._total_pages()
            for page_idx in range(total_pages):
                try:
                    rows = self._datasource.get_page(page_idx)
                except Exception:
                    break
                if any(str(rec.get("id")) == rid for rec in rows):
                    return page_idx
        except Exception:
            pass
        return None

    def _auto_size_columns(self, records: list[dict] | None = None) -> None:
        """Auto-size columns to the widest value among current rows/headings."""
        if not self._column_keys:
            return
        try:
            style = get_style()
            # Prefer the Treeview body font; fall back to TLabel/body or default
            tv_style = self._tree.cget("style") or "Treeview"
            body_font = (
                    style.lookup(tv_style, "font")
                    or style.lookup("TLabel", "font")
                    or getattr(style, "fonts", {}).get("body")
                    or "TkDefaultFont"
            )
            content_font = tkfont.nametofont(body_font)
        except Exception:
            content_font = None

        pad_px = 20

        # Gather samples from headings, provided records, and current tree values
        tree_samples = []
        for iid in self._tree.get_children(""):
            tree_samples.append(self._tree.item(iid, "values"))
            for ciid in self._tree.get_children(iid):
                tree_samples.append(self._tree.item(ciid, "values"))

        for idx, key in enumerate(self._column_keys):
            samples = []
            if idx < len(self._heading_texts):
                samples.append(str(self._heading_texts[idx]))
            if records:
                for rec in records:
                    samples.append(str(rec.get(key, "")))
            for vals in tree_samples:
                if idx < len(vals):
                    samples.append(str(vals[idx]))

            # Honor explicit column width if provided
            explicit_width = None
            if idx < len(self._column_defs):
                coldef = self._column_defs[idx]
                if isinstance(coldef, dict):
                    explicit_width = coldef.get("width")

            if explicit_width is not None:
                try:
                    self._tree.column(idx, width=explicit_width, minwidth=self._column_min_width)
                except Exception:
                    pass
                continue

            text = max(samples, key=len) if samples else ""
            if content_font:
                width = content_font.measure(text) + pad_px
            else:
                width = 0
            # Fallback to simple char-based estimate to avoid under-measuring
            char_estimate = len(text) * 10 + pad_px
            width = max(width, char_estimate, self._column_min_width)
            # Cap width to available viewport so we don't force the tree wider than its frame
            try:
                avail = max(0, int(self._tree.winfo_width()) - pad_px)
                if avail > 0:
                    width = min(width, avail)
            except Exception:
                pass
            try:
                self._tree.column(idx, width=width, minwidth=self._column_min_width)
            except Exception:
                pass

    def _apply_row_alternation(self) -> None:
        """Apply alternating row colors via a tag."""
        enabled = self._row_alternation.get('enabled', False)
        if not enabled or self._group_by_key:
            return
        bg, fg = self._resolve_alternating_row_color()
        try:
            self._tree.tag_configure("altrow", background=bg, foreground=fg)
            # Some themes honor the "striped" tag name; configure it too
            self._tree.tag_configure("striped", background=bg, foreground=fg)
        except Exception:
            return

        queue = list(self._tree.get_children(""))
        idx = 0
        while queue:
            iid = queue.pop(0)
            try:
                tags = list(self._tree.item(iid, "tags") or [])
                if idx % 2 == 1:
                    if "altrow" not in tags:
                        tags.append("altrow")
                    if "striped" not in tags:
                        tags.append("striped")
                else:
                    tags = [t for t in tags if t not in ("altrow", "striped")]
                self._tree.item(iid, tags=tags)
            except Exception:
                pass
            queue.extend(list(self._tree.get_children(iid)))
            idx += 1

    def _rebalance_grouped_widths(self) -> None:
        """Distribute available width across data columns when grouped so the left tree column is included."""
        # Only rebalance when grouping is active and xscroll is off (otherwise user can scroll)
        if not self._group_by_key or self._paging['xscroll']:
            return
        try:
            tree_width = max(0, int(self._tree.winfo_width()))
            group_width = max(0, int(self._tree.column("#0", option="width") or 0))
            vsb_width = 0
            if getattr(self, "_vsb", None):
                try:
                    self._vsb.update_idletasks()
                    if self._vsb.winfo_ismapped():
                        vsb_width = int(self._vsb.winfo_width())
                except Exception:
                    vsb_width = 0
            # Leave a small cushion to avoid oscillating scrollbar
            available = tree_width - group_width - vsb_width - 8
            if available <= 0:
                return
            cols = [c for c in self._display_columns if c < len(self._heading_texts)]
            if not cols:
                return
            width = max(self._column_min_width, available // len(cols))
            for c in cols:
                self._tree.column(c, width=width, stretch=True)
            # Keep the group column fixed so only data columns flex
            self._tree.column("#0", stretch=False)
        except Exception:
            pass

    def _on_tree_configure(self, _event=None) -> None:
        """Handle resize events to keep grouped layouts sized to the available width."""
        self._rebalance_grouped_widths()

    # ------------------------------------------------------------------ Export helpers
    def _export_all(self) -> None:
        try:
            rows = self._datasource.get_page_from_index(0, self._datasource.total_count())
            self._tree.event_generate("<<TableViewExportAll>>", data=rows)
        except Exception:
            pass

    def _export_selection(self) -> None:
        try:
            selected = [self._row_map[iid] for iid in self._tree.selection() if iid in self._row_map]
            self._tree.event_generate("<<TableViewExportSelection>>", data=selected)
        except Exception:
            pass

    def _export_page(self) -> None:
        try:
            start_index = self._current_page * self._paging['page_size']
            rows = self._datasource.get_page_from_index(start_index, self._paging['page_size'])
            self._tree.event_generate("<<TableViewExportPage>>", data=rows)
        except Exception:
            pass

    # ------------------------------------------------------------------ Header click handling
    def _on_header_click(self, event) -> None:
        """Handle left-click on headers for sorting."""
        region = self._tree.identify_region(event.x, event.y)
        if region != "heading":
            return

        if self._sorting == 'none':
            return

        col_id = self._tree.identify_column(event.x)  # e.g. "#1"
        try:
            display_idx = int(col_id.strip("#")) - 1
        except Exception:
            return

        if display_idx < 0 or display_idx >= len(self._display_columns):
            return

        column_idx = self._display_columns[display_idx]
        self._on_sort(column_idx)

    def _filter_header_column(self) -> None:
        """Show filter dialog for the currently selected header column."""
        col = self._header_menu_col
        if col is None or col >= len(self._column_keys):
            return
        self._show_column_filter_dialog(col)

    def _show_column_filter_dialog(self, column_idx: int) -> None:
        """Show FilterDialog with distinct values for the column."""
        from ttkbootstrap.dialogs.filterdialog import FilterDialog

        if column_idx >= len(self._column_keys):
            return

        key = self._column_keys[column_idx]
        heading_text = self._heading_texts[column_idx] if column_idx < len(self._heading_texts) else key

        # Get distinct values from datasource
        try:
            distinct_values = self._datasource.get_distinct_values(key)
        except Exception:
            distinct_values = []

        if not distinct_values:
            return

        empty_text = MessageCatalog.translate("table.empty")
        # Build items for the filter dialog
        current_filter = self._column_filters.get(key)
        items = []
        for val in distinct_values:
            display_text = str(val) if val is not None else empty_text
            selected = current_filter is None or val in current_filter
            items.append(
                {
                    "text": display_text,
                    "value": val,
                    "selected": selected
                })

        # Position dialog below the header
        col_id = f"#{self._display_columns.index(column_idx) + 1}" if column_idx in self._display_columns else "#1"
        pos_x = self._tree.winfo_rootx()
        pos_y = self._tree.winfo_rooty()

        tree_items = self._tree.get_children()
        if tree_items:
            bbox = self._tree.bbox(tree_items[0], col_id)
            if bbox:
                pos_x = self._tree.winfo_rootx() + bbox[0]
                pos_y = self._tree.winfo_rooty() + bbox[1] + 2

        dialog = FilterDialog(
            master=self.winfo_toplevel(),
            title=MessageCatalog.translate("table.filter_column", heading_text),
            items=items,
            allow_search=True,
            allow_select_all=True,
            frameless=True
        )

        result = dialog.show(position=(pos_x, pos_y))

        if result is not None:
            self._apply_column_filter(key, result, distinct_values)

    def _apply_column_filter(self, key: str, selected_values: list, all_values: list) -> None:
        """Apply column filter based on selected values."""
        # If all values selected, clear the filter for this column
        if set(selected_values) == set(all_values):
            self._column_filters.pop(key, None)
        else:
            self._column_filters[key] = selected_values

        # Build combined WHERE clause from all column filters
        self._rebuild_filter_where()

    def _rebuild_filter_where(self) -> None:
        """Rebuild WHERE clause from all active column filters."""
        clauses = []
        for key, values in self._column_filters.items():
            if not values:
                # No values selected = filter out everything
                clauses.append("1=0")
            else:
                quoted_key = self._quote_col(key)
                # Build IN clause
                quoted_values = []
                for v in values:
                    if v is None:
                        quoted_values.append("NULL")
                    else:
                        escaped = str(v).replace("'", "''")
                        quoted_values.append(f"'{escaped}'")
                # Handle NULL separately since IN doesn't work with NULL
                null_check = ""
                if None in values:
                    quoted_values = [qv for qv in quoted_values if qv != "NULL"]
                    null_check = f" OR {quoted_key} IS NULL"
                if quoted_values:
                    clauses.append(f"({quoted_key} IN ({','.join(quoted_values)}){null_check})")
                elif null_check:
                    clauses.append(f"({quoted_key} IS NULL)")

        where = " AND ".join(clauses) if clauses else ""
        try:
            self._datasource.set_filter(where)
        except Exception:
            pass
        self._clear_cache()
        self._load_page(0)
        self._update_status_labels()

    # ------------------------------------------------------------------ Context dispatch
    def _on_tree_context(self, event) -> None:
        if self._context_menus == "none":
            return
        region = self._tree.identify_region(event.x, event.y)
        if region == "heading":
            if not self._header_context_enabled():
                return
            self._on_header_context(event)
        else:
            if not self._row_context_enabled():
                return
            self._on_row_context(event)

    def _on_selection_event(self, _event=None) -> None:
        """Forward selection changes to subscribers."""
        rows = self.selected_rows
        self.event_generate("<<SelectionChange>>", data={"records": rows, "iids": list(self._tree.selection())})

    def _on_row_click_event(self, event) -> None:
        region = self._tree.identify_region(event.x, event.y)
        if region == "heading":
            return
        iid = self._tree.identify_row(event.y)
        if not iid:
            return
        rec = self._row_map.get(iid, {})
        self.event_generate("<<RowClick>>", data={"record": rec, "iid": iid})

    # ------------------------------------------------------------------ Header context menu
    def _ensure_header_menu(self) -> None:
        if not self._header_context_enabled():
            return
        if self._header_menu:
            return
        menu = ContextMenu(master=self, target=self._tree)
        menu.add_command(text="table.align_left", icon="align-start", command=self._align_header_left)
        menu.add_command(text="table.align_center", icon="align-center", command=self._align_header_center)
        menu.add_command(text="table.align_right", icon="align-end", command=self._align_header_right)
        menu.add_separator()
        menu.add_command(text="table.move_left", icon="arrow-left", command=self._move_header_left)
        menu.add_command(text="table.move_right", icon="arrow-right", command=self._move_header_right)
        menu.add_command(text="table.move_first", icon="arrow-bar-left", command=self._move_header_first)
        menu.add_command(text="table.move_last", icon="arrow-bar-right", command=self._move_header_last)
        menu.add_separator()
        menu.add_command(text="table.hide_column", icon="eye-slash", command=self._hide_header_column)
        menu.add_command(text="table.show_all", icon="eye", command=self._show_all_columns)
        if self._allow_grouping:
            menu.add_separator()
            menu.add_command(text="table.group_by_column", command=self._group_header_column)
            menu.add_command(text="table.ungroup_all", command=self._ungroup_all)
        menu.add_separator()
        menu.add_command(text="table.reset", icon="arrow-counterclockwise", command=self._reset_table)
        menu.add_separator()
        if not self._sorting == 'none':
            menu.add_command(text="table.clear_sort", icon="x-lg", command=self._clear_sort)
        self._header_menu = menu

    def _on_header_context(self, event) -> None:
        if not self._header_context_enabled():
            return
        # Only handle header clicks
        if self._tree.identify_region(event.x, event.y) != "heading":
            return
        col_id = self._tree.identify_column(event.x)  # e.g. "#1"
        try:
            idx = int(col_id.strip("#")) - 1
        except Exception:
            return
        if idx < 0 or idx >= len(self._display_columns):
            return
        self._header_menu_col = self._display_columns[idx]
        self._ensure_header_menu()

        # Try to position at bottom-left of the clicked header
        pos_x, pos_y = event.x_root, event.y_root
        items = self._tree.get_children()
        if items:
            bbox = self._tree.bbox(items[0], col_id)
            if bbox:
                # bbox is relative to the widget; bbox[1] is header height offset
                pos_x = self._tree.winfo_rootx() + bbox[0]
                pos_y = self._tree.winfo_rooty() + bbox[1] + 2
        self._header_menu.show(position=(pos_x, pos_y))

    def _align_header_left(self) -> None:
        self._set_heading_anchor("w")

    def _align_header_center(self) -> None:
        self._set_heading_anchor("center")

    def _align_header_right(self) -> None:
        self._set_heading_anchor("e")

    def _set_heading_anchor(self, anchor: str) -> None:
        """Align only the header text for the selected column."""
        col = self._header_menu_col
        if col is None:
            return
        self._tree.heading(col, anchor=anchor)
        self._tree.column(col, anchor=anchor)

    def _move_header_left(self) -> None:
        self._move_column(-1)

    def _move_header_right(self) -> None:
        self._move_column(1)

    def _move_header_first(self) -> None:
        self._move_column(to_index=0)

    def _move_header_last(self) -> None:
        self._move_column(to_index=len(self._display_columns) - 1)

    def _move_column(self, delta: int | None = None, to_index: int | None = None) -> None:
        col = self._header_menu_col
        if col is None or col not in self._display_columns:
            return
        current_pos = self._display_columns.index(col)
        if to_index is not None:
            new_pos = max(0, min(len(self._display_columns) - 1, to_index))
        else:
            new_pos = current_pos + (delta or 0)
        new_pos = max(0, min(len(self._display_columns) - 1, new_pos))
        if new_pos == current_pos:
            return
        self._display_columns.pop(current_pos)
        self._display_columns.insert(new_pos, col)
        self._tree.configure(displaycolumns=self._display_columns)

    def _hide_header_column(self) -> None:
        col = self._header_menu_col
        if col is None or col not in self._display_columns:
            return
        self._display_columns.remove(col)
        if not self._display_columns:
            self._display_columns = list(range(len(self._heading_texts)))
        self._tree.configure(displaycolumns=self._display_columns)

    def _show_all_columns(self) -> None:
        if not self._heading_texts:
            return
        self._display_columns = list(range(len(self._heading_texts)))
        self._tree.configure(displaycolumns=self._display_columns)

    def _show_column_chooser_dialog(self) -> None:
        """Show a dialog to select which columns are visible."""
        from ttkbootstrap.dialogs.filterdialog import FilterDialog

        if not self._heading_texts:
            return

        # Build items for the filter dialog
        items = []
        for idx, text in enumerate(self._heading_texts):
            items.append(
                {
                    "text": text,
                    "value": idx,
                    "selected": idx in self._display_columns
                })

        # Calculate position: align dialog's top-right to button's bottom-right
        btn = self._column_chooser_btn
        btn.update_idletasks()
        btn_right = btn.winfo_rootx() + btn.winfo_width()
        btn_bottom = btn.winfo_rooty() + btn.winfo_height()
        dialog_width = 250  # FilterDialog has fixed width of 250
        pos_x = btn_right - dialog_width - 2  # 2px west
        pos_y = btn_bottom + 2  # 2px south

        dialog = FilterDialog(
            master=self.winfo_toplevel(),
            title="Columns",
            items=items,
            allow_search=False,
            allow_select_all=True,
            frameless=True
        )

        result = dialog.show(position=(pos_x, pos_y))

        if result is not None:
            # Update display columns based on selection
            self._display_columns = [idx for idx in result if isinstance(idx, int)]
            if not self._display_columns:
                # Ensure at least one column is visible
                self._display_columns = list(range(len(self._heading_texts)))
            self._tree.configure(displaycolumns=self._display_columns)

    def _reset_table(self) -> None:
        # Reset sort, columns visibility/order, and reload first page
        self._display_columns = list(range(len(self._heading_texts)))
        self._tree.configure(displaycolumns=self._display_columns)
        self._clear_sort()

    # ------------------------------------------------------------------ Grouping
    def _group_header_column(self) -> None:
        """Group current view by the selected header column."""
        col = self._header_menu_col
        if col is None or col >= len(self._column_keys):
            return
        key = self._column_keys[col]
        quoted_key = self._quote_col(key)
        self._group_by_key = key
        self._group_parents.clear()
        # Sort entire datasource by the grouping column so grouping reflects full dataset order
        try:
            self._datasource.set_sort(f"{quoted_key} ASC")
        except Exception:
            pass
        self._sort_state = {key: True}
        self._clear_cache()
        self._update_heading_icons()
        # Restart at first page to reflect new ordering
        self._load_page(0)
        self._update_status_labels()

    def _ungroup_all(self) -> None:
        """Return to flat view."""
        if not self._group_by_key:
            return
        self._group_by_key = None
        self._group_parents.clear()
        self._apply_group_show_state(False)
        self._load_page(self._current_page)
        self._update_status_labels()

    def _apply_group_show_state(self, grouped: bool) -> None:
        """Toggle tree column visibility when grouping."""
        if grouped:
            self._tree.configure(show="tree headings")
            heading = "Group"
            try:
                if self._group_by_key and self._group_by_key in self._column_keys:
                    col_idx = self._column_keys.index(self._group_by_key)
                    heading = self._heading_texts[col_idx] if col_idx < len(self._heading_texts) else heading
            except Exception:
                pass
            self._tree.heading("#0", text=heading, anchor="w")
            # Fix the group column width so it stays visible even when space is tight
            self._tree.column("#0", width=200, minwidth=120, anchor="w", stretch=False)
            try:
                # Reset horizontal view so the group column is not scrolled out
                self._tree.xview_moveto(0)
            except Exception:
                pass
            self._rebalance_grouped_widths()
        else:
            self._tree.configure(show="headings")
            # Keep the tree column narrow/inert when unused
            self._tree.heading("#0", text="")
            self._tree.column("#0", width=0, minwidth=0, stretch=False)
            # Restore stretch behavior for data columns based on scroll mode
            try:
                stretch_cols = not self._paging['xscroll']
                for idx in range(len(self._heading_texts)):
                    self._tree.column(idx, stretch=stretch_cols)
            except Exception:
                pass

    def _render_flat(self, records: list[dict]) -> None:
        """Insert records as flat rows."""
        stripe = self._row_alternation.get('enabled', False) and not self._group_by_key
        for idx, rec in enumerate(records):
            values = [rec.get(k, "") for k in self._column_keys]
            tags = ("altrow",) if stripe and idx % 2 == 1 else ()
            iid = self._tree.insert("", "end", values=values, tags=tags)
            self._row_map[iid] = rec

    def _render_grouped(self, records: list[dict]) -> None:
        """Insert records under parent nodes for the active group."""
        key = self._group_by_key
        if not key or key not in self._column_keys:
            self._render_flat(records)
            return
        col_idx = self._column_keys.index(key)
        heading_text = self._heading_texts[col_idx] if col_idx < len(self._heading_texts) else key
        groups: OrderedDict[str | None, list[dict]] = OrderedDict()
        for rec in records:
            groups.setdefault(rec.get(key), []).append(rec)
        self._group_parents.clear()
        for val, items in groups.items():
            label_val = "(None)" if val is None else str(val)
            label = f"{heading_text}: {label_val} ({len(items)})"
            parent_iid = self._tree.insert("", "end", text=label, open=True)
            self._group_parents[val] = parent_iid
            for rec in items:
                values = [rec.get(k, "") for k in self._column_keys]
                iid = self._tree.insert(parent_iid, "end", values=values)
                self._row_map[iid] = rec

    def _clear_sort(self) -> None:
        self._sort_state.clear()
        self._datasource.set_sort("")
        self._clear_cache()
        self._update_heading_icons()
        self._load_page(0)
        self._update_status_labels()


# Backwards-compatible alias for the legacy Tableview name
Tableview = TableView
