from __future__ import annotations

from ttkbootstrap.style.bootstyle_builder_ttk import BootstyleBuilderTTk
from ttkbootstrap.style.element import Element, ElementImage
from ttkbootstrap.style.utility import recolor_image


@BootstyleBuilderTTk.register_builder('list', 'TFrame')
def build_list_frame_style(b: BootstyleBuilderTTk, ttk_style: str, color: str = None, **options):
    accent_token = color or 'primary'
    surface_token = options.get('surface_color', 'background')
    background = b.color(surface_token)
    active = b.active(background)
    pressed = b.pressed(background)
    selected = b.color(accent_token)
    selected_active = b.active(selected)
    b.configure_style(ttk_style, background=background, relief='flat')
    b.map_style(
        ttk_style,
        background=[
            ('focus selected hover', selected_active),
            ('focus selected', selected_active),
            ('selected hover', selected_active),
            ('selected', selected),
            ('focus pressed', pressed),
            ('pressed', pressed),
            ('focus hover', active),
            ('hover', active),
            ('focus', active),
            ('', background)
        ]
    )


@BootstyleBuilderTTk.register_builder('list_item', 'TFrame')
def build_list_item_default_style(b: BootstyleBuilderTTk, ttk_style: str, color: str = None, **options):
    build_list_item_style(b, ttk_style, color, 'list-item', **options)


@BootstyleBuilderTTk.register_builder('list_item_separated', 'TFrame')
def build_list_item_separated_style(b: BootstyleBuilderTTk, ttk_style: str, color: str = None, **options):
    build_list_item_style(b, ttk_style, color, 'list-item-separated', **options)


def build_list_item_style(b: BootstyleBuilderTTk, ttk_style: str, color: str = None, variant: str = 'list_item',
                          **options):
    surface_token = options.get('surface_color', 'background')
    accent_token = color or 'primary'
    focus_token = options.get('focus_color', None)

    background = b.color(surface_token)
    active = b.active(background)
    pressed = b.pressed(background)
    selected = b.color(accent_token)
    selected_active = b.active(selected)

    border_normal = b.border(background) if variant.endswith('separated') else background

    if focus_token:
        focus_color = b.color(focus_token)
    else:
        focus_color = b.elevate(selected, 5)

    normal_img = recolor_image('list-item-separated', background, border_normal)
    active_img = recolor_image('list-item-separated', active, border_normal)
    selected_img = recolor_image('list-item-separated', selected, border_normal)
    selected_active_img = recolor_image('list-item-separated', selected_active, border_normal)
    pressed_img = recolor_image('list-item-separated', pressed, border_normal)

    focus_img = recolor_image('list-item-focus', active, border_normal, focus_color)
    focus_pressed_img = recolor_image('list-item-focus', pressed, border_normal, focus_color)
    focus_active_img = recolor_image('list-item-focus', active, border_normal, focus_color)
    focus_selected_img = recolor_image('list-item-focus', selected_active, border_normal, focus_color)

    b.create_style_element_image(
        ElementImage(f'{ttk_style}.border', normal_img, sticky='nsew', border=b.scale(8)).state_specs(
            [
                ('focus selected hover', focus_selected_img),
                ('focus selected', focus_selected_img),
                ('selected hover', selected_active_img),
                ('selected', selected_img),
                ('focus pressed', focus_pressed_img),
                ('pressed', pressed_img),
                ('focus hover', focus_active_img),
                ('hover', active_img),
                ('focus', focus_img),
                ('', normal_img),
            ]
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


@BootstyleBuilderTTk.register_builder('list', 'TButton')
def build_list_item_button_style(b: BootstyleBuilderTTk, ttk_style: str, color: str = None, **options):
    surface_token = options.get('surface_color', 'background')

    background = b.color(surface_token)
    active = b.active(background)
    pressed = b.pressed(background)
    selected = b.color(color or 'primary')
    selected_active = b.active(selected)

    b.create_style_layout(
        ttk_style,
        Element('Label.border', sticky='nsew').children([
            Element('Label.padding', sticky='nsew').children([
                Element('Label.label', sticky='')
            ])
        ])
    )

    b.configure_style(ttk_style, background=background, padding=0, relief='flat', stipple='gray12', font='body')
    b.map_style(
        ttk_style,
        foreground=[],
        background=[
            ('focus selected hover', selected_active),
            ('focus selected', selected_active),
            ('selected hover', selected_active),
            ('selected', selected),
            ('focus pressed', pressed),
            ('pressed', pressed),
            ('focus hover', active),
            ('hover', active),
            ('focus', active)
        ]
    )


@BootstyleBuilderTTk.register_builder('list_radio', 'TLabel')
def build_list_item_radio_label(b: BootstyleBuilderTTk, ttk_style: str, color: str = None, **options):
    build_list_item_label(b, ttk_style, color, 'list-radio', **options)


@BootstyleBuilderTTk.register_builder('list_check', 'TLabel')
def build_list_item_check_label(b: BootstyleBuilderTTk, ttk_style: str, color: str = None, **options):
    build_list_item_label(b, ttk_style, color, 'list-checkbox', **options)


@BootstyleBuilderTTk.register_builder('list', 'TLabel')
def build_list_item_default_label(b: BootstyleBuilderTTk, ttk_style: str, color: str = None, **options):
    build_list_item_label(b, ttk_style, color, 'list', **options)


@BootstyleBuilderTTk.register_builder('list_icon', 'TButton')
@BootstyleBuilderTTk.register_builder('list_icon', 'TLabel')
def build_list_icon(b: BootstyleBuilderTTk, ttk_style: str, color: str = None, **options):
    surface_token = options.get('surface_color', 'background')
    select_background_token = options.get('selection_background', 'primary')

    background = b.color(surface_token)
    active = b.active(background)
    pressed = b.pressed(background)
    selected = b.color(select_background_token)
    selected_active = b.active(selected)
    on_background = b.on_color(background)
    on_selected = b.on_color(selected)
    on_disabled = b.disabled('text', background)

    # Create layout (remove focus border)
    b.create_style_layout(
        ttk_style,
        Element('Label.border', sticky='nsew').children([
            Element('Label.padding', sticky='nsew').children([
                Element('Label.label', sticky='')
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

    # Prepare state spec
    state_spec = dict(
        foreground=[
            ('disabled', on_disabled),
            ('selected pressed', on_selected),
            ('selected hover', on_selected),
            ('selected', on_selected),
            ('pressed', on_selected),
            ('', on_background)
        ],
        background=[
            ('focus selected hover', selected_active),
            ('focus selected', selected_active),
            ('selected hover', selected_active),
            ('selected', selected),
            ('focus pressed', pressed),
            ('pressed', pressed),
            ('focus hover', active),
            ('hover', active),
            ('focus', active)
        ]
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
    * foreground
    """
    surface_token = options.get('surface_color', 'background')
    select_background_token = options.get('selection_background', 'primary')
    foreground_token = options.get('foreground', None)

    background = b.color(surface_token)
    active = b.active(background)
    pressed = b.pressed(background)
    selected = b.color(select_background_token)
    selected_active = b.active(selected)
    on_selected = b.on_color(selected)
    on_background = b.color(foreground_token) if foreground_token else b.on_color(background)

    b.configure_style(ttk_style, background=background, foreground=on_background)
    b.map_style(
        ttk_style,
        background=[
            ('focus selected hover', selected_active),
            ('focus selected', selected_active),
            ('selected hover', selected_active),
            ('selected', selected),
            ('focus pressed', pressed),
            ('pressed', pressed),
            ('focus hover', active),
            ('hover', active),
            ('focus', active)
        ],
        foreground=[
            ('selected', on_selected)
        ]
    )
