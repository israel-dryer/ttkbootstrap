from __future__ import annotations

import json
# import tomllib
from importlib import resources

from ttkbootstrap.runtime.app import get_app_settings
from ttkbootstrap.core.exceptions import ThemeError
from ttkbootstrap.style.utility import shade_color, tint_color

_registered_themes = {}
_current_theme = None

# Weights for generating color spectrum tints (toward white) and shades (toward black)
# Each weight represents how much of the original color to retain when mixing
# Full 50-step increments from 50-450 (tints) and 550-950 (shades)
TINT_WEIGHTS = {
    50: 0.90,
    100: 0.80,
    150: 0.70,
    200: 0.60,
    250: 0.50,
    300: 0.40,
    350: 0.325,
    400: 0.25,
    450: 0.125,
}
SHADE_WEIGHTS = {
    550: 0.125,
    600: 0.25,
    650: 0.325,
    700: 0.40,
    750: 0.50,
    800: 0.60,
    850: 0.725,
    900: 0.85,
    950: 0.95,
}


def register_user_theme(name, path):
    data = load_user_defined_theme(path)
    _registered_themes[name] = data


def get_theme(name):
    """Return a registered theme by name.

    If the theme is not currently registered this will re-run
    ``load_system_themes`` once to pick up any newly added themes before
    failing.
    """
    if name in _registered_themes:
        return _registered_themes[name]

    # Lazy fallback: configuration (e.g., load_all_themes/include_legacy_themes)
    # may have changed after the provider singleton was first initialized.
    # Re-run the loader once to pick up any additional themes.
    try:
        load_system_themes()
        if name in _registered_themes:
            return _registered_themes[name]
    except Exception:
        # If anything goes wrong here, fall through to the ThemeError.
        pass

    # Build a helpful error message listing available themes
    available = sorted(
        {
            data.get("name")
            for data in _registered_themes.values()
            if isinstance(data, dict) and data.get("name")
        }
    )
    available_str = ", ".join(available) if available else "<none>"
    raise ThemeError(
        f"Theme '{name}' is not registered. "
        f"Registered themes: {available_str}"
    )


def load_system_themes():
    """Load system themes from the package.

    Loads all v2 themes from ``ttkbootstrap.assets.themes`` and all legacy
    themes from ``ttkbootstrap.assets.themes.legacy``. Themes matching
    app settings dark_theme or .light_theme are also registered with
    'dark' and 'light' aliases for convenience.
    """
    from importlib import resources

    global _registered_themes

    base_package = 'ttkbootstrap.assets.themes'
    legacy_package = 'ttkbootstrap.assets.themes.legacy'

    # Get configured theme names for dark/light aliases
    app_settings = get_app_settings()
    dark_theme_name = app_settings.dark_theme
    light_theme_name = app_settings.light_theme

    # Always load all v2 JSON themes from the primary themes package.
    try:
        base_dir = resources.files(base_package)
    except ModuleNotFoundError:
        base_dir = None
    if base_dir is not None:
        for theme_file in base_dir.iterdir():
            if not theme_file.name.endswith(".json"):
                continue
            data = load_package_theme(theme_file.name, base_package)
            name = data.get("name")
            if not name:
                continue
            _registered_themes[name] = data

            # Register aliases for dark/light themes
            if name == dark_theme_name:
                _registered_themes['dark'] = data
            elif name == light_theme_name:
                _registered_themes['light'] = data

    # Always supplement with legacy themes (if present)
    try:
        legacy_dir = resources.files(legacy_package)
    except ModuleNotFoundError:
        legacy_dir = None
    if legacy_dir is not None:
        for theme_file in legacy_dir.iterdir():
            if not theme_file.name.endswith(".json"):
                continue
            data = load_package_theme(theme_file.name, legacy_package)
            name = data.get("name")
            if not name:
                continue
            _registered_themes[name] = data


def load_user_defined_theme(path):
    with open(path, "rb") as f:
        None
        # return tomllib.load(f)


def load_package_theme(filename: str, package="ttkbootstrap.assets.themes"):
    with resources.files(package).joinpath(filename).open("r", encoding="utf-8") as f:
        return json.load(f)


def color_spectrum(token, value):
    """Generate a color spectrum with 50-step increments from 50-950.

    Creates tints (lighter) and shades (darker) of the base color:
    - 50-450: Tints toward white (50 is lightest)
    - 500: Base color
    - 550-950: Shades toward black (950 is darkest)

    Args:
        token: The color token name (e.g., 'gray', 'blue')
        value: The base hex color value

    Returns:
        Dict mapping spectrum names to hex colors
    """
    result = {}

    # Generate tints (50-450)
    for stop, weight in TINT_WEIGHTS.items():
        result[f'{token}[{stop}]'] = tint_color(value, weight)

    # Base color (500)
    result[f'{token}[500]'] = value

    # Generate shades (550-950)
    for stop, weight in SHADE_WEIGHTS.items():
        result[f'{token}[{stop}]'] = shade_color(value, weight)

    return result


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

    def __init__(self, name: str = "dark"):
        # Prevent reinitialization on subsequent ThemeProvider() calls
        if getattr(self, "_initialized", False):
            if name and name != self.name:
                self.use(name)
            return

        self._theme = {}
        self._colors = {}
        load_system_themes()

        from ttkbootstrap.style.typography import Typography
        Typography.initialize()

        self.use(name)
        self._initialized = True

    # ----- Theme metadata helpers -------------------------------------------------

    def list_themes(self) -> list[dict[str, str]]:
        """Return a list of available themes with names and display names.

        The result is a list of dictionaries in the form::

            {"name": "cosmo", "display_name": "Cosmo"}

        Aliases such as ``\"light\"`` and ``\"dark\"`` are not included; only the
        canonical theme entries loaded into the provider are returned.
        """
        themes: list[dict[str, str]] = []
        seen: set[str] = set()

        for key, data in _registered_themes.items():
            # Skip alias keys that point at an existing theme object
            name = data.get("name")
            if not name:
                continue
            if key != name and name in _registered_themes:
                # This is an alias like 'light' or 'dark'
                continue
            if name in seen:
                continue
            seen.add(name)
            themes.append(
                {
                    "name": name,
                    "display_name": data.get("display_name", name),
                }
            )

        # If the application has declared a specific set/order of themes
        # to expose, filter and order by that list.
        select_themes = get_app_settings().available_themes
        if select_themes:
            by_name = {t["name"]: t for t in themes}
            ordered: list[dict[str, str]] = []
            for name in select_themes:
                t = by_name.get(name)
                if t is not None:
                    ordered.append(t)
            return ordered

        # Otherwise, sort for stable UI ordering (by display name, then name)
        themes.sort(key=lambda t: (t["display_name"].lower(), t["name"].lower()))
        return themes

    def use(self, name):
        self._theme = get_theme(name)
        self.build_theme_colors()

    @property
    def raw(self):
        """Return the raw source dictionary"""
        return self._theme

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

        # semantic tokens
        neutral_tokens = {
            "foreground",
            "muted",
            "muted_alt",
            "subtle",
            "border",
            "border_subtle",
        }
        for token, value in self._semantic.items():
            # Neutral roles are derived elsewhere from the top-level
            # foreground/background and should not be overridden here.
            if token in neutral_tokens:
                continue
            colors[token] = colors[value]

        # Surface tokens - semantic ramps for container backgrounds
        self._build_surface_tokens(colors)

        self._colors.clear()
        self._colors.update(**colors)

    def _build_surface_tokens(self, colors: dict):
        """Build semantic surface tokens for container backgrounds.

        Surface tokens provide deterministic, theme-defined backgrounds
        that don't rely on "background +1 math" for elevation.

        Token families:
        - content: Main content areas (pages, cards, panels)
        - chrome: UI chrome (sidebars, toolbars, navigation)
        - overlay: Floating elements (menus, dialogs, tooltips)
        - titlebar: Window title bars
        """
        is_dark = self.mode == 'dark'

        if is_dark:
            colors['content[0]'] = colors['background']
            colors['content[1]'] = colors['gray[850]']
            colors['content[2]'] = colors['gray[800]']

            colors['chrome[0]'] = colors['gray[900]']
            colors['chrome[1]'] = colors['gray[850]']

            colors['titlebar[0]'] = colors['gray[900]']

            colors['overlay[0]'] = colors['gray[800]']
            colors['overlay[1]'] = colors['gray[750]']
            colors['overlay[2]'] = colors['gray[700]']
            colors['overlay[3]'] = colors['gray[650]']
        else:
            colors['content[0]'] = colors['background']
            colors['content[1]'] = colors['gray[50]']
            colors['content[2]'] = colors['gray[150]']

            colors['chrome[0]'] = colors['gray[50]']
            colors['chrome[1]'] = colors['gray[100]']

            colors['titlebar[0]'] = colors['gray[50]']

            colors['overlay[0]'] = colors['white']
            colors['overlay[1]'] = colors['gray[50]']
            colors['overlay[2]'] = colors['gray[50]']
            colors['overlay[3]'] = colors['gray[100]']

        colors['content'] = colors['content[0]']
        colors['chrome'] = colors['chrome[0]']
        colors['overlay'] = colors['overlay[0]']
        colors['titlebar'] = colors['titlebar[0]']

        # Stroke tokens - semantic border colors derived from surface
        self._build_stroke_tokens(colors)

    def _build_stroke_tokens(self, colors: dict):
        """Build semantic stroke tokens for borders.

        Stroke tokens provide consistent border colors derived from the
        background/foreground relationship. They are surface-aware and
        produce perceptibly different strengths.

        Token family:
        - stroke[1]: Subtle border (high background retention)
        - stroke[2]: Default border (medium contrast)
        - stroke[3]: Strong border (higher contrast)
        - stroke: Alias for stroke[2]
        """
        from ttkbootstrap.style.utility import mix_colors

        bg = colors['background']
        fg = colors['foreground']

        # Mix background toward foreground at different strengths
        # Higher values = more background retained = subtler stroke
        if self.mode == 'dark':
            colors['stroke[1]'] = mix_colors(bg, fg, 0.88)  # subtle
            colors['stroke[2]'] = mix_colors(bg, fg, 0.78)  # default
            colors['stroke[3]'] = mix_colors(bg, fg, 0.65)  # strong
        else:
            colors['stroke[1]'] = mix_colors(bg, fg, 0.90)  # subtle
            colors['stroke[2]'] = mix_colors(bg, fg, 0.82)  # default
            colors['stroke[3]'] = mix_colors(bg, fg, 0.70)  # strong

        # Alias: stroke -> stroke[2]
        colors['stroke'] = colors['stroke[2]']

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


def use_theme(name: str = None) -> ThemeProvider:
    """Return the global ThemeProvider singleton instance.

    Convenience helper that mirrors `use_style()` so callers can obtain
    the current ThemeProvider without handling singleton state.

    Args:
        name: Optional theme name to switch to, or None to return current instance.

    Returns:
        Global ThemeProvider instance.
    """
    # If instance doesn't exist yet, create it with default theme
    if ThemeProvider._instance is None:
        return ThemeProvider(name or "dark")

    # If name is provided and different, switch themes
    if name is not None and name != ThemeProvider._instance.name:
        ThemeProvider._instance.use(name)

    # Return the singleton
    return ThemeProvider._instance
