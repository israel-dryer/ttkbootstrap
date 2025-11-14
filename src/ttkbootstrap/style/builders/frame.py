from __future__ import annotations

from ttkbootstrap.style.bootstyle_builder_ttk import BootstyleBuilderTTk


@BootstyleBuilderTTk.register_builder('default', 'TFrame')
def build_frame(builder: BootstyleBuilderTTk, ttk_style: str, color: str = None, **options):
    # Prefer explicit surface_color option; else use color token or background
    surface_token = options.get('surface_color') or color or "background"
    background = builder.color(surface_token)
    builder.configure_style(ttk_style, background=background)
