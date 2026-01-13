from __future__ import annotations

from ttkbootstrap.style.bootstyle_builder_ttk import BootstyleBuilderTTk
from ttkbootstrap.style.builders.utils import toolbutton_layout, button_padding, button_font, apply_icon_mapping, icon_size
from ttkbootstrap.style.element import ElementImage
from ttkbootstrap.style.utility import recolor_element_image

# Calendar uses 'compact' density for all styles
CALENDAR_DENSITY = 'compact'


@BootstyleBuilderTTk.register_builder('calendar-day', 'Toolbutton')
def build_calendar_day_toolbutton_style(b: BootstyleBuilderTTk, ttk_style: str, accent: str = None, **options):
    """
    Configure the calendar day button style.

    Style options include:
        * icon_only
    """
    accent_token = accent or 'primary'
    surface_token = options.get('surface', 'content')
    icon_only = options.get('icon_only', False)

    surface = b.color(surface_token)
    on_surface = b.on_color(surface)
    accent_color = b.color(accent_token)

    active = b.active(accent_color)
    accent_focus = b.focus(accent_color)
    on_accent = b.on_color(accent_color)

    selected = b.selected(accent_color)

    focus_ring = b.focus_ring(accent_focus, surface)
    disabled = b.disabled()
    on_disabled = b.disabled('text', disabled)

    normal_img = recolor_element_image('button_compact', surface, surface, surface, surface)
    normal_focus_img = recolor_element_image('button_compact', surface, surface, focus_ring, surface)
    active_img = recolor_element_image('button_compact', active, active, surface, surface)
    selected_img = recolor_element_image('button_compact', selected, selected, surface, surface)
    selected_focus_img = recolor_element_image('button_compact', selected, selected, focus_ring, surface)

    disabled_img = recolor_element_image('button_compact', disabled, disabled, surface, surface)

    b.create_style_element_image(
        ElementImage(
            f'{ttk_style}.border', normal_img.image, sticky="nsew", border=normal_img.meta.border).state_specs(
            [
                ('disabled', disabled_img.image),
                ('pressed', selected_focus_img.image),
                ('focus selected', selected_focus_img.image),
                ('selected', selected_img.image),
                ('focus !selected', normal_focus_img.image),
                ('active !focus', active_img.image),
                ('', normal_img.image)
            ]))

    b.create_style_layout(
        ttk_style,
        toolbutton_layout(ttk_style),
    )

    b.configure_style(
        ttk_style,
        background=surface,
        foreground=on_surface,
        stipple="gray12",
        relief='flat',
        padding=button_padding(b, icon_only, CALENDAR_DENSITY),
        anchor="center",
        font=button_font(CALENDAR_DENSITY)
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

    state_spec = apply_icon_mapping(b, options, state_spec, icon_size(icon_only, CALENDAR_DENSITY))

    b.map_style(ttk_style, **state_spec)


@BootstyleBuilderTTk.register_builder('calendar-range', 'Toolbutton')
def build_calendar_range_toolbutton_style(b: BootstyleBuilderTTk, ttk_style: str, accent: str = None, **options):
    """
    Configure the calendar range button style.

    Style options include:
        * icon_only
    """
    accent_token = accent or 'primary'
    surface_token = options.get('surface', 'content')
    icon_only = options.get('icon_only', False)

    surface = b.color(surface_token)
    on_surface = b.on_color(surface)

    accent_color = b.subtle(accent_token, surface)

    surface_active = b.active(surface)
    accent_focus = b.focus(accent_color)
    on_accent = b.on_color(accent_color)

    focus_ring = b.focus_ring(accent_focus, surface)
    disabled = b.disabled()
    on_disabled = b.disabled('text', disabled)

    normal_img = recolor_element_image('button_compact', surface, surface, surface, surface)
    normal_focus_img = recolor_element_image('button_compact', surface, surface, focus_ring, surface)
    active_img = recolor_element_image('button_compact', surface_active, surface_active, surface, surface)
    selected_img = recolor_element_image('button_compact', accent_color, accent_color, accent_color, accent_color)
    selected_focus_img = recolor_element_image('button_compact', accent_focus, accent_focus, focus_ring, accent_color)

    disabled_img = recolor_element_image('button_compact', disabled, disabled, surface, surface)

    b.create_style_element_image(
        ElementImage(
            f'{ttk_style}.border', normal_img.image, sticky="nsew", border=normal_img.meta.border).state_specs(
            [
                ('disabled', disabled_img.image),
                ('pressed', selected_focus_img.image),
                ('focus selected', selected_focus_img.image),
                ('selected', selected_img.image),
                ('focus !selected', normal_focus_img.image),
                ('active !focus', active_img.image),
                ('', normal_img.image)
            ]))

    b.create_style_layout(
        ttk_style,
        toolbutton_layout(ttk_style),
    )

    b.configure_style(
        ttk_style,
        background=surface,
        foreground=on_surface,
        stipple="gray12",
        relief='flat',
        padding=button_padding(b, icon_only, CALENDAR_DENSITY),
        anchor="center",
        font=button_font(CALENDAR_DENSITY)
    )

    state_spec = dict(
        background=[('selected', accent_color)],
        foreground=[
            ('disabled', on_disabled),
            ('selected', on_accent),
            ('active', on_accent),
            ('pressed', on_accent),
            ('', on_surface)
        ],
    )

    state_spec = apply_icon_mapping(b, options, state_spec, icon_size(icon_only, CALENDAR_DENSITY))

    b.map_style(ttk_style, **state_spec)


@BootstyleBuilderTTk.register_builder('calendar-outside', 'Toolbutton')
def build_calendar_outside_style(b: BootstyleBuilderTTk, ttk_style: str, accent: str = None, **options):
    """
    Configure style for outside/disabled calendar days.

    Uses surface background and muted text to blend in with the calendar.
    """
    surface_token = options.get('surface', 'content')
    icon_only = options.get('icon_only', False)
    surface = b.color(surface_token)
    on_disabled = b.disabled('text', surface)

    b.configure_style(
        ttk_style,
        background=surface,
        foreground=on_disabled,
        relief='flat',
        padding=button_padding(b, icon_only, CALENDAR_DENSITY),
        anchor="center",
        font=button_font(CALENDAR_DENSITY)
    )

    # All states use surface background with muted text
    b.map_style(ttk_style, background=[('', surface)], foreground=[('', on_disabled)])



@BootstyleBuilderTTk.register_builder('calendar-date', 'Toolbutton')
def build_calendar_date_toolbutton_style(b: BootstyleBuilderTTk, ttk_style: str, accent: str = None, **options):
    """
    Configure the calendar date button style.

    Style options include:
        * icon_only
    """
    accent_token = accent or 'primary'
    surface_token = options.get('surface', 'content')
    icon_only = options.get('icon_only', False)

    surface = b.color(surface_token)
    on_surface = b.on_color(surface)

    accent_color = b.color(accent_token)
    accent_subtle = b.subtle(accent_token, surface)
    accent_selected = b.selected(accent_color)

    surface_active = b.active(surface)
    accent_focus = b.focus(accent_color)
    on_accent = b.on_color(accent_color)

    focus_ring = b.focus_ring(accent_focus, surface)
    disabled = b.disabled()
    on_disabled = b.disabled('text', disabled)

    normal_img = recolor_element_image('button_compact', surface, surface, surface, surface)
    normal_focus_img = recolor_element_image('button_compact', surface, surface, focus_ring, surface)
    active_img = recolor_element_image('button_compact', surface_active, surface_active, surface, surface)
    selected_img = recolor_element_image('button_compact', accent_selected, accent_selected, focus_ring, accent_subtle)
    selected_focus_img = recolor_element_image('button_compact', accent_selected, accent_selected, focus_ring, accent_subtle)

    disabled_img = recolor_element_image('button_compact', disabled, disabled, surface, surface)

    b.create_style_element_image(
        ElementImage(
            f'{ttk_style}.border', normal_img.image, sticky="nsew", border=normal_img.meta.border).state_specs(
            [
                ('disabled', disabled_img.image),
                ('pressed', selected_img.image),
                ('focus selected', selected_focus_img.image),
                ('selected', selected_img.image),
                ('focus !selected', normal_focus_img.image),
                ('active !focus', active_img.image),
                ('', normal_img.image)
            ]))

    b.create_style_layout(
        ttk_style,
        toolbutton_layout(ttk_style),
    )

    b.configure_style(
        ttk_style,
        background=surface,
        foreground=on_surface,
        stipple="gray12",
        relief='flat',
        padding=button_padding(b, icon_only, CALENDAR_DENSITY),
        anchor="center",
        font=button_font(CALENDAR_DENSITY)
    )

    state_spec = dict(
        background=[('selected', accent_subtle)],
        foreground=[
            ('disabled', on_disabled),
            ('pressed', on_accent),
            ('selected', on_accent),
            ('', on_surface)
        ],
    )

    state_spec = apply_icon_mapping(b, options, state_spec, icon_size(icon_only, CALENDAR_DENSITY))

    b.map_style(ttk_style, **state_spec)
