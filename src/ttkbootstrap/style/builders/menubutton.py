"""Menubutton widget style builders.

This module contains style builders for ttk.Menubutton widgets and variants.
"""

from __future__ import annotations

from ttkbootstrap.appconfig import use_icon_provider
from ttkbootstrap.style.bootstyle_builder_ttk import BootstyleBuilderTTk
from ttkbootstrap.style.element import Element, ElementImage
from ttkbootstrap.style.utility import create_transparent_image, recolor_image


@BootstyleBuilderTTk.register_builder('solid', 'TMenubutton')
@BootstyleBuilderTTk.register_builder('default', 'TMenubutton')
def build_solid_menubutton_style(b: BootstyleBuilderTTk, ttk_style: str, color: str = None, **options):
    accent_token = color or 'primary'
    surface_token = options.get('surface_color', 'background')

    surface = b.color(surface_token)
    normal = b.color(accent_token)
    foreground = b.on_color(normal)
    foreground_disabled = b.disabled('text')
    pressed = b.active(normal)
    hovered = focused = b.hover(normal)
    focused_border = b.focus_border(normal)
    disabled = b.disabled()
    focused_ring = b.focus_ring(normal, surface)

    normal_img = recolor_image('button', normal, normal, surface)
    pressed_img = recolor_image('button', pressed, pressed, surface)
    hovered_img = recolor_image('button', hovered, hovered, surface)
    focused_img = recolor_image('button', focused, focused_border, focused_ring)
    focused_hovered_img = recolor_image('button', hovered, focused_border, focused_ring)
    focused_pressed_img = recolor_image('button', pressed, focused_border, focused_ring)
    disabled_img = recolor_image('button', disabled, disabled, surface, surface)

    spacer_img = create_transparent_image(8, 1)
    b.create_style_element_image(ElementImage(f'{ttk_style}.spacer', spacer_img, sticky="ew"))

    # chevron images
    icon = use_icon_provider()
    normal_chevron_img = icon('caret-down-fill', size=14, color=foreground).image
    disabled_chevron_img = icon('caret-down-fill', size=14, color=disabled).image
    b.create_style_element_image(
        ElementImage(f'{ttk_style}.chevron', normal_chevron_img).state_specs(
            [
                ('disabled', disabled_chevron_img),
                ('', normal_chevron_img),
            ]))

    b.create_style_element_image(
        ElementImage(
            f'{ttk_style}.border', normal_img, sticky="nsew", border=8, padding=8).state_specs(
            [
                ('disabled', disabled_img),
                ('focus pressed', focused_pressed_img),
                ('focus hover', focused_hovered_img),
                ('focus', focused_img),
                ('pressed', pressed_img),
                ('hover', hovered_img),
            ]))

    b.create_style_layout(
        ttk_style, Element(f"{ttk_style}.border", sticky="nsew").children(
            [
                Element("Menubutton.padding", sticky="nsew").children(
                    [
                        Element("Menubutton.label", sticky="", side="left"),
                        Element(f"{ttk_style}.chevron", side="right", sticky=""),
                        Element(f'{ttk_style}.spacer', side="right", sticky=""),
                    ])
            ]))

    b.configure_style(
        ttk_style,
        background=surface,
        foreground=foreground,
        stipple="gray12",
        relief='flat',
        padding=(8, 0, 4, 0),
    )

    state_spec = dict(
        foreground=[('disabled', foreground_disabled), ('', foreground)],
        background=[('disabled', disabled)]
    )

    # map icon if available
    icon = options.get('icon')

    if icon is not None:
        icon = b.normalize_icon_spec(icon)
        state_spec['image'] = b.map_stateful_icons(icon, state_spec['foreground'])

    b.map_style(ttk_style, **state_spec)


@BootstyleBuilderTTk.register_builder('outline', 'TMenubutton')
def build_outline_menubutton_style(b: BootstyleBuilderTTk, ttk_style: str, color: str = None, **options):
    accent_token = color or 'primary'
    surface_token = options.get('surface_color', 'background')

    surface = b.color(surface_token)
    foreground_normal = b.color(accent_token)
    foreground_disabled = b.disabled('text')
    foreground_active = b.on_color(foreground_normal)

    disabled = foreground_disabled
    normal = surface
    pressed = b.hover(foreground_normal)
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

    spacer_img = create_transparent_image(8, 1)
    b.create_style_element_image(ElementImage(f'{ttk_style}.spacer', spacer_img, sticky="ew"))

    # chevron images
    icon = use_icon_provider()
    normal_chevron_img = icon('caret-down-fill', size=14, color=foreground_normal).image
    pressed_chevron_img = icon('caret-down-fill', size=14, color=foreground_active).image
    disabled_chevron_img = icon('caret-down-fill', size=14, color=disabled).image
    b.create_style_element_image(
        ElementImage(f'{ttk_style}.chevron', normal_chevron_img).state_specs(
            [
                ('disabled', disabled_chevron_img),
                ('hover !disabled', pressed_chevron_img),
                ('pressed !disabled', pressed_chevron_img),
                ('', normal_chevron_img),
            ]))

    b.create_style_element_image(
        ElementImage(
            f'{ttk_style}.border', normal_img, sticky="nsew", border=8, padding=8).state_specs(
            [
                ('disabled', disabled_img),
                ('focus pressed', focused_pressed_img),
                ('focus hover', focused_hovered_img),
                ('focus', focused_img),
                ('pressed', pressed_img),
                ('hover', hovered_img),
            ]))

    b.create_style_element_image(
        ElementImage(
            f'{ttk_style}.border', normal_img, sticky="nsew", border=8, padding=8).state_specs(
            [
                ('disabled', disabled_img),
                ('focus pressed', focused_pressed_img),
                ('focus hover', focused_hovered_img),
                ('focus', focused_img),
                ('pressed', pressed_img),
                ('hover', hovered_img),
            ])
    )

    b.create_style_layout(
        ttk_style, Element(f"{ttk_style}.border", sticky="nsew").children(
            [
                Element("Menubutton.padding", sticky="nsew").children(
                    [
                        Element("Menubutton.label", sticky="", side="left"),
                        Element(f"{ttk_style}.chevron", side="right", sticky=""),
                        Element(f'{ttk_style}.spacer', side="right", sticky=""),
                    ])
            ]))

    b.configure_style(
        ttk_style,
        background=surface,
        foreground=foreground_normal,
        relief='flat',
        stipple="gray12",
        padding=(8, 0, 4, 0)
    )

    state_spec = dict(
        foreground=[
            ('disabled', foreground_disabled),
            ('focus', foreground_active),
            ('hover', foreground_active),
            ('', foreground_normal)
        ], background=[('disabled', surface)]
    )

    # map icon if available
    icon = options.get('icon')

    if icon is not None:
        icon = b.normalize_icon_spec(icon)
        state_spec['image'] = b.map_stateful_icons(icon, state_spec['foreground'])

    b.map_style(ttk_style, **state_spec)


@BootstyleBuilderTTk.register_builder('text', 'TMenubutton')
def build_text_menubutton_style(b: BootstyleBuilderTTk, ttk_style: str, color: str = None, **options):
    accent_token = color or 'foreground'
    surface_token = options.get('surface_color', 'background')

    surface = b.color(surface_token)
    foreground_normal = b.color(accent_token)
    foreground_disabled = b.disabled('text')

    disabled = foreground_disabled
    focused_ring = b.focus_ring(foreground_normal, surface)

    # button element images
    normal_img = recolor_image('button', surface, surface, surface)
    focused_img = recolor_image('button', surface, surface, focused_ring)
    disabled_img = recolor_image('button', surface, disabled, surface, surface)

    spacer_img = create_transparent_image(8, 1)
    b.create_style_element_image(ElementImage(f'{ttk_style}.spacer', spacer_img, sticky="ew"))

    # chevron images
    icon = use_icon_provider()
    normal_chevron_img = icon('caret-down-fill', size=14, color=foreground_normal).image
    disabled_chevron_img = icon('caret-down-fill', size=14, color=disabled).image
    b.create_style_element_image(
        ElementImage(f'{ttk_style}.chevron', normal_chevron_img).state_specs(
            [
                ('disabled', disabled_chevron_img),
                ('', normal_chevron_img),
            ]))

    b.create_style_element_image(
        ElementImage(
            f'{ttk_style}.border', normal_img, sticky="nsew", border=8, padding=8).state_specs(
            [
                ('disabled', disabled_img),
                ('focus', focused_img),
            ])
    )

    b.create_style_layout(
        ttk_style, Element(f"{ttk_style}.border", sticky="nsew").children(
            [
                Element("Menubutton.padding", sticky="nsew").children(
                    [
                        Element("Menubutton.label", sticky="", side="left"),
                        Element(f"{ttk_style}.chevron", side="right", sticky=""),
                        Element(f'{ttk_style}.spacer', side="right", sticky=""),
                    ])
            ]))

    b.configure_style(
        ttk_style,
        background=surface,
        foreground=foreground_normal,
        relief='flat',
        stipple="gray12",
        padding=(8, 0, 4, 0)
    )

    state_spec = dict(
        foreground=[
            ('disabled', foreground_disabled),
            ('', foreground_normal)
        ], background=[('disabled', surface)]
    )

    # map icon if available
    icon = options.get('icon')

    if icon is not None:
        icon = b.normalize_icon_spec(icon)
        state_spec['image'] = b.map_stateful_icons(icon, state_spec['foreground'])

    b.map_style(ttk_style, **state_spec)


@BootstyleBuilderTTk.register_builder('ghost', 'TMenubutton')
def build_ghost_button_style(b: BootstyleBuilderTTk, ttk_style: str, color: str = None, **options):
    accent_token = color or 'primary'
    surface_token = options.get('surface_color', 'background')

    surface = b.color(surface_token)
    foreground_normal = b.color(accent_token)
    foreground_disabled = b.disabled('text')

    normal = surface
    pressed = b.subtle(accent_token, surface)
    focused = hovered = pressed
    focused_ring = b.focus_ring(focused, surface)

    # button element images
    normal_img = recolor_image('button', normal, normal, surface, surface)
    pressed_img = recolor_image('button', pressed, surface, surface, surface)
    hovered_img = recolor_image('button', hovered, surface, surface, surface)
    focused_img = recolor_image('button', focused, focused, focused_ring, surface)
    focused_hovered_img = recolor_image('button', hovered, focused, focused_ring, surface)
    focused_pressed_img = recolor_image('button', pressed, focused, focused_ring, surface)
    disabled_img = recolor_image('button', surface, surface, surface, surface)

    spacer_img = create_transparent_image(8, 1)
    b.create_style_element_image(ElementImage(f'{ttk_style}.spacer', spacer_img, sticky="ew"))

    # chevron images
    icon = use_icon_provider()
    normal_chevron_img = icon('caret-down-fill', size=14, color=foreground_normal).image
    disabled_chevron_img = icon('caret-down-fill', size=14, color=foreground_disabled).image
    b.create_style_element_image(
        ElementImage(f'{ttk_style}.chevron', normal_chevron_img).state_specs(
            [
                ('disabled', disabled_chevron_img),
                ('', normal_chevron_img),
            ]))

    b.create_style_element_image(
        ElementImage(
            f'{ttk_style}.border', normal_img, sticky="nsew", border=8, padding=8).state_specs(
            [
                ('disabled', disabled_img),
                ('focus pressed', focused_pressed_img),
                ('focus hover', focused_hovered_img),
                ('focus', focused_img),
                ('pressed', pressed_img),
                ('hover', hovered_img),
            ])
    )

    b.create_style_layout(
        ttk_style, Element(f"{ttk_style}.border", sticky="nsew").children(
            [
                Element("Menubutton.padding", sticky="nsew").children(
                    [
                        Element("Menubutton.label", sticky="", side="left"),
                        Element(f"{ttk_style}.chevron", side="right", sticky=""),
                        Element(f'{ttk_style}.spacer', side="right", sticky=""),
                    ])
            ]))

    b.configure_style(
        ttk_style,
        background=surface,
        foreground=foreground_normal,
        relief='flat',
        stipple="gray12",
        padding=(8, 0, 4, 0)
    )

    state_spec = dict(
        foreground=[('disabled', foreground_disabled), ('', foreground_normal)],
        background=[('disabled', surface)]
    )

    # map icon if available
    icon = options.get('icon')

    if icon is not None:
        icon = b.normalize_icon_spec(icon)
        state_spec['image'] = b.map_stateful_icons(icon, state_spec['foreground'])

    b.map_style(ttk_style, **state_spec)
