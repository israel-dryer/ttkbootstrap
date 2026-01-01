from __future__ import annotations

import tkinter as tk
from typing import Literal, Optional, Any

from ttkbootstrap.widgets.primitives.frame import Frame
from ttkbootstrap.widgets.mixins.configure_mixin import configure_delegate
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

    Children packed into this frame automatically receive the frame's
    default layout options. Simply use the standard `pack()` method
    on child widgets - no special `add()` method needed.

    Example:
        ```python
        frame = PackFrame(direction="vertical", gap=10, fill_items="x")
        Label(frame, text="First").pack()
        Label(frame, text="Second").pack()
        Button(frame, text="Click").pack(expand=True)  # override default
        ```

    Args:
        master: Parent widget. If None, uses the default root window.
        direction: Layout direction. Options: "vertical", "horizontal",
            "row", "column", "row-reverse", "column-reverse". Defaults to "vertical".
        gap: Spacing between children in pixels. Defaults to 0.
        fill_items: Default fill behavior for children ("none", "x", "y", "both").
        expand_items: Default expand behavior for children.
        anchor_items: Default anchor for children.
        propagate: Whether the frame should resize to fit its contents.
        **kwargs: Additional Frame options (color, variant, padding, etc.).
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
        fill_items: Optional[Fill] = None,
        expand_items: Optional[bool] = None,
        anchor_items: Optional[Anchor] = None,
        propagate: Optional[bool] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(master, **kwargs)

        self._direction = direction
        self._gap = gap
        self._default_fill = fill_items
        self._default_expand = expand_items
        self._default_anchor = anchor_items

        # Ordered list of (widget, user_options) tuples for gap tracking
        self._managed: list[tuple[tk.Widget, dict[str, Any]]] = []

        if propagate is not None:
            self.pack_propagate(propagate)

    @property
    def _side(self) -> Side:
        """Get the pack side based on direction."""
        return self.SIDE_MAP.get(self._direction, "top")

    @configure_delegate('direction')
    def _delegate_direction(self, value=None) -> Direction:
        """Get or set the layout direction."""
        if value is None:
            return self._direction
        self._direction = value
        # Repack all widgets with new direction
        self._repack_all()

    @configure_delegate('gap')
    def _delegate_gap(self, value=None) -> int:
        """Get or set the gap between children."""
        if value is None:
            return self._gap
        self._gap = value
        # Repack all widgets with new gap
        self._repack_all()

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
        options: dict[str, Any] = {"in_": self, "side": self._side}

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
            tk.Pack.forget(widget)

        # Repack in order
        for i, (widget, user_options) in enumerate(self._managed):
            options = self._build_options(i, user_options)
            tk.Pack.configure(widget, **options)

    def _find_widget_index(self, widget: tk.Widget) -> int:
        """Find index of widget in managed list, return -1 if not found."""
        for i, (w, _) in enumerate(self._managed):
            if w is widget:
                return i
        return -1

    def _find_insert_index(self, before: tk.Widget = None, after: tk.Widget = None) -> int:
        """Determine insertion index based on before/after options."""
        if before is not None:
            idx = self._find_widget_index(before)
            if idx >= 0:
                return idx
        if after is not None:
            idx = self._find_widget_index(after)
            if idx >= 0:
                return idx + 1
        return len(self._managed)

    # -------------------------------------------------------------------------
    # Hook methods called by PackMixin
    # -------------------------------------------------------------------------

    def _on_child_pack(self, widget: tk.Widget, **options: Any) -> None:
        """Hook called when a child widget calls pack().

        Applies frame defaults, handles gap spacing, and tracks the widget.
        """
        # Check if widget is already managed (reconfigure case)
        existing_idx = self._find_widget_index(widget)

        # Determine insertion position from before/after
        before = options.pop("before", None)
        after = options.pop("after", None)

        if existing_idx >= 0:
            # Widget already managed - update its options
            self._managed[existing_idx] = (widget, options)
            self._repack_all()
        else:
            # New widget - find insertion point
            insert_idx = self._find_insert_index(before, after)

            if insert_idx < len(self._managed):
                # Inserting in the middle - need to repack all
                self._managed.insert(insert_idx, (widget, options))
                self._repack_all()
            else:
                # Appending at the end - just pack it
                pack_options = self._build_options(len(self._managed), options)
                tk.Pack.configure(widget, **pack_options)
                self._managed.append((widget, options))

    def _on_child_pack_forget(self, widget: tk.Widget) -> None:
        """Hook called when a child widget calls pack_forget().

        Removes widget from tracking and repacks remaining widgets if needed.
        """
        idx = self._find_widget_index(widget)
        if idx < 0:
            # Not managed by us, just forget it normally
            tk.Pack.forget(widget)
            return

        # Remove from our tracking
        tk.Pack.forget(widget)
        self._managed.pop(idx)

        # Only repack if we removed something that affects gaps (not the last item)
        if idx < len(self._managed):
            self._repack_all()
