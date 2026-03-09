"""Public application and window API surface.

Application, window management, menu, and shortcuts functionality.
"""

from __future__ import annotations

from ttkbootstrap.runtime.app import App, AppSettings, Window, get_app_settings, get_current_app
from ttkbootstrap.runtime.toplevel import Toplevel
from ttkbootstrap.runtime.menu import MenuManager, create_menu
from ttkbootstrap.runtime.shortcuts import Shortcuts, Shortcut, get_shortcuts
from ttkbootstrap.widgets.composites.appshell import AppShell

__all__ = [
    # Application
    "App",
    "AppShell",
    "Window",
    "Toplevel",
    "AppSettings",
    "get_current_app",
    "get_app_settings",
    # Menu
    "MenuManager",
    "create_menu",
    # Shortcuts
    "Shortcuts",
    "Shortcut",
    "get_shortcuts",
]
