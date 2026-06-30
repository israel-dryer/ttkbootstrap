"""TTK checkbutton style recipes."""

from ttkbootstrap.constants import *
from ttkbootstrap.style import StyleBuilderTTK
from ttkbootstrap.style.layout import El, StyleName, image_element, layout, state_map
from ttkbootstrap.style.theme import Colors
from ttkbootstrap.style.builders.registry import register_builder
from ttkbootstrap.style.builders.utils import indicator_spacer


@register_builder("default", "checkbutton")
def build_checkbutton_style(builder: StyleBuilderTTK, colorname=DEFAULT):
    """Create a standard style for the ttk.Checkbutton widget.

    Parameters:

        builder (StyleBuilderTTK):
            The style builder
        colorname (str):
            The color label used to style the widget.
    """
    sn = StyleName("TCheckbutton", colorname)
    fg = builder.colors.fg
    disabled = Colors.make_transparent(0.3, fg, builder.colors.bg)
    fg_muted = Colors.make_transparent(0.4, fg, builder.colors.bg)

    # Resolve the "on" accent; LIGHT/DARK on their own background need a
    # contrasting indicator so the knockout interior stays readable
    # (visual-check item: verify LIGHT-on-light reads on the human spot-check).
    if sn.colorname == LIGHT and builder.is_light_theme:
        accent = builder.colors.dark
    elif sn.colorname == DARK and not builder.is_light_theme:
        accent = builder.colors.light
    else:
        accent = builder.colors.get(sn.colorname)

    # Foreground map FIRST -- color-less icon specs resolve against it.
    builder.configure(sn.ttk_style, foreground=fg)
    state_map(builder.style, sn.ttk_style, foreground={"disabled": disabled})

    # Create style assets
    a = builder.assets
    checked = a.recolor("checkbox_checked", white=builder.colors.bg, black=accent)
    unchecked = a.recolor("checkbox_unchecked", white=builder.colors.bg, black=fg_muted)
    indeterminate = a.recolor("checkbox_indeterminate", white=builder.colors.bg, black=accent)
    disabled_checked = a.recolor("checkbox_checked", white=builder.colors.bg, black=disabled)
    disabled_unchecked = a.recolor("checkbox_unchecked", white=builder.colors.bg, black=disabled)
    disabled_indeterminate = a.recolor("checkbox_indeterminate", white=builder.colors.bg, black=disabled)

    # Layout elements
    image_element(builder.style, f"{sn.ttk_style}.indicator", default=checked.image,
                  states={
            "disabled selected": disabled_checked.image,
            "disabled alternate": disabled_indeterminate.image,
            "disabled": disabled_unchecked.image,
            "alternate": indeterminate.image,
            "!selected": unchecked.image,
        },
                  border=checked.meta.border, padding=checked.meta.padding, sticky=W)

    spacer_name = f"{sn.ttk_style}.spacer"

    image_element(builder.style, spacer_name, default=indicator_spacer(builder), sticky=EW)

    layout(builder.style, sn.ttk_style, El("Checkbutton.padding", sticky=NSEW, children=[
        El(f"{sn.ttk_style}.indicator", side=LEFT, sticky=""),
        El(spacer_name, side=LEFT),
        El("Checkbutton.focus", side=LEFT, sticky="", children=[
            El("Checkbutton.label", sticky=NSEW)])]))

    # register ttkstyle
    builder.register_ttkstyle(sn.ttk_style)
