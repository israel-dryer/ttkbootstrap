from __future__ import annotations

from ttkbootstrap.style.bootstyle_builder_ttk import BootstyleBuilderTTk
from ttkbootstrap.style.element import Element, ElementImage
from ttkbootstrap.style.utility import create_rounded_border_image


@BootstyleBuilderTTk.register_builder('default', 'TFrame')
def build_frame(b: BootstyleBuilderTTk, ttk_style: str, accent: str = None, **options):
    surface_token = options.get('surface') or 'background'
    show_border = options.get('show_border', False)
    surface = b.color(surface_token)
    stroke = b.border(surface)
    stroke_thickness = options.get('stroke_thickness', 1)
    stroke_radius = options.get('stroke_radius', 4)


    # border assets and styles
    if show_border:
        border_img = create_rounded_border_image(
            size=100,
            radius=stroke_radius,
            fill=surface,
            stroke=stroke,
            thickness=stroke_thickness
        )

        # border_img = recolor_image('border', surface, stroke, surface, surface)
        b.create_style_element_image(
            ElementImage(
                f'{ttk_style}.border',
                border_img,
                border=int(stroke_radius * 4),
                padding=int(stroke_radius * 4),
                sticky="nsew")
        )
        b.create_style_layout(ttk_style, Element(f'{ttk_style}.border', sticky="nsew"))

    b.configure_style(ttk_style, background=surface)
