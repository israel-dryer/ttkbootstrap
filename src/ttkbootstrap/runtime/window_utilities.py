"""Window positioning and sizing utilities for ttkbootstrap.

This module provides centralized window management utilities used across
Window (App), Toplevel, and Dialog classes. These utilities handle:
- Window positioning (screen-centered, parent-centered, custom coords)
- Screen bounds checking
- Multi-monitor support
- Platform-aware positioning

The utilities can be used standalone or as part of mixins/base classes.
"""

from __future__ import annotations

import tkinter
from typing import Optional


class WindowPositioning:
    """Centralized window positioning utilities.

    Provides static methods for calculating and applying window positions
    relative to screen, parent windows, or explicit coordinates. All methods
    handle edge cases like multi-monitor setups and ensure windows remain
    fully visible on screen.

    This class can be used as:
    - A standalone utility: WindowPositioning.center_on_screen(window)
    - A mixin: class MyWindow(WindowPositioning, tkinter.Tk)

    Examples:
        >>> # Center window on screen
        >>> x, y = WindowPositioning.center_on_screen(window)
        >>> window.geometry(f"+{x}+{y}")
        >>>
        >>> # Center dialog on parent
        >>> x, y = WindowPositioning.center_on_parent(dialog, parent)
        >>> dialog.geometry(f"+{x}+{y}")
        >>>
        >>> # Ensure coordinates are on screen
        >>> x, y = WindowPositioning.ensure_on_screen(window, 2000, 2000)
        >>> # Returns adjusted coordinates within screen bounds
    """

    @staticmethod
    def center_on_screen(window: tkinter.Misc) -> tuple[int, int]:
        """Calculate coordinates to center window on screen.

        Centers the window on the primary display. For multi-monitor setups,
        this typically centers on the monitor containing the mouse pointer.

        Args:
            window: The window to center. Must be a tkinter widget with
                   geometry info available (call update_idletasks() first).

        Returns:
            Tuple of (x, y) coordinates representing the top-left position
            that will center the window on screen.

        Note:
            The window must have been geometry-managed before calling this
            method. Call window.update_idletasks() first to ensure accurate
            dimensions are available.

        Example:
            >>> window = tkinter.Tk()
            >>> window.update_idletasks()
            >>> x, y = WindowPositioning.center_on_screen(window)
            >>> window.geometry(f"+{x}+{y}")
        """
        window.update_idletasks()

        w_width = window.winfo_reqwidth()
        w_height = window.winfo_reqheight()
        s_width = window.winfo_screenwidth()
        s_height = window.winfo_screenheight()

        x = (s_width - w_width) // 2
        y = (s_height - w_height) // 2

        return x, y

    @staticmethod
    def center_on_parent(window: tkinter.Toplevel, parent: tkinter.Misc) -> tuple[int, int]:
        """Calculate coordinates to center window on parent widget/window.

        Centers the window relative to its parent window or widget. This is
        commonly used for dialogs to appear centered on their parent window.

        Args:
            window: The window to center (typically a Toplevel or Dialog).
            parent: The parent window or widget to center on.

        Returns:
            Tuple of (x, y) screen coordinates that will center the window
            on the parent.

        Note:
            Both window and parent must have geometry information available.
            The returned coordinates are in screen coordinates, not relative
            to the parent.

        Example:
            >>> parent = tkinter.Tk()
            >>> dialog = tkinter.Toplevel(parent)
            >>> dialog.update_idletasks()
            >>> parent.update_idletasks()
            >>> x, y = WindowPositioning.center_on_parent(dialog, parent)
            >>> dialog.geometry(f"+{x}+{y}")
        """
        window.update_idletasks()
        parent.update_idletasks()

        # Use requested size or actual size, whichever is larger
        w_width = max(window.winfo_reqwidth(), window.winfo_width())
        w_height = max(window.winfo_reqheight(), window.winfo_height())

        # Get parent's screen position and size
        p_x = parent.winfo_rootx()
        p_y = parent.winfo_rooty()
        p_width = max(parent.winfo_width(), parent.winfo_reqwidth())
        p_height = max(parent.winfo_height(), parent.winfo_reqheight())

        # Calculate centered position
        x = p_x + max(0, (p_width - w_width) // 2)
        y = p_y + max(0, (p_height - w_height) // 2)

        return x, y

    @staticmethod
    def ensure_on_screen(
        window: tkinter.Misc,
        x: int,
        y: int,
        padding: int = 20,
        titlebar_height: int = 60
    ) -> tuple[int, int]:
        """Adjust coordinates to keep window fully visible on screen.

        Ensures that a window positioned at (x, y) will be fully visible on
        screen. If the coordinates would place any part of the window off-screen,
        they are adjusted to keep the window within screen bounds with padding.

        This method supports multi-monitor setups by using virtual root
        coordinates, ensuring the window appears on the correct display.

        Args:
            window: The window to position. Must have geometry info available.
            x: Desired x coordinate (screen coordinates).
            y: Desired y coordinate (screen coordinates).
            padding: Minimum padding from screen edges in pixels. Default is 20.
            titlebar_height: Additional padding for titlebar at top. Default is 60.

        Returns:
            Tuple of (x, y) coordinates adjusted to keep window on screen.

        Note:
            The titlebar_height accounts for window manager decorations which
            aren't included in winfo_height(). This prevents the titlebar from
            being positioned off-screen.

        Example:
            >>> window = tkinter.Tk()
            >>> window.update_idletasks()
            >>> # Try to position far off screen
            >>> x, y = WindowPositioning.ensure_on_screen(window, 5000, 5000)
            >>> # Returns coordinates that keep window visible
            >>> window.geometry(f"+{x}+{y}")
        """
        window.update_idletasks()

        w_width = window.winfo_reqwidth()
        w_height = window.winfo_reqheight()

        # Use virtual root for multi-monitor support
        screen_x0 = window.winfo_vrootx()
        screen_y0 = window.winfo_vrooty()
        screen_width = window.winfo_vrootwidth()
        screen_height = window.winfo_vrootheight()

        # Calculate screen boundaries
        screen_x1 = screen_x0 + screen_width
        screen_y1 = screen_y0 + screen_height

        # Constrain to screen bounds with padding
        x = max(screen_x0 + padding, min(x, screen_x1 - w_width - padding))
        y = max(screen_y0 + padding, min(y, screen_y1 - w_height - titlebar_height))

        return int(x), int(y)

    @staticmethod
    def position_window(
        window: tkinter.Misc,
        position: Optional[tuple[int, int]] = None,
        parent: Optional[tkinter.Misc] = None,
        center_on_parent: bool = True,
        ensure_visible: bool = True
    ) -> None:
        """Smart window positioning with multiple strategies.

        Provides a high-level interface for positioning windows using the
        most common strategies:
        - Explicit coordinates (if position is provided)
        - Centered on parent (if parent is provided and center_on_parent=True)
        - Centered on screen (fallback)

        Optionally ensures the window remains fully visible on screen.

        Args:
            window: The window to position.
            position: Optional (x, y) coordinates in screen space. If provided,
                     positions window at these coordinates.
            parent: Optional parent window. If provided and center_on_parent=True,
                   centers window on this parent.
            center_on_parent: Whether to center on parent when parent is provided.
                             Ignored if position is explicitly provided.
            ensure_visible: Whether to adjust coordinates to keep window on screen.
                           Default is True.

        Note:
            This method calls window.update_idletasks() internally and applies
            the geometry immediately.

        Example:
            >>> # Position at specific coordinates
            >>> WindowPositioning.position_window(window, position=(100, 100))
            >>>
            >>> # Center on parent
            >>> WindowPositioning.position_window(dialog, parent=parent_window)
            >>>
            >>> # Center on screen
            >>> WindowPositioning.position_window(window)
        """
        window.update_idletasks()

        if position is not None:
            # Explicit coordinates provided
            x, y = position
            if ensure_visible:
                x, y = WindowPositioning.ensure_on_screen(window, int(x), int(y))
            window.geometry(f"+{x}+{y}")

        elif parent is not None and center_on_parent:
            # Center on parent
            x, y = WindowPositioning.center_on_parent(window, parent)
            if ensure_visible:
                x, y = WindowPositioning.ensure_on_screen(window, x, y)
            window.geometry(f"+{x}+{y}")

        else:
            # Fallback: center on screen
            x, y = WindowPositioning.center_on_screen(window)
            if ensure_visible:
                x, y = WindowPositioning.ensure_on_screen(window, x, y)
            window.geometry(f"+{x}+{y}")


class WindowSizing:
    """Utilities for window sizing and dimension constraints.

    Provides helper methods for managing window dimensions, including
    minimum/maximum sizes and calculating appropriate default sizes
    based on screen dimensions.
    """

    @staticmethod
    def get_default_size(
        window: tkinter.Misc,
        width_ratio: float = 0.6,
        height_ratio: float = 0.7,
        min_width: int = 400,
        min_height: int = 300,
        max_width: Optional[int] = None,
        max_height: Optional[int] = None
    ) -> tuple[int, int]:
        """Calculate a reasonable default window size based on screen dimensions.

        Calculates window size as a percentage of screen size, constrained
        by minimum and optional maximum dimensions. Useful for creating
        responsive windows that adapt to different screen sizes.

        Args:
            window: Window to calculate size for (used to get screen dimensions).
            width_ratio: Proportion of screen width (0.0 to 1.0). Default is 0.6 (60%).
            height_ratio: Proportion of screen height (0.0 to 1.0). Default is 0.7 (70%).
            min_width: Minimum window width in pixels. Default is 400.
            min_height: Minimum window height in pixels. Default is 300.
            max_width: Optional maximum window width in pixels.
            max_height: Optional maximum window height in pixels.

        Returns:
            Tuple of (width, height) in pixels.

        Example:
            >>> window = tkinter.Tk()
            >>> width, height = WindowSizing.get_default_size(window)
            >>> window.geometry(f"{width}x{height}")
        """
        window.update_idletasks()

        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        width = int(screen_width * width_ratio)
        height = int(screen_height * height_ratio)

        # Apply constraints
        width = max(min_width, width)
        height = max(min_height, height)

        if max_width is not None:
            width = min(width, max_width)
        if max_height is not None:
            height = min(height, max_height)

        return width, height

    @staticmethod
    def apply_size_constraints(
        window: tkinter.Misc,
        minsize: Optional[tuple[int, int]] = None,
        maxsize: Optional[tuple[int, int]] = None,
        resizable: Optional[tuple[bool, bool]] = None
    ) -> None:
        """Apply size constraints to a window.

        Convenience method to apply multiple size-related constraints at once.

        Args:
            window: Window to apply constraints to.
            minsize: Optional (width, height) minimum size.
            maxsize: Optional (width, height) maximum size.
            resizable: Optional (width, height) resizable flags.

        Example:
            >>> WindowSizing.apply_size_constraints(
            ...     window,
            ...     minsize=(400, 300),
            ...     maxsize=(1920, 1080),
            ...     resizable=(True, False)  # Width resizable, height fixed
            ... )
        """
        if minsize is not None:
            window.minsize(*minsize)

        if maxsize is not None:
            window.maxsize(*maxsize)

        if resizable is not None:
            window.resizable(*resizable)