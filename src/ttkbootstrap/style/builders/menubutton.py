"""Menubutton widget style builders.

This module contains style builders for ttk.Menubutton widgets and variants.
"""

from __future__ import annotations

from ttkbootstrap_icons_bs import BootstrapIcon
from ttkbootstrap.style.bootstyle_builder_ttk import BootstyleBuilderTTk
from ttkbootstrap.style.element import Element, ElementImage
from ttkbootstrap.style.utility import create_transparent_image, recolor_image


def _menubutton_layout(ttk_style: str, show_dropdown: bool = True) -> Element:
    """Create the layout for a menubutton."""
    children = [Element("Menubutton.label", sticky="", side="left")]

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


def _create_chevron_images(
        b: BootstyleBuilderTTk, ttk_style: str, foreground: str, disabled: str, active: str = None,
        icon_name: str = 'caret-down-fill'):
    """Create chevron icon images for dropdown indicator.

    Args:
        b: Style builder instance
        ttk_style: TTK style name
        foreground: Normal foreground color
        disabled: Disabled color
        active: Active/hover color (optional)
        icon_name: Name of the icon to use (default: 'caret-down-fill')
    """
    normal_chevron = BootstrapIcon(icon_name, size=b.scale(18), color=foreground).image
    disabled_chevron = BootstrapIcon(icon_name, size=b.scale(18), color=disabled).image

    state_specs = [
        ('disabled', disabled_chevron),
    ]

    if active:
        active_chevron = BootstrapIcon(icon_name, size=b.scale(18), color=active).image
        state_specs.extend(
            [
                ('focus !disabled', active_chevron),
                ('hover !disabled', active_chevron),
                ('pressed !disabled', active_chevron),
            ])

    state_specs.append(('', normal_chevron))

    b.create_style_element_image(
        ElementImage(f'{ttk_style}.chevron', normal_chevron).state_specs(state_specs)
    )


def _create_spacer(b: BootstyleBuilderTTk, ttk_style: str):
    """Create a small spacer element."""
    spacer_img = create_transparent_image(b.scale(8), b.scale(1))
    b.create_style_element_image(ElementImage(f'{ttk_style}.spacer', spacer_img, sticky="ew", width=b.scale(8)))


def _apply_icon_mapping(b: BootstyleBuilderTTk, options: dict, state_spec: dict) -> dict:
    """Apply icon mapping if an icon is provided in options."""
    icon = options.get('icon')
    if icon is None:
        return state_spec

    icon = b.normalize_icon_spec(icon, b.scale(24))
    state_spec['image'] = b.map_stateful_icons(icon, state_spec['foreground'])
    return state_spec


@BootstyleBuilderTTk.register_builder('solid', 'TMenubutton')
@BootstyleBuilderTTk.register_builder('default', 'TMenubutton')
def build_solid_menubutton_style(b: BootstyleBuilderTTk, ttk_style: str, color: str = None, **options):
    """Configure the solid menubutton style.

    Style options include:
        * show_dropdown_button: Show/hide the dropdown chevron (default: True)
        * dropdown_button_icon: Icon name for the dropdown indicator (default: 'caret-down-fill')
        * icon: Optional icon specification for the button content
    """
    accent_token = color or 'primary'
    surface_token = options.get('surface_color', 'background')
    show_dropdown = options.get('show_dropdown_button', True)
    dropdown_icon = options.get('dropdown_button_icon', 'caret-down-fill')
    icon_only = options.get('icon_only', False)

    surface = b.color(surface_token)
    normal = b.color(accent_token)
    foreground = b.on_color(normal)
    pressed = b.pressed(normal)
    hovered = focused = b.active(normal)
    focused_border = b.focus_border(normal)
    disabled = b.disabled()
    focused_ring = b.focus_ring(normal, surface)
    foreground_disabled = b.disabled('text', disabled)

    normal_img = recolor_image('button', normal, normal, surface)
    pressed_img = recolor_image('button', pressed, pressed, surface)
    hovered_img = recolor_image('button', hovered, hovered, surface)
    focused_img = recolor_image('button', focused, focused_border, focused_ring)
    focused_hovered_img = recolor_image('button', hovered, focused_border, focused_ring)
    focused_pressed_img = recolor_image('button', pressed, focused_border, focused_ring)
    disabled_img = recolor_image('button', disabled, disabled, surface, surface)

    if show_dropdown:
        _create_spacer(b, ttk_style)
        _create_chevron_images(b, ttk_style, foreground, disabled, icon_name=dropdown_icon)

    b.create_style_element_image(
        ElementImage(
            f'{ttk_style}.border', normal_img, sticky="nsew", border=b.scale(10),
            padding=b.scale(10)).state_specs(
            [
                ('disabled', disabled_img),
                ('focus pressed', focused_pressed_img),
                ('focus hover', focused_hovered_img),
                ('focus', focused_img),
                ('pressed', pressed_img),
                ('hover', hovered_img),
            ]))

    b.create_style_layout(ttk_style, _menubutton_layout(ttk_style, show_dropdown))

    b.configure_style(
        ttk_style,
        background=surface,
        foreground=foreground,
        stipple="gray12",
        relief='flat',
        font="body",
        takefocus=True,
        padding=0 if icon_only else b.scale((8, 0, 4, 0)),
        anchor="center" if icon_only else "w"
    )

    state_spec = dict(
        foreground=[('disabled', foreground_disabled), ('', foreground)],
        background=[('disabled', disabled)]
    )

    state_spec = _apply_icon_mapping(b, options, state_spec)
    b.map_style(ttk_style, **state_spec)


@BootstyleBuilderTTk.register_builder('outline', 'TMenubutton')
def build_outline_menubutton_style(b: BootstyleBuilderTTk, ttk_style: str, color: str = None, **options):
    """Configure the outline menubutton style."""
    accent_token = color or 'primary'
    surface_token = options.get('surface_color', 'background')
    show_dropdown = options.get('show_dropdown_button', True)
    dropdown_icon = options.get('dropdown_button_icon', 'caret-down-fill')
    icon_only = options.get('icon_only', False)

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
    normal_img = recolor_image('button', normal, foreground_normal, surface)
    pressed_img = recolor_image('button', pressed, pressed, surface)
    hovered_img = recolor_image('button', hovered, hovered, surface)
    focused_img = recolor_image('button', focused, focused_border, focused_ring)
    focused_hovered_img = recolor_image('button', hovered, focused_border, focused_ring)
    focused_pressed_img = recolor_image('button', pressed, focused_border, focused_ring)
    disabled_img = recolor_image('button', surface, disabled, surface, surface)

    if show_dropdown:
        _create_spacer(b, ttk_style)
        _create_chevron_images(b, ttk_style, foreground_normal, disabled, foreground_active, dropdown_icon)

    b.create_style_element_image(
        ElementImage(
            f'{ttk_style}.border', normal_img, sticky="nsew", border=b.scale(10),
            padding=b.scale(10)).state_specs(
            [
                ('disabled', disabled_img),
                ('focus pressed', focused_pressed_img),
                ('focus hover', focused_hovered_img),
                ('focus', focused_img),
                ('pressed', pressed_img),
                ('hover', hovered_img),
            ]))

    b.create_style_layout(ttk_style, _menubutton_layout(ttk_style, show_dropdown))

    b.configure_style(
        ttk_style,
        background=surface,
        foreground=foreground_normal,
        relief='flat',
        stipple="gray12",
        font="body",
        takefocus=True,
        padding=0 if icon_only else b.scale((8, 0, 4, 0)),
        anchor="center" if icon_only else "w"
    )

    state_spec = dict(
        foreground=[
            ('disabled', foreground_disabled),
            ('focus', foreground_active),
            ('hover', foreground_active),
            ('', foreground_normal)
        ],
        background=[('disabled', surface)]
    )

    state_spec = _apply_icon_mapping(b, options, state_spec)
    b.map_style(ttk_style, **state_spec)


@BootstyleBuilderTTk.register_builder('text', 'TMenubutton')
def build_text_menubutton_style(b: BootstyleBuilderTTk, ttk_style: str, color: str = None, **options):
    """Configure the text menubutton style."""
    accent_token = color or 'foreground'
    surface_token = options.get('surface_color', 'background')
    show_dropdown = options.get('show_dropdown_button', True)
    dropdown_icon = options.get('dropdown_button_icon', 'caret-down-fill')
    icon_only = options.get('icon_only', False)

    surface = b.color(surface_token)
    foreground_normal = b.color(accent_token)
    foreground_disabled = b.disabled('text', surface)

    # button element images
    normal_img = recolor_image('button', surface, surface, surface, surface)
    focused_img = recolor_image('button', surface, surface, surface, surface)
    disabled_img = recolor_image('button', surface, surface, surface, surface)

    if show_dropdown:
        _create_spacer(b, ttk_style)
        _create_chevron_images(b, ttk_style, foreground_normal, foreground_disabled, icon_name=dropdown_icon)

    b.create_style_element_image(
        ElementImage(
            f'{ttk_style}.border', normal_img, sticky="nsew", border=b.scale(10),
            padding=b.scale(10)).state_specs(
            [
                ('disabled', disabled_img),
                ('focus', focused_img),
            ]))

    b.create_style_layout(ttk_style, _menubutton_layout(ttk_style, show_dropdown))

    b.configure_style(
        ttk_style,
        background=surface,
        foreground=foreground_normal,
        relief='flat',
        stipple="gray12",
        font="body",
        takefocus=True,
        padding=0 if icon_only else b.scale((8, 0, 4, 0)),
        anchor="center" if icon_only else "w"
    )

    state_spec = dict(
        foreground=[
            ('disabled', foreground_disabled),
            ('', foreground_normal)
        ],
        background=[('disabled', surface)]
    )

    state_spec = _apply_icon_mapping(b, options, state_spec)
    b.map_style(ttk_style, **state_spec)


@BootstyleBuilderTTk.register_builder('ghost', 'TMenubutton')
def build_ghost_menubutton_style(b: BootstyleBuilderTTk, ttk_style: str, color: str = None, **options):
    """Configure the ghost menubutton style."""
    accent_token = color or 'primary'
    surface_token = options.get('surface_color', 'background')
    show_dropdown = options.get('show_dropdown_button', True)
    dropdown_icon = options.get('dropdown_button_icon', 'caret-down-fill')
    icon_only = options.get('icon_only', False)

    surface = b.color(surface_token)

    normal = surface
    pressed = b.subtle(accent_token, surface)
    focused = hovered = pressed
    focused_ring = b.focus_ring(focused, surface)

    foreground_normal = b.color(accent_token)
    foreground_disabled = b.disabled('text', surface)

    # button element images
    normal_img = recolor_image('button', normal, normal, surface, surface)
    pressed_img = recolor_image('button', pressed, surface, surface, surface)
    hovered_img = recolor_image('button', hovered, surface, surface, surface)
    focused_img = recolor_image('button', focused, foreground_normal, focused_ring, surface)
    focused_hovered_img = recolor_image('button', hovered, foreground_normal, focused_ring, surface)
    focused_pressed_img = recolor_image('button', pressed, foreground_normal, focused_ring, surface)
    disabled_img = recolor_image('button', surface, surface, surface, surface)

    if show_dropdown:
        _create_spacer(b, ttk_style)
        _create_chevron_images(b, ttk_style, foreground_normal, foreground_disabled, icon_name=dropdown_icon)

    b.create_style_element_image(
        ElementImage(
            f'{ttk_style}.border', normal_img, sticky="nsew", border=b.scale(10),
            padding=b.scale(10)).state_specs(
            [
                ('disabled', disabled_img),
                ('focus pressed', focused_pressed_img),
                ('focus hover', focused_hovered_img),
                ('focus', focused_img),
                ('pressed', pressed_img),
                ('hover', hovered_img),
            ]))

    b.create_style_layout(ttk_style, _menubutton_layout(ttk_style, show_dropdown))

    b.configure_style(
        ttk_style,
        background=surface,
        foreground=foreground_normal,
        relief='flat',
        stipple="gray12",
        font="body",
        takefocus=True,
        padding=0 if icon_only else b.scale((8, 0, 4, 0)),
        anchor="center" if icon_only else "w"
    )

    state_spec = dict(
        foreground=[('disabled', foreground_disabled), ('', foreground_normal)],
        background=[('disabled', surface)]
    )

    state_spec = _apply_icon_mapping(b, options, state_spec)
    b.map_style(ttk_style, **state_spec)
