"""Combobox widget style builders.

This module contains style builders for ttk.Combobox widget and variants.
"""

from __future__ import annotations

from ttkbootstrap import BootstrapIcon
from ttkbootstrap.style.bootstyle_builder_ttk import BootstyleBuilderTTk
from ttkbootstrap.style.element import Element, ElementImage
from ttkbootstrap.style.utility import recolor_image


@BootstyleBuilderTTk.register_builder('default', 'TCombobox')
def build_combobox_style(b: BootstyleBuilderTTk, ttk_style: str, color: str = None, **options):
    surface_token = options.get('surface_color', 'background')

    surface = b.color(surface_token)
    accent = b.color(color or 'primary')
    foreground = b.on_color(surface)

    normal = surface
    border = b.border(surface)
    disabled = b.disabled()
    focused_border = b.focus_border(accent)
    focused_ring = b.focus_ring(accent, surface)

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
    chevron_normal_img = BootstrapIcon('caret-down-fill', color=foreground, size=b.scale(14)).image
    chevron_disabled_img = BootstrapIcon('caret-down-fill', color=disabled_foreground, size=b.scale(14)).image

    b.create_style_element_image(
        ElementImage(
            f'{ttk_style}.chevron', chevron_normal_img, sticky='nsew', border=1, width=b.scale(16)).state_specs(
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

    b.configure_style(
        ttk_style,
        foreground=foreground,
        background=surface,
        padding=b.scale((6, 0)),
        selectforeground=select_foreground,
        selectbackground=select_background,
        insertcolor=foreground,
        selectborderwidth=0,
        font='body'
    )

    b.map_style(
        ttk_style,
        selectforeground=[],
        selectbackground=[],
        foreground=[('disabled !readonly', disabled_foreground), ('', foreground)],
    )
