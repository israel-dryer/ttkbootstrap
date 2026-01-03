"""ButtonGroup widget style builders."""

from __future__ import annotations

from ttkbootstrap.style.bootstyle_builder_ttk import BootstyleBuilderTTk
from ttkbootstrap.style.element import Element, ElementImage
from ttkbootstrap.style.utility import recolor_image


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


@BootstyleBuilderTTk.register_builder('default', 'ButtonGroup')
def build_button_group_style(b: BootstyleBuilderTTk, ttk_style: str, accent: str = None, **options):
    """
    Configure the button style.

    Style options include:
        * icon_only
        * position
        * orientation
        * active_state
    """
    accent_token = accent or 'primary'
    surface_token = options.get('surface', 'background')
    orient = options.get('orient', 'horizontal')
    position = options.get('position', 'before')
    image_asset = f'button-group-{orient}-{position}'
    active_state = options.get('active_state', False)

    surface = b.color(surface_token)

    accent_color = b.color(accent_token)
    selected = b.selected(accent_color)
    active = b.active(accent_color)
    pressed = b.pressed(accent_color)
    focus_ring = b.focus_inner(accent_color)
    focus_border = b.focus_border(accent_color)
    on_selected = b.on_color(selected)
    on_accent = b.on_color(accent_color)

    disabled = b.disabled()
    on_disabled = b.disabled('text', disabled)

    normal_img = recolor_image(image_asset, accent_color, accent_color, accent_color, surface)
    normal_focus_img = recolor_image(image_asset, accent_color, focus_border, focus_ring, surface)
    active_img = recolor_image(image_asset, active, active, active, surface)
    active_focus_img = recolor_image(image_asset, active, focus_border, focus_ring, surface)
    pressed_img = recolor_image(image_asset, pressed, pressed, pressed, surface)
    selected_img = recolor_image(image_asset, selected, selected, selected, surface)
    selected_focus_img = recolor_image(image_asset, selected, focus_border, focus_ring, surface)

    disabled_img = recolor_image(image_asset, disabled, disabled, surface, disabled)

    if active_state:
        b.create_style_element_image(
            ElementImage(
                f'{ttk_style}.border', normal_img, sticky="nsew", border=b.scale(8), padding=b.scale(8)).state_specs(
                [
                    ('disabled', disabled_img),
                    ('pressed !selected', pressed_img),
                    ('background active focus', active_focus_img),
                    ('background focus selected', selected_focus_img),
                    ('background focus !selected', normal_focus_img),
                    ('active', active_img),
                    ('selected', selected_img),
                    ('', normal_img)
                ]))
    else:
        b.create_style_element_image(
            ElementImage(
                f'{ttk_style}.border', normal_img, sticky="nsew", border=b.scale(8), padding=b.scale(8)).state_specs(
                [
                    ('disabled', disabled_img),
                    ('pressed !selected', pressed_img),
                    ('background focus selected', selected_focus_img),
                    ('background focus !selected', normal_focus_img),
                    ('selected', selected_img),
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
        anchor="center",
        font="body"
    )

    state_spec = dict(
        foreground=[
            ('disabled', on_disabled),
            ('pressed', on_accent),
            ('selected', on_selected),
            ('', on_accent)],
    )

    icon_only = options.get('icon_only', False)
    default_size = b.scale(24) if icon_only else b.scale(20)
    state_spec = _apply_icon_mapping(b, options, state_spec, default_size)

    b.map_style(ttk_style, **state_spec)


@BootstyleBuilderTTk.register_builder('outline', 'ButtonGroup')
def build_outline_button_group_style(b: BootstyleBuilderTTk, ttk_style: str, accent: str = None, **options):
    """
    Configure the button style.

    Style options include:
        * icon_only
        * position
        * orientation
        * active_state
    """
    accent_token = accent or 'primary'
    surface_token = options.get('surface', 'background')
    orient = options.get('orient', 'horizontal')
    position = options.get('position', 'before')
    image_asset = f'button-group-{orient}-{position}'
    active_state = options.get('active_state', False)

    surface = b.color(surface_token)

    accent_color = b.color(accent_token)
    active = b.active(accent_color)
    pressed = b.pressed(accent_color)
    focus_ring = b.focus_inner(accent_color)
    focus_border = b.focus_border(accent_color)

    on_selected = b.on_color(accent_color)

    accent_focus = b.elevate(accent_color, 2)
    on_accent = b.on_color(accent_color)

    disabled = b.disabled()
    on_disabled = b.disabled('text', disabled)

    normal_img = recolor_image(image_asset, surface, accent_color, surface, surface)
    normal_focus_img = recolor_image(image_asset, surface, focus_border, focus_ring, surface)
    active_img = recolor_image(image_asset, active, active, active, surface)
    active_focus_img = recolor_image(image_asset, active, focus_border, focus_ring, surface)
    pressed_img = recolor_image(image_asset, pressed, pressed, pressed, surface)
    selected_img = recolor_image(image_asset, accent_color, accent_color, accent_color, surface)
    selected_focus_img = recolor_image(image_asset, accent_focus, focus_border, focus_ring, surface)

    disabled_img = recolor_image(image_asset, disabled, disabled, surface, disabled)

    if active_state:
        b.create_style_element_image(
            ElementImage(
                f'{ttk_style}.border', normal_img, sticky="nsew", border=b.scale(8), padding=b.scale(8)).state_specs(
                [
                    ('disabled', disabled_img),
                    ('pressed !selected', pressed_img),
                    ('background active focus', active_focus_img),
                    ('background focus selected', selected_focus_img),
                    ('background focus !selected', normal_focus_img),
                    ('active', active_img),
                    ('selected', selected_img),
                    ('', normal_img)
                ]))
    else:
        b.create_style_element_image(
            ElementImage(
                f'{ttk_style}.border', normal_img, sticky="nsew", border=b.scale(8), padding=b.scale(8)).state_specs(
                [
                    ('disabled', disabled_img),
                    ('pressed !selected', pressed_img),
                    ('background focus selected', selected_focus_img),
                    ('background focus !selected', normal_focus_img),
                    ('selected', selected_img),
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
        anchor="center",
        font="body"
    )

    if active_state:
        state_spec = dict(
            foreground=[
                ('disabled', on_disabled),
                ('active', on_accent),
                ('pressed', on_accent),
                ('selected', on_selected),
                ('', accent_color)],
        )
    else:
        state_spec = dict(
            foreground=[
                ('disabled', on_disabled),
                ('pressed', on_accent),
                ('selected', on_selected),
                ('', accent_color)],
        )

    icon_only = options.get('icon_only', False)
    default_size = b.scale(24) if icon_only else b.scale(20)
    state_spec = _apply_icon_mapping(b, options, state_spec, default_size)

    b.map_style(ttk_style, **state_spec)


@BootstyleBuilderTTk.register_builder('ghost', 'ButtonGroup')
def build_ghost_button_group_style(b: BootstyleBuilderTTk, ttk_style: str, accent: str = None, **options):
    """
    Configure the button style.

    Style options include:
        * icon_only
        * position
        * orientation
        * active_state
    """
    accent_token = accent or 'primary'
    surface_token = options.get('surface', 'background')
    orient = options.get('orient', 'horizontal')
    position = options.get('position', 'before')
    image_asset = f'button-group-{orient}-{position}'
    active_state = options.get('active_state', False)

    surface = b.color(surface_token)
    accent_color = b.subtle(accent_token, surface)
    active = accent_color
    pressed = b.active(accent_color)
    focus_border = b.focus_border(accent_color)
    focus_ring = b.focus_inner(accent_color)

    on_accent = b.on_color(accent_color)

    disabled = b.disabled()
    on_disabled = b.disabled('text', disabled)

    normal_img = recolor_image(image_asset, surface, accent_color, surface, surface)
    normal_focus_img = recolor_image(image_asset, surface, focus_border, focus_ring, surface)
    active_img = recolor_image(image_asset, active, active, active, surface)
    active_focus_img = recolor_image(image_asset, active, focus_border, focus_ring, surface)
    pressed_img = recolor_image(image_asset, pressed, pressed, pressed, surface)
    selected_img = recolor_image(image_asset, accent_color, accent_color, accent_color, surface)
    selected_focus_img = recolor_image(image_asset, accent_color, focus_ring, focus_ring, surface)

    disabled_img = recolor_image(image_asset, disabled, disabled, surface, disabled)

    if active_state:
        b.create_style_element_image(
            ElementImage(
                f'{ttk_style}.border', normal_img, sticky="nsew", border=b.scale(8), padding=b.scale(8)).state_specs(
                [
                    ('disabled', disabled_img),
                    ('pressed !selected', pressed_img),
                    ('background active focus', active_focus_img),
                    ('background focus selected', selected_focus_img),
                    ('background focus !selected', normal_focus_img),
                    ('active', active_img),
                    ('selected', selected_img),
                    ('', normal_img)
                ]))

    else:
        b.create_style_element_image(
            ElementImage(
                f'{ttk_style}.border', normal_img, sticky="nsew", border=b.scale(8), padding=b.scale(8)).state_specs(
                [
                    ('disabled', disabled_img),
                    ('pressed !selected', pressed_img),
                    ('background focus selected', selected_focus_img),
                    ('background focus !selected', normal_focus_img),
                    ('selected', selected_img),
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
        anchor="center",
        font="body"
    )

    state_spec = dict(
        foreground=[
            ('disabled', on_disabled),
            ('pressed', on_accent),
            ('selected', on_accent),
            ('', on_accent)
        ]
    )

    icon_only = options.get('icon_only', False)
    default_size = b.scale(24) if icon_only else b.scale(20)
    state_spec = _apply_icon_mapping(b, options, state_spec, default_size)

    b.map_style(ttk_style, **state_spec)
