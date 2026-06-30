"""TTK calendar style recipes."""

import tkinter as tk

from ttkbootstrap.constants import *
from ttkbootstrap.style import StyleBuilderTTK
from ttkbootstrap.style.layout import El, layout
from ttkbootstrap.style.theme import Colors
from ttkbootstrap.style.builders.registry import register_builder


@register_builder("default", "calendar")
def build_calendar_style(builder: StyleBuilderTTK, colorname=DEFAULT):
    """Create a style for the
    ttkbootstrap.dialogs.DatePickerPopup widget.

    Parameters:

        builder (StyleBuilderTTK):
            The style builder
        colorname (str):
            The color label used to style the widget.
    """

    ttk_class = "TCalendar"

    if any([colorname == DEFAULT, colorname == ""]):
        prime_color = builder.colors.primary
        ttk_style = ttk_class
        chevron_style = "Chevron.TButton"
    else:
        prime_color = builder.colors.get(colorname)
        ttk_style = f"{colorname}.{ttk_class}"
        chevron_style = f"Chevron.{colorname}.TButton"

    if builder.is_light_theme:
        disabled_fg = Colors.update_hsv(builder.colors.inputbg, vd=-0.2)
        pressed = Colors.update_hsv(prime_color, vd=-0.1)
    else:
        disabled_fg = Colors.update_hsv(builder.colors.inputbg, vd=-0.3)
        pressed = Colors.update_hsv(prime_color, vd=0.1)

    builder.configure(
        ttk_style,
        foreground=builder.colors.fg,
        background=builder.colors.bg,
        bordercolor=builder.colors.bg,
        darkcolor=builder.colors.bg,
        lightcolor=builder.colors.bg,
        relief=tk.RAISED,
        focusthickness=builder.scale_size(1),
        focuscolor=builder.colors.fg,
        borderwidth=builder.scale_size(1),
        padding=builder.scale_size((10, 5)),
        anchor=tk.CENTER,
    )
    layout(builder.style, ttk_style,
           El("Toolbutton.border", sticky=tk.NSEW, children=[
               El("Toolbutton.focus", sticky=tk.NSEW, children=[
                   El("Toolbutton.padding", sticky=tk.NSEW, children=[
                       El("Toolbutton.label", sticky=tk.NSEW)])])]))

    builder.style.map(
        ttk_style,
        foreground=[
            ("disabled", disabled_fg),
            ("pressed !disabled", builder.colors.selectfg),
            ("selected !disabled", builder.colors.selectfg),
            ("hover !disabled", builder.colors.selectfg),
        ],
        background=[
            ("pressed !disabled", pressed),
            ("selected !disabled", pressed),
            ("hover !disabled", pressed),
        ],
        bordercolor=[
            ("disabled", disabled_fg),
            ("pressed !disabled", pressed),
            ("selected !disabled", pressed),
            ("hover !disabled", pressed),
        ],
        darkcolor=[
            ("pressed !disabled", pressed),
            ("selected !disabled", pressed),
            ("hover !disabled", pressed),
        ],
        lightcolor=[
            ("pressed !disabled", pressed),
            ("selected !disabled", pressed),
            ("hover !disabled", pressed),
        ],
        focuscolor=[
            ("disabled", disabled_fg),
            ("pressed !disabled", builder.colors.selectfg),
            ("selected !disabled", builder.colors.selectfg),
            ("hover !disabled", builder.colors.selectfg),
        ]
    )
    builder.configure(chevron_style, font="-size 14")

    # register ttk_style
    builder.register_ttkstyle(ttk_style)
    builder.register_ttkstyle(chevron_style)
