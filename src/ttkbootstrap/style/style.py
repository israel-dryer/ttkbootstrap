"""Enhanced TTK Style class with builder registry and theme management."""

from __future__ import annotations

from tkinter.ttk import Style as ttkStyle
from typing import Dict, Set, Optional

from ttkbootstrap.style.bootstyle_builder import BootstyleBuilder
from ttkbootstrap.style.theme_provider import ThemeProvider


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

    # Class-level singleton tracking (one Style instance per master)
    _instances: Dict[int, Style] = {}

    def __init__(self, master=None, theme: str = "light"):
        """Initialize the Style instance.

        Args:
            master: Tkinter master widget (None for default)
            theme: Initial theme name (default: "light")
        """
        super().__init__(master)

        # Builder manager - stateless, calls registered builder functions
        self._builder_manager = BootstyleBuilder()

        # Theme provider - manages themes and colors
        self._theme_provider = ThemeProvider(theme)

        # Style registries
        self._style_registry: Set[str] = set()
        """All styles created across all themes"""

        self._theme_styles: Dict[str, Set[str]] = {}
        """Styles per theme: {theme_name: {style1, style2, ...}}"""

        self._style_options: Dict[str, dict] = {}
        """Custom options per style: {style_name: {option: value, ...}}"""

        # Current theme tracking
        self._current_theme: Optional[str] = theme

        # Apply base TTK theme
        super().theme_use('clam')

    @classmethod
    def get_instance(cls, master=None) -> Style:
        """Get or create Style instance (singleton per master).

        Args:
            master: Tkinter master widget (None for default)

        Returns:
            Style instance for this master
        """
        key = id(master) if master else 0
        if key not in cls._instances:
            cls._instances[key] = cls(master)
        return cls._instances[key]

    @property
    def builder_manager(self) -> BootstyleBuilder:
        """Get the builder manager instance.

        Returns:
            BootstyleBuilder instance
        """
        return self._builder_manager

    @property
    def theme_provider(self) -> ThemeProvider:
        """Get the theme provider instance.

        Returns:
            ThemeProvider instance
        """
        return self._theme_provider

    @property
    def current_theme(self) -> Optional[str]:
        """Get the current theme name.

        Returns:
            Current theme name or None
        """
        return self._current_theme

    @property
    def colors(self):
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

    def style_exists_in_theme(self, ttkstyle: str) -> bool:
        """Check if a style exists in the current theme registry.

        This is used for caching - if a style exists in the current theme,
        we don't need to rebuild it.

        Args:
            ttkstyle: Full TTK style name

        Returns:
            True if style is registered in current theme
        """
        if self._current_theme is None:
            return False

        theme_styles = self._theme_styles.get(self._current_theme)
        if theme_styles is None:
            return False

        return ttkstyle in theme_styles

    def register_style(self, ttkstyle: str, options: Optional[dict] = None):
        """Register a style in the current theme.

        This adds the style to registries so it can be:
        - Cached (not recreated if already exists)
        - Rebuilt when theme changes
        - Recreated with same options

        Args:
            ttkstyle: Full TTK style name
            options: Optional custom style options
        """
        # Add to global registry
        self._style_registry.add(ttkstyle)

        # Add to current theme's registry
        if self._current_theme not in self._theme_styles:
            self._theme_styles[self._current_theme] = set()
        self._theme_styles[self._current_theme].add(ttkstyle)

        # Store custom options if provided
        if options:
            self._style_options[ttkstyle] = options

    def create_style(self, ttkstyle: str, builder_name: str, options: Optional[dict] = None):
        """Create a new style if it doesn't exist in current theme.

        Args:
            ttkstyle: Full TTK style name (e.g., "success.TButton")
            builder_name: Builder function name (e.g., "button")
            options: Optional custom style options
        """
        # Check if already exists in this theme
        if self.style_exists_in_theme(ttkstyle):
            return  # Already created for this theme

        # Call builder by name
        self._builder_manager.call_builder(
            name=builder_name,
            ttk_style=ttkstyle,
            **(options or {})
        )

        # Register it
        self.register_style(ttkstyle, options)

    def theme_use(self, themename: str):
        """Switch to a different theme and rebuild all styles.

        Args:
            themename: Theme name to switch to
        """
        # Tell ThemeProvider to switch
        self._theme_provider.use(themename)
        self._current_theme = themename

        # Rebuild all existing styles with new theme
        self._rebuild_all_styles()

        # TODO: Publish theme change event
        # Publisher.publish_message(Channel.STD)

    def _rebuild_all_styles(self):
        """Recreate all registered styles when theme changes.

        This iterates through all styles that have been created and
        rebuilds them using the new theme's colors, preserving any
        custom options.
        """
        for ttkstyle in self._style_registry:
            # Get stored options if any
            options = self._style_options.get(ttkstyle, {})

            # Parse style name to get builder name
            builder_name = self._parse_builder_name(ttkstyle)

            # Skip if we can't determine builder
            if not builder_name:
                continue

            # Call builder (it will use current theme from provider)
            try:
                self._builder_manager.call_builder(
                    name=builder_name,
                    ttk_style=ttkstyle,
                    **options
                )

                # Re-register in new theme
                if self._current_theme not in self._theme_styles:
                    self._theme_styles[self._current_theme] = set()
                self._theme_styles[self._current_theme].add(ttkstyle)

            except Exception as e:
                # Builder doesn't exist or failed - log but continue
                print(f"Warning: Failed to rebuild style '{ttkstyle}': {e}")

    def _parse_builder_name(self, ttkstyle: str) -> Optional[str]:
        """Parse TTK style name to extract builder name.

        Args:
            ttkstyle: Full TTK style name

        Returns:
            Builder name (e.g., "button", "button_outline") or None

        Examples:
            >>> _parse_builder_name("success.TButton")
            "button"
            >>> _parse_builder_name("custom_abc.danger.Outline.TButton")
            "button_outline"
            >>> _parse_builder_name("striped.Horizontal.TProgressbar")
            "progressbar_striped"
        """
        # Color tokens to exclude
        COLORS = {'primary', 'secondary', 'success', 'info', 'warning',
                  'danger', 'light', 'dark'}

        # Orientation tokens
        ORIENTATIONS = {'horizontal', 'vertical'}

        # Split into parts
        parts = ttkstyle.split('.')

        # Remove custom prefix if present
        if parts and parts[0].startswith('custom_'):
            parts = parts[1:]

        if not parts:
            return None

        # Extract widget class (e.g., "TButton")
        widget_class = None
        for part in parts:
            if part.startswith('T'):
                widget_class = part
                break

        if not widget_class:
            return None

        # Extract base widget name (e.g., "TButton" → "button")
        widget_base = widget_class[1:].lower()

        # Extract type/variant tokens (e.g., "Outline", "Link", "striped")
        variants = []
        for part in parts:
            part_lower = part.lower()
            if (part_lower not in COLORS and
                part_lower not in ORIENTATIONS and
                not part.startswith('T')):
                variants.append(part_lower)

        # Build builder name
        if variants:
            variant_str = '_'.join(variants)
            return f"{widget_base}_{variant_str}"
        return widget_base

    def get_builder_manager(self) -> BootstyleBuilder:
        """Get the builder manager instance.

        Returns:
            BootstyleBuilder instance
        """
        return self._builder_manager

    def __repr__(self) -> str:
        """String representation of Style instance."""
        return f"<Style theme={self._current_theme} styles={len(self._style_registry)}>"