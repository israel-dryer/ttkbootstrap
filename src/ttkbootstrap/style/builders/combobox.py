"""TTK combobox style recipes."""

import tkinter as tk

from ttkbootstrap.constants import *
from ttkbootstrap.style import StyleBuilderTTK
from ttkbootstrap.style.layout import El, image_element, layout
from ttkbootstrap.style.builders.registry import register_builder


@register_builder("default", "combobox")
def build_combobox_style(builder: StyleBuilderTTK, colorname=DEFAULT):
    """Create a style for the ttk.Combobox widget.

    Parameters:

        builder (StyleBuilderTTK):
            The style builder
        colorname (str):
            The color label to use as the primary widget color.
    """
    ttk_class = "TCombobox"

    on_disabled = builder.disabled("text", builder.colors.inputbg)
    border = builder.colors.border
    # readonly fields read like normal fields (no greyed box).
    readonly = builder.colors.inputbg

    if any([colorname == DEFAULT, colorname == ""]):
        ttk_style = ttk_class
        element = f"{ttk_style.replace('TC', 'C')}"
        focus_ring = builder.colors.primary
    else:
        ttk_style = f"{colorname}.{ttk_class}"
        element = f"{ttk_style.replace('TC', 'C')}"
        focus_ring = builder.colors.get(colorname)

    # A `chevron-down` glyph (the open V) rather than the solid `caret-down-fill`
    # triangle used elsewhere -- reads lighter in a combobox. Custom asset since
    # the native ttk arrow doesn't work with the Tcl/Tk bundled in python 3.13.
    a = builder.assets
    chevron_size = [12, 12]
    # One fixed color in every state (no focus/hover/pressed/disabled recolor) so
    # the chevron reads as a steady glyph rather than reacting to field state.
    down_arrow_image = a.icon("chevron-down", chevron_size, builder.colors.inputfg)
    image_element(
        builder.style, f"{element}.downarrow", default=down_arrow_image)
    #  builder.style.element_create(f"{element}.downarrow", "from", TTK_DEFAULT)  # doesn't work in python 3.13
    builder.style.element_create(f"{element}.padding", "from", TTK_CLAM)
    builder.style.element_create(f"{element}.textarea", "from", TTK_CLAM)

    builder.configure(
        ttk_style,
        bordercolor=border,
        darkcolor=builder.colors.inputbg,
        lightcolor=builder.colors.inputbg,
        foreground=builder.colors.inputfg,
        fieldbackground=builder.colors.inputbg,
        background=builder.colors.inputbg,
        insertcolor=builder.colors.inputfg,
        relief=tk.FLAT,
        # (left, top, right, bottom): extra right inset holds the chevron a bit
        # further off the border than the text is on the left.
        padding=builder.scale_size((5, 6, 7, 4)),
    )
    builder.style.map(
        ttk_style,
        background=[("readonly", readonly)],
        fieldbackground=[("readonly", readonly)],
        foreground=[("disabled", on_disabled)],
        bordercolor=[
            ("invalid", builder.colors.danger),
            ("focus !disabled", focus_ring),
        ],
        lightcolor=[
            ("focus invalid", builder.colors.danger),
            ("focus !disabled", focus_ring),
            ("readonly", readonly),
        ],
        darkcolor=[
            ("focus invalid", builder.colors.danger),
            ("focus !disabled", focus_ring),
            ("readonly", readonly),
        ],
    )
    # Lay the chevron out like the Menubutton indicator: inside the padded
    # region, packed right and vertically centered (sticky="") so the widget
    # padding holds it off the border instead of it being pinned bottom-right.
    layout(builder.style, ttk_style,
           El("combo.Spinbox.field", side=tk.TOP, sticky=tk.EW, children=[
               El("Combobox.padding", expand="1", sticky=tk.NSEW, children=[
                   El("Combobox.downarrow", side=tk.RIGHT, sticky=""),
                   El("Combobox.textarea", sticky=tk.NSEW)])]))
    builder.register_ttkstyle(ttk_style)
    try:
        # the popdown uses the thin scrollbar (a scroll indicator in a small space)
        builder.build_style("thin", "scrollbar", DEFAULT, required=True)
    except Exception:
        # style already created
        pass


def update_combobox_popdown_style(builder: StyleBuilderTTK, widget):
    """Update the legacy ttk.Combobox elements. This method is
    called every time the theme is changed in order to ensure
    that the legacy tkinter components embedded in this ttk widget
    are styled appropriate to the current theme.

    The ttk.Combobox contains several elements that are not styled
    using the ttk theme engine. This includes the **popdownwindow**
    and the **scrollbar**. Both of these widgets are configured
    manually using calls to tcl/tk.

    Parameters:

        builder (StyleBuilderTTK):
            The style builder
        widget (ttk.Combobox):
            The combobox element to be updated.
    """
    border = builder.colors.border

    tk_settings = []
    tk_settings.extend(["-borderwidth", 2])
    tk_settings.extend(["-highlightthickness", 1])
    tk_settings.extend(["-highlightcolor", border])
    tk_settings.extend(["-background", builder.colors.inputbg])
    tk_settings.extend(["-foreground", builder.colors.inputfg])
    tk_settings.extend(["-selectbackground", builder.colors.selectbg])
    tk_settings.extend(["-selectforeground", builder.colors.selectfg])

    # set popdown style
    popdown = widget.tk.eval(f"ttk::combobox::PopdownWindow {widget}")
    widget.tk.call(f"{popdown}.f.l", "configure", *tk_settings)

    # set scrollbar style -- the thin bar suits the narrow popdown
    sb_style = "Thin.Vertical.TScrollbar"
    if not builder.style.style_exists_in_theme(sb_style):
        builder.build_style("thin", "scrollbar", DEFAULT, required=True)
    widget.tk.call(f"{popdown}.f.sb", "configure", "-style", sb_style)
