"""Utility functions for style builders.

This module provides common utilities used across builder functions,
including accent extraction, variant parsing, and style name manipulation.
"""

from __future__ import annotations

from typing import Optional

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
