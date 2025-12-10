"""Public style-related API surface."""

from __future__ import annotations

from ttkbootstrap_icons_bs import BootstrapIcon

from ttkbootstrap.style.bootstyle import Bootstyle
from ttkbootstrap.style.style import (Style, get_style, get_style_builder, get_theme, get_theme_color,
                                      get_theme_provider, set_theme, toggle_theme)

__all__ = [
    "BootstrapIcon",
    "Bootstyle",
    "Style",
    "get_style",
    "get_style_builder",
    "get_theme",
    "set_theme",
    "toggle_theme",
    "get_theme_provider",
    "get_theme_color"
]
