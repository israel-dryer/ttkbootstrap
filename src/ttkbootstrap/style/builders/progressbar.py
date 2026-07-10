"""TTK progressbar style recipes."""

import tkinter as tk

from ttkbootstrap.constants import *
from ttkbootstrap.style import StyleBuilderTTK
from ttkbootstrap.style.layout import El, image_element, layout
from ttkbootstrap.style.builders.registry import register_builder


def _create_striped_progressbar_assets(builder, colorname=DEFAULT):
    """Create the horizontal and vertical striped progressbar images.

    Parameters:

        builder (StyleBuilderTTK):
            The style builder.
        colorname (str):
            The color label used to style the widget.

    Returns:

        tuple[str, str]:
            The horizontal and vertical photoimage names.
    """
    if any([colorname == DEFAULT, colorname == ""]):
        bar_color = builder.colors.primary
    else:
        bar_color = builder.colors.get(colorname)

    # A lighter diagonal highlight over the bar. Mixing toward white is
    # self-limiting (a near-white bar barely shifts; a dark bar lifts clearly),
    # which is what the old brightness-adaptive HSV delta hand-rolled.
    bar_color_light = builder.tint(bar_color)
    a = builder.assets

    # Diagonal stripe pattern over a bar_color_light field; the original
    # polygons were hand-fit to a 100-unit canvas, re-expressed here as
    # w/h-relative ratios. The vertical variant is the horizontal one
    # rotated 90 deg CCW.
    def draw_h(d, w, h):
        d.rectangle((0, 0, w, h), fill=bar_color_light)
        d.polygon([(0, 0), (0.48 * w, 0), (w, 0.52 * h), (w, h)], fill=bar_color)
        d.polygon([(0, 0.52 * h), (0.48 * w, h), (0, h)], fill=bar_color)

    def draw_v(d, w, h):
        d.rectangle((0, 0, w, h), fill=bar_color_light)
        d.polygon([(0, h), (0, 0.52 * h), (0.52 * w, 0), (w, 0)], fill=bar_color)
        d.polygon([(0.52 * w, h), (w, 0.52 * h), (w, h)], fill=bar_color)

    h_name = a.image((12, 12), draw_h, bar_color, bar_color_light)
    v_name = a.image((12, 12), draw_v, bar_color, bar_color_light)
    return h_name, v_name


@register_builder("striped", "progressbar")
def build_striped_progressbar_style(builder: StyleBuilderTTK, colorname=DEFAULT):
    """Create a striped style for the ttk.Progressbar widget.

    Parameters:

        builder (StyleBuilderTTK):
            The style builder
        colorname (str):
            The primary widget color label.
    """
    h_ttk_class = "Striped.Horizontal.TProgressbar"
    v_ttk_class = "Striped.Vertical.TProgressbar"

    thickness = builder.scale_size(12)

    if any([colorname == DEFAULT, colorname == ""]):
        h_ttk_style = builder.surface_prefix(h_ttk_class)
        v_ttk_style = builder.surface_prefix(v_ttk_class)
    else:
        h_ttk_style = builder.surface_prefix(f"{colorname}.{h_ttk_class}")
        v_ttk_style = builder.surface_prefix(f"{colorname}.{v_ttk_class}")

    # Recessed neutral trough = border(surface) (bootstack parity), subtle in
    # both modes. The surface (2.0 surface-color) defaults to the theme bg.
    trough_color = builder.border(builder.resolve_surface(builder._surface))
    border_color = trough_color

    # ( horizontal, vertical )
    images = _create_striped_progressbar_assets(builder, colorname)

    # horizontal progressbar
    h_element = h_ttk_style.replace(".TP", ".P")
    # A flat clam trough. Without our own trough element, the layout's
    # `{h_element}.trough` name falls back (via ttk's dotted-name resolution) to
    # the solid progressbar's *rounded* image trough; create a flat clam trough
    # so the square striped bar sits in a square channel.
    builder.style.element_create(f"{h_element}.trough", "from", TTK_CLAM)
    builder.style.element_create(
        f"{h_element}.pbar",
        "image",
        images[0],
        width=thickness,
        sticky=tk.EW,
    )
    layout(builder.style, h_ttk_style,
           El(f"{h_element}.trough", sticky=tk.NSEW, children=[
               El(f"{h_element}.pbar", side=tk.LEFT, sticky=tk.NS)]))
    builder.configure(
        h_ttk_style,
        troughcolor=trough_color,
        thickness=thickness,
        bordercolor=border_color,
        borderwidth=builder.scale_size(1),
    )

    # vertical progressbar
    v_element = v_ttk_style.replace(".TP", ".P")
    builder.style.element_create(f"{v_element}.trough", "from", TTK_CLAM)
    builder.style.element_create(
        f"{v_element}.pbar",
        "image",
        images[1],
        width=thickness,
        sticky=tk.NS,
    )
    layout(builder.style, v_ttk_style,
           El(f"{v_element}.trough", sticky=tk.NSEW, children=[
               El(f"{v_element}.pbar", side=tk.BOTTOM, sticky=tk.EW)]))
    builder.configure(
        v_ttk_style,
        troughcolor=trough_color,
        bordercolor=border_color,
        thickness=thickness,
        borderwidth=builder.scale_size(1),
    )
    builder.register_ttkstyle(h_ttk_style)
    builder.register_ttkstyle(v_ttk_style)


@register_builder("default", "progressbar")
def build_progressbar_style(builder: StyleBuilderTTK, colorname=DEFAULT):
    """Create a solid ttk style for the ttk.Progressbar widget.

    Parameters:

        builder (StyleBuilderTTK):
            The style builder
        colorname (str):
            The primary widget color.
    """
    _create_recolored_progressbar_style(builder,
        colorname, asset_name="progressbar_default", type_name="")


@register_builder("thin", "progressbar")
def build_thin_progressbar_style(builder, colorname=DEFAULT):
    """Create the compact raster-backed ttk.Progressbar style."""
    _create_recolored_progressbar_style(builder,
        colorname, asset_name="progressbar_thin", type_name="Thin.")


def _create_recolored_progressbar_style(
        builder, colorname, *, asset_name, type_name):
    """Build horizontal and vertical progressbars from one source asset."""
    h_base = f"{type_name}Horizontal.TProgressbar"
    v_base = f"{type_name}Vertical.TProgressbar"
    # The surface the bar sits on (2.0 surface-color); default == theme bg. The
    # recessed trough and the widget background both derive from it.
    surface = builder.resolve_surface(builder._surface)
    trough_color = builder.border(surface)

    if colorname in (DEFAULT, ""):
        bar_color = builder.colors.primary
        h_ttk_style = builder.surface_prefix(h_base)
        v_ttk_style = builder.surface_prefix(v_base)
    else:
        bar_color = builder.colors.get(colorname)
        h_ttk_style = builder.surface_prefix(f"{colorname}.{h_base}")
        v_ttk_style = builder.surface_prefix(f"{colorname}.{v_base}")

    a = builder.assets
    h_trough = a.recolor(
        asset_name, white=trough_color, black=trough_color)
    h_bar = a.recolor(asset_name, white=bar_color, black=bar_color)
    v_trough = a.recolor(
        asset_name, white=trough_color, black=trough_color,
        transform="rotate-90")
    v_bar = a.recolor(
        asset_name, white=bar_color, black=bar_color,
        transform="rotate-90")

    h_element = h_ttk_style.replace(".TP", ".P")
    h_trough_name = f"{h_element}.trough"
    h_bar_name = f"{h_element}.pbar"
    image_element(
        builder.style, h_trough_name, default=h_trough.image,
        border=h_trough.meta.border, padding=h_trough.meta.padding,
        sticky=tk.NSEW)
    image_element(
        builder.style, h_bar_name, default=h_bar.image,
        border=h_bar.meta.border, padding=h_bar.meta.padding)
    layout(builder.style, h_ttk_style,
           El(h_trough_name, sticky=tk.NSEW, children=[
               El(h_bar_name, side=tk.LEFT, sticky=tk.EW)]))

    v_element = v_ttk_style.replace(".TP", ".P")
    v_trough_name = f"{v_element}.trough"
    v_bar_name = f"{v_element}.pbar"
    image_element(
        builder.style, v_trough_name, default=v_trough.image,
        border=v_trough.meta.border, padding=v_trough.meta.padding,
        sticky=tk.NSEW)
    image_element(
        builder.style, v_bar_name, default=v_bar.image,
        border=v_bar.meta.border, padding=v_bar.meta.padding)
    layout(builder.style, v_ttk_style,
           El(v_trough_name, sticky=tk.NSEW, children=[
               El(v_bar_name, side=tk.BOTTOM, sticky=tk.NS)]))

    builder.configure(
        h_ttk_style, background=surface, troughcolor=trough_color,
        thickness=h_trough.meta.height, borderwidth=0)
    builder.configure(
        v_ttk_style, background=surface, troughcolor=trough_color,
        thickness=v_trough.meta.width, borderwidth=0)

    # register styles
    builder.register_ttkstyle(h_ttk_style)
    builder.register_ttkstyle(v_ttk_style)
