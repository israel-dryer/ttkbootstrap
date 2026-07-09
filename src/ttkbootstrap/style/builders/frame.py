"""TTK frame style recipes."""

from ttkbootstrap.constants import *
from ttkbootstrap.style import StyleBuilderTTK
from ttkbootstrap.style.builders.registry import register_builder


@register_builder("default", "frame")
def build_frame_style(builder: StyleBuilderTTK, colorname=DEFAULT):
    """Create a style for the ttk.Frame widget.

    Parameters:

        builder (StyleBuilderTTK):
            The style builder
        colorname (str):
            The color label used to style the widget.
    """
    ttk_class = "TFrame"

    if any([colorname == DEFAULT, colorname == ""]):
        ttk_style = ttk_class
        background = builder.colors.bg
    else:
        ttk_style = f"{colorname}.{ttk_class}"
        background = builder.colors.get(colorname)

    builder.configure(ttk_style, background=background)

    # register style
    builder.register_ttkstyle(ttk_style)


@register_builder("card", "frame")
def build_card_frame(builder: StyleBuilderTTK, colorname=DEFAULT):
    """A simple inert bordered surface (a "card").

    A container that owns a single flat 1px border so its contents sit inside
    one frame. `relief=RAISED` with `lightcolor`/`darkcolor` blended into the
    background suppresses the bevel, leaving just the `bordercolor` hairline --
    the same border weight the inputs draw. Give the frame a little widget
    `padding` so its children don't paint over the border (ttk frames inset from
    the widget's padding, not the style's).
    """
    ttk_class = "Card.TFrame"
    if any([colorname == DEFAULT, colorname == ""]):
        ttk_style = ttk_class
        background = builder.colors.bg
        border = builder.border(background)
    else:
        ttk_style = f"{colorname}.{ttk_class}"
        surface = builder.colors.get(colorname)
        background = builder.mute(builder.colors.fg, surface, 0.16)
        border = builder.border(background)

    builder.configure(
        ttk_style,
        background=background,
        darkcolor=background,
        lightcolor=background,
        bordercolor=border,
        relief=RAISED,
        borderwidth=builder.scale_size(1),
    )

    # register style
    builder.register_ttkstyle(ttk_style)


@register_builder("highlight", "frame")
def build_highlight_frame(builder: StyleBuilderTTK, colorname=DEFAULT):
    """A `card` whose border tracks widget state -- a focus ring.

    Identical to `card` at rest, but the border is state-mapped so it brightens
    to the accent while the frame is in the `focus` state. Apply it once and
    toggle the frame's state (`frame.state(["focus"])`) to drive the ring; no
    style swap needed.
    """
    ttk_class = "Highlight.TFrame"
    if any([colorname == DEFAULT, colorname == ""]):
        ttk_style = ttk_class
        background = builder.colors.bg
        accent = builder.colors.primary
    else:
        ttk_style = f"{colorname}.{ttk_class}"
        surface = builder.colors.get(colorname)
        background = builder.mute(builder.colors.fg, surface, 0.16)
        accent = builder.colors.get(colorname)

    resting = builder.border(background)
    builder.configure(
        ttk_style,
        background=background,
        bordercolor=resting,
        darkcolor=background,
        lightcolor=background,
        relief=RAISED,
        borderwidth=builder.scale_size(1),
    )
    builder.style.map(
        ttk_style,
        bordercolor=[("focus", accent)],
        lightcolor=[("focus", accent)],
        darkcolor=[("focus", accent)],
    )

    # register style
    builder.register_ttkstyle(ttk_style)
