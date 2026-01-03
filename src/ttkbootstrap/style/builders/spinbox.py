"""Spinbox widget style builders.

This module contains style builders for ttk.Spinbox widget and variants.
"""

from __future__ import annotations

from ttkbootstrap_icons_bs import BootstrapIcon
from ttkbootstrap.style.bootstyle_builder_ttk import BootstyleBuilderTTk
from ttkbootstrap.style.element import Element, ElementImage
from ttkbootstrap.style.utility import recolor_image


@BootstyleBuilderTTk.register_builder('default', 'TSpinbox')
def build_spinbox_style(b: BootstyleBuilderTTk, ttk_style: str, accent: str = None, **options):
    surface_token = options.get('surface', 'content')

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

    # input elements
    normal_img = recolor_image('input', normal, border, surface)
    focused_img = recolor_image('input', normal, focused_border, focused_ring)
    disabled_img = recolor_image('input', disabled, border, surface)

    b.create_style_element_image(
        ElementImage(f'{ttk_style}.field', normal_img, sticky='nsew', border=b.scale(8)).state_specs(
            [
                ('disabled', disabled_img),
                ('readonly', disabled_img),
                ('focus', focused_img)
            ]
        )
    )

    # add chevron image
    icon_size = b.scale(14)
    arrow_up_normal_img = BootstrapIcon('caret-up-fill', color=foreground, size=icon_size).image
    arrow_up_disabled_img = BootstrapIcon('caret-up-fill', color=disabled_foreground, size=icon_size).image
    arrow_down_normal_img = BootstrapIcon('caret-down-fill', color=foreground, size=icon_size).image
    arrow_down_disabled_img = BootstrapIcon('caret-down-fill', color=disabled_foreground, size=icon_size).image

    b.create_style_element_image(
        ElementImage(f'{ttk_style}.uparrow', arrow_up_normal_img, sticky='nsew', width=b.scale(16)).state_specs(
            [
                ('disabled', arrow_up_disabled_img),
                ('', arrow_up_normal_img),
            ])
    )

    b.create_style_element_image(
        ElementImage(f'{ttk_style}.downarrow', arrow_down_normal_img, sticky='nsew', width=b.scale(16)).state_specs(
            [
                ('disabled', arrow_down_disabled_img),
                ('', arrow_down_normal_img),
            ])
    )

    # layout
    b.create_style_layout(
        ttk_style,
        Element(f'{ttk_style}.field', sticky="ew", side="top").children(
            [
                Element('null', side='right', sticky='').children(
                    [
                        Element(f'{ttk_style}.uparrow', side='top', sticky='e'),
                        Element(f'{ttk_style}.downarrow', side='bottom', sticky='e'),
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
        background=surface,
        padding=b.scale((8, 0)),
        selectforeground=select_foreground,
        selectbackground=select_background,
        insertcolor=foreground,
        selectborderwidth=0,
        font="body"
    )

    b.map_style(
        ttk_style,
        selectforeground=[],
        selectbackground=[],
        foreground=[('disabled !readonly', disabled_foreground), ('', foreground)],
    )
