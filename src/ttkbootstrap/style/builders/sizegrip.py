"""TTK sizegrip style recipes."""

import tkinter as tk

from ttkbootstrap.constants import *
from ttkbootstrap.style import StyleBuilderTTK
from ttkbootstrap.style.builders.registry import register_builder


@register_builder("default", "sizegrip")
def build_sizegrip_style(builder: StyleBuilderTTK, colorname=DEFAULT):
    """Create a style for the ttk.Sizegrip widget.

    Parameters:

        builder (StyleBuilderTTK):
            The style builder
        colorname (str):
            The color label used to style the widget.
    """
    ttk_class = "TSizegrip"

    if any([colorname == DEFAULT, colorname == ""]):
        ttk_style = ttk_class

        if builder.is_light_theme:
            grip_color = builder.colors.border
        else:
            grip_color = builder.colors.inputbg
    else:
        ttk_style = f"{colorname}.{ttk_class}"
        grip_color = builder.colors.get(colorname)

    # Visual-check item: `grip-horizontal` vs a corner-grip glyph -- settle
    # on the human spot-check.
    size = 16
    image = builder.assets.icon("grip-horizontal", size, grip_color)

    builder.style.element_create(
        f"{ttk_style}.Sizegrip.sizegrip", "image", image
    )
    builder.style.layout(
        ttk_style,
        [
            (
                f"{ttk_style}.Sizegrip.sizegrip",
                {"side": tk.BOTTOM, "sticky": tk.SE},
            )
        ],
    )
    # register ttk style
    builder.register_ttkstyle(ttk_style)
