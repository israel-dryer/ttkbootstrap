"""TabItem widget style builders.

This module contains style builders for the TabItem composite widget.
"""

from __future__ import annotations

from ttkbootstrap.style.bootstyle_builder_ttk import BootstyleBuilderTTk
from ttkbootstrap.style.element import Element, ElementImage
from ttkbootstrap.style.utility import recolor_element_image


def _apply_icon_mapping(b: BootstyleBuilderTTk, options: dict, state_spec: dict, default_size: int):
    """Apply icon mapping to the state spec if icon is provided."""
    icon = options.get('icon')
    if icon is None:
        return state_spec

    icon = b.normalize_icon_spec(icon, default_size)
    state_spec['image'] = b.map_stateful_icons(icon, state_spec['foreground'])
    icon_only = options.get('icon_only', False)
    if not icon_only:
        state_spec['compound'] = 'left'
    return state_spec


@BootstyleBuilderTTk.register_builder('bar', 'TabItem.TFrame')
@BootstyleBuilderTTk.register_builder('default', 'TabItem.TFrame')
def build_tab_item_bar_frame(b: BootstyleBuilderTTk, ttk_style: str, accent: str = None, **options):
    """TabItem frame style for bar/underline variant."""
    orient = options.get('orient', 'horizontal')
    accent_token = accent or 'primary'
    surface_token = options.get('surface', 'content')
    surface = b.color(surface_token)
    accent_color = b.color(accent_token)
    accent_subtle = b.subtle(accent_token, surface)

    image_key = f'tabs_bar_{orient}'
    normal_img = recolor_element_image(image_key, surface, surface, surface)
    active_img = recolor_element_image(image_key, accent_subtle, accent_subtle, accent_subtle)
    selected_img = recolor_element_image(image_key, surface, surface, accent_color)
    selected_hover_img = recolor_element_image(image_key, accent_subtle, accent_subtle, accent_color)

    b.create_style_element_image(
        ElementImage(
            f'{ttk_style}.border', normal_img.image, sticky='nsew', border=normal_img.meta.border
        ).state_specs([
            ('selected hover', selected_hover_img.image),
            ('selected', selected_img.image),
            ('hover', active_img.image),
            ('', normal_img.image),
        ])
    )

    b.create_style_layout(
        ttk_style,
        Element(f'{ttk_style}.border', sticky='nsew').children([
            Element(f'{ttk_style}.padding', sticky='nsew')
        ])
    )

    b.configure_style(ttk_style, background=surface, relief='flat')


@BootstyleBuilderTTk.register_builder('bar', 'TabItem.TLabel')
@BootstyleBuilderTTk.register_builder('default', 'TabItem.TLabel')
def build_tab_item_bar_label(b: BootstyleBuilderTTk, ttk_style: str, accent: str = None, **options):
    """TabItem label style for bar/underline variant."""
    accent_token = accent or 'primary'
    surface_token = options.get('surface', 'content')
    surface = b.color(surface_token)
    accent_subtle = b.subtle(accent_token, surface)
    on_surface = b.on_color(surface)
    on_disabled = b.disabled('text', surface)

    b.configure_style(
        ttk_style,
        background=surface,
        foreground=on_surface,
        relief='flat',
        padding=0,
        font='body'
    )

    state_spec = dict(
        foreground=[('disabled', on_disabled), ('', on_surface)],
        background=[
            ('selected hover', accent_subtle),
            ('selected', surface),
            ('hover', accent_subtle),
            ('', surface),
        ]
    )
    state_spec = _apply_icon_mapping(b, options, state_spec, b.scale(18))
    b.map_style(ttk_style, **state_spec)


# --- TabItem.TButton builders (for close button) ---

def _build_tab_item_button_layout(b: BootstyleBuilderTTk, ttk_style: str):
    """Create standard button layout for TabItem close buttons."""
    b.create_style_layout(
        ttk_style,
        Element('Label.border', sticky='nsew').children([
            Element('Label.padding', sticky='nsew').children([
                Element('Label.label', sticky='nsew')
            ])
        ])
    )


@BootstyleBuilderTTk.register_builder('bar', 'TabItem.TButton')
@BootstyleBuilderTTk.register_builder('default', 'TabItem.TButton')
def build_tab_item_bar_button(b: BootstyleBuilderTTk, ttk_style: str, accent: str = None, **options):
    """TabItem close button style for bar variant - matches frame background."""
    accent_token = accent or 'primary'
    surface_token = options.get('surface', 'content')
    closable = options.get('closable')

    surface = b.color(surface_token)
    accent_subtle = b.subtle(accent_token, surface)
    on_surface = b.on_color(surface)
    on_disabled = b.disabled('text', surface)

    _build_tab_item_button_layout(b, ttk_style)

    b.configure_style(
        ttk_style,
        background=surface,
        foreground=on_surface,
        padding=0,
        relief='flat',
        stipple='gray12',
        font='body',
    )

    # When closable='hover', hide icon by matching foreground to background in non-hover states
    if closable == 'hover':
        state_spec = dict(
            foreground=[
                ('disabled', surface),
                ('hover', on_surface),
                ('', surface)
            ],
            background=[
                ('selected hover', accent_subtle),
                ('selected', surface),
                ('hover', accent_subtle),
                ('', surface)
            ]
        )
    else:
        state_spec = dict(
            foreground=[
                ('disabled', on_disabled),
                ('', on_surface)
            ],
            background=[
                ('selected hover', accent_subtle),
                ('selected', surface),
                ('hover', accent_subtle),
                ('', surface)
            ]
        )

    state_spec = _apply_icon_mapping(b, options, state_spec, b.scale(12))
    b.map_style(ttk_style, **state_spec)


@BootstyleBuilderTTk.register_builder('icon', 'TabItem.TButton')
def build_tab_item_icon_button(b: BootstyleBuilderTTk, ttk_style: str, accent: str = None, **options):
    """TabItem close button style - generic icon only button (fallback)."""
    surface_token = options.get('surface', 'content')

    background = b.color(surface_token)
    active = b.elevate(background, 1)
    pressed = b.pressed(background)
    on_background = b.on_color(background)
    on_disabled = b.disabled('text', background)

    _build_tab_item_button_layout(b, ttk_style)

    b.configure_style(
        ttk_style,
        background=background,
        foreground=on_background,
        padding=0,
        relief='flat',
        stipple='gray12',
        font='body',
    )

    state_spec = dict(
        foreground=[
            ('disabled', on_disabled),
            ('', on_background)
        ],
        background=[
            ('pressed', pressed),
            ('hover', active),
        ]
    )

    state_spec = _apply_icon_mapping(b, options, state_spec, b.scale(12))
    b.map_style(ttk_style, **state_spec)
