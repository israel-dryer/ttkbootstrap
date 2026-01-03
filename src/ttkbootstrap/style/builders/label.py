from __future__ import annotations

from ttkbootstrap.style.bootstyle_builder_ttk import BootstyleBuilderTTk


@BootstyleBuilderTTk.register_builder('default', 'TLabel')
def build_label(b: BootstyleBuilderTTk, ttk_style: str, accent: str = None, **options):
    surface_token = options.get('surface', 'content')
    background = b.color(surface_token)
    if accent is None:
        # best foreground on inherited background
        foreground = b.on_color(background)
    else:
        # override
        foreground = b.color(accent)

    b.configure_style(ttk_style, background=background, foreground=foreground, font="body")

    state_spec = dict(foreground=[('', foreground)])

    # map icon if available
    icon = options.get('icon')

    if icon is not None:
        icon = b.normalize_icon_spec(icon)
        state_spec['image'] = b.map_stateful_icons(icon, state_spec['foreground'])

    b.map_style(ttk_style, **state_spec)
