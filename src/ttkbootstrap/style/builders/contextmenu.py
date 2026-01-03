from __future__ import annotations

from ttkbootstrap_icons_bs import BootstrapIcon

from ttkbootstrap.style.bootstyle_builder_ttk import BootstyleBuilderTTk
from ttkbootstrap.style.builders.button import _apply_icon_mapping
from ttkbootstrap.style.element import Element
from ttkbootstrap.style.utility import create_transparent_image


def _context_item_layout(ttk_style: str) -> Element:
    """Layout for context menu items - simple background with padding and label."""
    return Element(f"{ttk_style}.border", sticky="nsew").children(
        [
            Element("Toolbutton.padding", sticky="nsew").children(
                [
                    Element("Toolbutton.label", sticky="nsew")
                ])
        ])


@BootstyleBuilderTTk.register_builder('context-check', 'Toolbutton')
def build_context_check_toolbutton_style(b: BootstyleBuilderTTk, ttk_style: str, accent: str = None, **options):
    surface_token = options.get('surface', 'content')

    surface = b.color(surface_token)
    on_surface = b.on_color(surface)
    on_disabled = b.disabled('text', surface)

    active = b.active(surface)
    pressed = b.pressed(surface)
    on_pressed = b.on_color(pressed)

    b.create_style_layout(
        ttk_style,
        _context_item_layout(ttk_style),
    )

    b.configure_style(
        ttk_style,
        background=surface,
        foreground=on_surface,
        relief='flat',
        stipple='gray12',
        padding=(6, 3),
        anchor='w',
        font='caption',
        compound='left',
        focuscolor=''
    )

    state_spec = dict(
        foreground=[
            ('disabled', on_disabled),
            ('focus !disabled', on_pressed),
            ('pressed', on_pressed),
            ('', on_surface)],
        background=[
            ('focus !disabled', active),
            ('pressed !disabled', pressed),
            ('active !disabled', active),
            ('', surface)
        ]
    )

    icon_empty = create_transparent_image(16, 16)
    icon_pressed = BootstrapIcon('check', 16, on_pressed)
    icon_normal = BootstrapIcon('check', 16, on_surface)

    state_spec['image'] = [
        ('selected pressed', icon_pressed),
        ('selected', icon_normal),
        ('', icon_empty)
    ]

    b.map_style(ttk_style, **state_spec)


@BootstyleBuilderTTk.register_builder('context-radio', 'Toolbutton')
def build_context_radio_toolbutton_style(b: BootstyleBuilderTTk, ttk_style: str, accent: str = None, **options):
    surface_token = options.get('surface', 'content')

    surface = b.color(surface_token)
    on_surface = b.on_color(surface)
    on_disabled = b.disabled('text', surface)

    active = b.active(surface)
    pressed = b.pressed(surface)
    on_pressed = b.on_color(pressed)

    b.create_style_layout(
        ttk_style,
        _context_item_layout(ttk_style),
    )

    b.configure_style(
        ttk_style,
        background=surface,
        foreground=on_surface,
        relief='flat',
        stipple='gray12',
        padding=(6, 3),
        anchor='w',
        font='caption',
        compound='left',
        focuscolor=''
    )

    state_spec = dict(
        foreground=[
            ('disabled', on_disabled),
            ('focus !disabled', on_pressed),
            ('pressed', on_pressed),
            ('', on_surface)],
        background=[
            ('focus !disabled', active),
            ('pressed !disabled', pressed),
            ('active !disabled', active),
            ('', surface)
        ]
    )

    icon_empty = create_transparent_image(16, 16)
    icon_pressed = BootstrapIcon('check', 16, on_pressed)
    icon_normal = BootstrapIcon('check', 16, on_surface)

    state_spec['image'] = [
        ('selected pressed', icon_pressed),
        ('selected', icon_normal),
        ('', icon_empty)
    ]

    b.map_style(ttk_style, **state_spec)


@BootstyleBuilderTTk.register_builder('context-item', 'TButton')
def build_context_item_button_style(b: BootstyleBuilderTTk, ttk_style: str, accent: str = None, **options):
    """
    Configure the context menu button style.

    Style options include:
        * icon
        * icon_only
        * anchor
    """
    anchor = options.get('anchor', 'w')
    surface_token = options.get('surface', 'content')

    surface = b.color(surface_token)
    on_surface = b.on_color(surface)
    on_disabled = b.disabled('text', surface)

    active = b.active(surface)
    pressed = b.pressed(surface)
    on_pressed = b.on_color(pressed)

    b.configure_style(
        ttk_style,
        background=surface,
        foreground=on_surface,
        relief='flat',
        stipple='gray12',
        padding=(6, 3),
        anchor=anchor,
        font='caption',
        focuscolor=''
    )

    state_spec = dict(
        foreground=[
            ('disabled', on_disabled),
            ('focus !disabled', on_pressed),
            ('pressed', on_pressed),
            ('', on_surface)],
        background=[
            ('focus !disabled', active),
            ('pressed !disabled', pressed),
            ('active !disabled', active),
            ('', surface)
        ]
    )

    icon_only = options.get('icon_only', False)
    default_size = 20 if icon_only else 16
    state_spec = _apply_icon_mapping(b, options, state_spec, default_size)

    b.map_style(ttk_style, **state_spec)
