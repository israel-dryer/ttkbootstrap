"""TTK calendar style recipes."""

import tkinter as tk

from ttkbootstrap.constants import *
from ttkbootstrap.style import StyleBuilderTTK
from ttkbootstrap.style.layout import El, layout
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
        accent = builder.colors.primary
        ttk_style = ttk_class
    else:
        accent = builder.colors.get(colorname)
        ttk_style = f"{colorname}.{ttk_class}"

    on_disabled = builder.disabled("text")
    active = builder.mute(accent, builder.colors.bg, 0.16)
    pressed = builder.mute(accent, builder.colors.bg, 0.26)

    builder.configure(
        ttk_style,
        foreground=builder.colors.fg,
        background=builder.colors.bg,
        bordercolor=builder.colors.bg,
        darkcolor=builder.colors.bg,
        lightcolor=builder.colors.bg,
        focuscolor=builder.colors.fg,
        borderwidth=builder.scale_size(1),
        padding=builder.scale_size(4),
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
            ("disabled", on_disabled),
        ],
        background=[
            ("pressed !disabled", pressed),
            ("selected !disabled", pressed),
            ("hover !disabled", active),
        ],
        bordercolor=[
            ("disabled", on_disabled),
            ("pressed !disabled", pressed),
            ("selected !disabled", pressed),
            ("hover !disabled", active),
        ],
        darkcolor=[
            ("pressed !disabled", pressed),
            ("selected !disabled", pressed),
            ("hover !disabled", active),
        ],
        lightcolor=[
            ("pressed !disabled", pressed),
            ("selected !disabled", pressed),
            ("hover !disabled", active),
        ],
        focuscolor=[
            ("disabled", on_disabled),
        ]
    )

    builder.register_ttkstyle(ttk_style)
