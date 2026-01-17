"""Style builders for NavigationView widget components.

This module provides image-based styling for NavigationView group headers
that matches the RadioToggle/Toolbutton ghost style for visual consistency.
"""

from __future__ import annotations

from ttkbootstrap.style.bootstyle_builder_ttk import BootstyleBuilderTTk
from ttkbootstrap.style.element import Element, ElementImage
from ttkbootstrap.style.utility import recolor_element_image
from ttkbootstrap.style.builders.utils import apply_icon_mapping


@BootstyleBuilderTTk.register_builder('default', 'NavigationView.TFrame')
def build_navigationview_frame_style(b: BootstyleBuilderTTk, ttk_style: str, accent: str = None, **options):
    """Build NavigationView frame style with image-based rounded background.

    Uses the same image-based approach as Toolbutton ghost variant for consistent
    visual appearance between navigation items and group headers.
    """
    accent_token = accent or 'primary'
    surface_token = options.get('surface', 'content')
    density = options.get('density', 'default')
    image_key = f'button_{density}'

    surface = b.color(surface_token)

    active = b.subtle(accent_token, surface)
    accent_color = b.color(accent_token)
    accent_pressed = b.pressed(active)
    accent_focus = b.focus(active)

    focus_ring = b.focus_ring(accent_focus, surface)
    disabled = b.disabled()

    normal_img = recolor_element_image(image_key, surface, surface, surface, surface)
    normal_focus_img = recolor_element_image(image_key, surface, accent_color, focus_ring, surface)
    hover_img = recolor_element_image(image_key, active, active, surface, surface)
    selected_img = recolor_element_image(image_key, active, active, surface, surface)
    selected_pressed_img = recolor_element_image(image_key, accent_pressed, accent_pressed, surface, surface)
    selected_focus_img = recolor_element_image(image_key, accent_focus, accent_color, focus_ring, surface)

    disabled_img = recolor_element_image(image_key, disabled, disabled, surface, surface)

    b.create_style_element_image(
        ElementImage(
            f'{ttk_style}.border', normal_img.image, sticky="nsew",
            border=normal_img.meta.border, padding=normal_img.meta.border
        ).state_specs(
            [
                ('disabled', disabled_img.image),
                ('pressed', hover_img.image),  # pressed shows hover-like background
                ('hover', hover_img.image),
                ('', normal_img.image)  # default is transparent
            ]))

    # Create layout to use the image-based border
    b.create_style_layout(
        ttk_style,
        Element(f'{ttk_style}.border', sticky="nsew", border=normal_img.meta.border)
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
    on_surface = b.color('secondary')

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
        ('pressed', accent_color),
        ('', on_surface)
    ]

    background_state_map = [
        ('selected', active),
        ('disabled', surface),
        ('pressed', active),
        ('hover', active),
        ('', surface)
    ]

    state_spec = dict(foreground=foreground_state_map, background=background_state_map)
    state_spec = apply_icon_mapping(b, options, state_spec)

    b.map_style(ttk_style, **state_spec)