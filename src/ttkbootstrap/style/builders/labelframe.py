"""TTK labelframe style recipes."""

import tkinter as tk

from ttkbootstrap.constants import *
from ttkbootstrap.style import StyleBuilderTTK
from ttkbootstrap.style.builders.registry import register_builder


@register_builder("default", "labelframe")
def build_labelframe_style(builder: StyleBuilderTTK, colorname=DEFAULT):
    """Create a style for the ttk.Labelframe widget.

    Parameters:

        builder (StyleBuilderTTK):
            The style builder
        colorname (str):
            The color label used to style the widget.
    """
    style_class = "TLabelframe"

    background = builder.colors.bg

    if any([colorname == DEFAULT, colorname == ""]):
        foreground = builder.colors.fg
        ttk_style = style_class

        if builder.is_light_theme:
            border_color = builder.colors.border
        else:
            border_color = builder.colors.selectbg

    else:
        foreground = builder.colors.get(colorname)
        border_color = foreground
        ttk_style = f"{colorname}.{style_class}"

    # create widget style
    builder.configure(
        f"{ttk_style}.Label",
        foreground=foreground,
        background=background,
    )
    builder.configure(
        ttk_style,
        relief=tk.RAISED,
        borderwidth=1,
        bordercolor=border_color,
        lightcolor=background,
        darkcolor=background,
        background=background,
    )
    # register ttkstyle
    builder.register_ttkstyle(ttk_style)
