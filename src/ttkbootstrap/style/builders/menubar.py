"""Menubutton widget style builders.

This module contains style builders for ttk.Menubutton widgets and variants.
"""

from __future__ import annotations

from ttkbootstrap.style.bootstyle_builder_ttk import BootstyleBuilderTTk
from ttkbootstrap.style.element import Element, ElementImage
from ttkbootstrap.style.utility import recolor_image

V_PAD = 6
H_PAD = 8


@BootstyleBuilderTTk.register_builder('menubar-item', 'TMenubutton')
@BootstyleBuilderTTk.register_builder('menubar-item', 'TButton')
def build_menubar_item(b: BootstyleBuilderTTk, ttk_style: str, color: str = None, **options):
    surface_token = options.get('surface', 'chrome')

    surface = b.color(surface_token)
    active = b.active(surface)
    pressed = b.pressed(surface)

    foreground_normal = b.on_color(surface)
    foreground_disabled = b.disabled('text', surface)

    normal_img = recolor_image('badge-default', surface)
    pressed_img = recolor_image('badge-default', pressed)
    active_img = recolor_image('badge-default', active)

    border = b.scale(6)
    padding = b.scale((H_PAD, V_PAD))

    # button element
    b.create_style_element_image(
        ElementImage(f'{ttk_style}.Button.border', normal_img, sticky="nsew", border=border,
                     padding=padding).state_specs([
            ('background focus pressed', pressed_img),
            ('background focus hover', active_img),
            ('background focus', pressed_img),
            ('pressed', pressed_img),
            ('hover', active_img)
        ]))

    b.create_style_layout(
        ttk_style, Element(f"{ttk_style}.Button.border", sticky="nsew").children([
            Element("Button.padding", sticky="nsew").children([
                Element("Button.label", sticky="nsew")
            ])
        ]))

    b.configure_style(ttk_style, font="caption", background=surface, foreground=foreground_normal)

    state_spec = dict(
        foreground=[
            ('disabled', foreground_disabled),
            ('background focus', foreground_normal),
            ('', foreground_normal)
        ]
    )

    state_spec = _apply_icon_mapping(b, options, state_spec)
    b.map_style(ttk_style, **state_spec)


def _apply_icon_mapping(b: BootstyleBuilderTTk, options: dict, state_spec: dict) -> dict:
    """Apply icon mapping if an icon is provided in options."""
    icon = options.get('icon')
    if icon is None:
        return state_spec

    icon = b.normalize_icon_spec(icon, b.scale(20))
    state_spec['image'] = b.map_stateful_icons(icon, state_spec['foreground'])
    return state_spec
