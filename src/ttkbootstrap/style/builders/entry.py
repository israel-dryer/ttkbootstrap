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
    ttk_class = "TEntry"

    on_disabled = builder.disabled("text", builder.colors.inputbg)
    border = builder.colors.border
    # readonly fields read like normal fields (no greyed box); the field bg is
    # the same input surface in both modes.
    readonly = builder.colors.inputbg

    if any([colorname == DEFAULT, not colorname]):
        # default style
        ttk_style = ttk_class
        focus_ring = builder.colors.primary
    else:
        # colored style
        ttk_style = f"{colorname}.{ttk_class}"
        focus_ring = builder.colors.get(colorname)

    builder.configure(
        ttk_style,
        bordercolor=border,
        darkcolor=builder.colors.inputbg,
        lightcolor=builder.colors.inputbg,
        fieldbackground=builder.colors.inputbg,
        foreground=builder.colors.inputfg,
        insertcolor=builder.colors.inputfg,
        padding=builder.scale_size(5),
    )
    builder.style.map(
        ttk_style,
        foreground=[("disabled", on_disabled)],
        fieldbackground=[("readonly", readonly)],
        bordercolor=[
            ("invalid", builder.colors.danger),
            ("focus !disabled", focus_ring),
        ],
        lightcolor=[
            ("focus invalid", builder.colors.danger),
            ("focus !disabled", focus_ring),
            ("readonly", readonly),
        ],
        darkcolor=[
            ("focus invalid", builder.colors.danger),
            ("focus !disabled", focus_ring),
            ("readonly", readonly),
        ],
    )
    # register ttk_style
    builder.register_ttkstyle(ttk_style)
