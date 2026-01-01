from __future__ import annotations

from typing import Any, Literal, TYPE_CHECKING

if TYPE_CHECKING:
    from typing_extensions import Self


class PackMixin:
    """Pack geometry manager helpers (pack).

    Tk's `pack` geometry manager places widgets relative to the sides of a container.

    In ttkbootstrap v2 you may prefer higher-level layout containers (e.g. `PackFrame`)
    for most UI layout. This mixin documents the underlying Tkinter `pack_*` API
    as an escape hatch and for interoperability with existing Tk code.

    Notes:
        - `pack()` attaches a widget to a parent container that is using pack.
        - `pack_propagate(False)` prevents a container from resizing to fit its children.
        - `fill`, `expand`, and `side` control how a widget consumes available space.
        - If the parent has a `_on_child_pack` hook (e.g. PackFrame), layout defaults
          are applied automatically.
    """

    # -------------------------------------------------------------------------
    # Core widget methods
    # -------------------------------------------------------------------------

    def pack(self, cnf: dict[str, Any] | None = None, **kw: Any) -> Self:
        """Position this widget using the pack geometry manager.

        Args:
            cnf: Optional dict of pack options.
            **kw: Pack options. Common options include:
                - side: Which side to pack against ("top", "bottom", "left", "right").
                - fill: How the widget should fill extra space ("x", "y", "both", "none").
                - expand: Whether the widget expands to fill extra space (0/1 or False/True).
                - anchor: Where to place the widget if it does not fill the space.
                - padx, pady: External padding around the widget.
                - ipadx, ipady: Internal padding inside the widget.
                - before, after: Pack relative to another widget.

        Returns:
            Self for method chaining.
        """
        options = cnf or {}
        options.update(kw)

        parent = self.master  # type: ignore[attr-defined]
        if hasattr(parent, '_on_child_pack'):
            parent._on_child_pack(self, **options)
        else:
            super().pack(**options)  # type: ignore[misc]
        return self  # type: ignore[return-value]

    def pack_configure(self, cnf: dict[str, Any] | None = None, **kw: Any) -> Self:
        """Alias for `pack()`.

        Args:
            cnf: Optional dict of pack options.
            **kw: Pack options (see `pack`).

        Returns:
            Self for method chaining.
        """
        return self.pack(cnf, **kw)

    def pack_forget(self) -> Self:
        """Unmap this widget and forget its pack configuration.

        The widget is removed from the layout, and its previous pack options
        are discarded.

        Returns:
            Self for method chaining.
        """
        parent = self.master  # type: ignore[attr-defined]
        if hasattr(parent, '_on_child_pack_forget'):
            parent._on_child_pack_forget(self)
        else:
            super().pack_forget()  # type: ignore[misc]
        return self  # type: ignore[return-value]

    def pack_info(self) -> dict[str, Any]:
        """Return this widget's current pack configuration.

        Returns:
            A dict containing the current pack options for this widget
            (side, fill, expand, padx, pady, etc.).
        """
        return super().pack_info()  # type: ignore[misc]

    # -------------------------------------------------------------------------
    # Container methods (applied to the pack parent container)
    # -------------------------------------------------------------------------

    def pack_propagate(self, flag: bool | None = None) -> bool | None:
        """Get or set pack geometry propagation for this container.

        When propagation is enabled (default), the container may resize itself
        to fit the size requests of its children.

        Args:
            flag: True/False to enable/disable propagation. If None, acts as a getter.

        Returns:
            When queried, returns the current propagation flag. When set, returns None.
        """
        return super().pack_propagate(flag)  # type: ignore[misc]

    def pack_slaves(self) -> list[Any]:
        """Return the widgets managed by pack in this container.

        Returns:
            A list of child widgets managed by pack (in packing order).
        """
        return super().pack_slaves()  # type: ignore[misc]
