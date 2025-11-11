from __future__ import annotations

from ttkbootstrap.style.bootstyle_builder_ttk import BootstyleBuilderBuilderTTk


@BootstyleBuilderBuilderTTk.register_builder('default', 'TLabel')
def build_label(b: BootstyleBuilderBuilderTTk, ttk_style: str, color: str = None, **options):
    foreground = b.color(color or "foreground")
    surface_token = options.get('surface_color', 'background')
    background = b.color(surface_token)

    b.configure_style(ttk_style, background=background, foreground=foreground)

    state_spec = dict(foreground=[('', foreground)])

    # map icon if available
    icon = options.get('icon')

    if icon is not None:
        icon = b.normalize_icon_spec(icon)
        state_spec['image'] = b.map_stateful_icons(icon, state_spec['foreground'])

    b.map_style(ttk_style, **state_spec)
