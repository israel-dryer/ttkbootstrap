"""Sizegrip widget style builders.

This module contains style builders for ttk.Sizegrip and variants.
"""

from __future__ import annotations

from ttkbootstrap.style.bootstyle_builder_ttk import BootstyleBuilderTTk


@BootstyleBuilderTTk.register_builder('default', 'TSizegrip')
def build_sizegrip_style(b: BootstyleBuilderTTk, ttk_style: str, color: str = None, **options):
    surface_token = options.get('surface_color', 'background')
    surface = b.color(surface_token)
    b.configure_style(ttk_style, background=surface)
