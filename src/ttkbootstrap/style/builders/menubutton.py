"""TTK menubutton style recipes."""

import tkinter as tk

from ttkbootstrap.constants import *
from ttkbootstrap.style import StyleBuilderTTK
from ttkbootstrap.style.layout import El, image_element, layout
from ttkbootstrap.style.builders.registry import register_builder
from ttkbootstrap.style.builders.utils import (
    simple_arrow_assets, neutral_fill, default_button_fill,
)


@register_builder("default", "menubutton")
def build_menubutton_style(builder: StyleBuilderTTK, colorname=DEFAULT):
    """Create a solid style for the ttk.Menubutton widget.

    Parameters:

        builder (StyleBuilderTTK):
            The style builder
        colorname (str):
            The color label used to style the widget.
    """
    ttk_class = "TMenubutton"

    # `neutral` = the no-accent adaptive fill; otherwise the accent (or primary).
    if colorname == NEUTRAL:
        ttk_style = f"{NEUTRAL}.{ttk_class}"
        background = neutral_fill(builder)
    elif any([colorname == DEFAULT, colorname == ""]):
        # base (no-color) menubutton follows the Style's default_button setting
        ttk_style = ttk_class
        background = default_button_fill(builder)
    else:
        ttk_style = f"{colorname}.{ttk_class}"
        background = builder.colors.get(colorname)
    foreground = builder.on_color(background)

    disabled_bg = builder.disabled()
    disabled_fg = builder.disabled("text", disabled_bg)
    pressed = builder.pressed(background)
    hover = builder.active(background)

    # 1px hairline border, matching the ttk.Button treatment: dark/light always
    # track the fill (no bevel), `bordercolor` is the only distinct edge.
    fill_states = [
        ("disabled", disabled_bg),
        ("pressed !disabled", pressed),
        ("hover !disabled", hover),
    ]
    border_states = [
        ("disabled", disabled_bg),
        ("pressed !disabled", builder.border(pressed)),
        ("hover !disabled", builder.border(hover)),
    ]

    builder.configure(
        ttk_style,
        foreground=foreground,
        background=background,
        bordercolor=builder.border(background),
        darkcolor=background,
        lightcolor=background,
        relief=tk.RAISED,
        borderwidth=1,  # 1px hairline; intentionally unscaled
        focusthickness=builder.scale_size(1),
        focuscolor=foreground,
        # (left, top, right, bottom): 10px label inset on the left, a tighter
        # 6px on the right so the caret sits closer to the edge than the label.
        padding=builder.scale_size((10, 4, 6, 4)),
    )
    builder.style.map(
        ttk_style,
        foreground=[("disabled", disabled_fg)],
        focuscolor=[("disabled", disabled_fg)],
        background=fill_states,
        bordercolor=border_states,
        darkcolor=fill_states,
        lightcolor=fill_states,
    )
    # caret-down-fill indicator (replaces the native clam triangle); the
    # solid menubutton arrow keeps one color (only the background changes on
    # hover), so just a normal + disabled image.
    _build_menubutton_arrow(builder, ttk_style, foreground, disabled_fg, foreground)

    # register ttkstyle
    builder.register_ttkstyle(ttk_style)


def _build_menubutton_arrow(builder: StyleBuilderTTK, ttk_style, normal, disabled, active):
    """Build the caret-down indicator element + layout for a Menubutton style.

    Replaces ttk's native `Menubutton.indicator` triangle with a Bootstrap
    `caret-down-fill` image element so the menubutton arrow matches the
    caret-fill arrows used elsewhere. `normal`/`disabled`/`active` are the
    arrow colors per state (`active` == `normal` when the arrow does not
    recolor on hover/press).
    """
    arrows = simple_arrow_assets(builder, normal, disabled, active)
    down, down_disabled, down_active = arrows[0][1], arrows[1][1], arrows[2][1]
    image_element(
        builder.style, f"{ttk_style}.indicator", default=down,
        states={"disabled": down_disabled,
                "pressed !disabled": down_active,
                "hover !disabled": down_active},
        sticky="")
    # Keep the indicator *inside* `Menubutton.padding` so the configured widget
    # padding (see `padding=` in configure) holds the caret off the right edge.
    # clam's image element ignores an outer `-padding` on the element itself, so
    # placing it outside padding left the caret flush against the border.
    layout(builder.style, ttk_style,
           El("Menubutton.border", sticky=NSEW, children=[
            El("Menubutton.focus", sticky=NSEW, children=[
                El("Menubutton.padding", sticky=NSEW, children=[
                    El(f"{ttk_style}.indicator", side=tk.RIGHT, sticky=""),
                    El("Menubutton.label", side=LEFT, sticky="")])])]))


def _build_neutral_outline_menubutton(builder: StyleBuilderTTK, ttk_style, disabled_fg):
    """Neutral outline menubutton: surface fill, derived border, normal fg.

    The no-accent analog of the outline menubutton -- it does not fill with an
    accent on hover (that would break the "unaccented" intent); it stays on the
    surface with a subtle elevate on interaction, matching the neutral outline
    button. Registered under whatever `ttk_style` the caller computed — the
    neutral name or the bare (unprefixed) one, which renders identically.
    """
    surface = builder.colors.bg
    fg = builder.colors.fg
    hover = builder.active(surface)
    pressed = builder.pressed(surface)
    fill_states = [
        ("pressed !disabled", pressed),
        ("hover !disabled", hover),
    ]
    border_states = [
        ("disabled", disabled_fg),
        ("pressed !disabled", builder.border(pressed)),
        ("hover !disabled", builder.border(hover)),
    ]
    builder.configure(
        ttk_style,
        foreground=fg,
        background=surface,
        bordercolor=builder.border(surface),
        darkcolor=surface,
        lightcolor=surface,
        relief=tk.RAISED,
        borderwidth=1,  # 1px hairline; intentionally unscaled
        focusthickness=builder.scale_size(1),
        focuscolor=fg,
        padding=builder.scale_size((10, 4, 6, 4)),
    )
    builder.style.map(
        ttk_style,
        foreground=[("disabled", disabled_fg)],
        focuscolor=[("disabled", disabled_fg)],
        background=fill_states,
        bordercolor=border_states,
        darkcolor=fill_states,
        lightcolor=fill_states,
    )
    _build_menubutton_arrow(builder, ttk_style, fg, disabled_fg, fg)
    builder.register_ttkstyle(ttk_style)


@register_builder("outline", "menubutton")
def build_outline_menubutton_style(builder: StyleBuilderTTK, colorname=DEFAULT):
    """Create an outline button style for the ttk.Menubutton widget.

    Parameters:

        builder (StyleBuilderTTK):
            The style builder
        colorname (str):
            The color label used to style the widget.
    """
    ttk_class = "Outline.TMenubutton"

    disabled_fg = builder.disabled("text")

    # A bare `outline` renders neutral, like every bare button-family variant (2.0).
    if colorname == NEUTRAL:
        _build_neutral_outline_menubutton(
            builder, f"{NEUTRAL}.{ttk_class}", disabled_fg)
        return
    if any([colorname == DEFAULT, colorname == ""]):
        _build_neutral_outline_menubutton(builder, ttk_class, disabled_fg)
        return

    ttk_style = f"{colorname}.{ttk_class}"

    foreground = builder.colors.get(colorname)
    background = builder.on_color(foreground)
    foreground_pressed = background
    border_color = foreground
    pressed = foreground
    hover = foreground

    builder.configure(
        ttk_style,
        foreground=foreground,
        background=builder.colors.bg,
        bordercolor=border_color,
        darkcolor=builder.colors.bg,
        lightcolor=builder.colors.bg,
        relief=tk.RAISED,
        borderwidth=1,  # 1px hairline; intentionally unscaled
        focusthickness=builder.scale_size(1),
        focuscolor=foreground,
        padding=builder.scale_size((10, 4, 6, 4)),
    )
    builder.style.map(
        ttk_style,
        foreground=[
            ("disabled", disabled_fg),
            ("pressed !disabled", foreground_pressed),
            ("hover !disabled", foreground_pressed),
        ],
        focuscolor=[("disabled", disabled_fg)],
        background=[
            ("pressed !disabled", pressed),
            ("hover !disabled", hover),
        ],
        bordercolor=[
            ("disabled", disabled_fg),
            ("pressed", pressed),
            ("hover", hover),
        ],
        darkcolor=[
            ("pressed !disabled", pressed),
            ("hover !disabled", hover),
        ],
        lightcolor=[
            ("pressed !disabled", pressed),
            ("hover !disabled", hover),
        ],
    )

    # caret-down-fill indicator; the outline arrow recolors on hover/press
    # (foreground -> the contrasting fill color), so pass that as `active`.
    _build_menubutton_arrow(builder, ttk_style, foreground, disabled_fg, foreground_pressed)

    # register ttkstyle1
    builder.register_ttkstyle(ttk_style)


@register_builder("ghost", "menubutton")
def build_ghost_menubutton_style(builder: StyleBuilderTTK, colorname=DEFAULT):
    """Create a ghost style for the ttk.Menubutton widget.

    A ghost menubutton is transparent at rest -- no fill, no border, just its
    label and caret -- and gains a subtle wash on hover/press: a light tint of
    the accent for a colored ghost, or a neutral surface raise for the
    default/neutral one. It is the menubutton analog of the ghost button: a
    low-emphasis dropdown trigger, quieter than `outline`. A bare ghost
    menubutton renders neutral, like every bare button-family variant.

    Parameters:

        builder (StyleBuilderTTK):
            The style builder
        colorname (str):
            The color label used to style the widget.
    """
    ttk_class = "Ghost.TMenubutton"
    surface = builder.colors.bg

    # OFF is the flat surface with no border; hover/press wash it. For
    # `neutral`/default (no accent to latch to) the wash is a neutral surface
    # raise rather than a color -- like the neutral outline menubutton.
    if colorname in (DEFAULT, "", NEUTRAL):
        ttk_style = f"{NEUTRAL}.{ttk_class}" if colorname == NEUTRAL else ttk_class
        fg = builder.colors.fg
        hover = neutral_fill(builder, 1)
        pressed = neutral_fill(builder, 2)
    else:
        ttk_style = f"{colorname}.{ttk_class}"
        fg = builder.colors.get(colorname)  # accent text is the resting signal
        hover = builder.mute(fg, surface, 0.16)  # light accent wash
        pressed = builder.mute(fg, surface, 0.26)

    disabled_fg = builder.disabled("text")

    # A menubutton is momentary (like a button): wash on hover/press, no toggle.
    # Flat relief draws no border; keep dark/light on the fill so no clam bevel
    # leaks, and hold borderwidth=1 (like the ghost button) so the ghost reserves
    # the same space as the solid/outline menubutton.
    fill_states = [
        ("disabled", surface),
        ("pressed !disabled", pressed),
        ("hover !disabled", hover),
    ]
    builder.configure(
        ttk_style,
        foreground=fg,
        background=surface,
        darkcolor=surface,
        lightcolor=surface,
        relief=tk.FLAT,
        borderwidth=1,  # reserve the 1px the solid/outline hairline occupies
        focusthickness=builder.scale_size(1),
        focuscolor=fg,
        padding=builder.scale_size((10, 4, 6, 4)),
    )
    builder.style.map(
        ttk_style,
        foreground=[("disabled", disabled_fg)],
        focuscolor=[("disabled", disabled_fg)],
        background=fill_states,
        darkcolor=fill_states,
        lightcolor=fill_states,
    )
    # caret-down-fill indicator; the caret keeps the text color (only the
    # background washes on hover/press), so normal == active.
    _build_menubutton_arrow(builder, ttk_style, fg, disabled_fg, fg)
    builder.register_ttkstyle(ttk_style)
