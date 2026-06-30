"""TTK treeview style recipes."""

import tkinter as tk
from tkinter import font

from ttkbootstrap.constants import *
from ttkbootstrap.style import StyleBuilderTTK
from ttkbootstrap.style.layout import El, layout
from ttkbootstrap.style.theme import Colors
from ttkbootstrap.style.builders.registry import register_builder


@register_builder("table", "treeview")
def build_table_treeview_style(builder: StyleBuilderTTK, colorname=DEFAULT):
    """Create a style for the Tableview widget.

    Parameters:

        builder (StyleBuilderTTK):
            The style builder
        colorname (str):
            The color label used to style the widget.
    """
    ttk_class = "Table.Treeview"

    f = font.nametofont("TkDefaultFont")
    row_height = f.metrics()["linespace"]

    if builder.is_light_theme:
        disabled_fg = Colors.update_hsv(builder.colors.inputbg, vd=-0.2)
        border_color = builder.colors.border
        hover = Colors.update_hsv(builder.colors.light, vd=-0.1)
    else:
        disabled_fg = Colors.update_hsv(builder.colors.inputbg, vd=-0.3)
        border_color = builder.colors.selectbg
        hover = Colors.update_hsv(builder.colors.dark, vd=0.1)

    if any([colorname == DEFAULT, colorname == ""]):
        background = builder.colors.inputbg
        foreground = builder.colors.inputfg
        body_style = ttk_class
        header_style = f"{ttk_class}.Heading"
    elif colorname == LIGHT and builder.is_light_theme:
        background = builder.colors.get(colorname)
        foreground = builder.colors.fg
        body_style = f"{colorname}.{ttk_class}"
        header_style = f"{colorname}.{ttk_class}.Heading"
        hover = Colors.update_hsv(background, vd=-0.1)
    else:
        background = builder.colors.get(colorname)
        foreground = builder.colors.selectfg
        body_style = f"{colorname}.{ttk_class}"
        header_style = f"{colorname}.{ttk_class}.Heading"
        hover = Colors.update_hsv(background, vd=0.1)

    # treeview header
    builder.configure(
        header_style,
        background=background,
        foreground=foreground,
        relief=RAISED,
        borderwidth=builder.scale_size(1),
        darkcolor=background,
        bordercolor=border_color,
        lightcolor=background,
        padding=builder.scale_size(5),
    )
    builder.style.map(
        header_style,
        foreground=[("disabled", disabled_fg)],
        background=[
            ("active !disabled", hover),
        ],
        darkcolor=[
            ("active !disabled", hover),
        ],
        lightcolor=[
            ("active !disabled", hover),
        ],
    )
    builder.configure(
        body_style,
        background=builder.colors.inputbg,
        fieldbackground=builder.colors.inputbg,
        foreground=builder.colors.inputfg,
        bordercolor=border_color,
        lightcolor=builder.colors.inputbg,
        darkcolor=builder.colors.inputbg,
        borderwidth=builder.scale_size(2),
        padding=0,
        rowheight=row_height,
        relief=tk.RAISED,
    )
    builder.style.map(
        body_style,
        background=[("selected", builder.colors.selectbg)],
        foreground=[
            ("disabled", disabled_fg),
            ("selected", builder.colors.selectfg),
        ],
    )
    layout(builder.style, body_style,
           El("Button.border", sticky=tk.NSEW, border=builder.scale_size(1), children=[
               El("Treeview.padding", sticky=tk.NSEW, children=[
                   El("Treeview.treearea", sticky=tk.NSEW)])]))

    # register ttk styles
    builder.register_ttkstyle(body_style)


@register_builder("default", "treeview")
def build_treeview_style(builder: StyleBuilderTTK, colorname=DEFAULT):
    """Create a style for the ttk.Treeview widget.

    Parameters:

        builder (StyleBuilderTTK):
            The style builder
        colorname (str):
            The color label used to style the widget.
    """
    ttk_class = "Treeview"

    f = font.nametofont("TkDefaultFont")
    row_height = f.metrics()["linespace"]

    if builder.is_light_theme:
        disabled_fg = Colors.update_hsv(builder.colors.inputbg, vd=-0.2)
        border_color = builder.colors.border
    else:
        disabled_fg = Colors.update_hsv(builder.colors.inputbg, vd=-0.3)
        border_color = builder.colors.selectbg

    if any([colorname == DEFAULT, colorname == ""]):
        background = builder.colors.inputbg
        foreground = builder.colors.inputfg
        body_style = ttk_class
        header_style = f"{ttk_class}.Heading"
        focus_color = builder.colors.primary
    elif colorname == LIGHT and builder.is_light_theme:
        background = builder.colors.get(colorname)
        foreground = builder.colors.fg
        body_style = f"{colorname}.{ttk_class}"
        header_style = f"{colorname}.{ttk_class}.Heading"
        focus_color = background
        border_color = focus_color
    else:
        background = builder.colors.get(colorname)
        foreground = builder.colors.selectfg
        body_style = f"{colorname}.{ttk_class}"
        header_style = f"{colorname}.{ttk_class}.Heading"
        focus_color = background
        border_color = focus_color

    # treeview header
    builder.configure(
        header_style,
        background=background,
        foreground=foreground,
        relief=tk.FLAT,
        padding=builder.scale_size(5),
    )
    builder.style.map(
        header_style,
        foreground=[("disabled", disabled_fg)],
        bordercolor=[("focus !disabled", background)],
    )
    # treeview body
    builder.configure(
        body_style,
        background=builder.colors.inputbg,
        fieldbackground=builder.colors.inputbg,
        foreground=builder.colors.inputfg,
        bordercolor=border_color,
        lightcolor=builder.colors.inputbg,
        darkcolor=builder.colors.inputbg,
        borderwidth=builder.scale_size(2),
        padding=0,
        rowheight=row_height,
        relief=tk.RAISED,
    )
    builder.style.map(
        body_style,
        background=[("selected", builder.colors.selectbg)],
        foreground=[
            ("disabled", disabled_fg),
            ("selected", builder.colors.selectfg),
        ],
        bordercolor=[
            ("disabled", border_color),
            ("focus", focus_color),
            ("pressed", focus_color),
            ("hover", focus_color),
        ],
        lightcolor=[("focus", focus_color)],
        darkcolor=[("focus", focus_color)],
    )
    layout(builder.style, body_style,
           El("Button.border", sticky=tk.NSEW, border=builder.scale_size(1), children=[
               El("Treeview.padding", sticky=tk.NSEW, children=[
                   El("Treeview.treearea", sticky=tk.NSEW)])]))

    try:
        builder.style.element_create("Treeitem.indicator", "from", TTK_ALT)
    except:
        pass

    # register ttk styles
    builder.register_ttkstyle(body_style)
