"""TTK toolbutton style recipes."""

import tkinter as tk

from ttkbootstrap.constants import *
from ttkbootstrap.style import StyleBuilderTTK
from ttkbootstrap.style.theme import Colors
from ttkbootstrap.style.builders.registry import register_builder


@register_builder("default", "toolbutton")
def build_toolbutton_style(builder: StyleBuilderTTK, colorname=DEFAULT):
    """Create a solid toolbutton style for the ttk.Checkbutton
    and ttk.Radiobutton widgets.

    Parameters:

        builder (StyleBuilderTTK):
            The style builder
        colorname (str):
            The color label used to style the widget.
    """
    ttk_class = "Toolbutton"

    if any([colorname == DEFAULT, colorname == ""]):
        ttk_style = ttk_class
        toggle_on = builder.colors.primary
    else:
        ttk_style = f"{colorname}.{ttk_class}"
        toggle_on = builder.colors.get(colorname)

    foreground = builder.colors.get_foreground(colorname)

    if builder.is_light_theme:
        toggle_off = builder.colors.border
    else:
        toggle_off = builder.colors.selectbg

    disabled_bg = Colors.make_transparent(0.10, builder.colors.fg, builder.colors.bg)
    disabled_fg = Colors.make_transparent(0.30, builder.colors.fg, builder.colors.bg)

    builder.configure(
        ttk_style,
        foreground=builder.colors.selectfg,
        background=toggle_off,
        bordercolor=toggle_off,
        darkcolor=toggle_off,
        lightcolor=toggle_off,
        relief=tk.RAISED,
        focusthickness=builder.scale_size(1),
        focuscolor=foreground,
        padding=builder.scale_size((10, 5)),
        anchor=tk.CENTER,
    )
    builder.style.map(
        ttk_style,
        foreground=[
            ("disabled", disabled_fg),
            ("hover", foreground),
            ("selected", foreground),
        ],
        focuscolor=[
            ("disabled", disabled_fg),
            ("hover", foreground),
            ("selected", foreground),
        ],
        background=[
            ("disabled", disabled_bg),
            ("pressed !disabled", toggle_on),
            ("selected !disabled", toggle_on),
            ("hover !disabled", toggle_on),
        ],
        bordercolor=[
            ("disabled", disabled_bg),
            ("pressed !disabled", toggle_on),
            ("selected !disabled", toggle_on),
            ("hover !disabled", toggle_on),
        ],
        darkcolor=[
            ("disabled", disabled_bg),
            ("pressed !disabled", toggle_on),
            ("selected !disabled", toggle_on),
            ("hover !disabled", toggle_on),
        ],
        lightcolor=[
            ("disabled", disabled_bg),
            ("pressed !disabled", toggle_on),
            ("selected !disabled", toggle_on),
            ("hover !disabled", toggle_on),
        ],
    )

    # register ttk style
    builder.register_ttkstyle(ttk_style)


@register_builder("outline", "toolbutton")
def build_outline_toolbutton_style(builder: StyleBuilderTTK, colorname=DEFAULT):
    """Create an outline toolbutton style for the ttk.Checkbutton
    and ttk.Radiobutton widgets.

    Parameters:

        builder (StyleBuilderTTK):
            The style builder
        colorname (str):
            The color label used to style the widget.
    """
    ttk_class = "Outline.Toolbutton"

    disabled_fg = Colors.make_transparent(0.30, builder.colors.fg, builder.colors.bg)

    if any([colorname == DEFAULT, colorname == ""]):
        ttk_style = ttk_class
        colorname = PRIMARY
    else:
        ttk_style = f"{colorname}.{ttk_class}"

    foreground = builder.colors.get(colorname)
    background = builder.colors.get_foreground(colorname)
    foreground_pressed = background
    border_color = foreground
    pressed = foreground
    hover = foreground

    builder.configure(
        ttk_style,
        foreground=foreground,
        background=builder.colors.bg,
        bordercolor=border_color,
        darkcolor=builder.colors.bg,
        lightcolor=builder.colors.bg,
        relief=tk.RAISED,
        focusthickness=0,
        focuscolor=foreground,
        padding=builder.scale_size((10, 5)),
        anchor=tk.CENTER,
        arrowcolor=foreground,
        arrowpadding=builder.scale_size((0, 0, 15, 0)),
        arrowsize=builder.scale_size(3),
    )
    builder.style.map(
        ttk_style,
        foreground=[
            ("disabled", disabled_fg),
            ("pressed !disabled", foreground_pressed),
            ("selected !disabled", foreground_pressed),
            ("hover !disabled", foreground_pressed),
        ],
        background=[
            ("pressed !disabled", pressed),
            ("selected !disabled", pressed),
            ("hover !disabled", hover),
        ],
        bordercolor=[
            ("disabled", disabled_fg),
            ("pressed !disabled", pressed),
            ("selected !disabled", pressed),
            ("hover !disabled", hover),
        ],
        darkcolor=[
            ("disabled", builder.colors.bg),
            ("pressed !disabled", pressed),
            ("selected !disabled", pressed),
            ("hover !disabled", hover),
        ],
        lightcolor=[
            ("disabled", builder.colors.bg),
            ("pressed !disabled", pressed),
            ("selected !disabled", pressed),
            ("hover !disabled", hover),
        ],
    )
    # register ttkstyle
    builder.register_ttkstyle(ttk_style)
