"""High-DPI awareness and size-scaling helpers for ttkbootstrap applications."""


def enable_high_dpi_awareness(root=None, scaling=None):
    """Enable high dpi awareness.

    **Windows OS**
    Call the method BEFORE creating the `Tk` object. No parameters
    required.

    **Linux OS**
    Must provided the `root` and `scaling` parameters. Call the method
    AFTER creating the `Tk` object. A number between 1.6 and 2.0 is
    usually suffient to scale for high-dpi screen.

    Warning:
        If the `root` argument is provided, then `scaling` must also
        be provided. Otherwise, there is no effect.

    Parameters:

        root (tk.Tk):
            The root widget

        scaling (float):
            Sets and queries the current scaling factor used by Tk to
            convert between physical units (for example, points,
            inches, or millimeters) and pixels. The number argument is
            a floating point number that specifies the number of pixels
            per point on window's display. If the window argument is
            omitted, it defaults to the main window. If the number
            argument is omitted, the current value of the scaling
            factor is returned.

            A “point” is a unit of measurement equal to 1/72 inch. A
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
    """
    # Keep the existing system-DPI-aware behavior. Per-monitor-v2 awareness
    # requires live style rebuilding when a window crosses displays, which is
    # outside ttkbootstrap's current scaling contract.
    try:
        from ctypes import windll
        try:
            windll.shcore.SetProcessDpiAwareness(1)
        except Exception:
            windll.user32.SetProcessDPIAware()
    except Exception:
        pass

    try:
        if root is not None and scaling is not None:
            root.tk.call('tk', 'scaling', scaling)
    except Exception:
        pass


def scale_size(widget, size):
    """Scale the size based on the scaling factor of tkinter.
    This is used most frequently to adjust the assets for
    image-based widget layouts and pixel-valued geometry.

    `size` is expressed in logical UI units. Conversion uses the scaling
    service attached to the widget's root and rounds half away from zero.

    Parameters:

        widget (Widget):
            The widget object.

        size (int | float | list | tuple):
            A number or sequence of numbers in logical UI units.

    Returns:

        int | list:
            An integer or list of integers representing the new size.
    """
    from ttkbootstrap.style.scaling import Scaling

    return Scaling.for_widget(widget).logical(size)
