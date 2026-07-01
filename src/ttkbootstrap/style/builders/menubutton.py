"""TTK menubutton style recipes."""

import tkinter as tk

from ttkbootstrap.constants import *
from ttkbootstrap.style import StyleBuilderTTK
from ttkbootstrap.style.layout import El, image_element, layout
from ttkbootstrap.style.builders.registry import register_builder
from ttkbootstrap.style.builders.utils import simple_arrow_assets


@register_builder("default", "menubutton")
def build_menubutton_style(builder: StyleBuilderTTK, colorname=DEFAULT):
    """Create a solid style for the ttk.Menubutton widget.

    Parameters:

        builder (StyleBuilderTTK):
            The style builder
        colorname (str):
            The color label used to style the widget.
    """
    ttk_class = "TMenubutton"

    if any([colorname == DEFAULT, colorname == ""]):
        ttk_style = ttk_class
        background = builder.colors.primary
        foreground = builder.on_color(background)
    else:
        ttk_style = f"{colorname}.{ttk_class}"
        background = builder.colors.get(colorname)
        foreground = builder.on_color(background)

    disabled_bg = builder.disabled()
    disabled_fg = builder.disabled("text", disabled_bg)
    pressed = builder.pressed(background)
    hover = builder.active(background)

    builder.configure(
        ttk_style,
        foreground=foreground,
        background=background,
        bordercolor=background,
        darkcolor=background,
        lightcolor=background,
        relief=tk.RAISED,
        focusthickness=0,
        focuscolor=foreground,
        padding=builder.scale_size((10, 5)),
    )
    builder.style.map(
        ttk_style,
        foreground=[("disabled", disabled_fg)],
        background=[
            ("disabled", disabled_bg),
            ("pressed !disabled", pressed),
            ("hover !disabled", hover),
        ],
        bordercolor=[
            ("disabled", disabled_bg),
            ("pressed !disabled", pressed),
            ("hover !disabled", hover),
        ],
        darkcolor=[
            ("disabled", disabled_bg),
            ("pressed !disabled", pressed),
            ("hover !disabled", hover),
        ],
        lightcolor=[
            ("disabled", disabled_bg),
            ("pressed !disabled", pressed),
            ("hover !disabled", hover),
        ],
    )
    # caret-down-fill indicator (replaces the native clam triangle); the
    # solid menubutton arrow keeps one color (only the background changes on
    # hover), so just a normal + disabled image.
    _build_menubutton_arrow(builder, ttk_style, foreground, disabled_fg, foreground)

    # register ttkstyle
    builder.register_ttkstyle(ttk_style)


def _build_menubutton_arrow(builder: StyleBuilderTTK, ttk_style, normal, disabled, active):
    """Build the caret-down indicator element + layout for a Menubutton style.

    Replaces ttk's native `Menubutton.indicator` triangle with a Bootstrap
    `caret-down-fill` image element so the menubutton arrow matches the
    caret-fill arrows used elsewhere. `normal`/`disabled`/`active` are the
    arrow colors per state (`active` == `normal` when the arrow does not
    recolor on hover/press).
    """
    arrows = simple_arrow_assets(builder, normal, disabled, active)
    down, down_disabled, down_active = arrows[0][1], arrows[1][1], arrows[2][1]
    image_element(
        builder.style, f"{ttk_style}.indicator", default=down,
        states={"disabled": down_disabled,
                "pressed !disabled": down_active,
                "hover !disabled": down_active},
        sticky="", padding=(0, 0, builder.scale_size(10), 0))
    layout(builder.style, ttk_style,
           El("Menubutton.border", sticky=NSEW, children=[
            El("Menubutton.focus", sticky=NSEW, children=[
                El(f"{ttk_style}.indicator", side=tk.RIGHT, sticky=""),
                El("Menubutton.padding", sticky=tk.EW, children=[
                    El("Menubutton.label", side=LEFT, sticky="")])])]))


@register_builder("outline", "menubutton")
def build_outline_menubutton_style(builder: StyleBuilderTTK, colorname=DEFAULT):
    """Create an outline button style for the ttk.Menubutton widget

    Parameters:

        builder (StyleBuilderTTK):
            The style builder
        colorname (str):
            The color label used to style the widget.
    """
    ttk_class = "Outline.TMenubutton"

    disabled_fg = builder.disabled("text")

    if any([colorname == DEFAULT, colorname == ""]):
        ttk_style = ttk_class
        colorname = PRIMARY
    else:
        ttk_style = f"{colorname}.{ttk_class}"

    foreground = builder.colors.get(colorname)
    background = builder.on_color(foreground)
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
    )
    builder.style.map(
        ttk_style,
        foreground=[
            ("disabled", disabled_fg),
            ("pressed !disabled", foreground_pressed),
            ("hover !disabled", foreground_pressed),
        ],
        background=[
            ("pressed !disabled", pressed),
            ("hover !disabled", hover),
        ],
        bordercolor=[
            ("disabled", disabled_fg),
            ("pressed", pressed),
            ("hover", hover),
        ],
        darkcolor=[
            ("pressed !disabled", pressed),
            ("hover !disabled", hover),
        ],
        lightcolor=[
            ("pressed !disabled", pressed),
            ("hover !disabled", hover),
        ],
    )

    # caret-down-fill indicator; the outline arrow recolors on hover/press
    # (foreground -> the contrasting fill color), so pass that as `active`.
    _build_menubutton_arrow(builder, ttk_style, foreground, disabled_fg, foreground_pressed)

    # register ttkstyle1
    builder.register_ttkstyle(ttk_style)
