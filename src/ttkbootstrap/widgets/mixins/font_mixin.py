"""Font modifier syntax for inline font customization in ttkbootstrap widgets.

This module provides a mixin that enables concise font modification syntax for all
ttkbootstrap widgets. The syntax uses bracket notation similar to bootstyle modifiers,
allowing inline font customization without creating custom Font objects.

Syntax
------
The full modifier syntax follows the pattern: `family[size][weight][style]`

All components are optional and can be mixed in any combination. When components are
omitted, the widget's current font values are preserved.

Components:
    - family: Font family name or typography token (e.g., 'helvetica', 'body', 'heading-lg')
    - size: Point size (e.g., '16'), pixel size (e.g., '16px'), or size token (e.g., 'sm', 'lg')
    - weight: 'bold' or 'normal'
    - style: 'italic', 'roman', 'underline', 'overstrike' (comma-separated for multiple)

Size Tokens:
    xs=8pt, sm=10pt, md=12pt, lg=14pt, xl=16pt, xxl=18pt

Font Tokens:
    body, label, heading-md, heading-lg, heading-xl, display-lg, display-xl,
    code, hyperlink, caption, body-sm, body-lg, body-xl

Behavior
--------
- **At widget creation**: Modifiers are applied to the widget's default style font
- **At runtime**: Modifiers are applied to the widget's current font
- **Missing family**: Uses widget's current font family (or 'body' token if none)
- **Missing size**: Uses widget's current font size (or 'body' token size if none)

Examples
--------
Basic modifications::

    # Use body token, make it bold
    Label(root, text="Title", font="body[bold]")

    # Change current font to 16pt (preserves family)
    label.configure(font="[16]")

    # Make current font bold and italic (preserves family and size)
    label.configure(font="[bold,italic]")

Custom font families::

    # Helvetica, 16pt, bold
    Button(root, text="Click", font="helvetica[16][bold]")

    # Arial, 14 pixels (negative in Tk), bold and italic
    Label(root, text="Text", font="arial[14px][bold,italic]")

Size tokens::

    # Small size (10pt) with bold
    Entry(root, font="[sm][bold]")

    # Large size (14pt)
    Label(root, font="[lg]")

Font tokens with modifiers::

    # Heading-lg token with italic style
    Label(root, text="Heading", font="heading-lg[italic]")

    # Label token at custom size
    Button(root, text="Button", font="label[16]")

Multiple style modifiers::

    # Bold, italic, and underlined
    Label(root, text="Emphasis", font="[16][bold,italic,underline]")

Integration
-----------
FontMixin is automatically integrated into all ttkbootstrap widgets via TTKWrapperBase.
No additional setup is required - all widgets supporting the 'font' argument automatically
gain modifier syntax support.

The mixin uses the @configure_delegate pattern to intercept font configuration, parse
the modifier syntax, and apply the resolved font specification to the underlying ttk widget.
"""

from __future__ import annotations

import re
from typing import Any, Literal, TYPE_CHECKING

if TYPE_CHECKING:
    from ttkbootstrap.style.typography import Typography, FontTokenNames

from ttkbootstrap.widgets.mixins.configure_mixin import configure_delegate


# Size tokens mapping (shortcuts for common sizes)
SIZE_TOKENS = {
    'xs': 8,
    'sm': 10,
    'md': 12,
    'lg': 14,
    'xl': 16,
    'xxl': 18,
}


def _get_font_token_names() -> set[str]:
    """Get all valid font token names (lazy to avoid import issues)."""
    from ttkbootstrap.style.typography import FontTokenNames
    return {
        name.replace('_', '-')
        for name in dir(FontTokenNames)
        if not name.startswith('_')
    }


def parse_font_modifier(font_spec: str) -> dict[str, Any]:
    """Parse font modifier syntax string into configuration dict.

    Args:
        font_spec: Font specification string (e.g., "helvetica[16][bold]")

    Returns:
        Dict with keys: family, size, weight, slant, underline, overstrike
    """
    if not font_spec or not font_spec.strip():
        return {}

    result = {}

    # Find all bracketed parts: [content]
    bracket_pattern = r'\[([^\]]+)\]'
    parts = re.findall(bracket_pattern, font_spec)

    # Get family/token (everything before first bracket, or whole string if no brackets)
    if '[' in font_spec:
        family_part = font_spec[:font_spec.index('[')].strip()
    else:
        family_part = font_spec.strip()

    if family_part:
        result['family'] = family_part

    # Process each bracketed part
    for part in parts:
        part = part.strip()
        if not part:
            continue

        # Check if it's a pixel size (e.g., "16px")
        if part.endswith('px'):
            try:
                # Pixel sizes are negative in Tk
                result['size'] = -int(part[:-2])
                continue
            except ValueError:
                pass

        # Check if it's a point size (e.g., "16")
        if part.isdigit():
            result['size'] = int(part)
            continue

        # Check if it's a size token (e.g., "sm", "lg")
        if part in SIZE_TOKENS:
            result['size'] = SIZE_TOKENS[part]
            continue

        # Otherwise, treat as comma-separated modifiers
        modifiers = [m.strip().lower() for m in part.split(',')]
        for modifier in modifiers:
            if not modifier:
                continue

            # Weight modifiers
            if modifier in ('bold', 'normal'):
                result['weight'] = modifier
            # Slant modifiers
            elif modifier in ('italic', 'roman'):
                result['slant'] = modifier
            # Boolean modifiers
            elif modifier == 'underline':
                result['underline'] = True
            elif modifier == 'overstrike':
                result['overstrike'] = True

    return result


def build_font_from_modifier(font_spec: str, base_font: Any = None) -> tuple | str:
    """Build Tk-compatible font tuple from modifier syntax, using base_font for missing values.

    Args:
        font_spec: Font specification with modifier syntax (e.g., "[16][bold]")
        base_font: Base font to extend (token name or tuple); defaults to 'body' token

    Returns:
        Font tuple like ('Helvetica', 16, 'bold italic') or token name
    """
    from ttkbootstrap.style.typography import Typography

    parsed = parse_font_modifier(font_spec)
    if not parsed:
        return base_font or 'body'

    # Start with base font configuration
    config = {}
    family_is_token = False
    font_token_names = _get_font_token_names()

    # Check if family is a known token
    if 'family' in parsed:
        family_name = parsed['family']
        if family_name in font_token_names:
            # It's a font token - get its spec
            token_spec = Typography.get_token(family_name)
            config['family'] = token_spec.font
            config['size'] = token_spec.size
            config['weight'] = token_spec.weight
            if token_spec.underline:
                config['underline'] = token_spec.underline
            family_is_token = True
        else:
            # It's a font family name
            config['family'] = family_name
    elif base_font:
        # Use base font if provided
        if isinstance(base_font, str) and base_font in font_token_names:
            token_spec = Typography.get_token(base_font)
            config['family'] = token_spec.font
            config['size'] = token_spec.size
            config['weight'] = token_spec.weight
            if token_spec.underline:
                config['underline'] = token_spec.underline
        elif isinstance(base_font, tuple) and len(base_font) >= 2:
            config['family'] = base_font[0]
            config['size'] = base_font[1]
            if len(base_font) >= 3:
                # Parse weight/slant from tuple
                styles = base_font[2].split()
                for style in styles:
                    if style in ('bold', 'normal'):
                        config['weight'] = style
                    elif style in ('italic', 'roman'):
                        config['slant'] = style

    # Apply parsed modifiers (override base)
    if 'size' in parsed:
        config['size'] = parsed['size']
    if 'weight' in parsed:
        config['weight'] = parsed['weight']
    if 'slant' in parsed:
        config['slant'] = parsed['slant']
    if 'underline' in parsed:
        config['underline'] = parsed['underline']
    if 'overstrike' in parsed:
        config['overstrike'] = parsed['overstrike']

    # Ensure we have family and size - use body token as fallback
    if 'family' not in config or 'size' not in config:
        body_spec = Typography.get_token('body')
        if 'family' not in config:
            config['family'] = body_spec.font
        if 'size' not in config:
            config['size'] = body_spec.size

    # Build Tk font specification as tuple (family, size, modifiers_string)
    family = config['family']
    size = config['size']
    modifiers = []

    if config.get('weight') == 'bold':
        modifiers.append('bold')
    if config.get('slant') == 'italic':
        modifiers.append('italic')
    if config.get('underline'):
        modifiers.append('underline')
    if config.get('overstrike'):
        modifiers.append('overstrike')

    if modifiers:
        return (family, size, ' '.join(modifiers))
    else:
        return (family, size)


class FontMixin:
    """Mixin that adds font modifier syntax support to ttkbootstrap widgets.

    This mixin is automatically integrated into all ttkbootstrap widgets via TTKWrapperBase.
    It intercepts font configuration and processes modifier syntax before applying the font
    to the underlying ttk widget.

    The modifier syntax enables inline font customization without creating Font objects,
    using bracket notation similar to bootstyle modifiers: family[size][weight][style]

    Font Modifier Behavior:
        - At widget creation: Modifiers are applied to the widget's default style font
        - At runtime (via configure): Modifiers are applied to the widget's current font
        - Missing components: Inherited from widget's current font or 'body' token

    Supported Syntax:
        - Font families: 'helvetica', 'arial', etc.
        - Font tokens: 'body', 'label', 'heading-lg', etc.
        - Point sizes: '16' (positive integers)
        - Pixel sizes: '16px' (converted to negative for Tk)
        - Size tokens: 'xs', 'sm', 'md', 'lg', 'xl', 'xxl'
        - Weight: 'bold', 'normal'
        - Slant: 'italic', 'roman'
        - Decorations: 'underline', 'overstrike'

    Examples:
        # Widget creation with font modifiers
        Button(root, text="Click", font="helvetica[16][bold]")
        Label(root, text="Title", font="body[bold,underline]")
        Entry(root, font="[sm]")

        # Runtime font modification
        label.configure(font="[16]")  # Changes size only
        label.configure(font="[bold,italic]")  # Changes style only
        label.configure(font="heading-lg[italic]")  # Token with modifier

    Notes:
        - All components are optional and can be combined
        - Multiple style modifiers are comma-separated: [bold,italic,underline]
        - The mixin uses @configure_delegate to intercept font configuration
        - Always returns Tk-compatible font specifications
    """

    @configure_delegate("font")
    def _delegate_font(self, value: Any = None):
        """Process font modifier syntax or pass through standard font specifications.

        Args:
            value: Font spec (str with modifiers, tuple, Font, or None to query)

        Returns:
            Current font (query) or None (set)
        """
        # Query path - return current font
        if value is None:
            # Get current font directly from ttk widget
            return self._ttk_base.cget(self, 'font')  # type: ignore[misc]

        # Set path - process font modifier if string
        if isinstance(value, str):
            font_token_names = _get_font_token_names()
            if '[' in value or value in font_token_names:
                # Check if it's just a token name without modifiers
                if value in font_token_names and '[' not in value:
                    # Just use the token directly
                    font_value = value
                else:
                    # Get current font to use as base for modifications
                    try:
                        current_font = self._ttk_base.cget(self, 'font')  # type: ignore[misc]
                    except:
                        current_font = None

                    # Parse and build font from modifier syntax using current font as base
                    font_value = build_font_from_modifier(value, base_font=current_font)
            else:
                # Use as-is (simple font family string)
                font_value = value
        else:
            # Use as-is (tuple, Font object, etc.)
            font_value = value

        # Apply directly via base ttk widget (bypass delegation to avoid recursion)
        return self._ttk_base.configure(self, font=font_value)  # type: ignore[misc]