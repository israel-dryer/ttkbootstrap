"""Menubutton widget style builders.

This module contains style builders for ttk.Menubutton widgets and variants.
"""

from __future__ import annotations

from ttkbootstrap_icons_bs import BootstrapIcon
from ttkbootstrap.style.bootstyle_builder_ttk import BootstyleBuilderTTk
from ttkbootstrap.style.element import Element, ElementImage
from ttkbootstrap.style.utility import create_transparent_image, recolor_element_image
from ttkbootstrap.style.builders.utils import (
    apply_icon_mapping,
    button_font,
    icon_size,
    normalize_button_density,
)


def _menubutton_layout(ttk_style: str, show_dropdown: bool = True) -> Element:
    """Create the layout for a menubutton."""
    children = [Element("Menubutton.label", sticky="nsew", side="left")]

    if show_dropdown:
        children.extend(
            [
                Element(f"{ttk_style}.chevron", side="right", sticky=""),
                Element(f'{ttk_style}.spacer', side="right", sticky=""),
            ])

    return Element(f"{ttk_style}.border", sticky="nsew").children(
        [
            Element("Menubutton.padding", sticky="nsew").children(children)
        ])


def _chevron_size(density: str) -> int:
    """Get chevron icon size based on density."""
    return 14 if density == 'compact' else 18


def _create_chevron_images(
        b: BootstyleBuilderTTk, ttk_style: str, foreground: str, disabled: str, active: str = None,
        icon_name: str = 'caret-down-fill', density: str = 'default'):
    """Create chevron icon images for dropdown indicator.

    Args:
        b: Style builder instance
        ttk_style: TTK style name
        foreground: Normal foreground color
        disabled: Disabled color
        active: Active/hover color (optional)
        icon_name: Name of the icon to use (default: 'caret-down-fill')
        density: Button density ('default' or 'compact')
    """
    size = _chevron_size(density)
    normal_chevron = BootstrapIcon(icon_name, size=size, color=foreground).image
    disabled_chevron = BootstrapIcon(icon_name, size=size, color=disabled).image

    state_specs = [
        ('disabled', disabled_chevron),
    ]

    if active:
        active_chevron = BootstrapIcon(icon_name, size=size, color=active).image
        state_specs.extend(
            [
                ('background focus !disabled', active_chevron),
                ('hover !disabled', active_chevron),
                ('pressed !disabled', active_chevron),
            ])

    state_specs.append(('', normal_chevron))

    b.create_style_element_image(
        ElementImage(f'{ttk_style}.chevron', normal_chevron).state_specs(state_specs)
    )


def _create_spacer(b: BootstyleBuilderTTk, ttk_style: str, density: str = 'default'):
    """Create a small spacer element."""
    width = 6 if density == 'compact' else 8
    spacer_img = create_transparent_image(width, 1)
    b.create_style_element_image(ElementImage(f'{ttk_style}.spacer', spacer_img, sticky="ew", width=width))


def _menubutton_padding(b: BootstyleBuilderTTk, icon_only: bool, density: str) -> int | tuple[int, ...]:
    """Calculate menubutton padding based on options."""
    if icon_only:
        return 0
    if density == 'compact':
        return b.scale((6, 0, 3, 0))
    return b.scale((8, 0, 4, 0))


@BootstyleBuilderTTk.register_builder('solid', 'TMenubutton')
@BootstyleBuilderTTk.register_builder('default', 'TMenubutton')
def build_solid_menubutton_style(b: BootstyleBuilderTTk, ttk_style: str, accent: str = None, **options):
    """Configure the solid menubutton style.

    Style options include:
        * show_dropdown_button: Show/hide the dropdown chevron (default: True)
        * dropdown_button_icon: Icon name for the dropdown indicator (default: 'caret-down-fill')
        * icon: Optional icon specification for the button content
        * icon_only: Whether the button shows only an icon
        * density: Button density ('default' or 'compact')
    """
    accent_token = accent or 'primary'
    surface_token = options.get('surface', 'content')
    density = options.get('density', 'default')
    show_dropdown = options.get('show_dropdown_button', True)
    dropdown_icon = options.get('dropdown_button_icon', 'caret-down-fill')
    icon_only = options.get('icon_only', False)
    image_key = f'button_{normalize_button_density(density)}'

    surface = b.color(surface_token)
    normal = b.color(accent_token)
    foreground = b.on_color(normal)
    pressed = b.pressed(normal)
    hovered = focused = b.active(normal)
    focused_border = b.focus_border(normal)
    disabled = b.disabled()
    focused_ring = b.focus_ring(normal, surface)
    foreground_disabled = b.disabled('text', disabled)

    normal_img = recolor_element_image(image_key, normal, normal, surface)
    pressed_img = recolor_element_image(image_key, pressed, pressed, surface)
    hovered_img = recolor_element_image(image_key, hovered, hovered, surface)
    focused_img = recolor_element_image(image_key, focused, focused_border, focused_ring)
    focused_hovered_img = recolor_element_image(image_key, hovered, focused_border, focused_ring)
    focused_pressed_img = recolor_element_image(image_key, pressed, focused_border, focused_ring)
    disabled_img = recolor_element_image(image_key, disabled, disabled, surface, surface)

    if show_dropdown:
        _create_spacer(b, ttk_style, density)
        _create_chevron_images(b, ttk_style, foreground, foreground_disabled, icon_name=dropdown_icon, density=density)

    b.create_style_element_image(
        ElementImage(
            f'{ttk_style}.border', normal_img.image, sticky="nsew",
            border=normal_img.meta.border, padding=normal_img.meta.border
        ).state_specs(
            [
                ('disabled', disabled_img.image),
                ('background focus pressed', focused_pressed_img.image),
                ('background focus hover', focused_hovered_img.image),
                ('background focus', focused_img.image),
                ('pressed', pressed_img.image),
                ('hover', hovered_img.image),
            ]))

    b.create_style_layout(ttk_style, _menubutton_layout(ttk_style, show_dropdown))

    b.configure_style(
        ttk_style,
        background=surface,
        foreground=foreground,
        stipple="gray12",
        relief='flat',
        font=button_font(density),
        takefocus=True,
        padding=_menubutton_padding(b, icon_only, density),
        anchor="center" if icon_only else "w"
    )

    state_spec = dict(
        foreground=[('disabled', foreground_disabled), ('', foreground)],
        background=[('disabled', disabled)]
    )

    state_spec = apply_icon_mapping(b, options, state_spec, icon_size(icon_only, density))
    b.map_style(ttk_style, **state_spec)


@BootstyleBuilderTTk.register_builder('outline', 'TMenubutton')
def build_outline_menubutton_style(b: BootstyleBuilderTTk, ttk_style: str, accent: str = None, **options):
    """Configure the outline menubutton style.

    Style options include:
        * show_dropdown_button: Show/hide the dropdown chevron (default: True)
        * dropdown_button_icon: Icon name for the dropdown indicator (default: 'caret-down-fill')
        * icon: Optional icon specification for the button content
        * icon_only: Whether the button shows only an icon
        * density: Button density ('default' or 'compact')
    """
    accent_token = accent or 'primary'
    surface_token = options.get('surface', 'content')
    density = options.get('density', 'default')
    show_dropdown = options.get('show_dropdown_button', True)
    dropdown_icon = options.get('dropdown_button_icon', 'caret-down-fill')
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

    if show_dropdown:
        _create_spacer(b, ttk_style, density)
        _create_chevron_images(b, ttk_style, foreground_normal, disabled, foreground_active, dropdown_icon, density)

    b.create_style_element_image(
        ElementImage(
            f'{ttk_style}.border', normal_img.image, sticky="nsew",
            border=normal_img.meta.border, padding=normal_img.meta.border
        ).state_specs(
            [
                ('disabled', disabled_img.image),
                ('background focus pressed', focused_pressed_img.image),
                ('background focus hover', focused_hovered_img.image),
                ('background focus', focused_img.image),
                ('pressed', pressed_img.image),
                ('hover', hovered_img.image),
            ]))

    b.create_style_layout(ttk_style, _menubutton_layout(ttk_style, show_dropdown))

    b.configure_style(
        ttk_style,
        background=surface,
        foreground=foreground_normal,
        relief='flat',
        stipple="gray12",
        font=button_font(density),
        takefocus=True,
        padding=_menubutton_padding(b, icon_only, density),
        anchor="center" if icon_only else "w"
    )

    state_spec = dict(
        foreground=[
            ('disabled', foreground_disabled),
            ('background focus', foreground_active),
            ('hover', foreground_active),
            ('', foreground_normal)
        ],
        background=[('disabled', surface)]
    )

    state_spec = apply_icon_mapping(b, options, state_spec, icon_size(icon_only, density))
    b.map_style(ttk_style, **state_spec)


@BootstyleBuilderTTk.register_builder('text', 'TMenubutton')
def build_text_menubutton_style(b: BootstyleBuilderTTk, ttk_style: str, accent: str = None, **options):
    """Configure the text menubutton style.

    Style options include:
        * show_dropdown_button: Show/hide the dropdown chevron (default: True)
        * dropdown_button_icon: Icon name for the dropdown indicator (default: 'caret-down-fill')
        * icon: Optional icon specification for the button content
        * icon_only: Whether the button shows only an icon
        * density: Button density ('default' or 'compact')
    """
    accent_token = accent or 'foreground'
    surface_token = options.get('surface', 'content')
    density = options.get('density', 'default')
    show_dropdown = options.get('show_dropdown_button', True)
    dropdown_icon = options.get('dropdown_button_icon', 'caret-down-fill')
    icon_only = options.get('icon_only', False)
    image_key = f'button_{normalize_button_density(density)}'

    surface = b.color(surface_token)
    foreground_normal = b.color(accent_token)
    foreground_disabled = b.disabled('text', surface)

    # button element images
    normal_img = recolor_element_image(image_key, surface, surface, surface, surface)
    focused_img = recolor_element_image(image_key, surface, surface, surface, surface)
    disabled_img = recolor_element_image(image_key, surface, surface, surface, surface)

    if show_dropdown:
        _create_spacer(b, ttk_style, density)
        _create_chevron_images(b, ttk_style, foreground_normal, foreground_disabled, icon_name=dropdown_icon, density=density)

    b.create_style_element_image(
        ElementImage(
            f'{ttk_style}.border', normal_img.image, sticky="nsew",
            border=normal_img.meta.border, padding=normal_img.meta.border
        ).state_specs(
            [
                ('disabled', disabled_img.image),
                ('focus', focused_img.image),
            ]))

    b.create_style_layout(ttk_style, _menubutton_layout(ttk_style, show_dropdown))

    b.configure_style(
        ttk_style,
        background=surface,
        foreground=foreground_normal,
        relief='flat',
        stipple="gray12",
        font=button_font(density),
        takefocus=True,
        padding=_menubutton_padding(b, icon_only, density),
        anchor="center" if icon_only else "w"
    )

    from ttkbootstrap.style.typography import Font

    state_spec = dict(
        font=[('background focus', Font('body[bold]'))],
        foreground=[
            ('disabled', foreground_disabled),
            ('', foreground_normal)
        ],
        background=[('disabled', surface)]
    )

    state_spec = apply_icon_mapping(b, options, state_spec, icon_size(icon_only, density))
    b.map_style(ttk_style, **state_spec)


@BootstyleBuilderTTk.register_builder('ghost', 'TMenubutton')
def build_ghost_menubutton_style(b: BootstyleBuilderTTk, ttk_style: str, accent: str = None, **options):
    """Configure the ghost menubutton style.

    Style options include:
        * show_dropdown_button: Show/hide the dropdown chevron (default: True)
        * dropdown_button_icon: Icon name for the dropdown indicator (default: 'caret-down-fill')
        * icon: Optional icon specification for the button content
        * icon_only: Whether the button shows only an icon
        * density: Button density ('default' or 'compact')
    """
    accent_token = accent or 'secondary'
    surface_token = options.get('surface', 'content')
    density = options.get('density', 'default')
    show_dropdown = options.get('show_dropdown_button', True)
    dropdown_icon = options.get('dropdown_button_icon', 'caret-down-fill')
    icon_only = options.get('icon_only', False)
    image_key = f'button_{normalize_button_density(density)}'

    surface = b.color(surface_token)

    normal = surface
    pressed = b.subtle(accent_token, surface)
    focused = hovered = pressed
    focused_ring = b.focus_ring(focused, surface)

    foreground_normal = b.color(accent_token)
    foreground_disabled = b.disabled('text', surface)

    # button element images
    normal_img = recolor_element_image(image_key, normal, normal, surface, surface)
    pressed_img = recolor_element_image(image_key, pressed, surface, surface, surface)
    hovered_img = recolor_element_image(image_key, hovered, surface, surface, surface)
    focused_img = recolor_element_image(image_key, focused, foreground_normal, focused_ring, surface)
    focused_hovered_img = recolor_element_image(image_key, hovered, foreground_normal, focused_ring, surface)
    focused_pressed_img = recolor_element_image(image_key, pressed, foreground_normal, focused_ring, surface)
    disabled_img = recolor_element_image(image_key, surface, surface, surface, surface)

    if show_dropdown:
        _create_spacer(b, ttk_style, density)
        _create_chevron_images(b, ttk_style, foreground_normal, foreground_disabled, icon_name=dropdown_icon, density=density)

    b.create_style_element_image(
        ElementImage(
            f'{ttk_style}.border', normal_img.image, sticky="nsew",
            border=normal_img.meta.border, padding=normal_img.meta.border
        ).state_specs(
            [
                ('disabled', disabled_img.image),
                ('background focus pressed', focused_pressed_img.image),
                ('background focus hover', focused_hovered_img.image),
                ('background focus', focused_img.image),
                ('pressed', pressed_img.image),
                ('hover', hovered_img.image),
            ]))

    b.create_style_layout(ttk_style, _menubutton_layout(ttk_style, show_dropdown))

    b.configure_style(
        ttk_style,
        background=surface,
        foreground=foreground_normal,
        relief='flat',
        stipple="gray12",
        font=button_font(density),
        takefocus=True,
        padding=_menubutton_padding(b, icon_only, density),
        anchor="center" if icon_only else "w"
    )

    state_spec = dict(
        foreground=[('disabled', foreground_disabled), ('', foreground_normal)],
        background=[('disabled', surface)]
    )

    state_spec = apply_icon_mapping(b, options, state_spec, icon_size(icon_only, density))
    b.map_style(ttk_style, **state_spec)
