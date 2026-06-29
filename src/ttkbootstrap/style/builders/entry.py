"""TTK entry style recipes."""

from ttkbootstrap.constants import *
from ttkbootstrap.style import StyleBuilderTTK
from ttkbootstrap.style.builders.registry import register_builder


@register_builder("default", "entry")
def build_entry_style(builder: StyleBuilderTTK, colorname=DEFAULT):
    """Create a style for the ttk.Entry widget.

    Parameters:

        builder:
            The style builder
        colorname (str):
            The color label used to style the widget.
    """
    style_class = "TEntry"

    # general default colors
    if builder.is_light_theme:
        disabled_fg = builder.colors.border
        border_color = builder.colors.border
        readonly = builder.colors.light
    else:
        disabled_fg = builder.colors.selectbg
        border_color = builder.colors.selectbg
        readonly = border_color

    if any([colorname == DEFAULT, not colorname]):
        # default style
        ttk_style = style_class
        focus_color = builder.colors.primary
    else:
        # colored style
        ttk_style = f"{colorname}.{style_class}"
        focus_color = builder.colors.get(colorname)
        border_color = focus_color

    builder.configure(
        ttk_style,
        bordercolor=border_color,
        darkcolor=builder.colors.inputbg,
        lightcolor=builder.colors.inputbg,
        fieldbackground=builder.colors.inputbg,
        foreground=builder.colors.inputfg,
        insertcolor=builder.colors.inputfg,
        padding=5,
    )
    builder.style.map(
        ttk_style,
        foreground=[("disabled", disabled_fg)],
        fieldbackground=[("readonly", readonly)],
        bordercolor=[
            ("invalid", builder.colors.danger),
            ("focus !disabled", focus_color),
            ("hover !disabled", focus_color),
        ],
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
    )
    # register ttk_style
    builder.register_ttkstyle(ttk_style)
