from __future__ import annotations

from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from typing_extensions import Self


class PlaceMixin:
    """Place geometry manager helpers (place).

    Tk's `place` geometry manager positions widgets using absolute coordinates
    and/or relative fractions of the container size.

    `place` is useful for:
        - overlays (badges, floating buttons, popovers)
        - precise positioning inside a fixed-size container
        - small "anchor" adjustments that don't fit grid/pack well

    Notes:
        - `place` is generally less adaptive than `grid` or `pack` for resizable UIs.
        - Relative coordinates (`relx`, `rely`, `relwidth`, `relheight`) are fractions
          of the container size (0.0–1.0).
    """

    # -------------------------------------------------------------------------
    # Core widget methods
    # -------------------------------------------------------------------------

    def place(self, cnf: dict[str, Any] | None = None, **kw: Any) -> Self:
        """Position this widget using the place geometry manager.

        Args:
            cnf: Optional dict of place options.
            **kw: Place options. Common options include:
                - x, y: Absolute coordinates in pixels (relative to container).
                - relx, rely: Relative coordinates (0.0–1.0) of the container size.
                - width, height: Absolute size in pixels.
                - relwidth, relheight: Relative size (0.0–1.0) of the container size.
                - anchor: Which point of the widget is placed at (x, y) / (relx, rely)
                  (e.g. "nw", "center", "se").
                - bordermode: How to interpret x/y relative to container borders.

        Returns:
            Self for method chaining.
        """
        options = cnf or {}
        options.update(kw)
        super().place(**options)  # type: ignore[misc]
        return self  # type: ignore[return-value]

    def place_configure(self, cnf: dict[str, Any] | None = None, **kw: Any) -> Self:
        """Alias for `place()`.

        Args:
            cnf: Optional dict of place options.
            **kw: Place options (see `place`).

        Returns:
            Self for method chaining.
        """
        return self.place(cnf, **kw)

    def place_forget(self) -> Self:
        """Unmap this widget and forget its place configuration.

        Returns:
            Self for method chaining.
        """
        super().place_forget()  # type: ignore[misc]
        return self  # type: ignore[return-value]

    def place_info(self) -> dict[str, Any]:
        """Return this widget's current place configuration.

        Returns:
            A dict containing the current place options for this widget
            (x, y, relx, rely, width, height, etc.).
        """
        return super().place_info()  # type: ignore[misc]

    # -------------------------------------------------------------------------
    # Container methods
    # -------------------------------------------------------------------------

    def place_slaves(self) -> list[Any]:
        """Return the widgets managed by place in this container.

        Returns:
            A list of child widgets managed by place.
        """
        return super().place_slaves()  # type: ignore[misc]
