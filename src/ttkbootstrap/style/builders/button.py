"""TTK button style recipes."""

import tkinter as tk

from ttkbootstrap.constants import *
from ttkbootstrap.style import StyleBuilderTTK
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
        accent = builder.colors.primary
        on_accent = builder.on_color(accent)
    else:
        ttk_style = f"{colorname}.{ttk_class}"
        accent = builder.colors.get(colorname)
        on_accent = builder.on_color(accent)

    pressed = builder.pressed(accent)
    hover = builder.active(accent)
    disabled = builder.disabled()
    on_disabled = builder.disabled("text", disabled)

    builder.configure(
        ttk_style,
        foreground=on_accent,
        background=accent,
        relief=tk.FLAT,
        focusthickness=builder.scale_size(1),
        focuscolor=on_accent,
        padding=builder.scale_size((10, 5)),
        anchor=tk.CENTER,
    )
    builder.style.map(
        ttk_style,
        foreground=[("disabled", on_disabled)],
        focuscolor=[("disabled", on_disabled)],
        background=[
            ("disabled", disabled),
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


    if any([colorname == DEFAULT, colorname == ""]):
        ttk_style = ttk_class
        colorname = PRIMARY
    else:
        ttk_style = f"{colorname}.{ttk_class}"

    accent = builder.colors.get(colorname)
    pressed = accent
    hover = accent
    border = accent

    on_pressed = builder.on_color(accent)
    on_disabled = builder.disabled("text")

    builder.configure(
        ttk_style,
        foreground=accent,
        background=builder.colors.bg,
        bordercolor=border,
        darkcolor=builder.colors.bg,
        lightcolor=builder.colors.bg,
        relief=tk.RAISED,
        focusthickness=builder.scale_size(1),
        focuscolor=accent,
        padding=builder.scale_size((10, 5)),
        anchor=tk.CENTER,
    )
    builder.style.map(
        ttk_style,
        foreground=[
            ("disabled", on_disabled),
            ("pressed !disabled", on_pressed),
            ("hover !disabled", on_pressed),
        ],
        background=[
            ("pressed !disabled", pressed),
            ("hover !disabled", hover),
        ],
        bordercolor=[
            ("disabled", on_disabled),
            ("pressed !disabled", pressed),
            ("hover !disabled", hover),
        ],
        focuscolor=[
            ("pressed !disabled", on_pressed),
            ("hover !disabled", on_pressed),
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


    if any([colorname == DEFAULT, colorname == ""]):
        on_surface = builder.colors.fg
        ttk_style = style_class
    elif colorname == LIGHT:
        on_surface = builder.colors.fg
        ttk_style = f"{colorname}.{style_class}"
    else:
        on_surface = builder.colors.get(colorname)
        ttk_style = f"{colorname}.{style_class}"

    pressed = builder.colors.info
    hover = builder.colors.info
    on_disabled = builder.disabled("text")

    builder.configure(
        ttk_style,
        foreground=on_surface,
        background=builder.colors.bg,
        relief=tk.FLAT,
        focusthickness=builder.scale_size(1),
        focuscolor=on_surface,
        anchor=tk.CENTER,
        padding=builder.scale_size((10, 5)),
    )
    builder.style.map(
        ttk_style,
        shiftrelief=[("pressed !disabled", builder.scale_size(-1))],
        foreground=[
            ("disabled", on_disabled),
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
        ]
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

    disabled = builder.disabled()
    on_disabled = builder.disabled("text", disabled)

    if any([colorname == DEFAULT, colorname == ""]):
        ttk_style = style_class
        background = builder.colors.primary
        on_background = builder.on_color(background)
    else:
        ttk_style = f"{colorname}.{style_class}"
        background = builder.colors.get(colorname)
        on_background = builder.on_color(background)

    # Calendar icon in the button foreground color.
    size = [21, 22]
    img_normal = builder.assets.icon("calendar3", size, on_background)
    img_disabled = builder.assets.icon("calendar3", size, on_disabled)

    pressed = builder.pressed(background)
    hover = builder.active(background)

    builder.configure(
        ttk_style,
        foreground=on_background,
        background=background,
        relief=tk.FLAT,
        focusthickness=0,
        focuscolor=on_background,
        padding=builder.scale_size((2, 2)),
        anchor=tk.CENTER,
        image=img_normal,
    )
    builder.style.map(
        ttk_style,
        image=[("disabled", img_disabled)],
        foreground=[("disabled", on_disabled)],
        background=[
            ("disabled", disabled),
            ("pressed !disabled", pressed),
            ("hover !disabled", hover),
        ],
        bordercolor=[("disabled", disabled)],
        darkcolor=[
            ("disabled", disabled),
            ("pressed !disabled", pressed),
            ("hover !disabled", hover),
        ],
        lightcolor=[
            ("disabled", disabled),
            ("pressed !disabled", pressed),
            ("hover !disabled", hover),
        ],
    )
    builder.register_ttkstyle(ttk_style)
