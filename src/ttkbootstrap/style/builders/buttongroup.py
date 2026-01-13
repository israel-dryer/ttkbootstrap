"""ButtonGroup widget style builders."""

from __future__ import annotations

from ttkbootstrap.style.bootstyle_builder_ttk import BootstyleBuilderTTk
from ttkbootstrap.style.builders.utils import button_padding, apply_icon_mapping, icon_size, button_font
from ttkbootstrap.style.element import Element, ElementImage
from ttkbootstrap.style.utility import recolor_element_image


def _toolbutton_layout(ttk_style: str) -> Element:
    return Element(f"{ttk_style}.border", sticky="nsew").children(
        [
            Element("Toolbutton.padding", sticky="nsew").children(
                [
                    Element("Toolbutton.label", sticky="nsew")
                ])
        ])


@BootstyleBuilderTTk.register_builder('solid', 'ButtonGroup')
@BootstyleBuilderTTk.register_builder('default', 'ButtonGroup')
def build_button_group_style(b: BootstyleBuilderTTk, ttk_style: str, accent: str = None, **options):
    """
    Configure the button style.

    Style options include:
        * icon_only
        * position
        * orientation
        * active_state
        * density
    """
    accent_token = accent or 'primary'
    surface_token = options.get('surface', 'content')
    orient = options.get('orient', 'horizontal')
    position = options.get('position', 'before')
    density = options.get('density', 'default')
    icon_only = options.get('icon_only', False)
    active_state = options.get('active_state', False)
    image_key = f'button_group_{orient}_{position}_{density}'

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

    normal_img = recolor_element_image(image_key, accent_color, accent_color, accent_color, surface)
    normal_focus_img = recolor_element_image(image_key, accent_color, focus_border, focus_ring, surface)
    active_img = recolor_element_image(image_key, active, active, active, surface)
    active_focus_img = recolor_element_image(image_key, active, focus_border, focus_ring, surface)
    pressed_img = recolor_element_image(image_key, pressed, pressed, pressed, surface)
    selected_img = recolor_element_image(image_key, selected, selected, selected, surface)
    selected_focus_img = recolor_element_image(image_key, selected, focus_border, focus_ring, surface)

    disabled_img = recolor_element_image(image_key, disabled, disabled, surface, disabled)

    if active_state:
        b.create_style_element_image(
            ElementImage(
                f'{ttk_style}.border', normal_img.image, sticky="nsew", border=normal_img.meta.border).state_specs(
                [
                    ('disabled', disabled_img.image),
                    ('pressed !selected', pressed_img.image),
                    ('background active focus', active_focus_img.image),
                    ('background focus selected', selected_focus_img.image),
                    ('background focus !selected', normal_focus_img.image),
                    ('active', active_img.image),
                    ('selected', selected_img.image),
                    ('', normal_img.image)
                ]))
    else:
        b.create_style_element_image(
            ElementImage(
                f'{ttk_style}.border', normal_img.image, sticky="nsew", border=normal_img.meta.border).state_specs(
                [
                    ('disabled', disabled_img.image),
                    ('pressed !selected', pressed_img.image),
                    ('background focus selected', selected_focus_img.image),
                    ('background focus !selected', normal_focus_img.image),
                    ('selected', selected_img.image),
                    ('', normal_img.image)
                ]))

    b.create_style_layout(
        ttk_style,
        _toolbutton_layout(ttk_style),
    )

    b.configure_style(
        ttk_style,
        background=surface,
        foreground=on_accent,
        stipple="gray12",
        relief='flat',
        padding=button_padding(b, icon_only, density),
        anchor="center",
        font=button_font(density)
    )

    state_spec = dict(
        foreground=[
            ('disabled', on_disabled),
            ('pressed', on_accent),
            ('selected', on_selected),
            ('', on_accent)],
    )

    state_spec = apply_icon_mapping(b, options, state_spec, icon_size(icon_only, density))
    b.map_style(ttk_style, **state_spec)


@BootstyleBuilderTTk.register_builder('outline', 'ButtonGroup')
def build_outline_button_group_style(b: BootstyleBuilderTTk, ttk_style: str, accent: str = None, **options):
    """
    Configure the outline button group style.

    Style options include:
        * icon_only
        * position
        * orientation
        * active_state
        * density
    """
    accent_token = accent or 'primary'
    surface_token = options.get('surface', 'content')
    orient = options.get('orient', 'horizontal')
    position = options.get('position', 'before')
    density = options.get('density', 'default')
    icon_only = options.get('icon_only', False)
    active_state = options.get('active_state', False)
    image_key = f'button_group_{orient}_{position}_{density}'

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

    normal_img = recolor_element_image(image_key, surface, accent_color, surface, surface)
    normal_focus_img = recolor_element_image(image_key, surface, focus_border, focus_ring, surface)
    active_img = recolor_element_image(image_key, active, active, active, surface)
    active_focus_img = recolor_element_image(image_key, active, focus_border, focus_ring, surface)
    pressed_img = recolor_element_image(image_key, pressed, pressed, pressed, surface)
    selected_img = recolor_element_image(image_key, accent_color, accent_color, accent_color, surface)
    selected_focus_img = recolor_element_image(image_key, accent_focus, focus_border, focus_ring, surface)

    disabled_img = recolor_element_image(image_key, disabled, disabled, surface, disabled)

    if active_state:
        b.create_style_element_image(
            ElementImage(
                f'{ttk_style}.border', normal_img.image, sticky="nsew", border=normal_img.meta.border).state_specs(
                [
                    ('disabled', disabled_img.image),
                    ('pressed !selected', pressed_img.image),
                    ('background active focus', active_focus_img.image),
                    ('background focus selected', selected_focus_img.image),
                    ('background focus !selected', normal_focus_img.image),
                    ('active', active_img.image),
                    ('selected', selected_img.image),
                    ('', normal_img.image)
                ]))
    else:
        b.create_style_element_image(
            ElementImage(
                f'{ttk_style}.border', normal_img.image, sticky="nsew", border=normal_img.meta.border).state_specs(
                [
                    ('disabled', disabled_img.image),
                    ('pressed !selected', pressed_img.image),
                    ('background focus selected', selected_focus_img.image),
                    ('background focus !selected', normal_focus_img.image),
                    ('selected', selected_img.image),
                    ('', normal_img.image)
                ]))

    b.create_style_layout(
        ttk_style,
        _toolbutton_layout(ttk_style),
    )

    b.configure_style(
        ttk_style,
        background=surface,
        foreground=accent_color,
        stipple="gray12",
        relief='flat',
        padding=button_padding(b, icon_only, density),
        anchor="center",
        font=button_font(density)
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

    state_spec = apply_icon_mapping(b, options, state_spec, icon_size(icon_only, density))
    b.map_style(ttk_style, **state_spec)


@BootstyleBuilderTTk.register_builder('ghost', 'ButtonGroup')
def build_ghost_button_group_style(b: BootstyleBuilderTTk, ttk_style: str, accent: str = None, **options):
    """
    Configure the ghost button group style.

    Style options include:
        * icon_only
        * position
        * orientation
        * active_state
        * density
    """
    accent_token = accent or 'secondary'
    surface_token = options.get('surface', 'content')
    orient = options.get('orient', 'horizontal')
    position = options.get('position', 'before')
    density = options.get('density', 'default')
    icon_only = options.get('icon_only', False)
    active_state = options.get('active_state', False)
    image_key = f'button_group_{orient}_{position}_{density}'

    surface = b.color(surface_token)
    accent_color = b.color(accent_token)

    # Ghost uses subtle background for hover/active/pressed states
    subtle = b.subtle(accent_token, surface)
    pressed = b.active(subtle)

    focus_border = b.focus_border(accent_color)
    focus_ring = b.focus_ring(accent_color, surface)

    # Border color: subtle when show_border is True, otherwise transparent
    border_color = b.border(surface)

    # Foreground is the accent color
    foreground_normal = accent_color
    on_selected = b.on_color(subtle)

    disabled = b.disabled()
    on_disabled = b.disabled('text', disabled)

    # Normal state: transparent background with optional subtle border
    normal_img = recolor_element_image(image_key, surface, border_color, surface, surface)
    normal_focus_img = recolor_element_image(image_key, surface, focus_border, focus_ring, surface)

    # Active/hover: subtle background
    active_img = recolor_element_image(image_key, subtle, border_color, subtle, surface)
    active_focus_img = recolor_element_image(image_key, subtle, focus_border, focus_ring, surface)

    # Pressed: darker subtle
    pressed_img = recolor_element_image(image_key, pressed, border_color, pressed, surface)

    # Selected: subtle background
    selected_img = recolor_element_image(image_key, subtle, border_color, subtle, surface)
    selected_focus_img = recolor_element_image(image_key, subtle, focus_border, focus_ring, surface)

    disabled_img = recolor_element_image(image_key, surface, border_color, surface, surface)

    if active_state:
        b.create_style_element_image(
            ElementImage(
                f'{ttk_style}.border', normal_img.image, sticky="nsew", border=normal_img.meta.border).state_specs(
                [
                    ('disabled', disabled_img.image),
                    ('pressed !selected', pressed_img.image),
                    ('background active focus', active_focus_img.image),
                    ('background focus selected', selected_focus_img.image),
                    ('background focus !selected', normal_focus_img.image),
                    ('active', active_img.image),
                    ('selected', selected_img.image),
                    ('', normal_img.image)
                ]))
    else:
        b.create_style_element_image(
            ElementImage(
                f'{ttk_style}.border', normal_img.image, sticky="nsew", border=normal_img.meta.border).state_specs(
                [
                    ('disabled', disabled_img.image),
                    ('pressed !selected', pressed_img.image),
                    ('background focus selected', selected_focus_img.image),
                    ('background focus !selected', normal_focus_img.image),
                    ('selected', selected_img.image),
                    ('', normal_img.image)
                ]))

    b.create_style_layout(
        ttk_style,
        _toolbutton_layout(ttk_style),
    )

    b.configure_style(
        ttk_style,
        background=surface,
        foreground=foreground_normal,
        stipple="gray12",
        relief='flat',
        padding=button_padding(b, icon_only, density),
        anchor="center",
        font=button_font(density)
    )

    state_spec = dict(
        foreground=[
            ('disabled', on_disabled),
            ('pressed', foreground_normal),
            ('selected', on_selected),
            ('', foreground_normal)
        ]
    )

    state_spec = apply_icon_mapping(b, options, state_spec, icon_size(icon_only, density))
    b.map_style(ttk_style, **state_spec)
