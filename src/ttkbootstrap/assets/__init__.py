"""Package assets utilities.

This module provides utilities for accessing package assets like icons,
themes, and locale files.
"""

from pathlib import Path

# Package assets directory
ASSETS_DIR = Path(__file__).parent

# Common asset paths
ICON_PATH = ASSETS_DIR / "ttkbootstrap.png"
THEMES_DIR = ASSETS_DIR / "themes"
LOCALES_DIR = ASSETS_DIR / "locales"
WIDGETS_DIR = ASSETS_DIR / "widgets"

__all__ = [
    "ASSETS_DIR",
    "ICON_PATH",
    "THEMES_DIR",
    "LOCALES_DIR",
    "WIDGETS_DIR",
]