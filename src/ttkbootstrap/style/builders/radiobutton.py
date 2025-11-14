"""Radio Button widget style builders.

This module contains style builders for ttk.Radiobutton widgets and variants.
"""

from __future__ import annotations

from ttkbootstrap.style.bootstyle_builder_ttk import BootstyleBuilderTTk
from ttkbootstrap.style.element import Element, ElementImage
from ttkbootstrap.style.utility import create_transparent_image, recolor_image


@BootstyleBuilderTTk.register_builder('default', 'TRadiobutton')
def build_radiobutton_style(b: BootstyleBuilderTTk, ttk_style: str, color: str = 'primary', **options):
    accent_token = color or 'primary'
    surface_token = options.get('surface_color', 'background')

    background = b.color(surface_token)
    background_hover = b.hover(background)
    foreground = b.on_color(background)
    foreground_disabled = b.disabled('text')

    normal = b.color(accent_token)
    foreground_active = b.on_color(normal)
    pressed = b.active(normal)
    hovered = b.hover(normal)
    border = b.border(background)
    focus = hovered
    focus_ring = b.focus_ring(normal, background)
    disabled = b.disabled()

    normal_checked_img = recolor_image('radio-selected', foreground_active, normal, background)
    normal_unchecked_img = recolor_image('radio-unselected', background, border, background)

    hovered_checked_img = recolor_image('radio-selected', foreground_active, hovered, background)
    hovered_unchecked_img = recolor_image('radio-unselected', background_hover, border, background)

    pressed_checked_img = recolor_image('radio-selected', foreground_active, pressed, background)
    pressed_unchecked_img = recolor_image('radio-unselected', background_hover, pressed, background)

    focus_checked_img = recolor_image('radio-selected', foreground_active, focus, focus_ring)
    focus_unchecked_img = recolor_image('radio-unselected', background_hover, focus, focus_ring)

    disabled_checked_img = recolor_image('radio-selected', disabled, foreground_disabled, background)
    disabled_unchecked_img = recolor_image('radio-unselected', foreground_disabled, foreground_disabled, background)

    spacer_img = create_transparent_image(8, 1)
    b.create_style_element_image(ElementImage(f'{ttk_style}.spacer', spacer_img, sticky="ew"))

    b.create_style_element_image(
        ElementImage(f'{ttk_style}.indicator', normal_unchecked_img, sticky="ns", padding=3).state_specs(
            [
                # Disabled states
                ('disabled selected', disabled_checked_img),
                ('disabled !selected !alternate', disabled_unchecked_img),

                # Focused states
                ('focus selected', focus_checked_img),
                ('focus !selected !alternate', focus_unchecked_img),

                # Pressed states
                ('pressed selected', pressed_checked_img),
                ('pressed !selected !alternate', pressed_unchecked_img),

                # Hover states
                ('hover selected', hovered_checked_img),
                ('hover !selected !alternate', hovered_unchecked_img),

                # Normal base states
                ('selected', normal_checked_img),
                ('!selected !alternate', normal_unchecked_img),
            ]
        ))

    b.create_style_layout(
        ttk_style, Element('Radiobutton.padding', sticky="nsew").children(
            [
                Element(f'{ttk_style}.indicator', side="left", sticky=""),
                Element(f'{ttk_style}.spacer', side="left"),
                Element('Radiobutton.label', side="left", sticky="nsew")
            ])
    )

    b.configure_style(ttk_style, background=background, foreground=foreground)
    b.map_style(ttk_style, background=[], foreground=[])
