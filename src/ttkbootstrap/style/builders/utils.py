"""Utility functions for style builders.

This module provides common utilities used across builder functions,
including accent extraction, variant parsing, and style name manipulation.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional

from ttkbootstrap.style.element import Element

if TYPE_CHECKING:
    from ttkbootstrap.style.bootstyle_builder_ttk import BootstyleBuilderTTk

# Standard ttkbootstrap color tokens
COLORS = {
    'primary', 'secondary', 'success', 'info',
    'warning', 'danger', 'light', 'dark', 'blue'
}


def extract_accent_from_style(ttk_style: str, default: str = 'primary') -> str:
    """Extract accent token from TTK style name.

    Args:
        ttk_style: Full TTK style name (e.g., "custom_abc.success.Outline.TButton")
        default: Default accent if none found

    Returns:
        Accent token name (e.g., "success")

    Examples:
        >>> extract_accent_from_style("success.Outline.TButton")
        'success'
        >>> extract_accent_from_style("custom_abc.danger.TLabel")
        'danger'
        >>> extract_accent_from_style("TButton")
        'primary'
    """
    # Remove custom prefix if present
    parts = ttk_style.split('.')
    if parts and parts[0].startswith('custom_'):
        parts = parts[1:]

    # Find accent in parts
    for part in parts:
        if part.lower() in COLORS:
            return part.lower()

    return default


def extract_variant_from_style(ttk_style: str) -> Optional[str]:
    """Extract variant name from TTK style name.

    Args:
        ttk_style: Full TTK style name (e.g., "success.Outline.TButton")

    Returns:
        Variant name (lowercase) or None

    Examples:
        >>> extract_variant_from_style("success.Outline.TButton")
        'outline'
        >>> extract_variant_from_style("primary.TLabel") is None
        True
    """
    parts = ttk_style.split('.')

    # Remove custom prefix if present
    if parts and parts[0].startswith('custom_'):
        parts = parts[1:]

    # Find variant (not accent, not widget class)
    for part in parts:
        part_lower = part.lower()
        if part_lower not in COLORS and not part.startswith('T'):
            return part_lower

    return None


def extract_widget_class_from_style(ttk_style: str) -> Optional[str]:
    """Extract widget class from TTK style name.

    Args:
        ttk_style: Full TTK style name (e.g., "success.Outline.TButton")

    Returns:
        Widget class name or None

    Examples:
        >>> extract_widget_class_from_style("success.Outline.TButton")
        'TButton'
        >>> extract_widget_class_from_style("primary.TLabel")
        'TLabel'
    """
    parts = ttk_style.split('.')

    # Find widget class (starts with 'T')
    for part in parts:
        if part.startswith('T'):
            return part

    return None


def parse_style_components(ttk_style: str) -> dict:
    """Parse TTK style name into all components.

    Args:
        ttk_style: Full TTK style name

    Returns:
        Dictionary with parsed components:
        {
            'custom_prefix': 'custom_abc123' or None,
            'accent': 'success' or default,
            'variant': 'outline' or None,
            'widget_class': 'TButton'
        }

    Examples:
        >>> parse_style_components("custom_abc.success.Outline.TButton")
        {'custom_prefix': 'custom_abc', 'accent': 'success', 'variant': 'outline', 'widget_class': 'TButton'}
        >>> parse_style_components("danger.TLabel")
        {'custom_prefix': None, 'accent': 'danger', 'variant': None, 'widget_class': 'TLabel'}
    """
    parts = ttk_style.split('.')

    # Check for custom prefix
    custom_prefix = None
    if parts and parts[0].startswith('custom_'):
        custom_prefix = parts[0]

    return {
        'custom_prefix': custom_prefix,
        'accent': extract_accent_from_style(ttk_style),
        'variant': extract_variant_from_style(ttk_style),
        'widget_class': extract_widget_class_from_style(ttk_style),
    }


# Button utilities
# These utilities are used by button style builders and can be reused by other widgets.

def button_layout(ttk_style: str) -> Element:
    """Create the standard button element layout.

    Args:
        ttk_style: The TTK style name prefix for the button.

    Returns:
        Element tree representing the button layout.
    """
    return Element(f"{ttk_style}.Button.border", sticky="nsew").children(
        [
            Element("Button.padding", sticky="nsew").children(
                [
                    Element("Button.label", sticky="nsew")
                ])
        ])


def icon_size(icon_only: bool, size: str) -> int:
    """Determine icon size based on button size and icon_only flag.

    Args:
        icon_only: Whether the button displays only an icon (no text).
        size: The button size ('xs', 'md', etc.).

    Returns:
        The icon size in pixels.
    """
    if size == 'xs':
        if icon_only:
            return 16
        return 17
    elif icon_only:
        return 20
    return 18


def button_font(size: str) -> str:
    """Get the font token for a button based on its size.

    Args:
        size: The button size ('xs', 'md', etc.).

    Returns:
        The font token name.
    """
    return 'caption' if size == 'xs' else 'body'


def button_padding(b: BootstyleBuilderTTk, icon_only: bool, size: Any) -> int | tuple[int, ...]:
    """Calculate button padding based on options.

    Args:
        b: The bootstyle builder instance.
        icon_only: Whether the button displays only an icon.
        size: The button size.

    Returns:
        Padding value (0 for icon_only, scaled tuple otherwise).
    """
    if icon_only:
        return 0
    if size == 'xs':
        return b.scale((6, 0))
    return b.scale((8, 0))


def apply_icon_mapping(
        b: BootstyleBuilderTTk,
        options: dict,
        state_spec: dict,
        default_size: int | None = None
) -> dict:
    """Apply icon mapping to a state specification dictionary.

    Args:
        b: The bootstyle builder instance.
        options: Style options dictionary containing 'icon' and 'icon_only' keys.
        state_spec: The state specification dictionary to update.
        default_size: Default icon size, or None to use normalize_icon_spec defaults.

    Returns:
        Updated state_spec with icon mappings applied.
    """
    icon = options.get('icon')
    if icon is None:
        return state_spec

    if default_size is None:
        icon = b.normalize_icon_spec(icon)
    else:
        icon = b.normalize_icon_spec(icon, default_size)

    state_spec['image'] = b.map_stateful_icons(icon, state_spec['foreground'])
    # Set compound to 'left' so text is visible alongside the icon
    icon_only = options.get('icon_only', False)
    if not icon_only:
        state_spec['compound'] = 'left'
    return state_spec
