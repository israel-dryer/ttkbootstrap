"""Field widget style builders.

This module contains style builders for ttk.Frame widget and field variants used to build
the Entry containers.
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
    field_height,
    entry_icon_size,
    entry_image_key,
)


@BootstyleBuilderTTk.register_builder('default', 'TField')
def build_field_style(b: BootstyleBuilderTTk, ttk_style: str, accent: str = None, **options):
    surface_token = options.get('surface', 'content')
    density = normalize_button_density(options.get('density', 'default'))

    surface = b.color(surface_token)
    accent_color = b.color(accent or 'primary')
    normal = surface
    border = b.border(surface)
    disabled = b.disabled('text')
    focused_border = b.focus_border(accent_color)
    focused_ring = b.focus_ring(accent_color, surface)

    # input element images - use density-aware images from manifest
    img_key = entry_image_key('input', density)
    normal_img = recolor_element_image(img_key, normal, border, surface)
    focused_img = recolor_element_image(img_key, normal, focused_border, focused_ring)
    disabled_img = recolor_element_image(img_key, normal, disabled, surface, surface)

    # input element
    b.create_style_element_image(
        ElementImage(f'{ttk_style}.border', normal_img.image, sticky="nsew", border=normal_img.meta.border).state_specs(
            [
                ('disabled', disabled_img.image),
                ('focus', focused_img.image),
            ]
        )
    )
    b.create_style_layout(
        ttk_style, Element(f'{ttk_style}.border', sticky="nsew").children(
            [
                Element(f'{ttk_style}.padding', sticky="nsew")
            ]))
    b.configure_style(ttk_style, background=surface)


@BootstyleBuilderTTk.register_builder('input', 'TField')
def build_field_input_style(b: BootstyleBuilderTTk, ttk_style: str, accent: str = None, **options):
    surface_token = options.get('surface', 'content')
    density = normalize_button_density(options.get('density', 'default'))

    surface = b.color(surface_token)
    disabled_bg = b.disabled('background')
    disabled_fg = b.disabled('text')
    foreground = b.on_color(surface)

    # Inner field is a white fill that gets recolored; height controls density
    field_img = recolor_element_image('field', surface)
    height = field_height(b, density)

    b.create_style_element_image(ElementImage(f'{ttk_style}.field', field_img.image, sticky="nsew", height=height))
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
        padding=entry_padding(b, density),
        font=entry_font(density),
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


@BootstyleBuilderTTk.register_builder('spinner', 'TField')
def build_spinner_input_style(b: BootstyleBuilderTTk, ttk_style: str, accent: str = None, **options):
    surface_token = options.get('surface', 'content')
    density = normalize_button_density(options.get('density', 'default'))

    surface = b.color(surface_token)
    disabled_bg = b.disabled('background')
    disabled_fg = b.disabled('text')
    foreground = b.on_color(surface)

    # Inner field is a white fill that gets recolored; height controls density
    field_img = recolor_element_image('field', surface)
    height = field_height(b, density)

    b.create_style_element_image(ElementImage(f'{ttk_style}.field', field_img.image, sticky="nsew", height=height))

    # add arrow images - use density-aware icon size
    icon_size = entry_icon_size(b, density)
    arrow_up_normal_img = BootstrapIcon('caret-up-fill', color=foreground, size=icon_size).image
    arrow_up_disabled_img = BootstrapIcon('caret-up-fill', color=disabled_fg, size=icon_size).image
    arrow_down_normal_img = BootstrapIcon('caret-down-fill', color=foreground, size=icon_size).image
    arrow_down_disabled_img = BootstrapIcon('caret-down-fill', color=disabled_fg, size=icon_size).image

    # Arrow element images - use smaller height for compact
    arrow_height = b.scale(10) if density == 'compact' else b.scale(13)

    b.create_style_element_image(
        ElementImage(f'{ttk_style}.uparrow', arrow_up_normal_img, sticky='', width=b.scale(16), height=arrow_height).state_specs([
            ('disabled', arrow_up_disabled_img),
            ('', arrow_up_normal_img),
        ])
    )

    b.create_style_element_image(
        ElementImage(f'{ttk_style}.downarrow', arrow_down_normal_img, sticky='', width=b.scale(16), height=arrow_height).state_specs([
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

    # Add extra right padding for spinner arrows
    base_padding = entry_padding(b, density)
    spinner_padding = (base_padding[0], base_padding[1], base_padding[0] + b.scale(3), base_padding[1])

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
        padding=spinner_padding,
        font=entry_font(density),
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
def build_field_prefix_style(b: BootstyleBuilderTTk, ttk_style: str, accent: str = None, **options):
    build_field_addon_style(b, ttk_style, accent, 'before', **options)


@BootstyleBuilderTTk.register_builder('suffix', 'TField')
def build_field_suffix_style(b: BootstyleBuilderTTk, ttk_style: str, accent: str = None, **options):
    build_field_addon_style(b, ttk_style, accent, 'after', **options)


def build_field_addon_style(b: BootstyleBuilderTTk, ttk_style: str, _: str, variant: str, **options):
    """Build prefix/suffix addon styles for entry fields.

    Args:
        b: The bootstyle builder instance.
        ttk_style: The TTK style name.
        _: Unused accent parameter.
        variant: 'before' for prefix, 'after' for suffix.
        **options: Style options including 'density', 'surface', 'use_active_states', 'icon'.
    """
    surface_token = options.get('surface', 'content')
    density = normalize_button_density(options.get('density', 'default'))
    use_active_states = options.get('use_active_states', False)
    surface = b.color(surface_token)

    if use_active_states:
        surface_active = b.active(surface)
        surface_pressed = b.pressed(surface)
    else:
        surface_active = surface_pressed = surface

    border = b.border(surface)
    foreground = b.on_color(surface)
    foreground_disabled = b.disabled('text')
    normal = b.disabled(surface=surface)

    # addon element images - use density-aware images from manifest
    # variant is 'before' or 'after', maps to input_before_* or input_after_*
    img_key = entry_image_key(f'input_{variant}', density)
    normal_img = recolor_element_image(img_key, normal, border)

    if use_active_states:
        active_img = recolor_element_image(img_key, surface_active, border)
        pressed_img = recolor_element_image(img_key, surface_pressed, border)
    else:
        active_img = pressed_img = normal_img

    # addon element - set explicit height to match field height
    height = field_height(b, density)
    b.create_style_element_image(
        ElementImage(f'{ttk_style}.border', normal_img.image, border=normal_img.meta.border, height=height).state_specs([
            ('pressed', pressed_img.image),
            ('active', active_img.image),
            ('', normal_img.image)
        ]))

    b.create_style_layout(
        ttk_style, Element(f"{ttk_style}.border", sticky="nsew").children(
            [
                Element("Button.padding", sticky="nsew").children(
                    [
                        Element("Button.label", sticky="nsew")
                    ])
            ]))

    # Add horizontal padding - less for icon-only buttons
    icon_only = options.get('icon_only', False)
    if icon_only:
        addon_padding = b.scale((5, 0)) if density == 'compact' else b.scale((4, 0))
    else:
        addon_padding = b.scale((8, 0))
    b.configure_style(
        ttk_style,
        background=surface,
        foreground=foreground,
        relief='flat',
        stipple="gray12",
        padding=addon_padding,
        anchor='center',
    )

    # map icon if available
    icon = options.get('icon')

    state_spec = dict(
        foreground=[
            ('disabled', foreground_disabled),
            ('pressed !disabled', foreground),
            ('hover !disabled', foreground),
            ('', foreground)
        ])

    if icon is not None:
        icon = b.normalize_icon_spec(icon)
        # Use density-aware icon size for addon icons
        addon_icon_size = b.scale(16) if density == 'compact' else b.scale(17)
        icon['size'] = addon_icon_size
        state_spec['image'] = b.map_stateful_icons(icon, state_spec['foreground'])

    b.map_style(ttk_style, **state_spec)
