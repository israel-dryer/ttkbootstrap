"""Public style-related API surface."""

from __future__ import annotations

from ttkbootstrap.core.appconfig import AppConfig
from ttkbootstrap_icons_bs import BootstrapIcon
from ttkbootstrap.style.bootstyle import Bootstyle
from ttkbootstrap.style.style import (
    Style, get_style, get_style_builder, get_active_theme, get_theme_provider, set_active_theme, get_theme_color
)

__all__ = [
    "AppConfig",
    "BootstrapIcon",
    "Bootstyle",
    "Style",
    "get_style",
    "get_style_builder",
    "get_active_theme",
    "set_active_theme",
    "get_theme_provider",
    "get_theme_color"
]
