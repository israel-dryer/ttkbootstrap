from __future__ import annotations

from ttkbootstrap.style.bootstyle_builder_ttk import BootstyleBuilderBuilderTTk


@BootstyleBuilderBuilderTTk.register_builder('default', 'TLabel')
def build_label(builder: BootstyleBuilderBuilderTTk, ttk_style: str, color: str = None, **options):
    foreground = builder.color(color or "foreground")
    surface_token = options.get('surface_color', 'background')
    background = builder.color(surface_token)

    builder.configure_style(ttk_style, background=background, foreground=foreground)
