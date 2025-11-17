"""Sizegrip widget style builders.

This module contains style builders for ttk.Sizegrip and variants.
"""

from __future__ import annotations

from ttkbootstrap.style.bootstyle_builder_ttk import BootstyleBuilderTTk
from ttkbootstrap.style.element import Element, ElementImage
from ttkbootstrap.style.utility import recolor_image


@BootstyleBuilderTTk.register_builder('default', 'TSizegrip')
def build_sizegrip_style(b: BootstyleBuilderTTk, ttk_style: str, color: str = None, **options):
    accent_token = color or 'border'
    surface_token = options.get('surface_color', 'background')

    accent = b.color(accent_token)
    surface = b.color(surface_token)

    img = recolor_image('sizegrip', surface, accent, scale=0.25)

    b.create_style_element_image(ElementImage(f'{ttk_style}.Sizegrip.sizegrip', img))

    b.create_style_layout(
        ttk_style,
        Element(f'{ttk_style}.Sizegrip.sizegrip', side='bottom', sticky='se'),
    )
    b.configure_style(ttk_style, background=surface)
