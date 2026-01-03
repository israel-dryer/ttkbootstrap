"""Style builders for the Expander widget."""

from ttkbootstrap.style.bootstyle_builder_ttk import BootstyleBuilderTTk


@BootstyleBuilderTTk.register_builder('solid', 'Expander.TFrame')
def build_solid_expander_header_style(b: BootstyleBuilderTTk, ttk_style: str, accent: str = None, **options):
    background = b.color(accent or 'primary')
    active = b.active(background)
    pressed = b.pressed(background)
    focus_border = b.focus_border(active)
    selected = b.selected(active)

    b.configure_style(ttk_style, background=background, borderwidth=1, relief='raised')

    b.map_style(
        ttk_style,
        background=[
            ('selected', selected),
            ('pressed', pressed),
            ('hover', active),
            ('', background)
        ],
        darkcolor=[
            ('selected', selected),
            ('pressed', pressed),
            ('hover', active),
            ('', background)
        ],
        lightcolor=[
            ('selected', selected),
            ('pressed', pressed),
            ('hover', active),
            ('', background)
        ],
        bordercolor=[
            ('background focus', focus_border),
            ('selected', selected),
            ('pressed', pressed),
            ('hover', active),
            ('', background)
        ]
    )


@BootstyleBuilderTTk.register_builder('solid', 'Expander.TLabel')
def build_solid_expander_header_label_style(b: BootstyleBuilderTTk, ttk_style: str, accent: str = None, **options):
    """
    Expander header label style with state-aware foreground.
    """
    background = b.color(accent or 'primary')
    active = b.active(background)
    pressed = b.pressed(background)
    selected = b.selected(active)

    on_background = b.on_color(background)
    on_active = b.on_color(active)
    on_pressed = b.on_color(pressed)
    disabled = b.disabled('text', background)

    b.configure_style(
        ttk_style,
        background=background,
        foreground=on_background,
        relief='flat',
        font='body'
    )

    foreground_state_map = [
        ('disabled', disabled),
        ('pressed', on_pressed),
        ('hover', on_active),
        ('', on_background)
    ]

    background_state_map = [
        ('selected', selected),
        ('pressed', pressed),
        ('hover', active),
        ('', background)
    ]

    # map icon if available
    icon = options.get('icon')

    image_state_map = []

    if icon is not None:
        icon = b.normalize_icon_spec(icon)
        image_state_map = b.map_stateful_icons(icon, foreground_state_map)

    b.map_style(ttk_style, foreground=foreground_state_map, background=background_state_map, image=image_state_map)


@BootstyleBuilderTTk.register_builder('default', 'Expander.TFrame')
def build_ghost_expander_header_style(b: BootstyleBuilderTTk, ttk_style: str, accent: str = None, **options):
    accent_token = accent or 'foreground'
    surface_token = options.get('surface_color', 'background')

    surface = b.color(surface_token)
    accent_color = b.color(accent_token)

    hovered = pressed = b.subtle(accent_token, surface)
    selected = b.selected(hovered)

    focused_border = b.focus_border(accent_color) if accent_token != 'foreground' else b.focus_border(b.color('primary'))

    b.configure_style(ttk_style, background=surface, borderwidth=1, relief='raised')
    b.map_style(
        ttk_style,
        background=[
            ('selected', selected),
            ('pressed', pressed),
            ('hover', hovered),
            ('', surface)
        ],
        darkcolor=[
            ('selected', selected),
            ('pressed', pressed),
            ('hover', hovered),
            ('', surface)
        ],
        lightcolor=[
            ('selected', selected),
            ('pressed', pressed),
            ('hover', hovered),
            ('', surface)
        ],
        bordercolor=[
            ('background focus', focused_border),
            ('selected', selected),
            ('pressed', pressed),
            ('hover', hovered),
            ('', surface)
        ]
    )


@BootstyleBuilderTTk.register_builder('default', 'Expander.TLabel')
def build_ghost_expander_header_label_style(b: BootstyleBuilderTTk, ttk_style: str, accent: str = None, **options):
    """
    Expander header label style with state-aware foreground.
    """
    accent_token = accent or 'foreground'
    surface_token = options.get('surface_color', 'background')

    surface = b.color(surface_token)
    accent_color = b.color(accent_token)

    hovered = pressed = b.subtle(accent_token, surface)
    selected = b.selected(hovered)

    on_surface = accent_color
    on_disabled = b.disabled('text', accent_color)

    b.configure_style(
        ttk_style,
        background=surface,
        foreground=on_surface,
        relief='flat',
        font='body'
    )

    foreground_state_map = [
        ('disabled', on_disabled),
        ('', on_surface)
    ]

    background_state_map = [
        ('selected', selected),
        ('disabled', surface),
        ('pressed', pressed),
        ('hover', hovered),
        ('', surface)
    ]

    # map icon if available
    icon = options.get('icon')

    image_state_map = []

    if icon is not None:
        icon = b.normalize_icon_spec(icon)
        image_state_map = b.map_stateful_icons(icon, foreground_state_map)

    b.map_style(ttk_style, foreground=foreground_state_map, background=background_state_map, image=image_state_map)
