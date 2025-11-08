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

# Widgets whose color token represents their surface (background)
FRAME_SURFACE_CLASSES = {'TFrame', 'TLabelframe'}


# =============================================================================
# V2 Parsing (New System)
# =============================================================================

def parse_bootstyle_v2(bootstyle: str, widget_class: str) -> dict:
    """Parse bootstyle string using V2 syntax (dash-separated).

    The V2 syntax is: `color-variant-widget` where all parts are optional.

    In V2, we check against the actual theme colors from ThemeProvider and
    registered variants from the builder registry. Unknown parts are treated
    as **custom colors** rather than variants.

    Args:
        bootstyle: Bootstyle string (e.g., "success-outline", "primary")
        widget_class: TTK widget class name (e.g., "TButton")

    Returns:
        Dict with parsed components:
            - color: Color token (standard or custom) or None
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

        >>> parse_bootstyle_v2("#FF5733-outline", "TButton")
        {'color': '#FF5733', 'variant': 'outline', 'widget_class': 'TButton', 'cross_widget': False}
    """
    if not bootstyle:
        return {
            'color': None,
            'variant': "default",
            'widget_class': widget_class,
            'cross_widget': False
        }

    # Import here to avoid circular import
    from ttkbootstrap.style.bootstyle_builder import BootstyleBuilder
    from ttkbootstrap.style.theme_provider import ThemeProvider

    # Get actual theme colors from the theme provider
    theme_colors = ThemeProvider.instance().colors

    # Split on dashes
    parts = bootstyle.lower().split('-')

    color = None
    variant = None
    resolved_widget = widget_class
    cross_widget = False

    # Process each part
    for part in parts:
        # Check if it's a theme color token (from actual theme)
        if part in theme_colors:
            color = part
        # Check if it's a widget name
        elif part in WIDGET_CLASS_MAP:
            resolved_widget = WIDGET_CLASS_MAP[part]
            if resolved_widget != widget_class:
                cross_widget = True
        # Check if it's a registered variant for the current widget
        elif BootstyleBuilder.has_builder(resolved_widget, part):
            variant = part
        # Check if it looks like a color (contains '[' for spectrum, '#' for hex, or standard color)
        elif '[' in part or '#' in part or part in COLORS:
            color = part
        # Otherwise treat as custom color (any remaining unknown part)
        else:
            color = part

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
        custom_prefix: Optional[str] = None,
        surface_color: Optional[str] = None) -> str:
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

    # Add surface prefix if provided and not default
    if surface_color and surface_color != 'background':
        parts.append(f"Surface[{surface_color}]")

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
        This class also wires ttkbootstrap into tkinter/ttk by overriding
        widget constructors and configure methods so users can pass
        `bootstyle=...` at construction time or via `configure(...)`.
    """

    @staticmethod
    def create_ttk_style(
            widget_class: str,
            bootstyle: Optional[str] = None,
            style_options: Optional[dict] = None,
            surface_color: Optional[str] = None) -> str:
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

        # If no explicit surface provided and this is a frame-like widget,
        # use the color token as the surface to simulate transparency.
        if (surface_color is None or surface_color == 'background') and \
                resolved_widget in FRAME_SURFACE_CLASSES and color:
            surface_color = color

        # Generate TTK style name (variant is None if not specified)
        ttk_style = generate_ttk_style_name(
            color=color,
            variant=variant,  # None if not specified -> simpler style name
            widget_class=resolved_widget,
            custom_prefix=custom_prefix,
            surface_color=surface_color
        )

        # Trigger style creation through Style.get_instance()
        from ttkbootstrap.style.style import Style
        style = Style.get_instance()

        # Ensure options persist surface color for rebuilds
        options = dict(style_options or {})
        if surface_color and surface_color != 'background':
            options['surface_color'] = surface_color

        # Create the style with parsed color
        style.create_style(
            widget_class=resolved_widget,
            variant=builder_variant,  # Use default if not specified
            ttkstyle=ttk_style,
            color=color,  # Pass parsed color directly
            options=options
        )

        return ttk_style

    # ---------------------------------------------------------------------
    # Widget Overrides and API Setup
    # ---------------------------------------------------------------------

    @staticmethod
    def override_ttk_widget_constructor(func):
        """Override ttk widget `__init__` to accept `bootstyle`.

        This wrapper:
        - Pops `bootstyle`, `bs_style`, and optional `style_options`
        - Calls original constructor
        - Parses and creates the target ttk style via the builder system
        - Applies the created style to the widget
        - If no bootstyle provided, attempts applying the default variant if
          a builder is registered for the widget class
        """

        def __init__wrapper(self, *args, **kwargs):
            # Respect an explicit ttk 'style' passed by user
            had_style_kwarg = 'style' in kwargs

            bootstyle = kwargs.pop("bootstyle", "")
            bs_style = kwargs.pop("bs_style", "")
            style_options = kwargs.pop("style_options", None)
            # Pop surface inheritance args BEFORE calling real __init__
            inherit_flag_arg = kwargs.pop('inherit_surface_color', None)
            explicit_surface_arg = kwargs.pop('surface_color', None)

            # Instantiate the widget first
            func(self, *args, **kwargs)

            # Resolve widget class after construction
            try:
                widget_class = self.winfo_class()
            except Exception:
                widget_class = None

            try:
                # Prefer explicit bootstyle; fall back to bs_style if present
                style_str = bootstyle or bs_style

                # Compute effective surface color and cache on widget
                if hasattr(self, 'master') and self.master is not None:
                    parent_surface = getattr(self.master, '_surface_color', 'background')
                else:
                    parent_surface = 'background'

                # Determine inheritance flag from arg or AppConfig
                inherit_flag = inherit_flag_arg
                if inherit_flag is None:
                    inherit_flag = AppConfig.get('inherit_surface_color', True)

                explicit_surface = explicit_surface_arg
                if explicit_surface:
                    effective_surface = explicit_surface
                elif inherit_flag:
                    effective_surface = parent_surface
                else:
                    effective_surface = 'background'

                # For frames, if a color token is provided via bootstyle and
                # no explicit surface was given, treat the color as surface.
                if style_str and widget_class in FRAME_SURFACE_CLASSES and explicit_surface is None:
                    try:
                        parsed = parse_bootstyle(style_str, widget_class)
                        if parsed.get('color'):
                            effective_surface = parsed['color']
                    except Exception:
                        pass

                try:
                    setattr(self, '_surface_color', effective_surface)
                except Exception:
                    pass
                if style_str and widget_class:
                    ttkstyle = Bootstyle.create_ttk_style(
                        widget_class=widget_class,
                        bootstyle=style_str,
                        style_options=style_options,
                        surface_color=effective_surface,
                    )
                    # Apply style to the widget
                    try:
                        self.configure(style=ttkstyle)
                    except Exception:
                        pass
                elif widget_class and not had_style_kwarg:
                    # No bootstyle - apply default variant if builder exists
                    from ttkbootstrap.style.bootstyle_builder import BootstyleBuilder
                    from ttkbootstrap.style.style import Style as NewStyle
                    default_variant = BootstyleBuilder.get_default_variant(widget_class)
                    if BootstyleBuilder.has_builder(widget_class, default_variant):
                        ttkstyle = generate_ttk_style_name(
                            color=None,
                            variant=default_variant,
                            widget_class=widget_class,
                            surface_color=effective_surface,
                        )

                        style_instance = NewStyle.get_instance()
                        if style_instance is not None:
                            style_instance.create_style(
                                widget_class=widget_class,
                                variant=default_variant,
                                ttkstyle=ttkstyle,
                                options={**(style_options or {}), **({'surface_color': effective_surface} if effective_surface and effective_surface != 'background' else {})},
                            )
                            try:
                                self.configure(style=ttkstyle)
                            except Exception:
                                pass
                    else:
                        # No registered builder: at least attach base class style
                        try:
                            self.configure(style=widget_class)
                        except Exception:
                            pass
            except Exception:
                # Leave unstyled on any unexpected error to avoid crashing
                pass

        return __init__wrapper

    @staticmethod
    def override_ttk_widget_configure(func):
        """Override ttk widget `configure` to accept `bootstyle` updates.

        Allows reading `configure('bootstyle')` and setting
        `configure(bootstyle='...')` which is translated into a concrete
        ttk style via the builder system.
        """

        def configure(self, cnf=None, **kwargs):
            # Read-style queries
            if cnf in ("bootstyle", "style"):
                try:
                    return self.cget("style")
                except Exception:
                    return ""

            # Pass-through for other direct queries
            if cnf is not None:
                return func(self, cnf)

            # Handle set operations
            style_options = kwargs.pop("style_options", None)
            inherit_flag = kwargs.pop('inherit_surface_color', None)
            explicit_surface = kwargs.pop('surface_color', None)

            # Support both `bootstyle` and legacy `bs_style`
            style_str = None
            if "bootstyle" in kwargs and kwargs["bootstyle"]:
                style_str = kwargs.pop("bootstyle")
            elif "bs_style" in kwargs and kwargs["bs_style"]:
                style_str = kwargs.pop("bs_style")

            if style_str:
                try:
                    widget_class = self.winfo_class()
                    # Compute effective surface color
                    if explicit_surface is not None:
                        surface = explicit_surface
                    else:
                        if inherit_flag is None:
                            inherit_flag = AppConfig.get('inherit_surface_color', True)
                        if inherit_flag:
                            # inherit from parent
                            surface = 'background'
                            try:
                                if hasattr(self, 'master') and self.master is not None:
                                    surface = getattr(self.master, '_surface_color', 'background')
                            except Exception:
                                pass
                        else:
                            # use cached or background
                            surface = getattr(self, '_surface_color', 'background')

                    # For frames, if no explicit surface was given and the
                    # bootstyle provides a color token, treat it as surface.
                    if widget_class in FRAME_SURFACE_CLASSES and explicit_surface is None:
                        try:
                            parsed = parse_bootstyle(style_str, widget_class)
                            if parsed.get('color'):
                                surface = parsed['color']
                        except Exception:
                            pass

                    # Cache updated surface on widget
                    try:
                        setattr(self, '_surface_color', surface)
                    except Exception:
                        pass
                    ttkstyle = Bootstyle.create_ttk_style(
                        widget_class=widget_class,
                        bootstyle=style_str,
                        style_options=style_options,
                        surface_color=surface,
                    )
                    kwargs["style"] = ttkstyle
                except Exception:
                    # If anything goes wrong, fall through and let ttk handle
                    pass

            # Delegate to original configure
            return func(self, cnf, **kwargs)

        return configure

    @staticmethod
    def override_tk_widget_constructor(func):
        """Minimal override for legacy Tk widgets.

        Applies a basic background from the current theme when `autostyle`
        is True (default). This keeps legacy widgets visually consistent
        without pulling in the full legacy TK styling machinery.
        """

        def __init__wrapper(self, *args, **kwargs):
            autostyle = kwargs.pop("autostyle", True)

            # Handle surface inheritance for Tk widgets as well
            inherit_flag = kwargs.pop('inherit_surface_color', None)
            if inherit_flag is None:
                inherit_flag = AppConfig.get('inherit_surface_color', True)
            explicit_surface = kwargs.pop('surface_color', None)

            # Instantiate widget
            func(self, *args, **kwargs)

            # Compute and cache surface color
            try:
                if hasattr(self, 'master') and self.master is not None:
                    parent_surface = getattr(self.master, '_surface_color', 'background')
                else:
                    parent_surface = 'background'

                if explicit_surface:
                    effective_surface = explicit_surface
                elif inherit_flag:
                    effective_surface = parent_surface
                else:
                    effective_surface = 'background'

                setattr(self, '_surface_color', effective_surface)
            except Exception:
                pass

            if autostyle:
                try:
                    from ttkbootstrap.style.style import Style as NewStyle
                    bg = NewStyle.get_instance().colors.bg
                    try:
                        self.configure(background=bg)
                    except Exception:
                        pass
                except Exception:
                    # If Style not initialized yet or any error occurs, skip
                    pass

        return __init__wrapper

    @staticmethod
    def setup_ttkbootstrap_api():
        """Install ttkbootstrap bootstyle API into ttk/tk widgets.

        - Wrap TTK widget constructors to accept `bootstyle`
        - Wrap TTK widget `configure` to translate `bootstyle` updates
        - Add `__getitem__`/`__setitem__` handling for 'style'/'bootstyle'
        - Apply minimal theming to legacy Tk widgets on construction
        """
        try:
            from ttkbootstrap.widgets import TTK_WIDGETS, TK_WIDGETS
        except Exception:
            # Widgets module may not be available in some contexts
            return

        # Patch TTK widgets
        for widget in TTK_WIDGETS:
            try:
                # Override constructor
                _init = Bootstyle.override_ttk_widget_constructor(widget.__init__)
                widget.__init__ = _init

                # Override configure
                _configure = Bootstyle.override_ttk_widget_configure(widget.configure)
                widget.configure = _configure
                widget.config = widget.configure

                # Override item access for style/bootstyle keys (skip OptionMenu)
                if getattr(widget, "__name__", "") != "OptionMenu":
                    _orig_getitem = getattr(widget, "__getitem__", None)
                    _orig_setitem = getattr(widget, "__setitem__", None)

                    if _orig_getitem and _orig_setitem:
                        def __setitem(self, key, val):
                            if key in ("bootstyle", "style"):
                                return _configure(self, **{key: val})
                            return _orig_setitem(self, key, val)

                        def __getitem(self, key):
                            if key in ("bootstyle", "style"):
                                return _configure(self, cnf=key)
                            return _orig_getitem(self, key)

                        widget.__setitem__ = __setitem
                        widget.__getitem__ = __getitem
            except Exception:
                # Be forgiving; some ttk widgets may not exist in older Pythons
                continue

        # Patch legacy Tk widgets
        for widget in TK_WIDGETS:
            try:
                _init = Bootstyle.override_tk_widget_constructor(widget.__init__)
                widget.__init__ = _init
            except Exception:
                continue


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
