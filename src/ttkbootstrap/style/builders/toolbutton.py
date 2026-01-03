"""Toolbutton widget style builders.

This module contains style builders for ttk.Checkbutton and Radiobutton toolbutton variants.
"""

from __future__ import annotations

from ttkbootstrap.style.bootstyle_builder_ttk import BootstyleBuilderTTk
from ttkbootstrap.style.element import Element, ElementImage
from ttkbootstrap.style.utility import recolor_image


# The active styles are intentionally limited on toolbuttons to improve interaction
# and limit the number of images created for each style.


def _toolbutton_layout(ttk_style: str) -> Element:
    return Element(f"{ttk_style}.border", sticky="nsew").children(
        [
            Element("Toolbutton.padding", sticky="nsew").children(
                [
                    Element("Toolbutton.label", sticky="nsew")
                ])
        ])


def _toolbutton_padding(b: BootstyleBuilderTTk, options: dict) -> int | tuple[int, int]:
    return 0 if options.get('icon_only', False) else b.scale((8, 0))


def _apply_icon_mapping(
        b: BootstyleBuilderTTk,
        options: dict,
        state_spec: dict,
        default_size: int,
) -> dict:
    icon = options.get('icon')
    if icon is None:
        return state_spec

    icon = b.normalize_icon_spec(icon, default_size)
    state_spec['image'] = b.map_stateful_icons(icon, state_spec['foreground'])
    return state_spec


@BootstyleBuilderTTk.register_builder('default', 'Toolbutton')
def build_solid_toolbutton_style(b: BootstyleBuilderTTk, ttk_style: str, accent: str = None, **options):
    """
    Configure the button style.

    Style options include:
        * anchor
        * icon
        * icon_only
    """
    anchor = options.get('anchor', 'center')
    accent_token = accent or 'primary'
    surface_token = options.get('surface', 'content')

    surface = b.color(surface_token)

    accent_color = b.color(accent_token)

    active = b.active(accent_color)
    accent_focus = b.focus(accent_color)
    on_accent = b.on_color(accent_color)

    selected = b.selected(accent_color)

    focus_ring = b.focus_ring(accent_focus, surface)
    disabled = b.disabled()
    on_disabled = b.disabled('text', disabled)

    normal_img = recolor_image('button', accent_color, accent_color, surface, surface)
    normal_focus_img = recolor_image('button', accent_color, accent_color, focus_ring, surface)
    active_img = recolor_image('button', active, active, surface, surface)
    selected_img = recolor_image('button', selected, selected, surface, surface)
    selected_focus_img = recolor_image('button', selected, selected, focus_ring, surface)

    disabled_img = recolor_image('button', disabled, disabled, surface, surface)

    b.create_style_element_image(
        ElementImage(
            f'{ttk_style}.border', normal_img, sticky="nsew", border=b.scale(8), padding=b.scale(8)).state_specs(
            [
                ('disabled', disabled_img),
                ('background pressed focus selected', selected_focus_img),
                ('pressed', selected_img),
                ('background focus selected', selected_focus_img),
                ('selected', selected_img),
                ('background focus !selected', normal_focus_img),
                ('background active !focus', active_img),
                ('', normal_img)
            ]))

    b.create_style_layout(
        ttk_style,
        _toolbutton_layout(ttk_style),
    )

    button_padding = _toolbutton_padding(b, options)

    b.configure_style(
        ttk_style,
        background=surface,
        foreground=on_accent,
        stipple="gray12",
        relief='flat',
        padding=button_padding,
        anchor=anchor,
        font="body"
    )

    state_spec = dict(foreground=[('disabled', on_disabled), ('', on_accent)])

    icon_only = options.get('icon_only', False)
    default_size = b.scale(24) if icon_only else b.scale(20)
    state_spec = _apply_icon_mapping(b, options, state_spec, default_size)

    b.map_style(ttk_style, **state_spec)


@BootstyleBuilderTTk.register_builder('outline', 'Toolbutton')
def build_outline_toolbutton_style(b: BootstyleBuilderTTk, ttk_style: str, accent: str = None, **options):
    """
    Configure the button style.

    Style options include:
        * anchor
        * icon
        * icon_only
    """
    anchor = options.get('anchor', 'center')
    accent_token = accent or 'primary'
    surface_token = options.get('surface', 'content')

    surface = b.color(surface_token)
    accent_color = b.color(accent_token)
    accent_focus = b.focus(accent_color)
    on_accent = b.on_color(accent_color)

    focus_ring = b.focus_ring(accent_focus, surface)
    disabled = b.disabled()
    on_disabled = b.disabled('text', disabled)

    normal_img = recolor_image('button', surface, accent_color, surface, surface)
    normal_focus_img = recolor_image('button', surface, accent_focus, focus_ring, surface)
    selected_img = recolor_image('button', accent_color, accent_color, surface, surface)
    selected_focus_img = recolor_image('button', accent_color, accent_focus, focus_ring, surface)

    disabled_img = recolor_image('button', disabled, disabled, surface, surface)

    b.create_style_element_image(
        ElementImage(
            f'{ttk_style}.border', normal_img, sticky="nsew", border=b.scale(8), padding=b.scale(8)).state_specs(
            [
                ('disabled', disabled_img),
                ('background pressed selected focus', selected_focus_img),
                ('pressed', selected_img),
                ('background selected focus', selected_focus_img),
                ('selected', selected_img),
                ('background focus !selected', normal_focus_img),
                ('', normal_img)
            ]))

    b.create_style_layout(
        ttk_style,
        _toolbutton_layout(ttk_style),
    )

    button_padding = _toolbutton_padding(b, options)

    b.configure_style(
        ttk_style,
        background=surface,
        foreground=accent_color,
        stipple="gray12",
        relief='flat',
        padding=button_padding,
        anchor=anchor,
        font="body"
    )

    state_spec = dict(
        foreground=[('disabled', on_disabled), ('selected !disabled', on_accent), ('pressed !disabled', on_accent),
                    ('', accent_color)],
    )

    icon_only = options.get('icon_only', False)
    default_size = b.scale(24) if icon_only else b.scale(20)
    state_spec = _apply_icon_mapping(b, options, state_spec, default_size)

    b.map_style(ttk_style, **state_spec)


@BootstyleBuilderTTk.register_builder('ghost', 'Toolbutton')
def build_ghost_toolbutton_style(b: BootstyleBuilderTTk, ttk_style: str, accent: str = None, **options):
    """
    Configure the button style.

    Style options include:
        * anchor
        * icon
        * icon_only
    """
    anchor = options.get('anchor', 'center')
    accent_token = accent or 'foreground'
    surface_token = options.get('surface', 'content')

    surface = b.color(surface_token)
    on_surface = b.on_color(surface)

    active = b.subtle(accent_token, surface)
    accent_color = b.color(accent_token)
    accent_pressed = b.pressed(active)
    accent_focus = b.focus(active)

    focus_ring = b.focus_ring(accent_focus, surface)
    disabled = b.disabled()
    on_disabled = b.disabled('text', disabled)

    normal_img = recolor_image('button', surface, surface, surface, surface)
    normal_focus_img = recolor_image('button', surface, accent_color, focus_ring, surface)
    selected_img = recolor_image('button', active, active, surface, surface)
    selected_pressed_img = recolor_image('button', accent_pressed, accent_pressed, surface, surface)
    selected_focus_img = recolor_image('button', accent_focus, accent_color, focus_ring, surface)

    disabled_img = recolor_image('button', disabled, disabled, surface, surface)

    b.create_style_element_image(
        ElementImage(
            f'{ttk_style}.border', normal_img, sticky="nsew", border=b.scale(8), padding=b.scale(8)).state_specs(
            [
                ('disabled', disabled_img),
                ('background pressed selected focus', selected_focus_img),
                ('pressed', selected_img),
                ('background selected focus', selected_focus_img),
                ('selected pressed', selected_pressed_img),
                ('selected', selected_img),
                ('background focus !selected', normal_focus_img),
                ('', normal_img)
            ]))

    b.create_style_layout(
        ttk_style,
        _toolbutton_layout(ttk_style),
    )

    button_padding = _toolbutton_padding(b, options)

    b.configure_style(
        ttk_style,
        background=surface,
        foreground=on_surface,
        stipple="gray12",
        relief='flat',
        padding=button_padding,
        anchor=anchor,
        font="body"
    )

    state_spec = dict(
        foreground=[
            ('disabled', on_disabled),
            ('selected', accent_color),
            ('pressed', accent_color),
            ('', on_surface)],
    )

    icon_only = options.get('icon_only', False)
    default_size = b.scale(24) if icon_only else b.scale(20)
    state_spec = _apply_icon_mapping(b, options, state_spec, default_size)

    b.map_style(ttk_style, **state_spec)
