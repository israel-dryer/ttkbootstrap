"""TTK toolbutton style recipes."""

import tkinter as tk

from ttkbootstrap.constants import *
from ttkbootstrap.style import StyleBuilderTTK
from ttkbootstrap.style.builders.registry import register_builder
from ttkbootstrap.style.builders.utils import neutral_fill


@register_builder("default", "toolbutton")
def build_toolbutton_style(builder: StyleBuilderTTK, colorname=DEFAULT):
    """Create a solid toolbutton style for the ttk.Checkbutton
    and ttk.Radiobutton widgets.

    Parameters:

        builder (StyleBuilderTTK):
            The style builder
        colorname (str):
            The color label used to style the widget.
    """
    ttk_class = "Toolbutton"

    # bootstack on/off model: OFF is a quiet raised surface with muted text; ON
    # is the accent -- or, for `neutral` (no accent to switch to), a stronger
    # surface raise so "on" still reads as distinct from "off".
    unselected = neutral_fill(builder, 1)

    if colorname == NEUTRAL:
        ttk_style = f"{NEUTRAL}.{ttk_class}"
        selected = neutral_fill(builder, 2)
    elif any([colorname == DEFAULT, colorname == ""]):
        ttk_style = ttk_class
        selected = builder.colors.primary
    else:
        ttk_style = f"{colorname}.{ttk_class}"
        selected = builder.colors.get(colorname)

    disabled = builder.disabled()

    on_selected = builder.on_color(selected)
    on_unselected = builder.mute(builder.colors.fg, unselected)  # muted off text
    on_disabled = builder.disabled("text", disabled)

    # 1px hairline border, matching the ttk.Button treatment: dark/light always
    # track the fill (no bevel); `bordercolor` is the only distinct edge and is
    # derived from whatever fill the segment is currently showing.
    # A toolbutton is a toggle: only ON (selected) and OFF (unselected) change
    # the appearance -- no hover/active or pressed preview.
    fill_states = [
        ("disabled", disabled),
        ("selected !disabled", selected),
    ]
    border_states = [
        ("disabled", disabled),
        ("selected !disabled", builder.border(selected)),
    ]

    builder.configure(
        ttk_style,
        foreground=on_unselected,
        background=unselected,
        bordercolor=builder.border(unselected),
        darkcolor=unselected,
        lightcolor=unselected,
        relief=tk.RAISED,
        borderwidth=1,  # 1px hairline; intentionally unscaled
        focusthickness=builder.scale_size(1),
        focuscolor=on_unselected,
        padding=builder.scale_size((10, 4)),
        anchor=tk.CENTER,
    )
    builder.style.map(
        ttk_style,
        foreground=[
            ("disabled", on_disabled),
            ("selected", on_selected),
        ],
        focuscolor=[
            ("disabled", on_disabled),
            ("selected", on_selected),
        ],
        background=fill_states,
        bordercolor=border_states,
        darkcolor=fill_states,
        lightcolor=fill_states,
    )

    # register ttk style
    builder.register_ttkstyle(ttk_style)


def _build_neutral_outline_toolbutton(builder: StyleBuilderTTK, ttk_style):
    """Neutral outline toolbutton: OFF is the flat surface, ON a raised surface.

    The no-accent analog of the outline toolbutton -- with no accent to latch to,
    "on" is shown by a subtle surface raise (`neutral_fill`) rather than a color.
    Registered under whatever `ttk_style` the caller computed — the neutral name
    or the bare (unprefixed) one, which renders identically.
    """
    unselected = builder.colors.bg
    selected = neutral_fill(builder, 1)
    on_unselected = builder.mute(builder.colors.fg, unselected)
    on_selected = builder.on_color(selected)
    disabled = builder.disabled()
    on_disabled = builder.disabled("text", disabled)

    # A toolbutton is a toggle: only ON (selected) and OFF (unselected) change
    # the appearance -- no hover/active or pressed preview.
    fill_states = [
        ("disabled", disabled),
        ("selected !disabled", selected),
    ]
    border_states = [
        ("disabled", disabled),
        ("selected !disabled", builder.border(selected)),
    ]
    builder.configure(
        ttk_style,
        foreground=on_unselected,
        background=unselected,
        bordercolor=builder.border(unselected),
        darkcolor=unselected,
        lightcolor=unselected,
        relief=tk.RAISED,
        borderwidth=1,  # 1px hairline; intentionally unscaled
        focusthickness=builder.scale_size(1),  # match solid toolbutton height
        focuscolor=on_unselected,
        padding=builder.scale_size((10, 4)),
        anchor=tk.CENTER,
    )
    builder.style.map(
        ttk_style,
        foreground=[
            ("disabled", on_disabled),
            ("selected", on_selected),
        ],
        focuscolor=[  # focus ring tracks the text color
            ("disabled", on_disabled),
            ("selected", on_selected),
        ],
        background=fill_states,
        bordercolor=border_states,
        darkcolor=fill_states,
        lightcolor=fill_states,
    )
    builder.register_ttkstyle(ttk_style)


@register_builder("outline", "toolbutton")
def build_outline_toolbutton_style(builder: StyleBuilderTTK, colorname=DEFAULT):
    """Create an outline toolbutton style for the ttk.Checkbutton
    and ttk.Radiobutton widgets.

    Parameters:

        builder (StyleBuilderTTK):
            The style builder
        colorname (str):
            The color label used to style the widget.
    """
    ttk_class = "Outline.Toolbutton"

    # A bare `outline` renders neutral, like every bare button-family variant (2.0).
    if colorname == NEUTRAL:
        _build_neutral_outline_toolbutton(builder, f"{NEUTRAL}.{ttk_class}")
        return
    if any([colorname == DEFAULT, colorname == ""]):
        _build_neutral_outline_toolbutton(builder, ttk_class)
        return

    ttk_style = f"{colorname}.{ttk_class}"

    accent = builder.colors.get(colorname)
    selected = accent
    on_selected = builder.on_color(selected)
    on_disabled = builder.disabled("text")

    builder.configure(
        ttk_style,
        foreground=accent,
        background=builder.colors.bg,
        bordercolor=accent,
        darkcolor=builder.colors.bg,
        lightcolor=builder.colors.bg,
        relief=tk.RAISED,
        borderwidth=1,  # 1px hairline; intentionally unscaled
        focusthickness=builder.scale_size(1),  # match solid toolbutton height
        focuscolor=accent,  # focus ring matches the text color (accent at rest)
        padding=builder.scale_size((10, 4)),
        anchor=tk.CENTER,
    )
    # A toolbutton is a toggle: only ON (selected) vs OFF (unselected) -- no
    # hover/active or pressed preview. The focus ring tracks the text color.
    builder.style.map(
        ttk_style,
        foreground=[
            ("disabled", on_disabled),
            ("selected !disabled", on_selected),
        ],
        focuscolor=[
            ("disabled", on_disabled),
            ("selected !disabled", on_selected),
        ],
        background=[
            ("selected !disabled", selected),
        ],
        bordercolor=[
            ("disabled", on_disabled),
            ("selected !disabled", selected),
        ],
        darkcolor=[
            ("disabled", builder.colors.bg),
            ("selected !disabled", selected),
        ],
        lightcolor=[
            ("disabled", builder.colors.bg),
            ("selected !disabled", selected),
        ],
    )
    # register ttkstyle
    builder.register_ttkstyle(ttk_style)
