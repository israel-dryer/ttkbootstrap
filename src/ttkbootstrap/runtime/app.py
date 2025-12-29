from __future__ import annotations

import tkinter
from dataclasses import dataclass
from typing import Literal, Optional, Sequence, TypedDict, Union

from babel.core import UnknownLocaleError
from babel.dates import get_date_format, get_time_format
from babel.numbers import get_decimal_symbol, get_group_symbol
from typing_extensions import Unpack

from ttkbootstrap.constants import *
from ttkbootstrap.core.localization.intl_format import detect_locale
from ttkbootstrap.core.localization.msgcat import MessageCatalog
from ttkbootstrap.core.publisher import Publisher
from ttkbootstrap.core.mixins.widget import WidgetCapabilitiesMixin
from ttkbootstrap.runtime.base_window import BaseWindow
from ttkbootstrap.runtime.utility import enable_high_dpi_awareness

_current_app: App | None = None


def set_current_app(app: App) -> None:
    """Set the process-wide current App instance.

    Intended to be called from App.__init__ for the first app created.
    """
    global _current_app
    _current_app = app


def get_app_settings() -> AppSettings:
    """Return the settings for current App.

    Returns:
        The AppSettings instance for the current application.

    Raises:
        RuntimeError: If no active App instance is set.
    """
    return get_current_app().settings


def clear_current_app(app: App) -> None:
    """Clear the current app reference if it matches the given app."""
    global _current_app
    if _current_app is app:
        _current_app = None


def get_current_app() -> App:
    """Return the current App instance.

    Returns:
        The currently active App instance.

    Raises:
        RuntimeError: If no App has been registered yet.
    """
    if _current_app is None:
        raise RuntimeError(
            "No current App instance is set. "
            "Create an App first, e.g. `app = App()`."
        )
    return _current_app


def has_current_app() -> bool:
    """Check if a current App instance is registered.

    Returns:
        True if an App instance exists, False otherwise.
    """
    return _current_app is not None


def get_default_root(what: Optional[str] = None) -> tkinter.Tk:
    """Get the default Tk root window.

    Returns the default root if it has been created, otherwise
    creates and returns a new instance.

    Args:
        what: Optional description of the operation requiring the root,
            used in error messages if called too early.

    Returns:
        The default Tk root window instance.

    Raises:
        RuntimeError: If tkinter is configured to not support default root,
            or if called too early with a 'what' description.
    """
    if not tkinter._support_default_root:
        raise RuntimeError(
            "No master specified and tkinter is "
            "configured to not support default root")
    if not tkinter._default_root:
        if what:
            raise RuntimeError(f"Too early to {what}: no default root window")
        root = tkinter.Tk()
        assert tkinter._default_root is root
    return tkinter._default_root


def apply_class_bindings(window: tkinter.Widget | App) -> None:
    """Add class level event bindings in application"""
    # Copy TCheckbutton bindings to Toolbutton class
    # This is needed because widgets using class_='Toolbutton' have their
    # bindtags reference 'Toolbutton' instead of 'TCheckbutton', so they
    # need the same mouse/keyboard bindings copied over.
    for event in ('<Button-1>', '<ButtonRelease-1>', '<B1-Leave>', '<B1-Enter>',
                  '<Enter>', '<Leave>', '<Key-space>', '<<Invoke>>'):
        binding = window.bind_class('TCheckbutton', event)
        if binding:
            window.bind_class('Toolbutton', event, binding)

    for className in ["TEntry", "TSpinbox", "TCombobox", "Text"]:
        window.bind_class(
            className=className,
            sequence="<Configure>",
            func=on_disabled_readonly_state,
            add="+")

        for sequence in ["<Control-a>", "<Control-A>"]:
            window.bind_class(
                className=className,
                sequence=sequence,
                func=on_select_all)

    window.unbind_class("TButton", "<Key-space>")

    def button_default_binding(event: tkinter.Event) -> None:
        """The default keybind on a button when the return or enter key
        is pressed and the button has focus or is the default button."""
        try:
            widget = window.nametowidget(event.widget)
            widget.invoke()
        except KeyError:
            window.tk.call(event.widget, 'invoke')

    window.bind_class(
        "TButton", "<Key-Return>", button_default_binding,
        add="+")
    window.bind_class("TButton", "<KP_Enter>", button_default_binding, add="+")


def apply_all_bindings(window: tkinter.Widget | App) -> None:
    """Add bindings to all widgets in the application"""
    window.bind_all('<Map>', on_map_child, '+')
    window.bind_all('<Destroy>', lambda e: Publisher.unsubscribe(e.widget))


def on_disabled_readonly_state(event: tkinter.Event) -> None:
    """Change the cursor of entry type widgets to 'arrow' if in a
    disabled or readonly state."""
    try:
        widget = event.widget
        state = str(widget.cget('state'))
        cursor = str(widget.cget('cursor'))
        if state in (DISABLED, READONLY):
            if cursor == 'arrow':
                return
            else:
                widget['cursor'] = 'arrow'
        else:
            if cursor in ('ibeam', ''):
                return
            else:
                widget['cursor'] = None
    except:
        pass


def on_map_child(event: tkinter.Event) -> None:
    """Callback for <Map> event which generates a <<MapChild>> virtual
    event on the parent"""
    widget: tkinter.Widget = event.widget
    try:
        if widget.master is None:  # root widget
            return
        else:
            widget.master.event_generate('<<MapChild>>')
    except:
        # not a tkinter widget that I'm handling (ex. Combobox.popdown)
        return


def on_select_all(event: tkinter.Event) -> None:
    """Callback to select all text in Entry or Text widget when Ctrl+A is pressed."""
    widget = event.widget

    if isinstance(widget, tkinter.Text):
        widget.tag_add(SEL, "1.0", END)
        widget.mark_set(INSERT, END)
        widget.see(INSERT)
    elif isinstance(widget, tkinter.Entry):
        widget.selection_range(0, END)
        widget.icursor(END)


LocalizeMode = Union[bool, Literal['auto']]


@dataclass
class AppSettings:
    """Application-wide settings for ttkbootstrap applications.

    This dataclass holds configuration for theming, localization, and
    application metadata. It is automatically populated with sensible
    defaults based on the system locale.

    Attributes:
        app_name: The application name displayed in the title bar.
        app_author: The application author (used for config paths).
        app_version: The application version string.
        theme: The current theme name ('light', 'dark', or a specific theme).
        light_theme: The theme to use when `theme='light'`.
        dark_theme: The theme to use when `theme='dark'`.
        available_themes: Sequence of available theme names.
        inherit_surface_color: If True, child widgets inherit the parent's
            surface color for consistent backgrounds.
        locale: The locale identifier (e.g., 'en_US', 'de_DE'). Auto-detected
            from system if not specified.
        language: The base language code (e.g., 'en', 'de'). Derived from
            locale if not specified.
        date_format: The date format pattern. Derived from locale if not
            specified (e.g., 'M/d/yy' for en_US).
        time_format: The time format pattern. Derived from locale if not
            specified (e.g., 'h:mm a' for en_US).
        number_decimal: The decimal separator character. Derived from locale
            if not specified (e.g., '.' for en_US).
        number_thousands: The thousands separator character. Derived from
            locale if not specified (e.g., ',' for en_US).
        localize_mode: Controls localization behavior. 'auto' enables
            localization based on locale, True always enables, False disables.

    Examples:
        ```python
        # Create app with default settings
        app = App()

        # Create app with custom settings
        settings = AppSettings(
            app_name="My App",
            theme="dark",
            locale="de_DE"
        )
        app = App(settings=settings)

        # Access settings
        print(app.settings.locale)  # 'de_DE'
        print(app.settings.date_format)  # 'd.M.yy'
        ```
    """
    # information
    app_name: str | None = None
    app_author: str | None = None
    app_version: str | None = None

    # theme
    theme: str = "light"
    light_theme: str = "docs-light"
    dark_theme: str = "docs-dark"
    available_themes: Sequence[str] = ()
    inherit_surface_color: bool = True

    # internationalization
    locale: str | None = None
    language: str | None = None
    date_format: str | None = None
    time_format: str | None = None
    number_decimal: str | None = None
    number_thousands: str | None = None

    # localization behavior
    localize_mode: LocalizeMode = "auto"

    def __post_init__(self):
        """Populate localization defaults when not explicitly configured."""
        _apply_localization_defaults(self)


class AppSettingsKwargs(TypedDict, total=False):
    app_name: str
    app_author: str
    app_version: str

    # theme
    theme: str
    light_theme: str
    dark_theme: str
    available_themes: Sequence[str]
    inherit_surface_color: bool

    # localization
    locale: str
    language: str
    date_format: str
    time_format: str
    number_decimal: str
    number_thousands: str


DEFAULT_LOCALE = "en_US"


def _apply_localization_defaults(settings: AppSettings) -> None:
    """Ensure locale-based fields always have meaningful defaults."""
    locale_code = settings.locale or detect_locale(DEFAULT_LOCALE)
    settings.locale = locale_code

    if settings.language is None:
        settings.language = _language_from_locale(locale_code)

    if settings.date_format is None:
        settings.date_format = _safe_date_format(locale_code)

    if settings.time_format is None:
        settings.time_format = _safe_time_format(locale_code)

    if settings.number_decimal is None:
        settings.number_decimal = _safe_decimal_symbol(locale_code)

    if settings.number_thousands is None:
        settings.number_thousands = _safe_group_symbol(locale_code)


def _language_from_locale(locale_code: str) -> str:
    """Return the base language (e.g., en_US -> en)."""
    base = locale_code.split("_", 1)[0]
    return base.lower() if base else locale_code


def _safe_date_format(locale_code: str) -> str:
    try:
        return str(get_date_format("short", locale=locale_code))
    except (UnknownLocaleError, ValueError):
        return str(get_date_format("short", locale=DEFAULT_LOCALE))


def _safe_time_format(locale_code: str) -> str:
    try:
        return str(get_time_format("short", locale=locale_code))
    except (UnknownLocaleError, ValueError):
        return str(get_time_format("short", locale=DEFAULT_LOCALE))


def _safe_decimal_symbol(locale_code: str) -> str:
    try:
        return get_decimal_symbol(locale_code)
    except (UnknownLocaleError, ValueError):
        return get_decimal_symbol(DEFAULT_LOCALE)


def _safe_group_symbol(locale_code: str) -> str:
    try:
        return get_group_symbol(locale_code)
    except (UnknownLocaleError, ValueError):
        return get_group_symbol(DEFAULT_LOCALE)


class TkKwargs(TypedDict, total=False):
    """The following attributes are available per the Tkinter API (not commonly used).

    Attributes:
        screenName: Sets the display environment variable (X11 only).
        baseName: Name of the profile file. By default, derived from program name.
        className: Name of the widget class
        useTk: If True, initializes the Tk system.
        sync: If true, executes all X server commands synchronously.
        use: The id of the window in which to embed the application.
    """
    screenName: str
    baseName: str
    className: str
    useTk: bool
    sync: bool
    use: str


class App(BaseWindow, WidgetCapabilitiesMixin, tkinter.Tk):
    """The primary application window and entry point.

    App adds theming, localization, and platform setup on top of `tkinter.Tk`.

    The standard widget API (events, scheduling, clipboard, geometry managers,
    winfo, etc.) is documented under ttkbootstrap capabilities and is available
    on App via inheritance.
    """

    def __init__(
            self,
            title: str | None = None,
            theme: str | None = None,
            icon: tkinter.PhotoImage | None = None,

            settings: AppSettings | AppSettingsKwargs | None = None,
            localize: LocalizeMode | None = None,

            # window settings
            size: tuple[int, int] | None = None,
            position: tuple[int, int] | None = None,
            minsize: tuple[int, int] | None = None,
            maxsize: tuple[int, int] | None = None,
            resizable: tuple[bool, bool] | None = None,
            scaling: float | None = None,
            hdpi: bool = True,
            alpha: float = 1.0,
            transient: object | None = None,
            override_redirect: bool = False,
            **kwargs: Unpack[TkKwargs],
    ) -> None:
        """Initializes the application window.

        Args:
            title: The text to display in the window's title bar. This
                overrides the `app_name` in `settings` if provided.
            theme: The name of the theme to use. This overrides the `theme`
                in `settings` if provided.
            icon: A PhotoImage or file path used for the window's icon.
                If None, the default ttkbootstrap.png icon is used.
            settings: A dictionary or `AppSettings` object containing
                application-wide settings. If not provided, default settings
                are used.
            localize: The localization mode for the application. Can be
                'auto', `True`, or `False`. This overrides the `localize_mode`
                in `settings`.
            size: A tuple specifying the window's initial width and height.
            position: A tuple specifying the window's initial x and y
                coordinates on the screen.
            minsize: A tuple specifying the window's minimum width and height.
            maxsize: A tuple specifying the window's maximum width and height.
            resizable: A tuple of booleans specifying whether the window can
                be resized horizontally and vertically.
            scaling: The DPI scaling factor for the window. If `None`,
                automatic scaling is used.
            hdpi: If `True`, enables high-DPI awareness for the application.
            alpha: The window's transparency level, from 0.0 (fully
                transparent) to 1.0 (fully opaque).
            transient: The parent window for this window.
            override_redirect: If `True`, creates a window without standard
                decorations (title bar, borders, etc.).
            **kwargs: Additional keyword arguments to pass to the
                underlying `tkinter.Tk` constructor.
        """
        # --- Settings ---------------------------------------------------
        if settings is None:
            self.settings = AppSettings()
        elif isinstance(settings, AppSettings):
            self.settings = settings
        else:
            self.settings = AppSettings(**settings)

        # App-level overrides from ctor
        if theme is not None:
            self.settings.theme = theme
        if title is not None:
            self.settings.app_name = title

        # If app_name is still None, give it a sensible default
        if self.settings.app_name is None:
            self.settings.app_name = "ttkbootstrap"

        if localize is not None:
            self.settings.localize_mode = localize

        # --- Window options ---------------------------------------------
        self._size = size
        self._position = position
        self._minsize = minsize
        self._maxsize = maxsize
        self._resizable = resizable
        self._scaling = scaling
        self._hdpi = hdpi
        self._transient = transient
        self._alpha = alpha
        self._override_redirect = override_redirect

        # Register app
        if not has_current_app():
            set_current_app(self)

        # Enable HDPI before creating window
        if self._hdpi:
            enable_high_dpi_awareness()

        # Initialize Tk
        tkinter.Tk.__init__(self, **kwargs)
        self.withdraw()  # hide immediately until ready to show.

        # Setup window system info
        self.winsys: str = self.tk.call('tk', 'windowingsystem')

        # Apply theme (use resolved settings.theme)
        from ttkbootstrap.style.style import set_theme
        set_theme(self.settings.theme)

        # Initialize the localization bridge so MessageCatalog.translate()
        # and <<LocaleChanged>> are available throughout the app.
        MessageCatalog.init(
            locales_dir=None,
            domain="ttkbootstrap",
            default_locale=self.settings.locale or DEFAULT_LOCALE,
        )

        # Apply HDPI scaling after window creation
        if self._hdpi:
            if self._scaling is None:
                enable_high_dpi_awareness(self, 'auto')
            else:
                enable_high_dpi_awareness(self, self._scaling)

        # Setup icon
        self._setup_icon(icon, default_icon_enabled=True)

        # Setup window using BaseWindow
        self._setup_window(
            title=self.settings.app_name,
            size=self._size,
            position=self._position,
            minsize=self._minsize,
            maxsize=self._maxsize,
            resizable=self._resizable,
            transient=self._transient,
            overrideredirect=self._override_redirect,
            alpha=self._alpha,
        )

        # Apply ttkbootstrap-specific bindings
        apply_class_bindings(self)
        apply_all_bindings(self)

    def mainloop(self, n=0) -> None:
        """Start the application event loop

        Args:
            n (int): A threshold that keeps the window open if at least n windows is open. This is an archaic c-level
                detail that should not be adjusted unless you have a specific reason.
        """
        self.show()
        super().mainloop(n=n)

    def close(self) -> None:
        """Close the application window (destroys the Tk root)"""
        clear_current_app(self)
        self.quit()

    def destroy(self) -> None:
        """Destroys the window and all its children."""
        clear_current_app(self)
        super().destroy()


# Backward compatibility alias
Window = App
