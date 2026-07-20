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

    if any([colorname == DEFAULT, colorname == ""]):
        unselected_bg = builder.colors.inputbg
        ttk_style = ttk_class
    else:
        unselected_bg = builder.colors.get(colorname)
        ttk_style = f"{colorname}.{ttk_class}"

    # Tab foregrounds are computed from each tab's own background so the label
    # stays readable: the selected tab sits on `colors.bg`, the unselected tabs
    # on `unselected_bg`. The unselected label is muted toward its background to
    # de-emphasize inactive tabs (gently -- it must stay legible, unlike the
    # decorative 0.4 indicator mute; 0.6 keeps 60% of the on-color).
    selected_fg = builder.on_color(builder.colors.bg)
    unselected_fg = builder.mute(builder.on_color(unselected_bg), unselected_bg, 0.6)

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
        foreground=selected_fg,
        bordercolor=border_color,
        padding=builder.scale_size((6, 5)),
    )
    builder.style.map(
        ttk_style_tab,
        background=[
            ("selected", builder.colors.bg),
            ("!selected", unselected_bg),
        ],
        lightcolor=[
            ("selected", builder.colors.bg),
            ("!selected", unselected_bg),
        ],
        # NOTE: `padding` and `bordercolor` are deliberately NOT mapped. They
        # used to be mapped to the same value for both `selected` and
        # `!selected` -- a no-op that changed nothing visually but, because the
        # two states cover every state, made `lookup` always resolve through the
        # map and silently mask any user `configure(ttk_style_tab, padding=...)`.
        # The values still come from `configure` above; leaving them unmapped is
        # what makes a user override (durable or not) actually take effect.
        foreground=[("selected", selected_fg), ("!selected", unselected_fg)],
    )

    # register ttkstyle
    builder.register_ttkstyle(ttk_style)
