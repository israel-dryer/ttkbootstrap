"""Checkbutton widget style builders.

This module contains style builders for ttk.Checkbutton widgets and variants.
"""

from __future__ import annotations

from ttkbootstrap.style.bootstyle_builder_ttk import BootstyleBuilderTTk
from ttkbootstrap.style.element import Element, ElementImage
from ttkbootstrap.style.utility import create_transparent_image, recolor_element_image


@BootstyleBuilderTTk.register_builder('default', 'TCheckbutton')
def build_checkbutton_style(b: BootstyleBuilderTTk, ttk_style: str, accent: str = 'primary', **options):
    accent_token = accent or 'primary'
    surface_token = options.get('surface', 'content')

    background = b.color(surface_token)
    background_hover = b.active(background)
    foreground = b.on_color(background)
    foreground_disabled = b.disabled('text', background)

    normal = b.color(accent_token)
    pressed = b.pressed(normal)
    hovered = b.active(normal)
    border = b.border(background)
    focus = hovered
    focus_ring = b.focus_ring(normal, background)
    disabled = b.disabled()

    normal_checked_img = recolor_element_image('checkbox_checked', background, normal, background)
    normal_unchecked_img = recolor_element_image('checkbox_unchecked', background, border, background)
    normal_indeterminate_img = recolor_element_image('checkbox_indeterminate', background, normal, background)

    hovered_checked_img = recolor_element_image('checkbox_checked', background, hovered, background)
    hovered_unchecked_img = recolor_element_image('checkbox_unchecked', background_hover, border, background)
    hovered_indeterminate_img = recolor_element_image('checkbox_indeterminate', background, hovered, background)

    pressed_checked_img = recolor_element_image('checkbox_checked', background, pressed, background)
    pressed_unchecked_img = recolor_element_image('checkbox_unchecked', background_hover, pressed, background)
    pressed_indeterminate_img = recolor_element_image('checkbox_indeterminate', background, pressed, background)

    focus_checked_img = recolor_element_image('checkbox_checked', background, focus, focus_ring)
    focus_unchecked_img = recolor_element_image('checkbox_unchecked', background_hover, focus, focus_ring)
    focus_indeterminate_img = recolor_element_image('checkbox_indeterminate', background, focus, focus_ring)

    disabled_checked_img = recolor_element_image('checkbox_checked', disabled, foreground_disabled, background)
    disabled_unchecked_img = recolor_element_image(
        'checkbox_unchecked', foreground_disabled, foreground_disabled, background)
    disabled_indeterminate_img = recolor_element_image('checkbox_indeterminate', disabled, foreground_disabled, background)

    spacer_img = create_transparent_image(6, 1)
    b.create_style_element_image(ElementImage(f'{ttk_style}.spacer', spacer_img, sticky="ew"))

    b.create_style_element_image(
        ElementImage(f'{ttk_style}.indicator', normal_unchecked_img.image, sticky="ns").state_specs(
            [
                # Disabled states
                ('disabled alternate !selected', disabled_indeterminate_img.image),
                ('disabled selected', disabled_checked_img.image),
                ('disabled !selected !alternate', disabled_unchecked_img.image),

                # Focused states
                ('focus alternate !selected', focus_indeterminate_img.image),
                ('focus selected', focus_checked_img.image),
                ('focus !selected !alternate', focus_unchecked_img.image),

                # Pressed states
                ('pressed alternate !selected', pressed_indeterminate_img.image),
                ('pressed selected', pressed_checked_img.image),
                ('pressed !selected !alternate', pressed_unchecked_img.image),

                # Hover states
                ('hover alternate !selected', hovered_indeterminate_img.image),
                ('hover selected', hovered_checked_img.image),
                ('hover !selected !alternate', hovered_unchecked_img.image),

                # Normal base states
                ('alternate !selected', normal_indeterminate_img.image),
                ('selected', normal_checked_img.image),
                ('!selected !alternate', normal_unchecked_img.image),
            ]
        ))

    b.create_style_layout(
        ttk_style, Element('Checkbutton.padding', sticky="nsew").children(
            [
                Element(f'{ttk_style}.indicator', side="left", sticky=""),
                Element(f'{ttk_style}.spacer', side="left"),
                Element('Checkbutton.label', side="left", sticky="nsew")
            ])
    )

    b.configure_style(ttk_style, background=background, foreground=foreground, font="body")
    b.map_style(ttk_style, background=[], foreground=[('disabled', foreground_disabled), ('', foreground)])
