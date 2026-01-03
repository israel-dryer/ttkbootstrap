"""Badge style builders.

This module contains style builders for ttk.Label widget badge variants.
"""

from ttkbootstrap.style.bootstyle_builder_ttk import BootstyleBuilderTTk
from ttkbootstrap.style.element import Element, ElementImage
from ttkbootstrap.style.utility import recolor_image


@BootstyleBuilderTTk.register_builder('square', 'TBadge')
@BootstyleBuilderTTk.register_builder('default', 'TBadge')
def build_default_badge_style(b: BootstyleBuilderTTk, ttk_style: str, accent: str = None, **options):
    build_badge(b, ttk_style, accent, 'default', **options)


@BootstyleBuilderTTk.register_builder('pill', 'TBadge')
def build_pill_badge_style(b: BootstyleBuilderTTk, ttk_style: str, accent: str = None, **options):
    build_badge(b, ttk_style, accent, 'pill', **options)


def build_badge(b: BootstyleBuilderTTk, ttk_style: str, accent: str = None, variant: str = 'default', **options):
    surface_token = options.get('surface', 'content')

    surface = b.color(surface_token)
    normal = b.color(accent or 'primary')
    foreground = b.on_color(normal)

    normal_img = recolor_image(f'badge-{variant}', normal)

    border = b.scale(6)
    padding = b.scale((6, 0))

    # button element
    b.create_style_element_image(
        ElementImage(
            f'{ttk_style}.border', normal_img,
            sticky="nsew", border=border, padding=padding))

    b.create_style_layout(
        ttk_style, Element(f"{ttk_style}.border", sticky="").children(
            [
                Element("Label.padding", sticky="nsew").children(
                    [
                        Element("Label.label", sticky="nsew")
                    ])
            ]))

    style_padding = b.scale((4, 2))
    b.configure_style(ttk_style, font="caption", background=surface, foreground=foreground, padding=style_padding)
