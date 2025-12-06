"""
DataGrid widget backed by an in-memory SQLite datasource.

The datasource handles filtering, sorting, and pagination; the widget only
renders the current page in a Treeview.
"""

from __future__ import annotations

import logging
from collections import OrderedDict
from tkinter import Misc

from typing_extensions import Literal

from ttkbootstrap import use_style
from ttkbootstrap.datasource.sqlite_source import SqliteDataSource
from ttkbootstrap.widgets.button import Button
from ttkbootstrap.widgets.contextmenu import ContextMenu
from ttkbootstrap.widgets.dropdownbutton import DropdownButton
from ttkbootstrap.widgets.entry import Entry
from ttkbootstrap.widgets.frame import Frame
from ttkbootstrap.widgets.label import Label
from ttkbootstrap.widgets.scrollbar import Scrollbar
from ttkbootstrap.widgets.selectbox import SelectBox
from ttkbootstrap.widgets.separator import Separator
from ttkbootstrap.widgets.textentry import TextEntry
from ttkbootstrap.widgets.treeview import Treeview

logger = logging.getLogger(__name__)


class DataGrid(Frame):
    """
    Simple data grid that delegates filtering, sorting, and pagination to a
    SqliteDataSource (in-memory by default).
    """

    def __init__(
            self,
            master: Misc | None = None,
            columns: list[str | dict] | None = None,
            rows: list | None = None,
            datasource: SqliteDataSource | None = None,
            page_size: int = 250,
            virtual_scroll: bool = False,
            cache_size: int = 5,
            show_yscroll: bool = True,
            show_xscroll: bool = False,
            allow_header_sort: bool = True,
            show_table_status: bool = True,
            show_column_chooser: bool = True,
            show_searchbar: bool = True,
            searchbar_mode: Literal['standard', 'advanced'] = 'simple',
            allow_export: bool = False,
            export_options: list[str] | None = None,
            allow_edit: bool = False,
            form_options: dict | None = None,
            **kwargs,
    ):
        super().__init__(master, **kwargs)
        self._datasource = datasource or SqliteDataSource(":memory:", page_size=page_size)
        self._page_size = page_size
        self._virtual_scroll = virtual_scroll
        self._show_yscroll = show_yscroll
        self._show_xscroll = show_xscroll
        self._allow_header_sort = allow_header_sort
        self._show_table_status = show_table_status
        self._show_column_chooser = show_column_chooser
        self._show_searchbar = show_searchbar
        self._allow_export = allow_export
        self._export_options = export_options or ["all", "selection", "page"]
        self._allow_edit = allow_edit
        self._form_options = form_options or {}
        self._cache_size = max(0, cache_size)
        self._page_cache: OrderedDict[int, list[dict]] = OrderedDict()
        self._column_defs = columns or []
        self._column_keys: list[str] = []
        self._heading_texts: list[str] = []
        self._sort_state: dict[str, bool] = {}  # key -> ascending
        self._current_page = 0
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
        if self._show_searchbar:
            self._build_toolbar()
        self._build_tree()
        if not self._virtual_scroll:
            self._build_pagination_bar()

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

    # ------------------------------------------------------------------ UI
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

        self._search_entry = TextEntry(bar)
        self._search_entry.pack(side="left", fill="x", expand=True, padx=(0, 6))
        self._search_entry.on_enter(lambda _e: self._run_search())

        self._search_mode = SelectBox(
            bar,
            items=["EQUALS", "CONTAINS", "STARTS WITH", "ENDS WITH", "SQL"],
            value="EQUALS",
            width=14,
            allow_custom_values=False,
            search_enabled=False,
        )
        self._search_mode.pack(side="left", padx=(0, 6))
        Button(bar, text="Clear", bootstyle="ghost", command=self._clear_search).pack(side="left", padx=(0, 4))
        if self._allow_edit:
            Button(
                bar,
                icon="plus",
                icon_only=True,
                bootstyle="ghost",
                command=self._open_new_record,
            ).pack(side="left", padx=(0, 4))
        if self._allow_export:
            export_items = []
            if "all" in self._export_options:
                export_items.append({"type": "command", "text": "Export all", "command": self._export_all})
            if "selection" in self._export_options:
                export_items.append({"type": "command", "text": "Export selection", "command": self._export_selection})
            if "page" in self._export_options:
                export_items.append({"type": "command", "text": "Export page", "command": self._export_page})
            if not export_items:
                export_items.append({"type": "command", "text": "Export all", "command": self._export_all})
            DropdownButton(
                bar,
                icon="download",
                icon_only=True,
                bootstyle="ghost",
                compound="image",
                items=export_items,
                show_dropdown_button=False,
            ).pack(side="left")

        if self._show_column_chooser:
            self._column_chooser_btn = Button(
                bar,
                icon="layout-three-columns",
                icon_only=True,
                bootstyle="ghost",
                command=self._show_column_chooser_dialog,
            )
            self._column_chooser_btn.pack(side="left", padx=(4, 0))

    def _build_tree(self) -> None:
        frame = Frame(self)
        frame.pack(fill="both", expand=True)

        cols = [self._col_text(c) for c in self._column_defs] or self._column_keys
        self._tree = Treeview(frame, columns=list(range(len(cols))), show="headings")
        self._tree.pack(side="left", fill="both", expand=True, padx=3)
        self._display_columns = list(range(len(cols)))

        if self._show_yscroll:
            self._vsb = Scrollbar(frame, orient="vertical", command=self._tree.yview)
            self._vsb.pack(side="right", fill="y")
            if self._virtual_scroll:
                self._tree.configure(yscrollcommand=self._on_scroll)
            else:
                self._tree.configure(yscrollcommand=self._vsb.set)
        else:
            self._vsb = None

        if self._show_xscroll:
            self._hsb = Scrollbar(frame, orient="horizontal", command=self._tree.xview)
            self._hsb.pack(side="bottom", fill="x")
            self._tree.configure(xscrollcommand=self._hsb.set)
        else:
            self._hsb = None

        self._heading_texts = []
        self._column_anchors = []
        for idx, text in enumerate(cols):
            self._heading_texts.append(text)
            anchor = self._determine_anchor(idx)
            self._column_anchors.append(anchor)
            heading_kwargs = {"text": text, "anchor": anchor}
            # Don't use heading command - we'll handle clicks via Button-1 binding
            self._tree.heading(idx, **heading_kwargs)
            self._tree.column(idx, anchor=anchor, width=120, stretch=True)
        self._update_heading_icons()
        self._tree.bind("<Button-1>", self._on_header_click)
        self._tree.bind("<Button-3>", self._on_tree_context)
        if self._allow_edit:
            self._tree.bind("<Double-1>", self._on_row_double_click)

    def _build_pagination_bar(self) -> None:
        bar = Frame(self)
        bar.pack(fill="x", pady=(4, 0))
        status_frame = Frame(bar)
        status_frame.pack(side="left", fill="x", expand=True)
        self._filter_label = Label(status_frame, text="", anchor="w", bootstyle="secondary")
        self._filter_label.pack(side="left", padx=(0, 4))
        self._sort_label = Label(status_frame, text="", anchor="w", bootstyle="secondary")
        self._sort_label.pack(side="left", padx=(8, 4))
        if not self._show_table_status:
            status_frame.pack_forget()

        info_frame = Frame(bar)
        info_frame.pack(side='left')
        Label(info_frame, text='Page').pack(side='left')
        self._page_entry = Entry(info_frame, width=6, justify="center")
        self._page_entry.bind("<Return>", self._jump_page)
        self._page_entry.pack(side="left", padx=8)
        self._page_label = Label(info_frame, text="")
        self._page_label.pack(side="left", padx=(0, 8))

        sep = Separator(bar, orient="vertical")
        sep.pack(side="left", fill="y", padx=8)

        btn_frame = Frame(bar)
        btn_frame.pack(side="right")
        Button(btn_frame, icon="chevron-double-left", bootstyle="ghost", icon_only=True, command=self._first_page).pack(
            side="left")
        Button(btn_frame, icon="chevron-left", icon_only=True, bootstyle="ghost", command=self._prev_page).pack(
            side="left")
        Button(btn_frame, icon="chevron-right", icon_only=True, bootstyle="ghost", command=self._next_page).pack(
            side="left")
        Button(btn_frame, icon="chevron-double-right", icon_only=True, bootstyle="ghost", command=self._last_page).pack(
            side="left")

    # ------------------------------------------------------------------ Helpers
    def _col_text(self, col) -> str:
        if isinstance(col, str):
            return col
        if isinstance(col, dict):
            return col.get("text") or col.get("key") or ""
        return str(col)

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

    def _append_tree(self, records: list[dict]) -> None:
        # Grouped mode rebuilds the view instead of appending to keep hierarchy consistent
        if self._group_by_key:
            self._refresh_tree(records)
            return
        for rec in records:
            values = [rec.get(k, "") for k in self._column_keys]
            iid = self._tree.insert("", "end", values=values)
            self._row_map[iid] = rec

    def _total_pages(self) -> int:
        try:
            # Use cached count to avoid expensive COUNT(*) queries on every navigation
            if self._cached_total_count is None:
                self._cached_total_count = self._datasource.total_count()
            total = self._cached_total_count
            size = getattr(self._datasource, "page_size", self._page_size) or 1
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
            self._update_page_label()
        finally:
            self._loading_next = False

    def _update_page_label(self) -> None:
        if hasattr(self, "_page_entry"):
            self._page_entry.delete(0, 'end')
            self._page_entry.insert(0, str(self._current_page + 1))
        if hasattr(self, "_page_label"):
            self._page_label.configure(text=f"of {self._total_pages()}")
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
                self._virtual_scroll
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
        mode = self._search_mode.get()
        colnames = self._column_keys
        where = ""
        if text and colnames:
            crit = text.replace("'", "''")
            mode_upper = mode.upper().replace(" ", "_")
            if mode_upper == "CONTAINS":
                where = " OR ".join([f"{c} LIKE '%{crit}%'" for c in colnames])
            elif mode_upper == "STARTS_WITH":
                where = " OR ".join([f"{c} LIKE '{crit}%'" for c in colnames])
            elif mode_upper == "ENDS_WITH":
                where = " OR ".join([f"{c} LIKE '%{crit}'" for c in colnames])
            elif mode_upper == "SQL":
                where = text
            else:  # equals
                where = " OR ".join([f"{c} = '{crit}'" for c in colnames])
        try:
            self._datasource.set_filter(where)
        except Exception:
            pass
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
        asc = not self._sort_state.get(key, True)
        # Clear other sort states to keep single-column sort
        self._sort_state = {key: asc}
        order = "ASC" if asc else "DESC"
        try:
            self._datasource.set_sort(f"{key} {order}")
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
                filter_txt = f"Filter: {where}"
        except Exception:
            pass
        # Sort
        sort_txt = ""
        try:
            order = getattr(self._datasource, "_order_by", "")
            if order:
                sort_txt = f"Sort: {order}"
        except Exception:
            pass
        group_txt = ""
        if self._group_by_key:
            try:
                col_idx = self._column_keys.index(self._group_by_key)
                heading_text = self._heading_texts[col_idx] if col_idx < len(self._heading_texts) else self._group_by_key
            except Exception:
                heading_text = self._group_by_key
            group_txt = f"Group: {heading_text}"

        if hasattr(self, "_filter_label"):
            self._filter_label.configure(text=filter_txt)
        if hasattr(self, "_sort_label"):
            joined = " | ".join([t for t in (sort_txt, group_txt) if t])
            self._sort_label.configure(text=joined)

    # ------------------------------------------------------------------ Row context menu
    def _ensure_row_menu(self) -> None:
        if self._row_menu:
            return
        menu = ContextMenu(master=self, target=self._tree)
        menu.add_command(text="Sort Ascending", command=lambda: self._sort_selection(True))
        menu.add_command(text="Sort Descending", command=lambda: self._sort_selection(False))
        menu.add_separator()
        menu.add_command(text="Filter by Value", command=self._filter_by_value)
        menu.add_command(text="Clear Filter", command=self._clear_filter_cmd)
        menu.add_separator()
        menu.add_command(text="Move Up", command=self._move_row_up)
        menu.add_command(text="Move Down", command=self._move_row_down)
        menu.add_command(text="Move to Top", command=self._move_row_top)
        menu.add_command(text="Move to Bottom", command=self._move_row_bottom)
        menu.add_separator()
        menu.add_command(text="Hide Selection", command=self._hide_selection)
        menu.add_command(text="Delete Selection", command=self._delete_selection)
        self._row_menu = menu

    def _on_row_context(self, event) -> None:
        iid = self._tree.identify_row(event.y)
        col_id = self._tree.identify_column(event.x)
        try:
            col_idx = int(col_id.strip("#")) - 1
        except Exception:
            col_idx = 0
        if iid:
            if iid not in self._tree.selection():
                self._tree.selection_set(iid)
        if not self._tree.selection():
            return
        self._row_menu_col = col_idx
        self._ensure_row_menu()
        self._row_menu.show(position=(event.x_root, event.y_root))

    def _on_row_double_click(self, event) -> None:
        if not self._allow_edit:
            return
        region = self._tree.identify_region(event.x, event.y)
        if region == "heading":
            return
        iid = self._tree.identify_row(event.y)
        if not iid:
            return
        rec = self._row_map.get(iid, {})
        self._open_form_dialog(rec)

    def _open_new_record(self) -> None:
        if not self._allow_edit:
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

        form_options = dict(self._form_options)
        form_options.setdefault('col_count', 2)
        form_options.setdefault('min_col_width', 260)
        form_options.setdefault('scrollable', True)
        form_options.setdefault('resizable', True)
        form_options.setdefault('buttons', ["Cancel", "Save"])

        dialog = FormDialog(
            master=dialog_master,
            title="Edit Record" if record else "New Record",
            data=initial_data,
            items=form_items,
            col_count=form_options.get('col_count', 2),
            min_col_width=form_options.get('min_col_width', 260),
            scrollable=form_options.get('scrollable', True),
            buttons=form_options.get('buttons'),
            resizable=(True, True) if form_options.get('resizable', True) else (False, False),
        )

        dialog.show_centered()
        data = dialog.result

        if data is None:
            return

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
        values = self._tree.item(iid, "values")
        if col_idx >= len(values):
            return
        val = values[col_idx]
        crit = str(val).replace("'", "''")
        where = f"{key} = '{crit}'"
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
        self._sort_state = {key: ascending}
        order = "ASC" if ascending else "DESC"
        try:
            self._datasource.set_sort(f"{key} {order}")
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

    def _move_row_absolute(self, new_idx: int) -> None:
        sel = list(self._tree.selection())
        if not sel:
            return
        target_iid = sel[0]
        children = list(self._tree.get_children())
        new_idx = max(0, min(len(children) - 1, new_idx))
        self._tree.move(target_iid, "", new_idx)

    def _hide_selection(self) -> None:
        sel = list(self._tree.selection())
        for iid in sel:
            self._tree.delete(iid)
            self._row_map.pop(iid, None)

    def _delete_selection(self) -> None:
        sel = list(self._tree.selection())
        changed = False
        for iid in sel:
            rec = self._row_map.get(iid) or {}
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

    # ------------------------------------------------------------------ Cache helpers
    def _clear_cache(self) -> None:
        if self._page_cache:
            self._page_cache.clear()
        # Invalidate total count cache when data/filter/sort changes
        self._cached_total_count = None

    def _load_heading_icons(self) -> None:
        """Load and cache heading icons (sort arrows) sized to match the heading color."""
        try:
            from ttkbootstrap.appconfig import use_icon_provider
            provider = use_icon_provider()
            fg = self._get_heading_fg()
            if fg == self._heading_fg and self._icon_sort_up:
                return
            self._heading_fg = fg
            self._icon_sort_up = provider("sort-up", 20, fg)
            self._icon_sort_down = provider("sort-down", 20, fg)
        except Exception:
            self._icon_sort_up = None
            self._icon_sort_down = None

    def _get_heading_fg(self) -> str:
        """Resolve a heading foreground color with light-biased fallbacks."""
        style = use_style()
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
        if self._cache_size <= 0:
            return
        # Move/update LRU cache
        if page in self._page_cache:
            self._page_cache.pop(page)
        self._page_cache[page] = records
        if len(self._page_cache) > self._cache_size:
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

    # ------------------------------------------------------------------ Export helpers
    def _export_all(self) -> None:
        try:
            rows = self._datasource.get_page_from_index(0, self._datasource.total_count())
            self._tree.event_generate("<<DataGridExportAll>>", data=rows)
        except Exception:
            pass

    def _export_selection(self) -> None:
        try:
            selected = [self._row_map[iid] for iid in self._tree.selection() if iid in self._row_map]
            self._tree.event_generate("<<DataGridExportSelection>>", data=selected)
        except Exception:
            pass

    def _export_page(self) -> None:
        try:
            start_index = self._current_page * self._page_size
            rows = self._datasource.get_page_from_index(start_index, self._page_size)
            self._tree.event_generate("<<DataGridExportPage>>", data=rows)
        except Exception:
            pass

    # ------------------------------------------------------------------ Header click handling
    def _on_header_click(self, event) -> None:
        """Handle left-click on headers for sorting."""
        region = self._tree.identify_region(event.x, event.y)
        if region != "heading":
            return

        if not self._allow_header_sort:
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

        # Build items for the filter dialog
        current_filter = self._column_filters.get(key)
        items = []
        for val in distinct_values:
            display_text = str(val) if val is not None else "(empty)"
            selected = current_filter is None or val in current_filter
            items.append({
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
            title=f"Filter: {heading_text}",
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
                    null_check = f" OR {key} IS NULL"
                if quoted_values:
                    clauses.append(f"({key} IN ({','.join(quoted_values)}){null_check})")
                elif null_check:
                    clauses.append(f"({key} IS NULL)")

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
        region = self._tree.identify_region(event.x, event.y)
        if region == "heading":
            self._on_header_context(event)
        else:
            self._on_row_context(event)

    # ------------------------------------------------------------------ Header context menu
    def _ensure_header_menu(self) -> None:
        if self._header_menu:
            return
        menu = ContextMenu(master=self, target=self._tree)
        menu.add_command(text="Filter", icon="filter", command=self._filter_header_column)
        menu.add_command(text="Clear Filter", icon="x-lg", command=self._clear_filter_cmd)
        menu.add_separator()
        menu.add_command(text="Align Left", icon="align-start", command=self._align_header_left)
        menu.add_command(text="Align Center", icon="align-center", command=self._align_header_center)
        menu.add_command(text="Align Right", icon="align-end", command=self._align_header_right)
        menu.add_separator()
        menu.add_command(text="Move Left", icon="arrow-left", command=self._move_header_left)
        menu.add_command(text="Move Right", icon="arrow-right", command=self._move_header_right)
        menu.add_command(text="Move First", icon="arrow-bar-left", command=self._move_header_first)
        menu.add_command(text="Move Last", icon="arrow-bar-right", command=self._move_header_last)
        menu.add_separator()
        menu.add_command(text="Hide Column", icon="eye-slash", command=self._hide_header_column)
        menu.add_command(text="Show All", icon="eye", command=self._show_all_columns)
        menu.add_separator()
        menu.add_command(text="Clear Sort", icon="x-lg", command=self._clear_sort)
        menu.add_separator()
        menu.add_command(text="Group by This Column", command=self._group_header_column)
        menu.add_command(text="Ungroup All", command=self._ungroup_all)
        menu.add_separator()
        menu.add_command(text="Reset Table", icon="arrow-counterclockwise", command=self._reset_table)
        self._header_menu = menu

    def _on_header_context(self, event) -> None:
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
            items.append({
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
        self._group_by_key = key
        self._group_parents.clear()
        # Sort entire datasource by the grouping column so grouping reflects full dataset order
        try:
            self._datasource.set_sort(f"{key} ASC")
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
            self._tree.column("#0", width=200, anchor="w", stretch=True)
        else:
            self._tree.configure(show="headings")
            # Keep the tree column narrow/inert when unused
            self._tree.heading("#0", text="")
            self._tree.column("#0", width=0, minwidth=0, stretch=False)

    def _render_flat(self, records: list[dict]) -> None:
        """Insert records as flat rows."""
        for rec in records:
            values = [rec.get(k, "") for k in self._column_keys]
            iid = self._tree.insert("", "end", values=values)
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
