"""TTK treeview style recipes."""

import tkinter as tk
from tkinter import font

from ttkbootstrap.constants import *
from ttkbootstrap.style import StyleBuilderTTK
from ttkbootstrap.style.layout import El, layout
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
    metrics = f.metrics()
    # A comfortable data-grid row: the text line plus ~half an ascent of
    # breathing room. Bare `linespace` (1.x) left the text flush to the row
    # edges; `linespace + ascent` overshot to nearly 2x the line height.
    row_height = metrics['linespace'] + metrics['ascent'] // 2
    on_disabled = builder.disabled("text", builder.colors.inputbg)

    if any([colorname == DEFAULT, colorname == ""]):
        background = builder.colors.inputbg
        on_background = builder.colors.inputfg
        tb_ttk_style = ttk_class
        th_ttk_style = f"{ttk_class}.Heading"
    elif colorname == LIGHT and builder.is_light_theme:
        background = builder.colors.get(colorname)
        on_background = builder.on_color(background)
        tb_ttk_style = f"{colorname}.{ttk_class}"
        th_ttk_style = f"{colorname}.{ttk_class}.Heading"
    else:
        background = builder.colors.get(colorname)
        on_background = builder.on_color(background)
        tb_ttk_style = f"{colorname}.{ttk_class}"
        th_ttk_style = f"{colorname}.{ttk_class}.Heading"
    hover = builder.active(background)
    header_border = builder.border(background)
    body_border = builder.border(builder.colors.inputbg)

    # treeview header
    builder.configure(
        th_ttk_style,
        background=background,
        foreground=on_background,
        relief=RAISED,
        borderwidth=builder.scale_size(1),
        darkcolor=header_border,
        bordercolor=background,
        lightcolor=background,
        padding=builder.scale_size(5),
    )
    builder.style.map(
        th_ttk_style,
        foreground=[("disabled", on_disabled)],
        background=[("active !disabled", hover)],
        lightcolor=[("active !disabled", hover)],
        darkcolor=[("active !disabled", hover)],
        bordercolor=[("active !disabled", hover)]
    )
    builder.configure(
        tb_ttk_style,
        background=builder.colors.inputbg,
        fieldbackground=builder.colors.inputbg,
        foreground=builder.colors.inputfg,
        bordercolor=body_border,
        lightcolor=builder.colors.inputbg,
        darkcolor=builder.colors.inputbg,
        borderwidth=builder.scale_size(1),
        padding=0,
        rowheight=row_height,
        relief=tk.RAISED,
    )
    builder.style.map(
        tb_ttk_style,
        background=[("selected", builder.colors.selectbg)],
        foreground=[
            ("disabled", on_disabled),
            ("selected", builder.colors.selectfg),
        ],
    )
    layout(builder.style, tb_ttk_style,
           El("Button.border", sticky=tk.NSEW, border=builder.scale_size(1), children=[
               El("Treeview.padding", sticky=tk.NSEW, children=[
                   El("Treeview.treearea", sticky=tk.NSEW)])]))

    # register ttk styles
    builder.register_ttkstyle(tb_ttk_style)


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

    border = builder.border(builder.colors.bg)
    on_disabled = builder.disabled("text", builder.colors.inputbg)

    if any([colorname == DEFAULT, colorname == ""]):
        background = builder.colors.inputbg
        on_background = builder.colors.inputfg
        tb_ttk_style = ttk_class
        th_ttk_style = f"{ttk_class}.Heading"
    elif colorname == LIGHT and builder.is_light_theme:
        background = builder.colors.get(colorname)
        on_background = builder.on_color(background)
        tb_ttk_style = f"{colorname}.{ttk_class}"
        th_ttk_style = f"{colorname}.{ttk_class}.Heading"
    else:
        background = builder.colors.get(colorname)
        on_background = builder.on_color(background)
        tb_ttk_style = f"{colorname}.{ttk_class}"
        th_ttk_style = f"{colorname}.{ttk_class}.Heading"

    # treeview header
    builder.configure(
        th_ttk_style,
        background=background,
        foreground=on_background,
        relief=tk.FLAT,
        padding=builder.scale_size(5),
    )
    builder.style.map(
        th_ttk_style,
        foreground=[("disabled", on_disabled)],
        bordercolor=[("focus !disabled", background)],
    )
    # treeview body
    builder.configure(
        tb_ttk_style,
        background=builder.colors.inputbg,
        fieldbackground=builder.colors.inputbg,
        foreground=builder.colors.inputfg,
        bordercolor=border,
        lightcolor=builder.colors.inputbg,
        darkcolor=builder.colors.inputbg,
        borderwidth=builder.scale_size(2),
        padding=0,
        rowheight=row_height,
        relief=tk.RAISED,
    )
    builder.style.map(
        tb_ttk_style,
        background=[("selected", builder.colors.selectbg)],
        foreground=[
            ("disabled", on_disabled),
            ("selected", builder.colors.selectfg),
        ],
    )
    layout(builder.style, tb_ttk_style,
           El("Button.border", sticky=tk.NSEW, border=builder.scale_size(1), children=[
               El("Treeview.padding", sticky=tk.NSEW, children=[
                   El("Treeview.treearea", sticky=tk.NSEW)])]))

    try:
        builder.style.element_create("Treeitem.indicator", "from", TTK_ALT)
    except:
        pass

    # register ttk styles
    builder.register_ttkstyle(tb_ttk_style)
