"""Panedwindow widget style builders.

This module contains style builders for ttk.Panedwindow widget and variants.
"""

from __future__ import annotations

from ttkbootstrap.style.bootstyle_builder_ttk import BootstyleBuilderTTk


@BootstyleBuilderTTk.register_builder('default', 'TPanedwindow')
def build_paned_window_style(b: BootstyleBuilderTTk, ttk_style: str, accent: str = None, **options):
    accent_token = accent or 'border'
    surface_token = options.get('surface_color', 'background')
    sash_thickness = options.get('sash_thickness', b.scale(6))

    surface = b.color(surface_token)
    if accent_token == 'border':
        accent_color = b.border(surface)
    else:
        accent_color = b.color(accent_token)

    # Sash thickness is a global adjustment that affects all paned windows
    b.configure_style("Sash", sashthickness=sash_thickness, gripcount=0)
    b.configure_style(ttk_style, background=accent_color)
