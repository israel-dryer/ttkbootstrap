"""TTK scrollbar style recipes."""

import tkinter as tk

from ttkbootstrap.constants import *
from ttkbootstrap.style import StyleBuilderTTK
from ttkbootstrap.style.layout import El, image_element, layout
from ttkbootstrap.style.builders.registry import register_builder


# A few-pixel thumb for the 'thin' variant -- suits narrow lists/dropdowns.
_THIN_SCROLLBAR_THICKNESS = 4


@register_builder("thin", "scrollbar")
def build_thin_scrollbar_style(builder: StyleBuilderTTK, colorname=DEFAULT):
    """Create a thin scrollbar style for the ttk.Scrollbar widget.

    A few-pixel flat thumb on a surface-matched track, no arrows -- for narrow
    lists and dropdowns where the bar is more a scroll *indicator* than a drag
    handle (combobox popdown, font picker, ...). The thumb is neutral (the
    surface border color) by default, or the accent when a color is given, and
    darkens/lightens on hover/press. Ported from bootstack (mechanism, not API):
    a solid box thumb via the `rect` toolkit rather than a rounded PNG.

    Parameters:

        builder (StyleBuilderTTK):
            The style builder
        colorname (str):
            The color label used to style the widget.
    """
    ttk_class = "TScrollbar"
    surface = builder.colors.bg

    if any([colorname == DEFAULT, colorname == ""]):
        h_ttk_style = f"Thin.Horizontal.{ttk_class}"
        v_ttk_style = f"Thin.Vertical.{ttk_class}"
        thumb = builder.border(surface)  # neutral by default
    else:
        h_ttk_style = f"{colorname}.Thin.Horizontal.{ttk_class}"
        v_ttk_style = f"{colorname}.Thin.Vertical.{ttk_class}"
        thumb = builder.colors.get(colorname)

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
               El(f"{h_ttk_style}.thumb", expand="1", sticky="ew")]))

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


def _create_round_scrollbar_assets(builder, thumb_color, pressed, active):
    """Create image assets to be used when building the round
    scrollbar style.

    Parameters:

        thumb_color (str):
            The color value of the thumb in normal state.

        pressed (str):
            The color value to use when the thumb is pressed.

        active (str):
            The color value to use when the thumb is active or
            hovered.
    """
    return _create_scrollbar_assets(builder, thumb_color, pressed, active)


@register_builder("round", "scrollbar")
def build_round_scrollbar_style(builder: StyleBuilderTTK, colorname=DEFAULT):
    """Create a round style for the ttk.Scrollbar widget.

    Parameters:

        builder (StyleBuilderTTK):
            The style builder
        colorname (str):
            The color label used to style the widget.
    """
    ttk_class = "TScrollbar"

    if any([colorname == DEFAULT, colorname == ""]):
        h_ttk_style = f"Round.Horizontal.{ttk_class}"
        v_ttk_style = f"Round.Vertical.{ttk_class}"

        if builder.is_light_theme:
            background = builder.colors.border
        else:
            background = builder.colors.selectbg

    else:
        h_ttk_style = f"{colorname}.Round.Horizontal.{ttk_class}"
        v_ttk_style = f"{colorname}.Round.Vertical.{ttk_class}"
        background = builder.colors.get(colorname)

    pressed = builder.pressed(background)
    active = builder.active(background)

    scroll_images = _create_round_scrollbar_assets(builder, background, pressed, active)

    # horizontal scrollbar
    builder.configure(
        h_ttk_style,
        troughcolor=builder.colors.bg,
        darkcolor=builder.colors.bg,
        bordercolor=builder.colors.bg,
        lightcolor=builder.colors.bg,
        background=builder.colors.bg,
        relief=tk.FLAT,
        borderwidth=0,
    )
    image_element(
        builder.style, f"{h_ttk_style}.thumb", default=scroll_images[0].image,
        states={"pressed": scroll_images[1].image,
                "active": scroll_images[2].image},
        border=scroll_images[0].meta.border,
        padding=scroll_images[0].meta.padding)
    layout(builder.style, h_ttk_style,
           El("Horizontal.Scrollbar.trough", sticky="we", children=[
               El(f"{h_ttk_style}.thumb", expand="1", sticky="we")]))

    # vertical scrollbar
    builder.configure(
        v_ttk_style,
        troughcolor=builder.colors.bg,
        darkcolor=builder.colors.bg,
        bordercolor=builder.colors.bg,
        lightcolor=builder.colors.bg,
        background=builder.colors.bg,
        relief=tk.FLAT,
    )
    image_element(
        builder.style, f"{v_ttk_style}.thumb", default=scroll_images[3].image,
        states={"pressed": scroll_images[4].image,
                "active": scroll_images[5].image},
        border=scroll_images[3].meta.border,
        padding=scroll_images[3].meta.padding)
    layout(builder.style, v_ttk_style,
           El("Vertical.Scrollbar.trough", sticky="ns", children=[
               El(f"{v_ttk_style}.thumb", expand="1", sticky="ns")]))

    # register ttk styles
    builder.register_ttkstyle(h_ttk_style)
    builder.register_ttkstyle(v_ttk_style)


def _create_scrollbar_assets(builder: StyleBuilderTTK, thumb_color, pressed, active):
    """Create the image assets used to build the standard scrollbar
    style.

    Parameters:
        builder (StyleBuilderTTK):
            The style builder.

        thumb_color (str):
            The primary color value used to color the thumb.

        pressed (str):
            The color value to use when the thumb is pressed.

        active (str):
            The color value to use when the thumb is active or
            hovered.
    """
    a = builder.assets
    h_normal = a.recolor("scrollbar_thumb", white=thumb_color, black=thumb_color)
    h_pressed = a.recolor("scrollbar_thumb", white=pressed, black=pressed)
    h_active = a.recolor("scrollbar_thumb", white=active, black=active)
    v_normal = a.recolor("scrollbar_thumb", white=thumb_color, black=thumb_color, transform="rotate-90")
    v_pressed = a.recolor("scrollbar_thumb", white=pressed, black=pressed, transform="rotate-90")
    v_active = a.recolor("scrollbar_thumb", white=active, black=active, transform="rotate-90")
    return h_normal, h_pressed, h_active, v_normal, v_pressed, v_active


@register_builder("default", "scrollbar")
def build_scrollbar_style(builder: StyleBuilderTTK, colorname=DEFAULT):
    """Create a standard style for the ttk.Scrollbar widget.

    Parameters:

        builder (StyleBuilderTTK):
            The style builder.
        colorname (str):
            The color label used to style the widget.
    """
    ttk_class = "TScrollbar"

    if any([colorname == DEFAULT, colorname == ""]):
        h_ttk_style = f"Horizontal.{ttk_class}"
        v_ttk_style = f"Vertical.{ttk_class}"

        if builder.is_light_theme:
            background = builder.colors.border
        else:
            background = builder.colors.selectbg

    else:
        h_ttk_style = f"{colorname}.Horizontal.{ttk_class}"
        v_ttk_style = f"{colorname}.Vertical.{ttk_class}"
        background = builder.colors.get(colorname)

    pressed = builder.pressed(background)
    active = builder.active(background)

    scroll_images = _create_scrollbar_assets(builder,
        background, pressed, active
    )
    # horizontal scrollbar
    builder.configure(
        h_ttk_style,
        troughcolor=builder.colors.bg,
        darkcolor=builder.colors.bg,
        bordercolor=builder.colors.bg,
        lightcolor=builder.colors.bg,
        arrowcolor=background,
        arrowsize=builder.scale_size(11),
        background=builder.colors.bg,
        relief=tk.FLAT,
        borderwidth=0,
    )
    image_element(
        builder.style, f"{h_ttk_style}.thumb", default=scroll_images[0].image,
        states={"pressed": scroll_images[1].image,
                "active": scroll_images[2].image},
        border=scroll_images[0].meta.border,
        padding=scroll_images[0].meta.padding)
    layout(builder.style, h_ttk_style,
           El("Horizontal.Scrollbar.trough", sticky="we", children=[
               El(f"{h_ttk_style}.thumb", expand="1", sticky="we")]))

    # vertical scrollbar
    builder.configure(
        v_ttk_style,
        troughcolor=builder.colors.bg,
        darkcolor=builder.colors.bg,
        bordercolor=builder.colors.bg,
        lightcolor=builder.colors.bg,
        arrowcolor=background,
        arrowsize=builder.scale_size(11),
        background=builder.colors.bg,
        relief=tk.FLAT,
        borderwidth=0,
    )
    image_element(
        builder.style, f"{v_ttk_style}.thumb", default=scroll_images[3].image,
        states={"pressed": scroll_images[4].image,
                "active": scroll_images[5].image},
        border=scroll_images[3].meta.border,
        padding=scroll_images[3].meta.padding)
    layout(builder.style, v_ttk_style,
           El("Vertical.Scrollbar.trough", sticky="ns", children=[
               El(f"{v_ttk_style}.thumb", expand="1", sticky="ns")]))

    # register ttk_styles
    builder.register_ttkstyle(h_ttk_style)
    builder.register_ttkstyle(v_ttk_style)
