"""Button widget style builders.

This module contains style builders for ttk.Button widgets and variants.
"""

from __future__ import annotations

from ttkbootstrap.style.bootstyle_builder_ttk import BootstyleBuilderTTk
from ttkbootstrap.style.element import Element, ElementImage
from ttkbootstrap.style.utility import recolor_image


def _button_layout(ttk_style: str) -> Element:
    return Element(f"{ttk_style}.Button.border", sticky="nsew").children(
        [
            Element("Button.padding", sticky="nsew").children(
                [
                    Element("Button.label", sticky="")
                ])
        ])


def _button_padding(b: BootstyleBuilderTTk, options: dict) -> int | tuple[int, int]:
    return 0 if options.get('icon_only', False) else b.scale((8, 0))


def _apply_icon_mapping(
        b: BootstyleBuilderTTk,
        options: dict,
        state_spec: dict,
        default_size: int | None = None
) -> dict:
    icon = options.get('icon')
    if icon is None:
        return state_spec

    if default_size is None:
        icon = b.normalize_icon_spec(icon)
    else:
        icon = b.normalize_icon_spec(icon, default_size)

    state_spec['image'] = b.map_stateful_icons(icon, state_spec['foreground'])
    # Set compound to 'left' so text is visible alongside the icon
    icon_only = options.get('icon_only', False)
    if not icon_only:
        state_spec['compound'] = 'left'
    return state_spec


@BootstyleBuilderTTk.register_builder('solid', 'TButton')
@BootstyleBuilderTTk.register_builder('default', 'TButton')
def build_solid_button_style(b: BootstyleBuilderTTk, ttk_style: str, color: str = None, **options):
    """
    Configure the button style.

    Style options include:
        * icon
        * icon_only
        * anchor
    """
    anchor = options.get('anchor', 'center')
    accent_token = color or 'primary'
    surface_token = options.get('surface_color', 'background')

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

    b.create_style_element_image(
        ElementImage(
            f'{ttk_style}.Button.border', normal_img, sticky="nsew", border=b.scale(10),
            padding=b.scale(10)).state_specs(
            [
                ('disabled', disabled_img),
                ('background focus pressed', focused_pressed_img),
                ('background focus hover', focused_hovered_img),
                ('background focus', focused_img),
                ('pressed', pressed_img),
                ('hover', hovered_img),
            ]))

    b.create_style_layout(
        ttk_style,
        _button_layout(ttk_style),
    )

    button_padding = _button_padding(b, options)

    b.configure_style(
        ttk_style,
        background=surface,
        foreground=foreground,
        stipple="gray12",
        relief='flat',
        padding=button_padding,
        anchor=anchor,
        font="body"
    )

    state_spec = dict(
        foreground=[('disabled', foreground_disabled), ('', foreground)],
        background=[('disabled', disabled)]
    )

    icon_only = options.get('icon_only', False)
    default_size = b.scale(24) if icon_only else b.scale(20)
    state_spec = _apply_icon_mapping(b, options, state_spec, default_size)

    b.map_style(ttk_style, **state_spec)


@BootstyleBuilderTTk.register_builder('outline', 'TButton')
def build_outline_button_style(b: BootstyleBuilderTTk, ttk_style: str, color: str = None, **options):
    """
    Configure the outline button style.

    Style options include:
        * icon
        * icon_only
        * anchor
    """
    anchor = options.get('anchor', 'center')
    accent_token = color or 'primary'
    surface_token = options.get('surface_color', 'background')

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

    b.create_style_element_image(
        ElementImage(
            f'{ttk_style}.Button.border', normal_img, sticky="nsew", border=b.scale(10),
            padding=b.scale(10)).state_specs(
            [
                ('disabled', disabled_img),
                ('background focus pressed', focused_pressed_img),
                ('background focus hover', focused_hovered_img),
                ('background focus', focused_img),
                ('pressed', pressed_img),
                ('hover', hovered_img),
            ])
    )

    b.create_style_layout(
        ttk_style,
        _button_layout(ttk_style),
    )

    button_padding = _button_padding(b, options)

    b.configure_style(
        ttk_style,
        background=surface,
        foreground=foreground_normal,
        relief='flat',
        stipple="gray12",
        padding=button_padding,
        anchor=anchor,
        font="body"
    )

    state_spec = dict(
        foreground=[
            ('disabled', foreground_disabled),
            ('background focus', foreground_active),
            ('hover', foreground_active),
            ('', foreground_normal)
        ], background=[('disabled', surface)]
    )

    state_spec = _apply_icon_mapping(b, options, state_spec)

    b.map_style(ttk_style, **state_spec)


@BootstyleBuilderTTk.register_builder('text', 'TButton')
def build_text_button_style(b: BootstyleBuilderTTk, ttk_style: str, color: str = None, **options):
    """
    Configure the text button style.

    Style options include:
        * icon
        * icon_only
        * anchor
    """
    anchor = options.get('anchor', 'center')
    accent_token = color or 'foreground'
    surface_token = options.get('surface_color', 'background')

    surface = b.color(surface_token)
    foreground_normal = b.color(accent_token)
    foreground_disabled = b.disabled('text', surface)

    # button element images
    normal_img = recolor_image('button', surface, surface, surface, surface)
    focused_img = recolor_image('button', surface, surface, surface, surface)
    disabled_img = recolor_image('button', surface, surface, surface, surface)

    b.create_style_element_image(
        ElementImage(
            f'{ttk_style}.Button.border', normal_img, sticky="nsew", border=b.scale(10),
            padding=b.scale(10)).state_specs(
            [
                ('disabled', disabled_img),
                ('focus', focused_img),
            ])
    )

    b.create_style_layout(
        ttk_style,
        _button_layout(ttk_style),
    )

    button_padding = _button_padding(b, options)

    b.configure_style(
        ttk_style,
        background=surface,
        foreground=foreground_normal,
        relief='flat',
        stipple="gray12",
        padding=button_padding,
        anchor=anchor,
        font="body"
    )

    from ttkbootstrap.style.typography import Font


    state_spec = dict(
        font=[('background focus', Font('body[bold]'))],
        foreground=[
            ('disabled', foreground_disabled),
            ('', foreground_normal)
        ], background=[('disabled', surface)]
    )

    icon_only = options.get('icon_only', False)
    default_size = 24 if icon_only else 20
    state_spec = _apply_icon_mapping(b, options, state_spec, default_size)

    b.map_style(ttk_style, **state_spec)


@BootstyleBuilderTTk.register_builder('link', 'TButton')
def build_link_button_style(b: BootstyleBuilderTTk, ttk_style: str, color: str = None, **options):
    """
    Configure the link button style.

    Style options include:
        * icon
        * icon_only
        * anchor
    """
    anchor = options.get('anchor', 'center')
    accent_token = color or 'primary'
    surface_token = options.get('surface_color', 'background')

    surface = b.color(surface_token)
    foreground_normal = b.color(accent_token)
    foreground_disabled = b.disabled('text', surface)

    # button element images
    normal_img = recolor_image('button', surface, surface, surface, surface)
    focused_img = recolor_image('button', surface, surface, surface, surface)
    disabled_img = recolor_image('button', surface, surface, surface, surface)

    b.create_style_element_image(
        ElementImage(
            f'{ttk_style}.Button.border', normal_img, sticky="nsew", border=b.scale(10),
            padding=b.scale(10)).state_specs(
            [
                ('disabled', disabled_img),
                ('focus', focused_img),
            ])
    )

    b.create_style_layout(
        ttk_style,
        _button_layout(ttk_style),
    )

    button_padding = _button_padding(b, options)

    b.configure_style(
        ttk_style,
        background=surface,
        foreground=foreground_normal,
        relief='flat',
        stipple="gray12",
        padding=button_padding,
        anchor=anchor,
        font="body"
    )

    state_spec = dict(
        font=[
            ("active !disabled", "hyperlink"),
            ("background focus !disabled", "hyperlink"),
            ("", "body")],
        cursor=[('', 'hand2')],
        foreground=[
            ('disabled', foreground_disabled),
            ('', foreground_normal)
        ], background=[('disabled', surface)]
    )

    icon_only = options.get('icon_only', False)
    default_size = 24 if icon_only else 20
    state_spec = _apply_icon_mapping(b, options, state_spec, default_size)

    b.map_style(ttk_style, **state_spec)


@BootstyleBuilderTTk.register_builder('ghost', 'TButton')
def build_ghost_button_style(b: BootstyleBuilderTTk, ttk_style: str, color: str = None, **options):
    """
    Configure the ghost button style.

    Style options include:
        * icon
        * icon_only
        * anchor
    """
    anchor = options.get('anchor', 'center')
    accent_token = color or 'foreground'
    surface_token = options.get('surface_color', 'background')

    surface = b.color(surface_token)

    accent = b.color(accent_token)
    normal = surface
    hovered = focused = pressed = b.subtle(accent_token, surface)
    focused_ring = b.focus_ring(accent, surface)

    foreground_normal = accent
    foreground_disabled = b.disabled('text', surface)

    # button element images
    normal_img = recolor_image('button', normal, normal, surface, surface)
    pressed_img = recolor_image('button', pressed, surface, surface, surface)
    hovered_img = recolor_image('button', hovered, surface, surface, surface)
    focused_img = recolor_image('button', focused, accent, focused_ring, surface)
    focused_hovered_img = recolor_image('button', hovered, accent, focused_ring, surface)
    focused_pressed_img = recolor_image('button', pressed, accent, focused_ring, surface)
    disabled_img = recolor_image('button', surface, surface, surface, surface)

    b.create_style_element_image(
        ElementImage(
            f'{ttk_style}.Button.border', normal_img, sticky="nsew", border=b.scale(10),
            padding=b.scale(10)).state_specs(
            [
                ('disabled', disabled_img),
                ('background focus pressed', focused_pressed_img),
                ('background focus hover', focused_hovered_img),
                ('background focus', focused_img),
                ('pressed', pressed_img),
                ('hover', hovered_img),
            ])
    )

    b.create_style_layout(
        ttk_style,
        _button_layout(ttk_style),
    )

    button_padding = _button_padding(b, options)

    b.configure_style(
        ttk_style,
        background=surface,
        foreground=foreground_normal,
        relief='flat',
        stipple="gray12",
        padding=button_padding,
        anchor=anchor,
        font="body"
    )

    state_spec = dict(
        foreground=[('disabled', foreground_disabled), ('', foreground_normal)],
        background=[('disabled', surface)]
    )

    icon_only = options.get('icon_only', False)
    default_size = 24 if icon_only else 20
    state_spec = _apply_icon_mapping(b, options, state_spec, default_size)

    b.map_style(ttk_style, **state_spec)


@BootstyleBuilderTTk.register_builder('selectbox_item', 'TButton')
def build_selectbox_item_button_style(b: BootstyleBuilderTTk, ttk_style: str, color: str = None, **options):
    """Configure the style for selectbox dropdown items with selected state support.

    Style options include:
        * icon
        * icon_only
        * anchor
    """
    anchor = options.get('anchor', 'w')
    accent_token = color or 'primary'
    surface_token = options.get('surface_color', 'background')

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
