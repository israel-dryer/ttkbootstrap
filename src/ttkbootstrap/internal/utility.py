"""Internal utility helpers for ttkbootstrap.

These are implementation details with no backward-compatibility guarantee.
Public utility functions (`enable_high_dpi_awareness`, `scale_size`) live in
the `ttkbootstrap.utils` package.
"""


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