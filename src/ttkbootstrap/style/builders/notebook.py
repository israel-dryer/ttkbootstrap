"""TTK notebook style recipes."""

from ttkbootstrap.constants import *
from ttkbootstrap.style import StyleBuilderTTK
from ttkbootstrap.style.builders.registry import register_builder


@register_builder("default", "notebook")
def build_notebook_style(builder: StyleBuilderTTK, colorname=DEFAULT):
    """Create a standard style for the ttk.Notebook widget.

    Parameters:

        builder (StyleBuilderTTK):
            The style builder
        colorname (str):
            The color label used to style the widget.
    """
    ttk_class = "TNotebook"

    border_color = builder.colors.border
    foreground = builder.colors.inputfg if builder.is_light_theme else builder.colors.selectfg

    if any([colorname == DEFAULT, colorname == ""]):
        background = builder.colors.inputbg
        select_fg = builder.colors.fg
        ttk_style = ttk_class
    else:
        background = builder.colors.get(colorname)
        select_fg = builder.on_color(background)
        ttk_style = f"{colorname}.{ttk_class}"

    ttk_style_tab = f"{ttk_style}.Tab"

    # create widget style
    builder.configure(
        ttk_style,
        background=builder.colors.bg,
        bordercolor=border_color,
        lightcolor=builder.colors.bg,
        darkcolor=builder.colors.bg,
        tabmargins=builder.scale_size((0, 1, 1, 0)),
    )
    builder.configure(
        ttk_style_tab,
        focuscolor="",
        foreground=foreground,
        padding=builder.scale_size((6, 5)),
    )
    builder.style.map(
        ttk_style_tab,
        background=[
            ("selected", builder.colors.bg),
            ("!selected", background),
        ],
        lightcolor=[
            ("selected", builder.colors.bg),
            ("!selected", background),
        ],
        bordercolor=[
            ("selected", border_color),
            ("!selected", border_color),
        ],
        padding=[
            ("selected", builder.scale_size((6, 5))),
            ("!selected", builder.scale_size((6, 5))),
        ],
        foreground=[("selected", foreground), ("!selected", select_fg)],
    )

    # register ttkstyle
    builder.register_ttkstyle(ttk_style)
