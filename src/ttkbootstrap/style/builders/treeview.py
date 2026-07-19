"""TTK treeview style recipes."""

import tkinter as tk
from tkinter import font

from ttkbootstrap.constants import *
from ttkbootstrap.style import StyleBuilderTTK
from ttkbootstrap.style.layout import El, layout
from ttkbootstrap.style.builders.registry import register_builder


def _style_font_metrics(builder: StyleBuilderTTK, ttk_style: str):
    """Return ``(linespace, ascent)`` of the font `ttk_style` actually uses.

    Row height must follow the configured font, not a fixed default: a font set
    on `.` or `Treeview` (the documented technique) otherwise leaves taller text
    clipped (#1160). `_effective_style_option` resolves the font a durable user
    override will land on as well as the inherited Tcl value, so the row is sized
    from the font the style ends up with rather than the one it had mid-build.

    Measured with Tk's ``font metrics``, which accepts any font *description* --
    a named font, a ``("family", size)`` tuple, or a ``-size N`` spec -- so no
    Font object is allocated per build.
    """
    spec = builder.style._effective_style_option(ttk_style, "font", "TkDefaultFont")
    try:
        measure = builder.style.tk.call
        return (
            int(measure("font", "metrics", spec, "-linespace")),
            int(measure("font", "metrics", spec, "-ascent")),
        )
    except tk.TclError:
        metrics = font.nametofont("TkDefaultFont").metrics()
        return metrics["linespace"], metrics["ascent"]


# Row heights are computed in these helpers rather than inline so the geometry
# passed to `configure(rowheight=...)` carries no numeric literal: font metrics
# are already DPI-physical, and a ratio of one is physical too (it must NOT go
# through the scaling service). Keeping the ratio here states that once.

def _grid_row_height(builder: StyleBuilderTTK, ttk_style: str) -> int:
    """Data-grid row: the text line plus ~half an ascent of breathing room.

    Bare `linespace` (1.x) left the text flush to the row edges;
    `linespace + ascent` overshot to nearly 2x the line height.
    """
    linespace, ascent = _style_font_metrics(builder, ttk_style)
    return linespace + ascent // 2


def _tree_row_height(builder: StyleBuilderTTK, ttk_style: str) -> int:
    """Plain tree row: flush to the text line."""
    linespace, _ = _style_font_metrics(builder, ttk_style)
    return linespace


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
    # Sized from the style's own font, so a configured font sizes the row
    # instead of clipping it (#1160).
    row_height = _grid_row_height(builder, tb_ttk_style)

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

    # Sized from the style's own font, so a configured font sizes the row
    # instead of clipping it (#1160).
    row_height = _tree_row_height(builder, tb_ttk_style)

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
