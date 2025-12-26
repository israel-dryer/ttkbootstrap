from __future__ import annotations

from typing import Any


class GridMixin:
    """Grid geometry manager helpers (grid).

    Tk’s `grid` geometry manager arranges widgets in a table of rows and columns.

    In ttkbootstrap v2 you may prefer higher-level layout containers (e.g. `GridFrame`)
    for most UI layout. This mixin documents the underlying Tkinter `grid_*` API
    as an escape hatch and for interoperability with existing Tk code.

    Notes:
        - `grid()` attaches a widget to a parent container that is using grid.
        - `rowconfigure()` / `columnconfigure()` set sizing behavior (weight/minsize/pad).
        - `grid_propagate(False)` prevents a container from resizing to fit its children.
    """

    # -------------------------------------------------------------------------
    # Core widget methods
    # -------------------------------------------------------------------------

    def grid(self, cnf: dict[str, Any] | None = None, **kw: Any) -> None:
        """Position this widget using the grid geometry manager.

        Args:
            cnf: Optional dict of grid options.
            **kw: Grid options. Common options include:
                - row, column: Cell coordinates (0-based).
                - rowspan, columnspan: Span across multiple cells.
                - sticky: How the widget expands within its cell (e.g. "nsew").
                - padx, pady: External padding around the widget.
                - ipadx, ipady: Internal padding inside the widget.
        """
        if cnf is None:
            return super().grid(**kw)  # type: ignore[misc]
        return super().grid(cnf, **kw)  # type: ignore[misc]

    def grid_configure(self, cnf: dict[str, Any] | None = None, **kw: Any) -> None:
        """Alias for `grid()`.

        Args:
            cnf: Optional dict of grid options.
            **kw: Grid options (see `grid`).
        """
        if cnf is None:
            return super().grid_configure(**kw)  # type: ignore[misc]
        return super().grid_configure(cnf, **kw)  # type: ignore[misc]

    def grid_forget(self) -> None:
        """Unmap this widget and forget its grid configuration.

        The widget is removed from the layout, and its previous grid options
        are discarded.
        """
        return super().grid_forget()  # type: ignore[misc]

    def grid_remove(self) -> None:
        """Unmap this widget but remember its grid configuration.

        Use `grid()` with no args to restore it to its previous grid location.
        """
        return super().grid_remove()  # type: ignore[misc]

    def grid_info(self) -> dict[str, Any]:
        """Return this widget's current grid configuration.

        Returns:
            A dict containing the current grid options for this widget
            (row, column, sticky, padx, pady, etc.).
        """
        return super().grid_info()  # type: ignore[misc]

    # -------------------------------------------------------------------------
    # Container methods (applied to the grid parent container)
    # -------------------------------------------------------------------------

    def grid_propagate(self, flag: bool | None = None) -> bool | None:
        """Get or set grid geometry propagation for this container.

        When propagation is enabled (default), the container may resize itself
        to fit the size requests of its children.

        Args:
            flag: True/False to enable/disable propagation. If None, acts as a getter.

        Returns:
            When queried, returns the current propagation flag. When set, returns None.
        """
        return super().grid_propagate(flag)  # type: ignore[misc]

    def grid_rowconfigure(self, index: int, cnf: dict[str, Any] | None = None, **kw: Any) -> None:
        """Configure sizing behavior for a grid row in this container.

        Common options:
            - weight: How extra space is distributed (0 means no expansion).
            - minsize: Minimum row size in pixels.
            - pad: Extra padding added to the row.

        Args:
            index: Row index (0-based).
            cnf: Optional dict of configuration options.
            **kw: Row configuration options.
        """
        if cnf is None:
            return super().grid_rowconfigure(index, **kw)  # type: ignore[misc]
        return super().grid_rowconfigure(index, cnf, **kw)  # type: ignore[misc]

    def grid_columnconfigure(self, index: int, cnf: dict[str, Any] | None = None, **kw: Any) -> None:
        """Configure sizing behavior for a grid column in this container.

        Common options:
            - weight: How extra space is distributed (0 means no expansion).
            - minsize: Minimum column size in pixels.
            - pad: Extra padding added to the column.

        Args:
            index: Column index (0-based).
            cnf: Optional dict of configuration options.
            **kw: Column configuration options.
        """
        if cnf is None:
            return super().grid_columnconfigure(index, **kw)  # type: ignore[misc]
        return super().grid_columnconfigure(index, cnf, **kw)  # type: ignore[misc]

    def grid_size(self) -> tuple[int, int]:
        """Return the grid size (columns, rows) used in this container.

        Returns:
            A tuple (num_columns, num_rows).
        """
        return super().grid_size()  # type: ignore[misc]

    def grid_slaves(
            self,
            row: int | None = None,
            column: int | None = None,
    ) -> list[Any]:
        """Return the widgets managed by grid in this container.

        Args:
            row: If provided, return only widgets in the given row.
            column: If provided, return only widgets in the given column.

        Returns:
            A list of child widgets managed by grid.
        """
        if row is None and column is None:
            return super().grid_slaves()  # type: ignore[misc]
        if row is None:
            return super().grid_slaves(column=column)  # type: ignore[misc]
        if column is None:
            return super().grid_slaves(row=row)  # type: ignore[misc]
        return super().grid_slaves(row=row, column=column)  # type: ignore[misc]
