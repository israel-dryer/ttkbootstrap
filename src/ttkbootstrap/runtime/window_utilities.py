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
from typing import Literal, Optional, Tuple, Union

# Type definitions for anchor points (using tkinter convention)
AnchorPoint = Literal['n', 's', 'e', 'w', 'ne', 'nw', 'se', 'sw', 'center']
AutoFlip = Union[bool, Literal['vertical', 'horizontal']]


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

        Examples:
            >>> window = tkinter.Tk()
            >>> window.update_idletasks()
            >>> x, y = WindowPositioning.center_on_screen(window)
            >>> window.geometry(f"+{x}+{y}")
        """
        window.update_idletasks()

        w_width = max(window.winfo_reqwidth(), window.winfo_width())
        w_height = max(window.winfo_reqheight(), window.winfo_height())
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

        Examples:
import ttkbootstrap.runtime.toplevel            >>> parent = tkinter.Tk()
            >>> dialog = ttkbootstrap.runtime.toplevel.Toplevel(parent)
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

        Examples:
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

        Examples:
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

    @staticmethod
    def _get_anchor_coordinates(
        widget: tkinter.Misc,
        anchor: AnchorPoint = 'nw',
        use_requested_size: bool = True
    ) -> Tuple[int, int]:
        """Calculate screen coordinates for an anchor point on a widget.

        Uses tkinter's standard anchor naming convention:
        - 'n', 's', 'e', 'w' for cardinal directions (north, south, east, west)
        - 'ne', 'nw', 'se', 'sw' for corners
        - 'center' for the center point

        Args:
            widget: Widget to get anchor coordinates for.
            anchor: Which point on the widget to return coordinates for.
            use_requested_size: If True, uses requested size; otherwise actual size.

        Returns:
            Tuple of (x, y) screen coordinates for the anchor point.
        """
        widget.update_idletasks()

        # Get widget position
        x = widget.winfo_rootx()
        y = widget.winfo_rooty()

        # Get widget dimensions
        if use_requested_size:
            width = widget.winfo_reqwidth()
            height = widget.winfo_reqheight()
        else:
            width = widget.winfo_width()
            height = widget.winfo_height()

        # Calculate anchor position using tkinter convention
        if anchor == 'nw':
            return x, y
        elif anchor == 'n':
            return x + width // 2, y
        elif anchor == 'ne':
            return x + width, y
        elif anchor == 'w':
            return x, y + height // 2
        elif anchor == 'center':
            return x + width // 2, y + height // 2
        elif anchor == 'e':
            return x + width, y + height // 2
        elif anchor == 'sw':
            return x, y + height
        elif anchor == 's':
            return x + width // 2, y + height
        elif anchor == 'se':
            return x + width, y + height
        else:
            return x, y

    @staticmethod
    def _get_screen_anchor_coordinates(
        window: tkinter.Misc,
        anchor: AnchorPoint = 'center'
    ) -> Tuple[int, int]:
        """Calculate screen coordinates for an anchor point on the screen.

        Args:
            window: Window (used to get screen dimensions).
            anchor: Which point on the screen to return coordinates for.

        Returns:
            Tuple of (x, y) screen coordinates for the anchor point.
        """
        window.update_idletasks()

        # Get screen dimensions
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        # Screen position is always (0, 0) at top-left
        x, y = 0, 0

        # Calculate anchor position on screen
        if anchor == 'nw':
            return 0, 0
        elif anchor == 'n':
            return screen_width // 2, 0
        elif anchor == 'ne':
            return screen_width, 0
        elif anchor == 'w':
            return 0, screen_height // 2
        elif anchor == 'center':
            return screen_width // 2, screen_height // 2
        elif anchor == 'e':
            return screen_width, screen_height // 2
        elif anchor == 'sw':
            return 0, screen_height
        elif anchor == 's':
            return screen_width // 2, screen_height
        elif anchor == 'se':
            return screen_width, screen_height
        else:
            return screen_width // 2, screen_height // 2

    @staticmethod
    def _get_cursor_anchor_coordinates(
        window: tkinter.Misc,
        anchor: AnchorPoint = 'nw'
    ) -> Tuple[int, int]:
        """Calculate screen coordinates for an anchor point relative to cursor.

        The cursor is treated as a point (no width/height), so all anchor points
        return the same cursor position. The anchor parameter is kept for API
        consistency but doesn't affect the result.

        Args:
            window: Window (used to get cursor position).
            anchor: Anchor point (ignored, cursor is a point).

        Returns:
            Tuple of (x, y) screen coordinates of the cursor.
        """
        window.update_idletasks()

        # Cursor is a point, so all anchors return cursor position
        x = window.winfo_pointerx()
        y = window.winfo_pointery()

        return x, y

    @staticmethod
    def _flip_anchor_vertical(anchor: AnchorPoint) -> AnchorPoint:
        """Flip an anchor point vertically (north ↔ south).

        Args:
            anchor: Anchor point to flip.

        Returns:
            Vertically flipped anchor point.
        """
        flip_map = {
            'n': 's', 's': 'n',
            'ne': 'se', 'se': 'ne',
            'nw': 'sw', 'sw': 'nw',
            'e': 'e', 'w': 'w',
            'center': 'center'
        }
        return flip_map.get(anchor, anchor)

    @staticmethod
    def _flip_anchor_horizontal(anchor: AnchorPoint) -> AnchorPoint:
        """Flip an anchor point horizontally (east ↔ west).

        Args:
            anchor: Anchor point to flip.

        Returns:
            Horizontally flipped anchor point.
        """
        flip_map = {
            'e': 'w', 'w': 'e',
            'ne': 'nw', 'nw': 'ne',
            'se': 'sw', 'sw': 'se',
            'n': 'n', 's': 's',
            'center': 'center'
        }
        return flip_map.get(anchor, anchor)

    @staticmethod
    def _check_offscreen(
        window: tkinter.Misc,
        x: int,
        y: int,
        padding: int = 20
    ) -> Tuple[bool, bool]:
        """Check if a window positioned at (x, y) would be off-screen.

        Args:
            window: Window to check.
            x: Proposed x coordinate.
            y: Proposed y coordinate.
            padding: Minimum padding from screen edges.

        Returns:
            Tuple of (vertical_offscreen, horizontal_offscreen) booleans.
        """
        window.update_idletasks()

        w_width = max(window.winfo_reqwidth(), window.winfo_width())
        w_height = max(window.winfo_reqheight(), window.winfo_height())

        # Get screen boundaries
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        # Check vertical (top/bottom off-screen)
        vertical_offscreen = (
            y < padding or  # Too far up
            y + w_height + padding > screen_height  # Too far down
        )

        # Check horizontal (left/right off-screen)
        horizontal_offscreen = (
            x < padding or  # Too far left
            x + w_width + padding > screen_width  # Too far right
        )

        return vertical_offscreen, horizontal_offscreen

    @staticmethod
    def position_anchored(
        window: tkinter.Misc,
        anchor_to: Union[tkinter.Misc, Literal["screen", "cursor", "parent"]],
        parent: Optional[tkinter.Misc] = None,
        anchor_point: AnchorPoint = 'center',
        window_point: AnchorPoint = 'center',
        offset: Tuple[int, int] = (0, 0),
        auto_flip: AutoFlip = False,
        ensure_visible: bool = True
    ) -> None:
        """Position window using unified anchor-based positioning with auto-flip.

        This is the new consolidated positioning method that handles:
        - Widget anchoring
        - Screen anchoring (with anchor points)
        - Cursor anchoring
        - Parent anchoring
        - Auto-flip (vertical and/or horizontal)

        Args:
            window: The window to position.
            anchor_to: Positioning target:
                - Widget: Anchor to a specific widget
                - "screen": Anchor to screen edges/corners
                - "cursor": Anchor to mouse cursor
                - "parent": Anchor to parent window
            parent: Parent window (required if anchor_to="parent").
            anchor_point: Point on the anchor target.
            window_point: Point on the window.
            offset: Additional (x, y) offset in pixels.
            auto_flip: Smart flipping to keep window on screen:
                - False: No flipping
                - True: Flip both vertically and horizontally
                - 'vertical': Only flip up/down
                - 'horizontal': Only flip left/right
            ensure_visible: Whether to adjust position to keep window on screen.

        Examples:
            >>> # Center on screen
            >>> WindowPositioning.position_anchored(window, anchor_to="screen")
            >>>
            >>> # Top-right corner of screen
            >>> WindowPositioning.position_anchored(
            ...     window, anchor_to="screen", anchor_point='ne', window_point='ne'
            ... )
            >>>
            >>> # Dropdown with auto-flip
            >>> WindowPositioning.position_anchored(
            ...     window, anchor_to=button,
            ...     anchor_point='sw', window_point='nw',
            ...     auto_flip='vertical'
            ... )
        """
        window.update_idletasks()

        # Get anchor coordinates based on anchor_to type
        if anchor_to == "screen":
            anchor_x, anchor_y = WindowPositioning._get_screen_anchor_coordinates(
                window, anchor_point
            )
        elif anchor_to == "cursor":
            anchor_x, anchor_y = WindowPositioning._get_cursor_anchor_coordinates(
                window, anchor_point
            )
        elif anchor_to == "parent":
            if parent is None:
                raise ValueError("parent parameter required when anchor_to='parent'")
            parent.update_idletasks()
            anchor_x, anchor_y = WindowPositioning._get_anchor_coordinates(
                parent, anchor_point
            )
        else:
            # Assume it's a widget
            anchor_to.update_idletasks()
            anchor_x, anchor_y = WindowPositioning._get_anchor_coordinates(
                anchor_to, anchor_point
            )

        # Calculate window position based on window_point
        w_width = max(window.winfo_reqwidth(), window.winfo_width())
        w_height = max(window.winfo_reqheight(), window.winfo_height())

        # Calculate offset based on window anchor point
        x_offset, y_offset = 0, 0

        if window_point == 'nw':
            x_offset, y_offset = 0, 0
        elif window_point == 'n':
            x_offset, y_offset = -w_width // 2, 0
        elif window_point == 'ne':
            x_offset, y_offset = -w_width, 0
        elif window_point == 'w':
            x_offset, y_offset = 0, -w_height // 2
        elif window_point == 'center':
            x_offset, y_offset = -w_width // 2, -w_height // 2
        elif window_point == 'e':
            x_offset, y_offset = -w_width, -w_height // 2
        elif window_point == 'sw':
            x_offset, y_offset = 0, -w_height
        elif window_point == 's':
            x_offset, y_offset = -w_width // 2, -w_height
        elif window_point == 'se':
            x_offset, y_offset = -w_width, -w_height

        # Calculate initial position
        x = int(anchor_x + x_offset + offset[0])
        y = int(anchor_y + y_offset + offset[1])

        # Auto-flip logic
        if auto_flip:
            vertical_offscreen, horizontal_offscreen = WindowPositioning._check_offscreen(
                window, x, y
            )

            should_flip_vertical = False
            should_flip_horizontal = False

            if auto_flip is True or auto_flip == 'vertical':
                should_flip_vertical = vertical_offscreen

            if auto_flip is True or auto_flip == 'horizontal':
                should_flip_horizontal = horizontal_offscreen

            # Flip if needed
            if should_flip_vertical or should_flip_horizontal:
                flipped_anchor_point = anchor_point
                flipped_window_point = window_point

                if should_flip_vertical:
                    flipped_anchor_point = WindowPositioning._flip_anchor_vertical(
                        flipped_anchor_point
                    )
                    flipped_window_point = WindowPositioning._flip_anchor_vertical(
                        flipped_window_point
                    )

                if should_flip_horizontal:
                    flipped_anchor_point = WindowPositioning._flip_anchor_horizontal(
                        flipped_anchor_point
                    )
                    flipped_window_point = WindowPositioning._flip_anchor_horizontal(
                        flipped_window_point
                    )

                # Recalculate with flipped anchors
                if anchor_to == "screen":
                    anchor_x, anchor_y = WindowPositioning._get_screen_anchor_coordinates(
                        window, flipped_anchor_point
                    )
                elif anchor_to == "cursor":
                    anchor_x, anchor_y = WindowPositioning._get_cursor_anchor_coordinates(
                        window, flipped_anchor_point
                    )
                elif anchor_to == "parent":
                    anchor_x, anchor_y = WindowPositioning._get_anchor_coordinates(
                        parent, flipped_anchor_point
                    )
                else:
                    anchor_x, anchor_y = WindowPositioning._get_anchor_coordinates(
                        anchor_to, flipped_anchor_point
                    )

                # Recalculate offset for flipped window_point
                if flipped_window_point == 'nw':
                    x_offset, y_offset = 0, 0
                elif flipped_window_point == 'n':
                    x_offset, y_offset = -w_width // 2, 0
                elif flipped_window_point == 'ne':
                    x_offset, y_offset = -w_width, 0
                elif flipped_window_point == 'w':
                    x_offset, y_offset = 0, -w_height // 2
                elif flipped_window_point == 'center':
                    x_offset, y_offset = -w_width // 2, -w_height // 2
                elif flipped_window_point == 'e':
                    x_offset, y_offset = -w_width, -w_height // 2
                elif flipped_window_point == 'sw':
                    x_offset, y_offset = 0, -w_height
                elif flipped_window_point == 's':
                    x_offset, y_offset = -w_width // 2, -w_height
                elif flipped_window_point == 'se':
                    x_offset, y_offset = -w_width, -w_height

                x = int(anchor_x + x_offset + offset[0])
                y = int(anchor_y + y_offset + offset[1])

        # Final ensure visible check
        if ensure_visible:
            x, y = WindowPositioning.ensure_on_screen(window, x, y)

        window.geometry(f"+{x}+{y}")

    @staticmethod
    def position_with_anchor(
        window: tkinter.Misc,
        anchor_to: tkinter.Misc,
        anchor_point: AnchorPoint = 'sw',
        window_point: AnchorPoint = 'nw',
        offset: Tuple[int, int] = (0, 0),
        ensure_visible: bool = True
    ) -> None:
        """Position window relative to another widget using anchor points.

        This method positions a window by aligning specific points on both
        the window and the anchor widget, with optional offset. This is useful
        for dropdowns, tooltips, context menus, and popovers.

        Uses tkinter's standard anchor naming:
        - 'n' (north/top), 's' (south/bottom), 'e' (east/right), 'w' (west/left)
        - 'ne', 'nw', 'se', 'sw' for corners
        - 'center' for center point

        Args:
            window: The window to position.
            anchor_to: The widget to anchor the window to.
            anchor_point: Which point on the anchor widget to use as reference.
                         Default 'sw' (bottom-left) is common for dropdowns.
            window_point: Which point on the window to align with the anchor point.
                         Default 'nw' (top-left) aligns window's top-left to anchor point.
            offset: Additional (x, y) offset in pixels.
            ensure_visible: Whether to adjust position to keep window on screen.

        Examples:
            >>> # Show dropdown below button (button's bottom-left -> window's top-left)
            >>> WindowPositioning.position_with_anchor(
            ...     window=dropdown,
            ...     anchor_to=button,
            ...     anchor_point='sw',  # button's bottom-left
            ...     window_point='nw',  # window's top-left
            ...     offset=(0, 2)
            ... )
            >>>
            >>> # Show tooltip above widget (widget's top -> tooltip's bottom)
            >>> WindowPositioning.position_with_anchor(
            ...     window=tooltip,
            ...     anchor_to=widget,
            ...     anchor_point='n',   # widget's top-center
            ...     window_point='s',   # tooltip's bottom-center
            ...     offset=(0, -5)
            ... )
        """
        window.update_idletasks()
        anchor_to.update_idletasks()

        # Get anchor point on the reference widget
        anchor_x, anchor_y = WindowPositioning._get_anchor_coordinates(
            anchor_to, anchor_point
        )

        # Get window dimensions
        w_width = max(window.winfo_reqwidth(), window.winfo_width())
        w_height = max(window.winfo_reqheight(), window.winfo_height())

        # Calculate offset based on window anchor point
        x_offset, y_offset = 0, 0

        if window_point == 'nw':
            x_offset, y_offset = 0, 0
        elif window_point == 'n':
            x_offset, y_offset = -w_width // 2, 0
        elif window_point == 'ne':
            x_offset, y_offset = -w_width, 0
        elif window_point == 'w':
            x_offset, y_offset = 0, -w_height // 2
        elif window_point == 'center':
            x_offset, y_offset = -w_width // 2, -w_height // 2
        elif window_point == 'e':
            x_offset, y_offset = -w_width, -w_height // 2
        elif window_point == 'sw':
            x_offset, y_offset = 0, -w_height
        elif window_point == 's':
            x_offset, y_offset = -w_width // 2, -w_height
        elif window_point == 'se':
            x_offset, y_offset = -w_width, -w_height

        # Calculate final position
        x = anchor_x + x_offset + offset[0]
        y = anchor_y + y_offset + offset[1]

        # Ensure window stays on screen
        if ensure_visible:
            x, y = WindowPositioning.ensure_on_screen(window, int(x), int(y))

        window.geometry(f"+{int(x)}+{int(y)}")

    @staticmethod
    def position_at_cursor(
        window: tkinter.Misc,
        offset: Tuple[int, int] = (5, 5),
        ensure_visible: bool = True
    ) -> None:
        """Position window at the current mouse cursor location.

        Useful for context menus, tooltips that follow the cursor, or
        click-to-show dialogs.

        Args:
            window: The window to position.
            offset: Additional (x, y) offset from cursor in pixels.
            ensure_visible: Whether to adjust position to keep window on screen.

        Examples:
            >>> # Show context menu at cursor
            >>> WindowPositioning.position_at_cursor(menu, offset=(2, 2))
        """
        window.update_idletasks()

        # Get cursor position
        x = window.winfo_pointerx() + offset[0]
        y = window.winfo_pointery() + offset[1]

        # Ensure window stays on screen
        if ensure_visible:
            x, y = WindowPositioning.ensure_on_screen(window, int(x), int(y))

        window.geometry(f"+{int(x)}+{int(y)}")

    @staticmethod
    def position_dropdown(
        window: tkinter.Misc,
        trigger_widget: tkinter.Misc,
        prefer_below: bool = True,
        align: Literal['left', 'right', 'center'] = 'left',
        offset: Tuple[int, int] = (0, 2),
        ensure_visible: bool = True,
        auto_flip: bool = True
    ) -> None:
        """Position window as a dropdown relative to a trigger widget.

        Smart positioning that automatically flips above/below based on
        available space. Commonly used for combobox dropdowns, autocomplete
        suggestions, and dropdown menus.

        Args:
            window: The dropdown window to position.
            trigger_widget: The widget that triggers the dropdown (e.g., button).
            prefer_below: If True, tries to show below trigger; else tries above.
            align: Horizontal alignment ('left', 'right', or 'center').
            offset: Additional (x, y) offset in pixels.
            ensure_visible: Whether to adjust position to keep window on screen.
            auto_flip: If True, automatically flips above/below if no room.

        Examples:
            >>> # Dropdown below button, left-aligned
            >>> WindowPositioning.position_dropdown(
            ...     window=dropdown,
            ...     trigger_widget=button,
            ...     prefer_below=True,
            ...     align='left'
            ... )
        """
        window.update_idletasks()
        trigger_widget.update_idletasks()

        # Get trigger widget position and size
        trigger_x = trigger_widget.winfo_rootx()
        trigger_y = trigger_widget.winfo_rooty()
        trigger_height = trigger_widget.winfo_height()
        trigger_width = trigger_widget.winfo_width()

        # Get window size
        w_width = max(window.winfo_reqwidth(), window.winfo_width())
        w_height = max(window.winfo_reqheight(), window.winfo_height())

        # Get screen boundaries
        screen_height = window.winfo_screenheight()

        # Determine vertical position
        show_below = prefer_below

        if auto_flip:
            # Check if there's room below
            space_below = screen_height - (trigger_y + trigger_height)
            space_above = trigger_y

            if prefer_below and space_below < w_height and space_above > space_below:
                show_below = False
            elif not prefer_below and space_above < w_height and space_below > space_above:
                show_below = True

        # Calculate vertical position
        if show_below:
            y = trigger_y + trigger_height + offset[1]
        else:
            y = trigger_y - w_height - offset[1]

        # Calculate horizontal position based on alignment
        if align == 'left':
            x = trigger_x + offset[0]
        elif align == 'right':
            x = trigger_x + trigger_width - w_width + offset[0]
        elif align == 'center':
            x = trigger_x + (trigger_width - w_width) // 2 + offset[0]
        else:
            x = trigger_x + offset[0]

        # Ensure window stays on screen
        if ensure_visible:
            x, y = WindowPositioning.ensure_on_screen(window, int(x), int(y))

        window.geometry(f"+{int(x)}+{int(y)}")


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

        Examples:
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

        Examples:
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