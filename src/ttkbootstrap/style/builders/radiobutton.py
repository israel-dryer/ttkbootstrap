"""TTK radiobutton style recipes."""

from ttkbootstrap.constants import *
from ttkbootstrap.style import StyleBuilderTTK
from ttkbootstrap.style.layout import El, StyleName, image_element, layout, state_map
from ttkbootstrap.style.builders.registry import register_builder
from ttkbootstrap.style.builders.utils import indicator_spacer


@register_builder("default", "radiobutton")
def build_radiobutton_style(builder: StyleBuilderTTK, colorname=DEFAULT):
    """Create a style for the ttk.Radiobutton widget.

    Parameters:

        builder (StyleBuilderTTK):
            The style builder
        colorname (str):
            The color label used to style the widget.
    """
    sn = StyleName("TRadiobutton", colorname)
    fg = builder.colors.fg
    disabled = builder.disabled("text")
    fg_muted = builder.mute(fg)

    # Resolve the "on" accent; LIGHT/DARK on their own background need a
    # contrasting indicator so the knockout interior stays readable
    # (visual-check item: verify LIGHT-on-light reads on the human spot-check).
    if sn.colorname == LIGHT and builder.is_light_theme:
        accent = builder.colors.dark
    elif sn.colorname == DARK and not builder.is_light_theme:
        accent = builder.colors.light
    else:
        accent = builder.colors.get(sn.colorname)

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

    a = builder.assets
    selected = a.recolor("radiobutton", white=accent, black=accent)
    unselected = a.recolor("radiobutton", white=builder.colors.bg, black=fg_muted)
    disabled_selected = a.recolor("radiobutton", white=disabled, black=disabled)
    disabled_unselected = a.recolor("radiobutton", white=builder.colors.bg, black=disabled)
    image_element(
        builder.style, f"{sn.ttk_style}.indicator", default=selected.image,
        states={
            "disabled selected": disabled_selected.image,
            "disabled": disabled_unselected.image,
            "!selected": unselected.image,
        },
        border=selected.meta.border, padding=selected.meta.padding, sticky=W)
    spacer_name = f"{sn.ttk_style}.spacer"
    image_element(builder.style, spacer_name, default=indicator_spacer(builder), sticky=EW)
    layout(
        builder.style, sn.ttk_style,
        El("Radiobutton.padding", sticky=NSEW, children=[
            El(f"{sn.ttk_style}.indicator", side=LEFT, sticky=""),
            El(spacer_name, side=LEFT),
            El("Radiobutton.focus", side=LEFT, sticky="", children=[
                El("Radiobutton.label", sticky=NSEW)])]))

    builder.register_ttkstyle(sn.ttk_style)
