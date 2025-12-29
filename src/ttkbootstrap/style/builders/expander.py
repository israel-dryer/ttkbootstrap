"""Style builders for the Expander widget."""

from ttkbootstrap.style.bootstyle_builder_ttk import BootstyleBuilderTTk
from ttkbootstrap.style.element import ElementImage, Element
from ttkbootstrap.style.utility import recolor_image


@BootstyleBuilderTTk.register_builder('default', 'Expander.TFrame')
def build_expander_header_style(b: BootstyleBuilderTTk, ttk_style: str, color: str = None, **options):
    surface_token = options.get('surface_color', 'background')

    surface = b.color(surface_token)
    accent = b.color(color or 'primary')
    normal = surface
    border = b.border(surface)
    active = b.active(surface)
    pressed = b.pressed(accent)
    disabled = b.disabled('text')
    focused_border = b.focus_border(accent)
    focused_ring = b.focus_ring(accent, surface)

    # input element images
    normal_img = recolor_image('input', normal, border, surface)
    active_img = recolor_image('input', active, border, surface)
    pressed_img = recolor_image('input', pressed, border, surface)
    focused_img = recolor_image('input', normal, focused_border, focused_ring)
    disabled_img = recolor_image('input', normal, disabled, surface, surface)

    # input element
    b.create_style_element_image(
        ElementImage(f'{ttk_style}.border', normal_img, sticky="nsew", border=b.scale(8)).state_specs(
            [
                ('disabled', disabled_img),
                ('pressed', pressed_img),
                ('hover', active_img),
                ('background focus', focused_img),
            ]
        )
    )
    b.create_style_layout(
        ttk_style, Element(f'{ttk_style}.border', sticky="nsew").children(
            [
                Element(f'{ttk_style}.padding', sticky="")
            ]))
    b.configure_style(ttk_style, background=surface, padding=8)


@BootstyleBuilderTTk.register_builder('default', 'Expander.TLabel')
def build_expander_header_label_style(b: BootstyleBuilderTTk, ttk_style: str, color: str = None, **options):
    """
    Expander header label style with state-aware foreground.
    """
    accent_token = color or 'primary'
    surface_token = options.get('surface_color', 'background')

    surface = b.color(surface_token)
    on_surface = b.on_color(surface)
    accent = b.color(accent_token)

    disabled = b.disabled()
    on_disabled = b.disabled('text', disabled)

    b.configure_style(
        ttk_style,
        background=surface,
        foreground=on_surface,
        relief='flat',
        font='body'
    )

    foreground_state_map = [
        ('disabled', on_disabled),
        ('pressed', b.on_color(accent)),
        ('hover', b.on_color(surface)),
        ('', on_surface)
    ]

    background_state_map = [
        ('disabled', surface),
        ('pressed', b.pressed(accent)),
        ('hover', b.active(surface)),
        ('', surface)
    ]

    # map icon if available
    icon = options.get('icon')

    image_state_map = []

    if icon is not None:
        icon = b.normalize_icon_spec(icon)
        image_state_map = b.map_stateful_icons(icon, foreground_state_map)

    b.map_style(ttk_style, foreground=foreground_state_map, background=background_state_map, image=image_state_map)