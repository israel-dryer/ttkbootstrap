"""Utility functions for ttkbootstrap.

This module provides various utility functions for common tasks in
ttkbootstrap applications, including high-DPI support, screen geometry
calculations, and color manipulations.

Functions:
    enable_high_dpi_awareness: Enable high-DPI scaling on Windows/Linux
    detect_scale_factor: Detect the appropriate scale factor for the display
    scale_size: Scale a size value for high-DPI displays
    get_desktop_geometry: Get the screen dimensions
    get_asset_path: Get the path to an asset file

Example:
    ```python
    from ttkbootstrap.utility import enable_high_dpi_awareness
    import ttkbootstrap as ttk

    # Enable high-DPI before creating window
    enable_high_dpi_awareness()

    root = ttk.Window()
    root.mainloop()
    ```
"""


class _ScalingState:
    """Internal class to store global scaling state."""
    _scale_factor: float = 1.0
    _baseline: float = 1.33398982438864281  # Default tk scaling on Windows 96 DPI

    @classmethod
    def set_scale_factor(cls, factor: float):
        """Set the global scale factor."""
        cls._scale_factor = factor

    @classmethod
    def get_scale_factor(cls) -> float:
        """Get the current global scale factor."""
        return cls._scale_factor

    @classmethod
    def get_ui_scale(cls) -> float:
        """Get the UI scale factor (relative to baseline)."""
        return cls._scale_factor / cls._baseline

    @classmethod
    def get_image_scale(cls, source_resolution: float = 2.0) -> float:
        """Get the scale factor for images.

        Args:
            source_resolution: The resolution multiplier of source images.
                For example, 2.0 means images are 2x resolution.

        Returns:
            The scale factor to apply to images.
        """
        return cls.get_ui_scale() / source_resolution


def enable_high_dpi_awareness(root=None, scaling=None):
    """Enable high dpi awareness.

    **Windows OS**
    Call the method BEFORE creating the `Tk` object. No parameters
    required. After the root is created, call again with the root
    parameter to apply detected scaling.

    **Linux OS**
    Must provided the `root` and `scaling` parameters. Call the method
    AFTER creating the `Tk` object. A number between 1.6 and 2.0 is
    usually suffient to scale for high-dpi screen.

    !!! warning
        If the `root` argument is provided, then `scaling` must also
        be provided. Otherwise, there is no effect.

    Parameters:

        root (tk.Tk):
            The root widget

        scaling (float or 'auto'):
            Sets and queries the current scaling factor used by Tk to
            convert between physical units (for example, points,
            inches, or millimeters) and pixels. The number argument is
            a floating point number that specifies the number of pixels
            per point on window's display. If the window argument is
            omitted, it defaults to the main window. If the number
            argument is omitted, the current value of the scaling
            factor is returned.

            If set to 'auto', the scale factor will be detected
            automatically from the system DPI settings.

            A "point" is a unit of measurement equal to 1/72 inch. A
            scaling factor of 1.0 corresponds to 1 pixel per point,
            which is equivalent to a standard 72 dpi monitor. A scaling
            factor of 1.25 would mean 1.25 pixels per point, which is
            the setting for a 90 dpi monitor; setting the scaling factor
            to 1.25 on a 72 dpi monitor would cause everything in the
            application to be displayed 1.25 times as large as normal.
            The initial value for the scaling factor is set when the
            application starts, based on properties of the installed
            monitor, but it can be changed at any time. Measurements
            made after the scaling factor is changed will use the new
            scaling factor, but it is undefined whether existing
            widgets will resize themselves dynamically to accommodate
            the new scaling factor.

    Returns:

        float:
            The scaling factor that was applied, or None if no scaling
            was applied.
    """
    import platform

    # Enable DPI awareness on Windows
    try:
        from ctypes import windll
        # Use shcore for better DPI awareness (Windows 8.1+)
        try:
            windll.shcore.SetProcessDpiAwareness(1)
        except:
            # Fallback to older API
            windll.user32.SetProcessDPIAware()
    except:
        pass

    # Apply scaling if root is provided
    if root:
        # Auto-detect scaling if requested
        if scaling == 'auto':
            scaling = detect_scale_factor(root)

        if scaling:
            try:
                root.tk.call('tk', 'scaling', scaling)
                # Store the scale factor globally
                _ScalingState.set_scale_factor(scaling)
                return scaling
            except:
                pass

    return None


def detect_scale_factor(root):
    """Detect the appropriate scale factor for the display.

    This function attempts to detect the system DPI scaling and return
    an appropriate scale factor for Tk. The scale factor is measured in
    "pixels per point" (72 points per inch).

    Parameters:

        root (tk.Tk):
            The root window (must be created before calling)

    Returns:

        float:
            The detected scale factor in pixels per point
            (e.g., 1.333 for 96 DPI, 2.0 for 144 DPI)
    """
    import platform

    system = platform.system()

    try:
        if system == 'Windows':
            # Try to get scale factor from Windows (Windows 8.1+)
            try:
                from ctypes import windll
                # GetScaleFactorForDevice returns percentage (100, 125, 150, 200, etc.)
                scale_percent = windll.shcore.GetScaleFactorForDevice(0)
                # Convert to DPI: 100% = 96 DPI, 125% = 120 DPI, etc.
                dpi = (96 * scale_percent) / 100
                # Convert to tk scaling (pixels per point, 72 points per inch)
                scale_factor = dpi / 72
                return scale_factor
            except:
                pass

        # Fallback: detect from current DPI
        # This works on Linux, Mac, and older Windows
        current_dpi = root.winfo_fpixels('1i')
        # Tk scaling is pixels per point (72 points per inch)
        scale_factor = current_dpi / 72
        return scale_factor

    except:
        # If all else fails, return default for 96 DPI
        return 96 / 72  # 1.333...


def get_image_name(image):
    """Extract and return the tcl/tk image name from a PhotoImage
    object.

    Parameters:

        image (ImageTk.PhotoImage):
            A photoimage object.

    Returns:

        str:
            The tcl/tk name of the photoimage object.
    """
    return image._PhotoImage__photo.name


def scale_size(widget=None, size=None):
    """Scale the size based on the scaling factor of tkinter.
    This is used most frequently to adjust the assets for
    image-based widget layouts and padding values.

    Can be called in two ways:
    1. scale_size(widget, size) - Legacy mode, calculates from widget
    2. scale_size(size) - Uses global scaling state

    Parameters:

        widget (Widget, optional):
            The widget object. If provided, scaling is calculated from
            the widget's tk instance. If None, uses global scaling state.

        size (Union[int, List, Tuple]):
            A single integer or an iterable of integers

    Returns:

        Union[int, List]:
            An integer or list of integers representing the new size.

    Examples:

        >>> # Using widget (legacy mode)
        >>> scaled = scale_size(my_widget, 10)

        >>> # Using global state (new mode)
        >>> scaled = scale_size(10)
    """
    # Handle both calling conventions
    if widget is not None and size is None:
        # Called as scale_size(size) - widget is actually the size
        size = widget
        factor = _ScalingState.get_ui_scale()
    elif widget is not None and size is not None:
        # Called as scale_size(widget, size) - legacy mode
        BASELINE = _ScalingState._baseline
        scaling = widget.tk.call('tk', 'scaling')
        factor = scaling / BASELINE
    else:
        # Called as scale_size(size=size) - use global state
        factor = _ScalingState.get_ui_scale()

    if isinstance(size, int):
        return int(size * factor)
    elif isinstance(size, tuple) or isinstance(size, list):
        return [int(x * factor) for x in size]
    else:
        return size


# --- Debug helpers ---------------------------------------------------------
def _debug_enabled() -> bool:
    """Return True if debug logging is enabled.

    Controlled via the environment variable `TTKBOOTSTRAP_DEBUG`.
    Accepts: "1", "true", "yes" (case-insensitive) as truthy values.
    """
    import os
    return str(os.environ.get("TTKBOOTSTRAP_DEBUG", "")).lower() in {"1", "true", "yes"}


def debug_log_exception(message: str = "") -> None:
    """Print the current exception traceback if debug is enabled.

    Args:
        message: Optional context message to print before the traceback.
    """
    if not _debug_enabled():
        return
    try:
        import traceback
        if message:
            print(f"TTKBootstrap DEBUG: {message}")
        traceback.print_exc()
    except Exception:
        # Never raise from debug logging
        pass


def center_on_parent(win, parent=None):
    """Center `win` on parent or over its master if not given"""
    win.update_idletasks()  # ensure geometry
    if parent is None:
        parent = getattr(win, 'master', None) or win  # root if no parent

    # parent geometry
    parent.update_idletasks()
    px, py = parent.winfo_rootx(), parent.winfo_rooty()
    pw, ph = parent.winfo_width(), parent.winfo_height()
    if pw <= 1 or ph <= 1:
        # not yet realized, fallback to requested size
        pw, ph = parent.winfo_reqwidth(), parent.winfo_reqheight()

    # window geometry
    ww = win.winfo_width() or win.winfo_reqwidth()
    wh = win.winfo_height() or win.winfo_reqheight()

    x = px + (pw - ww) // 2
    y = py + (ph - wh) // 2
    win.geometry(f"{ww}x{wh}+{x}+{y}")


def clamp(value, min_val, max_val):
    """Return a value that is bounded by a minimum and maximum.

    Args:
        value: The value to evaluate.
        min_val: The minimum allowed value.
        max_val: The maximum allowed value.

    Returns:
        The value, constrained between `min_val` and `max_val`.
    """
    return min(max(value, min_val), max_val)
