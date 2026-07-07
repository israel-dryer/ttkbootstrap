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
        chevron_style = "Chevron.TButton"
    else:
        accent = builder.colors.get(colorname)
        ttk_style = f"{colorname}.{ttk_class}"
        chevron_style = f"Chevron.{colorname}.TButton"

    on_disabled = builder.disabled("text")
    pressed = builder.pressed(accent)
    active = builder.active(accent)
    on_pressed = builder.on_color(pressed)
    on_active = builder.on_color(active)

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
            ("pressed !disabled", on_pressed),
            ("selected !disabled", on_pressed),
            ("hover !disabled", on_active),
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
            ("pressed !disabled", on_pressed),
            ("selected !disabled", on_pressed),
            ("hover !disabled", on_active),
        ]
    )
    # The prev/next chevrons sit on the accent-colored title bar. Style them as
    # ghost buttons: blend into the header (no border, no fill of their own, no
    # padding) with a subtle darken/lighten on hover/press.
    builder.configure(
        chevron_style,
        font="-size 12",
        foreground=builder.on_color(accent),
        focuscolor='',
        background=accent,
        relief=tk.FLAT,
        padding=builder.scale_size(4),
        anchor=tk.CENTER,
    )
    chevron_states = [
        ("pressed !disabled", pressed),
        ("hover !disabled", active),
    ]
    builder.style.map(
        chevron_style,
        background=chevron_states,
        bordercolor=chevron_states,
        darkcolor=chevron_states,
        lightcolor=chevron_states,
    )

    # register ttk_style
    builder.register_ttkstyle(ttk_style)
    builder.register_ttkstyle(chevron_style)
