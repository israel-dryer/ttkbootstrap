from __future__ import annotations

from ttkbootstrap.style.bootstyle_builder_ttk import BootstyleBuilderTTk
from ttkbootstrap.style.element import Element, ElementImage
from ttkbootstrap.style.utility import create_rounded_border_image


@BootstyleBuilderTTk.register_builder('default', 'TFrame')
def build_frame(b: BootstyleBuilderTTk, ttk_style: str, accent: str = None, **options):
    surface_token = options.get('surface') or 'background'
    surface = b.color(surface_token)

    # border options
    show_border = options.get('show_border', False)
    stroke = options.get('stroke', None)
    stroke_radius = options.get('stroke_radius', 4)

    # Border reconciliation: determine if border is enabled and resolve stroke token
    border_enabled = show_border or (stroke is not None)

    if stroke is not None:
        stroke_token = stroke
    elif show_border:
        stroke_token = 'stroke[1]'
    else:
        stroke_token = None

    # border assets and styles
    if border_enabled and stroke_token:
        # Resolve stroke color from semantic token
        stroke_color = b.color(stroke_token)

        # Stroke → thickness inference (internal, not exposed as API)
        # stroke[1] → 1, stroke[2] → 1, stroke[3] → 2
        stroke_thickness = options.get('stroke_thickness')
        if stroke_thickness is None:
            if stroke_token == 'stroke[3]':
                stroke_thickness = 2
            else:
                stroke_thickness = 1

        border_img = create_rounded_border_image(
            size=100,
            radius=stroke_radius,
            fill=surface,
            stroke=stroke_color,
            thickness=stroke_thickness
        )

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
