"""TTK button style recipes."""

import tkinter as tk

from ttkbootstrap.constants import *
from ttkbootstrap.style import StyleBuilderTTK
from ttkbootstrap.style.theme import Colors
from ttkbootstrap.style.builders.registry import register_builder


@register_builder("default", "button")
def build_button_style(builder: StyleBuilderTTK, colorname=DEFAULT):
    """Create a solid style for the ttk.Button widget.

    Parameters:

        builder (StyleBuilderTTK):
            The style builder
        colorname (str):
            The color label used to style the widget.
    """
    ttk_class = "TButton"

    if any([colorname == DEFAULT, colorname == ""]):
        ttk_style = ttk_class
        foreground = builder.colors.get_foreground(PRIMARY)
        background = builder.colors.primary
    else:
        ttk_style = f"{colorname}.{ttk_class}"
        foreground = builder.colors.get_foreground(colorname)
        background = builder.colors.get(colorname)

    border_color = background
    disabled_bg = Colors.make_transparent(0.10, builder.colors.fg, builder.colors.bg)
    disabled_fg = Colors.make_transparent(0.30, builder.colors.fg, builder.colors.bg)
    pressed = Colors.make_transparent(0.80, background, builder.colors.bg)
    hover = Colors.make_transparent(0.90, background, builder.colors.bg)

    builder.configure(
        ttk_style,
        foreground=foreground,
        background=background,
        bordercolor=border_color,
        darkcolor=background,
        lightcolor=background,
        relief=tk.RAISED,
        focusthickness=builder.scale_size(1),
        focuscolor=foreground,
        padding=builder.scale_size((10, 5)),
        anchor=tk.CENTER,
    )
    builder.style.map(
        ttk_style,
        foreground=[("disabled", disabled_fg)],
        focuscolor=[("disabled", disabled_fg)],
        background=[
            ("disabled", disabled_bg),
            ("pressed !disabled", pressed),
            ("hover !disabled", hover),
        ],
        bordercolor=[("disabled", disabled_bg)],
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
    # register ttkstyle
    builder.register_ttkstyle(ttk_style)


@register_builder("outline", "button")
def build_outline_button_style(builder: StyleBuilderTTK, colorname=DEFAULT):
    """Create an outline style for the ttk.Button widget.

    Parameters:

        builder (StyleBuilderTTK):
            The style builder
        colorname (str):
            The color label used to style the widget.
    """
    ttk_class = "Outline.TButton"

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
        focusthickness=builder.scale_size(1),
        focuscolor=foreground,
        padding=builder.scale_size((10, 5)),
        anchor=tk.CENTER,
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
            ("pressed !disabled", pressed),
            ("hover !disabled", hover),
        ],
        focuscolor=[
            ("pressed !disabled", foreground_pressed),
            ("hover !disabled", foreground_pressed),
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
    # register ttkstyle
    builder.register_ttkstyle(ttk_style)


@register_builder("link", "button")
def build_link_button_style(builder: StyleBuilderTTK, colorname=DEFAULT):
    """Create a link button style for the ttk.Button widget.

    Parameters:

        builder (StyleBuilderTTK):
            The style builder
        colorname (str):
            The color label used to style the widget.
    """
    style_class = "Link.TButton"

    pressed = builder.colors.info
    hover = builder.colors.info

    if any([colorname == DEFAULT, colorname == ""]):
        foreground = builder.colors.fg
        ttk_style = style_class
    elif colorname == LIGHT:
        foreground = builder.colors.fg
        ttk_style = f"{colorname}.{style_class}"
    else:
        foreground = builder.colors.get(colorname)
        ttk_style = f"{colorname}.{style_class}"

    disabled_fg = Colors.make_transparent(0.30, builder.colors.fg, builder.colors.bg)

    builder.configure(
        ttk_style,
        foreground=foreground,
        background=builder.colors.bg,
        bordercolor=builder.colors.bg,
        darkcolor=builder.colors.bg,
        lightcolor=builder.colors.bg,
        relief=tk.RAISED,
        focusthickness=builder.scale_size(1),
        focuscolor=foreground,
        anchor=tk.CENTER,
        padding=builder.scale_size((10, 5)),
    )
    builder.style.map(
        ttk_style,
        shiftrelief=[("pressed !disabled", builder.scale_size(-1))],
        foreground=[
            ("disabled", disabled_fg),
            ("pressed !disabled", pressed),
            ("hover !disabled", hover),
        ],
        focuscolor=[
            ("pressed !disabled", pressed),
            ("hover !disabled", pressed),
        ],
        background=[
            ("disabled", builder.colors.bg),
            ("pressed !disabled", builder.colors.bg),
            ("hover !disabled", builder.colors.bg),
        ],
        bordercolor=[
            ("disabled", builder.colors.bg),
            ("pressed !disabled", builder.colors.bg),
            ("hover !disabled", builder.colors.bg),
        ],
        darkcolor=[
            ("disabled", builder.colors.bg),
            ("pressed !disabled", builder.colors.bg),
            ("hover !disabled", builder.colors.bg),
        ],
        lightcolor=[
            ("disabled", builder.colors.bg),
            ("pressed !disabled", builder.colors.bg),
            ("hover !disabled", builder.colors.bg),
        ],
    )
    # register ttkstyle
    builder.register_ttkstyle(ttk_style)


@register_builder("date", "button")
def build_date_button_style(builder: StyleBuilderTTK, colorname=DEFAULT):
    """Create a date button style for the ttk.Button widget.

    Parameters:

        builder (StyleBuilderTTK):
            The style builder
        colorname (str):
            The color label used to style widget.
    """
    style_class = "Date.TButton"

    if builder.is_light_theme:
        disabled_fg = builder.colors.border
    else:
        disabled_fg = builder.colors.selectbg

    if any([colorname == DEFAULT, colorname == ""]):
        ttk_style = style_class
        foreground = builder.colors.get_foreground(PRIMARY)
        background = builder.colors.primary
        btn_foreground = Colors.get_foreground(builder.colors, PRIMARY)
    else:
        ttk_style = f"{colorname}.{style_class}"
        foreground = builder.colors.get_foreground(colorname)
        background = builder.colors.get(colorname)
        btn_foreground = Colors.get_foreground(builder.colors, colorname)

    # Calendar icon in the button foreground color.
    size = [21, 22]
    img_normal = builder.assets.icon("calendar3", size, btn_foreground)

    pressed = Colors.update_hsv(background, vd=-0.1)
    hover = Colors.update_hsv(background, vd=0.10)

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
        padding=builder.scale_size((2, 2)),
        anchor=tk.CENTER,
        image=img_normal,
    )
    builder.style.map(
        ttk_style,
        foreground=[("disabled", disabled_fg)],
        background=[
            ("disabled", disabled_fg),
            ("pressed !disabled", pressed),
            ("hover !disabled", hover),
        ],
        bordercolor=[("disabled", disabled_fg)],
        darkcolor=[
            ("disabled", disabled_fg),
            ("pressed !disabled", pressed),
            ("hover !disabled", hover),
        ],
        lightcolor=[
            ("disabled", disabled_fg),
            ("pressed !disabled", pressed),
            ("hover !disabled", hover),
        ],
    )
    builder.register_ttkstyle(ttk_style)
