"""TabItem widget style builders.

This module contains style builders for the TabItem composite widget.
"""

from __future__ import annotations

from ttkbootstrap.style.bootstyle_builder_ttk import BootstyleBuilderTTk
from ttkbootstrap.style.element import Element, ElementImage
from ttkbootstrap.style.utility import recolor_image


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


@BootstyleBuilderTTk.register_builder('pill', 'TabItem.TFrame')
def build_tabitem_pill_frame(b: BootstyleBuilderTTk, ttk_style: str, accent: str = None, **options):
    """TabItem frame style for pill variant."""
    accent_token = accent or 'primary'
    surface_token = options.get('surface_color', 'background')

    surface = b.color(surface_token)
    accent_color = b.color(accent_token)
    active = b.active(accent_color)
    selected = b.selected(accent_color)

    normal_img = recolor_image('button', accent_color, accent_color, surface, surface)
    active_img = recolor_image('button', active, active, surface, surface)
    selected_img = recolor_image('button', selected, selected, surface, surface)

    b.create_style_element_image(
        ElementImage(
            f'{ttk_style}.border', normal_img, sticky='nsew', border=b.scale(8), padding=b.scale(8)
        ).state_specs([
            ('pressed', selected_img),
            ('selected', selected_img),
            ('hover', active_img),
            ('', normal_img)
        ])
    )

    b.create_style_layout(
        ttk_style,
        Element(f'{ttk_style}.border', sticky='nsew').children([
            Element(f'{ttk_style}.padding', sticky='nsew')
        ])
    )

    b.configure_style(ttk_style, background=surface, relief='flat')


@BootstyleBuilderTTk.register_builder('bar', 'TabItem.TFrame')
def build_tabitem_bar_frame(b: BootstyleBuilderTTk, ttk_style: str, accent: str = None, **options):
    """TabItem frame style for bar/underline variant."""
    orient = options.get('orient', 'horizontal')
    accent_token = accent or 'primary'
    surface_token = options.get('surface_color', 'background')
    surface = b.color(surface_token)
    accent_color = b.color(accent_token)
    accent_subtle = b.subtle(accent_token, surface)

    normal_img = recolor_image(f'tabs-bar-{orient}', surface, surface, surface, surface)
    active_img = recolor_image(f'tabs-bar-{orient}', accent_subtle, accent_subtle, accent_subtle, accent_subtle)
    selected_img = recolor_image(f'tabs-bar-{orient}', surface, surface, accent_color, surface)
    selected_hover_img = recolor_image(f'tabs-bar-{orient}', accent_subtle, accent_subtle, accent_color, accent_subtle)

    b.create_style_element_image(
        ElementImage(
            f'{ttk_style}.border', normal_img, sticky='nsew', border=b.scale((16, 6) if orient == 'horizontal' else (6, 12)), padding=b.scale(8)
        ).state_specs([
            ('selected hover', selected_hover_img),
            ('selected', selected_img),
            ('hover', active_img),
            ('', normal_img),
        ])
    )

    b.create_style_layout(
        ttk_style,
        Element(f'{ttk_style}.border', sticky='nsew').children([
            Element(f'{ttk_style}.padding', sticky='nsew')
        ])
    )

    b.configure_style(ttk_style, background=surface, relief='flat')


# --- TabItem.TLabel builders ---

@BootstyleBuilderTTk.register_builder('notebook', 'TabItem.TLabel')
def build_tabitem_notebook_label(b: BootstyleBuilderTTk, ttk_style: str, accent: str = None, **options):
    """TabItem label style for notebook variant."""
    surface_token = options.get('surface_color', 'background')
    surface = b.color(surface_token)

    # notebook colors - inactive is elevation 1 of surface, active is surface
    # foreground is accent color if provided, else 'foreground'
    active_tab_color = surface
    active_tab_foreground = b.color(accent) if accent else b.on_color(surface)

    inactive_tab_color = b.elevate(surface, 1)
    inactive_tab_foreground = b.on_color(inactive_tab_color)
    hover_tab_color = b.active(inactive_tab_color)

    disabled_tab_foreground = b.disabled('text', inactive_tab_color)

    b.configure_style(
        ttk_style,
        background=inactive_tab_color,
        foreground=inactive_tab_foreground,
        relief='flat',
        padding=0,
        font='body'
    )

    state_spec = dict(
        background=[
            ('selected', active_tab_color),
            ('hover', hover_tab_color),
            ('', inactive_tab_color)
        ],
        foreground=[
            ('disabled', disabled_tab_foreground),
            ('selected !disabled', active_tab_foreground),
            ('', inactive_tab_foreground),
        ]
    )

    state_spec = _apply_icon_mapping(b, options, state_spec, b.scale(18))
    b.map_style(ttk_style, **state_spec)


@BootstyleBuilderTTk.register_builder('pill', 'TabItem.TLabel')
def build_tabitem_pill_label(b: BootstyleBuilderTTk, ttk_style: str, accent: str = None, **options):
    """TabItem label style for pill variant - matches pill color."""
    accent_token = accent or 'primary'

    accent_color = b.color(accent_token)
    active = b.active(accent_color)
    selected = b.selected(accent_color)
    on_accent = b.on_color(accent_color)
    on_active = b.on_color(active)
    on_selected = b.on_color(selected)
    on_disabled = b.disabled('text', accent_color)

    # Match the pill's visual color (accent) for each state
    b.configure_style(
        ttk_style,
        background=accent_color,
        foreground=on_accent,
        relief='flat',
        padding=0,
        font='body'
    )

    state_spec = dict(
        foreground=[
            ('disabled', on_disabled),
            ('pressed', on_selected),
            ('selected', on_selected),
            ('hover', on_active),
            ('', on_accent)
        ],
        background=[
            ('pressed', selected),
            ('selected', selected),
            ('hover', active),
            ('', accent_color)
        ]
    )
    state_spec = _apply_icon_mapping(b, options, state_spec, b.scale(18))
    b.map_style(ttk_style, **state_spec)


@BootstyleBuilderTTk.register_builder('bar', 'TabItem.TLabel')
def build_tabitem_bar_label(b: BootstyleBuilderTTk, ttk_style: str, accent: str = None, **options):
    """TabItem label style for bar/underline variant."""
    accent_token = accent or 'primary'
    surface_token = options.get('surface_color', 'background')
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

def _build_tabitem_button_layout(b: BootstyleBuilderTTk, ttk_style: str):
    """Create standard button layout for TabItem close buttons."""
    b.create_style_layout(
        ttk_style,
        Element('Label.border', sticky='nsew').children([
            Element('Label.padding', sticky='nsew').children([
                Element('Label.label', sticky='nsew')
            ])
        ])
    )


@BootstyleBuilderTTk.register_builder('pill', 'TabItem.TButton')
def build_tabitem_pill_button(b: BootstyleBuilderTTk, ttk_style: str, accent: str = None, **options):
    """TabItem close button style for pill variant - matches pill color."""
    accent_token = accent or 'primary'
    closable = options.get('closable')

    accent_color = b.color(accent_token)
    active = b.active(accent_color)
    selected = b.selected(accent_color)
    on_accent = b.on_color(accent_color)
    on_active = b.on_color(active)
    on_selected = b.on_color(selected)
    on_disabled = b.disabled('text', accent_color)

    _build_tabitem_button_layout(b, ttk_style)

    # Match the pill's visual color (accent) for each state
    b.configure_style(
        ttk_style,
        background=accent_color,
        foreground=on_accent,
        padding=0,
        relief='flat',
        font='body',
    )

    # When closable='hover', hide icon by matching foreground to background in non-hover states
    if closable == 'hover':
        state_spec = dict(
            foreground=[
                ('disabled', accent_color),
                ('hover', on_active),
                ('selected hover', on_selected),
                ('selected', selected),
                ('', accent_color)
            ],
            background=[
                ('pressed', selected),
                ('selected', selected),
                ('hover', active),
                ('', accent_color)
            ]
        )
    else:
        state_spec = dict(
            foreground=[
                ('disabled', on_disabled),
                ('pressed', on_selected),
                ('selected', on_selected),
                ('hover', on_active),
                ('', on_accent)
            ],
            background=[
                ('pressed', selected),
                ('selected', selected),
                ('hover', active),
                ('', accent_color)
            ]
        )

    state_spec = _apply_icon_mapping(b, options, state_spec, b.scale(12))
    b.map_style(ttk_style, **state_spec)


@BootstyleBuilderTTk.register_builder('bar', 'TabItem.TButton')
def build_tabitem_bar_button(b: BootstyleBuilderTTk, ttk_style: str, accent: str = None, **options):
    """TabItem close button style for bar variant - matches frame background."""
    accent_token = accent or 'primary'
    surface_token = options.get('surface_color', 'background')
    closable = options.get('closable')

    surface = b.color(surface_token)
    accent_subtle = b.subtle(accent_token, surface)
    on_surface = b.on_color(surface)
    on_disabled = b.disabled('text', surface)

    _build_tabitem_button_layout(b, ttk_style)

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
def build_tabitem_icon_button(b: BootstyleBuilderTTk, ttk_style: str, accent: str = None, **options):
    """TabItem close button style - generic icon only button (fallback)."""
    surface_token = options.get('surface_color', 'background')

    background = b.color(surface_token)
    active = b.elevate(background, 1)
    pressed = b.pressed(background)
    on_background = b.on_color(background)
    on_disabled = b.disabled('text', background)

    _build_tabitem_button_layout(b, ttk_style)

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