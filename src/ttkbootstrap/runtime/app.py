from __future__ import annotations

import tkinter
from dataclasses import dataclass
from typing import Any, Optional, Sequence, Tuple, TypedDict, Union

from babel.core import UnknownLocaleError
from babel.dates import get_date_format, get_time_format
from babel.numbers import get_decimal_symbol, get_group_symbol
from typing_extensions import Unpack

from ttkbootstrap.constants import *
from ttkbootstrap.core.publisher import Publisher
from ttkbootstrap.runtime.base_window import BaseWindow
from ttkbootstrap.runtime.utility import enable_high_dpi_awareness
from ttkbootstrap.core.localization.intl_format import detect_locale
from ttkbootstrap.core.localization.msgcat import MessageCatalog

_current_app: App | None = None


def set_current_app(app: App) -> None:
    """Set the process-wide current App instance.

    Intended to be called from App.__init__ for the first app created.
    """
    global _current_app
    _current_app = app


def get_app_settings() -> AppSettings:
    """Return the settings for current App

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
    """Return True if a current App instance is registered."""
    return _current_app is not None


def get_default_root(what: Optional[str] = None) -> tkinter.Tk:
    """Returns the default root if it has been created, otherwise
    returns a new instance."""
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


def apply_class_bindings(window: tkinter.Widget) -> None:
    """Add class level event bindings in application"""
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


def apply_all_bindings(window: tkinter.Widget) -> None:
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


@dataclass
class AppSettings:
    # information
    app_name: str | None = None
    app_author: str | None = None
    app_version: str | None = None

    # theme
    theme: str = "light"
    light_theme: str = "bootstrap-light"
    dark_theme: str = "bootstrap-dark"
    available_themes: Sequence[str] = ()
    inherit_surface_color: bool = True

    # internationalization
    locale: str | None = None  # e.g. "en_US"
    language: str | None = None  # e.g. "en"
    date_format: str | None = None  # override; otherwise use locale
    time_format: str | None = None  # override
    number_decimal: str | None = None
    number_thousands: str | None = None

    def __post_init__(self):
        """Populate localization defaults when not explicitly configured."""
        _apply_localization_defaults(self)


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


class App(BaseWindow, tkinter.Tk):

    def __init__(
            self,
            title: str | None = None,
            theme: str | None = None,
            icon: tkinter.PhotoImage | None = None,
            settings: AppSettings | None = None,

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
        # --- Settings ---------------------------------------------------
        self.settings = settings or AppSettings()

        # App-level overrides from ctor
        if theme is not None:
            self.settings.theme = theme
        if title is not None:
            self.settings.app_name = title

        # If app_name is still None, give it a sensible default
        if self.settings.app_name is None:
            self.settings.app_name = "ttkbootstrap"

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
        self.withdraw() # hide immediately until ready to show.

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

    def mainloop(self, n=0):
        """Start the main Tk event loop"""
        self.show()
        super().mainloop(n)

    def destroy(self) -> None:
        """Destroy the window and all its children."""
        clear_current_app(self)
        super().destroy()


# Backward compatibility alias
Window = App


class Toplevel(BaseWindow, tkinter.Toplevel):
    """A class that wraps the tkinter.Toplevel class in order to
    provide a more convenient api with additional bells and whistles.
    For more information on how to use the inherited `Toplevel`
    methods, see the [tcl/tk documentation](https://tcl.tk/man/tcl8.6/TkCmd/toplevel.htm)
    and the [Python documentation](https://docs.python.org/3/library/tkinter.html#tkinter.Toplevel).

    ![](../../assets/window/window-toplevel.png)

    Examples:

        ```python
        app = Toplevel(title="My Toplevel")
        app.mainloop()
        ```
    """

    def __init__(
            self,
            title: str = "ttkbootstrap",
            icon: tkinter.PhotoImage | None = None,
            size: Optional[Tuple[int, int]] = None,
            position: Optional[Tuple[int, int]] = None,
            minsize: Optional[Tuple[int, int]] = None,
            maxsize: Optional[Tuple[int, int]] = None,
            resizable: Optional[Tuple[bool, bool]] = None,
            transient: Optional[tkinter.Misc] = None,
            overrideredirect: bool = False,
            windowtype: Optional[str] = None,
            topmost: bool = False,
            toolwindow: bool = False,
            alpha: float = 1.0,
            **kwargs: Any,
    ) -> None:
        """
        Parameters:

            title (str):
                The title that appears on the application titlebar.

            icon (tkinter.PhotoImage):
                A PhotoImage used for the titlebar icon.
                Internally this is passed to the `Toplevel.iconphoto` method.
                No default icon is used for Toplevel windows.

            size (tuple[int, int]):
                The width and height of the application window.
                Internally, this argument is passed to the
                `Toplevel.geometry` method.

            position (tuple[int, int]):
                The horizontal and vertical position of the window on
                the screen relative to the top-left coordinate.
                Internally this is passed to the `Toplevel.geometry`
                method.

            minsize (tuple[int, int]):
                Specifies the minimum permissible dimensions for the
                window. Internally, this argument is passed to the
                `Toplevel.minsize` method.

            maxsize (tuple[int, int]):
                Specifies the maximum permissible dimensions for the
                window. Internally, this argument is passed to the
                `Toplevel.maxsize` method.

            resizable (tuple[bool, bool]):
                Specifies whether the user may interactively resize the
                toplevel window. Must pass in two arguments that specify
                this flag for _horizontal_ and _vertical_ dimensions.
                This can be adjusted after the window is created by using
                the `Toplevel.resizable` method.

            transient (Union[Tk, Widget]):
                Instructs the window manager that this widget is
                transient with regard to the widget master. Internally
                this is passed to the `Toplevel.transient` method.

            overrideredirect (bool):
                Instructs the window manager to ignore this widget if
                True. Internally, this argument is processed as
                `Toplevel.overrideredirect(1)`.

            windowtype (str):
                On X11, requests that the window should be interpreted by
                the window manager as being of the specified type. Internally,
                this is passed to the `Toplevel.attributes('-type', windowtype)`.

                See the [-type option](https://tcl.tk/man/tcl8.6/TkCmd/wm.htm#M64)
                for a list of available options.

            topmost (bool):
                Specifies whether this is a topmost window (displays above all
                other windows). Internally, this processed by the window as
                `Toplevel.attributes('-topmost', 1)`.

            toolwindow (bool):
                On Windows, specifies a toolwindow style. Internally, this is
                processed as `Toplevel.attributes('-toolwindow', 1)`.

            alpha (float):
                On Windows, specifies the alpha transparency level of the
                toplevel. Where not supported, alpha remains at 1.0. Internally,
                this is processed as `Toplevel.attributes('-alpha', alpha)`.

            **kwargs (Dict):
                Other optional keyword arguments.
        """
        # Extract iconify kwarg if present
        iconify = kwargs.pop('iconify', None)

        # Initialize Toplevel
        tkinter.Toplevel.__init__(self, **kwargs)

        # Setup window system info
        self.winsys: str = self.tk.call('tk', 'windowingsystem')

        # Setup icon (no default for Toplevel)
        self._setup_icon(icon, default_icon_enabled=False)

        # Setup window using BaseWindow
        self._setup_window(
            title=title,
            size=size,
            position=position,
            minsize=minsize,
            maxsize=maxsize,
            resizable=resizable,
            transient=transient,
            overrideredirect=overrideredirect,
            alpha=alpha
        )

        # Handle iconify
        if iconify:
            self.iconify()

        # Toplevel-specific window attributes
        if windowtype is not None and self.winsys == 'x11':
            self.attributes("-type", windowtype)

        if topmost:
            self.attributes("-topmost", 1)

        if toolwindow and self.winsys == 'win32':
            self.attributes("-toolwindow", 1)
