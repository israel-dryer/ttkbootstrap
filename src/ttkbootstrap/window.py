"""Window and Toplevel classes for ttkbootstrap applications.

`Window` and `Toplevel` wrap `tkinter.Tk`/`tkinter.Toplevel` with integrated
ttkbootstrap `Style` support and a consolidated construction API — theme, title,
size/position/geometry, resizability, high-DPI, alpha, and icon handling.
"""
import sys
import tkinter
import warnings
from pathlib import Path
from typing import Any, Optional, Tuple, Union

from ttkbootstrap import utility
from ttkbootstrap.constants import *
from ttkbootstrap.internal import positioning
from ttkbootstrap.style import Style, Bootstyle
from ttkbootstrap.style._compat import normalize_window_kwargs

# The default ttkbootstrap window icon (brand logo, 32x32 PNG) used when a
# Window/Toplevel is created with ``iconphoto=''``. This is a base64-encoded
# PhotoImage data string -- a brand mark, not a Bootstrap glyph, so it stays an
# embedded asset rather than routing through the icon-font engine. (Formerly
# ``ttkbootstrap.icons.Icon.icon``, removed in 2.0.) Used as the last-resort
# fallback when the packaged app-icon files below can't be found.
_DEFAULT_ICON_DATA = "iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAAFxEAABcRAcom8z8AAAT/SURBVFhHzZd9TNR1HMff/O64BwKOp+NRnkIScJI2n7ZqFmqjVhkrHExrrDFZLnPkqmEyW2WtlQ1SQawWPSAYiJLNGvK0VhJOaDgVBDPCw0PwEOUQfsfd/fp+v/cFbt0Bd6yxXvfP5+F79/l+P9+H+3w8wMnO3r40I+P5vOCQ4I1ymVzrQeCu/wSJYDabB/sHbp45XlnzQUnJgcvcBRQUHEjX6/vH6aCFQK/XjxcWHnyBxpbRle/Ysf3n0NAQJTWMmiRUnB/FNy1GNHaNYdwsIS7IE4JdPqxWKxoam3D0aAVq6+rR39+P2NhYKBQKPsJGx3Abyq8dxGldBbrvXkSoVyR8Pf3g7e0tj46O2mQ0Gqs96urqv1u/PmUL/cLfQ2a8/O0t9A2b2Q9MsjpGicOZQfBSeEAURbyZtxstLee410awVovCgk8RGxPD9NLuT1B6dT+TJ/EUFMhL/gwpYZuYXl/fUCbQPaeKVQJyqwwOwSnnekR8VDvM5JIjnzsEpwwMDmL32/mwWCxoHqhzCE6ZsJrw4YWduHGvh+k0tkAPHFXadSZc1k8whzNOtt+DcWwCJ2p+4BZH/urpwfnWNpzs/YpbHJmwivjxehmTaWxh8rTT9M+GSM7CpZ5BjI2NcYtzdH069PEVzsSkn8YWmETQek+JTpER9/3h/pDL5dzinKDAQAQqg7nmHHv/VNRV5KCFaWRcc2RdvBpajRopjz/GLY4EBARgzerVeCKc3TCneJDPxohp/9QEFDIPfJwWwE76v1nkL8fep/yYnLvzNURFRTLZHqVSib35e6BSqfDkokysC32ae6ahwbPidyFRs4JbiK2jo1NKSFjCVaDHYMaRX0fQ3mcikwIeiVMh+2EfaNTTW2Q0jqKsvBxnzzaza5mYmICXXtw6dQUpVslK7n85ztyogkEcQIRXLNKis7BWu4GPADo7rzhOYCGZ9wQmxi249NN19P5xCxaTFdo4XyQ/Gw3fEDUf4RrzmoA4MoFT77RiqNfILTY8VTKk5i1HWJI/t8wNncDsd88JzV93OQSn0Kw0FF5kGXEHtyZgJj/+5283uebI6JAI3QUD11zDrQmIIyZYzLOvcNQgcsk13JqASqOAXDnzY0XxcfMgujUBmVzAkpRwrjmiCfNCxLIArrmG24dwzZbFTk+6mmRnw+vLIJAX1R3m9Q5IpHjo/kWP3jYDOZgW9g4sTY2EyseTj3CN/8VL6PYWMO70A1W7gHeTgfzFwBcZpBpp4U7OuAl4jxQm8ZvJ/pB/0IeygC9P0fKYD7DhfgaGeoFDzwAjA9zAEcjtyDwEPEjqPZFUVqm5QFMbd9rxShpQ9AYT55eBmj2OwSlWC1D9Fln5XaC42nlwSvEJoLGVK+7eApE8wVcauOKEsTtAVxPwfT03zMCxab9AGwUuz834iG2lszF6GzCQLMzGkM1PYwu0XWKaK/iQAlqt4coMhDwAJE0XJk7hfhpboL0a01xBIAXpo9u44oRIUmrFriV1G7kV9q2UPb73AdueYyKNLfNSazpXrlyRTdslZp2LmFXAbR2gn+4tGSHkJmWVkgz5AtGhpOsgT3ItaWBIGzeFnw9QuQ9YHk/bObG4qGgrs9NGkTaMdE9c5trvknR6nyTV5EtS23HS+pq4w46rOkl6v1SSXt0vSQXHJGlwmJltzWkhK42n8pSTk5OUnr5598K055WkPS8hKQT+AVyRrtzM5URAAAAAAElFTkSuQmCC"

# Packaged app-icon files, both built by ``tools/make_app_ico.py`` from the
# top-level (unshipped) source PNGs. The Windows titlebar/taskbar icon uses the
# multi-resolution ``.ico``; macOS/Linux use the 512px ``.png`` through
# ``iconphoto``. Resolved relative to this file so it works from an installed
# package.
_APP_ICONS_DIR = Path(__file__).parent / "assets" / "app_icons"
_APP_ICON_ICO = _APP_ICONS_DIR / "ttkbootstrap.ico"
_APP_ICON_PNG = _APP_ICONS_DIR / "ttkbootstrap.png"

# On macOS, override-redirect is a no-op (it breaks Cocoa click handling), so a
# borderless popup ``window_type`` would otherwise be drawn with full window
# chrome -- a titlebar on a tooltip. Map the EWMH-style ``window_type`` onto a
# native Aqua window class instead, which brings the real system shadow/rounded
# corners with no chrome. Types with no native equivalent keep default chrome.
_AQUA_WINDOW_STYLES = {
    "tooltip": ("help", "none"),
    "splash": ("plain", "none"),
    "utility": ("utility", "none"),
    "dock": ("plain", "none"),
}


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


def _require_single_root(new_root: tkinter.Misc) -> None:
    """Raise if a Style is already bound to a different, still-live root.

    The Style engine is a process-wide singleton tied to the first root that
    created it; a second concurrent root silently no-ops all theming. Enforce
    a single root with a clear error. Destroying the existing root clears the
    singleton, so sequential roots (e.g. one app after another) are allowed.
    """
    existing = Style.get_instance()
    if existing is None:
        return
    other = getattr(existing, "master", None)
    if other is None or other is new_root:
        return
    try:
        still_alive = bool(other.winfo_exists())
    except tkinter.TclError:
        still_alive = False
    if still_alive:
        raise RuntimeError(
            "ttkbootstrap supports a single application root window. A Style "
            "is already bound to an existing live root; create one "
            "Window/Tk per process and reuse it (or destroy the existing "
            "root before creating a new one). Multi-root support is out of "
            "scope."
        )


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


def on_visibility(event: tkinter.Event) -> None:
    """Set Window or Toplevel alpha value on Visibility (X11)"""
    widget = event.widget
    if isinstance(widget, (Window, Toplevel)) and widget.alpha_bind:
        widget.unbind(widget.alpha_bind)
        widget.attributes("-alpha", widget.alpha)


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


class _BaseWindow:
    """Window logic shared by `Window` (root) and `Toplevel` (secondary).

    Used as a mixin alongside `tkinter.Tk`/`tkinter.Toplevel`, so both classes
    stop duplicating -- and drifting on -- their icon, geometry, alpha, and
    positioning handling.
    """

    winsys: str

    @property
    def style(self) -> Style:
        """Return a reference to the `ttkbootstrap.style.Style` object."""
        return Style.get_instance()

    # -- setup helpers -----------------------------------------------------

    def _setup_icon(self, iconphoto: Optional[str], default_data: Optional[str] = None) -> None:
        """Configure the titlebar icon uniformly across both window classes.

        Semantics (identical for `Window` and `Toplevel`):
            None  -> leave the icon untouched (skip).
            ''    -> use `default_data` if given (the brand icon on `Window`),
                     otherwise inherit the application default (`Toplevel`).
            path  -> load the image, falling back to `default_data` on failure.

        A `.ico` path is applied through `wm_iconbitmap` on Windows; other
        formats go through `iconphoto`.
        """
        if iconphoto is None:
            return
        if iconphoto == '':
            if default_data is not None:
                self._apply_default_icon(default_data)
            return
        try:
            path = str(iconphoto)
            if path.lower().endswith('.ico') and self.winsys == 'win32':
                self.wm_iconbitmap(path)
            else:
                self._icon = tkinter.PhotoImage(file=path, master=self)
                self.iconphoto(True, self._icon)
        except tkinter.TclError:
            warnings.warn(
                f"iconphoto path {iconphoto!r} could not be loaded; "
                "using the default image.",
                UserWarning,
                stacklevel=3,
            )
            if default_data is not None:
                self._apply_default_icon(default_data)

    def _apply_default_icon(self, default_data: str) -> None:
        """Apply the brand app icon per platform.

        Windows gets the multi-resolution ``.ico`` via ``wm_iconbitmap`` (built
        by ``tools/make_app_ico.py``); macOS/Linux get a PNG via ``iconphoto``.
        Falls back to the embedded ``default_data`` (base64 PNG) if the packaged
        asset is missing or fails to load, so the icon is always set.
        """
        try:
            if self.winsys == 'win32':
                if _APP_ICON_ICO.is_file():
                    self.wm_iconbitmap(str(_APP_ICON_ICO))
                    return
            elif _APP_ICON_PNG.is_file():
                self._icon = tkinter.PhotoImage(master=self, file=str(_APP_ICON_PNG))
                self.iconphoto(True, self._icon)
                return
        except tkinter.TclError:
            pass
        self._icon = tkinter.PhotoImage(master=self, data=default_data)
        self.iconphoto(True, self._icon)

    def _apply_geometry(
            self,
            size: Optional[Tuple[int, int]],
            position: Optional[Tuple[int, int]],
    ) -> None:
        """Apply `size` and/or `position` as a single `geometry` call.

        `position` uses a signed format (`f"{x:+d}{y:+d}"`) so negative offsets
        express edge-relative placement (`position=(-10, -10)` -> near the
        bottom-right), which the old hardcoded `+{x}+{y}` could not.
        """
        geo = ""
        if size is not None:
            geo += f"{size[0]}x{size[1]}"
        if position is not None:
            x, y = position
            geo += f"{int(x):+d}{int(y):+d}"
        if geo:
            self.geometry(geo)

    def _apply_constraints(
            self,
            minsize: Optional[Tuple[int, int]],
            maxsize: Optional[Tuple[int, int]],
            resizable: Optional[Tuple[bool, bool]],
    ) -> None:
        """Apply `minsize`/`maxsize`/`resizable`, skipping any left as `None`."""
        if minsize is not None:
            self.minsize(minsize[0], minsize[1])
        if maxsize is not None:
            self.maxsize(maxsize[0], maxsize[1])
        if resizable is not None:
            self.resizable(resizable[0], resizable[1])

    def _setup_alpha(self, alpha: Optional[float]) -> None:
        """Set window transparency, platform-aware.

        On X11 alpha must be applied after the window is visible, so it is
        deferred to the `<Visibility>` event; Windows/aqua set it immediately.
        """
        if alpha is None:
            return
        if self.winsys == 'x11':
            self.alpha = alpha
            self.alpha_bind = self.bind("<Visibility>", on_visibility, '+')
        else:
            self.attributes("-alpha", alpha)

    def overrideredirect(self, boolean: Optional[bool] = None):
        """Get/set override-redirect, guarding the macOS no-op.

        On aqua, enabling override-redirect breaks click handling and can crash
        Tk/Cocoa, so a truthy request is silently ignored there.
        """
        if boolean and getattr(self, 'winsys', None) == 'aqua':
            return None
        return super().overrideredirect(boolean)

    def _apply_mac_window_style(self, window_type: str) -> None:
        """On aqua, map a borderless ``window_type`` to a native window class.

        No-op off aqua and for types with no native equivalent. The
        ``MacWindowStyle`` call lives in Tk's ``unsupported`` namespace, so it's
        wrapped and falls back to default chrome when unavailable.
        """
        if getattr(self, 'winsys', None) != 'aqua':
            return
        aqua_style = _AQUA_WINDOW_STYLES.get(window_type)
        if aqua_style is None:
            return
        try:
            self.tk.call(
                "::tk::unsupported::MacWindowStyle", "style",
                self, aqua_style[0], aqua_style[1],
            )
        except tkinter.TclError:
            pass

    # -- positioning -------------------------------------------------------

    def place_window_center(self) -> None:
        """Center the window on the screen (monitor under the cursor when
        `screeninfo` is available), clamped to stay fully visible."""
        x, y = positioning.center_on_screen(self)
        x, y = positioning.ensure_on_screen(self, x, y)
        self.geometry(f'+{x}+{y}')

    position_center = place_window_center  # alias


class Window(_BaseWindow, tkinter.Tk):
    """A class that wraps the tkinter.Tk class in order to provide a
    more convenient api with additional bells and whistles. For more
    information on how to use the inherited `Tk` methods, see the
    [tcl/tk documentation](https://tcl.tk/man/tcl8.6/TkCmd/wm.htm)
    and the [Python documentation](https://docs.python.org/3/library/tkinter.html#tkinter.Tk).

    Examples:

        ```python
        app = Window(title="My Application", themename="bootstrap-dark")
        app.mainloop()
        ```
    """

    def __init__(
            self,
            title: str = "ttkbootstrap",
            themename: str = "bootstrap-light",
            *,
            default_button: str = "neutral",
            iconphoto: Optional[str] = '',
            size: Optional[Tuple[int, int]] = None,
            position: Optional[Tuple[int, int]] = None,
            minsize: Optional[Tuple[int, int]] = None,
            maxsize: Optional[Tuple[int, int]] = None,
            resizable: Optional[Tuple[bool, bool]] = None,
            high_dpi: bool = True,
            scaling: Optional[float] = None,
            transient: Optional[tkinter.Misc] = None,
            override_redirect: bool = False,
            alpha: float = 1.0,
            **kwargs: Any,
    ) -> None:
        """
        Parameters:

            title (str):
                The title that appears on the application titlebar.

            themename (str):
                The name of the ttkbootstrap theme to apply to the
                application.

            default_button (str):
                The color a bare `Button`/`Menubutton` (no `bootstyle`) uses.
                Defaults to `"neutral"` (a quiet, unaccented button); pass
                `"primary"` to restore the pre-2.0 accented default.

            iconphoto (str):
                A path to the image used for the titlebar icon.
                Internally this is passed to the `Tk.iconphoto` method
                and the image will be the default icon for all windows.
                A ttkbootstrap image is used by default. To disable
                this default behavior, set the value to `None` and use
                the `Tk.iconphoto` or `Tk.iconbitmap` methods directly.

            size (tuple[int, int]):
                The width and height of the application window.
                Internally, this argument is passed to the
                `Window.geometry` method.

            position (tuple[int, int]):
                The horizontal and vertical position of the window on
                the screen relative to the top-left coordinate. Negative
                values are edge-relative (e.g. `(-10, -10)` places the
                window near the bottom-right). Internally this is passed
                to the `Window.geometry` method.

            minsize (tuple[int, int]):
                Specifies the minimum permissible dimensions for the
                window. Internally, this argument is passed to the
                `Window.minsize` method.

            maxsize (tuple[int, int]):
                Specifies the maximum permissible dimensions for the
                window. Internally, this argument is passed to the
                `Window.maxsize` method.

            resizable (tuple[bool, bool]):
                Specifies whether the user may interactively resize the
                toplevel window. Must pass in two arguments that specify
                this flag for _horizontal_ and _vertical_ dimensions.
                This can be adjusted after the window is created by using
                the `Window.resizable` method.

            high_dpi (bool):
                Enable high-dpi support for Windows OS. This option is
                enabled by default. (Renamed from `hdpi` in 2.0.)

            scaling (float):
                Sets the current scaling factor used by Tk to convert
                between physical units (for example, points, inches, or
                millimeters) and pixels. The number argument is a
                floating point number that specifies the number of pixels
                per point on window's display.

            transient (Union[Tk, Widget]):
                Instructs the window manager that this widget is
                transient with regard to the widget master. Internally
                this is passed to the `Window.transient` method.

            override_redirect (bool):
                Instructs the window manager to ignore this widget if
                True. Internally, this argument is passed to the
                `Window.overrideredirect(1)` method. Ignored on macOS
                (aqua), where it destabilizes Tk. (Renamed from
                `overrideredirect` in 2.0.)

            alpha (float):
                Sets the window's alpha transparency level (1.0 is opaque).
                Applied immediately via `Window.attributes('-alpha', alpha)`,
                except on X11 where it is deferred until the window becomes
                visible.

            **kwargs:
                Any other keyword arguments that are passed through to tkinter.Tk() constructor
                List of available keywords available at: https://docs.python.org/3/library/tkinter.html#tkinter.Tk
        """
        # Accept the pre-2.0 raw-Tk kwarg spellings with a deprecation warning.
        aliases = normalize_window_kwargs(kwargs)
        high_dpi = aliases.get("high_dpi", high_dpi)
        override_redirect = aliases.get("override_redirect", override_redirect)

        # ttkbootstrap supports a single application root. The Style engine is
        # a process-wide singleton bound to the first root; a second live root
        # would silently no-op all theming. Fail loudly before any side effects.
        _require_single_root(self)

        if high_dpi:
            utility.enable_high_dpi_awareness()

        # On win32, tag the process so the taskbar shows the app icon rather
        # than the generic python.exe one (bootstack app.py:534-540).
        self._set_app_user_model_id()

        super().__init__(**kwargs)
        self.winsys: str = utility.windowing_system(self)

        if scaling is not None:
            utility.enable_high_dpi_awareness(self, scaling)

        self._setup_icon(iconphoto, default_data=_DEFAULT_ICON_DATA)
        self.title(title)
        self._apply_geometry(size, position)
        self._apply_constraints(minsize, maxsize, resizable)

        if transient is not None:
            self.transient(transient)

        if override_redirect:
            self.overrideredirect(1)

        self._setup_alpha(alpha)

        apply_class_bindings(self)
        apply_all_bindings(self)
        self._style = Style(themename, default_button=default_button)

    @staticmethod
    def _set_app_user_model_id() -> None:
        """On win32, set an explicit AppUserModelID so the taskbar groups this
        app under its own icon instead of python.exe. No-op elsewhere."""
        if sys.platform != 'win32':
            return
        try:
            import ctypes
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
                "ttkbootstrap.app")
        except Exception:
            pass

    def destroy(self) -> None:
        """Destroy the window and all its children."""
        # Clear the process-wide singleton (a class attribute) so a later root
        # rebinds the Style cleanly instead of reusing this destroyed one.
        Style.instance = None
        super().destroy()


class Toplevel(_BaseWindow, tkinter.Toplevel):
    """A class that wraps the tkinter.Toplevel class in order to
    provide a more convenient api with additional bells and whistles.
    For more information on how to use the inherited `Toplevel`
    methods, see the [tcl/tk documentation](https://tcl.tk/man/tcl8.6/TkCmd/toplevel.htm)
    and the [Python documentation](https://docs.python.org/3/library/tkinter.html#tkinter.Toplevel).

    Examples:

        ```python
        app = Toplevel(title="My Toplevel")
        app.mainloop()
        ```
    """

    def __init__(
            self,
            title: str = "ttkbootstrap",
            *,
            iconphoto: Optional[str] = '',
            size: Optional[Tuple[int, int]] = None,
            position: Optional[Tuple[int, int]] = None,
            minsize: Optional[Tuple[int, int]] = None,
            maxsize: Optional[Tuple[int, int]] = None,
            resizable: Optional[Tuple[bool, bool]] = None,
            transient: Optional[tkinter.Misc] = None,
            override_redirect: bool = False,
            window_type: Optional[str] = None,
            topmost: bool = False,
            tool_window: bool = False,
            iconify: bool = False,
            alpha: float = 1.0,
            **kwargs: Any,
    ) -> None:
        """
        Parameters:

            title (str):
                The title that appears on the application titlebar.

            iconphoto (str):
                A path to the image used for the titlebar icon.
                Internally this is passed to the `Tk.iconphoto` method.
                By default the application icon is inherited. Set to
                `None` to leave the icon untouched.

            size (tuple[int, int]):
                The width and height of the application window.
                Internally, this argument is passed to the
                `Toplevel.geometry` method.

            position (tuple[int, int]):
                The horizontal and vertical position of the window on
                the screen relative to the top-left coordinate. Negative
                values are edge-relative. Internally this is passed to
                the `Toplevel.geometry` method.

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

            override_redirect (bool):
                Instructs the window manager to ignore this widget if
                True. Internally, this argument is processed as
                `Toplevel.overrideredirect(1)`. Ignored on macOS (aqua).
                (Renamed from `overrideredirect` in 2.0.)

            window_type (str):
                On X11, requests that the window should be interpreted by
                the window manager as being of the specified type. Internally,
                this is passed to the `Toplevel.attributes('-type', window_type)`.

                See the [-type option](https://tcl.tk/man/tcl8.6/TkCmd/wm.htm#M64)
                for a list of available options. (Renamed from `windowtype`
                in 2.0.)

                On macOS, the borderless types (`tooltip`, `splash`, `utility`,
                `dock`) instead map to a native window class via
                `MacWindowStyle`, so the popup gets a real system shadow and no
                titlebar; other values keep the default chrome.

            topmost (bool):
                Specifies whether this is a topmost window (displays above all
                other windows). Internally, this processed by the window as
                `Toplevel.attributes('-topmost', 1)`.

            tool_window (bool):
                On Windows, specifies a toolwindow style. Internally, this is
                processed as `Toplevel.attributes('-toolwindow', 1)`. (Renamed
                from `toolwindow` in 2.0.)

            iconify (bool):
                If True, the window starts minimized (iconified). Internally
                this calls `Toplevel.iconify`.

            alpha (float):
                Sets the window's alpha transparency level (1.0 is opaque).
                Applied immediately via `Toplevel.attributes('-alpha', alpha)`,
                except on X11 where it is deferred until the window becomes
                visible.

            **kwargs (Dict):
                Other optional keyword arguments.
        """
        # Accept the pre-2.0 raw-Tk kwarg spellings with a deprecation warning.
        aliases = normalize_window_kwargs(kwargs)
        override_redirect = aliases.get("override_redirect", override_redirect)
        window_type = aliases.get("window_type", window_type)
        tool_window = aliases.get("tool_window", tool_window)

        super().__init__(**kwargs)
        self.winsys: str = utility.windowing_system(self)

        # On aqua, give a borderless popup type (tooltip/splash/...) a native
        # macOS window class instead of the default chrome, so it isn't drawn
        # with a titlebar. This must run on a freshly-created, never-mapped
        # window -- before the icon/geometry setup below pumps the event loop --
        # or Tk silently ignores it.
        if window_type is not None:
            self._apply_mac_window_style(window_type)

        # Toplevel subclasses tkinter.Toplevel directly (not the AutoStyleMixin
        # tk.Toplevel), so paint it with the active theme at construction --
        # otherwise it shows the native background until the next theme switch.
        Bootstyle.update_tk_widget_style(self)
        Bootstyle.stamp_theme_version(self)

        # A Toplevel inherits the application icon by default (iconphoto='');
        # pass default_data=None so '' means "inherit", not "brand icon".
        self._setup_icon(iconphoto, default_data=None)
        self.title(title)
        self._apply_geometry(size, position)
        self._apply_constraints(minsize, maxsize, resizable)

        if iconify:
            self.iconify()

        if transient is not None:
            self.transient(transient)

        if override_redirect:
            self.overrideredirect(1)

        if window_type is not None and self.winsys == 'x11':
            self.attributes("-type", window_type)

        if topmost:
            self.attributes("-topmost", 1)

        if tool_window and self.winsys == 'win32':
            self.attributes("-toolwindow", 1)

        self._setup_alpha(alpha)


if __name__ == "__main__":
    root = Window(themename="bootstrap-dark", alpha=0.5, size=(1000, 1000))
    # root.withdraw()
    root.place_window_center()
    # root.deiconify()

    top = Toplevel(title="My Toplevel", alpha=0.4, size=(1000, 1000))
    top.place_window_center()

    root.mainloop()
