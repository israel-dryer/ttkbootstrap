from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .app import App

_current_app: App | None = None


def set_current_app(app: App) -> None:
    """Set the process-wide current App instance.

    Intended to be called from App.__init__ for the first app created.
    """
    global _current_app
    _current_app = app


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
