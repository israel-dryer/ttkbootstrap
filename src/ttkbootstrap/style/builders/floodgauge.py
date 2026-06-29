"""TTK floodgauge style recipes."""

import tkinter as tk

from ttkbootstrap.constants import *
from ttkbootstrap.style import StyleBuilderTTK
from ttkbootstrap.style.layout import El, layout
from ttkbootstrap.style.theme import Colors
from ttkbootstrap.style.builders.registry import register_builder


@register_builder("default", "floodgauge")
def build_floodgauge_style(builder: StyleBuilderTTK, colorname=DEFAULT):
    """Create a ttk style for the ttkbootstrap.widgets.Floodgauge
    widget. This is a custom widget style that uses components of
    the progressbar and label.

    Parameters:

        builder (StyleBuilderTTK):
            The style builder
        colorname (str):
            The color label used to style the widget.
    """
    horizontal_style_class = "Horizontal.TFloodgauge"
    vertical_style_class = "Vertical.TFloodgauge"
    flood_font = "-size 14"

    if any([colorname == DEFAULT, colorname == ""]):
        h_ttk_style = horizontal_style_class
        v_ttk_style = vertical_style_class
        background = builder.colors.primary
    else:
        h_ttk_style = f"{colorname}.{horizontal_style_class}"
        v_ttk_style = f"{colorname}.{vertical_style_class}"
        background = builder.colors.get(colorname)

    if colorname == LIGHT:
        foreground = builder.colors.fg
        trough_color = builder.colors.bg
    else:
        trough_color = Colors.update_hsv(background, sd=-0.3, vd=0.8)
        foreground = builder.colors.selectfg

    # horizontal floodgauge
    h_element = h_ttk_style.replace(".TF", ".F")
    builder.style.element_create(f"{h_element}.trough", "from", TTK_CLAM)
    builder.style.element_create(f"{h_element}.pbar", "from", TTK_DEFAULT)
    layout(builder.style, h_ttk_style,
           El(f"{h_element}.trough", sticky=tk.NSEW, children=[
               El(f"{h_element}.pbar", sticky=tk.NS),
               El("Floodgauge.label", sticky="")]))
    builder.configure(
        h_ttk_style,
        thickness=50,
        borderwidth=1,
        bordercolor=background,
        lightcolor=background,
        pbarrelief=tk.FLAT,
        troughcolor=trough_color,
        background=background,
        foreground=foreground,
        justify=tk.CENTER,
        anchor=tk.CENTER,
        font=flood_font,
    )
    # vertical floodgauge
    v_element = v_ttk_style.replace(".TF", ".F")
    builder.style.element_create(f"{v_element}.trough", "from", TTK_CLAM)
    builder.style.element_create(f"{v_element}.pbar", "from", TTK_DEFAULT)
    layout(builder.style, v_ttk_style,
           El(f"{v_element}.trough", sticky=tk.NSEW, children=[
               El(f"{v_element}.pbar", sticky=tk.EW),
               El("Floodgauge.label", sticky="")]))
    builder.configure(
        v_ttk_style,
        thickness=50,
        borderwidth=1,
        bordercolor=background,
        lightcolor=background,
        pbarrelief=tk.FLAT,
        troughcolor=trough_color,
        background=background,
        foreground=foreground,
        justify=tk.CENTER,
        anchor=tk.CENTER,
        font=flood_font,
    )
    # register ttk_styles
    builder.register_ttkstyle(h_ttk_style)
    builder.register_ttkstyle(v_ttk_style)
