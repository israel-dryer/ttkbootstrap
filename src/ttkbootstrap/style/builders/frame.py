from __future__ import annotations

from ttkbootstrap.style.bootstyle_builder import BootstyleBuilder


@BootstyleBuilder.register_builder('default', 'TFrame')
def build_frame(builder: BootstyleBuilder, ttk_style: str, color: str = None, **options):
    background = builder.color(color or "background")
    builder.configure_style(ttk_style, background=background)
