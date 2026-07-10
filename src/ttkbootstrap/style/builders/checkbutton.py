"""TTK checkbutton style recipes."""

from ttkbootstrap.constants import *
from ttkbootstrap.style import StyleBuilderTTK
from ttkbootstrap.style.layout import El, StyleName, image_element, layout, state_map
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
    sn = StyleName("TCheckbutton", colorname, surface=builder._surface)
    # Label/focus text reads against the surface (2.0 surface-color); the
    # indicator glyph is self-contained (its paper is `on_accent`, not the bg).
    fg = builder.on_surface_fg()

    disabled = builder.disabled("text")
    fg_muted = builder.mute(fg)

    accent = builder.colors.get(colorname or 'primary')
    on_accent = builder.on_color(accent)

    # A 1px keyboard-focus ring around the label (drawn by the `.focus` element
    # in the layout below), matching the button family so focus is visible here
    # too. It hugs the label and does not change the indicator-driven height.
    builder.configure(
        sn.ttk_style, foreground=fg,
        focuscolor=fg, focusthickness=builder.scale_size(1),
    )
    state_map(
        builder.style, sn.ttk_style,
        foreground={"disabled": disabled},
        focuscolor={"disabled": disabled},
    )

    # Create style assets
    a = builder.assets
    checked = a.recolor("checkbox_checked", white=on_accent, black=accent)
    unchecked = a.recolor("checkbox_unchecked", white=on_accent, black=fg_muted)
    indeterminate = a.recolor("checkbox_indeterminate", white=on_accent, black=accent)
    disabled_checked = a.recolor("checkbox_checked", white=on_accent, black=disabled)
    disabled_unchecked = a.recolor("checkbox_unchecked", white=on_accent, black=disabled)
    disabled_indeterminate = a.recolor("checkbox_indeterminate", white=on_accent, black=disabled)

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
