"""Themed top-level window for secondary application windows."""
from __future__ import annotations

import tkinter
from typing import Any, Optional, Tuple

from ttkbootstrap.core.mixins.widget import WidgetCapabilitiesMixin
from ttkbootstrap.runtime.base_window import BaseWindow


class Toplevel(BaseWindow, WidgetCapabilitiesMixin, tkinter.Toplevel):
    """A themed top-level window.

    Wraps `tkinter.Toplevel` and adds ttkbootstrap window conveniences
    (title/geometry helpers, centering, alpha/topmost/toolwindow helpers,
    transient/override-redirect handling). The standard widget API (events,
    scheduling, clipboard, geometry managers, winfo, etc.) is inherited
    from `BaseWindow` and `WidgetCapabilitiesMixin`.

    Platform:
        On Windows, `toolwindow`, `alpha`, and `window_style` use platform
        attributes (`-toolwindow`, `-alpha`, pywinstyles); the latter
        accepts `mica`, `acrylic`, `aero`, `transparent`, `win7`.
        On X11, `windowtype` requests a window-manager type via `-type`.
        On macOS (Aqua), `windowtype` maps to `MacWindowStyle` for
        `tooltip`, `splash`, `utility`, and `dock`; this must be applied
        before the window is mapped, which is handled internally.
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
            window_style: Optional[str] = None,
            **kwargs: Any,
    ) -> None:
        """Initialize a top-level window.

        Args:
            title: The title that appears on the window titlebar.
            icon: A PhotoImage used for the titlebar icon. If None, the default ttkbootstrap icon is used.
            size: Window size as (width, height). Applied via `geometry`.
            position: Window position as (x, y). Applied via `geometry`.
            minsize: Minimum permissible window size as (width, height).
            maxsize: Maximum permissible window size as (width, height).
            resizable: Whether the user may resize the window as (x, y).
            transient: Mark this window as transient for the given master.
            overrideredirect: If True, instruct the window manager to ignore this window.
            windowtype: On X11, request a specific window manager type via `-type`.
            topmost: If True, keep this window above others (`-topmost`).
            toolwindow: On Windows, request a toolwindow style (`-toolwindow`).
            alpha: On Windows, the window alpha transparency (0.0–1.0) via `-alpha`.
            window_style: Windows-only pywinstyles effect. Options include
                'mica', 'acrylic', 'aero', 'transparent', 'win7', etc.
                Defaults to 'mica'. Set to None to disable.
            **kwargs: Other keyword arguments passed to `tkinter.Toplevel`.
        """
        # Extract iconify kwarg if present
        iconify = kwargs.pop("iconify", None)

        # Initialize Toplevel
        tkinter.Toplevel.__init__(self, **kwargs)

        # Setup window system info
        self.winsys: str = self.tk.call("tk", "windowingsystem")

        # Apply Aqua MacWindowStyle BEFORE any setup that might pump the
        # event loop (icons, geometry, update_idletasks). Tk's docs require
        # the style to be set on a freshly-created, never-mapped window;
        # after the first event-loop trip the call silently has no effect
        # and the window keeps its default chrome. We withdraw immediately
        # so the window is unmapped, set the style, then continue.
        self.withdraw()
        if windowtype is not None and self.winsys == "aqua":
            aqua_style = {
                "tooltip": ("help", "none"),
                "splash": ("plain", "none"),
                "utility": ("utility", "none"),
                "dock": ("plain", "none"),
            }.get(windowtype)
            if aqua_style is not None:
                try:
                    self.tk.call(
                        "::tk::unsupported::MacWindowStyle", "style",
                        self, aqua_style[0], aqua_style[1],
                    )
                except tkinter.TclError:
                    pass

        # Setup icon (use default ttkbootstrap icon if no icon provided)
        self._setup_icon(icon, default_icon_enabled=True)

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
            alpha=alpha,
            window_style=window_style,
        )

        # Handle iconify
        if iconify:
            self.iconify()

        # X11 -type attribute. The Aqua case was handled before
        # _setup_window above (style must be set pre-map).
        if windowtype is not None and self.winsys == "x11":
            self.attributes("-type", windowtype)

        if topmost:
            self.attributes("-topmost", 1)

        if toolwindow and self.winsys == "win32":
            self.attributes("-toolwindow", 1)
