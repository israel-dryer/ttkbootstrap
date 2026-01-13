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

# Valid button densities: 'default' (normal) and 'compact' (smaller/tighter)
BUTTON_DENSITIES = {'default', 'compact'}


def normalize_button_density(density: str) -> str:
    """Normalize button density to valid values ('default' or 'compact').

    Args:
        density: The requested button density.

    Returns:
        'compact' for compact buttons, 'default' for all other densities.
    """
    return 'compact' if density == 'compact' else 'default'


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


def toolbutton_layout(ttk_style: str) -> Element:
    """Create the standard toolbutton element layout.

    Args:
        ttk_style: The TTK style name prefix for the toolbutton.

    Returns:
        Element tree representing the toolbutton layout.
    """
    return Element(f"{ttk_style}.border", sticky="nsew").children(
        [
            Element("Toolbutton.padding", sticky="nsew").children(
                [
                    Element("Toolbutton.label", sticky="nsew")
                ])
        ])


def icon_size(icon_only: bool, density: str) -> int:
    """Determine icon size based on button density and icon_only flag.

    Args:
        icon_only: Whether the button displays only an icon (no text).
        density: The button density ('default' or 'compact').

    Returns:
        The icon size in pixels.
    """
    from tkinter import font

    if icon_only:
        return 23 if density != 'compact' else 18

    # Get icon size from font ascent for proper alignment with text
    # Different buffers compensate for y_bias effect per density
    font_name = 'caption' if density == 'compact' else 'body'
    f = font.nametofont(font_name)
    buffer = 4 if density == 'compact' else 3
    return f.metrics()['ascent'] + buffer


def button_font(density: str) -> str:
    """Get the font token for a button based on its density.

    Args:
        density: The button density ('default' or 'compact').

    Returns:
        The font token name.
    """
    return 'caption' if density == 'compact' else 'body'


def button_padding(b: BootstyleBuilderTTk, icon_only: bool, density: Any) -> int | tuple[int, ...]:
    """Calculate button padding based on options.

    Args:
        b: The bootstyle builder instance.
        icon_only: Whether the button displays only an icon.
        density: The button density ('default' or 'compact').

    Returns:
        Padding value (0 for icon_only, scaled tuple otherwise).
    """
    if icon_only:
        return b.scale((2, 3, 2, 3)) if density == 'compact' else 0
    if density == 'compact':
        # (left, top, right, bottom) - extra top padding to center text
        return b.scale((6, 5, 6, 3))
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


# Entry/Field utilities
# These utilities are used by entry-type style builders (Entry, Combobox, Spinbox, Field).

def entry_font(density: str) -> str:
    """Get the font for an entry widget based on its density.

    Args:
        density: The entry density ('default' or 'compact').

    Returns:
        The Tk font name.
    """
    from ttkbootstrap.style.typography import get_font
    font_token = 'caption' if density == 'compact' else 'body'
    return str(get_font(font_token))


def entry_padding(b: BootstyleBuilderTTk, density: str) -> tuple:
    """Get entry padding based on density.

    Args:
        b: The bootstyle builder instance.
        density: The entry density ('default' or 'compact').

    Returns:
        Scaled padding tuple (horizontal, vertical).
    """
    if density == 'compact':
        return b.scale((6, 0))
    return b.scale((6, 0))

def field_height(b: BootstyleBuilderTTk, density: str) -> int:
    """Get entry element height based on density.

    Args:
        b: The bootstyle builder instance.
        density: The entry density ('default' or 'compact').

    Returns:
        Scaled height in pixels.
    """
    return b.scale(26) if density == 'compact' else b.scale(33)

def entry_height(b: BootstyleBuilderTTk, density: str) -> int:
    """Get entry element height based on density.

    Args:
        b: The bootstyle builder instance.
        density: The entry density ('default' or 'compact').

    Returns:
        Scaled height in pixels.
    """
    return b.scale(25) if density == 'compact' else b.scale(31)


def entry_icon_size(b: BootstyleBuilderTTk, density: str) -> int:
    """Get icon size for entry widgets (chevrons, spinner arrows).

    Args:
        b: The bootstyle builder instance.
        density: The entry density ('default' or 'compact').

    Returns:
        Scaled icon size in pixels.
    """
    return b.scale(12) if density == 'compact' else b.scale(14)


def entry_image_key(base: str, density: str) -> str:
    """Get density-aware manifest key for entry elements.

    Args:
        base: Base key name (e.g., 'input', 'input_before', 'input_after').
        density: The entry density ('default' or 'compact').

    Returns:
        Full manifest key with density suffix (e.g., 'input_default', 'input_compact').
    """
    return f'{base}_{density}'


def spinner_arrow_height(b: BootstyleBuilderTTk, density: str) -> int:
    """Get height for spinner arrow elements based on density.

    Args:
        b: The bootstyle builder instance.
        density: The entry density ('default' or 'compact').

    Returns:
        Scaled arrow height in pixels.
    """
    return b.scale(10) if density == 'compact' else b.scale(13)


def spinner_arrow_width(b: BootstyleBuilderTTk) -> int:
    """Get width for spinner arrow elements.

    Args:
        b: The bootstyle builder instance.

    Returns:
        Scaled arrow width in pixels.
    """
    return b.scale(16)


def chevron_width(b: BootstyleBuilderTTk) -> int:
    """Get width for combobox chevron element.

    Args:
        b: The bootstyle builder instance.

    Returns:
        Scaled chevron width in pixels.
    """
    return b.scale(16)
