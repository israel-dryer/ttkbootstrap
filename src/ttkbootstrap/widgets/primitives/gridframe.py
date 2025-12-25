from __future__ import annotations

import tkinter as tk
from typing import Literal, Optional, Any, Union

from ttkbootstrap.widgets.primitives.frame import Frame
from ttkbootstrap.widgets.types import Master

Direction = Literal["vertical", "horizontal", "row", "column", "row-reverse", "column-reverse"]
Fill = Literal["none", "x", "y", "both"]
Side = Literal["top", "bottom", "left", "right"]
Anchor = Literal["n", "ne", "e", "se", "s", "sw", "w", "nw", "center"]
Sticky = Literal["n", "s", "e", "w", "ns", "ew", "nsew", "ne", "nw", "se", "sw", "nse", "nsw", "new", "sew", ""]
AutoFlow = Literal["row", "column", "row-dense", "column-dense", "none"]
Gap = Union[int, tuple[int, int]]


def _parse_size(value: Union[int, str]) -> tuple[int, int]:
    """Parse size value into (weight, minsize) tuple."""
    if isinstance(value, int):
        return value, 0
    if isinstance(value, str):
        if value == "auto":
            return 0, 0
        if value.endswith("px"):
            try:
                return 0, int(value[:-2])
            except ValueError:
                return 0, 0
    return 0, 0


class GridFrame(Frame):
    """A Frame with simplified grid-based layout management and auto-placement.

    GridFrame extends the ttkbootstrap Frame with automatic grid-based
    layout management, including support for row/column definitions,
    gap spacing, auto-placement, and default sticky behavior.

    Args:
        master: Parent widget. If None, uses the default root window.
        rows: Number of rows (int) or list of row size specs.
            Size specs can be int (weight) or str ("auto", "100px").
        columns: Number of columns (int) or list of column size specs.
        gap: Spacing between cells. Int for uniform, tuple for (column, row).
        sticky: Default sticky value for children.
        propagate: Whether the frame should resize to fit its contents.
        auto_flow: Auto-placement mode ("row", "column", "row-dense", "column-dense", "none").
        **kwargs: Additional Frame options (bootstyle, padding, etc.).
    """

    def __init__(
        self,
        master: Master = None,
        *,
        rows: Optional[Union[int, list[Union[int, str]]]] = None,
        columns: Optional[Union[int, list[Union[int, str]]]] = None,
        gap: Gap = 0,
        sticky: Optional[Sticky] = None,
        propagate: Optional[bool] = None,
        auto_flow: AutoFlow = "row",
        **kwargs: Any,
    ) -> None:
        super().__init__(master, **kwargs)

        self._gap = self._normalize_gap(gap)
        self._default_sticky = sticky
        self._auto_flow = auto_flow

        # Track managed widgets: list of (widget, user_options, computed_position)
        # computed_position is (row, col, rowspan, colspan)
        self._managed: list[tuple[tk.Widget, dict[str, Any], tuple[int, int, int, int]]] = []

        # Track occupied cells for auto-placement
        self._occupied: set[tuple[int, int]] = set()

        # Auto-placement cursor
        self._next_row = 0
        self._next_col = 0

        # Parse and store row/column definitions
        self._row_defs: list[tuple[int, int]] = []
        self._col_defs: list[tuple[int, int]] = []

        if isinstance(rows, int):
            self._row_defs = [(1, 0)] * rows
        elif isinstance(rows, list):
            self._row_defs = [_parse_size(r) for r in rows]

        if isinstance(columns, int):
            self._col_defs = [(1, 0)] * columns
        elif isinstance(columns, list):
            self._col_defs = [_parse_size(c) for c in columns]

        # Apply initial row/column configuration
        for i, (weight, minsize) in enumerate(self._row_defs):
            self.rowconfigure(i, weight=weight, minsize=minsize)
        for i, (weight, minsize) in enumerate(self._col_defs):
            self.columnconfigure(i, weight=weight, minsize=minsize)

        if propagate is not None:
            self.grid_propagate(propagate)

    @staticmethod
    def _normalize_gap(gap: Gap) -> tuple[int, int]:
        """Normalize gap to (column_gap, row_gap) tuple."""
        if isinstance(gap, int):
            return gap, gap
        return gap

    @property
    def column_gap(self) -> int:
        return self._gap[0]

    @property
    def row_gap(self) -> int:
        return self._gap[1]

    @property
    def num_columns(self) -> int:
        """Number of defined columns, or a large default for auto-placement."""
        return len(self._col_defs) if self._col_defs else 100

    @property
    def num_rows(self) -> int:
        """Number of defined rows, or a large default for auto-placement."""
        return len(self._row_defs) if self._row_defs else 100

    @property
    def children(self) -> list[tk.Widget]:
        """Return list of managed widgets in order."""
        return [w for w, _, _ in self._managed]

    def _is_area_free(self, row: int, col: int, rowspan: int, colspan: int) -> bool:
        """Check if a rectangular area is free."""
        return all(
            (row + dr, col + dc) not in self._occupied
            for dr in range(rowspan)
            for dc in range(colspan)
        )

    def _occupy_area(self, row: int, col: int, rowspan: int, colspan: int) -> None:
        """Mark a rectangular area as occupied."""
        for dr in range(rowspan):
            for dc in range(colspan):
                self._occupied.add((row + dr, col + dc))

    def _free_area(self, row: int, col: int, rowspan: int, colspan: int) -> None:
        """Mark a rectangular area as free."""
        for dr in range(rowspan):
            for dc in range(colspan):
                self._occupied.discard((row + dr, col + dc))

    def _find_next_position(self, rowspan: int = 1, colspan: int = 1) -> tuple[int, int]:
        """Find the next available position using auto-flow rules."""
        if self._auto_flow == "none":
            return 0, 0

        max_cols = self.num_columns
        max_rows = self.num_rows

        if "dense" in self._auto_flow:
            # Dense packing: search from (0,0)
            if self._auto_flow == "row-dense":
                for r in range(max_rows):
                    for c in range(max_cols - colspan + 1):
                        if self._is_area_free(r, c, rowspan, colspan):
                            return r, c
            else:  # column-dense
                for c in range(max_cols):
                    for r in range(max_rows - rowspan + 1):
                        if self._is_area_free(r, c, rowspan, colspan):
                            return r, c
        else:
            # Normal flow: continue from cursor
            if self._auto_flow == "row":
                r, c = self._next_row, self._next_col
                while r < max_rows:
                    while c <= max_cols - colspan:
                        if self._is_area_free(r, c, rowspan, colspan):
                            # Update cursor for next placement
                            next_c = c + colspan
                            if self._col_defs and next_c >= len(self._col_defs):
                                self._next_row = r + 1
                                self._next_col = 0
                            else:
                                self._next_row = r
                                self._next_col = next_c
                            return r, c
                        c += 1
                    r += 1
                    c = 0
            else:  # column
                r, c = self._next_row, self._next_col
                while c < max_cols:
                    while r <= max_rows - rowspan:
                        if self._is_area_free(r, c, rowspan, colspan):
                            # Update cursor for next placement
                            next_r = r + rowspan
                            if self._row_defs and next_r >= len(self._row_defs):
                                self._next_col = c + 1
                                self._next_row = 0
                            else:
                                self._next_col = c
                                self._next_row = next_r
                            return r, c
                        r += 1
                    c += 1
                    r = 0

        return 0, 0  # Fallback

    def _compute_gap_padding(
        self, row: int, col: int, user_padx: Any = None, user_pady: Any = None
    ) -> dict[str, Any]:
        """Compute padding that includes gap for non-first rows/columns."""
        result: dict[str, Any] = {}

        # Handle column gap (padx)
        if col > 0 and self.column_gap:
            gap_padx = (self.column_gap, 0)
            if user_padx is not None:
                result["padx"] = self._merge_padding(gap_padx, user_padx)
            else:
                result["padx"] = gap_padx
        elif user_padx is not None:
            result["padx"] = user_padx

        # Handle row gap (pady)
        if row > 0 and self.row_gap:
            gap_pady = (self.row_gap, 0)
            if user_pady is not None:
                result["pady"] = self._merge_padding(gap_pady, user_pady)
            else:
                result["pady"] = gap_pady
        elif user_pady is not None:
            result["pady"] = user_pady

        return result

    @staticmethod
    def _merge_padding(
        gap_pad: tuple[int, int], user_pad: Any
    ) -> tuple[int, int]:
        """Merge gap padding with user padding."""
        if isinstance(user_pad, int):
            return (gap_pad[0] + user_pad, user_pad)
        elif isinstance(user_pad, (tuple, list)) and len(user_pad) == 2:
            return (gap_pad[0] + user_pad[0], user_pad[1])
        return gap_pad

    def _build_options(
        self,
        row: int,
        col: int,
        rowspan: int,
        colspan: int,
        user_options: dict[str, Any],
    ) -> dict[str, Any]:
        """Build final grid options."""
        options: dict[str, Any] = {
            "in_": self,
            "row": row,
            "column": col,
        }

        if rowspan > 1:
            options["rowspan"] = rowspan
        if colspan > 1:
            options["columnspan"] = colspan

        # Apply gap padding
        gap_padding = self._compute_gap_padding(
            row, col,
            user_options.get("padx"),
            user_options.get("pady")
        )
        options.update(gap_padding)

        # Apply default sticky
        if self._default_sticky and "sticky" not in user_options:
            options["sticky"] = self._default_sticky

        # User options override (except padx/pady which we handled)
        for key, value in user_options.items():
            if key not in ("padx", "pady", "row", "column"):
                options[key] = value

        return options

    def _regrid_all(self) -> None:
        """Remove and re-grid all widgets."""
        # Ungrid all
        for widget, _, _ in self._managed:
            widget.grid_forget()

        # Clear and rebuild occupied set
        self._occupied.clear()
        self._next_row = 0
        self._next_col = 0

        # Regrid in order, recalculating positions
        new_managed: list[tuple[tk.Widget, dict[str, Any], tuple[int, int, int, int]]] = []

        for widget, user_options, _ in self._managed:
            rowspan = int(user_options.get("rowspan", 1))
            colspan = int(user_options.get("columnspan", 1))

            # Check if user specified explicit position
            explicit_row = user_options.get("row")
            explicit_col = user_options.get("column")

            if explicit_row is not None and explicit_col is not None:
                row, col = int(explicit_row), int(explicit_col)
            else:
                row, col = self._find_next_position(rowspan, colspan)

            self._occupy_area(row, col, rowspan, colspan)
            options = self._build_options(row, col, rowspan, colspan, user_options)
            widget.grid(**options)
            new_managed.append((widget, user_options, (row, col, rowspan, colspan)))

        self._managed = new_managed

    def _find_index(self, widget: tk.Widget) -> int:
        """Find index of widget, raise ValueError if not found."""
        for i, (w, _, _) in enumerate(self._managed):
            if w is widget:
                return i
        raise ValueError(f"Widget {widget} is not managed by this GridFrame")

    def add(
        self,
        widget: tk.Widget,
        *,
        row: Optional[int] = None,
        column: Optional[int] = None,
        rowspan: int = 1,
        columnspan: int = 1,
        **options: Any,
    ) -> tk.Widget:
        """
        Add a widget to the grid.

        If row/column are not specified, auto-placement is used.

        Args:
            widget: The widget to add
            row: Row index (auto if None)
            column: Column index (auto if None)
            rowspan: Number of rows to span
            columnspan: Number of columns to span
            **options: Additional grid options (sticky, padx, pady, ipadx, ipady)

        Returns:
            The widget (for chaining)
        """
        user_options: dict[str, Any] = {**options}
        if row is not None:
            user_options["row"] = row
        if column is not None:
            user_options["column"] = column
        if rowspan != 1:
            user_options["rowspan"] = rowspan
        if columnspan != 1:
            user_options["columnspan"] = columnspan

        # Determine position
        if row is not None and column is not None:
            final_row, final_col = row, column
        else:
            final_row, final_col = self._find_next_position(rowspan, columnspan)

        # Occupy and grid
        self._occupy_area(final_row, final_col, rowspan, columnspan)
        grid_options = self._build_options(final_row, final_col, rowspan, columnspan, user_options)
        widget.grid(**grid_options)

        self._managed.append((widget, user_options, (final_row, final_col, rowspan, columnspan)))
        return widget

    def insert(self, index: int, widget: tk.Widget, **options: Any) -> tk.Widget:
        """
        Insert a widget at a specific index in the managed list.

        The widget will be placed using auto-placement rules relative to
        its position in the list.

        Args:
            index: Position in managed list
            widget: The widget to insert
            **options: Grid options

        Returns:
            The widget (for chaining)
        """
        index = max(0, min(index, len(self._managed)))
        # Temporary position, will be recalculated
        self._managed.insert(index, (widget, options, (0, 0, 1, 1)))
        self._regrid_all()
        return widget

    def remove(self, widget: tk.Widget) -> None:
        """
        Remove a widget from the grid.

        The widget is ungridded but not destroyed.
        """
        index = self._find_index(widget)
        _, _, (row, col, rowspan, colspan) = self._managed[index]

        widget.grid_forget()
        self._free_area(row, col, rowspan, colspan)
        self._managed.pop(index)

    def move(self, widget: tk.Widget, new_index: int) -> None:
        """
        Move a widget to a new position in the managed list.

        This affects auto-placement order.
        """
        old_index = self._find_index(widget)
        entry = self._managed.pop(old_index)
        new_index = max(0, min(new_index, len(self._managed)))
        self._managed.insert(new_index, entry)
        self._regrid_all()

    def move_to(
        self,
        widget: tk.Widget,
        row: int,
        column: int,
        rowspan: Optional[int] = None,
        columnspan: Optional[int] = None,
    ) -> None:
        """
        Move a widget to a specific grid position.

        Args:
            widget: The widget to move
            row: New row
            column: New column
            rowspan: New rowspan (keeps current if None)
            columnspan: New columnspan (keeps current if None)
        """
        index = self._find_index(widget)
        _, user_options, (_, _, old_rowspan, old_colspan) = self._managed[index]

        # Update options with new position
        new_options = {**user_options, "row": row, "column": column}
        if rowspan is not None:
            new_options["rowspan"] = rowspan
        if columnspan is not None:
            new_options["columnspan"] = columnspan

        self._managed[index] = (widget, new_options, (0, 0, 1, 1))  # Temp position
        self._regrid_all()

    def update_options(self, widget: tk.Widget, **options: Any) -> None:
        """
        Update grid options for a widget.

        Args:
            widget: The widget to update
            **options: New grid options (merged with existing)
        """
        index = self._find_index(widget)
        _, current_options, position = self._managed[index]
        new_options = {**current_options, **options}
        self._managed[index] = (widget, new_options, position)
        self._regrid_all()

    def configure_row(
        self,
        index: int,
        weight: int = 1,
        minsize: Optional[int] = None,
        pad: Optional[int] = None,
    ) -> None:
        """Configure a row's properties."""
        kwargs: dict[str, Any] = {"weight": weight}
        if minsize is not None:
            kwargs["minsize"] = minsize
        if pad is not None:
            kwargs["pad"] = pad
        self.rowconfigure(index, **kwargs)

    def configure_column(
        self,
        index: int,
        weight: int = 1,
        minsize: Optional[int] = None,
        pad: Optional[int] = None,
    ) -> None:
        """Configure a column's properties."""
        kwargs: dict[str, Any] = {"weight": weight}
        if minsize is not None:
            kwargs["minsize"] = minsize
        if pad is not None:
            kwargs["pad"] = pad
        self.columnconfigure(index, **kwargs)

    def clear(self) -> None:
        """Remove all widgets (ungrids but doesn't destroy them)."""
        for widget, _, _ in self._managed:
            widget.grid_forget()
        self._managed.clear()
        self._occupied.clear()
        self._next_row = 0
        self._next_col = 0

    def get_position(self, widget: tk.Widget) -> tuple[int, int, int, int]:
        """Get the current (row, column, rowspan, colspan) of a widget."""
        index = self._find_index(widget)
        return self._managed[index][2]

    def index_of(self, widget: tk.Widget) -> int:
        """Get the index of a widget in the managed list."""
        return self._find_index(widget)

    def __len__(self) -> int:
        return len(self._managed)

    def __iter__(self):
        return iter(self.children)