"""Bootstyle parsing and widget integration for ttkbootstrap.

This module handles the parsing of bootstyle strings and provides the
integration layer between user-friendly bootstyle syntax and TTK style names.

Two parsing modes are supported:
1. **New V2 Parsing** (default): Simple dash-separated pattern
2. **Legacy V1 Parsing**: Complex regex-based parsing (deprecated)

The parsing mode is controlled by the AppConfig.legacy_bootstyle flag.
"""

from __future__ import annotations

from typing import Optional

from ttkbootstrap.appconfig import AppConfig

# =============================================================================
# Color and Widget Constants
# =============================================================================

# Standard ttkbootstrap color tokens
COLORS = {
    'primary', 'secondary', 'success', 'info',
    'warning', 'danger', 'light', 'dark'
}

# Widget class name mappings (common name <-> TTK class name)
WIDGET_CLASS_MAP = {
    'button': 'TButton',
    'label': 'TLabel',
    'entry': 'TEntry',
    'frame': 'TFrame',
    'labelframe': 'TLabelframe',
    'progressbar': 'TProgressbar',
    'scale': 'TScale',
    'scrollbar': 'TScrollbar',
    'checkbutton': 'TCheckbutton',
    'radiobutton': 'TRadiobutton',
    'combobox': 'TCombobox',
    'notebook': 'TNotebook',
    'treeview': 'Treeview',
    'separator': 'TSeparator',
    'sizegrip': 'TSizegrip',
    'panedwindow': 'TPanedwindow',
    'spinbox': 'TSpinbox',
    'menubutton': 'TMenubutton',
}

WIDGET_NAME_MAP = {v: k for k, v in WIDGET_CLASS_MAP.items()}


# =============================================================================
# V2 Parsing (New System)
# =============================================================================

def parse_bootstyle_v2(bootstyle: str, widget_class: str) -> dict:
    """Parse bootstyle string using V2 syntax (dash-separated).

    The V2 syntax is: `color-variant-widget` where all parts are optional.

    Args:
        bootstyle: Bootstyle string (e.g., "success-outline", "primary")
        widget_class: TTK widget class name (e.g., "TButton")

    Returns:
        Dict with parsed components:
            - color: Color token or None
            - variant: Variant name or None
            - widget_class: Resolved widget class name
            - cross_widget: True if widget override detected

    Examples:
        >>> parse_bootstyle_v2("success-outline", "TButton")
        {'color': 'success', 'variant': 'outline', 'widget_class': 'TButton', 'cross_widget': False}

        >>> parse_bootstyle_v2("primary", "TLabel")
        {'color': 'primary', 'variant': None, 'widget_class': 'TLabel', 'cross_widget': False}

        >>> parse_bootstyle_v2("outline-button", "TLabel")
        {'color': None, 'variant': 'outline', 'widget_class': 'TButton', 'cross_widget': True}
    """
    if not bootstyle:
        return {
            'color': None,
            'variant': None,
            'widget_class': widget_class,
            'cross_widget': False
        }

    # Split on dashes
    parts = bootstyle.lower().split('-')

    color = None
    variant = None
    resolved_widget = widget_class
    cross_widget = False

    # Process each part
    for part in parts:
        # Check if it's a color token
        if part in COLORS:
            color = part
        # Check if it's a widget name
        elif part in WIDGET_CLASS_MAP:
            resolved_widget = WIDGET_CLASS_MAP[part]
            if resolved_widget != widget_class:
                cross_widget = True
        # Otherwise treat as variant
        else:
            variant = part

    return {
        'color': color,
        'variant': variant,
        'widget_class': resolved_widget,
        'cross_widget': cross_widget
    }


def generate_ttk_style_name(
        color: Optional[str],
        variant: Optional[str],
        widget_class: str,
        custom_prefix: Optional[str] = None) -> str:
    """Generate TTK style name from parsed components.

    Args:
        color: Color token (e.g., "success") or None
        variant: Variant name (e.g., "outline") or None
        widget_class: TTK widget class (e.g., "TButton")
        custom_prefix: Optional custom prefix (e.g., "custom_abc123")

    Returns:
        Full TTK style name

    Examples:
        >>> generate_ttk_style_name("success", "outline", "TButton")
        'success.Outline.TButton'

        >>> generate_ttk_style_name("primary", None, "TLabel")
        'primary.TLabel'

        >>> generate_ttk_style_name(None, "outline", "TButton", "custom_abc")
        'custom_abc.Outline.TButton'
    """
    parts = []

    # Add custom prefix if provided
    if custom_prefix:
        parts.append(custom_prefix)

    # Add color
    if color:
        parts.append(color)

    # Add variant (capitalized)
    if variant:
        parts.append(variant.capitalize())

    # Add widget class
    parts.append(widget_class)

    return '.'.join(parts)


# =============================================================================
# V1 Parsing (Legacy System)
# =============================================================================

def parse_bootstyle_legacy(bootstyle: str, widget_class: str) -> dict:
    """Parse bootstyle string using legacy V1 regex-based syntax.

    This method is deprecated and maintained only for backward compatibility.
    It will be removed in a future version.

    Args:
        bootstyle: Bootstyle string (legacy format)
        widget_class: TTK widget class name

    Returns:
        Dict with parsed components (same format as V2)

    Note:
        This is a placeholder. The actual legacy parsing logic would need
        to be extracted from the old style/__init__.py file.
    """
    # TODO: Extract actual legacy parsing logic from style/__init__.py
    # For now, fall back to V2 parsing
    return parse_bootstyle_v2(bootstyle, widget_class)


# =============================================================================
# Main Parsing Entry Point
# =============================================================================

def parse_bootstyle(bootstyle: str, widget_class: str) -> dict:
    """Parse bootstyle string using configured parsing method.

    This is the main entry point for bootstyle parsing. It checks the
    AppConfig.legacy_bootstyle flag to determine which parsing method to use.

    Args:
        bootstyle: Bootstyle string to parse
        widget_class: TTK widget class name

    Returns:
        Dict with parsed components:
            - color: Color token or None
            - variant: Variant name or None
            - widget_class: Resolved widget class name
            - cross_widget: True if widget override detected

    Examples:
        >>> # With legacy_bootstyle=False (default), uses V2 parsing
        >>> result = parse_bootstyle("success-outline", "TButton")
        >>> result['color']
        'success'
        >>> result['variant']
        'outline'
        >>> result['widget_class']
        'TButton'
    """
    # Check which parsing method to use
    use_legacy = AppConfig.get('legacy_bootstyle', False)

    if use_legacy:
        # ========== LEGACY V1 PARSING ==========
        return parse_bootstyle_legacy(bootstyle, widget_class)
    else:
        # ========== NEW V2 PARSING ==========
        return parse_bootstyle_v2(bootstyle, widget_class)


# =============================================================================
# TTK Style Name Utilities
# =============================================================================

def extract_color_from_style(ttk_style: str, default: str = 'primary') -> str:
    """Extract color token from TTK style name.

    Args:
        ttk_style: Full TTK style name (e.g., "custom_abc.success.Outline.TButton")
        default: Default color if none found

    Returns:
        Color token name (e.g., "success")

    Examples:
        >>> extract_color_from_style("success.Outline.TButton")
        'success'

        >>> extract_color_from_style("custom_abc.danger.TLabel")
        'danger'

        >>> extract_color_from_style("TButton")
        'primary'
    """
    # Remove custom prefix if present
    parts = ttk_style.split('.')
    if parts and parts[0].startswith('custom_'):
        parts = parts[1:]

    # Find color in parts
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

    # Find variant (not color, not widget class)
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

    # Find widget class (starts with 'T' or is 'Treeview')
    for part in parts:
        if part.startswith('T'):
            return part

    return None


# =============================================================================
# Bootstyle Class (Widget Integration)
# =============================================================================

class Bootstyle:
    """Widget integration layer for bootstyle functionality.

    This class provides methods for integrating bootstyle parsing with
    TTK widget constructors and the Style class.

    Note:
        This is currently a placeholder. The actual implementation would
        include widget constructor overrides and integration with the
        Style class to trigger style creation.
    """

    @staticmethod
    def create_ttk_style(
            widget_class: str,
            bootstyle: Optional[str] = None,
            style_options: Optional[dict] = None) -> str:
        """Create or get TTK style name for a widget.

        This method parses the bootstyle string, generates the TTK style name,
        and triggers style creation if needed.

        Args:
            widget_class: TTK widget class (e.g., "TButton")
            bootstyle: Optional bootstyle string (e.g., "success-outline")
            style_options: Optional custom styling options

        Returns:
            TTK style name to apply to widget

        Examples:
            >>> Bootstyle.create_ttk_style("TButton", "success-outline")
            'success.Outline.TButton'

            >>> Bootstyle.create_ttk_style("TLabel", "primary")
            'primary.TLabel'
        """
        from ttkbootstrap.style.bootstyle_builder import BootstyleBuilder

        # If no bootstyle, return default widget class
        if not bootstyle:
            return widget_class

        # Parse bootstyle string
        parsed = parse_bootstyle(bootstyle, widget_class)

        color = parsed['color']
        variant = parsed['variant']
        resolved_widget = parsed['widget_class']

        # Generate custom prefix if style_options provided
        custom_prefix = None
        if style_options:
            # Hash the options to create unique prefix
            import hashlib
            import json
            options_str = json.dumps(style_options, sort_keys=True)
            options_hash = hashlib.md5(options_str.encode()).hexdigest()[:8]
            custom_prefix = f"custom_{options_hash}"

        # Determine builder variant (use default if not specified)
        # Note: We keep the variant as None for the style name if not specified,
        # but use the default variant when calling the builder
        builder_variant = variant if variant is not None else \
            BootstyleBuilder.get_default_variant(resolved_widget)

        # Generate TTK style name (variant is None if not specified)
        ttk_style = generate_ttk_style_name(
            color=color,
            variant=variant,  # None if not specified -> simpler style name
            widget_class=resolved_widget,
            custom_prefix=custom_prefix
        )

        # TODO: Trigger style creation through Style.get_instance()
        # from ttkbootstrap.style.style import Style
        # style = Style.get_instance()
        # style.create_style(
        #     widget_class=resolved_widget,
        #     variant=builder_variant,  # Use default if not specified
        #     ttkstyle=ttk_style,
        #     options=style_options
        # )

        return ttk_style


# =============================================================================
# Module Exports
# =============================================================================

__all__ = [
    # Main parsing functions
    'parse_bootstyle',
    'parse_bootstyle_v2',
    'parse_bootstyle_legacy',

    # Style name generation
    'generate_ttk_style_name',

    # Extraction utilities
    'extract_color_from_style',
    'extract_variant_from_style',
    'extract_widget_class_from_style',

    # Widget integration
    'Bootstyle',

    # Constants
    'COLORS',
    'WIDGET_CLASS_MAP',
    'WIDGET_NAME_MAP',
]
