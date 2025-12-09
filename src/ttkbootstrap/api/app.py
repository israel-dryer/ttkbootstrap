"""Public window/toplevel API surface."""

from __future__ import annotations

from ttkbootstrap.runtime._app_context import get_current_app as _get_current_app
from ttkbootstrap.runtime.app import App, AppSettings, Toplevel, Window


def get_current_app() -> App:
    """Return the currently active App instance.

    Raises:
        RuntimeError: If no active App instance is set.
    """
    return _get_current_app()


def get_app_settings() -> AppSettings:
    """Return the settings for current App

    Raises:
        RuntimeError: If no active App instance is set.
    """
    return get_current_app().settings


__all__ = ["Toplevel", "App", "Window", "get_current_app", "get_app_settings"]
