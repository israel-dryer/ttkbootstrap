from __future__ import annotations

import json
import tomllib
from importlib import resources

from ttkbootstrap.exceptions import ThemeError
from ttkbootstrap.style.utility import shade_color, tint_color

_registered_themes = {}
_current_theme = None

TINT_WEIGHTS = (0.80, 0.60, 0.40, 0.25)
SHADE_WEIGHTS = (0.25, 0.4, 0.6, 0.85)


def register_user_theme(name, path):
    data = load_user_defined_theme(path)
    _registered_themes[name] = data


def get_theme(name):
    if name in _registered_themes:
        return _registered_themes[name]
    else:
        raise ThemeError(f"Theme '{name}' is not registered")


def load_system_themes():
    """Load system themes from the package.

    Loads either all themes or just dark/light based on AppConfig setting.
    By default, only loads dark.json and light.json unless AppConfig.load_all_themes is True.

    Themes matching AppConfig.dark_theme or AppConfig.light_theme are also registered
    with 'dark' and 'light' aliases for convenience.
    """
    from ttkbootstrap.appconfig import AppConfig
    from importlib import resources

    global _registered_themes

    load_all = AppConfig.get('load_all_themes', False)
    package = 'ttkbootstrap.assets.themes'

    # Get configured theme names for dark/light aliases
    dark_theme_name = AppConfig.get('dark_theme', 'bootstrap-dark')
    light_theme_name = AppConfig.get('light_theme', 'bootstrap-light')

    if load_all:
        # Discover and load all .json theme files in the package
        theme_files = resources.files(package)
        for theme_file in theme_files.iterdir():
            if theme_file.name.endswith('.json'):
                data = load_package_theme(theme_file.name, package)
                name = data["name"]
                _registered_themes[name] = data

                # Register aliases for dark/light themes
                if name == dark_theme_name:
                    _registered_themes['dark'] = data
                elif name == light_theme_name:
                    _registered_themes['light'] = data
    else:
        # Only load the themes designated as dark and light in AppConfig
        # Map filenames to the theme names they should match
        theme_files = {
            'dark.json': ('dark', dark_theme_name),
            'light.json': ('light', light_theme_name)
        }

        for filename, (alias, expected_name) in theme_files.items():
            data = load_package_theme(filename, package)
            name = data["name"]

            # Register under the actual theme name
            _registered_themes[name] = data

            # Register alias only if theme name matches AppConfig
            if name == expected_name:
                _registered_themes[alias] = data


def load_user_defined_theme(path):
    with open(path, "rb") as f:
        return tomllib.load(f)


def load_package_theme(filename: str, package="ttkbootstrap.assets.themes"):
    with resources.files(package).joinpath(filename).open("r", encoding="utf-8") as f:
        return json.load(f)


def color_spectrum(token, value):
    spectrum_names = [f'{token}[{x}]' for x in [100, 200, 300, 400, 500, 600, 700, 800, 900]]
    tints = [tint_color(value, w) for w in TINT_WEIGHTS]
    shades = [shade_color(value, w) for w in SHADE_WEIGHTS]
    spectrum_colors = [*tints, value, *shades]
    return {name: color for name, color in zip(spectrum_names, spectrum_colors)}


class ThemeProvider:
    """Theme data provider with singleton access and helpers.

    Mirrors the pattern used by Style/use_style():
    - `ThemeProvider()` returns the global instance (singleton)
    - `use_theme(name)` returns/initializes the singleton with optional theme
    - `ThemeProvider.instance(name)` remains for backward compatibility
    """

    # Class-level global singleton instance
    _instance: ThemeProvider | None = None

    def __new__(cls, *args, **kwargs):
        """Ensure ThemeProvider() always returns the global singleton instance."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, name: str = "light"):
        # Prevent reinitialization on subsequent ThemeProvider() calls
        if getattr(self, "_initialized", False):
            if name and name != self.name:
                self.use(name)
            return

        self._theme = {}
        self._colors = {}
        load_system_themes()

        # Initialize typography from AppConfig if font is configured
        from ttkbootstrap.style.typography import Typography
        Typography.initialize_from_appconfig()

        self.use(name)
        self._initialized = True

    def use(self, name):
        self._theme = get_theme(name)
        self.build_theme_colors()
        self.update_theme_styles()

    @property
    def raw(self):
        """Return the raw source dictionary"""
        return self._theme

    @staticmethod
    def update_theme_styles():
        """Trigger a style update for the active theme"""
        from tkinter.ttk import Style
        Style().theme_use('clam')

    def build_theme_colors(self):
        colors = {}
        colors.update(
            foreground=self.raw.get('foreground'),
            background=self.raw.get('background'),
            white=self.raw.get('white'),
            black=self.raw.get('black'),
            **self._shades,
        )
        # add shaded spectrum
        for color, value in self._shades.items():
            colors.update(**color_spectrum(color, value))

        # sematic tokens
        for token, value in self._semantic.items():
            colors[token] = colors[value]

        self._colors.clear()
        self._colors.update(**colors)

    @property
    def name(self):
        """The name of the theme"""
        return self.raw.get('name')

    @property
    def display_name(self):
        """The display name of the theme"""
        return self.raw.get('display_name')

    @property
    def mode(self):
        """Returns the color mode 'light' or 'dark'"""
        return self.raw.get('mode')

    @property
    def colors(self):
        return self._colors

    @property
    def typography(self):
        """Returns the current typography configuration as FontTokens"""
        from ttkbootstrap.style.typography import Typography
        return Typography.all()

    @property
    def _shades(self):
        return self.raw.get('shades')

    @property
    def _semantic(self):
        return self.raw.get('semantic')

    def __repr__(self):
        """Return a string representation of the current theme"""
        return f"<Theme name={self.name} mode={self.mode}>"


def use_theme(name: str = "light") -> ThemeProvider:
    """Return the global ThemeProvider singleton instance.

    Convenience helper that mirrors `use_style()` so callers can obtain
    the current ThemeProvider without handling singleton state.

    Args:
        name: Optional initial theme name for first-time initialization.

    Returns:
        Global ThemeProvider instance.
    """
    # Lazily construct via direct call; __new__/__init__ enforce singleton
    return ThemeProvider(name)
