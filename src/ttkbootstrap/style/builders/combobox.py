"""TTK combobox style recipes."""

import tkinter as tk

from ttkbootstrap.constants import *
from ttkbootstrap.style import StyleBuilderTTK
from ttkbootstrap.style.layout import El, image_element, layout
from ttkbootstrap.style.builders.registry import register_builder
from ttkbootstrap.style.builders.utils import simple_arrow_assets


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
    readonly = builder.colors.light if builder.is_light_theme else builder.colors.selectbg

    if any([colorname == DEFAULT, colorname == ""]):
        ttk_style = ttk_class
        element = f"{ttk_style.replace('TC', 'C')}"
        focus_ring = builder.colors.primary
    else:
        ttk_style = f"{colorname}.{ttk_class}"
        element = f"{ttk_style.replace('TC', 'C')}"
        focus_ring = builder.colors.get(colorname)

    # Create custom arrow assets since the default ones don't work with Tcl/Tk bundled in python 3.13
    arrow_images = simple_arrow_assets(builder,
        builder.colors.inputfg,
        on_disabled,
        focus_ring,
    )
    down_arrow_image = arrow_images[0][1]
    down_arrow_disabled_image = arrow_images[1][1]
    down_arrow_focused_image = arrow_images[2][1]
    image_element(
        builder.style, f"{element}.downarrow", default=down_arrow_image,
        states={"disabled": down_arrow_disabled_image,
                "pressed !disabled": down_arrow_focused_image,
                "focus !disabled": down_arrow_focused_image,
                "hover !disabled": down_arrow_focused_image},
        # right padding so the caret isn't flush against the border
        padding=(0, 0, builder.scale_size(6), 0))
    #  builder.style.element_create(f"{element}.downarrow", "from", TTK_DEFAULT)  # doesn't work in python 3.13
    builder.style.element_create(f"{element}.padding", "from", TTK_CLAM)
    builder.style.element_create(f"{element}.textarea", "from", TTK_CLAM)

    if all([colorname, colorname != DEFAULT]):
        border = focus_ring

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
        padding=builder.scale_size(5),
    )
    builder.style.map(
        ttk_style,
        background=[("readonly", readonly)],
        fieldbackground=[("readonly", readonly)],
        foreground=[("disabled", on_disabled)],
        bordercolor=[
            ("invalid", builder.colors.danger),
            ("focus !disabled", focus_ring),
            ("hover !disabled", focus_ring),
        ],
        lightcolor=[
            ("focus invalid", builder.colors.danger),
            ("focus !disabled", focus_ring),
            ("pressed !disabled", focus_ring),
            ("readonly", readonly),
        ],
        darkcolor=[
            ("focus invalid", builder.colors.danger),
            ("focus !disabled", focus_ring),
            ("pressed !disabled", focus_ring),
            ("readonly", readonly),
        ],
    )
    layout(builder.style, ttk_style,
           El("combo.Spinbox.field", side=tk.TOP, sticky=tk.EW, children=[
               El("Combobox.downarrow", side=tk.RIGHT, sticky=tk.S),
               El("Combobox.padding", expand="1", sticky=tk.NSEW, children=[
                   El("Combobox.textarea", sticky=tk.NSEW)])]))
    builder.register_ttkstyle(ttk_style)
    try:
        builder.build_style("default", "scrollbar", DEFAULT, required=True)
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

    # set scrollbar style
    sb_style = "TCombobox.Vertical.TScrollbar"
    widget.tk.call(f"{popdown}.f.sb", "configure", "-style", sb_style)
