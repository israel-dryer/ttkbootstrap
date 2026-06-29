"""Shared private helpers used by multiple ttk recipe families."""

def indicator_spacer(builder):
    """Return the shared transparent image used between indicator and label."""
    size = builder.scale_size((6, 1))

    def draw_spacer(_draw, _width, _height):
        pass

    return builder.assets.image(size, draw_spacer, "indicator-spacer")


def simple_arrow_assets(builder, arrowcolor: str, disabledcolor: str, activecolor: str, y_offset: int = 0):
    """Create caret arrow assets using Bootstrap Icons glyphs.

    Used for Combobox and Spinbox indicators. Uses the solid `caret-*-fill`
    triangles so the indicators read consistently with the filled-triangle
    arrows elsewhere in the app (menubutton, datepicker header).

    The `y_offset` parameter is accepted for API compatibility but is no
    longer used (it was specific to the old hand-drawn triangle approach).

    Args:
        arrowcolor: The color value to use as the arrow fill color.
        disabledcolor: A second color value to use when the arrow is disabled.
        activecolor: A third color value to use when the arrow has focus.
        y_offset: Accepted for API compatibility; ignored.
    Returns:
        A nested tuple (normal, disabled, active), each a 4-tuple of Tcl
        image names in the order (up, down, left, right).
    """
    a = builder.assets
    size = builder.scale_size([13, 11])

    def make_arrows(color):
        up = a.icon("caret-up-fill", size, color)
        down = a.icon("caret-down-fill", size, color)
        left = a.icon("caret-left-fill", size, color)
        right = a.icon("caret-right-fill", size, color)
        return up, down, left, right

    return make_arrows(arrowcolor), make_arrows(disabledcolor), make_arrows(activecolor)
