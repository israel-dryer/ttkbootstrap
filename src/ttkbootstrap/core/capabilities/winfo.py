from __future__ import annotations

from typing import Any


class WinfoMixin:
    """Widget information (winfo) helpers.

    Tk uses the term **window** to mean **any widget** with a Tk window handle
    (not just a `Toplevel`). In ttkbootstrap documentation we use the word
    **widget** unless we specifically mean a top-level window.

    Tk's `winfo` command family exposes runtime information about a widget/window:
    geometry, hierarchy, mapping/visibility, pointer location, screen metrics, and more.

    This mixin provides thin pass-through methods with modern Google-style
    docstrings for commonly used `winfo_*` APIs in Tkinter.

    Intended usage:
        class Widget(WinfoMixin, ttk.Widget): ...
        class App(WinfoMixin, tkinter.Tk): ...
        class Window(WinfoMixin, tkinter.Toplevel): ...

    Notes:
        - All methods delegate to the underlying Tkinter implementation.
        - Many `winfo_*` values are only meaningful after the widget has been
          realized and geometry has been computed. If you need up-to-date sizes,
          call `update_idletasks()` first.
    """

    # -------------------------------------------------------------------------
    # Existence / mapping / visibility
    # -------------------------------------------------------------------------

    def winfo_exists(self) -> int:
        """Return whether this widget exists.

        Returns:
            1 if the widget exists, 0 otherwise.
        """
        return super().winfo_exists()  # type: ignore[misc]

    def winfo_ismapped(self) -> int:
        """Return whether this widget is currently mapped (shown) on screen.

        A widget may exist but not be mapped (e.g., never packed/gridded/placed,
        or explicitly unmapped).

        Returns:
            1 if mapped, 0 otherwise.
        """
        return super().winfo_ismapped()  # type: ignore[misc]

    def winfo_viewable(self) -> int:
        """Return whether this widget and all its ancestors are mapped.

        A widget can be mapped but not viewable if an ancestor is not mapped.

        Returns:
            1 if viewable, 0 otherwise.
        """
        return super().winfo_viewable()  # type: ignore[misc]

    # -------------------------------------------------------------------------
    # Widget identity / hierarchy
    # -------------------------------------------------------------------------

    def winfo_id(self) -> int:
        """Return a platform-specific identifier for the underlying window.

        Returns:
            An integer window identifier. Meaning varies by platform.
        """
        return super().winfo_id()  # type: ignore[misc]

    def winfo_name(self) -> str:
        """Return the widget's Tk name (path component, not full path).

        Returns:
            The widget's name (e.g. "button", "frame", etc.).
        """
        return super().winfo_name()  # type: ignore[misc]

    def winfo_pathname(self, id: int, displayof: int | None = None) -> str:
        """Return the Tk pathname for a window id.

        This is an advanced helper; most apps won't need it.

        Args:
            id: A platform-specific window id (often from `winfo_id()`).
            displayof: Optional display selector (Tk-specific). Rarely needed.

        Returns:
            The Tk pathname corresponding to `id`.
        """
        if displayof is None:
            return super().winfo_pathname(id)  # type: ignore[misc]
        return super().winfo_pathname(id, displayof)  # type: ignore[misc]

    def winfo_parent(self) -> str:
        """Return the Tk pathname of this widget's parent.

        Returns:
            The parent's Tk pathname.
        """
        return super().winfo_parent()  # type: ignore[misc]

    def winfo_toplevel(self) -> Any:
        """Return the toplevel window that contains this widget.

        Returns:
            The toplevel widget instance.
        """
        return super().winfo_toplevel()  # type: ignore[misc]

    def winfo_children(self) -> list[Any]:
        """Return this widget's direct children.

        Returns:
            A list of child widget instances.
        """
        return super().winfo_children()  # type: ignore[misc]

    def winfo_class(self) -> str:
        """Return the Tk class name for this widget (e.g. 'TButton').

        Returns:
            The Tk class name string.
        """
        return super().winfo_class()  # type: ignore[misc]

    def winfo_manager(self) -> str:
        """Return the geometry manager controlling this widget.

        Typical values are: "pack", "grid", "place", or "" if unmanaged.

        Returns:
            The name of the geometry manager or an empty string.
        """
        return super().winfo_manager()  # type: ignore[misc]

    # -------------------------------------------------------------------------
    # Geometry: local position/size (relative to parent)
    # -------------------------------------------------------------------------

    def winfo_x(self) -> int:
        """Return the x-coordinate of this widget relative to its parent.

        Returns:
            The x position in pixels.
        """
        return super().winfo_x()  # type: ignore[misc]

    def winfo_y(self) -> int:
        """Return the y-coordinate of this widget relative to its parent.

        Returns:
            The y position in pixels.
        """
        return super().winfo_y()  # type: ignore[misc]

    def winfo_width(self) -> int:
        """Return the current width of this widget in pixels.

        Note:
            Geometry may be stale until Tk processes idle tasks. Use
            `update_idletasks()` if you need a fresh value.

        Returns:
            The width in pixels.
        """
        return super().winfo_width()  # type: ignore[misc]

    def winfo_height(self) -> int:
        """Return the current height of this widget in pixels.

        Note:
            Geometry may be stale until Tk processes idle tasks. Use
            `update_idletasks()` if you need a fresh value.

        Returns:
            The height in pixels.
        """
        return super().winfo_height()  # type: ignore[misc]

    def winfo_reqwidth(self) -> int:
        """Return the requested width (geometry request) in pixels.

        This is the size the widget asks for before geometry management.

        Returns:
            The requested width in pixels.
        """
        return super().winfo_reqwidth()  # type: ignore[misc]

    def winfo_reqheight(self) -> int:
        """Return the requested height (geometry request) in pixels.

        This is the size the widget asks for before geometry management.

        Returns:
            The requested height in pixels.
        """
        return super().winfo_reqheight()  # type: ignore[misc]

    def winfo_rootx(self) -> int:
        """Return the absolute x-coordinate of this widget on the screen.

        Returns:
            The screen x position in pixels.
        """
        return super().winfo_rootx()  # type: ignore[misc]

    def winfo_rooty(self) -> int:
        """Return the absolute y-coordinate of this widget on the screen.

        Returns:
            The screen y position in pixels.
        """
        return super().winfo_rooty()  # type: ignore[misc]

    # -------------------------------------------------------------------------
    # Pointer (mouse) information
    # -------------------------------------------------------------------------

    def winfo_pointerx(self) -> int:
        """Return the pointer x-coordinate on the screen.

        This returns the mouse pointer position in screen (root) coordinates.

        Returns:
            The screen x position of the pointer in pixels.
        """
        return super().winfo_pointerx()  # type: ignore[misc]

    def winfo_pointery(self) -> int:
        """Return the pointer y-coordinate on the screen.

        This returns the mouse pointer position in screen (root) coordinates.

        Returns:
            The screen y position of the pointer in pixels.
        """
        return super().winfo_pointery()  # type: ignore[misc]

    def winfo_pointerxy(self) -> tuple[int, int]:
        """Return the pointer (x, y) coordinates on the screen.

        Returns:
            A tuple (x, y) in screen (root) coordinates.
        """
        return super().winfo_pointerxy()  # type: ignore[misc]

    def winfo_containing(self, rootx: int, rooty: int) -> Any:
        """Return the widget that contains the given screen coordinate.

        Args:
            rootx: Screen x coordinate in pixels.
            rooty: Screen y coordinate in pixels.

        Returns:
            The widget instance at that screen coordinate, or None if no widget
            is present at that location.
        """
        return super().winfo_containing(rootx, rooty)  # type: ignore[misc]

    # -------------------------------------------------------------------------
    # Screen / display metrics
    # -------------------------------------------------------------------------

    def winfo_screenwidth(self) -> int:
        """Return the width of the screen in pixels.

        Returns:
            Screen width in pixels.
        """
        return super().winfo_screenwidth()  # type: ignore[misc]

    def winfo_screenheight(self) -> int:
        """Return the height of the screen in pixels.

        Returns:
            Screen height in pixels.
        """
        return super().winfo_screenheight()  # type: ignore[misc]

    def winfo_fpixels(self, number: str) -> float:
        """Convert a distance string to pixels (floating point).

        Tk distance strings can include units like:
            - "c" (centimeters)
            - "i" (inches)
            - "m" (millimeters)
            - "p" (points)

        Plain numbers are pixels.

        Args:
            number: A Tk distance string (e.g. "2c", "0.5i", "10").

        Returns:
            The distance in pixels as a float.
        """
        return super().winfo_fpixels(number)  # type: ignore[misc]

    def winfo_pixels(self, number: str) -> int:
        """Convert a distance string to pixels (integer).

        Args:
            number: A Tk distance string (e.g. "2c", "0.5i", "10").

        Returns:
            The distance in pixels as an int (rounded by Tk).
        """
        return super().winfo_pixels(number)  # type: ignore[misc]
