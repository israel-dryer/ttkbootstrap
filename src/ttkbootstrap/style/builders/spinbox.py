"""Spinbox widget style builders.

This module contains style builders for ttk.Spinbox widget and variants.
"""

from __future__ import annotations

from ttkbootstrap_icons_bs import BootstrapIcon
from ttkbootstrap.style.bootstyle_builder_ttk import BootstyleBuilderTTk
from ttkbootstrap.style.element import Element, ElementImage
from ttkbootstrap.style.utility import recolor_element_image
from ttkbootstrap.style.builders.utils import (
    normalize_button_density,
    entry_font,
    entry_padding,
    entry_icon_size,
    entry_image_key,
    spinner_arrow_height,
    spinner_arrow_width,
)


@BootstyleBuilderTTk.register_builder('default', 'TSpinbox')
def build_spinbox_style(b: BootstyleBuilderTTk, ttk_style: str, accent: str = None, **options):
    surface_token = options.get('surface', 'content')
    fill_token = options.get('input_background') or 'content'
    density = normalize_button_density(options.get('density', 'default'))

    fill = b.color(fill_token)
    container_surface = b.color(surface_token)
    accent_color = b.color(accent or 'primary')
    foreground = b.on_color(fill)

    normal = fill
    border = b.border(fill)
    disabled = b.disabled()
    focused_border = b.focus_border(accent_color)
    focused_ring = b.focus_ring(accent_color, container_surface)

    select_background = b.color('primary')
    select_foreground = b.on_color(select_background)
    disabled_foreground = b.disabled('text')

    # input elements - use density-aware images from manifest
    img_key = entry_image_key('input', density)
    normal_img = recolor_element_image(img_key, normal, border, container_surface, container_surface)
    focused_img = recolor_element_image(img_key, normal, focused_border, focused_ring, container_surface)
    disabled_img = recolor_element_image(img_key, disabled, border, container_surface, container_surface)

    b.create_style_element_image(
        ElementImage(f'{ttk_style}.field', normal_img.image, sticky='nsew', border=normal_img.meta.border).state_specs(
            [
                ('disabled', disabled_img.image),
                ('readonly', disabled_img.image),
                ('focus', focused_img.image)
            ]
        )
    )

    # add arrow images - use density-aware icon size (same as combobox)
    icon_size = entry_icon_size(b, density)
    arrow_up_normal_img = BootstrapIcon('caret-up-fill', color=foreground, size=icon_size).image
    arrow_up_disabled_img = BootstrapIcon('caret-up-fill', color=disabled_foreground, size=icon_size).image
    arrow_down_normal_img = BootstrapIcon('caret-down-fill', color=foreground, size=icon_size).image
    arrow_down_disabled_img = BootstrapIcon('caret-down-fill', color=disabled_foreground, size=icon_size).image

    # Arrow element images
    arrow_height = spinner_arrow_height(b, density)
    arrow_width = spinner_arrow_width(b)

    b.create_style_element_image(
        ElementImage(f'{ttk_style}.uparrow', arrow_up_normal_img, sticky='', width=arrow_width, height=arrow_height).state_specs([
            ('disabled', arrow_up_disabled_img),
            ('', arrow_up_normal_img),
        ])
    )

    b.create_style_element_image(
        ElementImage(f'{ttk_style}.downarrow', arrow_down_normal_img, sticky='', width=arrow_width, height=arrow_height).state_specs([
            ('disabled', arrow_down_disabled_img),
            ('', arrow_down_normal_img),
        ])
    )

    # layout - arrows stacked vertically
    b.create_style_layout(
        ttk_style,
        Element(f'{ttk_style}.field', sticky="nsew").children(
            [
                Element('null', side='right', sticky='').children(
                    [
                        Element(f'{ttk_style}.uparrow', side='top', sticky=''),
                        Element(f'{ttk_style}.downarrow', side='top', sticky=''),
                    ]),
                Element('Spinbox.padding', sticky='nsew').children(
                    [
                        Element('Spinbox.textarea', sticky='nsew'),
                    ])
            ]),
    )

    b.configure_style(
        ttk_style,
        foreground=foreground,
        background=fill,
        padding=entry_padding(b, density),
        selectforeground=select_foreground,
        selectbackground=select_background,
        insertcolor=foreground,
        selectborderwidth=0,
        font=entry_font(density)
    )

    b.map_style(
        ttk_style,
        selectforeground=[],
        selectbackground=[],
        foreground=[('disabled !readonly', disabled_foreground), ('', foreground)],
    )
