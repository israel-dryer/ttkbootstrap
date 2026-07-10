"""TTK scrollbar style recipes."""

import tkinter as tk

from ttkbootstrap.constants import *
from ttkbootstrap.style import StyleBuilderTTK
from ttkbootstrap.style.layout import El, image_element, layout
from ttkbootstrap.style.builders.registry import register_builder


# A few-pixel thumb for the 'thin' variant -- suits narrow lists/dropdowns.
_THIN_SCROLLBAR_THICKNESS = 4

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
# trough shows around it. Baked into the thumb image (a transparent margin) --
# ttk's trough borderwidth doesn't reliably inset an image thumb.
_SCROLLBAR_THUMB_INSET = 1
_SCROLLBAR_MIN_THUMB = 16  # minimum thumb length (logical) so it stays grabbable


def _scrollbar_thumb(builder, color, orient, rounded):
    """A thumb image with a transparent cross-axis margin, so the trough shows
    around it. Returns (image_name, border) for `image_element`.

    Square thumbs are a solid rect that stretches uniformly (border 0); round
    thumbs are a capped pill 9-sliced along the length so the caps don't
    distort when the thumb stretches.
    """
    a = builder.assets
    inset = _SCROLLBAR_THUMB_INSET
    t = _SCROLLBAR_THICKNESS
    cross = 0 if orient == "vertical" else 1  # x for vertical, y for horizontal

    def draw(d, w, h):
        dims = (w, h)
        margin = round(dims[cross] * inset / t)
        box = [0, 0, w - 1, h - 1]
        box[cross] += margin
        box[cross + 2] -= margin
        if rounded:
            radius = round((dims[cross] - 2 * margin) / 2)
            d.rounded_rectangle(box, radius=radius, fill=color)
        else:
            d.rectangle(box, fill=color)

    # A 9-slice border sets the *minimum* thumb length -- its fixed end regions
    # can't shrink -- so a long list (e.g. the font family picker) can't squash
    # the thumb to a microscopic sliver. For the round thumb those end regions
    # also hold the rounded caps.
    cap = builder.scale_size(_SCROLLBAR_MIN_THUMB // 2)
    length = _SCROLLBAR_MIN_THUMB + 1
    if orient == "vertical":
        size = (t, length)
        border = (0, cap)
    else:
        size = (length, t)
        border = (cap, 0)
    return a.image(size, draw, "scrollbar-thumb", color, orient, rounded), border


def _build_scrollbar(builder: StyleBuilderTTK, colorname, rounded):
    """Build the horizontal + vertical scrollbar styles (square or round).

    A subtle visible trough (every region shares the trough color, so the whole
    widget reads as one track) with an inset thumb, no arrows.
    """
    ttk_class = "TScrollbar"
    prefix = "Round." if rounded else ""
    trough = _scrollbar_trough(builder)
    thumb = _scrollbar_thumb_color(builder, colorname)
    pressed = builder.pressed(thumb)
    active = builder.active(thumb)

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
        normal, border = _scrollbar_thumb(builder, thumb, orient, rounded)
        pressed_img, _ = _scrollbar_thumb(builder, pressed, orient, rounded)
        active_img, _ = _scrollbar_thumb(builder, active, orient, rounded)
        image_element(
            builder.style, f"{ttk_style}.thumb", default=normal,
            states={"pressed": pressed_img, "active": active_img},
            border=border, sticky=sticky)
        layout(builder.style, ttk_style,
               El(trough_el, sticky=sticky, children=[
                   El(f"{ttk_style}.thumb", expand="1", sticky=sticky)]))
        builder.register_ttkstyle(ttk_style)


@register_builder("thin", "scrollbar")
def build_thin_scrollbar_style(builder: StyleBuilderTTK, colorname=DEFAULT):
    """Create a thin scrollbar style for the ttk.Scrollbar widget.

    A few-pixel flat thumb on a surface-matched track, no arrows -- for narrow
    lists and dropdowns where the bar is more a scroll *indicator* than a drag
    handle (combobox popdown, font picker, ...). The thumb shares the neutral/
    accent color of the standard bar (`_scrollbar_thumb_color`) and darkens/
    lightens on hover/press. Ported from bootstack (mechanism, not API): a solid
    box thumb via the `rect` toolkit rather than a rounded PNG.

    Parameters:

        builder (StyleBuilderTTK):
            The style builder
        colorname (str):
            The color label used to style the widget.
    """
    ttk_class = "TScrollbar"
    # The surface the bar sits on (2.0 surface-color); default == theme bg.
    surface = builder.resolve_surface(builder._surface)

    if any([colorname == DEFAULT, colorname == ""]):
        h_ttk_style = builder.surface_prefix(f"Thin.Horizontal.{ttk_class}")
        v_ttk_style = builder.surface_prefix(f"Thin.Vertical.{ttk_class}")
    else:
        h_ttk_style = builder.surface_prefix(f"{colorname}.Thin.Horizontal.{ttk_class}")
        v_ttk_style = builder.surface_prefix(f"{colorname}.Thin.Vertical.{ttk_class}")
    # share the darker, clearly-visible thumb color with the default/round bars
    thumb = _scrollbar_thumb_color(builder, colorname)

    active = builder.active(thumb)
    pressed = builder.pressed(thumb)
    a = builder.assets
    t = _THIN_SCROLLBAR_THICKNESS

    def _configure(ttk_style):
        builder.configure(
            ttk_style,
            troughcolor=surface,
            bordercolor=surface,
            background=surface,
            relief=tk.FLAT,
            borderwidth=0,
            arrowsize=0,
        )

    # horizontal: a `t`-px-thick sliver that stretches along the track (EW)
    _configure(h_ttk_style)
    image_element(
        builder.style, f"{h_ttk_style}.thumb",
        default=a.rect(thumb, (8, t)),
        states={"pressed": a.rect(pressed, (8, t)),
                "active": a.rect(active, (8, t))},
        border=0, sticky="ew")
    layout(builder.style, h_ttk_style,
           El("Horizontal.Scrollbar.trough", sticky="we", children=[
               El(f"{h_ttk_style}.thumb", expand="1", sticky="we")]))

    # vertical
    _configure(v_ttk_style)
    image_element(
        builder.style, f"{v_ttk_style}.thumb",
        default=a.rect(thumb, (t, 8)),
        states={"pressed": a.rect(pressed, (t, 8)),
                "active": a.rect(active, (t, 8))},
        border=0, sticky="ns")
    layout(builder.style, v_ttk_style,
           El("Vertical.Scrollbar.trough", sticky="ns", children=[
               El(f"{v_ttk_style}.thumb", expand="1", sticky="ns")]))

    builder.register_ttkstyle(h_ttk_style)
    builder.register_ttkstyle(v_ttk_style)


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
