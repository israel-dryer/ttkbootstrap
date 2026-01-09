"""Badge style builders.

This module contains style builders for ttk.Label widget badge variants.
"""
from ttkbootstrap.style.bootstyle_builder_ttk import BootstyleBuilderTTk
from ttkbootstrap.style.element import Element, ElementImage
from ttkbootstrap.style.utility import recolor_element_image


@BootstyleBuilderTTk.register_builder('square', 'TBadge')
def build_default_badge_style(b: BootstyleBuilderTTk, ttk_style: str, accent: str = None, **options):
    build_badge(b, ttk_style, accent, 'square', **options)

@BootstyleBuilderTTk.register_builder('pill', 'TBadge')
def build_pill_badge_style(b: BootstyleBuilderTTk, ttk_style: str, accent: str = None, **options):
    build_badge(b, ttk_style, accent, 'pill', **options)


def build_badge(b: BootstyleBuilderTTk, ttk_style: str, accent: str = None, variant: str = 'square', **options):
    """Create a badge style for the variant specified"""

    surface_token = options.get('surface', 'content')
    surface = b.color(surface_token)
    normal = b.color(accent or 'primary')
    foreground = b.on_color(normal)

    badge_img = recolor_element_image(f'badge_{variant}', normal, surface, surface, surface)

    b.create_style_element_image(ElementImage(f'{ttk_style}.border', badge_img.image, 
                                              border=badge_img.meta.border, 
                                              padding=badge_img.meta.padding, 
                                              height=badge_img.meta.height,
                                              sticky='nsew'))

    b.create_style_layout(
        ttk_style, Element(f"{ttk_style}.border", sticky="nsew").children(
            [
                Element("Label.padding", sticky="nsew").children(
                    [
                        Element("Label.label", sticky="ew")
                    ])
            ]))
    
    b.configure_style(ttk_style, background=surface, foreground=foreground, padding=(6, 0))
