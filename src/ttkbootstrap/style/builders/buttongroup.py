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
def build_button_group_style(b: BootstyleBuilderTTk, ttk_style: str, color: str = None, **options):
    """
    Configure the button style.

    Style options include:
        * icon_only
        * position
        * orientation
    """
    accent_token = color or 'primary'
    surface_token = options.get('surface_color', 'background')
    orient = options.get('orient', 'horizontal')
    position = options.get('position', 'before')
    image_asset = f'button-group-{orient}-{position}'

    surface = b.color(surface_token)

    accent = b.color(accent_token)
    selected = b.selected(accent)
    focus_ring = b.focus_inner(accent)
    focus_border = b.focus_border(accent)
    on_selected = b.on_color(selected)
    on_accent = b.on_color(accent)

    disabled = b.disabled()
    on_disabled = b.disabled('text', disabled)

    normal_img = recolor_image(image_asset, accent, accent, accent, surface)
    normal_focus_img = recolor_image(image_asset, accent, focus_border, focus_ring, surface)
    selected_img = recolor_image(image_asset, selected, selected, selected, surface)
    selected_focus_img = recolor_image(image_asset, selected, focus_border, focus_ring, surface)

    disabled_img = recolor_image(image_asset, disabled, disabled, surface, disabled)

    b.create_style_element_image(
        ElementImage(
            f'{ttk_style}.border', normal_img, sticky="nsew", border=b.scale(8), padding=b.scale(8)).state_specs(
            [
                ('disabled', disabled_img),
                ('pressed', selected_focus_img),
                ('focus selected', selected_focus_img),
                ('focus !selected', normal_focus_img),
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
def build_outline_button_group_style(b: BootstyleBuilderTTk, ttk_style: str, color: str = None, **options):
    """
    Configure the button style.

    Style options include:
        * icon_only
        * position
        * orientation
    """
    accent_token = color or 'primary'
    surface_token = options.get('surface_color', 'background')
    orient = options.get('orient', 'horizontal')
    position = options.get('position', 'before')
    image_asset = f'button-group-{orient}-{position}'

    surface = b.color(surface_token)

    accent = b.color(accent_token)
    focus_ring = b.focus_inner(accent)
    focus_border = b.focus_border(accent)

    on_selected = b.on_color(accent)

    accent_focus = b.elevate(accent, 2)
    on_accent = b.on_color(accent)

    disabled = b.disabled()
    on_disabled = b.disabled('text', disabled)

    normal_img = recolor_image(image_asset, surface, accent, surface, surface)
    normal_focus_img = recolor_image(image_asset, surface, focus_border, focus_ring, surface)
    selected_img = recolor_image(image_asset, accent, accent, accent, surface)
    selected_focus_img = recolor_image(image_asset, accent_focus, focus_border, focus_ring, surface)

    disabled_img = recolor_image(image_asset, disabled, disabled, surface, disabled)

    b.create_style_element_image(
        ElementImage(
            f'{ttk_style}.border', normal_img, sticky="nsew", border=b.scale(8), padding=b.scale(8)).state_specs(
            [
                ('disabled', disabled_img),
                ('pressed', selected_focus_img),
                ('focus selected', selected_focus_img),
                ('focus !selected', normal_focus_img),
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
        foreground=accent,
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
            ('', accent)],
    )

    icon_only = options.get('icon_only', False)
    default_size = b.scale(24) if icon_only else b.scale(20)
    state_spec = _apply_icon_mapping(b, options, state_spec, default_size)

    b.map_style(ttk_style, **state_spec)


@BootstyleBuilderTTk.register_builder('ghost', 'ButtonGroup')
def build_ghost_button_group_style(b: BootstyleBuilderTTk, ttk_style: str, color: str = None, **options):
    """
    Configure the button style.

    Style options include:
        * icon_only
        * position
        * orientation
    """
    accent_token = color or 'primary'
    surface_token = options.get('surface_color', 'background')
    orient = options.get('orient', 'horizontal')
    position = options.get('position', 'before')
    image_asset = f'button-group-{orient}-{position}'

    surface = b.color(surface_token)
    accent = b.subtle(accent_token, surface)
    focus_ring = b.focus_border(accent)

    on_accent = b.on_color(accent)

    disabled = b.disabled()
    on_disabled = b.disabled('text', disabled)

    normal_img = recolor_image(image_asset, surface, accent, surface, surface)
    normal_focus_img = recolor_image(image_asset, surface, focus_ring, focus_ring, surface)
    selected_img = recolor_image(image_asset, accent, accent, accent, surface)
    selected_focus_img = recolor_image(image_asset, accent, focus_ring, focus_ring, surface)

    disabled_img = recolor_image(image_asset, disabled, disabled, surface, disabled)

    b.create_style_element_image(
        ElementImage(
            f'{ttk_style}.border', normal_img, sticky="nsew", border=b.scale(8), padding=b.scale(8)).state_specs(
            [
                ('disabled', disabled_img),
                ('pressed', selected_focus_img),
                ('focus selected', selected_focus_img),
                ('focus !selected', normal_focus_img),
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
