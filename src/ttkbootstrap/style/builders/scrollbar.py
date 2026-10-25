"""TTK scrollbar style recipes."""

import tkinter as tk

from ttkbootstrap.constants import *
from ttkbootstrap.style import StyleBuilderTTK
from ttkbootstrap.style.layout import El, image_element, layout, state_map
from ttkbootstrap.style.builders.registry import register_builder


# A few-pixel thumb for the 'thin' variant -- suits narrow lists/dropdowns.
_THIN_SCROLLBAR_THICKNESS = 4
_THIN_SCROLLBAR_MIN_THUMB = 8  # minimum thumb length (logical)

# The standard scrollbar thumb thickness (square + round variants).
_SCROLLBAR_THICKNESS = 8


def _scrollbar_trough(builder):
    """The scrollbar track color: the surface, so the thumb floats with no
    visible channel around it. Honors the 2.0 surface-color token (default ==
    theme bg)."""
    return builder.resolve_surface(builder._surface)


def _scrollbar_thumb_color(builder, colorname):
    """The default (neutral) thumb color, or the accent when a color is given.

    In light mode the raw border color is too pale to read against the near-white
    trough, so darken it to a clearly visible mid-gray; dark mode's `selectbg`
    already reads against the dark trough.
    """
    if colorname in (DEFAULT, ""):
        if builder.is_light_theme:
            return builder.shade(builder.colors.border, 0.25)
        return builder.colors.selectbg
    return builder.colors.get(colorname)


# Trough margin (logical px) left on each side of the thumb, so the visible
# trough shows around it. Applied as the thumb's cross-axis padding.
_SCROLLBAR_THUMB_INSET = 1
_SCROLLBAR_MIN_THUMB = 16  # minimum thumb length (logical) so it stays grabbable


def _scrollbar_cap(builder, color, trough, orient, end, thickness, length, rounded):
    """One end cap of the thumb: `thickness` across the bar, `length` along it.

    A round cap is drawn flattened onto the trough color, so the image has no
    transparency: on X11 Tk draws a photo with alpha by reading the window
    back to blend it, a server round trip per draw.
    """
    a = builder.assets
    size = (thickness, length) if orient == "vertical" else (length, thickness)
    if not rounded:
        return a.rect(color, size)

    def draw(d, w, h):
        d.rectangle((0, 0, w - 1, h - 1), fill=trough)
        # a pill that overhangs the inner edge, so only its rounded end shows
        if orient == "vertical":
            box = [0, 0, w - 1, h - 1 + w] if end == "start" else [0, -w, w - 1, h - 1]
            radius = round(w / 2)
        else:
            box = [0, 0, w - 1 + h, h - 1] if end == "start" else [-h, 0, w - 1, h - 1]
            radius = round(h / 2)
        d.rounded_rectangle(box, radius=radius, fill=color)

    return a.image(size, draw, "scrollbar-cap", color, trough, orient, end)


def _scrollbar_thumb(builder, ttk_style, orient, thumb, trough, *,
                     thickness, inset, cap, rounded):
    """Build the thumb elements of `ttk_style`; returns the thumb layout node.

    The thumb is a `padding` element (the cross-axis inset) holding a cap image
    at each end around a solid fill that stretches with the thumb. Only the
    caps are images: ttk *tiles* the middle of an image element rather than
    stretching it, so a 9-sliced image thumb is redrawn from tiles once per
    pixel of its length, while the fill is one rectangle at any length. The
    two caps also set the minimum thumb length.

    The fill is the default theme's `field` element (flat at borderwidth 0),
    colored by `fieldbackground` -- an option nothing else on a scrollbar
    reads, so `background` stays the trough color like every other region.

    The children are named `*.thumb` on purpose: Tk's scrollbar bindings
    (library/ttk/scrollbar.tcl) decide whether a press starts a drag with
    `switch -glob -- [$w identify $x $y] { *thumb {...} *trough {...} }`, and
    `identify` returns the *innermost* element under the pointer. Named
    `.fill` / `.startcap` / `.endcap`, they match neither pattern, so pressing
    the thumb does nothing and only trough clicks work. Ending the names in
    `thumb` keeps every part of the thumb draggable.
    """
    vertical = orient == "vertical"
    scaling = builder.style.scaling
    pad = scaling.logical(inset)
    # Size the cap from the full thickness: rounding the inset and the cap
    # separately would add a pixel to the bar at fractional scaling. The
    # physical width is passed back in logical units, which the asset toolkit
    # rounds to the same pixel count.
    cap_thickness = (scaling.logical(thickness) - 2 * pad) / scaling.factor
    builder.configure(ttk_style, fieldbackground=thumb, focuswidth=0,
                      padding=(pad, 0) if vertical else (0, pad))
    state_map(builder.style, ttk_style, fieldbackground={
        "pressed": builder.pressed(thumb), "active": builder.active(thumb)})

    builder.style.element_create(f"{ttk_style}.thumb", "from", TTK_DEFAULT, "padding")
    builder.style.element_create(f"{ttk_style}.fill.thumb", "from", TTK_DEFAULT, "field")
    cap_sticky = "ew" if vertical else "ns"
    for end in ("start", "end"):
        def image(color):
            return _scrollbar_cap(builder, color, trough, orient, end,
                                  cap_thickness, cap, rounded)
        image_element(
            builder.style, f"{ttk_style}.{end}cap.thumb", default=image(thumb),
            states={"pressed": image(builder.pressed(thumb)),
                    "active": image(builder.active(thumb))},
            sticky=cap_sticky)

    start_side, end_side = ("top", "bottom") if vertical else ("left", "right")
    return El(f"{ttk_style}.thumb", expand="1", sticky="ns" if vertical else "we",
              children=[
                  El(f"{ttk_style}.startcap.thumb", side=start_side, sticky=cap_sticky),
                  El(f"{ttk_style}.endcap.thumb", side=end_side, sticky=cap_sticky),
                  El(f"{ttk_style}.fill.thumb", sticky="nswe")])


def _build_scrollbar(builder: StyleBuilderTTK, colorname, rounded):
    """Build the horizontal + vertical scrollbar styles (square or round).

    A subtle visible trough (every region shares the trough color, so the whole
    widget reads as one track) with an inset thumb, no arrows.
    """
    ttk_class = "TScrollbar"
    prefix = "Round." if rounded else ""
    trough = _scrollbar_trough(builder)
    thumb = _scrollbar_thumb_color(builder, colorname)

    if colorname in (DEFAULT, ""):
        base = prefix
    else:
        base = f"{colorname}.{prefix}"

    for orient, sticky, trough_el in (
        ("horizontal", "we", "Horizontal.Scrollbar.trough"),
        ("vertical", "ns", "Vertical.Scrollbar.trough"),
    ):
        axis = "Horizontal" if orient == "horizontal" else "Vertical"
        ttk_style = builder.surface_prefix(f"{base}{axis}.{ttk_class}")
        builder.configure(
            ttk_style,
            troughcolor=trough,
            bordercolor=trough,
            background=trough,
            darkcolor=trough,
            lightcolor=trough,
            relief=tk.FLAT,
            borderwidth=0,
            arrowsize=0,
        )
        thumb_el = _scrollbar_thumb(
            builder, ttk_style, orient, thumb, trough,
            thickness=_SCROLLBAR_THICKNESS, inset=_SCROLLBAR_THUMB_INSET,
            cap=_SCROLLBAR_MIN_THUMB // 2, rounded=rounded)
        layout(builder.style, ttk_style,
               El(trough_el, sticky=sticky, children=[thumb_el]))
        builder.register_ttkstyle(ttk_style)


@register_builder("thin", "scrollbar")
def build_thin_scrollbar_style(builder: StyleBuilderTTK, colorname=DEFAULT):
    """Create a thin scrollbar style for the ttk.Scrollbar widget.

    A few-pixel flat thumb on a surface-matched track, no arrows -- for narrow
    lists and dropdowns where the bar is more a scroll *indicator* than a drag
    handle (combobox popdown, font picker, ...). The thumb shares the neutral/
    accent color of the standard bar (`_scrollbar_thumb_color`) and darkens/
    lightens on hover/press. Ported from bootstack (mechanism, not API): a solid
    box thumb rather than a rounded PNG.

    Parameters:

        builder (StyleBuilderTTK):
            The style builder
        colorname (str):
            The color label used to style the widget.
    """
    ttk_class = "TScrollbar"
    # The surface the bar sits on (2.0 surface-color); default == theme bg.
    surface = builder.resolve_surface(builder._surface)
    # share the darker, clearly-visible thumb color with the default/round bars
    thumb = _scrollbar_thumb_color(builder, colorname)

    if any([colorname == DEFAULT, colorname == ""]):
        prefix = "Thin."
    else:
        prefix = f"{colorname}.Thin."

    for orient, sticky, trough_el in (
        ("horizontal", "we", "Horizontal.Scrollbar.trough"),
        ("vertical", "ns", "Vertical.Scrollbar.trough"),
    ):
        axis = "Horizontal" if orient == "horizontal" else "Vertical"
        ttk_style = builder.surface_prefix(f"{prefix}{axis}.{ttk_class}")
        builder.configure(
            ttk_style,
            troughcolor=surface,
            bordercolor=surface,
            background=surface,
            relief=tk.FLAT,
            borderwidth=0,
            arrowsize=0,
        )
        # a `t`-px-thick sliver that stretches along the track
        thumb_el = _scrollbar_thumb(
            builder, ttk_style, orient, thumb, surface,
            thickness=_THIN_SCROLLBAR_THICKNESS, inset=0,
            cap=_THIN_SCROLLBAR_MIN_THUMB // 2, rounded=False)
        layout(builder.style, ttk_style,
               El(trough_el, sticky=sticky, children=[thumb_el]))
        builder.register_ttkstyle(ttk_style)


@register_builder("round", "scrollbar")
def build_round_scrollbar_style(builder: StyleBuilderTTK, colorname=DEFAULT):
    """Create a round style for the ttk.Scrollbar widget.

    Parameters:

        builder (StyleBuilderTTK):
            The style builder
        colorname (str):
            The color label used to style the widget.
    """
    _build_scrollbar(builder, colorname, rounded=True)


@register_builder("default", "scrollbar")
def build_scrollbar_style(builder: StyleBuilderTTK, colorname=DEFAULT):
    """Create a standard style for the ttk.Scrollbar widget.

    Parameters:

        builder (StyleBuilderTTK):
            The style builder.
        colorname (str):
            The color label used to style the widget.
    """
    _build_scrollbar(builder, colorname, rounded=False)
