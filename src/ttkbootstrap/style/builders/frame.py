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
    # The surface the frame sits on (2.0 surface-color); default == theme bg, so
    # a plain `@card`/`@chrome` frame gets the elevation surface as its fill.
    surface = builder.resolve_surface(builder._surface)

    if any([colorname == DEFAULT, colorname == ""]):
        ttk_style = builder.surface_prefix(ttk_class)
        background = surface
    else:
        ttk_style = builder.surface_prefix(f"{colorname}.{ttk_class}")
        background = builder.colors.get(colorname)

    builder.configure(ttk_style, background=background)

    # register style
    builder.register_ttkstyle(ttk_style)


@register_builder("bordered", "frame")
def build_bordered_frame(builder: StyleBuilderTTK, colorname=DEFAULT):
    """A container with a single flat hairline border (the `bordered` variant).

    Owns one flat 1px border so its contents sit inside one frame. `relief=RAISED`
    with `lightcolor`/`darkcolor` blended into the background suppresses the bevel,
    leaving just the `bordercolor` hairline -- the same border weight the inputs
    draw. Give the frame a little widget `padding` so its children don't paint over
    the border (ttk frames inset from the widget's padding, not the style's).

    This is a border only, orthogonal to the `@card`/`@chrome` surface (which
    fills a frame); combine them for a bordered frame on a surface.
    """
    ttk_class = "Bordered.TFrame"
    # The border sits on a surface (2.0 surface-color); default == theme bg, so
    # `bordered @card` is a hairline border on the card surface (orthogonal).
    surface = builder.resolve_surface(builder._surface)
    if any([colorname == DEFAULT, colorname == ""]):
        ttk_style = builder.surface_prefix(ttk_class)
        background = surface
        border = builder.border(background)
    else:
        ttk_style = builder.surface_prefix(f"{colorname}.{ttk_class}")
        colored = builder.colors.get(colorname)
        background = builder.mute(builder.colors.fg, colored, 0.16)
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
    """A `bordered` frame whose border tracks widget state -- a focus ring.

    Identical to `bordered` at rest, but the border is state-mapped so it
    brightens to the accent while the frame is in the `focus` state. Apply it once
    and toggle the frame's state (`frame.state(["focus"])`) to drive the ring; no
    style swap needed.
    """
    ttk_class = "Highlight.TFrame"
    surface = builder.resolve_surface(builder._surface)
    if any([colorname == DEFAULT, colorname == ""]):
        ttk_style = builder.surface_prefix(ttk_class)
        background = surface
        accent = builder.colors.primary
    else:
        ttk_style = builder.surface_prefix(f"{colorname}.{ttk_class}")
        colored = builder.colors.get(colorname)
        background = builder.mute(builder.colors.fg, colored, 0.16)
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
