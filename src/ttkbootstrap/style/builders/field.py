"""Field widget style builders.

This module contains style builders for ttk.Frame widget and field variants used to build
the Entry containers.
"""

from __future__ import annotations

from ttkbootstrap.style.bootstyle_builder_ttk import BootstyleBuilderTTk
from ttkbootstrap.style.element import Element, ElementImage
from ttkbootstrap.style.utility import recolor_image


@BootstyleBuilderTTk.register_builder('default', 'TField')
def build_field_style(b: BootstyleBuilderTTk, ttk_style: str, color: str = None, **options):
    surface_token = options.get('surface_color', 'background')

    surface = b.color(surface_token)
    accent = b.color(color or 'primary')
    normal = surface
    border = b.border(surface)
    disabled = b.disabled('text')
    focused_border = b.focus_border(accent)
    focused_ring = b.focus_ring(accent, surface)

    # input element images
    normal_img = recolor_image(f'input', normal, border, surface)
    focused_img = recolor_image(f'input', normal, focused_border, focused_ring)
    disabled_img = recolor_image(f'input', normal, disabled, surface, surface)

    # input element
    b.create_style_element_image(
        ElementImage(f'{ttk_style}.border', normal_img, sticky="nsew", border=8).state_specs(
            [
                ('disabled', disabled_img),
                ('focus', focused_img),
            ]
        )
    )
    b.create_style_layout(
        ttk_style, Element(f'{ttk_style}.border', sticky="nsew").children(
            [
                Element(f'{ttk_style}.padding', sticky="")
            ]))
    b.configure_style(ttk_style, background=surface)


@BootstyleBuilderTTk.register_builder('input', 'TField')
def build_field_input_style(b: BootstyleBuilderTTk, ttk_style: str, color: str = None, **options):
    surface = b.color("background")  # always use the theme background
    disabled_bg = b.disabled('background')
    disabled_fg = b.disabled('text')
    foreground = b.on_color(surface)

    normal_img = recolor_image('input-inner', surface)
    b.create_style_element_image(ElementImage(f'{ttk_style}.field', normal_img, sticky="nsew"))
    b.create_style_layout(
        ttk_style, Element(f'{ttk_style}.field').children(
            [
                Element('Entry.padding', sticky="ew").children(
                    [
                        Element('Entry.textarea', sticky="nsew")
                    ])
            ]))

    b.configure_style(
        ttk_style,
        relief='flat',
        foreground=foreground,
        background=surface,
        fieldbackground=surface,
        selectborderwidth=0,
        bordercolor=surface,
        darkcolor=surface,
        lightcolor=surface,
        insertcolor=foreground,
        padding=(8, 0),
        selectforeground=b.on_color(b.color('primary')),
        selectbackground=b.color('primary')
    )

    b.map_style(
        ttk_style,
        background=[('disabled', disabled_bg), ('readonly', disabled_bg)],
        fieldbackground=[('disabled', disabled_bg)],
        selectforeground=[],
        selectbackground=[],
        bordercolor=[('disabled', disabled_bg)],
        darkcolor=[('disabled', disabled_bg)],
        lightcolor=[('disabled', disabled_bg)],
        foreground=[('disabled !readonly', disabled_fg), ('', foreground)],
    )


@BootstyleBuilderTTk.register_builder('prefix', 'TField')
def build_field_prefix_style(b: BootstyleBuilderTTk, ttk_style: str, color: str = None, **options):
    build_field_addon_style(b, ttk_style, color, 'prefix', **options)


@BootstyleBuilderTTk.register_builder('suffix', 'TField')
def build_field_suffix_style(b: BootstyleBuilderTTk, ttk_style: str, color: str = None, **options):
    build_field_addon_style(b, ttk_style, color, 'suffix', **options)


def build_field_addon_style(b: BootstyleBuilderTTk, ttk_style: str, _: str, variant: str, **options):
    surface_token = options.get('surface_color', 'background')

    surface = b.color(surface_token)
    border = b.border(surface)
    foreground = b.on_color(surface)
    foreground_disabled = b.disabled('text')
    normal = b.disabled()

    # button element images
    normal_img = recolor_image(f'input-{variant}', normal, border)
    img_padding = 8

    # button element
    b.create_style_element_image(
        ElementImage(
            f'{ttk_style}.border', normal_img, sticky="nsew", border=img_padding, padding=img_padding))

    b.create_style_layout(
        ttk_style, Element(f"{ttk_style}.border", sticky="nsew").children(
            [
                Element("Label.padding", sticky="nsew").children(
                    [
                        Element("Label.label", sticky="")
                    ])
            ]))

    b.configure_style(
        ttk_style,
        background=surface,
        foreground=foreground,
        relief='flat',
        stipple="gray12",
        padding=0
    )

    # map icon if available
    icon = options.get('icon')

    state_spec = dict(
        foreground=[('disabled', foreground_disabled), ('', foreground)])

    if icon is not None:
        icon = b.normalize_icon_spec(icon)
        icon['size'] = 18
        state_spec['image'] = b.map_stateful_icons(icon, state_spec['foreground'])

    b.map_style(ttk_style, **state_spec)
