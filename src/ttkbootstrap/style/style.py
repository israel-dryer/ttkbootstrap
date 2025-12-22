"""Enhanced TTK Style class with builder registry and theme management."""

from __future__ import annotations

import weakref
from tkinter.ttk import Style as ttkStyle
from typing import Dict, Optional, Set

from ttkbootstrap.runtime.app import get_app_settings
from ttkbootstrap.style.bootstyle_builder_ttk import BootstyleBuilderTTk
from ttkbootstrap.style.theme_provider import ThemeProvider, use_theme
from ttkbootstrap.widgets.types import Master

_style_instance: Style | None = None


class Style(ttkStyle):
    """Enhanced TTK Style with builder registry and theme management.

    This class extends ttk.Style to provide:

    - Singleton pattern (one instance per Tkinter master)
    - Integration with BootstyleBuilder registry
    - Theme management via ThemeProvider
    - Automatic style rebuilding on theme changes
    - Custom style options support

    The Style class maintains registries to track:

    - All created styles (for theme change rebuilds)
    - Which styles exist in each theme (for caching)
    - Custom options per style (for recreating with same options)
    """

    def __new__(cls, *args, **kwargs):
        """Ensure Style() always returns the global singleton instance.

        If an instance already exists, return it. Otherwise, create it.
        """
        global _style_instance
        if _style_instance is None:
            _style_instance = super().__new__(cls)
        return _style_instance

    def __init__(self, master: Master = None, theme: str = "light"):
        """Initialize the Style instance.

        Args:
            master: Tkinter master widget (None for default)
            theme: Initial theme name (default: "light")
        """
        # Prevent reinitialization on subsequent Style() calls
        if getattr(self, "_initialized", False):
            # Optionally honor a theme argument after initialization
            try:
                if theme and theme != self._current_theme:
                    self.theme_use(theme)
            except Exception:
                pass
            return

        super().__init__(master)

        self._theme_provider = use_theme(theme)
        self._style_builder = BootstyleBuilderTTk(theme_provider=self._theme_provider, style_instance=None)
        self._style_builder.set_style_instance(self)

        # Style registries
        self._style_registry: Set[str] = set()
        self._style_colors: Dict[str, Optional[str]] = {}
        self._style_options: Dict[str, dict] = {}

        # Current theme tracking
        self._current_theme: Optional[str] = theme

        # Track legacy Tk widgets for theme-change restyling
        self._tk_widgets = weakref.WeakSet()

        self.theme_use(theme)
        self._initialized = True

    @property
    def style_builder(self) -> BootstyleBuilderTTk:
        """Get the builder manager instance.

        Returns:
            BootstyleBuilder instance
        """
        return self._style_builder

    @property
    def theme_provider(self) -> ThemeProvider:
        """Get the theme provider instance.

        Returns:
            ThemeProvider instance
        """
        return self._theme_provider

    # ----- Theme metadata helpers -------------------------------------------------

    def list_themes(self) -> list[dict[str, str]]:
        """Return available themes as [{'name', 'display_name'}, ...].

        This delegates to the underlying ThemeProvider. Themes are always
        loaded from both the v2 and legacy theme packages.

        Returns:
            List of theme dictionaries with 'name' and 'display_name' keys.
        """
        return self._theme_provider.list_themes()

    @property
    def current_theme(self) -> Optional[str]:
        """Get the current theme name.

        Returns:
            Current theme name or None
        """
        return self._current_theme

    @property
    def colors(self) -> dict[str, str]:
        """Get colors for the current theme.

        Returns:
            Colors dictionary from ThemeProvider
        """
        return self._theme_provider.colors

    def style_exists(self, style: str) -> bool:
        """Check if a style exists (basic check).

        Args:
            style: TTK style name

        Returns:
            True if style has any configuration
        """
        return bool(self.configure(style))

    def register_style(self, ttk_style: str, options: Optional[dict] = None):
        """Register a style in the current theme.

        This adds the style to registries so it can be:

        - Cached (not recreated if already exists)
        - Rebuilt when theme changes
        - Recreated with same options

        Args:
            ttk_style: Full TTK style name
            options: Optional custom style options
        """
        # Add to global registry
        self._style_registry.add(ttk_style)

        # Store custom options if provided
        if options:
            self._style_options[ttk_style] = options

    def create_style(
            self,
            widget_class: str,
            variant: str,
            ttk_style: str,
            color: Optional[str] = None,
            options: Optional[dict] = None) -> None:
        """Create a new style if it doesn't exist in current theme.

        Args:
            widget_class: TTK widget class (e.g., "TButton")
            variant: Variant name (e.g., "outline")
            ttk_style: Full TTK style name (e.g., "success.Outline.TButton")
            color: Optional color token (e.g., "success", "blue[100]")
            options: Optional custom style options
        """
        # Check if already exists in this theme
        if self.style_exists(ttk_style):
            return  # Already created for this theme

        # Call builder with widget class, variant, and parsed color
        self._style_builder.call_builder(
            widget_class=widget_class,
            variant=variant,
            ttk_style=ttk_style,
            color=color,
            **(options or {})
        )

        # Store the color so we can rebuild with the same color
        self._style_colors[ttk_style] = color

        # Register it
        self.register_style(ttk_style, options)

    def theme_use(self, name: str = None) -> str | None:
        """Switch to a different theme and rebuild all styles.

        Applies theme change to the global Style instance, rebuilds all
        TTK styles and registered Tk widgets, and publishes a legacy
        theme-change event for subscribers.

        Args:
            name: Theme name to switch to. If None, returns the current theme.

        Returns:
            The current theme name, or None if no theme is set.
        """
        if name is None:
            return super().theme_use()

        # Only call use() if theme is changing to avoid redundant build_theme_colors()
        if name != self._theme_provider.name:
            self._theme_provider.use(name)
        self._current_theme = name

        if name not in self.theme_names():
            self.theme_create(name, 'clam', {})

        super().theme_use(name)

        # Initialize all default widget styles before rebuilding custom styles
        # self._style_builder.initialize_all_default_styles()

        self._rebuild_all_styles()

        # Re-apply Tk widget styling (legacy widgets)
        self._rebuild_all_tk_widgets()

        # Publish theme-change event for legacy subscribers
        from ttkbootstrap.core.publisher import Channel, Publisher  # lazy import
        Publisher.publish_message(Channel.STD)

        return self._current_theme

    def _rebuild_all_styles(self):
        """Recreate all registered styles when theme changes.

        This iterates through all styles that have been created and
        rebuilds them using the new theme's colors, preserving any
        custom options.
        """
        for style in self._style_registry:
            # Get stored options and color
            options = self._style_options.get(style, {})
            color = self._style_colors.get(style)

            # Parse style name to get widget class and variant
            parsed = self._parse_style_name(style)
            if not parsed:
                continue

            widget_class = parsed['widget_class']
            variant = parsed['variant']

            self._style_builder.call_builder(
                widget_class=widget_class,
                variant=variant,
                ttk_style=style,
                color=color,  # Pass the stored color
                **options
            )

    def register_tk_widget(self, widget) -> None:
        """Register a Tk widget to be restyled on theme changes."""
        self._tk_widgets.add(widget)

    def _rebuild_all_tk_widgets(self) -> None:
        """Restyle all registered Tk widgets on theme change."""
        from ttkbootstrap.style.bootstyle_builder_tk import BootstyleBuilderBuilderTk
        builder_tk = BootstyleBuilderBuilderTk(theme_provider=self._theme_provider, style_instance=self)

        for widget in list(self._tk_widgets):
            try:
                surface = getattr(widget, '_surface_color', 'background')
                builder_tk.call_builder(widget, surface_color=surface)
            except Exception:
                # ignore incompatible or unmapped widgets
                pass

    @staticmethod
    def _parse_style_name(ttk_style: str) -> Optional[dict]:
        """Parse TTK style name to extract widget class and variant.

        Args:
            ttk_style: Full TTK style name

        Returns:
            Dict with 'widget_class' and 'variant', or None

        Examples:
            >>> Style._parse_style_name("success.TButton")
            {'widget_class': 'TButton', 'variant': 'solid'}
            >>> Style._parse_style_name("info.Striped.TProgressbar")
            {'widget_class': 'TProgressbar', 'variant': 'striped'}
        """
        # Split into parts
        parts = ttk_style.split('.')

        if not parts:
            return None

        # Extract widget class (e.g., "TButton")
        # Widget class is always the LAST part starting with 'T'
        widget_class = None
        for part in parts:
            if part.startswith('T'):
                widget_class = part

        if not widget_class:
            return None

        # Determine variant using registered builders for this widget
        from ttkbootstrap.style.bootstyle_builder_ttk import BootstyleBuilderTTk
        builder_variants = set(v.lower() for v in BootstyleBuilderTTk.get_registered_builders(widget_class))

        variant = None
        color = None
        for part in parts:
            # Skip the widget class itself (e.g., 'TCheckbutton')
            if part == widget_class:
                continue
            token = part.lower()
            # Identify variant by registry match
            if token in builder_variants and variant is None:
                variant = token
                continue
            # First non-variant token becomes color
            if color is None:
                color = part

        if variant is None:
            variant = BootstyleBuilderTTk.get_default_variant(widget_class)

        return {
            'widget_class': widget_class,
            'variant': variant
        }

    def get_style_builder(self) -> BootstyleBuilderTTk:
        """Get the style builder instance.

        Returns:
            BootstyleBuilder instance
        """
        return self._style_builder

    def __repr__(self) -> str:
        """String representation of Style instance."""
        return f"<Style theme={self._current_theme} styles={len(self._style_registry)}>"


def get_style(master: Master = None) -> Style:
    """Return the global Style singleton instance.

    Convenience helper function that ensures a single Style instance
    is used across the application.

    Args:
        master: Optional master for initial construction; ignored thereafter.

    Returns:
        Global Style instance.

    Examples:
        >>> style = get_style()
        >>> style.theme_use("darkly")
    """
    if _style_instance:
        return _style_instance
    else:
        return Style(master)


def get_style_builder() -> BootstyleBuilderTTk:
    """Return the style builder for the currently active theme.

    Returns:
        The BootstyleBuilderTTk instance for the active theme.

    Examples:
        >>> builder = get_style_builder()
        >>> primary_color = builder.color("primary")
    """
    style = get_style()
    return style.style_builder


# --- Global Utilities ---

def set_theme(name: str) -> None:
    """Set the active application theme.

    Args:
        name: Theme name to activate (e.g., "darkly", "cosmo", "superhero").

    Examples:
        >>> set_theme("darkly")
    """
    style = get_style()
    style.theme_use(name)


def toggle_theme() -> None:
    """Toggle the active application theme between light and dark mode.

    Uses the light and dark themes specified in app settings, or defaults
    to bootstrap-light and bootstrap-dark.

    Examples:
        >>> toggle_theme()
    """
    settings = get_app_settings()
    light = settings.light_theme
    dark = settings.dark_theme
    theme = get_theme()
    if theme == light or theme == "light":
        set_theme(dark)
    else:
        set_theme(light)


def get_theme() -> str:
    """Return the name of the currently active theme.

    Returns:
        Name of the active theme.

    Examples:
        >>> theme = get_theme()
        >>> print(theme)  # "darkly"
    """
    style = get_style()
    return style.theme_use()


def get_themes() -> list[dict[str, str]]:
    """Return the list of all registered themes.

    Returns:
        List of dictionaries containing ``name`` and ``display_name`` for each theme.

    Examples:
        >>> themes = get_themes()
        >>> print([theme["name"] for theme in themes])
    """
    style = get_style()
    return style.list_themes()


def get_theme_provider() -> ThemeProvider:
    """Get the theme provider instance for the active theme.

    Returns:
        ThemeProvider instance.

    Examples:
        >>> provider = get_theme_provider()
        >>> colors = provider.get_colors()
    """
    style = get_style()
    return style.theme_provider


def get_theme_color(token: str) -> str:
    """Get a hex color value from a color token based on the active theme.

    Args:
        token: Color token name (e.g., "primary", "background").

    Returns:
        Hex color string (e.g., "#007bff").

    Raises:
        ValueError: If the color token is invalid.

    Examples:
        >>> primary = get_theme_color("primary")
        >>> print(primary)  # "#007bff"
    """
    builder = get_style_builder()
    try:
        return builder.color(token)
    except Exception:
        raise ValueError(f"Invalid color token: {token}")
