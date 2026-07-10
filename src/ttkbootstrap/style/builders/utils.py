"""Shared private helpers used by multiple ttk recipe families."""

from ttkbootstrap.constants import NEUTRAL


def default_button_fill(builder, base=None):
    """Return the fill for a bare (no-color) button/menubutton.

    Reads the Style's `default_button` setting (default `"neutral"`): returns
    the neutral elevation fill for `"neutral"`, or the resolved accent color
    for any other color name. `base` (2.0 surface-color) is the surface the
    neutral fill elevates from; defaults to the theme background.
    """
    color = getattr(builder.style, "default_button", NEUTRAL)
    if color == NEUTRAL:
        return neutral_fill(builder, base=base)
    return builder.colors.get(color)


def neutral_fill(builder, level=1, base=None):
    """Return a mode-aware elevation of a surface color.

    Darkens the surface in a light theme, lightens it in a dark theme, so an
    unaccented control reads as a subtly raised surface in either mode. `level`
    1 (~6%) is the quiet neutral fill; `level` 2 (~12%) is a stronger raise used
    to distinguish an "on"/selected neutral state from the "off" fill. `base`
    (2.0 surface-color) is the surface to elevate from; defaults to the theme
    background.
    """
    weight = level * 0.06
    surface = builder.colors.bg if base is None else base
    if builder.is_light_theme:
        return builder.shade(surface, weight)
    return builder.tint(surface, weight)


def indicator_spacer(builder):
    """Return the shared transparent image used between indicator and label."""
    size = (6, 1)

    def draw_spacer(_draw, _width, _height):
        pass

    return builder.assets.image(size, draw_spacer, "indicator-spacer")


def simple_arrow_assets(builder, arrowcolor: str, disabledcolor: str, activecolor: str, y_offset: int = 0):
    """Create caret arrow assets using Bootstrap Icons glyphs.

    Used for Combobox and Spinbox indicators. Renders the solid `caret-*-fill`
    triangles for up/down/left/right in each of the given colors.

    Parameters:
        arrowcolor: The color value to use as the arrow fill color.
        disabledcolor: A second color value to use when the arrow is disabled.
        activecolor: A third color value to use when the arrow has focus.
        y_offset: Accepted for API compatibility; ignored.

    Returns:
        A nested tuple (normal, disabled, active), each a 4-tuple of Tcl
        image names in the order (up, down, left, right).
    """
    a = builder.assets
    size = [13, 11]

    def make_arrows(color):
        up = a.icon("caret-up-fill", size, color)
        down = a.icon("caret-down-fill", size, color)
        left = a.icon("caret-left-fill", size, color)
        right = a.icon("caret-right-fill", size, color)
        return up, down, left, right

    return make_arrows(arrowcolor), make_arrows(disabledcolor), make_arrows(activecolor)
