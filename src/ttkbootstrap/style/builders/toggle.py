"""TTK toggle style recipes."""

import tkinter as tk

from ttkbootstrap.constants import *
from ttkbootstrap.style import StyleBuilderTTK
from ttkbootstrap.style.layout import El, image_element, layout
from ttkbootstrap.style.builders.registry import register_builder
from ttkbootstrap.style.builders.utils import indicator_spacer


@register_builder("default", "toggle")
def build_toggle_style(builder: StyleBuilderTTK, colorname=DEFAULT):
    """Create the default toggle style for the ttk.Checkbutton widget.

    The default toggle *is* a round toggle, but it must be built under the base
    ``Toggle`` style name -- that is what the bare ``bootstyle="toggle"`` resolves
    to (``round-toggle`` resolves to ``Round.Toggle``). Building it under
    ``Round.Toggle`` here left ``Toggle`` with no layout ("Layout Toggle not
    found").

    Parameters:

        builder (StyleBuilderTTK):
            The style builder.
        colorname (str):
            The color label used to style the widget.
    """
    _build_round_toggle_style(builder, colorname, "Toggle")


@register_builder("round", "toggle")
def build_round_toggle_style(builder: StyleBuilderTTK, colorname=DEFAULT):
    """Create a round toggle style for the ttk.Checkbutton widget.

    Parameters:

        builder (StyleBuilderTTK):
            The style builder
        colorname (str):
            The color label used to style the widget.
    """
    _build_round_toggle_style(builder, colorname, "Round.Toggle")


def _build_round_toggle_style(builder: StyleBuilderTTK, colorname, ttk_class):
    """Build a round toggle under `ttk_class` (`Toggle` or `Round.Toggle`)."""
    # The surface the toggle sits on (2.0 surface-color): the off track, the
    # background, and the switch glyph's knockout (black channel) all track it.
    surface = builder.resolve_surface(builder._surface)
    disabled_fg = builder.disabled("text", surface)
    fg = builder.on_surface_fg()
    off_track = builder.border(surface)  # bootstack: off track = border(surface)

    if any([colorname == DEFAULT, colorname == ""]):
        ttk_style = builder.surface_prefix(ttk_class)
        colorname = PRIMARY
    else:
        ttk_style = builder.surface_prefix(f"{colorname}.{ttk_class}")


    # Resolve the "on" accent; LIGHT/DARK on their own background need a
    # contrasting indicator (visual-check item: verify toggle aspect ratio
    # and LIGHT-on-light on the human spot-check).
    if colorname == LIGHT:
        accent = builder.colors.dark
    elif colorname == DARK:
        accent = builder.colors.light
    else:
        accent = builder.colors.get(colorname)

    builder.configure(
        ttk_style,
        relief=tk.FLAT,
        borderwidth=0,
        padding=0,
        foreground=fg,
        background=surface,
        # 1px keyboard-focus ring around the label (via the `Toolbutton.focus`
        # element in the layout below), matching the rest of the button family.
        focuscolor=fg,
        focusthickness=builder.scale_size(1),
    )
    builder.style.map(
        ttk_style,
        foreground=[("disabled", disabled_fg)],
        focuscolor=[("disabled", disabled_fg)],
        background=[("selected", surface)],
    )
    a = builder.assets
    on = a.recolor("switch_round", white=accent, black=surface)
    off = a.recolor("switch_round", white=off_track, black=surface, transform="flip-x")
    disabled_on = a.recolor("switch_round", white=disabled_fg, black=surface)
    disabled_off = a.recolor("switch_round", white=disabled_fg, black=surface, transform="flip-x")
    spacer_name = f"{ttk_style}.spacer"
    try:
        image_element(
            builder.style, f"{ttk_style}.indicator", default=on.image,
            states={
                "disabled selected": disabled_on.image,
                "disabled": disabled_off.image,
                "!selected": off.image,
            },
            border=on.meta.border, padding=on.meta.padding, sticky=W)
        image_element(
            builder.style, spacer_name,
            default=indicator_spacer(builder), sticky=EW)
    except Exception:
        """This method is used as the default Toggle style, so it is
        necessary to catch Tcl errors when it tries to create an element
        that was already created by the Toggle or Round Toggle style."""
        pass

    layout(builder.style, ttk_style,
        El("Toolbutton.border", sticky=NSEW, children=[
            El("Toolbutton.padding", sticky=NSEW, children=[
                El(f"{ttk_style}.indicator", side=LEFT),
                El(spacer_name, side=LEFT),
                El("Toolbutton.focus", side=LEFT, sticky="", children=[
                    El("Toolbutton.label", side=LEFT)])])]))
    # register ttkstyle
    builder.register_ttkstyle(ttk_style)


@register_builder("square", "toggle")
def build_square_toggle_style(builder: StyleBuilderTTK, colorname=DEFAULT):
    """Create a square toggle style for the ttk.Checkbutton widget.

    The square toggle uses its own recolorable raster template.

    Parameters:

        builder (StyleBuilderTTK):
            The style builder.
        colorname (str):
            The color label used to style the widget.
    """
    ttk_class = "Square.Toggle"
    # The surface the toggle sits on (2.0 surface-color).
    surface = builder.resolve_surface(builder._surface)
    disabled_fg = builder.disabled("text", surface)
    fg = builder.on_surface_fg()
    off_track = builder.border(surface)  # bootstack: off track = border(surface)

    if any([colorname == DEFAULT, colorname == ""]):
        ttk_style = builder.surface_prefix(ttk_class)
        colorname = PRIMARY
    else:
        ttk_style = builder.surface_prefix(f"{colorname}.{ttk_class}")

    # Resolve the "on" accent (same logic as round-toggle).
    if colorname == LIGHT:
        accent = builder.colors.dark
    elif colorname == DARK:
        accent = builder.colors.light
    else:
        accent = builder.colors.get(colorname)

    builder.configure(
        ttk_style, relief=tk.FLAT, borderwidth=0, foreground=fg,
        # 1px keyboard-focus ring around the label (via the `Toolbutton.focus`
        # element in the layout below), matching the rest of the button family.
        focuscolor=fg, focusthickness=builder.scale_size(1),
    )
    builder.style.map(
        ttk_style,
        foreground=[("disabled", disabled_fg)],
        focuscolor=[("disabled", disabled_fg)],
        background=[
            ("selected", surface),
            ("!selected", surface),
        ],
    )
    a = builder.assets
    on = a.recolor("switch_square", white=accent, black=surface)
    off = a.recolor("switch_square", white=off_track, black=surface, transform="flip-x")
    disabled_on = a.recolor("switch_square", white=disabled_fg, black=surface)
    disabled_off = a.recolor("switch_square", white=disabled_fg, black=surface, transform="flip-x")
    spacer_name = f"{ttk_style}.spacer"
    image_element(
        builder.style, f"{ttk_style}.indicator", default=on.image,
        states={
            "disabled selected": disabled_on.image,
            "disabled": disabled_off.image,
            "!selected": off.image,
        },
        border=on.meta.border, padding=on.meta.padding, sticky=W)
    image_element(
        builder.style, spacer_name,
        default=indicator_spacer(builder), sticky=EW)
    layout(builder.style, ttk_style,
        El("Toolbutton.border", sticky=NSEW, children=[
            El("Toolbutton.padding", sticky=NSEW, children=[
                El(f"{ttk_style}.indicator", side=LEFT),
                El(spacer_name, side=LEFT),
                El("Toolbutton.focus", side=LEFT, sticky="", children=[
                    El("Toolbutton.label", side=LEFT)])])]))

    # register ttk style
    builder.register_ttkstyle(ttk_style)
