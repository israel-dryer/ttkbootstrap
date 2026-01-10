"""Scale widget style builders.

This module contains style builders for ttk.Scale widget and variants.
"""

from __future__ import annotations

from ttkbootstrap.style.bootstyle_builder_ttk import BootstyleBuilderTTk
from ttkbootstrap.style.element import Element, ElementImage
from ttkbootstrap.style.utility import recolor_element_image


@BootstyleBuilderTTk.register_builder('default', 'TScale')
def build_scale_style(b: BootstyleBuilderTTk, ttk_style: str, accent: str = 'primary', **options):
    accent_token = accent or 'primary'
    surface_token = options.get('surface', 'content')
    orient = options.get('orient', 'vertical').title()

    background = b.color(surface_token)
    foreground = b.on_color(background)
    foreground_disabled = b.disabled("text")
    track_color = b.border(background)
    handle_normal = b.color(accent_token)
    handle_pressed = b.pressed(handle_normal)
    handle_disabled = b.disabled("text")
    track_disabled = b.disabled("background")

    # style images
    handle_normal_img = recolor_element_image("slider_handle", background, handle_normal)
    handle_pressed_img = recolor_element_image("slider_handle_focus", background, handle_normal)
    handle_focus_img = recolor_element_image("slider_handle_focus", background, handle_pressed)
    handle_disabled_img = recolor_element_image("slider_handle", handle_disabled, handle_disabled)

    track_normal_img = recolor_element_image(f"slider_track_{orient.lower()}", track_color)
    track_disabled_img = recolor_element_image(f"slider_track_{orient.lower()}", track_disabled)
    sticky = "ew" if orient == "Horizontal" else "ns"
    side = "left" if orient == "Horizontal" else "top"

    b.create_style_element_image(
        ElementImage(f"{ttk_style}.{orient}.Scale.slider", handle_normal_img.image,
                     width=handle_normal_img.meta.height,
                     height=handle_normal_img.meta.width,
                     sticky=''
                     ).state_specs(
            [
                ('disabled', handle_disabled_img.image),
                ('background focus', handle_focus_img.image),
                ('pressed', handle_pressed_img.image),
            ]))

    b.create_style_element_image(
        ElementImage(f"{ttk_style}.{orient}.Scale.trough", track_normal_img.image,
                     padding=track_normal_img.meta.padding,
                     border=track_normal_img.meta.border).state_specs(
            [
                ('disabled', track_disabled_img.image)
            ]))

    b.create_style_layout(
        ttk_style, Element(f"{orient}.Scale.padding", sticky=sticky).children(
            [
                Element(f'{ttk_style}.{orient}.Scale.trough', sticky=sticky),
                Element(f'{ttk_style}.{orient}.Scale.slider', sticky="", side=side)]))

    b.configure_style(ttk_style, background=background, foreground=foreground)
    b.map_style(ttk_style, background=[], foreground=[('disabled', foreground_disabled), ('', foreground)])