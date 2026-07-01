"""TTK scale style recipes."""

from ttkbootstrap.constants import *
from ttkbootstrap.style import StyleBuilderTTK
from ttkbootstrap.style.layout import El, StyleName, image_element, layout
from ttkbootstrap.style.theme import Colors
from ttkbootstrap.style.builders.registry import register_builder


def _create_scale_assets(builder, colorname=DEFAULT):
    """Create the assets used for the ttk.Scale widget.

    The slider handle is automatically adjusted to fit the
    screen resolution.

    Parameters:

        colorname (str):
            The color label.

    Returns:

        tuple[RecolorResult, ...]:
            Recolored handle and track assets.
    """
    a = builder.assets
    disabled_color = builder.disabled("text")
    if builder.is_light_theme:
        track_color = builder.colors.bg if colorname == LIGHT else builder.colors.light
    else:
        track_color = Colors.update_hsv(builder.colors.selectbg, vd=-0.2)

    if any([colorname == DEFAULT, colorname == ""]):
        normal_color = builder.colors.primary
    else:
        normal_color = builder.colors.get(colorname)
    pressed_color = builder.pressed(normal_color)
    hover_color = builder.active(normal_color)

    # ( normal, pressed, hover, disabled thumbs; horizontal, vertical track )
    return (
        a.recolor("slider_handle", white=builder.colors.bg,
                  black=disabled_color, magenta=normal_color),
        a.recolor("slider_handle", white=builder.colors.bg,
                  black=disabled_color, magenta=pressed_color),
        a.recolor("slider_handle", white=builder.colors.bg,
                  black=disabled_color, magenta=hover_color),
        a.recolor("slider_handle", white=builder.colors.bg,
                  black=disabled_color, magenta=disabled_color),
        a.recolor("slider_track", white=track_color, black=track_color),
        a.recolor("slider_track", white=track_color, black=track_color,
                  transform="rotate-90"),
    )


@register_builder("default", "scale")
def build_scale_style(builder: StyleBuilderTTK, colorname=DEFAULT):
    """Create a style for the ttk.Scale widget.

    Parameters:

        builder (StyleBuilderTTK):
            The style builder.
        colorname (str):
            The color label used to style the widget.
    """
    h = StyleName("TScale", colorname, orient="Horizontal")
    v = StyleName("TScale", colorname, orient="Vertical")

    # ( normal, pressed, hover, disabled, htrack, vtrack )
    images = _create_scale_assets(builder, colorname)

    # horizontal scale
    image_element(
        builder.style, f"{h.element}.slider", default=images[0].image,
        states={"disabled": images[3].image, "pressed": images[1].image,
                "hover": images[2].image},
        border=images[0].meta.border, padding=images[0].meta.padding)
    builder.style.element_create(
        f"{h.element}.track", "image", images[4].image,
        border=images[4].meta.border, padding=images[4].meta.padding)
    layout(
        builder.style, h.ttk_style,
        El(f"{h.element}.focus", expand=1, sticky=NSEW, children=[
            El(f"{h.element}.track", sticky=EW),
            El(f"{h.element}.slider", side=LEFT, sticky="")]))

    # vertical scale
    image_element(
        builder.style, f"{v.element}.slider", default=images[0].image,
        states={"disabled": images[3].image, "pressed": images[1].image,
                "hover": images[2].image},
        border=images[0].meta.border, padding=images[0].meta.padding)
    builder.style.element_create(
        f"{v.element}.track", "image", images[5].image,
        border=images[5].meta.border, padding=images[5].meta.padding)
    layout(
        builder.style, v.ttk_style,
        El(f"{v.element}.focus", expand=1, sticky=NSEW, children=[
            El(f"{v.element}.track", sticky=NS),
            El(f"{v.element}.slider", side=TOP, sticky="")]))


    # register ttk styles
    builder.register_ttkstyle(h.ttk_style)
    builder.register_ttkstyle(v.ttk_style)
