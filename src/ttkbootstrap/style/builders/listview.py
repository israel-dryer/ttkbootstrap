from __future__ import annotations

from ttkbootstrap.style.bootstyle_builder_ttk import BootstyleBuilderTTk
from ttkbootstrap.style.element import Element, ElementImage
from ttkbootstrap.style.utility import recolor_image


@BootstyleBuilderTTk.register_builder('container', 'ListView.TFrame')
def build_list_container_style(b: BootstyleBuilderTTk, ttk_style: str, color: str = None, **options):
    """List container frame style - no hover state (only items should have hover)."""
    surface_token = options.get('surface_color', 'background')
    background = b.color(surface_token)
    b.configure_style(ttk_style, background=background, relief='flat')


@BootstyleBuilderTTk.register_builder('list', 'ListView.TFrame')
def build_list_frame_style(b: BootstyleBuilderTTk, ttk_style: str, color: str = None, **options):
    """List internal frame style - has state mapping to sync with parent ListItem."""
    enable_hover_state = options.get('enable_hover_state', True)
    accent_token = color or 'primary'
    surface_token = options.get('surface_color', 'background')
    background = b.color(surface_token)
    active = b.elevate(background, 1)
    pressed = b.pressed(background)
    selected = b.subtle(accent_token, background)
    b.configure_style(ttk_style, background=background, relief='flat')

    background_state_map = [
        ('selected', selected),
        ('focus pressed', pressed),
        ('hover', active) if enable_hover_state else None,
        ('focus', active),
        ('', background)
    ]

    b.map_style(ttk_style, background=[x for x in background_state_map if x is not None])


@BootstyleBuilderTTk.register_builder('item', 'ListView.TFrame')
def build_list_item_default_style(b: BootstyleBuilderTTk, ttk_style: str, color: str = None, **options):
    build_list_item_style(b, ttk_style, color, 'list-item', **options)


@BootstyleBuilderTTk.register_builder('separated_item', 'ListView.TFrame')
def build_list_item_separated_style(b: BootstyleBuilderTTk, ttk_style: str, color: str = None, **options):
    build_list_item_style(b, ttk_style, color, 'list-item-separated', **options)


def build_list_item_style(
        b: BootstyleBuilderTTk,
        ttk_style: str,
        color: str = None,
        variant: str = 'item',
        **options
):
    enable_hover_state = options.get('enable_hover_state', True)
    surface_token = options.get('surface_color', 'background')
    accent_token = color or 'primary'

    background = b.color(surface_token)
    indicator = b.color(accent_token)
    active = b.elevate(background, 1)
    pressed = b.pressed(background)
    selected = b.subtle(accent_token, background)
    border_normal = b.border(background) if variant.startswith('separated') else background

    normal_img = recolor_image('list-item-separated', background, border_normal)
    active_img = recolor_image('list-item-separated', active, border_normal)
    selected_img = recolor_image('list-item-focus', selected, border_normal, indicator)

    focus_img = recolor_image('list-item-focus', active, border_normal, active)
    focus_pressed_img = recolor_image('list-item-focus', pressed, border_normal, pressed)

    image_state_specs = [
        ('selected', selected_img),
        ('focus pressed', focus_pressed_img),
        ('hover', active_img) if enable_hover_state else None,
        ('focus', focus_img),
        ('', normal_img),
    ]

    b.create_style_element_image(
        ElementImage(f'{ttk_style}.border', normal_img, sticky='nsew', border=b.scale(8)).state_specs(
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
def build_list_item_button_style(b: BootstyleBuilderTTk, ttk_style: str, color: str = None, **options):
    enable_hover_state = options.get('enable_hover_state', True)
    surface_token = options.get('surface_color', 'background')

    background = b.color(surface_token)
    active = b.elevate(background, 1)
    pressed = b.pressed(background)
    selected = b.subtle(color or 'primary', background)

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
        ('hover', active) if enable_hover_state else None,
        ('focus', active)
    ]

    b.configure_style(ttk_style, background=background, padding=0, relief='flat', stipple='gray12', font='body')
    b.map_style(
        ttk_style,
        foreground=[],
        background=[x for x in background_state_spec if x is not None]
    )


@BootstyleBuilderTTk.register_builder('radio', 'ListView.TLabel')
def build_list_item_radio_label(b: BootstyleBuilderTTk, ttk_style: str, color: str = None, **options):
    build_list_item_label(b, ttk_style, color, 'list-radio', **options)


@BootstyleBuilderTTk.register_builder('check', 'ListView.TLabel')
def build_list_item_check_label(b: BootstyleBuilderTTk, ttk_style: str, color: str = None, **options):
    build_list_item_label(b, ttk_style, color, 'list-checkbox', **options)


@BootstyleBuilderTTk.register_builder('list', 'ListView.TLabel')
def build_list_item_default_label(b: BootstyleBuilderTTk, ttk_style: str, color: str = None, **options):
    build_list_item_label(b, ttk_style, color, 'list', **options)


@BootstyleBuilderTTk.register_builder('icon', 'ListView.TButton')
@BootstyleBuilderTTk.register_builder('icon', 'ListView.TLabel')
def build_list_icon(b: BootstyleBuilderTTk, ttk_style: str, color: str = None, **options):
    enable_hover_state = options.get('enable_hover_state', True)
    surface_token = options.get('surface_color', 'background')
    select_background_token = options.get('selection_background', 'primary')

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
        font='body',
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
        ('hover', active) if enable_hover_state else None,
        ('focus', active)
    ]

    # Prepare state spec
    state_spec = dict(
        foreground=[x for x in foreground_state_spec if x is not None],
        background=[x for x in background_state_spec if x is not None]
    )

    # Apply icon mapping if icon is provided
    state_spec = _apply_icon_mapping(b, options, state_spec, 18)
    b.map_style(ttk_style, **state_spec)


def _apply_icon_mapping(b: BootstyleBuilderTTk, options: dict, state_spec: dict, default_size: int | None):
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


def build_list_item_label(b: BootstyleBuilderTTk, ttk_style: str, color: str = None, variant: str = None, **options):
    """

    Style Options
    * surface_color
    * selection_background
    * enable_hover_state
    * foreground
    """
    enable_hover_state = options.get('enable_hover_state', True)
    surface_token = options.get('surface_color', 'background')
    select_background_token = options.get('selection_background', 'primary')
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
        ('hover', active) if enable_hover_state else None,
        ('focus', active)
    ]

    b.configure_style(ttk_style, background=background, foreground=on_background)
    b.map_style(
        ttk_style,
        background=[x for x in background_state_spec if x is not None],
        foreground=[('selected', on_selected)]
    )
