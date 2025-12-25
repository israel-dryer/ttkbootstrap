from __future__ import annotations

import tkinter as tk
from typing import Literal, Optional, Any

from ttkbootstrap.widgets.primitives.frame import Frame
from ttkbootstrap.widgets.types import Master

Direction = Literal["vertical", "horizontal", "row", "column", "row-reverse", "column-reverse"]
Fill = Literal["none", "x", "y", "both"]
Side = Literal["top", "bottom", "left", "right"]
Anchor = Literal["n", "ne", "e", "se", "s", "sw", "w", "nw", "center"]


class PackFrame(Frame):
    """A Frame with simplified pack-based layout management.

    PackFrame extends the ttkbootstrap Frame with automatic pack-based
    layout management, including support for direction, gap spacing,
    and default fill/expand behavior.

    Args:
        master: Parent widget. If None, uses the default root window.
        direction: Layout direction. Options: "vertical", "horizontal",
            "row", "column", "row-reverse", "column-reverse". Defaults to "vertical".
        gap: Spacing between children in pixels. Defaults to 0.
        fill: Default fill behavior for children ("none", "x", "y", "both").
        expand: Default expand behavior for children.
        anchor: Default anchor for children.
        propagate: Whether the frame should resize to fit its contents.
        **kwargs: Additional Frame options (bootstyle, padding, etc.).
    """

    SIDE_MAP: dict[Direction, Side] = {
        "vertical": "top",
        "column": "top",
        "column-reverse": "bottom",
        "horizontal": "left",
        "row": "left",
        "row-reverse": "right",
    }

    def __init__(
        self,
        master: Master = None,
        *,
        direction: Direction = "vertical",
        gap: int = 0,
        fill: Optional[Fill] = None,
        expand: Optional[bool] = None,
        anchor: Optional[Anchor] = None,
        propagate: Optional[bool] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(master, **kwargs)

        self._direction = direction
        self._gap = gap
        self._default_fill = fill
        self._default_expand = expand
        self._default_anchor = anchor

        # Ordered list of (widget, user_options) tuples
        self._managed: list[tuple[tk.Widget, dict[str, Any]]] = []

        if propagate is not None:
            self.pack_propagate(propagate)

    @property
    def side(self) -> Side:
        """Get the pack side based on direction."""
        return self.SIDE_MAP.get(self._direction, "top")

    @property
    def children(self) -> list[tk.Widget]:
        """Return list of managed widgets in order."""
        return [w for w, _ in self._managed]

    def _compute_gap(self, index: int) -> dict[str, Any]:
        """Compute padding for gap based on position and direction."""
        if index == 0 or self._gap == 0:
            return {}

        if self._direction in ("vertical", "column"):
            return {"pady": (self._gap, 0)}
        elif self._direction == "column-reverse":
            return {"pady": (0, self._gap)}
        elif self._direction in ("horizontal", "row"):
            return {"padx": (self._gap, 0)}
        elif self._direction == "row-reverse":
            return {"padx": (0, self._gap)}
        return {}

    def _build_options(self, index: int, user_options: dict[str, Any]) -> dict[str, Any]:
        """Build final pack options by merging defaults with user options."""
        options: dict[str, Any] = {"in_": self, "side": self.side}

        # Apply gap based on position
        options.update(self._compute_gap(index))

        # Apply container-level defaults
        if self._default_fill is not None:
            options["fill"] = self._default_fill
        if self._default_expand is not None:
            options["expand"] = self._default_expand
        if self._default_anchor is not None:
            options["anchor"] = self._default_anchor

        # User options override everything
        options.update(user_options)
        return options

    def _repack_all(self) -> None:
        """Unpack and repack all widgets to maintain correct order and gaps."""
        # Unpack all
        for widget, _ in self._managed:
            widget.pack_forget()

        # Repack in order
        for i, (widget, user_options) in enumerate(self._managed):
            options = self._build_options(i, user_options)
            widget.pack(**options)

    def _find_index(self, widget: tk.Widget) -> int:
        """Find index of widget, raise ValueError if not found."""
        for i, (w, _) in enumerate(self._managed):
            if w is widget:
                return i
        raise ValueError(f"Widget {widget} is not managed by this PackFrame")

    def add(self, widget: tk.Widget, **options: Any) -> tk.Widget:
        """
        Add a widget to the end of the frame.

        Args:
            widget: The widget to add (should already have this frame as master)
            **options: Pack options that override container defaults
                      (fill, expand, anchor, padx, pady, ipadx, ipady)

        Returns:
            The widget (for chaining)
        """
        index = len(self._managed)
        pack_options = self._build_options(index, options)
        widget.pack(**pack_options)
        self._managed.append((widget, options))
        return widget

    def insert(self, index: int, widget: tk.Widget, **options: Any) -> tk.Widget:
        """
        Insert a widget at a specific index.

        Args:
            index: Position to insert at (0 = first)
            widget: The widget to insert
            **options: Pack options that override container defaults

        Returns:
            The widget (for chaining)
        """
        # Clamp index to valid range
        index = max(0, min(index, len(self._managed)))
        self._managed.insert(index, (widget, options))
        self._repack_all()
        return widget

    def remove(self, widget: tk.Widget) -> None:
        """
        Remove a widget from the frame.

        The widget is unpacked but not destroyed.
        """
        index = self._find_index(widget)
        widget.pack_forget()
        self._managed.pop(index)
        # Only repack if we removed something that affects gaps
        if index < len(self._managed):
            self._repack_all()

    def move(self, widget: tk.Widget, new_index: int) -> None:
        """
        Move a widget to a new position.

        Args:
            widget: The widget to move
            new_index: The new position index
        """
        old_index = self._find_index(widget)
        entry = self._managed.pop(old_index)
        new_index = max(0, min(new_index, len(self._managed)))
        self._managed.insert(new_index, entry)
        self._repack_all()

    def update_options(self, widget: tk.Widget, **options: Any) -> None:
        """
        Update pack options for a widget.

        Args:
            widget: The widget to update
            **options: New pack options (merged with existing)
        """
        index = self._find_index(widget)
        _, current_options = self._managed[index]
        new_options = {**current_options, **options}
        self._managed[index] = (widget, new_options)
        self._repack_all()

    def clear(self) -> None:
        """Remove all widgets (unpacks but doesn't destroy them)."""
        for widget, _ in self._managed:
            widget.pack_forget()
        self._managed.clear()

    def index_of(self, widget: tk.Widget) -> int:
        """Get the index of a widget."""
        return self._find_index(widget)

    def __len__(self) -> int:
        return len(self._managed)

    def __iter__(self):
        return iter(self.children)