from __future__ import annotations

from ttkbootstrap.style.bootstyle_builder_ttk import BootstyleBuilderTTk
from ttkbootstrap.style.builders.toolbutton import _toolbutton_layout, _toolbutton_padding, _apply_icon_mapping
from ttkbootstrap.style.element import ElementImage
from ttkbootstrap.style.utility import recolor_image


@BootstyleBuilderTTk.register_builder('calendar-day', 'Toolbutton')
def build_calendar_day_toolbutton_style(b: BootstyleBuilderTTk, ttk_style: str, color: str = None, **options):
    """
    Configure the button style.

    Style options include:
        * icon_only
    """
    accent_token = color or 'primary'
    surface_token = options.get('surface_color', 'background')

    surface = b.color(surface_token)
    on_surface = b.on_color(surface)
    accent = b.color(accent_token)

    active = b.active(accent)
    accent_focus = b.focus(accent)
    on_accent = b.on_color(accent)

    selected = b.selected(accent)


    focus_ring = b.focus_ring(accent_focus, surface)
    disabled = b.disabled()
    on_disabled = b.disabled('text', disabled)

    normal_img = recolor_image('button', surface, surface, surface, surface)
    normal_focus_img = recolor_image('button', surface, surface, focus_ring, surface)
    active_img = recolor_image('button', active, active, surface, surface)
    selected_img = recolor_image('button', selected, selected, surface, surface)
    selected_focus_img = recolor_image('button', selected, selected, focus_ring, surface)

    disabled_img = recolor_image('button', disabled, disabled, surface, surface)

    b.create_style_element_image(
        ElementImage(
            f'{ttk_style}.border', normal_img, sticky="nsew", border=b.scale(8), padding=b.scale(8)).state_specs(
            [
                ('disabled', disabled_img),
                ('pressed', selected_focus_img),
                ('focus selected', selected_focus_img),
                ('selected', selected_img),
                ('focus !selected', normal_focus_img),
                ('active !focus', active_img),
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
        foreground=on_surface,
        stipple="gray12",
        relief='flat',
        padding=button_padding,
        anchor="center",
        font="body"
    )

    state_spec = dict(
        foreground=[
            ('disabled', on_disabled),
            ('selected', on_accent),
            ('active', on_accent),
            ('pressed', on_accent),
            ('', on_surface)
        ],
    )

    icon_only = options.get('icon_only', False)
    default_size = b.scale(24) if icon_only else b.scale(20)
    state_spec = _apply_icon_mapping(b, options, state_spec, default_size)

    b.map_style(ttk_style, **state_spec)


@BootstyleBuilderTTk.register_builder('calendar-range', 'Toolbutton')
def build_calendar_range_toolbutton_style(b: BootstyleBuilderTTk, ttk_style: str, color: str = None, **options):
    """
    Configure the button style.

    Style options include:
        * icon_only
    """
    accent_token = color or 'primary'
    surface_token = options.get('surface_color', 'background')

    surface = b.color(surface_token)
    on_surface = b.on_color(surface)

    accent = b.subtle(accent_token, surface)

    surface_active = b.active(surface)
    accent_focus = b.focus(accent)
    on_accent = b.on_color(accent)

    focus_ring = b.focus_ring(accent_focus, surface)
    disabled = b.disabled()
    on_disabled = b.disabled('text', disabled)

    normal_img = recolor_image('button', surface, surface, surface, surface)
    normal_focus_img = recolor_image('button', surface, surface, focus_ring, surface)
    active_img = recolor_image('button', surface_active, surface_active, surface, surface)
    selected_img = recolor_image('button', accent, accent, accent, accent)
    selected_focus_img = recolor_image('button', accent_focus, accent_focus, focus_ring, accent)

    disabled_img = recolor_image('button', disabled, disabled, surface, surface)

    b.create_style_element_image(
        ElementImage(
            f'{ttk_style}.border', normal_img, sticky="nsew", border=b.scale(8), padding=b.scale(8)).state_specs(
            [
                ('disabled', disabled_img),
                ('pressed', selected_focus_img),
                ('focus selected', selected_focus_img),
                ('selected', selected_img),
                ('focus !selected', normal_focus_img),
                ('active !focus', active_img),
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
        foreground=on_surface,
        stipple="gray12",
        relief='flat',
        padding=button_padding,
        anchor="center",
        font="body"
    )

    state_spec = dict(
        background=[('selected', accent)],
        foreground=[('disabled', on_disabled), ('selected', on_accent), ('active', on_accent), ('pressed', on_accent), ('', on_surface)],
    )

    icon_only = options.get('icon_only', False)
    default_size = b.scale(24) if icon_only else b.scale(20)
    state_spec = _apply_icon_mapping(b, options, state_spec, default_size)

    b.map_style(ttk_style, **state_spec)


@BootstyleBuilderTTk.register_builder('calendar-outside', 'Toolbutton')
def build_calendar_outside_style(b: BootstyleBuilderTTk, ttk_style: str, color: str = None, **options):
    """
    Configure style for outside/disabled calendar days.

    Uses surface background and muted text to blend in with the calendar.
    """
    surface_token = options.get('surface_color', 'background')
    surface = b.color(surface_token)
    on_disabled = b.disabled('text', surface)

    button_padding = _toolbutton_padding(b, options)

    b.configure_style(
        ttk_style,
        background=surface,
        foreground=on_disabled,
        relief='flat',
        padding=button_padding,
        anchor="center",
        font="body"
    )

    # All states use surface background with muted text
    b.map_style(ttk_style, background=[('', surface)], foreground=[('', on_disabled)])



@BootstyleBuilderTTk.register_builder('calendar-date', 'Toolbutton')
def build_calendar_date_toolbutton_style(b: BootstyleBuilderTTk, ttk_style: str, color: str = None, **options):
    """
    Configure the button style.

    Style options include:
        * icon_only
    """
    accent_token = color or 'primary'
    surface_token = options.get('surface_color', 'background')

    surface = b.color(surface_token)
    on_surface = b.on_color(surface)

    accent = b.color(accent_token)
    accent_subtle = b.subtle(accent_token, surface)
    accent_selected = b.selected(accent)

    surface_active = b.active(surface)
    accent_focus = b.focus(accent)
    on_accent = b.on_color(accent)

    focus_ring = b.focus_ring(accent_focus, surface)
    disabled = b.disabled()
    on_disabled = b.disabled('text', disabled)

    normal_img = recolor_image('button', surface, surface, surface, surface)
    normal_focus_img = recolor_image('button', surface, surface, focus_ring, surface)
    active_img = recolor_image('button', surface_active, surface_active, surface, surface)
    selected_img = recolor_image('button', accent_selected, accent_selected, focus_ring, accent_subtle)
    selected_focus_img = recolor_image('button', accent_selected, accent_selected, focus_ring, accent_subtle)

    disabled_img = recolor_image('button', disabled, disabled, surface, surface)

    b.create_style_element_image(
        ElementImage(
            f'{ttk_style}.border', normal_img, sticky="nsew", border=b.scale(8), padding=b.scale(8)).state_specs(
            [
                ('disabled', disabled_img),
                ('pressed', selected_img),
                ('focus selected', selected_focus_img),
                ('selected', selected_img),
                ('focus !selected', normal_focus_img),
                ('active !focus', active_img),
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
        foreground="black",
        stipple="gray12",
        relief='flat',
        padding=button_padding,
        anchor="center",
        font="body"
    )

    state_spec = dict(
        background=[('selected', accent_subtle)],
        foreground=[('disabled', on_disabled), ('pressed', on_accent), ('selected', on_accent), ('', on_surface)],
    )

    icon_only = options.get('icon_only', False)
    default_size = b.scale(24) if icon_only else b.scale(20)
    state_spec = _apply_icon_mapping(b, options, state_spec, default_size)

    b.map_style(ttk_style, **state_spec)
