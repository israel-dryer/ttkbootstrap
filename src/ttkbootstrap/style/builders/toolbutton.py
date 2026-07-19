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

    # A bare toolbutton renders neutral, like every bare button-family variant
    # (2.0) -- identical to `neutral toolbutton`; you opt into an accent ON with
    # `primary toolbutton`. With no accent to latch to, ON is a stronger surface
    # raise rather than a color.
    if colorname in (NEUTRAL, DEFAULT, ""):
        ttk_style = f"{NEUTRAL}.{ttk_class}" if colorname == NEUTRAL else ttk_class
        selected = neutral_fill(builder, 2)
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


@register_builder("ghost", "toolbutton")
def build_ghost_toolbutton_style(builder: StyleBuilderTTK, colorname=DEFAULT):
    """Create a ghost toolbutton style for the ttk.Checkbutton
    and ttk.Radiobutton widgets.

    A ghost toolbutton is transparent at rest -- no fill, no border, just its
    label -- and gains a subtle wash when toggled ON: a light tint of the accent
    for a colored ghost, or a neutral surface raise for the default/neutral one.
    It is the toggle analog of the ghost button, and quieter than the `outline`
    toolbutton (which shows an accent border at rest and a full accent fill ON):
    it suits flat toolbars where only the ON button should read as filled.

    Parameters:

        builder (StyleBuilderTTK):
            The style builder
        colorname (str):
            The color label used to style the widget.
    """
    ttk_class = "Ghost.Toolbutton"

    # OFF is the flat app surface with no border; ON is a subtle wash. For
    # `neutral`/default (no accent to latch to), ON is a neutral surface raise
    # rather than a color -- like the neutral solid/outline toolbutton. A bare
    # ghost toolbutton renders neutral, like every bare button-family variant.
    # ON (selected) reuses the ghost *button's* engaged surface -- its hover
    # wash -- so a toggled ghost toolbutton and a hovered ghost button read
    # identically: `neutral_fill(1)` for neutral, a 0.16 accent tint for colored.
    surface = builder.colors.bg
    if colorname in (NEUTRAL, DEFAULT, ""):
        ttk_style = f"{NEUTRAL}.{ttk_class}" if colorname == NEUTRAL else ttk_class
        off_fg = builder.mute(builder.colors.fg, surface)  # muted off text
        selected = neutral_fill(builder, 1)
        on_selected = builder.on_color(selected)
    else:
        ttk_style = f"{colorname}.{ttk_class}"
        accent = builder.colors.get(colorname)
        off_fg = accent  # the accent text is the resting signal (no border)
        selected = builder.mute(accent, surface, 0.16)  # light accent wash
        on_selected = accent  # accent text stays on the quiet wash

    disabled = builder.disabled()
    on_disabled = builder.disabled("text", disabled)

    # A toolbutton is a toggle: only ON (selected) and OFF (unselected) change
    # the appearance -- no hover/active or pressed preview. Flat relief draws no
    # border; keep dark/light on the fill so no clam bevel leaks, and hold
    # borderwidth=1 (like the ghost button) so the ghost reserves the same space
    # and matches the solid/outline toolbutton size.
    fill_states = [
        ("disabled", disabled),
        ("selected !disabled", selected),
    ]
    builder.configure(
        ttk_style,
        foreground=off_fg,
        background=surface,
        darkcolor=surface,
        lightcolor=surface,
        relief=tk.FLAT,
        borderwidth=1,  # reserve the 1px the solid/outline hairline occupies
        focusthickness=builder.scale_size(1),  # match solid toolbutton height
        focuscolor=off_fg,
        padding=builder.scale_size((10, 4)),
        anchor=tk.CENTER,
    )
    builder.style.map(
        ttk_style,
        foreground=[
            ("disabled", on_disabled),
            ("selected !disabled", on_selected),
        ],
        focuscolor=[  # focus ring tracks the text color
            ("disabled", on_disabled),
            ("selected !disabled", on_selected),
        ],
        background=fill_states,
        darkcolor=fill_states,
        lightcolor=fill_states,
    )
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
