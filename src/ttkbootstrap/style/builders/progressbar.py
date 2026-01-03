"""Progressbar widget style builders.

This module contains style builders for ttk.Progressbar widgets and variants.
"""

from __future__ import annotations

from ttkbootstrap.style.bootstyle_builder_ttk import BootstyleBuilderTTk
from ttkbootstrap.style.element import Element, ElementImage
from ttkbootstrap.style.utility import recolor_image


@BootstyleBuilderTTk.register_builder('default', 'TProgressbar')
def build_default_progressbar_style(b: BootstyleBuilderTTk, ttk_style: str, accent: str = 'primary', **options):
    build_progressbar_style(b, ttk_style, accent, 'default', **options)


@BootstyleBuilderTTk.register_builder('striped', 'TProgressbar')
def build_striped_progressbar_style(b: BootstyleBuilderTTk, ttk_style: str, accent: str = 'primary', **options):
    build_progressbar_style(b, ttk_style, accent, 'striped', **options)


def build_progressbar_style(b: BootstyleBuilderTTk, ttk_style: str, accent: str, variant: str, **options):
    orient = options.get("orient")
    surface_token = options.get("surface", "background")

    # style colors
    background = b.color(surface_token)
    trough_color = b.border(background)
    trough_disabled = b.disabled("background")
    bar_color = b.color(accent or "primary")
    bar_disabled = b.disabled("text")

    sticky = "ew" if orient == "horizontal" else "ns"
    side = "left" if orient == "horizontal" else "top"

    trough_normal_img = recolor_image(f"progress-trough-{orient}", trough_color)
    trough_disabled_img = recolor_image(f"progress-trough-{orient}", trough_disabled)
    bar_normal_img = recolor_image(f"progress-bar-{orient}-{variant}", background, bar_color)
    bar_disabled_img = recolor_image(f"progress-bar-{orient}-{variant}", background, bar_disabled)
    element_prefix = ttk_style.replace('TProgressbar', 'Progressbar')

    b.create_style_element_image(
        ElementImage(
            f"{element_prefix}.trough", trough_normal_img).state_specs(
            [
                ('disabled', trough_disabled_img)
            ]))

    b.create_style_element_image(
        ElementImage(f"{element_prefix}.pbar", bar_normal_img).state_specs(
            [
                ('disabled', bar_disabled_img)
            ]))

    b.create_style_layout(
        ttk_style,
        Element(f'{element_prefix}.trough', sticky="nsew").children(
            [
                Element(f'{element_prefix}.pbar', sticky=sticky, side=side)
            ]))

    b.configure_style(ttk_style, background=background)
    b.map_style(ttk_style, background=[])
