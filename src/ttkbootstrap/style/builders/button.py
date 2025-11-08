"""Button widget style builders.

This module contains style builders for ttk.Button widgets and variants.
"""

from __future__ import annotations

from ttkbootstrap.style.bootstyle_builder import BootstyleBuilder


@BootstyleBuilder.register_builder('solid', 'TButton')
@BootstyleBuilder.register_builder('default', 'TButton')
def build_button_solid(builder: BootstyleBuilder, ttk_style: str,
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

    # Get theme colors
    background = builder.color(colorname)
    foreground = builder.on_color(background)

    # Calculate state colors
    bordercolor = background
    disabled_bg = builder.disabled('background')
    disabled_fg = builder.disabled('text')
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
    builder.map_style(
        ttk_style,
        foreground=[('disabled', disabled_fg)],
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


@BootstyleBuilder.register_builder('outline', 'TButton')
def build_button_outline(builder: BootstyleBuilder, ttk_style: str,
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
    surface_token = options.get('surface_color')
    background = builder.color(surface_token)


    # Get theme colors
    foreground = builder.color(colorname)
    foreground_pressed = background

    # Calculate state colors
    bordercolor = foreground
    disabled_fg = builder.disabled('text')
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
    builder.map_style(
        ttk_style,
        foreground=[
            ('disabled', disabled_fg),
            ('pressed !disabled', foreground_pressed),
            ('hover !disabled', foreground_pressed),
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


@BootstyleBuilder.register_builder('link', 'TButton')
def build_button_link(builder: BootstyleBuilder, ttk_style: str,
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
    disabled_fg = builder.disabled('text')
    bg_color = builder.color('background')

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
    builder.map_style(
        ttk_style,
        shiftrelief=[('pressed !disabled', -1)],
        foreground=[
            ('disabled', disabled_fg),
            ('pressed !disabled', pressed),
            ('hover !disabled', hover),
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