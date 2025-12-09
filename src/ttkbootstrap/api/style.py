"""Public style-related API surface."""

from __future__ import annotations

from ttkbootstrap.core.appconfig import AppConfig
from ttkbootstrap_icons_bs import BootstrapIcon
from ttkbootstrap.style.bootstyle import Bootstyle
from ttkbootstrap.style.style import Style
from ttkbootstrap.style.theme_provider import ThemeProvider


def get_style(master=None) -> Style:
    """Return the global Style singleton instance.

    Convenience helper function that ensures a single Style instance
    is used across the application.

    Args:
        master: Optional master for initial construction; ignored thereafter.

    Returns:
        Global Style instance.

    Example:
        >>> style = get_style()
        >>> style.theme_use("darkly")
    """
    return Style(master)


def get_style_builder():
    """Return the style builder for the currently active theme.

    Returns:
        BootstyleBuilder instance for the active theme.

    Example:
        >>> builder = get_style_builder()
        >>> primary_color = builder.color("primary")
    """
    style = get_style()
    return style.style_builder


def set_active_theme(name: str) -> None:
    """Set the active application theme.

    Args:
        name: Theme name to activate (e.g., "darkly", "cosmo", "superhero").

    Example:
        >>> set_active_theme("darkly")
    """
    style = get_style()
    style.theme_use(name)


def get_active_theme() -> str:
    """Return the name of the currently active theme.

    Returns:
        Name of the active theme.

    Example:
        >>> theme = get_active_theme()
        >>> print(theme)  # "darkly"
    """
    style = get_style()
    return style.theme_use()


def get_theme_provider() -> ThemeProvider:
    """Get the theme provider instance for the active theme.

    Returns:
        ThemeProvider instance.

    Example:
        >>> provider = get_theme_provider()
        >>> colors = provider.get_colors()
    """
    style = get_style()
    return style.theme_provider


def get_theme_color(token: str) -> str:
    """Get a hex color value from a color token based on the active theme.

    Args:
        token: Color token name (e.g., "primary", "bg", "fg").

    Returns:
        Hex color string (e.g., "#007bff").

    Raises:
        ValueError: If the color token is invalid.

    Example:
        >>> primary = get_theme_color("primary")
        >>> print(primary)  # "#007bff"
    """
    builder = get_style_builder()
    try:
        return builder.color(token)
    except Exception:
        raise ValueError(f"Invalid color token: {token}")


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
