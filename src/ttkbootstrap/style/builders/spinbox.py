"""TTK spinbox style recipes."""

import tkinter as tk

from ttkbootstrap.constants import *
from ttkbootstrap.style import StyleBuilderTTK
from ttkbootstrap.style.layout import El, image_element, layout
from ttkbootstrap.style.builders.registry import register_builder
from ttkbootstrap.style.builders.utils import simple_arrow_assets


@register_builder("default", "spinbox")
def build_spinbox_style(builder: StyleBuilderTTK, colorname=DEFAULT):
    """Create a style for the ttk.Spinbox widget.

    Parameters:

        builder (StyleBuilderTTK):
            The style builder
        colorname (str):
            The color label used to style the widget.
    """
    ttk_class = "TSpinbox"

    if builder.is_light_theme:
        disabled_fg = builder.colors.border
        border_color = builder.colors.border
        readonly = builder.colors.light
    else:
        disabled_fg = builder.colors.selectbg
        border_color = builder.colors.selectbg
        readonly = border_color

    if any([colorname == DEFAULT, colorname == ""]):
        ttk_style = ttk_class
        focus_color = builder.colors.primary
    else:
        ttk_style = f"{colorname}.{ttk_class}"
        focus_color = builder.colors.get(colorname)

    if all([colorname, colorname != DEFAULT]):
        border_color = focus_color

    if colorname == "light":
        arrow_focus = builder.colors.fg
    else:
        arrow_focus = focus_color

    element = ttk_style.replace(".TS", ".S")
    arrow_images = simple_arrow_assets(builder, builder.colors.inputfg, disabled_fg, arrow_focus, y_offset=2)
    up_arrow_image = arrow_images[0][0]
    up_arrow_disabled_image = arrow_images[1][0]
    up_arrow_focus_image = arrow_images[2][0]
    down_arrow_image = arrow_images[0][1]
    down_arrow_disabled_image = arrow_images[1][1]
    down_arrow_focus_image = arrow_images[2][1]

    # right padding so the carets aren't flush against the border
    arrow_pad = (0, 0, builder.scale_size(6), 0)
    image_element(
        builder.style, f"{element}.uparrow", default=up_arrow_image,
        states={"disabled": up_arrow_disabled_image,
                "pressed !disabled": up_arrow_focus_image,
                "hover !disabled": up_arrow_focus_image},
        padding=arrow_pad)
    image_element(
        builder.style, f"{element}.downarrow", default=down_arrow_image,
        states={"disabled": down_arrow_disabled_image,
                "pressed !disabled": down_arrow_focus_image,
                "hover !disabled": down_arrow_focus_image},
        padding=arrow_pad)
    layout(builder.style, ttk_style,
           El(f"{element}.field", side=tk.TOP, sticky=tk.EW, children=[
               El("null", side=tk.RIGHT, sticky="", children=[
                   El(f"{element}.uparrow", side=tk.TOP, sticky=tk.E),
                   El(f"{element}.downarrow", side=tk.BOTTOM, sticky=tk.E)]),
               El(f"{element}.padding", sticky=tk.NSEW, children=[
                   El(f"{element}.textarea", sticky=tk.NSEW)])]))

    builder.configure(
        ttk_style,
        bordercolor=border_color,
        darkcolor=builder.colors.inputbg,
        lightcolor=builder.colors.inputbg,
        fieldbackground=builder.colors.inputbg,
        foreground=builder.colors.inputfg,
        borderwidth=0,
        background=builder.colors.inputbg,
        relief=tk.FLAT,
        insertcolor=builder.colors.inputfg,
        padding=builder.scale_size((10, 5)),
    )

    builder.style.map(
        ttk_style,
        foreground=[("disabled", disabled_fg)],
        fieldbackground=[("readonly", readonly)],
        background=[("readonly", readonly)],
        lightcolor=[
            ("focus invalid", builder.colors.danger),
            ("focus !disabled", focus_color),
            ("readonly", readonly),
        ],
        darkcolor=[
            ("focus invalid", builder.colors.danger),
            ("focus !disabled", focus_color),
            ("readonly", readonly),
        ],
        bordercolor=[
            ("invalid", builder.colors.danger),
            ("focus !disabled", focus_color),
            ("hover !disabled", focus_color),
        ],
    )

    # register ttk styles
    builder.register_ttkstyle(ttk_style)
