"""Button widget style builders.

This module contains style builders for ttk.Button widgets and variants.
"""

from __future__ import annotations

from ttkbootstrap.style.bootstyle_builder_ttk import BootstyleBuilderBuilderTTk
from ttkbootstrap.style.element import Element, ElementImage
from ttkbootstrap.style.style import use_style
from ttkbootstrap.style.theme_provider import use_theme
from ttkbootstrap.style.utility import recolor_image


@BootstyleBuilderBuilderTTk.register_builder('updated', 'TButton')
def build_new_button(b: BootstyleBuilderBuilderTTk, ttk_style: str, color: str = 'primary', **options):
    accent_token = color or 'primary'
    surface_token = options.get('surface_color', 'background')

    surface = b.color(surface_token)
    normal = b.color(accent_token)
    foreground = b.on_color(normal)
    foreground_disabled = b.disabled('text')
    pressed = b.active(normal)
    hovered = focused = b.hover(normal)
    focused_border = b.focus_border(normal)
    disabled = b.disabled()
    focused_ring = b.focus_ring(normal, surface)

    normal_img = recolor_image('button', normal, normal, surface)
    pressed_img = recolor_image('button', pressed, pressed, surface)
    hovered_img = recolor_image('button', hovered, hovered, surface)
    focused_img = recolor_image('button', focused, focused_border, focused_ring)
    focused_hovered_img = recolor_image('button', hovered, focused_border, focused_ring)
    focused_pressed_img = recolor_image('button', pressed, focused_border, focused_ring)
    disabled_img = recolor_image('button', disabled, disabled, surface, surface)

    b.create_style_element_image(
        ElementImage(
            f'{ttk_style}.border', normal_img, sticky="nsew", border=8, padding=8).state_specs(
            [
                ('disabled', disabled_img),
                ('focus pressed', focused_pressed_img),
                ('focus hover', focused_hovered_img),
                ('focus', focused_img),
                ('pressed', pressed_img),
                ('hover', hovered_img),
            ]))

    b.create_style_layout(
        ttk_style, Element(f"{ttk_style}.border", sticky="nsew").children(
            [
                Element("Button.padding", sticky="nsew").children(
                    [
                        Element("Button.label", sticky="")
                    ])
            ]))

    b.configure_style(
        ttk_style,
        background=surface,
        foreground=foreground,
        stipple="gray12",
        relief='flat',
        padding=(8, 0)
    )

    state_spec = dict(
        foreground=[('disabled', foreground_disabled), ('', foreground)],
        background=[('disabled', disabled)]
    )

    # map icon if available
    icon = options.get('icon')

    if icon is not None:
        icon = b.normalize_icon_spec(icon)
        state_spec['image'] = b.map_stateful_icons(icon, state_spec['foreground'])

    b.map_style(ttk_style, **state_spec)


@BootstyleBuilderBuilderTTk.register_builder('solid', 'TButton')
@BootstyleBuilderBuilderTTk.register_builder('default', 'TButton')
def build_button_solid(
        builder: BootstyleBuilderBuilderTTk, ttk_style: str,
        color: str = None, **options):
    """Build solid button style with filled background.

    This is the default button style with a solid colored background.

    Args:
        builder: BootstyleBuilder instance with style, colors, utilities
        ttk_style: Full TTK style name (e.g., "success.TButton")
        color: Color token (e.g., 'success', '#FF5733') or None for default
        **options: Custom style options (currently unused, reserved for future)

    Supported Options:
        None currently - reserved for future use (border_width, padding, etc.)
    """
    # Use the color passed directly from parsing (default to 'primary' if None)
    colorname = color or 'primary'
    surface_token = options.get('surface_color', 'background')
    surface = builder.color(surface_token)

    # Get theme colors
    background = builder.color(colorname)
    foreground = builder.on_color(background)

    # Calculate state colors
    bordercolor = background
    disabled_bg = builder.disabled('background', surface=surface)
    disabled_fg = builder.disabled('text', surface=surface)
    pressed = builder.active(background)
    hover = builder.hover(background)

    # Configure base style
    builder.configure_style(
        ttk_style,
        foreground=foreground,
        background=background,
        bordercolor=bordercolor,
        darkcolor=background,
        lightcolor=background,
        relief='raised',
        focusthickness=1,
        focuscolor=foreground,
        padding=(10, 5),
        anchor='center',
    )

    # Map state-specific colors
    state_spec = dict(
        foreground=[('disabled', disabled_fg), ('', foreground)],
        focuscolor=[('disabled', disabled_fg)],
        background=[
            ('disabled', disabled_bg),
            ('pressed !disabled', pressed),
            ('hover !disabled', hover),
        ],
        bordercolor=[('disabled', disabled_bg)],
        darkcolor=[
            ('disabled', disabled_bg),
            ('pressed !disabled', pressed),
            ('hover !disabled', hover),
        ],
        lightcolor=[
            ('disabled', disabled_bg),
            ('pressed !disabled', pressed),
            ('hover !disabled', hover),
        ],
    )

    icon = options.get('icon')

    if icon is not None:
        icon = builder.normalize_icon_spec(icon)
        state_spec['image'] = builder.map_stateful_icons(icon, state_spec['foreground'])

    builder.map_style(ttk_style, **state_spec)


@BootstyleBuilderBuilderTTk.register_builder('outline', 'TButton')
def build_button_outline(
        builder: BootstyleBuilderBuilderTTk, ttk_style: str,
        color: str = None, **options):
    """Build outline button style with border.

    Outline buttons have a transparent background with a colored border.
    On hover/press, the background fills with the color.

    Args:
        builder: BootstyleBuilder instance with style, colors, utilities
        ttk_style: Full TTK style name (e.g., "danger.Outline.TButton")
        color: Color token (e.g., 'danger', '#FF5733') or None for default
        **options: Custom style options (currently unused)

    Supported Options:
        None currently - reserved for future use
    """
    # Use the color passed directly from parsing (default to 'primary' if None)
    colorname = color or 'primary'
    surface_token = options.get('surface_color', 'background')
    background = builder.color(surface_token)

    # Get theme colors
    foreground = builder.color(colorname)
    foreground_pressed = background

    # Calculate state colors
    bordercolor = foreground
    disabled_fg = builder.disabled('text', surface=background)
    pressed = foreground
    hover = foreground

    # Configure base style
    builder.configure_style(
        ttk_style,
        foreground=foreground,
        background=background,
        bordercolor=bordercolor,
        darkcolor=background,
        lightcolor=background,
        relief='raised',
        focusthickness=1,
        focuscolor=foreground,
        padding=(10, 5),
        anchor='center',
    )

    # Map state-specific colors
    state_spec = dict(
        foreground=[
            ('disabled', disabled_fg),
            ('pressed !disabled', foreground_pressed),
            ('hover !disabled', foreground_pressed),
            ('', foreground)
        ],
        background=[
            ('pressed !disabled', pressed),
            ('hover !disabled', hover),
        ],
        bordercolor=[
            ('disabled', disabled_fg),
            ('pressed !disabled', pressed),
            ('hover !disabled', hover),
        ],
        focuscolor=[
            ('pressed !disabled', foreground_pressed),
            ('hover !disabled', foreground_pressed),
        ],
        darkcolor=[
            ('pressed !disabled', pressed),
            ('hover !disabled', hover),
        ],
        lightcolor=[
            ('pressed !disabled', pressed),
            ('hover !disabled', hover),
        ],
    )
    icon = options.get('icon')

    if icon is not None:
        icon = builder.normalize_icon_spec(icon)
        state_spec['image'] = builder.map_stateful_icons(icon, state_spec['foreground'])

    builder.map_style(ttk_style, **state_spec)


@BootstyleBuilderBuilderTTk.register_builder('link', 'TButton')
def build_button_link(
        builder: BootstyleBuilderBuilderTTk, ttk_style: str,
        color: str = None, **options):
    """Build link-style button (text only, no visible button).

    Link buttons appear as clickable text with no background or border.
    They change color on hover to indicate interactivity.

    Args:
        builder: BootstyleBuilder instance with style, colors, utilities
        ttk_style: Full TTK style name (e.g., "info.Link.TButton")
        color: Color token (e.g., 'info', '#FF5733') or None for default
        **options: Custom style options (currently unused)

    Supported Options:
        None currently - reserved for future use
    """
    # Use the color passed directly from parsing (default to 'primary' if None)
    colorname = color or 'primary'

    # Get theme colors
    if colorname in ('light', 'primary'):
        foreground = builder.color('foreground')
    else:
        foreground = builder.color(colorname)

    # Link buttons typically use info color for hover
    pressed = builder.color('info')
    hover = builder.color('info')
    surface_token = options.get('surface_color', 'background')
    bg_color = builder.color(surface_token)
    disabled_fg = builder.disabled('text', surface=bg_color)

    # Configure base style
    builder.configure_style(
        ttk_style,
        foreground=foreground,
        background=bg_color,
        bordercolor=bg_color,
        darkcolor=bg_color,
        lightcolor=bg_color,
        relief='raised',
        focusthickness=1,
        focuscolor=foreground,
        anchor='center',
        padding=(10, 5),
    )

    # Map state-specific colors
    state_spec = dict(
        shiftrelief=[('pressed !disabled', -1)],
        foreground=[
            ('disabled', disabled_fg),
            ('pressed !disabled', pressed),
            ('hover !disabled', hover),
            ('', foreground)
        ],
        focuscolor=[
            ('pressed !disabled', pressed),
            ('hover !disabled', pressed),
        ],
        background=[
            ('disabled', bg_color),
            ('pressed !disabled', bg_color),
            ('hover !disabled', bg_color),
        ],
        bordercolor=[
            ('disabled', bg_color),
            ('pressed !disabled', bg_color),
            ('hover !disabled', bg_color),
        ],
        darkcolor=[
            ('disabled', bg_color),
            ('pressed !disabled', bg_color),
            ('hover !disabled', bg_color),
        ],
        lightcolor=[
            ('disabled', bg_color),
            ('pressed !disabled', bg_color),
            ('hover !disabled', bg_color),
        ],
    )

    icon = options.get('icon')

    if icon is not None:
        icon = builder.normalize_icon_spec(icon)
        state_spec['image'] = builder.map_stateful_icons(icon, state_spec['foreground'])

    builder.map_style(ttk_style, **state_spec)
