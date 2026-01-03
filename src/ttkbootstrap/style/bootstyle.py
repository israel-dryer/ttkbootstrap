"""Bootstyle parsing and widget integration for ttkbootstrap.

Handles parsing of bootstyle strings and provides integration layer between
user-friendly bootstyle syntax and TTK style names.
"""

from __future__ import annotations

import warnings
from typing import Optional

from ttkbootstrap.runtime.app import get_app_settings
from ttkbootstrap.core.exceptions import BootstyleParsingError
from ttkbootstrap.style.token_maps import (COLOR_TOKENS, CONTAINER_CLASSES, ORIENT_CLASSES, WIDGET_CLASS_MAP)


def _warn_bootstyle_deprecated():
    """Issue deprecation warning for bootstyle parameter usage.

    Uses dynamic stack level detection to find the user's code,
    accounting for variable MRO depths across different widget types.
    """
    import sys
    import os

    # Walk up the stack to find the first frame outside ttkbootstrap package
    frame = sys._getframe(1)
    level = 2  # Start at 2 (1 for this function, 1 for caller)

    # Get the actual ttkbootstrap package path (src/ttkbootstrap), normalized
    ttkbootstrap_pkg_path = os.path.normpath(os.path.dirname(os.path.dirname(__file__)))

    while frame.f_back is not None:
        frame = frame.f_back
        level += 1  # Increment BEFORE checking, so level points to this frame
        filepath = os.path.normpath(frame.f_code.co_filename)
        # Stop when we find code outside ttkbootstrap package
        if ttkbootstrap_pkg_path not in filepath:
            break

    warnings.warn(
        "The 'bootstyle' parameter is deprecated. "
        "Use 'accent' and 'variant' parameters instead.",
        FutureWarning,
        stacklevel=level
    )


def convert_bootstyle_to_accent_variant(
        bootstyle: str,
        widget_class: str,
        warn: bool = True
) -> tuple[Optional[str], Optional[str]]:
    """Convert bootstyle string to separate accent and variant.

    Args:
        bootstyle: Bootstyle string (e.g., "success-outline", "primary")
        widget_class: TTK widget class for variant validation
        warn: Whether to issue deprecation warning

    Returns:
        Tuple of (accent, variant) where either may be None
    """
    if not bootstyle:
        return None, None

    if warn:
        _warn_bootstyle_deprecated()

    parsed = parse_bootstyle(bootstyle, widget_class)
    return parsed.get('accent'), parsed.get('variant')


def parse_bootstyle_v2(bootstyle: str, widget_class: str) -> dict:
    """Parse bootstyle string using V2 syntax (dash-separated).

    Syntax: `accent-variant-widget` where all parts are optional.
    Checks actual theme colors and registered variants. Unknown parts are
    treated as custom colors.

    Args:
        bootstyle: Bootstyle string (e.g., "success-outline", "primary")
        widget_class: TTK widget class name (e.g., "TButton")

    Returns:
        Dict with: accent, variant, widget_class, cross_widget
    """
    if not bootstyle:
        return {
            'accent': None,
            'variant': "default",
            'widget_class': widget_class,
            'cross_widget': False,
            'orient': None,
        }

    from ttkbootstrap.style.bootstyle_builder_ttk import BootstyleBuilderTTk
    from ttkbootstrap.style.theme_provider import use_theme

    theme_colors = use_theme().colors
    if not isinstance(bootstyle, str):
        raise BootstyleParsingError(f'bootstyle must be a string. Received the value: {bootstyle}')
    parts = bootstyle.lower().split('-')

    accent = None
    variant = None
    resolved_widget = widget_class
    cross_widget = False
    orient = None

    # First pass: resolve widget target (so variant tokens can be validated)
    for part in parts:
        if part in WIDGET_CLASS_MAP:
            resolved_widget = WIDGET_CLASS_MAP[part]
            if resolved_widget != widget_class:
                cross_widget = True

    # Second pass: resolve accent/variant/orientation
    for part in parts:
        if part in WIDGET_CLASS_MAP:
            # already handled in first pass
            continue
        if part in theme_colors or part in COLOR_TOKENS or '[' in part:
            accent = part
            continue
        if part in ("horizontal", "vertical"):
            orient = part
            continue
        if BootstyleBuilderTTk.has_builder(resolved_widget, part):
            variant = part
            continue
        # If we reach here, it's unrecognized
        message = f"Unrecognized variant or accent token: '{part}'"
        raise BootstyleParsingError(message)

    return {
        'accent': accent,
        'variant': variant,
        'widget_class': resolved_widget,
        'cross_widget': cross_widget,
        'orient': orient
    }


def to_pascal_case(s: str) -> str:
    """Convert dash-separated string to PascalCase.

    Examples:
        'context-check' -> 'ContextCheck'
        'outline' -> 'Outline'
        'solid' -> 'Solid'
    """
    return ''.join(part.capitalize() for part in s.split('-'))


def from_pascal_case(s: str) -> str:
    """Convert PascalCase string to dash-separated lowercase.

    Examples:
        'ContextCheck' -> 'context-check'
        'Outline' -> 'outline'
        'Solid' -> 'solid'
    """
    import re
    # Insert dash before uppercase letters (except at start), then lowercase
    return re.sub(r'(?<!^)(?=[A-Z])', '-', s).lower()


def generate_ttk_style_name(
        accent: Optional[str],
        variant: Optional[str],
        widget_class: str,
        custom_prefix: Optional[str] = None,
        orient: Optional[str] = None,
) -> str:
    """Generate TTK style name from parsed components.

    Returns style name in format: [custom_prefix].[accent].[Variant].[Orient].[Widget]
    """
    parts = []

    if custom_prefix:
        parts.append(custom_prefix)
    if accent:
        parts.append(accent)
    if variant:
        parts.append(to_pascal_case(variant))
    if orient:
        parts.append(normalize_orientation(orient))
    parts.append(widget_class)
    return '.'.join(parts)


def normalize_orientation(orient: str):
    """Normalize TTK style orientation."""
    if orient.lower().startswith('v'):
        return 'Vertical'
    else:
        return 'Horizontal'


def parse_bootstyle_legacy(bootstyle: str, widget_class: str) -> dict:
    """Parse bootstyle using legacy V1 regex syntax (deprecated).

    Currently falls back to V2 parsing. TODO: Extract actual legacy logic.
    """
    return parse_bootstyle_v2(bootstyle, widget_class)


def parse_bootstyle(bootstyle: str, widget_class: str) -> dict:
    """Parse bootstyle string using configured parsing method.

    Main entry point for bootstyle parsing.
    """
    return parse_bootstyle_v2(bootstyle, widget_class)


def extract_orient_from_style(ttk_style: str):
    """Extract orientation from TTK style name."""
    if 'horizontal' in ttk_style.lower():
        return 'Horizontal'
    elif 'vertical' in ttk_style.lower():
        return 'Vertical'
    else:
        return None


def extract_accent_from_style(ttk_style: str, default: str = 'primary') -> str:
    """Extract accent token from TTK style name, including modifiers like [subtle]."""
    parts = ttk_style.split('.')

    # Skip custom prefix if present (e.g., bs[hash] or custom_xyz)
    if parts and (parts[0].startswith('bs[') or parts[0].startswith('custom_')):
        parts = parts[1:]

    for part in parts:
        part_lower = part.lower()
        # Check exact match first
        if part_lower in COLOR_TOKENS:
            return part_lower
        # Check if base accent (before modifier) is an accent token
        # e.g., 'primary[subtle]' -> 'primary'
        if '[' in part_lower:
            base_accent = part_lower.split('[')[0]
            if base_accent in COLOR_TOKENS:
                return part_lower  # Return full token with modifier

    return default


def extract_variant_from_style(ttk_style: str, widget_class: str = None) -> Optional[str]:
    """Extract variant name from TTK style name.

    Args:
        ttk_style: The TTK style name to parse.
        widget_class: Optional widget class from winfo_class() to exclude from parsing.

    Returns:
        Variant name in dash-separated lowercase format (e.g., 'context-check')
    """
    parts = ttk_style.split('.')

    # Skip custom prefix if present (e.g., bs[hash] or custom_xyz)
    if parts and (parts[0].startswith('bs[') or parts[0].startswith('custom_')):
        parts = parts[1:]

    # Build set of class-related parts to skip (e.g., 'Expander', 'TLabel')
    class_parts = set()
    if widget_class:
        class_parts.update(widget_class.split('.'))

    for part in parts:
        part_lower = part.lower()
        # Skip color tokens (including those with modifiers like 'primary[subtle]')
        if part_lower in COLOR_TOKENS:
            continue
        if '[' in part_lower:
            base_color = part_lower.split('[')[0]
            if base_color in COLOR_TOKENS:
                continue
        # Skip known class parts from widget_class
        if part in class_parts:
            continue
        # Skip standard ttk class names (TLabel, TButton, etc.)
        if part.startswith('T'):
            continue
        # Skip orientation parts
        if part in ('Horizontal', 'Vertical'):
            continue
        # Found a variant - convert from PascalCase to dash-separated
        return from_pascal_case(part)

    return None


def extract_widget_class_from_style(ttk_style: str) -> Optional[str]:
    """Extract widget class from TTK style name."""
    parts = ttk_style.split('.')

    for part in parts:
        if part.startswith('T'):
            return part

    return None


class Bootstyle:
    """Widget integration layer for bootstyle functionality.

    Wires ttkbootstrap into tkinter/ttk by overriding widget constructors and
    configure methods to accept `bootstyle` parameter.
    """

    @staticmethod
    def create_ttk_style(
            widget_class: str,
            bootstyle: Optional[str] = None,
            style_options: Optional[dict] = None,
            *,
            accent: Optional[str] = None,
            variant: Optional[str] = None,
    ) -> str:
        """Create or get TTK style name for a widget.

        Parses bootstyle string OR uses accent/variant directly to generate
        TTK style name and trigger style creation.

        Args:
            widget_class: TTK widget class (e.g., "TButton")
            bootstyle: DEPRECATED - Use accent and variant instead
            style_options: Custom style options dict
            accent: Accent token (e.g., "success", "primary[subtle]")
            variant: Variant name (e.g., "outline", "solid")

        Returns:
            Generated TTK style name
        """
        from ttkbootstrap.style.bootstyle_builder_ttk import BootstyleBuilderTTk

        # Handle legacy bootstyle parameter
        if bootstyle:
            if accent is not None or variant is not None:
                raise ValueError(
                    "Cannot use 'bootstyle' together with 'accent' or 'variant'. "
                    "Use either bootstyle (deprecated) OR accent/variant."
                )
            # Parse bootstyle (warning already issued at widget level)
            parsed = parse_bootstyle(bootstyle, widget_class)
            accent = parsed['accent']
            variant = parsed['variant']
            widget_class = parsed['widget_class']  # May be cross-widget

        # If no accent and no variant, return base widget class
        if not accent and not variant:
            return widget_class

        # Initialize style_options to empty dict if None
        if style_options is None:
            style_options = {}

        surface = style_options.get("surface")

        builder_variant = variant if variant is not None else \
            BootstyleBuilderTTk.get_default_variant(widget_class)

        custom_prefix = None

        if style_options.keys() or surface != 'background':
            import hashlib
            import json
            options_str = json.dumps(style_options, sort_keys=True)
            options_hash = hashlib.md5(options_str.encode()).hexdigest()[:8]
            custom_prefix = f"bs[{options_hash}]"

        ttk_style = generate_ttk_style_name(
            accent=accent,
            variant=variant,
            widget_class=widget_class,
            custom_prefix=custom_prefix,
            orient=style_options.get('orient'),
        )

        from ttkbootstrap.style.style import get_style
        style = get_style()

        style.create_style(
            widget_class=widget_class,
            variant=builder_variant,
            ttk_style=ttk_style,
            accent=accent,
            options=style_options
        )

        return ttk_style

    @staticmethod
    def override_ttk_widget_constructor(func):
        """Override ttk widget __init__ to accept bootstyle, accent, and variant parameters."""

        def __init__wrapper(self, *args, **kwargs):

            # Extract new accent/variant parameters
            accent = kwargs.pop("accent", None)
            variant = kwargs.pop("variant", None)

            # Extract legacy bootstyle parameter
            had_style_kwarg = 'style' in kwargs
            bootstyle = kwargs.pop("bootstyle", "")

            # Check for conflicting params (bootstyle with accent/variant)
            if bootstyle and (accent is not None or variant is not None):
                raise ValueError(
                    "Cannot use 'bootstyle' together with 'accent' or 'variant'. "
                    "Use either bootstyle (deprecated) OR accent/variant."
                )

            style_options = kwargs.pop("style_options", {})
            inherit_surface = kwargs.pop('inherit_surface', None)
            surface_token = kwargs.pop('surface', None)

            # Extract ttk_class for style lookup (doesn't affect widget's actual class_)
            # This allows custom style builders without affecting bindtags
            ttk_class = kwargs.pop('ttk_class', None)

            func(self, *args, **kwargs)  # the actual widget constructor

            # Use ttk_class for style lookup if provided, otherwise use widget's actual class
            widget_class = self.winfo_class()
            style_class = ttk_class or widget_class

            # Handle bootstyle -> accent/variant conversion AFTER widget constructor
            # so we have the correct style_class for variant validation
            if bootstyle:
                _warn_bootstyle_deprecated()
                bs_accent, bs_variant = convert_bootstyle_to_accent_variant(
                    bootstyle, style_class, warn=False  # Already warned above
                )
                accent = bs_accent
                variant = bs_variant

            # ===== Surface color inheritance =====

            if inherit_surface is None:
                inherit_surface = get_app_settings().inherit_surface_color

            if hasattr(self, 'master') and self.master is not None:
                parent_surface_token = getattr(self.master, '_surface', 'content')
            else:
                parent_surface_token = 'content'

            if surface_token:
                effective_surface_token = surface_token
            elif inherit_surface:
                effective_surface_token = parent_surface_token
            else:
                effective_surface_token = 'content'

            # container widgets can take their surface color from the accent param
            # Use style_class so custom ttk_class like 'Field' can opt out of this behavior
            if accent and style_class in CONTAINER_CLASSES and surface_token is None:
                effective_surface_token = accent

            # cache the surface color for child components
            setattr(self, '_surface', effective_surface_token)
            if effective_surface_token != 'content' and effective_surface_token is not None:
                style_options.setdefault('surface', effective_surface_token)

            # ==== Orientation =====

            # handle widgets with orientation
            if widget_class in ORIENT_CLASSES:
                orient = str(self.cget('orient'))
                style_options.setdefault('orient', orient)

            # ==== Create actual ttk style & assign to widget =====

            if (accent or variant) and style_class:

                ttk_style = Bootstyle.create_ttk_style(
                    widget_class=style_class,
                    style_options=style_options,
                    accent=accent,
                    variant=variant,
                )
                self.configure(style=ttk_style)

            elif style_class and not had_style_kwarg:
                from ttkbootstrap.style.bootstyle_builder_ttk import BootstyleBuilderTTk
                from ttkbootstrap.style.style import get_style

                default_variant = BootstyleBuilderTTk.get_default_variant(style_class)

                if BootstyleBuilderTTk.has_builder(style_class, default_variant):

                    # Build options first so we can decide if a custom bs[...] prefix is needed
                    custom_prefix = None
                    if style_options.keys():
                        import hashlib
                        import json
                        options_str = json.dumps(style_options, sort_keys=True)
                        options_hash = hashlib.md5(options_str.encode()).hexdigest()[:8]
                        custom_prefix = f"bs[{options_hash}]"

                    ttk_style = generate_ttk_style_name(
                        accent=None,
                        variant=default_variant,
                        widget_class=style_class,
                        custom_prefix=custom_prefix,
                    )

                    style_instance = get_style()
                    if style_instance is not None:
                        style_instance.create_style(
                            widget_class=style_class,
                            variant=default_variant,
                            ttk_style=ttk_style,
                            options=style_options,
                        )
                        self.configure(style=ttk_style)
                else:
                    self.configure(style=style_class)

            # Store accent, variant, ttk_class, and style_options for later retrieval
            setattr(self, '_accent', accent)
            setattr(self, '_variant', variant)
            setattr(self, '_ttk_class', ttk_class)
            setattr(self, '_style_options', style_options)

        return __init__wrapper

    @staticmethod
    def override_tk_widget_constructor(func):
        """Override Tk widget __init__ to apply theme background when autostyle=True."""

        def __init__wrapper(self, *args, **kwargs):

            # capture bootstrap arguments
            auto_style = kwargs.pop("autostyle", True)
            inherit_surface = kwargs.pop('inherit_surface', None)
            if inherit_surface is None:
                inherit_surface = get_app_settings().inherit_surface_color
            surface_token = kwargs.pop('surface', None)

            func(self, *args, **kwargs)  # the actual constructor

            # ===== Surface color inheritance =====

            if hasattr(self, 'master') and self.master is not None:
                parent_surface_token = getattr(self.master, '_surface', 'content')
            else:
                parent_surface_token = 'content'

            if inherit_surface:
                surface_token = parent_surface_token
            else:
                surface_token = surface_token or 'content'

            setattr(self, '_surface', surface_token)

            if not auto_style:
                return

            # ==== Update widget style & register for theme changes =====

            from ttkbootstrap.style.style import get_style
            from ttkbootstrap.style.bootstyle_builder_tk import BootstyleBuilderBuilderTk
            style = get_style()
            builder_tk = BootstyleBuilderBuilderTk(
                theme_provider=style.theme_provider if style else None,
                style_instance=style
            )
            surface = getattr(self, '_surface', 'content')
            builder_tk.call_builder(self, surface=surface)

            style.register_tk_widget(self)

        return __init__wrapper


__all__ = [
    'parse_bootstyle',
    'parse_bootstyle_v2',
    'parse_bootstyle_legacy',
    'generate_ttk_style_name',
    'extract_accent_from_style',
    'extract_variant_from_style',
    'extract_widget_class_from_style',
    'convert_bootstyle_to_accent_variant',
    'Bootstyle',
]
