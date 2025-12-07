"""Global Application Configuration.

This module provides a global static configuration class for ttkbootstrap
applications. AppConfig allows you to set default preferences that will be
applied to widgets and windows throughout your application.

Examples:
    >>> from ttkbootstrap import AppConfig
    >>>
    >>> AppConfig.set(
    ...     theme="dark",
    ...     font=("Segoe UI", 10),
    ...     window_size=(800, 600),
    ...     window_scaling=1.5
    ... )
    >>>
    >>> # Get a specific config value
    >>> theme = AppConfig.get("theme")
    >>>
    >>> # Get all config as dict
    >>> all_config = AppConfig.get_all()
    >>>
    >>> # Reset to defaults
    >>> AppConfig.reset()
"""

from typing import Any, Dict, Optional, Tuple, Type, List
from typing_extensions import TypedDict, Unpack


class AppConfigOptions(TypedDict, total=False):
    app_name: str
    app_author: str
    theme: str
    dark_theme: str
    light_theme: str
    load_select_themes: List[str]
    font: Tuple[str, int]
    legacy_bootstyle: bool
    inherit_surface_color: bool
    window_size: Tuple[int, int]
    window_position: Tuple[int, int]
    window_minsize: Tuple[int, int]
    window_maxsize: Tuple[int, int]
    window_resizable: Tuple[bool, bool]
    window_scaling: float
    window_hdpi: bool
    window_alpha: float
    icon_provider: Type[Any]
    language: str
    date_format: str
    time_format: str
    number_decimal: str
    number_thousands: str

    # Undocumented, used internally by reset()
    colors: Dict[str, Any]


class AppConfig:
    """Global static configuration class for ttkbootstrap applications.

    This class provides a centralized way to manage application-wide settings
    such as default theme, fonts, window properties, and localization options.
    All methods are class methods, so no instantiation is required.

    Configuration changes only affect widgets and windows created after the
    change. Existing widgets will not be updated automatically.

    Configuration Keys:
        The following keys can be used with set(), get(), has(), and reset():

        Application Info:
            app_name (str): Application name for titles, dialogs, and file paths.
            app_author (str): Application author/organization name.

        Theme & Styling:
            light_theme (str): The default light theme; bound to "light" theme name.
            dark_theme (str): The default dark theme; bound to "dark" theme name.
            theme (str): Default theme name (e.g., "darkly", "cosmo", "flatly").
            load_select_themes (List[str]): Optional list of theme names that
                should be exposed in application UI helpers (e.g., theme pickers).
                When set, helpers like ``Style.list_themes()`` will filter and
                order themes using this list. All themes remain registered and
                can still be used programmatically.
            font (Tuple[str, int]): Default application font as (family, size).
            legacy_bootstyle (bool): Use legacy bootstyle parsing behavior.
                When True, uses relaxed parsing for backward compatibility.
                When False (default), uses strict parsing. Default is False.

        Window Defaults:
            window_size (Tuple[int, int]): Default window size as (width, height).
            window_position (Tuple[int, int]): Default window position as (x, y).
            window_minsize (Tuple[int, int]): Minimum window size as (width, height).
            window_maxsize (Tuple[int, int]): Maximum window size as (width, height).
            window_resizable (Tuple[bool, bool]): Window resizable as (width, height).
            window_scaling (float): Window scaling factor for high-DPI displays.
            window_hdpi (bool): Enable high-DPI support.
            window_alpha (float): Window transparency (0.0 to 1.0).

        Icons & Assets:
            icon_provider (type): Icon provider class (e.g., BootstrapIcon).

        Localization:
            language (str): Default language code (e.g., "en", "es", "fr").
            date_format (str): Date format string (e.g., "%Y-%m-%d", "%m/%d/%Y").
            time_format (str): Time format string (e.g., "%H:%M:%S", "%I:%M %p").
            number_decimal (str): Decimal separator character (e.g., ".", ",").
            number_thousands (str): Thousands separator character (e.g., ",", ".", " ").
    """

    # Application Info
    _app_name: Optional[str] = None
    _app_author: Optional[str] = None

    # Theme & Styling defaults
    _light_theme: Optional[str] = "bootstrap-light"
    _dark_theme: Optional[str] = "bootstrap-dark"
    _theme: Optional[str] = None
    _load_select_themes: Optional[List[str]] = None
    _font: Optional[Tuple[str, int]] = None
    _legacy_bootstyle: Optional[bool] = None
    _inherit_surface_color: Optional[bool] = True

    # Window defaults
    _window_size: Optional[Tuple[int, int]] = None
    _window_position: Optional[Tuple[int, int]] = None
    _window_minsize: Optional[Tuple[int, int]] = None
    _window_maxsize: Optional[Tuple[int, int]] = None
    _window_resizable: Optional[Tuple[bool, bool]] = None
    _window_scaling: Optional[float] = None
    _window_hdpi: Optional[bool] = None
    _window_alpha: Optional[float] = None

    # Icons & Assets
    _icon_provider: Optional[Type[Any]] = None

    # Localization
    _language: Optional[str] = None
    _date_format: Optional[str] = None
    _time_format: Optional[str] = None
    _number_decimal: Optional[str] = None
    _number_thousands: Optional[str] = None

    @classmethod
    def set(cls, **kwargs: Unpack[AppConfigOptions]) -> None:
        """Set one or more configuration values.

        Configuration changes only affect widgets and windows created after
        this call. Existing widgets will not be updated.

        Args:
            **kwargs: Configuration key-value pairs. Valid keys include:
                app_name (str): Application name
                app_author (str): Application author
                theme (str): Default theme name
                dark_theme (str): Default dark theme. Bound to "dark" theme name.
                light_theme (str): Default light theme. Bound to "light" theme name.
                load_select_themes (List[str]): Optional ordered list of theme
                    names to expose in application UI (e.g., theme pickers).
                    When set, helpers like Style.list_themes() will filter and
                    order themes using this list. Themes not in this list are
                    still registered and may be used programmatically.
                font (Tuple[str, int]): Default font as (family, size)
                legacy_bootstyle (bool): Use legacy bootstyle parsing
                inherit_surface_color (bool): Use the parent widget's background color to simulate transparency.
                window_size (Tuple[int, int]): Default window size
                window_position (Tuple[int, int]): Default window position
                window_minsize (Tuple[int, int]): Minimum window size
                window_maxsize (Tuple[int, int]): Maximum window size
                window_resizable (Tuple[bool, bool]): Window resizable flags
                window_scaling (float): Window scaling factor
                window_hdpi (bool): Enable high-DPI support
                window_alpha (float): Window transparency (0.0 to 1.0)
                icon_provider (type): Icon provider class (e.g., BootstrapIcon)
                language (str): Default language code
                date_format (str): Date format string
                time_format (str): Time format string
                number_decimal (str): Decimal separator character
                number_thousands (str): Thousands separator character

        Examples:
            >>> AppConfig.set(
            ...     dark_theme="dark",
            ...     light_theme="light",
            ...     theme="dark",
            ...     font=("Arial", 11),
            ...     window_size=(1024, 768),
            ...     window_hdpi=True
            ... )

        Raises:
            ValueError: If an invalid configuration key is provided.
        """
        valid_keys = {
            'app_name', 'app_author',
            'theme', 'font', 'dark_theme', 'light_theme',
            'load_select_themes',
            'legacy_bootstyle',
            'inherit_surface_color',
            'window_size', 'window_position', 'window_minsize', 'window_maxsize',
            'window_resizable', 'window_scaling', 'window_hdpi', 'window_alpha',
            'icon_provider',
            'language', 'date_format', 'time_format', 'number_decimal', 'number_thousands'
        }

        invalid_keys = set(kwargs.keys()) - valid_keys
        if invalid_keys:
            raise ValueError(
                f"Invalid configuration key(s): {', '.join(invalid_keys)}. "
                f"Valid keys are: {', '.join(sorted(valid_keys))}"
            )

        for key, value in kwargs.items():
            setattr(cls, f'_{key}', value)

    @classmethod
    def get(cls, key: str, default: Any = None) -> Any:
        """Get a configuration value by key.

        Args:
            key: Configuration key to retrieve.
            default: Default value to return if key is not set.

        Returns:
            The configuration value, or default if not set.

        Examples:
            >>> theme = AppConfig.get("theme", "dark")
            >>> window_size = AppConfig.get("window_size")

        Raises:
            ValueError: If an invalid configuration key is provided.
        """
        attr_name = f'_{key}'
        if not hasattr(cls, attr_name):
            raise ValueError(
                f"Invalid configuration key: {key}. "
                f"Use get_all() to see all valid keys."
            )

        value = getattr(cls, attr_name)
        return value if value is not None else default

    @classmethod
    def get_all(cls) -> Dict[str, Any]:
        """Get all configuration values as a dictionary.

        Returns:
            Dictionary of all configuration key-value pairs. Only includes
            keys that have been explicitly set (non-None, non-empty values).

        Examples:
            >>> AppConfig.reset()  # Start fresh
            >>> AppConfig.set(theme="bootstrap-dark", font=("Arial", 11), window_size=(1024, 768))
            >>> config = AppConfig.get_all()
            >>> config == {'theme': 'bootstrap-dark', 'font': ('Arial', 11), 'window_size': (1024, 768)}
            True
            >>> AppConfig.reset()  # Clean up
        """
        config = {}

        for attr_name in dir(cls):
            if attr_name.startswith('_') and not attr_name.startswith('__'):
                value = getattr(cls, attr_name)
                if value is not None and not callable(value):
                    if isinstance(value, (dict, list, tuple, set)) and len(value) == 0:
                        continue
                    key = attr_name[1:]
                    config[key] = value

        return config

    @classmethod
    def reset(cls, key: Optional[str] = None) -> None:
        """Reset configuration to defaults.

        Args:
            key: Optional specific key to reset. If None, resets all configuration.

        Examples:
            >>> # Reset specific key
            >>> AppConfig.reset("theme")
            >>>
            >>> # Reset all configuration
            >>> AppConfig.reset()

        Raises:
            ValueError: If an invalid configuration key is provided.
        """
        if key is None:
            cls._app_name = None
            cls._app_author = None
            cls._theme = None
            cls._font = None
            cls._colors = {}
            cls._inherit_surface_color = None
            cls._legacy_bootstyle = None
            cls._window_size = None
            cls._window_position = None
            cls._window_minsize = None
            cls._window_maxsize = None
            cls._window_resizable = None
            cls._window_scaling = None
            cls._window_hdpi = None
            cls._window_alpha = None
            cls._icon_provider = None
            cls._language = None
            cls._date_format = None
            cls._time_format = None
            cls._number_decimal = None
            cls._number_thousands = None
        else:
            attr_name = f'_{key}'
            if not hasattr(cls, attr_name):
                raise ValueError(
                    f"Invalid configuration key: {key}. "
                    f"Use get_all() to see all valid keys."
                )

            if key == 'colors':
                setattr(cls, attr_name, {})
            else:
                setattr(cls, attr_name, None)

    @classmethod
    def has(cls, key: str) -> bool:
        """Check if a configuration key has been set.

        Args:
            key: Configuration key to check.

        Returns:
            True if the key has been set to a non-None value, False otherwise.

        Examples:
            >>> AppConfig.set(theme="darkly")
            >>> AppConfig.has("theme")
            True
            >>> AppConfig.has("font")
            False

        Raises:
            ValueError: If an invalid configuration key is provided.
        """
        attr_name = f'_{key}'
        if not hasattr(cls, attr_name):
            raise ValueError(
                f"Invalid configuration key: {key}. "
                f"Use get_all() to see all valid keys."
            )

        value = getattr(cls, attr_name)
        return value is not None

    @classmethod
    def __repr__(cls) -> str:
        """String representation of the current configuration."""
        config = cls.get_all()
        if not config:
            return "AppConfig()"

        items = [f"{k}={repr(v)}" for k, v in config.items()]
        return f"AppConfig({', '.join(items)})"


def use_icon_provider() -> Type[Any]:
    """Return the configured icon provider class.

    Behavior:
    - If `AppConfig.icon_provider` is set, return it.
    - Otherwise, attempt to use the default `BootstrapIcon` from
      the optional `ttkbootstrap_icons` package.

    Returns:
        Icon provider class.

    Raises:
        ImportError: If no provider is configured and the default
            `BootstrapIcon` cannot be imported.
    """
    provider = AppConfig.get('icon_provider')
    if provider is not None:
        return provider  # type: ignore[return-value]

    # Try importing the default BootstrapIcon from ttkbootstrap_icons
    errors: list[str] = []
    candidates = (
        'ttkbootstrap_icons',
        'ttkbootstrap_icons.bootstrap_icon',
        'ttkbootstrap_icons.icons',
        'ttkbootstrap_icons_bs'
    )
    for modname in candidates:
        try:
            mod = __import__(modname, fromlist=['BootstrapIcon'])
            default = getattr(mod, 'BootstrapIcon')
            # Cache for subsequent calls
            AppConfig.set(icon_provider=default)
            return default  # type: ignore[return-value]
        except Exception as e:  # pragma: no cover - best-effort fallback
            errors.append(f"{modname}: {e}")

    raise ImportError(
        "Icon provider is not configured and default BootstrapIcon could not be imported. "
        "Install 'ttkbootstrap-icons' or set AppConfig.set(icon_provider=YourProviderClass).\n"
        + "; ".join(errors)
    )
