"""Separator widget style builders.

This module contains style builders for ttk.Separator widgets and variants.
"""

from __future__ import annotations

from ttkbootstrap.style.bootstyle_builder_ttk import BootstyleBuilderTTk
from ttkbootstrap.style.element import Element, ElementImage
from ttkbootstrap.style.utility import recolor_image


@BootstyleBuilderTTk.register_builder('default', 'TSeparator')
def build_separator_style(b: BootstyleBuilderTTk, ttk_style: str, accent: str = None, **options):
    accent_token = accent or 'border'
    surface_token = options.get('surface', 'background')
    orient = options.get('orient', 'horizontal')

    surface = b.color(surface_token)
    if accent_token == 'border':
        accent_color = b.border(surface)
    else:
        accent_color = b.color(accent_token)

    img = recolor_image(f"separator-{orient}", accent_color)
    sticky = "ew" if orient == "horizontal" else "ns"

    b.create_style_element_image(ElementImage(f"{ttk_style}.Separator", img, border=0, sticky=sticky))
    b.create_style_layout(ttk_style, Element(f"{ttk_style}.Separator", sticky=sticky))
    b.configure_style(ttk_style, background=surface)
