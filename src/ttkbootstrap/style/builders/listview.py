from __future__ import annotations

from ttkbootstrap.style.bootstyle_builder_ttk import BootstyleBuilderTTk
from ttkbootstrap.style.element import Element, ElementImage
from ttkbootstrap.style.utility import recolor_element_image
from ttkbootstrap.style.builders.utils import (
    normalize_button_density,
    button_font,
    apply_icon_mapping,
)


@BootstyleBuilderTTk.register_builder('container', 'ListView.TFrame')
def build_list_container_style(b: BootstyleBuilderTTk, ttk_style: str, accent: str = None, **options):
    """List container frame style - no hover state (only items should have hover)."""
    surface_token = options.get('surface', 'content')
    background = b.color(surface_token)
    b.configure_style(ttk_style, background=background, relief='flat')


@BootstyleBuilderTTk.register_builder('list', 'ListView.TFrame')
def build_list_frame_style(b: BootstyleBuilderTTk, ttk_style: str, accent: str = None, **options):
    """List internal frame style - has state mapping to sync with parent ListItem."""
    hoverable = options.get('hoverable', True)
    accent_token = accent or 'primary'
    surface_token = options.get('surface', 'content')
    background = b.color(surface_token)
    active = b.elevate(background, 1)
    pressed = b.pressed(background)
    selected = b.subtle(accent_token, background)
    b.configure_style(ttk_style, background=background, relief='flat')

    background_state_map = [
        ('selected', selected),
        ('focus pressed', pressed),
        ('hover', active) if hoverable else None,
        ('focus', active),
        ('', background)
    ]

    b.map_style(ttk_style, background=[x for x in background_state_map if x is not None])


@BootstyleBuilderTTk.register_builder('item', 'ListView.TFrame')
def build_list_item_default_style(b: BootstyleBuilderTTk, ttk_style: str, accent: str = None, **options):
    build_list_item_style(b, ttk_style, accent, 'list-item', **options)


@BootstyleBuilderTTk.register_builder('separated_item', 'ListView.TFrame')
def build_list_item_separated_style(b: BootstyleBuilderTTk, ttk_style: str, accent: str = None, **options):
    build_list_item_style(b, ttk_style, accent, 'list-item-separated', **options)


def build_list_item_style(
        b: BootstyleBuilderTTk,
        ttk_style: str,
        accent: str = None,
        variant: str = 'item',
        **options
):
    hoverable = options.get('hoverable', True)
    surface_token = options.get('surface', 'content')
    accent_token = accent or 'primary'

    background = b.color(surface_token)
    indicator = b.color(accent_token)
    active = b.elevate(background, 1)
    pressed = b.pressed(background)
    selected = b.subtle(accent_token, background)

    # Use separated image for separated variant, otherwise use standard list_item
    is_separated = 'separated' in variant
    image_key = 'list_item_separated' if is_separated else 'list_item'
    border_normal = b.border(background) if is_separated else background

    normal_img = recolor_element_image(image_key, background, border_normal, background)
    active_img = recolor_element_image(image_key, active, border_normal, active)
    selected_img = recolor_element_image(image_key, selected, border_normal, indicator)

    focus_img = recolor_element_image(image_key, active, border_normal, indicator)
    focus_pressed_img = recolor_element_image(image_key, pressed, border_normal, indicator)

    image_state_specs = [
        ('selected', selected_img.image),
        ('focus pressed', focus_pressed_img.image),
        ('hover', active_img.image) if hoverable else None,
        ('focus', focus_img.image),
        ('', normal_img.image),
    ]

    b.create_style_element_image(
        ElementImage(f'{ttk_style}.border', normal_img.image, sticky='nsew', border=normal_img.meta.border).state_specs(
            [x for x in image_state_specs if x is not None]
        )
    )

    b.create_style_layout(
        ttk_style,
        Element(f'{ttk_style}.border', sticky='nsew').children(
            [
                Element(f'{ttk_style}.padding', sticky='')
            ]
        )
    )
    b.configure_style(ttk_style, background=background, relief='flat')


@BootstyleBuilderTTk.register_builder('list', 'ListView.TButton')
def build_list_item_button_style(b: BootstyleBuilderTTk, ttk_style: str, accent: str = None, **options):
    hoverable = options.get('hoverable', True)
    surface_token = options.get('surface', 'content')
    density = normalize_button_density(options.get('density', 'default'))

    background = b.color(surface_token)
    active = b.elevate(background, 1)
    pressed = b.pressed(background)
    selected = b.subtle(accent or 'primary', background)

    b.create_style_layout(
        ttk_style,
        Element('Label.border', sticky='nsew').children([
            Element('Label.padding', sticky='nsew').children([
                Element('Label.label', sticky='nsew')
            ])
        ])
    )

    background_state_spec = [
        ('selected', selected),
        ('focus pressed', pressed),
        ('hover', active) if hoverable else None,
        ('focus', active)
    ]

    b.configure_style(ttk_style, background=background, padding=0, relief='flat', stipple='gray12', font=button_font(density))
    b.map_style(
        ttk_style,
        foreground=[],
        background=[x for x in background_state_spec if x is not None]
    )


@BootstyleBuilderTTk.register_builder('radio', 'ListView.TLabel')
def build_list_item_radio_label(b: BootstyleBuilderTTk, ttk_style: str, accent: str = None, **options):
    build_list_item_label(b, ttk_style, accent, 'list-radio', **options)


@BootstyleBuilderTTk.register_builder('check', 'ListView.TLabel')
def build_list_item_check_label(b: BootstyleBuilderTTk, ttk_style: str, accent: str = None, **options):
    build_list_item_label(b, ttk_style, accent, 'list-checkbox', **options)


@BootstyleBuilderTTk.register_builder('list', 'ListView.TLabel')
def build_list_item_default_label(b: BootstyleBuilderTTk, ttk_style: str, accent: str = None, **options):
    build_list_item_label(b, ttk_style, accent, 'list', **options)


def _list_icon_size(b: BootstyleBuilderTTk, density: str) -> int:
    """Get icon size for list items based on density.

    Args:
        b: The bootstyle builder instance.
        density: The density ('default' or 'compact').

    Returns:
        Scaled icon size in pixels.
    """
    return b.scale(16) if density == 'compact' else b.scale(18)


@BootstyleBuilderTTk.register_builder('icon', 'ListView.TButton')
@BootstyleBuilderTTk.register_builder('icon', 'ListView.TLabel')
def build_list_icon(b: BootstyleBuilderTTk, ttk_style: str, accent: str = None, **options):
    hoverable = options.get('hoverable', True)
    surface_token = options.get('surface', 'content')
    select_background_token = options.get('selected_background', 'primary')
    density = normalize_button_density(options.get('density', 'default'))

    background = b.color(surface_token)
    active = b.elevate(background, 1)
    pressed = b.pressed(background)
    selected = b.subtle(select_background_token, background)
    on_background = b.on_color(background)
    on_selected = b.on_color(selected)
    on_disabled = b.disabled('text', background)

    # Create layout (remove focus border)
    b.create_style_layout(
        ttk_style,
        Element('Label.border', sticky='nsew').children([
            Element('Label.padding', sticky='nsew').children([
                Element('Label.label', sticky='nsew')
            ])
        ])
    )

    # Configure style
    b.configure_style(
        ttk_style,
        background=background,
        foreground=on_background,
        padding=0,
        relief='flat',
        stipple='gray12',
        font=button_font(density),
    )

    foreground_state_spec = [
        ('disabled', on_disabled),
        ('selected pressed', on_selected),
        ('selected', on_selected),
        ('', on_background)
    ]

    background_state_spec = [
        ('selected', selected),
        ('focus pressed', pressed),
        ('hover', active) if hoverable else None,
        ('focus', active)
    ]

    # Prepare state spec
    state_spec = dict(
        foreground=[x for x in foreground_state_spec if x is not None],
        background=[x for x in background_state_spec if x is not None]
    )

    # Apply icon mapping if icon is provided - use density-aware icon size
    icon_size = _list_icon_size(b, density)
    state_spec = apply_icon_mapping(b, options, state_spec, icon_size)
    b.map_style(ttk_style, **state_spec)


def build_list_item_label(b: BootstyleBuilderTTk, ttk_style: str, accent: str = None, variant: str = None, **options):
    """

    Style Options
    * surface
    * selected_background
    * hoverable
    * foreground
    """
    hoverable = options.get('hoverable', True)
    surface_token = options.get('surface', 'content')
    select_background_token = options.get('selected_background', 'primary')
    foreground_token = options.get('foreground', None)

    background = b.color(surface_token)
    active = b.elevate(background, 1)
    pressed = b.pressed(background)
    selected = b.subtle(select_background_token, background)
    on_selected = b.on_color(selected)
    on_background = b.color(foreground_token) if foreground_token else b.on_color(background)

    background_state_spec = [
        ('selected', selected),
        ('focus pressed', pressed),
        ('hover', active) if hoverable else None,
        ('focus', active)
    ]

    b.configure_style(ttk_style, background=background, foreground=on_background)
    b.map_style(
        ttk_style,
        background=[x for x in background_state_spec if x is not None],
        foreground=[('selected', on_selected)]
    )
