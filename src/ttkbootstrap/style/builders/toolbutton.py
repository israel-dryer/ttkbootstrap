"""TTK toolbutton style recipes."""

import tkinter as tk

from ttkbootstrap.constants import *
from ttkbootstrap.style import StyleBuilderTTK
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
        selected = builder.colors.primary
    else:
        ttk_style = f"{colorname}.{ttk_class}"
        selected = builder.colors.get(colorname)

    if builder.is_light_theme:
        unselected = builder.colors.border
    else:
        unselected = builder.colors.selectbg

    disabled = builder.disabled()

    on_selected = builder.on_color(selected)
    on_unselected = builder.on_color(unselected)
    on_disabled = builder.disabled("text", disabled)

    builder.configure(
        ttk_style,
        foreground=on_unselected,
        background=unselected,
        relief=tk.FLAT,
        focusthickness=builder.scale_size(1),
        focuscolor=on_unselected,
        padding=builder.scale_size((10, 5)),
        anchor=tk.CENTER,
    )
    builder.style.map(
        ttk_style,
        foreground=[
            ("disabled", on_disabled),
            ("active", on_selected),
            ("selected", on_selected),
        ],
        focuscolor=[
            ("disabled", on_disabled),
            ("active", on_selected),
            ("selected", on_selected),
        ],
        background=[
            ("disabled", disabled),
            ("pressed !disabled", selected),
            ("selected !disabled", selected),
            ("active !disabled", selected),
        ]
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


    if any([colorname == DEFAULT, colorname == ""]):
        ttk_style = ttk_class
        colorname = PRIMARY
    else:
        ttk_style = f"{colorname}.{ttk_class}"

    accent = builder.colors.get(colorname)
    selected = active = pressed = accent
    unselected = builder.colors.bg

    on_selected = on_active = on_pressed = builder.on_color(selected)
    on_unselected = builder.on_color(unselected)
    on_disabled = builder.disabled("text")


    builder.configure(
        ttk_style,
        foreground=accent,
        background=builder.colors.bg,
        bordercolor=accent,
        darkcolor=builder.colors.bg,
        lightcolor=builder.colors.bg,
        relief=tk.RAISED,
        focusthickness=0,
        focuscolor=on_unselected,
        padding=builder.scale_size((10, 5)),
        anchor=tk.CENTER,
    )
    builder.style.map(
        ttk_style,
        foreground=[
            ("disabled", on_disabled),
            ("pressed !disabled", on_pressed),
            ("selected !disabled", on_selected),
            ("active !disabled", on_active),
        ],
        background=[
            ("pressed !disabled", pressed),
            ("selected !disabled", pressed),
            ("active !disabled", active),
        ],
        bordercolor=[
            ("disabled", on_disabled),
            ("pressed !disabled", pressed),
            ("selected !disabled", pressed),
            ("active !disabled", active),
        ],
        darkcolor=[
            ("disabled", builder.colors.bg),
            ("pressed !disabled", pressed),
            ("selected !disabled", pressed),
            ("active !disabled", active),
        ],
        lightcolor=[
            ("disabled", builder.colors.bg),
            ("pressed !disabled", pressed),
            ("selected !disabled", pressed),
            ("active !disabled", active),
        ],
    )
    # register ttkstyle
    builder.register_ttkstyle(ttk_style)
