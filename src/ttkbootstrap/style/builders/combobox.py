"""Combobox widget style builders.

This module contains style builders for ttk.Combobox widget and variants.
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
    chevron_width,
)


@BootstyleBuilderTTk.register_builder('default', 'TCombobox')
def build_combobox_style(b: BootstyleBuilderTTk, ttk_style: str, accent: str = None, **options):
    surface_token = options.get('surface', 'content')
    density = normalize_button_density(options.get('density', 'default'))

    surface = b.color(surface_token)
    accent_color = b.color(accent or 'primary')
    foreground = b.on_color(surface)

    normal = surface
    border = b.border(surface)
    disabled = b.disabled()
    focused_border = b.focus_border(accent_color)
    focused_ring = b.focus_ring(accent_color, surface)

    select_background = b.color('primary')
    select_foreground = b.on_color(select_background)
    disabled_foreground = b.disabled('text')

    # input elements - use density-aware images from manifest
    img_key = entry_image_key('input', density)
    normal_img = recolor_element_image(img_key, normal, border, surface)
    focused_img = recolor_element_image(img_key, normal, focused_border, focused_ring)
    disabled_img = recolor_element_image(img_key, disabled, border, surface)

    b.create_style_element_image(
        ElementImage(f'{ttk_style}.field', normal_img.image, sticky='nsew', border=normal_img.meta.border).state_specs(
            [
                ('disabled', disabled_img.image),
                ('readonly', disabled_img.image),
                ('focus', focused_img.image)
            ]
        )
    )

    # add chevron image - use density-aware icon size
    icon_size = entry_icon_size(b, density)
    chevron_normal_img = BootstrapIcon('caret-down-fill', color=foreground, size=icon_size).image
    chevron_disabled_img = BootstrapIcon('caret-down-fill', color=disabled_foreground, size=icon_size).image

    b.create_style_element_image(
        ElementImage(
            f'{ttk_style}.chevron', chevron_normal_img, sticky='', border=1, width=chevron_width(b)).state_specs(
            [
                ('disabled', chevron_disabled_img),
                ('', chevron_normal_img),
            ])
    )

    # layout
    b.create_style_layout(
        ttk_style,
        Element(f'{ttk_style}.field', sticky="ew").children(
            [
                Element(f'{ttk_style}.chevron', side='right', sticky='s'),
                Element('Combobox.padding', sticky="nsew", expand=1).children(
                    [
                        Element("Combobox.textarea", sticky="nsew")
                    ])
            ])
    )

    # postoffset aligns the popdown with the inner edge of the visible input
    # border, accounting for both the focus-ring affordance and the border
    # line baked into the input image (10 source-px for default, 8 source-px
    # for compact). Tk's PlacePopdown reads {dx dy dw dh} and adjusts the
    # popdown geometry accordingly.
    inset = b.scale_from_source(8 if density == 'compact' else 10)
    postoffset = (inset, 0, -2 * inset, 0)

    b.configure_style(
        ttk_style,
        foreground=foreground,
        background=surface,
        padding=entry_padding(b, density),
        selectforeground=select_foreground,
        selectbackground=select_background,
        insertcolor=foreground,
        selectborderwidth=0,
        font=entry_font(density),
        postoffset=postoffset,
    )

    b.map_style(
        ttk_style,
        selectforeground=[],
        selectbackground=[],
        foreground=[('disabled !readonly', disabled_foreground), ('', foreground)],
    )
