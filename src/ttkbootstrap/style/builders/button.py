"""Button widget style builders.

This module contains style builders for ttk.Button widgets and variants.
"""

from __future__ import annotations

from ttkbootstrap.style.bootstyle_builder_ttk import BootstyleBuilderTTk
from ttkbootstrap.style.element import ElementImage
from ttkbootstrap.style.utility import recolor_element_image
from ttkbootstrap.style.builders.utils import (
    apply_icon_mapping,
    button_font,
    button_layout,
    button_padding,
    icon_size,
    normalize_button_density,
)


@BootstyleBuilderTTk.register_builder('solid', 'TButton')
@BootstyleBuilderTTk.register_builder('default', 'TButton')
def build_solid_button_style(b: BootstyleBuilderTTk, ttk_style: str, accent: str = None, **options):
    """
    Configure the button style.

    Style options include:
        * icon
        * icon_only
        * anchor
    """
    anchor = options.get('anchor', 'center')
    accent_token = accent or 'primary'
    surface_token = options.get('surface', 'content')
    density = options.get('density', 'default')

    surface = b.color(surface_token)
    normal = b.color(accent_token)
    foreground = b.on_color(normal)
    pressed = b.pressed(normal)
    hovered = focused = b.active(normal)
    focused_border = b.focus_border(normal)
    disabled = b.disabled()
    focused_ring = b.focus_ring(normal, surface)
    foreground_disabled = b.disabled('text', disabled)

    icon_only = options.get('icon_only', False)
    image_key = f'button_{normalize_button_density(density)}'

    normal_img = recolor_element_image(image_key, normal, normal, surface)
    pressed_img = recolor_element_image(image_key, pressed, pressed, surface)
    hovered_img = recolor_element_image(image_key, hovered, hovered, surface)
    focused_img = recolor_element_image(image_key, focused, focused_border, focused_ring)
    focused_hovered_img = recolor_element_image(image_key, hovered, focused_border, focused_ring)
    focused_pressed_img = recolor_element_image(image_key, pressed, focused_border, focused_ring)
    disabled_img = recolor_element_image(image_key, disabled, disabled, surface, surface)


    b.create_style_element_image(
        ElementImage(
            f'{ttk_style}.Button.border',
            normal_img.image,
            sticky="nsew",
            border=normal_img.meta.border,
            padding=normal_img.meta.border
        ).state_specs(
            [
                ('disabled', disabled_img.image),
                ('background focus pressed', focused_pressed_img.image),
                ('background focus hover', focused_hovered_img.image),
                ('background focus', focused_img.image),
                ('pressed', pressed_img.image),
                ('hover', hovered_img.image),
            ]))

    b.create_style_layout(
        ttk_style,
        button_layout(ttk_style),
    )

    b.configure_style(
        ttk_style,
        background=surface,
        foreground=foreground,
        stipple="gray12",
        relief='flat',
        padding=button_padding(b, icon_only, density),
        anchor=anchor,
        font=button_font(density)
    )

    state_spec = dict(
        foreground=[('disabled', foreground_disabled), ('', foreground)],
        background=[('disabled', disabled)]
    )
    state_spec = apply_icon_mapping(b, options, state_spec, icon_size(icon_only, density))

    b.map_style(ttk_style, **state_spec)


@BootstyleBuilderTTk.register_builder('outline', 'TButton')
def build_outline_button_style(b: BootstyleBuilderTTk, ttk_style: str, accent: str = None, **options):
    """
    Configure the outline button style.

    Style options include:
        * icon
        * icon_only
        * anchor
    """
    anchor = options.get('anchor', 'center')
    accent_token = accent or 'primary'
    surface_token = options.get('surface', 'content')
    density = options.get('density', 'default')
    icon_only = options.get('icon_only', False)
    image_key = f'button_{normalize_button_density(density)}'

    surface = b.color(surface_token)

    foreground_normal = b.color(accent_token)
    foreground_disabled = b.disabled('text', surface)
    foreground_active = b.on_color(foreground_normal)

    disabled = foreground_disabled
    normal = surface
    pressed = b.active(foreground_normal)
    focused = hovered = pressed
    focused_border = b.focus_border(foreground_normal)
    focused_ring = b.focus_ring(foreground_normal, surface)



    # button element images
    normal_img = recolor_element_image(image_key, normal, foreground_normal, surface)
    pressed_img = recolor_element_image(image_key, pressed, pressed, surface)
    hovered_img = recolor_element_image(image_key, hovered, hovered, surface)
    focused_img = recolor_element_image(image_key, focused, focused_border, focused_ring)
    focused_hovered_img = recolor_element_image(image_key, hovered, focused_border, focused_ring)
    focused_pressed_img = recolor_element_image(image_key, pressed, focused_border, focused_ring)
    disabled_img = recolor_element_image(image_key, surface, disabled, surface, surface)

    b.create_style_element_image(
        ElementImage(
            f'{ttk_style}.Button.border',
            normal_img.image,
            sticky="nsew",
            border=normal_img.meta.border,
            padding=normal_img.meta.border
        ).state_specs(
            [
                ('disabled', disabled_img.image),
                ('background focus pressed', focused_pressed_img.image),
                ('background focus hover', focused_hovered_img.image),
                ('background focus', focused_img.image),
                ('pressed', pressed_img.image),
                ('hover', hovered_img.image),
            ])
    )

    b.create_style_layout(
        ttk_style,
        button_layout(ttk_style),
    )

    padding = button_padding(b, icon_only, density)

    b.configure_style(
        ttk_style,
        background=surface,
        foreground=foreground_normal,
        relief='flat',
        stipple="gray12",
        anchor=anchor,
        padding=padding,
        font=button_font(density)
    )

    state_spec = dict(
        foreground=[
            ('disabled', foreground_disabled),
            ('background focus', foreground_active),
            ('hover', foreground_active),
            ('', foreground_normal)
        ], background=[('disabled', surface)]
    )

    state_spec = apply_icon_mapping(b, options, state_spec, icon_size(icon_only, density))

    b.map_style(ttk_style, **state_spec)


@BootstyleBuilderTTk.register_builder('text', 'TButton')
def build_text_button_style(b: BootstyleBuilderTTk, ttk_style: str, accent: str = None, **options):
    """
    Configure the text button style.

    Style options include:
        * icon
        * icon_only
        * anchor
    """
    anchor = options.get('anchor', 'center')
    accent_token = accent or 'foreground'
    surface_token = options.get('surface', 'content')
    density = options.get('density', 'default')
    icon_only = options.get('icon_only', False)
    image_key = f'button_{normalize_button_density(density)}'

    surface = b.color(surface_token)
    foreground_normal = b.color(accent_token) if accent else b.on_color(surface)
    foreground_disabled = b.disabled('text', surface)

    # button element images
    normal_img = recolor_element_image(image_key, surface, surface, surface, surface)
    focused_img = recolor_element_image(image_key, surface, surface, surface, surface)
    disabled_img = recolor_element_image(image_key, surface, surface, surface, surface)

    b.create_style_element_image(
        ElementImage(
            f'{ttk_style}.Button.border', normal_img.image, sticky="nsew",
            border=normal_img.meta.border, padding=normal_img.meta.border).state_specs(
            [
                ('disabled', disabled_img.image),
                ('focus', focused_img.image),
            ])
    )

    b.create_style_layout(
        ttk_style,
        button_layout(ttk_style),
    )

    padding = button_padding(b, icon_only, density)

    b.configure_style(
        ttk_style,
        background=surface,
        foreground=foreground_normal,
        relief='flat',
        stipple="gray12",
        padding=padding,
        anchor=anchor,
        font=button_font(density)
    )

    from ttkbootstrap.style.typography import Font

    state_spec = dict(
        font=[('background focus', Font('body[bold]'))],
        foreground=[
            ('disabled', foreground_disabled),
            ('', foreground_normal)
        ], background=[('disabled', surface)]
    )

    state_spec = apply_icon_mapping(b, options, state_spec, icon_size(icon_only, density))

    b.map_style(ttk_style, **state_spec)


@BootstyleBuilderTTk.register_builder('link', 'TButton')
def build_link_button_style(b: BootstyleBuilderTTk, ttk_style: str, accent: str = None, **options):
    """
    Configure the link button style.

    Style options include:
        * icon
        * icon_only
        * anchor
    """
    anchor = options.get('anchor', 'center')
    accent_token = accent or 'primary'
    surface_token = options.get('surface', 'content')
    density = options.get('density', 'default')
    icon_only = options.get('icon_only', False)
    image_key = f'button_{normalize_button_density(density)}'

    surface = b.color(surface_token)
    foreground_normal = b.color(accent_token)
    foreground_disabled = b.disabled('text', surface)

    # button element images - all transparent for link style
    normal_img = recolor_element_image(image_key, surface, surface, surface, surface)
    focused_img = recolor_element_image(image_key, surface, surface, surface, surface)
    disabled_img = recolor_element_image(image_key, surface, surface, surface, surface)

    b.create_style_element_image(
        ElementImage(
            f'{ttk_style}.Button.border', normal_img.image, sticky="nsew",
            border=normal_img.meta.border, padding=normal_img.meta.border).state_specs(
            [
                ('disabled', disabled_img.image),
                ('focus', focused_img.image),
            ])
    )

    b.create_style_layout(
        ttk_style,
        button_layout(ttk_style),
    )

    b.configure_style(
        ttk_style,
        background=surface,
        foreground=foreground_normal,
        relief='flat',
        stipple="gray12",
        padding=button_padding(b, icon_only, density),
        anchor=anchor,
        font=button_font(density)
    )

    state_spec = dict(
        font=[
            ("active !disabled", "hyperlink"),
            ("background focus !disabled", "hyperlink"),
            ("", button_font(density))],
        cursor=[('', 'hand2')],
        foreground=[
            ('disabled', foreground_disabled),
            ('', foreground_normal)
        ], background=[('disabled', surface)]
    )

    state_spec = apply_icon_mapping(b, options, state_spec, icon_size(icon_only, density))

    b.map_style(ttk_style, **state_spec)


@BootstyleBuilderTTk.register_builder('ghost', 'TButton')
def build_ghost_button_style(b: BootstyleBuilderTTk, ttk_style: str, accent: str = None, **options):
    """
    Configure the ghost button style.

    Style options include:
        * icon
        * icon_only
        * anchor
    """
    anchor = options.get('anchor', 'center')
    accent_token = accent or 'secondary'
    surface_token = options.get('surface', 'content')
    density = options.get('density', 'default')
    icon_only = options.get('icon_only', False)
    image_key = f'button_{normalize_button_density(density)}'

    surface = b.color(surface_token)

    accent_color = b.color(accent_token)
    normal = surface
    hovered = focused = pressed = b.subtle(accent_token, surface)
    focused_ring = b.focus_ring(accent_color, surface)

    foreground_normal = accent_color if accent else b.on_color(surface)
    foreground_disabled = b.disabled('text', surface)

    # button element images
    normal_img = recolor_element_image(image_key, normal, normal, surface, surface)
    pressed_img = recolor_element_image(image_key, pressed, surface, surface, surface)
    hovered_img = recolor_element_image(image_key, hovered, surface, surface, surface)
    focused_img = recolor_element_image(image_key, focused, accent_color, focused_ring, surface)
    focused_hovered_img = recolor_element_image(image_key, hovered, accent_color, focused_ring, surface)
    focused_pressed_img = recolor_element_image(image_key, pressed, accent_color, focused_ring, surface)
    disabled_img = recolor_element_image(image_key, surface, surface, surface, surface)

    b.create_style_element_image(
        ElementImage(
            f'{ttk_style}.Button.border', normal_img.image, sticky="nsew",
            border=normal_img.meta.border, padding=normal_img.meta.border).state_specs(
            [
                ('disabled', disabled_img.image),
                ('background focus pressed', focused_pressed_img.image),
                ('background focus hover', focused_hovered_img.image),
                ('background focus', focused_img.image),
                ('pressed', pressed_img.image),
                ('hover', hovered_img.image),
            ])
    )

    b.create_style_layout(
        ttk_style,
        button_layout(ttk_style),
    )

    b.configure_style(
        ttk_style,
        background=surface,
        foreground=foreground_normal,
        relief='flat',
        stipple="gray12",
        padding=button_padding(b, icon_only, density),
        anchor=anchor,
        font=button_font(density)
    )

    state_spec = dict(
        foreground=[('disabled', foreground_disabled), ('', foreground_normal)],
        background=[('disabled', surface)]
    )

    state_spec = apply_icon_mapping(b, options, state_spec, icon_size(icon_only, density))

    b.map_style(ttk_style, **state_spec)


@BootstyleBuilderTTk.register_builder('selectbox_item', 'TButton')
def build_selectbox_item_button_style(b: BootstyleBuilderTTk, ttk_style: str, accent: str = None, **options):
    """Configure the style for selectbox dropdown items with selected state support.

    Style options include:
        * icon
        * icon_only
        * anchor
    """
    anchor = options.get('anchor', 'w')
    accent_token = accent or 'primary'
    surface_token = options.get('surface', 'content')

    surface = b.color(surface_token)
    on_surface = b.on_color(surface)
    on_disabled = b.disabled('text', surface)

    active = b.elevate(surface, 1)
    selected = b.color(accent_token)
    on_selected = b.on_color(selected)

    b.configure_style(
        ttk_style,
        background=surface,
        foreground=on_surface,
        relief='flat',
        stipple='gray12',
        padding=(6, 3),
        anchor=anchor,
        font='body',
        focuscolor=''
    )

    state_spec = dict(
        foreground=[
            ('disabled', on_disabled),
            ('selected !disabled', on_selected),
            ('pressed', on_selected),
            ('', on_surface)],
        background=[
            ('selected !disabled', selected),
            ('pressed !disabled', selected),
            ('active !disabled', active),
            ('', surface)
        ]
    )

    b.map_style(ttk_style, **state_spec)
