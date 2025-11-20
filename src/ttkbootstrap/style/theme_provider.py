from __future__ import annotations

import json
# import tomllib
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
    AppConfig.dark_theme or AppConfig.light_theme are also registered with
    'dark' and 'light' aliases for convenience.
    """
    from ttkbootstrap.appconfig import AppConfig
    from importlib import resources

    global _registered_themes

    base_package = 'ttkbootstrap.assets.themes'
    legacy_package = 'ttkbootstrap.assets.themes.legacy'

    # Get configured theme names for dark/light aliases
    dark_theme_name = AppConfig.get('dark_theme', 'bootstrap-dark')
    light_theme_name = AppConfig.get('light_theme', 'bootstrap-light')

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

    def __init__(self, name: str = "dark"):
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

    # ----- Theme metadata helpers -------------------------------------------------

    def list_themes(self) -> list[dict[str, str]]:
        """Return a list of available themes with names and display names.

        The result is a list of dictionaries in the form::

            {"name": "cosmo", "display_name": "Cosmo"}

        Aliases such as ``\"light\"`` and ``\"dark\"`` are not included; only the
        canonical theme entries loaded into the provider are returned.
        """
        from ttkbootstrap.appconfig import AppConfig

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
        select_themes = AppConfig.get("load_select_themes", None)
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
