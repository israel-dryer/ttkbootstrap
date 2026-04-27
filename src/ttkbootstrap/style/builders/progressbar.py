"""Progressbar widget style builders.

This module contains style builders for ttk.Progressbar widgets and variants.
"""

from __future__ import annotations

from ttkbootstrap.style.bootstyle_builder_ttk import BootstyleBuilderTTk
from ttkbootstrap.style.element import Element, ElementImage
from ttkbootstrap.style.utility import recolor_element_image


@BootstyleBuilderTTk.register_builder('default', 'TProgressbar')
def build_default_progressbar_style(b: BootstyleBuilderTTk, ttk_style: str, accent: str = 'primary', **options):
    build_progressbar_style(b, ttk_style, accent, 'default', **options)


@BootstyleBuilderTTk.register_builder('striped', 'TProgressbar')
def build_striped_progressbar_style(b: BootstyleBuilderTTk, ttk_style: str, accent: str = 'primary', **options):
    build_progressbar_style(b, ttk_style, accent, 'striped', **options)


@BootstyleBuilderTTk.register_builder('thin', 'TProgressbar')
def build_thin_progressbar_style(b: BootstyleBuilderTTk, ttk_style: str, accent: str = 'primary', **options):
    build_progressbar_style(b, ttk_style, accent, 'thin', **options)

def build_progressbar_style(b: BootstyleBuilderTTk, ttk_style: str, accent: str, variant: str, **options):
    orient = options.get("orient")
    surface_token = options.get("surface", "content")

    # style colors
    background = b.color(surface_token)
    trough_color = b.border(background)
    trough_disabled = b.disabled("background")
    bar_color = b.color(accent or "primary")
    bar_disabled = b.disabled("text")

    sticky = "ew" if orient == "horizontal" else "ns"
    side = "left" if orient == "horizontal" else "top"

    bar_image_key = f'progress_bar_{orient}_{variant}'
    trough_image_key = bar_image_key if variant == 'thin' else f"progress_bar_{orient}_trough"

    trough_normal_img = recolor_element_image(trough_image_key, trough_color, trough_color)
    trough_disabled_img = recolor_element_image(trough_image_key, trough_disabled, trough_disabled)
    bar_normal_img = recolor_element_image(bar_image_key, background, bar_color)
    bar_disabled_img = recolor_element_image(bar_image_key, background, bar_disabled)
    element_prefix = ttk_style.replace('TProgressbar', 'Progressbar')

    b.create_style_element_image(
        ElementImage(
            f"{element_prefix}.trough", trough_normal_img.image, sticky='nsew').state_specs(
            [
                ('disabled', trough_disabled_img.image)
            ]))

    b.create_style_element_image(
        ElementImage(f"{element_prefix}.pbar", bar_normal_img.image).state_specs(
            [
                ('disabled', bar_disabled_img.image)
            ]))

    b.create_style_layout(
        ttk_style,
        Element(f'{element_prefix}.trough', sticky="nsew").children(
            [
                Element(f'{element_prefix}.pbar', sticky=sticky, side=side)
            ]))

    b.configure_style(ttk_style, background=background)
    b.map_style(ttk_style, background=[])