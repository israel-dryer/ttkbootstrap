"""Labelframe widget style builders.

This module contains style builders for ttk.Labelframe widget and variants.

The Labelframe color is different than the normal frame in that the background color of the
labelframe is inherited only unless overridden explicitly by the surface option. The
bootstyle color is only relevant for the border color of the labelframe.
"""

from __future__ import annotations

from ttkbootstrap.style.bootstyle_builder_ttk import BootstyleBuilderTTk
from ttkbootstrap.style.element import Element, ElementImage
from ttkbootstrap.style.utility import recolor_image


@BootstyleBuilderTTk.register_builder('default', 'TLabelframe')
def build_labelframe_style(b: BootstyleBuilderTTk, ttk_style: str, accent: str = None, **options):
    surface_token = options.get('surface') or 'background'
    show_border = options.get('show_border', True)
    surface = b.color(surface_token)

    border = b.border(surface)
    foreground = b.on_color(surface)

    # border assets and styles
    if show_border:
        border_img = recolor_image('border', surface, border, surface, surface)
    else:
        border_img = recolor_image('border', surface, surface, surface, surface)

    b.create_style_element_image(
        ElementImage(
            f'{ttk_style}.border',
            border_img,
            border=b.scale(6),
            sticky="nsew")
    )
    b.create_style_layout(ttk_style, Element(f'{ttk_style}.border', sticky="nsew"))
    b.configure_style(f'{ttk_style}.Label', background=surface, foreground=foreground, font="label")
    b.configure_style(ttk_style, background=surface)
