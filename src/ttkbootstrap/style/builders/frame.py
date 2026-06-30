"""TTK frame style recipes."""

from ttkbootstrap.constants import *
from ttkbootstrap.style import StyleBuilderTTK
from ttkbootstrap.style.builders.registry import register_builder


@register_builder("default", "frame")
def build_frame_style(builder: StyleBuilderTTK, colorname=DEFAULT):
    """Create a style for the ttk.Frame widget.

    Parameters:

        builder (StyleBuilderTTK):
            The style builder
        colorname (str):
            The color label used to style the widget.
    """
    ttk_class = "TFrame"

    if any([colorname == DEFAULT, colorname == ""]):
        ttk_style = ttk_class
        background = builder.colors.bg
    else:
        ttk_style = f"{colorname}.{ttk_class}"
        background = builder.colors.get(colorname)

    builder.configure(ttk_style, background=background)

    # register style
    builder.register_ttkstyle(ttk_style)
