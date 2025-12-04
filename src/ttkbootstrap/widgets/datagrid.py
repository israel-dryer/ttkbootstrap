"""
DataGrid widget backed by an in-memory SQLite datasource.

The datasource handles filtering, sorting, and pagination; the widget only
renders the current page in a Treeview.
"""

from __future__ import annotations

from collections import OrderedDict
from tkinter import Misc
import tkinter.ttk as ttk

from ttkbootstrap import use_style
from ttkbootstrap.datasource.sqlite_source import SqliteDataSource
from ttkbootstrap.widgets.button import Button
from ttkbootstrap.widgets.frame import Frame
from ttkbootstrap.widgets.label import Label
from ttkbootstrap.widgets.selectbox import SelectBox
from ttkbootstrap.widgets.scrollbar import Scrollbar
from ttkbootstrap.widgets.textentry import TextEntry
from ttkbootstrap.widgets.treeview import Treeview
from ttkbootstrap.widgets.separator import Separator
from ttkbootstrap.widgets.entry import Entry


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
        **kwargs,
    ):
        super().__init__(master, **kwargs)
        self._datasource = datasource or SqliteDataSource(":memory:", page_size=page_size)
        self._page_size = page_size
        self._virtual_scroll = virtual_scroll
        self._show_yscroll = show_yscroll
        self._show_xscroll = show_xscroll
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
        self._build_search_bar()
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

    def _build_search_bar(self) -> None:
        bar = Frame(self)
        bar.pack(fill="x", padx=4, pady=(0, 4))

        self._search_entry = TextEntry(bar)
        self._search_entry.pack(side="left", fill="x", expand=True, padx=(0, 6))
        self._search_entry.bind("<Return>", lambda e: self._run_search())

        self._search_mode = SelectBox(
            bar,
            items=["EQUALS", "CONTAINS", "STARTS WITH", "ENDS WITH", "SQL"],
            value="EQUALS",
            width=14,
            allow_custom_values=False,
            search_enabled=False,
        )
        self._search_mode.pack(side="left", padx=(0, 6))
        Button(bar, text="Clear", command=self._clear_search).pack(side="left", padx=(0, 4))

    def _build_tree(self) -> None:
        frame = Frame(self)
        frame.pack(fill="both", expand=True)

        cols = [self._col_text(c) for c in self._column_defs] or self._column_keys
        self._tree = Treeview(frame, columns=list(range(len(cols))), show="headings")
        self._tree.pack(side="left", fill="both", expand=True)

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
        for idx, text in enumerate(cols):
            self._heading_texts.append(text)
            self._tree.heading(idx, text=text, command=lambda c=idx: self._on_sort(c))
            self._tree.column(idx, anchor="w", width=120, stretch=True)
        self._update_heading_icons()

    def _build_pagination_bar(self) -> None:
        bar = Frame(self)
        bar.pack(fill="x", pady=(4, 0))
        Frame(bar).pack(side='left', fill='x', expand=True) # spacer
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
        Button(btn_frame, icon="chevron-double-left", bootstyle="ghost", icon_only=True, command=self._first_page).pack(side="left")
        Button(btn_frame, icon="chevron-left", icon_only=True, bootstyle="ghost", command=self._prev_page).pack(side="left")
        Button(btn_frame, icon="chevron-right", icon_only=True, bootstyle="ghost", command=self._next_page).pack(side="left")
        Button(btn_frame, icon="chevron-double-right", icon_only=True, bootstyle="ghost", command=self._last_page).pack(side="left")


    # ------------------------------------------------------------------ Helpers
    def _col_text(self, col) -> str:
        if isinstance(col, str):
            return col
        if isinstance(col, dict):
            return col.get("text") or col.get("key") or ""
        return str(col)

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
        if not self._column_keys and records:
            self._column_keys = list(records[0].keys())
        for rec in records:
            values = [rec.get(k, "") for k in self._column_keys]
            self._tree.insert("", "end", values=values)
    def _append_tree(self, records: list[dict]) -> None:
        for rec in records:
            values = [rec.get(k, "") for k in self._column_keys]
            self._tree.insert("", "end", values=values)

    def _total_pages(self) -> int:
        try:
            total = self._datasource.total_count()
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

    def _clear_search(self) -> None:
        self._search_entry.delete(0, 'end')
        try:
            self._datasource.set_filter("")
        except Exception:
            pass
        self._clear_cache()
        self._load_page(0)

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

    # ------------------------------------------------------------------ Cache helpers
    def _clear_cache(self) -> None:
        if self._page_cache:
            self._page_cache.clear()

    def _load_sort_icons(self) -> None:
        """Load and cache sort direction icons sized to match the heading color."""
        try:
            from ttkbootstrap.appconfig import use_icon_provider
            provider = use_icon_provider()
            fg = self._get_heading_fg()
            if fg == self._heading_fg and self._icon_sort_up and self._icon_sort_down:
                return
            self._heading_fg = fg
            self._icon_sort_up = provider("sort-alpha-up", 20, fg)
            self._icon_sort_down = provider("sort-alpha-down", 20, fg)
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
        """Apply sort icons to the current sort column, clear others."""
        if not self._heading_texts:
            return
        self._load_sort_icons()
        # Determine active sort column (single-column sort)
        active_key = None
        for key, state in self._sort_state.items():
            if state is not None:
                active_key = key
                break
        for idx, text in enumerate(self._heading_texts):
            image = ""
            if idx < len(self._column_keys) and active_key:
                key = self._column_keys[idx]
                state = self._sort_state.get(key) if key == active_key else None
                if state is True and self._icon_sort_up:
                    image = self._icon_sort_up
                elif state is False and self._icon_sort_down:
                    image = self._icon_sort_down
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
