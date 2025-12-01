from __future__ import annotations

from ttkbootstrap.style.bootstyle_builder_ttk import BootstyleBuilderTTk
from ttkbootstrap.style.element import Element, ElementImage
from ttkbootstrap.style.utility import recolor_image


@BootstyleBuilderTTk.register_builder('default', 'TFrame')
def build_frame(b: BootstyleBuilderTTk, ttk_style: str, color: str = None, **options):
    surface_token = options.get('surface_color') or 'background'
    show_border = options.get('show_border', False)
    surface = b.color(surface_token)
    border = b.border(surface)

    # border assets and styles
    if show_border:
        border_img = recolor_image('border', surface, border, surface, surface)
        b.create_style_element_image(
            ElementImage(
                f'{ttk_style}.border',
                border_img,
                border=b.scale(6),
                sticky="nsew")
        )
        b.create_style_layout(ttk_style, Element(f'{ttk_style}.border', sticky="nsew"))

    b.configure_style(ttk_style, background=surface)
