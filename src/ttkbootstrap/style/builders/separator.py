"""Separator widget style builders.

This module contains style builders for ttk.Separator widgets and variants.
"""

from __future__ import annotations



from ttkbootstrap.style.bootstyle_builder_ttk import BootstyleBuilderTTk
from ttkbootstrap.core.images import Image
from ttkbootstrap.style.element import ElementImage, Element


@BootstyleBuilderTTk.register_builder('default', 'TSeparator')
def build_separator_style(b: BootstyleBuilderTTk, ttk_style: str, accent: str = None, **options):
    accent_token = accent or 'border'
    surface_token = options.get('surface', 'content')
    orient = options.get('orient', 'horizontal')
    thickness = options.get('thickness', 1)

    width, height = (40, thickness)
    if orient == 'vertical':
        width, height = (thickness, 40)

    surface = b.color(surface_token)
    if accent_token == 'border':
        accent_color = b.border(surface)
    else:
        accent_color = b.color(accent_token)

    img = Image.box(width, height, accent_color)
    sticky = "ew" if orient == "horizontal" else "ns"
    b.create_style_element_image(ElementImage(f"{ttk_style}.Separator", img, border=0, sticky=sticky))
    b.create_style_layout(ttk_style, Element(f"{ttk_style}.Separator", sticky=sticky))
    b.configure_style(ttk_style, background=surface)
