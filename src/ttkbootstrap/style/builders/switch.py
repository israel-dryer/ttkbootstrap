"""Switch widget style builders.

This module contains style builders for switch (toggle) variants of ttk.Checkbutton.
"""

from __future__ import annotations

from ttkbootstrap.style.bootstyle_builder_ttk import BootstyleBuilderTTk
from ttkbootstrap.style.element import Element, ElementImage
from ttkbootstrap.style.utility import create_transparent_image, recolor_element_image


@BootstyleBuilderTTk.register_builder('switch', 'TCheckbutton')
def build_switch_style(b: BootstyleBuilderTTk, ttk_style: str, accent: str = 'primary', **options):
    accent_token = accent or 'primary'
    surface_token = options.get('surface', 'content')

    background = b.color(surface_token)
    foreground = b.on_color(background)
    foreground_disabled = b.disabled('text', background)

    normal = b.color(accent_token)
    hovered = b.active(normal)
    border = b.border(background)
    focus = hovered
    focus_ring = b.focus_ring(normal, background)

    normal_checked_img = recolor_element_image('switch_on', background, normal, background)
    normal_unchecked_img = recolor_element_image('switch_off', background, border, background)

    focus_checked_img = recolor_element_image('switch_on', background, focus, focus_ring)
    focus_unchecked_img = recolor_element_image('switch_off', background, border, focus_ring)

    disabled_checked_img = recolor_element_image('switch_on', background, foreground_disabled, background)
    disabled_unchecked_img = recolor_element_image('switch_off', foreground_disabled, foreground_disabled, background)

    spacer_img = create_transparent_image(6, 1)
    b.create_style_element_image(ElementImage(f'{ttk_style}.spacer', spacer_img, sticky="ew"))

    b.create_style_element_image(
        ElementImage(f'{ttk_style}.indicator', normal_unchecked_img.image, sticky="ns").state_specs(
            [
                # Disabled states
                ('disabled selected', disabled_checked_img.image),
                ('disabled !selected !alternate', disabled_unchecked_img.image),

                # Focused states
                ('focus selected', focus_checked_img.image),
                ('focus !selected !alternate', focus_unchecked_img.image),

                # Normal base states
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
