"""Base window functionality shared between App (Tk) and Toplevel.

This module provides the BaseWindow mixin class that encapsulates common
window management functionality used by both the main App (formerly Window)
and Toplevel classes. This eliminates code duplication and ensures consistent
behavior across all window types.

The BaseWindow mixin provides:
- Window configuration (size, position, constraints)
- Alpha transparency handling (platform-aware)
- Icon management
- Positioning utilities
- Common window attributes
"""

from __future__ import annotations

import tkinter
from typing import Optional

from ttkbootstrap.runtime.window_utilities import WindowPositioning, WindowSizing


def on_visibility_alpha(event: tkinter.Event) -> None:
    """Set Window or Toplevel alpha value on Visibility (X11).

    X11 requires alpha to be set after the window is visible, so we bind
    to the <Visibility> event and set alpha then, unbinding after first use.

    Args:
        event: The visibility event containing the widget.
    """
    widget = event.widget
    if hasattr(widget, 'alpha') and hasattr(widget, 'alpha_bind'):
        if widget.alpha_bind:
            widget.unbind(widget.alpha_bind)
        widget.attributes("-alpha", widget.alpha)


class BaseWindow:
    """Mixin providing shared window management functionality.

    This class is designed to be used as a mixin with tkinter.Tk or
    tkinter.Toplevel. It provides common window setup and management
    methods that are shared between the main App window and secondary
    Toplevel windows.

    Important:
        This is a MIXIN class, not a standalone widget class. It must be
        used with multiple inheritance alongside tkinter.Tk or tkinter.Toplevel.

    Usage:
        >>> class App(BaseWindow, tkinter.Tk):
        ...     def __init__(self, **kwargs):
        ...         tkinter.Tk.__init__(self)
        ...         BaseWindow._setup_window(self, **kwargs)

    Provides:
        - Window geometry configuration (size, position)
        - Size constraints (minsize, maxsize, resizable)
        - Alpha transparency (platform-aware)
        - Icon management
        - Positioning helpers (center on screen/parent)
        - Window attributes (title, transient, overrideredirect)
    """

    def _setup_window(
        self,
        title: str = "ttkbootstrap",
        size: Optional[tuple[int, int]] = None,
        position: Optional[tuple[int, int]] = None,
        minsize: Optional[tuple[int, int]] = None,
        maxsize: Optional[tuple[int, int]] = None,
        resizable: Optional[tuple[bool, bool]] = None,
        transient: Optional[tkinter.Misc] = None,
        overrideredirect: bool = False,
        alpha: float = 1.0,
    ) -> None:
        """Configure common window properties.

        This method should be called during window initialization to set up
        standard window properties. It handles platform differences automatically.
        The window is temporarily hidden during setup so that sizing and
        positioning are applied before it is shown.

        Args:
            title: Window title shown in titlebar.
            size: Optional (width, height) in pixels.
            position: Optional (x, y) position on screen.
            minsize: Optional (width, height) minimum window size.
            maxsize: Optional (width, height) maximum window size.
            resizable: Optional (width, height) resizable flags.
            transient: Optional master window for transient behavior.
            overrideredirect: If True, removes window decorations.
            alpha: Transparency level (0.0 to 1.0). Platform-aware.

        Note:
            The window must already be initialized (tkinter.Tk.__init__ or
            tkinter.Toplevel.__init__ called) before calling this method.
        """
        # Hide window until we finish applying geometry/resizing to avoid flicker
        self.withdraw()

        # Store window system for platform-specific behavior
        if not hasattr(self, 'winsys'):
            self.winsys = self.tk.call('tk', 'windowingsystem')

        # Basic configuration
        self.title(title)

        # Geometry
        if size is not None:
            width, height = size
            self.geometry(f"{width}x{height}")

        # Track whether we should center (defer until after constraints)
        _should_center = (position is None)

        if position is not None:
            xpos, ypos = position
            self.geometry(f"+{xpos}+{ypos}")

        # Size constraints
        if minsize is not None:
            width, height = minsize
            self.minsize(width, height)

        if maxsize is not None:
            width, height = maxsize
            self.maxsize(width, height)

        if resizable is not None:
            width, height = resizable
            self.resizable(width, height)

        # Window attributes
        if transient is not None:
            self.transient(transient)

        if overrideredirect:
            self.overrideredirect(1)

        # Alpha transparency (platform-aware)
        self._setup_alpha(alpha)

        # Center window on screen if no explicit position was provided
        if _should_center:
            # Update geometry to ensure size is applied before centering
            self.update_idletasks()
            x, y = WindowPositioning.center_on_screen(self)
            x, y = WindowPositioning.ensure_on_screen(self, x, y)
            self.geometry(f'+{x}+{y}')

        # Show the window now that sizing and positioning are complete
        self.deiconify()

    def _setup_alpha(self, alpha: float) -> None:
        """Configure window alpha transparency in a platform-aware manner.

        Handles platform differences in alpha transparency support:
        - X11: Requires setting alpha after window is visible
        - Windows/macOS: Can set alpha immediately

        Args:
            alpha: Transparency level (0.0 = fully transparent, 1.0 = opaque).

        Note:
            On X11, this binds to <Visibility> event to set alpha after
            the window becomes visible. The binding is automatically
            removed after first use.
        """
        if alpha is not None and alpha != 1.0:
            if self.winsys == 'x11':
                # X11 requires alpha to be set after window is visible
                self.alpha = alpha
                self.alpha_bind = self.bind("<Visibility>", on_visibility_alpha, '+')
            else:
                # Windows and macOS can set alpha immediately
                self.attributes("-alpha", alpha)

    def _setup_icon(self, iconphoto: Optional[str], default_icon_enabled: bool = True) -> None:
        """Configure window icon from file path or use default.

        Sets up the window icon, with support for:
        - Custom icon from file path
        - Default ttkbootstrap icon
        - No icon (None)

        Args:
            iconphoto: Path to icon image file, empty string for default, or None for no icon.
            default_icon_enabled: Whether to use default icon when iconphoto is empty string.

        Note:
            The icon is stored in self._icon to prevent garbage collection.
            On failure to load custom icon, falls back to default icon if enabled.
        """
        if iconphoto is None:
            # Explicitly no icon
            return

        if iconphoto == '' and default_icon_enabled:
            # Use default ttkbootstrap icon
            try:
                from ttkbootstrap_icons_bs import BootstrapIcon
                self._icon = BootstrapIcon('feather', 24, 'black')
                self.iconphoto(True, self._icon)
            except (ImportError, Exception):
                # Icon module not available or icon creation failed
                pass

        elif iconphoto:
            # Use user-provided icon
            try:
                self._icon = tkinter.PhotoImage(file=iconphoto, master=self)
                self.iconphoto(True, self._icon)
            except tkinter.TclError:
                # Failed to load user icon
                print(f'iconphoto path is invalid or not found: {iconphoto}')
                if default_icon_enabled:
                    # Fall back to default icon
                    try:
                        from ttkbootstrap_icons_bs import BootstrapIcon
                        self._icon = BootstrapIcon('feather', 24, 'black')
                        self.iconphoto(True, self._icon)
                    except (ImportError, Exception):
                        pass

    # ----------------------------------------------------------------- Positioning
    # Public positioning methods using WindowPositioning utilities

    def place_center(self) -> None:
        """Position the window in the center of the screen.

        Centers the window on the primary display. For multi-monitor setups,
        this typically centers on the monitor containing the mouse pointer.

        The window geometry is updated immediately.

        Example:
            >>> app = App()
            >>> app.place_center()
            >>> app.mainloop()
        """
        x, y = WindowPositioning.center_on_screen(self)
        x, y = WindowPositioning.ensure_on_screen(self, x, y)
        self.geometry(f'+{x}+{y}')

    def place_center_on(self, parent: tkinter.Misc) -> None:
        """Position the window centered on a parent widget or window.

        Centers this window on the specified parent widget or window.
        Commonly used for dialogs to center them on their parent window.

        Args:
            parent: The parent widget or window to center on.

        Example:
            >>> parent = App()
            >>> dialog = Toplevel()
            >>> dialog.place_center_on(parent)
        """
        x, y = WindowPositioning.center_on_parent(self, parent)
        x, y = WindowPositioning.ensure_on_screen(self, x, y)
        self.geometry(f'+{x}+{y}')

    def place_at(self, x: int, y: int, ensure_visible: bool = True) -> None:
        """Position the window at specific screen coordinates.

        Places the window at the given (x, y) coordinates, optionally
        adjusting the position to ensure the window remains fully visible
        on screen.

        Args:
            x: X coordinate on screen (in pixels from left edge).
            y: Y coordinate on screen (in pixels from top edge).
            ensure_visible: If True, adjusts coordinates to keep window on screen.

        Example:
            >>> window = App()
            >>> window.place_at(100, 100)
        """
        if ensure_visible:
            x, y = WindowPositioning.ensure_on_screen(self, x, y)
        self.geometry(f'+{x}+{y}')

    # Backward compatibility aliases
    def place_window_center(self) -> None:
        """Alias for place_center(). Deprecated, use place_center() instead."""
        self.place_center()

    position_center = place_center  # Additional alias for compatibility


class WindowMixin(BaseWindow):
    """Extended mixin with additional window utilities.

    Extends BaseWindow with additional convenience methods and utilities
    that are commonly needed but not strictly required for basic window
    functionality.

    This class can be used when you want the full suite of window utilities
    beyond the core BaseWindow functionality.
    """

    def set_default_size(
        self,
        width_ratio: float = 0.6,
        height_ratio: float = 0.7,
        min_width: int = 400,
        min_height: int = 300,
        max_width: Optional[int] = None,
        max_height: Optional[int] = None
    ) -> None:
        """Set window size as a percentage of screen size.

        Calculates and applies a window size based on screen dimensions,
        constrained by minimum and optional maximum sizes. Useful for
        creating responsive windows that adapt to different screen sizes.

        Args:
            width_ratio: Proportion of screen width (0.0 to 1.0).
            height_ratio: Proportion of screen height (0.0 to 1.0).
            min_width: Minimum window width in pixels.
            min_height: Minimum window height in pixels.
            max_width: Optional maximum window width in pixels.
            max_height: Optional maximum window height in pixels.

        Example:
            >>> window = App()
            >>> window.set_default_size(width_ratio=0.8, height_ratio=0.8)
            >>> # Window will be 80% of screen size
        """
        width, height = WindowSizing.get_default_size(
            self, width_ratio, height_ratio,
            min_width, min_height, max_width, max_height
        )
        self.geometry(f"{width}x{height}")

    def apply_size_constraints(
        self,
        minsize: Optional[tuple[int, int]] = None,
        maxsize: Optional[tuple[int, int]] = None,
        resizable: Optional[tuple[bool, bool]] = None
    ) -> None:
        """Apply multiple size constraints at once.

        Convenience method to set minsize, maxsize, and resizable in one call.

        Args:
            minsize: Optional (width, height) minimum size.
            maxsize: Optional (width, height) maximum size.
            resizable: Optional (width, height) resizable flags.

        Example:
            >>> window = App()
            >>> window.apply_size_constraints(
            ...     minsize=(400, 300),
            ...     resizable=(True, False)  # Width resizable, height fixed
            ... )
        """
        WindowSizing.apply_size_constraints(self, minsize, maxsize, resizable)
