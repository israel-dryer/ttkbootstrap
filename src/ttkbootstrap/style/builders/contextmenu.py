from __future__ import annotations

from ttkbootstrap_icons_bs import BootstrapIcon

from ttkbootstrap.style.bootstyle_builder_ttk import BootstyleBuilderTTk
from ttkbootstrap.style.utility import create_transparent_image


@BootstyleBuilderTTk.register_builder('context_check', 'Toolbutton')
def build_context_check_toolbutton_style(b: BootstyleBuilderTTk, ttk_style: str, color: str = None, **options):
    accent_token = color or 'primary'
    surface_token = options.get('surface_color', 'background')

    surface = b.color(surface_token)
    on_surface = b.on_color(surface)
    on_disabled = b.disabled('text', surface)

    active = b.elevate(surface, 1)
    pressed = b.elevate(surface, 2)
    on_pressed = b.on_color(pressed)

    b.configure_style(
        ttk_style,
        background=surface,
        foreground=on_surface,
        relief='flat',
        stipple='gray12',
        padding=(6, 3),
        anchor='w',
        font='body',
        compound='left',
        focuscolor=''
    )

    state_spec = dict(
        foreground=[
            ('disabled', on_disabled),
            ('pressed', on_pressed),
            ('', on_surface)],
        background=[
            ('pressed !disabled', pressed),
            ('active !disabled', active),
            ('', surface)
        ]
    )

    icon_empty = create_transparent_image(20, 20)
    icon_pressed = BootstrapIcon('check', 20, on_pressed)
    icon_normal = BootstrapIcon('check', 20, on_surface)

    state_spec['image'] = [
        ('selected pressed', icon_pressed),
        ('selected', icon_normal),
        ('', icon_empty)
    ]

    b.map_style(ttk_style, **state_spec)


@BootstyleBuilderTTk.register_builder('context_radio', 'Toolbutton')
def build_context_radio_toolbutton_style(b: BootstyleBuilderTTk, ttk_style: str, color: str = None, **options):
    accent_token = color or 'primary'
    surface_token = options.get('surface_color', 'background')

    surface = b.color(surface_token)
    on_surface = b.on_color(surface)
    on_disabled = b.disabled('text', surface)

    active = b.elevate(surface, 1)
    pressed = b.elevate(surface, 2)
    on_pressed = b.on_color(pressed)

    b.configure_style(
        ttk_style,
        background=surface,
        foreground=on_surface,
        relief='flat',
        stipple='gray12',
        padding=(6, 3),
        anchor='w',
        font='body',
        compound='left',
        focuscolor=''
    )

    state_spec = dict(
        foreground=[
            ('disabled', on_disabled),
            ('pressed', on_pressed),
            ('', on_surface)],
        background=[
            ('pressed !disabled', pressed),
            ('active !disabled', active),
            ('', surface)
        ]
    )

    icon_empty = create_transparent_image(20, 20)
    icon_pressed = BootstrapIcon('check', 20, on_pressed)
    icon_normal = BootstrapIcon('check', 20, on_surface)

    state_spec['image'] = [
        ('selected pressed', icon_pressed),
        ('selected', icon_normal),
        ('', icon_empty)
    ]

    b.map_style(ttk_style, **state_spec)
