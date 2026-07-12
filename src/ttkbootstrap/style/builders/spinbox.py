"""TTK spinbox style recipes."""

import tkinter as tk

from ttkbootstrap.constants import *
from ttkbootstrap.style import StyleBuilderTTK
from ttkbootstrap.style.layout import El, image_element, layout
from ttkbootstrap.style.builders.registry import register_builder


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

    border_color = builder.colors.border
    # readonly fields read like normal fields (no greyed box).
    readonly = builder.colors.inputbg
    disabled_fg = builder.disabled("text", builder.colors.inputbg)

    if any([colorname == DEFAULT, colorname == ""]):
        ttk_style = ttk_class
        focus_color = builder.colors.primary
    else:
        ttk_style = f"{colorname}.{ttk_class}"
        focus_color = builder.colors.get(colorname)

    element = ttk_style.replace(".TS", ".S")
    # The carets keep one fixed color in every state (no focus/hover/pressed/
    # disabled recolor) so they read as steady glyphs rather than reacting to
    # field state.
    a = builder.assets
    arrow_size = [12, 10]
    up_arrow_image = a.icon("caret-up-fill", arrow_size, builder.colors.inputfg)
    down_arrow_image = a.icon("caret-down-fill", arrow_size, builder.colors.inputfg)

    image_element(builder.style, f"{element}.uparrow", default=up_arrow_image)
    image_element(builder.style, f"{element}.downarrow", default=down_arrow_image)

    # A transparent spacer pinned to the right edge so the carets aren't flush
    # against the border. clam ignores an outer `-padding` on a packed image
    # element (the arrows sit outside the field's padded region), so the gap has
    # to be a real element rather than element padding.
    gap = builder.scale_size(3) or 1
    image_element(
        builder.style, f"{element}.arrowgap",
        default=builder.assets.image((gap, 1), lambda *_: None, "spinbox-arrowgap"),
        sticky=tk.NS)
    layout(builder.style, ttk_style,
           El(f"{element}.field", side=tk.TOP, sticky=tk.EW, children=[
               El(f"{element}.arrowgap", side=tk.RIGHT, sticky=tk.NS),
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
        ],
    )

    # register ttk styles
    builder.register_ttkstyle(ttk_style)
