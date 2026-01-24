"""Style builders for NavigationView widget components.

This module provides navigation-specific styling with selection indicator bars.
"""

from __future__ import annotations

from ttkbootstrap.style.bootstyle_builder_ttk import BootstyleBuilderTTk
from ttkbootstrap.style.element import Element, ElementImage
from ttkbootstrap.style.utility import recolor_element_image
from ttkbootstrap.style.builders.utils import apply_icon_mapping
from ttkbootstrap.style.builders.toolbutton import (
    toolbutton_layout, button_padding, button_font, icon_size, normalize_button_density
)


@BootstyleBuilderTTk.register_builder('default', 'NavigationView.TFrame')
def build_navigationview_frame_style(b: BootstyleBuilderTTk, ttk_style: str, accent: str = None, **options):
    """Build NavigationView frame style for group expanders.

    Uses standard button assets (no selection indicator needed since
    groups don't get selected, only their child items do).
    """
    accent_token = accent or 'primary'
    surface_token = options.get('surface', 'content')
    density = options.get('density', 'default')
    image_key = f'button_{density}'

    surface = b.color(surface_token)
    surface_hover = b.color(f'{surface_token}_hover') if b.colors.get(f'{surface_token}_hover') else b.subtle('secondary', surface)
    surface_pressed = b.pressed(surface_hover)

    disabled = b.disabled()

    normal_img = recolor_element_image(image_key, surface, surface, surface, surface)
    hover_img = recolor_element_image(image_key, surface_hover, surface_hover, surface, surface)
    pressed_img = recolor_element_image(image_key, surface_pressed, surface_pressed, surface, surface)
    disabled_img = recolor_element_image(image_key, disabled, disabled, surface, surface)

    b.create_style_element_image(
        ElementImage(
            f'{ttk_style}.border', normal_img.image, sticky="nsew",
            border=normal_img.meta.border, padding=normal_img.meta.border
        ).state_specs(
            [
                ('disabled', disabled_img.image),
                ('pressed', pressed_img.image),
                ('hover', hover_img.image),
                ('', normal_img.image)
            ]))

    # Create layout to use the image-based border
    b.create_style_layout(
        ttk_style,
        Element(f'{ttk_style}.border', sticky="nsew")
    )

    b.configure_style(
        ttk_style,
        background=surface,
        relief='flat',
    )


@BootstyleBuilderTTk.register_builder('default', 'NavigationView.TLabel')
def build_navigationview_label_style(b: BootstyleBuilderTTk, ttk_style: str, accent: str = None, **options):
    """Build NavigationView label style with state-aware foreground colors.

    Matches the ghost Toolbutton foreground color behavior.
    """
    accent_token = accent or 'primary'
    surface_token = options.get('surface', 'content')

    surface = b.color(surface_token)
    surface_hover = b.color(f'{surface_token}_hover') if b.colors.get(f'{surface_token}_hover') else b.subtle('secondary', surface)
    surface_pressed = b.pressed(surface_hover)
    on_surface = b.on_color(surface)

    accent_color = b.color(accent_token)
    active = b.subtle(accent_token, surface)

    on_disabled = b.disabled('text', surface)

    b.configure_style(
        ttk_style,
        background=surface,
        foreground=on_surface,
        relief='flat',
        font='body'
    )

    foreground_state_map = [
        ('disabled', on_disabled),
        ('selected', accent_color),
        ('', on_surface)
    ]

    background_state_map = [
        ('selected', active),
        ('disabled', surface),
        ('pressed !selected', surface_pressed),
        ('hover !selected', surface_hover),
        ('', surface)
    ]

    state_spec = dict(foreground=foreground_state_map, background=background_state_map)
    state_spec = apply_icon_mapping(b, options, state_spec)

    b.map_style(ttk_style, **state_spec)


@BootstyleBuilderTTk.register_builder('navigation', 'Toolbutton')
def build_navigation_toolbutton_style(b: BootstyleBuilderTTk, ttk_style: str, accent: str = None, **options):
    """Build navigation Toolbutton style with selection indicator.

    Uses nav-button assets with a left-side selection indicator bar
    that shows the accent color when selected.
    """
    accent_token = accent or 'primary'
    surface_token = options.get('surface', 'content')
    density = options.get('density', 'default')
    icon_only = options.get('icon_only', False)
    anchor = options.get('anchor', 'center' if icon_only else 'w')
    # Use lighter indicator assets for icon-only buttons
    asset_prefix = 'nav_icon_button' if icon_only else 'nav_button'
    image_key = f'{asset_prefix}_{normalize_button_density(density)}'

    surface = b.color(surface_token)
    surface_hover = b.color(f'{surface_token}_hover') if b.colors.get(f'{surface_token}_hover') else b.subtle('secondary', surface)
    surface_pressed = b.pressed(surface_hover)
    on_surface = b.on_color(surface)

    active = b.subtle(accent_token, surface)
    accent_color = b.color(accent_token)
    accent_pressed = b.pressed(active)

    disabled = b.disabled()
    on_disabled = b.disabled('text', disabled)

    # Normal states: indicator hidden (same color as button background)
    normal_img = recolor_element_image(image_key, surface, surface, surface, surface)
    hover_img = recolor_element_image(image_key, surface_hover, surface_hover, surface_hover, surface)
    pressed_img = recolor_element_image(image_key, surface_pressed, surface_pressed, surface_pressed, surface)

    # Selected states: indicator visible (accent color)
    selected_img = recolor_element_image(image_key, active, active, accent_color, surface)
    selected_hover_img = recolor_element_image(image_key, active, active, accent_color, surface)
    selected_pressed_img = recolor_element_image(image_key, accent_pressed, accent_pressed, accent_color, surface)

    disabled_img = recolor_element_image(image_key, disabled, disabled, disabled, surface)

    b.create_style_element_image(
        ElementImage(
            f'{ttk_style}.border', normal_img.image, sticky="nsew",
            border=normal_img.meta.border, padding=normal_img.meta.border
        ).state_specs(
            [
                ('disabled', disabled_img.image),
                ('selected pressed', selected_pressed_img.image),
                ('selected hover', selected_hover_img.image),
                ('selected', selected_img.image),
                ('pressed', pressed_img.image),
                ('hover', hover_img.image),
                ('', normal_img.image)
            ]))

    b.create_style_layout(
        ttk_style,
        toolbutton_layout(ttk_style),
    )

    b.configure_style(
        ttk_style,
        background=surface,
        foreground=on_surface,
        relief='flat',
        padding=button_padding(b, icon_only, density),
        anchor=anchor,
        font=button_font(density)
    )

    state_spec = dict(
        foreground=[
            ('disabled', on_disabled),
            ('selected', accent_color),
            ('', on_surface)
        ],
    )
    state_spec = apply_icon_mapping(b, options, state_spec, icon_size(icon_only, density))

    b.map_style(ttk_style, **state_spec)


@BootstyleBuilderTTk.register_builder('default', 'NavigationButton.TFrame')
def build_navigationbutton_frame_style(b: BootstyleBuilderTTk, ttk_style: str, accent: str = None, **options):
    """Build NavigationButton frame style with selection indicator.

    Uses nav-button assets with a left-side selection indicator bar
    that shows the accent color when selected. This is the container
    frame for the composite navigation button.
    """
    accent_token = accent or 'primary'
    surface_token = options.get('surface', 'content')
    density = options.get('density', 'default')
    icon_only = options.get('icon_only', False)
    # Use lighter indicator assets for icon-only (compact) mode
    asset_prefix = 'nav_icon_button' if icon_only else 'nav_button'
    image_key = f'{asset_prefix}_{normalize_button_density(density)}'

    surface = b.color(surface_token)
    surface_hover = b.color(f'{surface_token}_hover') if b.colors.get(f'{surface_token}_hover') else b.subtle('secondary', surface)
    surface_pressed = b.pressed(surface_hover)

    active = b.subtle(accent_token, surface)
    accent_color = b.color(accent_token)
    accent_pressed = b.pressed(active)

    disabled = b.disabled()

    # Normal states: indicator hidden (same color as button background)
    normal_img = recolor_element_image(image_key, surface, surface, surface, surface)
    hover_img = recolor_element_image(image_key, surface_hover, surface_hover, surface_hover, surface)
    pressed_img = recolor_element_image(image_key, surface_pressed, surface_pressed, surface_pressed, surface)

    # Selected states: indicator visible (accent color)
    selected_img = recolor_element_image(image_key, active, active, accent_color, surface)
    selected_hover_img = recolor_element_image(image_key, active, active, accent_color, surface)
    selected_pressed_img = recolor_element_image(image_key, accent_pressed, accent_pressed, accent_color, surface)

    disabled_img = recolor_element_image(image_key, disabled, disabled, disabled, surface)

    b.create_style_element_image(
        ElementImage(
            f'{ttk_style}.border', normal_img.image, sticky="ew",
            border=normal_img.meta.border
        ).state_specs(
            [
                ('disabled', disabled_img.image),
                ('selected pressed', selected_pressed_img.image),
                ('selected hover', selected_hover_img.image),
                ('selected', selected_img.image),
                ('pressed', pressed_img.image),
                ('hover', hover_img.image),
                ('', normal_img.image)
            ]))

    # Create layout to use the image-based border
    b.create_style_layout(
        ttk_style,
        Element(f'{ttk_style}.border', sticky="nsew")
    )

    b.configure_style(
        ttk_style,
        background=surface,
        relief='flat',
    )


@BootstyleBuilderTTk.register_builder('default', 'NavigationButton.TLabel')
def build_navigationbutton_label_style(b: BootstyleBuilderTTk, ttk_style: str, accent: str = None, **options):
    """Build NavigationButton label style with state-aware colors.

    Labels inside the navigation button container that respond to
    hover, pressed, and selected states.
    """
    accent_token = accent or 'primary'
    surface_token = options.get('surface', 'content')
    icon_only = options.get('icon_only', False)
    density = options.get('density', 'default')

    surface = b.color(surface_token)
    surface_hover = b.color(f'{surface_token}_hover') if b.colors.get(f'{surface_token}_hover') else b.subtle('secondary', surface)
    surface_pressed = b.pressed(surface_hover)
    on_surface = b.on_color(surface)

    accent_color = b.color(accent_token)
    active = b.subtle(accent_token, surface)
    active_pressed = b.pressed(active)

    on_disabled = b.disabled('text', surface)

    b.configure_style(
        ttk_style,
        background=surface,
        foreground=on_surface,
        relief='flat',
        font='body'
    )

    foreground_state_map = [
        ('disabled', on_disabled),
        ('selected', accent_color),
        ('', on_surface)
    ]

    background_state_map = [
        ('disabled', surface),
        ('selected pressed', active_pressed),
        ('selected', active),
        ('pressed !selected', surface_pressed),
        ('hover !selected', surface_hover),
        ('', surface)
    ]

    state_spec = dict(foreground=foreground_state_map, background=background_state_map)
    state_spec = apply_icon_mapping(b, options, state_spec, icon_size(icon_only, density))

    b.map_style(ttk_style, **state_spec)