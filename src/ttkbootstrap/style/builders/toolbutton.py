"""Toolbutton widget style builders.

This module contains style builders for ttk.Checkbutton and Radiobutton toolbutton variants.
"""

from __future__ import annotations

from ttkbootstrap.style.bootstyle_builder_ttk import BootstyleBuilderTTk
from ttkbootstrap.style.element import ElementImage
from ttkbootstrap.style.utility import recolor_element_image
from ttkbootstrap.style.builders.utils import (
    apply_icon_mapping,
    button_font,
    button_padding,
    icon_size,
    normalize_button_density,
    toolbutton_layout,
)


# The active styles are intentionally limited on toolbuttons to improve interaction
# and limit the number of images created for each style.


@BootstyleBuilderTTk.register_builder('default', 'Toolbutton')
@BootstyleBuilderTTk.register_builder('solid', 'Toolbutton')
def build_solid_toolbutton_style(b: BootstyleBuilderTTk, ttk_style: str, accent: str = None, **options):
    """
    Configure the button style.

    Style options include:
        * anchor
        * icon
        * icon_only
        * density
    """
    anchor = options.get('anchor', 'center')
    accent_token = accent or 'primary'
    surface_token = options.get('surface', 'content')
    density = options.get('density', 'default')
    icon_only = options.get('icon_only', False)
    image_key = f'button_{normalize_button_density(density)}'

    surface = b.color(surface_token)

    accent_color = b.color(accent_token)

    active = b.active(accent_color)
    accent_focus = b.focus(accent_color)
    on_accent = b.on_color(accent_color)

    selected = b.selected(accent_color)

    focus_ring = b.focus_ring(accent_focus, surface)
    disabled = b.disabled()
    on_disabled = b.disabled('text', disabled)

    normal_img = recolor_element_image(image_key, accent_color, accent_color, surface, surface)
    normal_focus_img = recolor_element_image(image_key, accent_color, accent_color, focus_ring, surface)
    active_img = recolor_element_image(image_key, active, active, surface, surface)
    selected_img = recolor_element_image(image_key, selected, selected, surface, surface)
    selected_focus_img = recolor_element_image(image_key, selected, selected, focus_ring, surface)

    disabled_img = recolor_element_image(image_key, disabled, disabled, surface, surface)

    b.create_style_element_image(
        ElementImage(
            f'{ttk_style}.border', normal_img.image, sticky="nsew",
            border=normal_img.meta.border, padding=normal_img.meta.border
        ).state_specs(
            [
                ('disabled', disabled_img.image),
                ('background pressed focus selected', selected_focus_img.image),
                ('pressed', selected_img.image),
                ('background focus selected', selected_focus_img.image),
                ('selected', selected_img.image),
                ('background focus !selected', normal_focus_img.image),
                ('background active !focus', active_img.image),
                ('', normal_img.image)
            ]))

    b.create_style_layout(
        ttk_style,
        toolbutton_layout(ttk_style),
    )

    b.configure_style(
        ttk_style,
        background=surface,
        foreground=on_accent,
        stipple="gray12",
        relief='flat',
        padding=button_padding(b, icon_only, density),
        anchor=anchor,
        font=button_font(density)
    )

    state_spec = dict(foreground=[('disabled', on_disabled), ('', on_accent)])
    state_spec = apply_icon_mapping(b, options, state_spec, icon_size(icon_only, density))

    b.map_style(ttk_style, **state_spec)


@BootstyleBuilderTTk.register_builder('outline', 'Toolbutton')
def build_outline_toolbutton_style(b: BootstyleBuilderTTk, ttk_style: str, accent: str = None, **options):
    """
    Configure the button style.

    Style options include:
        * anchor
        * icon
        * icon_only
        * density
    """
    anchor = options.get('anchor', 'center')
    accent_token = accent or 'primary'
    surface_token = options.get('surface', 'content')
    density = options.get('density', 'default')
    icon_only = options.get('icon_only', False)
    image_key = f'button_{normalize_button_density(density)}'

    surface = b.color(surface_token)
    accent_color = b.color(accent_token)
    accent_focus = b.focus(accent_color)
    on_accent = b.on_color(accent_color)

    focus_ring = b.focus_ring(accent_focus, surface)
    disabled = b.disabled()
    on_disabled = b.disabled('text', disabled)

    normal_img = recolor_element_image(image_key, surface, accent_color, surface, surface)
    normal_focus_img = recolor_element_image(image_key, surface, accent_focus, focus_ring, surface)
    selected_img = recolor_element_image(image_key, accent_color, accent_color, surface, surface)
    selected_focus_img = recolor_element_image(image_key, accent_color, accent_focus, focus_ring, surface)

    disabled_img = recolor_element_image(image_key, disabled, disabled, surface, surface)

    b.create_style_element_image(
        ElementImage(
            f'{ttk_style}.border', normal_img.image, sticky="nsew",
            border=normal_img.meta.border, padding=normal_img.meta.border
        ).state_specs(
            [
                ('disabled', disabled_img.image),
                ('background pressed selected focus', selected_focus_img.image),
                ('pressed', selected_img.image),
                ('background selected focus', selected_focus_img.image),
                ('selected', selected_img.image),
                ('background focus !selected', normal_focus_img.image),
                ('', normal_img.image)
            ]))

    b.create_style_layout(
        ttk_style,
        toolbutton_layout(ttk_style),
    )

    b.configure_style(
        ttk_style,
        background=surface,
        foreground=accent_color,
        stipple="gray12",
        relief='flat',
        padding=button_padding(b, icon_only, density),
        anchor=anchor,
        font=button_font(density)
    )

    state_spec = dict(
        foreground=[('disabled', on_disabled), ('selected !disabled', on_accent), ('pressed !disabled', on_accent),
                    ('', accent_color)],
    )
    state_spec = apply_icon_mapping(b, options, state_spec, icon_size(icon_only, density))

    b.map_style(ttk_style, **state_spec)


@BootstyleBuilderTTk.register_builder('ghost', 'Toolbutton')
def build_ghost_toolbutton_style(b: BootstyleBuilderTTk, ttk_style: str, accent: str = None, **options):
    """
    Configure the button style.

    Style options include:
        * anchor
        * icon
        * icon_only
        * density
    """
    anchor = options.get('anchor', 'center')
    accent_token = accent or 'secondary'
    surface_token = options.get('surface', 'content')
    density = options.get('density', 'default')
    icon_only = options.get('icon_only', False)
    image_key = f'button_{normalize_button_density(density)}'

    surface = b.color(surface_token)
    on_surface = b.color('foreground')

    active = b.subtle(accent_token, surface)
    accent_color = b.color(accent_token)
    accent_pressed = b.pressed(active)
    accent_focus = b.focus(active)

    focus_ring = b.focus_ring(accent_focus, surface)
    disabled = b.disabled()
    on_disabled = b.disabled('text', disabled)

    normal_img = recolor_element_image(image_key, surface, surface, surface, surface)
    normal_focus_img = recolor_element_image(image_key, surface, accent_color, focus_ring, surface)
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
                ('background pressed selected focus', selected_focus_img.image),
                ('pressed', selected_img.image),
                ('background selected focus', selected_focus_img.image),
                ('selected pressed', selected_pressed_img.image),
                ('selected', selected_img.image),
                ('background focus !selected', normal_focus_img.image),
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
        stipple="gray12",
        relief='flat',
        padding=button_padding(b, icon_only, density),
        anchor=anchor,
        font=button_font(density)
    )

    state_spec = dict(
        foreground=[
            ('disabled', on_disabled),
            ('selected', accent_color),
            ('pressed', accent_color),
            ('', on_surface)],
    )
    state_spec = apply_icon_mapping(b, options, state_spec, icon_size(icon_only, density))

    b.map_style(ttk_style, **state_spec)
