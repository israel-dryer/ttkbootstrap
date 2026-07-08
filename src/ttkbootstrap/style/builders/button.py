"""TTK button style recipes."""

import tkinter as tk

from ttkbootstrap.constants import *
from ttkbootstrap.style import StyleBuilderTTK
from ttkbootstrap.style.builders.registry import register_builder
from ttkbootstrap.style.builders.utils import neutral_fill, default_button_fill


@register_builder("default", "button")
def build_button_style(builder: StyleBuilderTTK, colorname=DEFAULT):
    """Create a solid style for the ttk.Button widget.

    Parameters:

        builder (StyleBuilderTTK):
            The style builder
        colorname (str):
            The color label used to style the widget.
    """
    ttk_class = "TButton"

    # Every solid button carries a subtle border derived from its own fill
    # (`border(fill)` -- the fill blended toward its text color), so the shape
    # stays defined on any surface. `darkcolor`/`lightcolor` track the fill so
    # only the border ring shows (no clam bevel). `neutral` is just the
    # no-accent fill (a mode-aware raise of the surface) through this same path.
    if colorname == NEUTRAL:
        ttk_style = f"{NEUTRAL}.{ttk_class}"
        fill = neutral_fill(builder)
    elif any([colorname == DEFAULT, colorname == ""]):
        # The base (no-color) button follows the Style's default_button setting
        # (neutral by default; "primary" restores the pre-2.0 accented default).
        ttk_style = ttk_class
        fill = default_button_fill(builder)
    else:
        ttk_style = f"{colorname}.{ttk_class}"
        fill = builder.colors.get(colorname)

    on_fill = builder.on_color(fill)
    hover = builder.active(fill)
    pressed = builder.pressed(fill)
    disabled = builder.disabled()
    on_disabled = builder.disabled("text", disabled)

    # Border: a subtle same-hue edge derived from the fill. The clam dark/light
    # regions always track the *fill* (in every state), so no two-tone bevel is
    # ever drawn -- `bordercolor` is the only distinct edge color, itself the
    # fill's derived border in each state.
    fill_states = [
        ("disabled", disabled),
        ("pressed !disabled", pressed),
        ("hover !disabled", hover),
    ]
    border_states = [
        ("disabled", disabled),
        ("pressed !disabled", builder.border(pressed)),
        ("hover !disabled", builder.border(hover)),
    ]

    builder.configure(
        ttk_style,
        foreground=on_fill,
        background=fill,
        bordercolor=builder.border(fill),
        darkcolor=fill,
        lightcolor=fill,
        relief=tk.RAISED,
        borderwidth=1,  # 1px hairline; intentionally unscaled
        focusthickness=builder.scale_size(1),
        focuscolor=on_fill,
        padding=builder.scale_size((10, 5)),
        anchor=tk.CENTER,
    )
    builder.style.map(
        ttk_style,
        foreground=[("disabled", on_disabled)],
        focuscolor=[("disabled", on_disabled)],
        background=fill_states,
        bordercolor=border_states,
        darkcolor=fill_states,
        lightcolor=fill_states,
    )
    # register ttkstyle
    builder.register_ttkstyle(ttk_style)


def _build_neutral_outline_button_style(builder: StyleBuilderTTK, ttk_class):
    """Outline `neutral` button: flush with the surface, a derived neutral border.

    fill = the surface itself; border = `border(bg)`; text = normal `fg`. Hover
    fills with a subtle elevate of the surface (`active`), staying unaccented.
    """
    ttk_style = f"{NEUTRAL}.{ttk_class}"
    surface = builder.colors.bg
    fg = builder.colors.fg
    hover = builder.active(surface)
    pressed = builder.pressed(surface)
    on_disabled = builder.disabled("text")

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
        padding=builder.scale_size((10, 5)),
        anchor=tk.CENTER,
    )
    builder.style.map(
        ttk_style,
        foreground=[("disabled", on_disabled)],
        focuscolor=[("disabled", on_disabled)],
        background=[
            ("pressed !disabled", pressed),
            ("hover !disabled", hover),
        ],
        bordercolor=[
            ("disabled", on_disabled),
            ("pressed !disabled", builder.border(pressed)),
            ("hover !disabled", builder.border(hover)),
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
    builder.register_ttkstyle(ttk_style)


@register_builder("outline", "button")
def build_outline_button_style(builder: StyleBuilderTTK, colorname=DEFAULT):
    """Create an outline style for the ttk.Button widget.

    Parameters:

        builder (StyleBuilderTTK):
            The style builder
        colorname (str):
            The color label used to style the widget.
    """
    ttk_class = "Outline.TButton"

    if colorname == NEUTRAL:
        _build_neutral_outline_button_style(builder, ttk_class)
        return

    if any([colorname == DEFAULT, colorname == ""]):
        ttk_style = ttk_class
        colorname = PRIMARY
    else:
        ttk_style = f"{colorname}.{ttk_class}"

    accent = builder.colors.get(colorname)
    pressed = accent
    hover = accent
    border = accent

    on_pressed = builder.on_color(accent)
    on_disabled = builder.disabled("text")

    builder.configure(
        ttk_style,
        foreground=accent,
        background=builder.colors.bg,
        bordercolor=border,
        darkcolor=builder.colors.bg,
        lightcolor=builder.colors.bg,
        relief=tk.RAISED,
        borderwidth=1,  # 1px hairline; intentionally unscaled
        focusthickness=builder.scale_size(1),
        focuscolor=accent,
        padding=builder.scale_size((10, 5)),
        anchor=tk.CENTER,
    )
    builder.style.map(
        ttk_style,
        foreground=[
            ("disabled", on_disabled),
            ("pressed !disabled", on_pressed),
            ("hover !disabled", on_pressed),
        ],
        background=[
            ("pressed !disabled", pressed),
            ("hover !disabled", hover),
        ],
        bordercolor=[
            ("disabled", on_disabled),
            ("pressed !disabled", pressed),
            ("hover !disabled", hover),
        ],
        focuscolor=[
            ("pressed !disabled", on_pressed),
            ("hover !disabled", on_pressed),
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
    # register ttkstyle
    builder.register_ttkstyle(ttk_style)


@register_builder("link", "button")
def build_link_button_style(builder: StyleBuilderTTK, colorname=DEFAULT):
    """Create a link button style for the ttk.Button widget.

    Parameters:

        builder (StyleBuilderTTK):
            The style builder
        colorname (str):
            The color label used to style the widget.
    """
    style_class = "Link.TButton"


    if any([colorname == DEFAULT, colorname == ""]):
        on_surface = builder.colors.fg
        ttk_style = style_class
    elif colorname == LIGHT:
        on_surface = builder.colors.fg
        ttk_style = f"{colorname}.{style_class}"
    else:
        on_surface = builder.colors.get(colorname)
        ttk_style = f"{colorname}.{style_class}"

    pressed = builder.colors.info
    hover = builder.colors.info
    on_disabled = builder.disabled("text")

    builder.configure(
        ttk_style,
        foreground=on_surface,
        background=builder.colors.bg,
        relief=tk.FLAT,
        focusthickness=builder.scale_size(1),
        focuscolor=on_surface,
        anchor=tk.CENTER,
        padding=builder.scale_size((10, 5)),
    )
    builder.style.map(
        ttk_style,
        shiftrelief=[("pressed !disabled", builder.scale_size(-1))],
        foreground=[
            ("disabled", on_disabled),
            ("pressed !disabled", pressed),
            ("hover !disabled", hover),
        ],
        focuscolor=[
            ("pressed !disabled", pressed),
            ("hover !disabled", pressed),
        ],
        background=[
            ("disabled", builder.colors.bg),
            ("pressed !disabled", builder.colors.bg),
            ("hover !disabled", builder.colors.bg),
        ]
    )
    # register ttkstyle
    builder.register_ttkstyle(ttk_style)


@register_builder("ghost", "button")
def build_ghost_button_style(builder: StyleBuilderTTK, colorname=DEFAULT):
    """Create a ghost style for the ttk.Button widget.

    A ghost button is transparent at rest -- no fill, no border, just its
    (accent-colored) label -- and gains a subtle wash on hover/press: a light
    tint of the accent for a colored ghost, or a neutral surface raise for the
    default/neutral ghost. It sits between `link` (text-only) and `outline`
    (bordered): more button-like than a link, quieter than an outline. Ported
    from bootstack's ghost button.

    Parameters:

        builder (StyleBuilderTTK):
            The style builder
        colorname (str):
            The color label used to style the widget.
    """
    style_class = "Ghost.TButton"
    surface = builder.colors.bg

    if colorname in (DEFAULT, "", NEUTRAL):
        # default/neutral ghost: normal text, a neutral surface raise on hover
        ttk_style = style_class if colorname in (DEFAULT, "") else f"{NEUTRAL}.{style_class}"
        fg = builder.colors.fg
        hover = neutral_fill(builder, 1)
        pressed = neutral_fill(builder, 2)
    else:
        # colored ghost: accent text, a subtle wash of the accent on hover
        ttk_style = f"{colorname}.{style_class}"
        fg = builder.colors.get(colorname)
        hover = builder.mute(fg, surface, 0.16)
        pressed = builder.mute(fg, surface, 0.26)

    on_disabled = builder.disabled("text")

    builder.configure(
        ttk_style,
        foreground=fg,
        background=surface,
        relief=tk.FLAT,
        # flat relief draws no border, but keep borderwidth=1 (like link) so the
        # ghost reserves the same space and matches the solid/outline size.
        borderwidth=1,
        focusthickness=builder.scale_size(1),
        focuscolor=fg,
        padding=builder.scale_size((10, 5)),
        anchor=tk.CENTER,
    )
    builder.style.map(
        ttk_style,
        foreground=[("disabled", on_disabled)],
        focuscolor=[("disabled", on_disabled)],
        background=[
            ("disabled", surface),
            ("pressed !disabled", pressed),
            ("hover !disabled", hover),
        ],
    )
    builder.register_ttkstyle(ttk_style)


@register_builder("date", "button")
def build_date_button_style(builder: StyleBuilderTTK, colorname=DEFAULT):
    """Create a date button style for the ttk.Button widget.

    Parameters:

        builder (StyleBuilderTTK):
            The style builder
        colorname (str):
            The color label used to style widget.
    """
    style_class = "Date.TButton"

    disabled = builder.disabled()
    on_disabled = builder.disabled("text", disabled)

    if any([colorname == DEFAULT, colorname == ""]):
        ttk_style = style_class
        background = builder.colors.primary
        on_background = builder.on_color(background)
    else:
        ttk_style = f"{colorname}.{style_class}"
        background = builder.colors.get(colorname)
        on_background = builder.on_color(background)

    # Calendar icon in the button foreground color. Sized against the 4% glyph
    # pad (icons.py): ~18 keeps the prior visual size (the old 21 was tuned to the
    # larger 10% pad; the reduced pad now renders the glyph bigger per unit size).
    size = [18, 19]
    img_normal = builder.assets.icon("calendar3", size, on_background)
    img_disabled = builder.assets.icon("calendar3", size, on_disabled)

    pressed = builder.pressed(background)
    hover = builder.active(background)

    # Same hairline-border treatment as the solid button: dark/light track the
    # fill (no bevel), bordercolor is the fill's derived border.
    fill_states = [
        ("disabled", disabled),
        ("pressed !disabled", pressed),
        ("hover !disabled", hover),
    ]
    border_states = [
        ("disabled", disabled),
        ("pressed !disabled", builder.border(pressed)),
        ("hover !disabled", builder.border(hover)),
    ]

    builder.configure(
        ttk_style,
        foreground=on_background,
        background=background,
        bordercolor=builder.border(background),
        darkcolor=background,
        lightcolor=background,
        relief=tk.RAISED,
        borderwidth=1,  # 1px hairline; intentionally unscaled
        focusthickness=0,
        focuscolor=on_background,
        padding=builder.scale_size((2, 2)),
        anchor=tk.CENTER,
        image=img_normal,
    )
    builder.style.map(
        ttk_style,
        image=[("disabled", img_disabled)],
        foreground=[("disabled", on_disabled)],
        background=fill_states,
        bordercolor=border_states,
        darkcolor=fill_states,
        lightcolor=fill_states,
    )
    builder.register_ttkstyle(ttk_style)
