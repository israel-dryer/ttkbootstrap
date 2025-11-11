"""Checkbutton widget style builders.

This module contains style builders for ttk.Checkbutton widgets and variants.
"""

from __future__ import annotations

from ttkbootstrap.style.bootstyle_builder_ttk import BootstyleBuilderBuilderTTk
from ttkbootstrap.style.element import Element, ElementImage
from ttkbootstrap.style.utility import create_transparent_image, recolor_image


@BootstyleBuilderBuilderTTk.register_builder('default', 'TCheckbutton')
def build_checkbutton_style(b: BootstyleBuilderBuilderTTk, ttk_style: str, color: str = 'primary', **options):
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

    normal_checked_img = recolor_image('checkbox-checked', foreground_active, normal, background)
    normal_unchecked_img = recolor_image('checkbox-unchecked', background, border, background)
    normal_indeterminate_img = recolor_image('checkbox-indeterminate', foreground_active, normal, background)

    hovered_checked_img = recolor_image('checkbox-checked', foreground_active, hovered, background)
    hovered_unchecked_img = recolor_image('checkbox-unchecked', background_hover, border, background)
    hovered_indeterminate_img = recolor_image('checkbox-indeterminate', foreground_active, hovered, background)

    pressed_checked_img = recolor_image('checkbox-checked', foreground_active, pressed, background)
    pressed_unchecked_img = recolor_image('checkbox-unchecked', background_hover, pressed, background)
    pressed_indeterminate_img = recolor_image('checkbox-indeterminate', foreground_active, pressed, background)

    focus_checked_img = recolor_image('checkbox-checked', foreground_active, focus, focus_ring)
    focus_unchecked_img = recolor_image('checkbox-unchecked', background_hover, focus, focus_ring)
    focus_indeterminate_img = recolor_image('checkbox-indeterminate', foreground_active, focus, focus_ring)

    disabled_checked_img = recolor_image('checkbox-checked', disabled, foreground_disabled, background)
    disabled_unchecked_img = recolor_image(
        'checkbox-unchecked', foreground_disabled, foreground_disabled, background)
    disabled_indeterminate_img = recolor_image('checkbox-indeterminate', disabled, foreground_disabled, background)

    spacer_img = create_transparent_image(8, 1)
    b.create_style_element_image(ElementImage(f'{ttk_style}.spacer', spacer_img, sticky="ew"))

    b.create_style_element_image(
        ElementImage(f'{ttk_style}.indicator', normal_unchecked_img, sticky="ns", padding=3).state_specs(
            [
                # Disabled states
                ('disabled alternate !selected', disabled_indeterminate_img),
                ('disabled selected', disabled_checked_img),
                ('disabled !selected !alternate', disabled_unchecked_img),

                # Focused states
                ('focus alternate !selected', focus_indeterminate_img),
                ('focus selected', focus_checked_img),
                ('focus !selected !alternate', focus_unchecked_img),

                # Pressed states
                ('pressed alternate !selected', pressed_indeterminate_img),
                ('pressed selected', pressed_checked_img),
                ('pressed !selected !alternate', pressed_unchecked_img),

                # Hover states
                ('hover alternate !selected', hovered_indeterminate_img),
                ('hover selected', hovered_checked_img),
                ('hover !selected !alternate', hovered_unchecked_img),

                # Normal base states
                ('alternate !selected', normal_indeterminate_img),
                ('selected', normal_checked_img),
                ('!selected !alternate', normal_unchecked_img),
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

    b.configure_style(ttk_style, background=background, foreground=foreground)
    b.map_style(ttk_style, background=[], foreground=[])
