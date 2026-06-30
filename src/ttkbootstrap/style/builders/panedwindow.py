"""TTK panedwindow style recipes."""

from ttkbootstrap.constants import *
from ttkbootstrap.style import StyleBuilderTTK
from ttkbootstrap.style.builders.registry import register_builder


@register_builder("default", "panedwindow")
def build_panedwindow_style(builder: StyleBuilderTTK, colorname=DEFAULT):
    """Create a standard style for the ttk.Panedwindow widget.

    Parameters:

        builder (StyleBuilderTTK):
            The style builder
        colorname (str):
            The color label used to style the widget.
    """
    h_ttk_class = "Horizontal.TPanedwindow"
    v_ttk_class = "Vertical.TPanedwindow"

    if builder.is_light_theme:
        default_color = builder.colors.border
    else:
        default_color = builder.colors.selectbg

    if any([colorname == DEFAULT, colorname == ""]):
        sash_color = default_color
        h_ttk_style = h_ttk_class
        v_ttk_style = v_ttk_class
    else:
        sash_color = builder.colors.get(colorname)
        h_ttk_style = f"{colorname}.{h_ttk_class}"
        v_ttk_style = f"{colorname}.{v_ttk_class}"

    builder.configure(
        "Sash", gripcount=0, sashthickness=builder.scale_size(2)
    )
    builder.configure(h_ttk_style, background=sash_color)
    builder.configure(v_ttk_style, background=sash_color)

    # register ttkstyle
    builder.register_ttkstyle(h_ttk_style)
    builder.register_ttkstyle(v_ttk_style)
