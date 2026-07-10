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

    # The surface the button sits on (2.0 surface-color); default == theme bg,
    # so the branches below are byte-for-byte the pre-surface recipe when unset.
    surface = builder.resolve_surface(builder._surface)

    # Every solid button carries a subtle border derived from its own fill
    # (`border(fill)` -- the fill blended toward its text color), so the shape
    # stays defined on any surface. `darkcolor`/`lightcolor` track the fill so
    # only the border ring shows (no clam bevel). `neutral` is just the
    # no-accent fill (a mode-aware raise of the surface) through this same path.
    if colorname == NEUTRAL:
        ttk_style = builder.surface_prefix(f"{NEUTRAL}.{ttk_class}")
        fill = neutral_fill(builder, base=surface)
    elif any([colorname == DEFAULT, colorname == ""]):
        # The base (no-color) button follows the Style's default_button setting
        # (neutral by default; "primary" restores the pre-2.0 accented default).
        ttk_style = builder.surface_prefix(ttk_class)
        fill = default_button_fill(builder, base=surface)
    else:
        ttk_style = builder.surface_prefix(f"{colorname}.{ttk_class}")
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
        padding=builder.scale_size((10, 4)),
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
    ttk_style = builder.surface_prefix(f"{NEUTRAL}.{ttk_class}")
    surface = builder.resolve_surface(builder._surface)
    # On a non-default surface the text must read against it, not the app bg.
    fg = builder.on_surface_fg()
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
        padding=builder.scale_size((10, 4)),
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
        ttk_style = builder.surface_prefix(ttk_class)
        colorname = PRIMARY
    else:
        ttk_style = builder.surface_prefix(f"{colorname}.{ttk_class}")

    # The surface the button sits on (2.0 surface-color); the flat rest fill and
    # the clam dark/light regions track it so the outline stays flush.
    surface = builder.resolve_surface(builder._surface)
    accent = builder.colors.get(colorname)
    pressed = accent
    hover = accent
    border = accent

    on_pressed = builder.on_color(accent)
    on_disabled = builder.disabled("text")

    builder.configure(
        ttk_style,
        foreground=accent,
        background=surface,
        bordercolor=border,
        darkcolor=surface,
        lightcolor=surface,
        relief=tk.RAISED,
        borderwidth=1,  # 1px hairline; intentionally unscaled
        focusthickness=builder.scale_size(1),
        focuscolor=accent,
        padding=builder.scale_size((10, 4)),
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

    # The surface the link sits on (2.0 surface-color); its (transparent-looking)
    # background tracks it so the link is flush with an accent bar/card.
    surface = builder.resolve_surface(builder._surface)
    # On a non-default surface the default/light link text reads against it.
    on_surface_default = builder.on_surface_fg()

    if any([colorname == DEFAULT, colorname == ""]):
        on_surface = on_surface_default
        ttk_style = builder.surface_prefix(style_class)
    elif colorname == LIGHT:
        on_surface = on_surface_default
        ttk_style = builder.surface_prefix(f"{colorname}.{style_class}")
    else:
        on_surface = builder.colors.get(colorname)
        ttk_style = builder.surface_prefix(f"{colorname}.{style_class}")

    pressed = builder.colors.info
    hover = builder.colors.info
    on_disabled = builder.disabled("text")

    builder.configure(
        ttk_style,
        foreground=on_surface,
        background=surface,
        relief=tk.FLAT,
        focusthickness=builder.scale_size(1),
        focuscolor=on_surface,
        anchor=tk.CENTER,
        padding=builder.scale_size((10, 4)),
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
            ("disabled", surface),
            ("pressed !disabled", surface),
            ("hover !disabled", surface),
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
    # The surface the ghost sits on (2.0 surface-color): it is transparent at
    # rest, so its background *is* the surface -- this is what lets it ghost on
    # an accent bar/card instead of only the app background.
    surface = builder.resolve_surface(builder._surface)

    if colorname in (DEFAULT, "", NEUTRAL):
        # default/neutral ghost: normal text, a neutral surface raise on hover
        base = style_class if colorname in (DEFAULT, "") else f"{NEUTRAL}.{style_class}"
        ttk_style = builder.surface_prefix(base)
        # On a non-default surface the text reads against it, not the app bg.
        fg = builder.on_surface_fg()
        hover = neutral_fill(builder, 1, base=surface)
        pressed = neutral_fill(builder, 2, base=surface)
    else:
        # colored ghost: accent text, a subtle wash of the accent on hover
        ttk_style = builder.surface_prefix(f"{colorname}.{style_class}")
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
        padding=builder.scale_size((10, 4)),
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
