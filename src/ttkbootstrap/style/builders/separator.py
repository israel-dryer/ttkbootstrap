"""TTK separator style recipes."""

import tkinter as tk

from ttkbootstrap.constants import *
from ttkbootstrap.style import StyleBuilderTTK
from ttkbootstrap.style.layout import El, layout
from ttkbootstrap.style.builders.registry import register_builder


@register_builder("default", "separator")
def build_separator_style(builder: StyleBuilderTTK, accent=DEFAULT):
    """Create a style for the ttk.Separator widget.

    Parameters:

        builder (StyleBuilderTTK):
            The style builder
        accent (str):
            The primary widget color.
    """
    h_ttk_class = "Horizontal.TSeparator"
    v_ttk_class = "Vertical.TSeparator"

    h_size = [40, 1]
    v_size = [1, 40]

    # style colors
    if builder.is_light_theme:
        default_color = builder.colors.border
    else:
        default_color = builder.colors.selectbg

    if any([accent == DEFAULT, accent == ""]):
        background = default_color
        h_ttk_style = h_ttk_class
        v_ttk_style = v_ttk_class
    else:
        background = builder.colors.get(accent)
        h_ttk_style = f"{accent}.{h_ttk_class}"
        v_ttk_style = f"{accent}.{v_ttk_class}"

    a = builder.assets

    # horizontal separator
    h_element = h_ttk_style.replace(".TS", ".S")
    h_name = a.rect(background, h_size)
    builder.style.element_create(f"{h_element}.separator", "image", h_name)
    layout(builder.style, h_ttk_style,
           El(f"{h_element}.separator", sticky=tk.EW))

    # vertical separator
    v_element = v_ttk_style.replace(".TS", ".S")
    v_name = a.rect(background, v_size)
    builder.style.element_create(f"{v_element}.separator", "image", v_name)
    layout(builder.style, v_ttk_style,
           El(f"{v_element}.separator", sticky=tk.NS))

    builder.register_ttkstyle(h_ttk_style)
    builder.register_ttkstyle(v_ttk_style)
