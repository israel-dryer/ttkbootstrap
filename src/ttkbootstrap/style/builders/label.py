"""TTK label style recipes."""

from ttkbootstrap.constants import *
from ttkbootstrap.style import StyleBuilderTTK
from ttkbootstrap.style.builders.registry import register_builder


@register_builder("metersubtxt", "label")
def build_meter_subtxt_label_style(builder: StyleBuilderTTK, colorname=DEFAULT):
    """Create a subtext label style for the
    ttkbootstrap.widgets.Meter widget.

    Parameters:

        builder (StyleBuilderTTK):
            The style builder
        colorname (str):
            The color label used to style the widget.
    """
    ttk_class = "Metersubtxt.TLabel"

    if any([colorname == DEFAULT, colorname == ""]):
        ttk_style = ttk_class
        if builder.is_light_theme:
            foreground = builder.colors.secondary
        else:
            foreground = builder.colors.light
    else:
        ttk_style = f"{colorname}.{ttk_class}"
        foreground = builder.colors.get(colorname)

    background = builder.colors.bg

    builder.configure(
        ttk_style, foreground=foreground, background=background
    )
    # register ttkstyle
    builder.register_ttkstyle(ttk_style)


@register_builder("meter", "label")
def build_meter_label_style(builder: StyleBuilderTTK, colorname=DEFAULT):
    """Create a label style for the
    ttkbootstrap.widgets.Meter widget. This style also stores some
    metadata that is called by the Meter class to lookup relevant
    colors for the trough and bar when the new image is drawn.

    Parameters:

        builder (StyleBuilderTTK):
            The style builder
        colorname (str):
            The color label used to style the widget.
    """

    ttk_class = "Meter.TLabel"

    # text color = `foreground`
    # trough color = `space`

    # Recessed neutral trough = border(surface) (bootstack parity).
    trough_color = builder.border(builder.colors.bg)

    if any([colorname == DEFAULT, colorname == ""]):
        ttk_style = ttk_class
        background = builder.colors.bg
        textcolor = builder.colors.primary
    else:
        ttk_style = f"{colorname}.{ttk_class}"
        textcolor = builder.colors.get(colorname)
        background = builder.colors.bg

    builder.configure(
        ttk_style,
        foreground=textcolor,
        background=background,
        space=trough_color,
    )
    # register ttkstyle
    builder.register_ttkstyle(ttk_style)


@register_builder("default", "label")
def build_label_style(builder: StyleBuilderTTK, colorname=DEFAULT):
    """Create a standard style for the ttk.Label widget.

    Parameters:

        builder (StyleBuilderTTK):
            The style builder
        colorname (str):
            The color label used to style the widget.
    """
    ttk_class = "TLabel"
    # The surface the label sits on (2.0 surface-color); default == theme bg.
    surface = builder.resolve_surface(builder._surface)

    if any([colorname == DEFAULT, colorname == ""]):
        ttk_style = builder.surface_prefix(ttk_class)
        foreground = builder.on_surface_fg()
        background = surface
    else:
        ttk_style = builder.surface_prefix(f"{colorname}.{ttk_class}")
        foreground = builder.colors.get(colorname)
        background = surface

    # standard label
    builder.configure(
        ttk_style, foreground=foreground, background=background
    )
    builder.style.map(ttk_style, foreground=[('disabled', builder.disabled("text"))])

    # register ttkstyle
    builder.register_ttkstyle(ttk_style)


@register_builder("inverse", "label")
def build_inverse_label_style(builder: StyleBuilderTTK, colorname=DEFAULT):
    """Create an inverted style for the ttk.Label.

    The foreground and background are inverted versions of that
    used in the standard label style.

    Parameters:

        builder (StyleBuilderTTK):
            The style builder
        colorname (str):
            The color label used to style the widget.
    """
    ttk_class = "Inverse.TLabel"

    if any([colorname == DEFAULT, colorname == ""]):
        ttk_style = ttk_class
        background = builder.colors.fg
        foreground = builder.colors.bg
    else:
        ttk_style = f"{colorname}.{ttk_class}"
        background = builder.colors.get(colorname)
        foreground = builder.on_color(background)

    builder.configure(
        ttk_style, foreground=foreground, background=background
    )
    # register ttkstyle
    builder.register_ttkstyle(ttk_style)
