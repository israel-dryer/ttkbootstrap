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
    style_class = "TNotebook"

    if builder.is_light_theme:
        border_color = builder.colors.border
        foreground = builder.colors.inputfg
    else:
        border_color = builder.colors.selectbg
        foreground = builder.colors.selectfg

    if any([colorname == DEFAULT, colorname == ""]):
        background = builder.colors.inputbg
        select_fg = builder.colors.fg
        ttk_style = style_class
    else:
        select_fg = builder.colors.get_foreground(colorname)
        background = builder.colors.get(colorname)
        ttk_style = f"{colorname}.{style_class}"

    ttk_style_tab = f"{ttk_style}.Tab"

    # create widget style
    builder.configure(
        ttk_style,
        background=builder.colors.bg,
        bordercolor=border_color,
        lightcolor=builder.colors.bg,
        darkcolor=builder.colors.bg,
        tabmargins=(0, 1, 1, 0),
    )
    builder.configure(
        ttk_style_tab, focuscolor="", foreground=foreground, padding=(6, 5)
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
        padding=[("selected", (6, 5)), ("!selected", (6, 5))],
        foreground=[("selected", foreground), ("!selected", select_fg)],
    )

    # register ttkstyle
    builder.register_ttkstyle(ttk_style)
