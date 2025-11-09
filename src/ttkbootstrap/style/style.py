"""Enhanced TTK Style class with builder registry and theme management."""

from __future__ import annotations

import weakref
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

        # Theme provider - manages themes and colors
        self._theme_provider = ThemeProvider(theme)

        # Builder manager - stateless, calls registered builder functions
        # Pass theme_provider and set style instance to avoid circular import
        self._builder_manager = BootstyleBuilder(
            theme_provider=self._theme_provider,
            style_instance=None  # Set below after creation
        )
        self._builder_manager.set_style_instance(self)

        # Style registries
        self._style_registry: Set[str] = set()
        """All styles created across all themes"""

        self._theme_styles: Dict[str, Set[str]] = {}
        """Styles per theme: {theme_name: {style1, style2, ...}}"""

        self._style_options: Dict[str, dict] = {}
        """Custom options per style: {style_name: {option: value, ...}}"""

        self._style_colors: Dict[str, Optional[str]] = {}
        """Color per style: {style_name: color}"""

        # Current theme tracking
        self._current_theme: Optional[str] = theme

        # Track legacy Tk widgets for theme-change restyling
        self._tk_widgets = weakref.WeakSet()

        # Apply a base TTK theme - needed for TTK widgets to function
        # We use 'default' or 'clam' as the base, then layer our styles on top
        try:
            super().theme_use('default')
        except:
            try:
                super().theme_use('clam')
            except:
                pass  # No base theme available, continue anyway

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

    def create_style(self, widget_class: str, variant: str, ttkstyle: str,
                    color: Optional[str] = None, options: Optional[dict] = None):
        """Create a new style if it doesn't exist in current theme.

        Args:
            widget_class: TTK widget class (e.g., "TButton")
            variant: Variant name (e.g., "outline")
            ttkstyle: Full TTK style name (e.g., "success.Outline.TButton")
            color: Optional color token (e.g., "success", "#FF5733", "blue[100]")
            options: Optional custom style options
        """
        # Check if already exists in this theme
        if self.style_exists_in_theme(ttkstyle):
            return  # Already created for this theme

        # Call builder with widget class, variant, and parsed color
        self._builder_manager.call_builder(
            widget_class=widget_class,
            variant=variant,
            ttk_style=ttkstyle,
            color=color,
            **(options or {})
        )

        # Store the color so we can rebuild with the same color
        self._style_colors[ttkstyle] = color

        # Register it
        self.register_style(ttkstyle, options)

    def theme_use(self, themename: str = None):
        """Switch to a different theme and rebuild all styles.

        Args:
            themename: Theme name to switch to
        """
        if themename is None:
            return super().theme_use()
        # Tell ThemeProvider to switch
        self._theme_provider.use(themename)
        self._current_theme = themename

        # Rebuild all existing styles with new theme
        self._rebuild_all_styles()
        # Re-apply Tk widget styling (legacy widgets)
        self._rebuild_all_tk_widgets()

        # TODO: Publish theme change event
        # Publisher.publish_message(Channel.STD)

    def _rebuild_all_styles(self):
        """Recreate all registered styles when theme changes.

        This iterates through all styles that have been created and
        rebuilds them using the new theme's colors, preserving any
        custom options.
        """
        for ttkstyle in self._style_registry:
            # Get stored options and color
            options = self._style_options.get(ttkstyle, {})
            color = self._style_colors.get(ttkstyle)

            # Parse style name to get widget class and variant
            parsed = self._parse_style_name(ttkstyle)
            if not parsed:
                continue

            widget_class = parsed['widget_class']
            variant = parsed['variant']

            # Call builder (it will use current theme from provider)
            try:
                self._builder_manager.call_builder(
                    widget_class=widget_class,
                    variant=variant,
                    ttk_style=ttkstyle,
                    color=color,  # Pass the stored color
                    **options
                )

                # Re-register in new theme
                if self._current_theme not in self._theme_styles:
                    self._theme_styles[self._current_theme] = set()
                self._theme_styles[self._current_theme].add(ttkstyle)

            except Exception as e:
                # Builder doesn't exist or failed - log but continue
                print(f"Warning: Failed to rebuild style '{ttkstyle}': {e}")

    def register_tk_widget(self, widget) -> None:
        """Register a Tk widget to be restyled on theme changes."""
        try:
            self._tk_widgets.add(widget)
        except Exception:
            pass

    def _rebuild_all_tk_widgets(self) -> None:
        """Restyle all registered Tk widgets on theme change."""
        try:
            from ttkbootstrap.style.bootstyle_builder_tk import BootstyleBuilderTk
        except Exception:
            return

        builder_tk = BootstyleBuilderTk(style_instance=self)
        for widget in list(self._tk_widgets):
            try:
                surface = getattr(widget, '_surface_color', 'background')
                builder_tk.call_builder(widget, surface_color=surface)
            except Exception:
                # Skip widgets that may have been destroyed or incompatible
                continue

    def _parse_style_name(self, ttkstyle: str) -> Optional[dict]:
        """Parse TTK style name to extract widget class and variant.

        Args:
            ttkstyle: Full TTK style name

        Returns:
            Dict with 'widget_class' and 'variant', or None

        Examples:
            >>> _parse_style_name("success.TButton")
            {'widget_class': 'TButton', 'variant': 'solid'}
            >>> _parse_style_name("custom_abc.danger.Outline.TButton")
            {'widget_class': 'TButton', 'variant': 'outline'}
            >>> _parse_style_name("info.Striped.TProgressbar")
            {'widget_class': 'TProgressbar', 'variant': 'striped'}
        """
        # Split into parts
        parts = ttkstyle.split('.')

        # Remove custom prefix if present
        if parts and parts[0].startswith('custom_'):
            parts = parts[1:]

        # Remove surface prefix if present: Surface[...]
        if parts and parts[0].startswith('Surface['):
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

        # Determine variant using registered builders for this widget
        from ttkbootstrap.style.bootstyle_builder import BootstyleBuilder
        builder_variants = set(v.lower() for v in BootstyleBuilder.get_registered_builders(widget_class))

        variant = None
        color = None
        for part in parts:
            if part.startswith('T'):
                continue
            token = part.lower()
            # Skip surface/style prefixes (already removed) and custom
            if token.startswith('custom_'):
                continue
            # Identify variant by registry match
            if token in builder_variants and variant is None:
                variant = token
                continue
            # First non-variant token becomes color (accept anything)
            if color is None:
                color = part

        if variant is None:
            variant = BootstyleBuilder.get_default_variant(widget_class)

        return {
            'widget_class': widget_class,
            'variant': variant
        }

    def get_builder_manager(self) -> BootstyleBuilder:
        """Get the builder manager instance.

        Returns:
            BootstyleBuilder instance
        """
        return self._builder_manager

    def __repr__(self) -> str:
        """String representation of Style instance."""
        return f"<Style theme={self._current_theme} styles={len(self._style_registry)}>"
