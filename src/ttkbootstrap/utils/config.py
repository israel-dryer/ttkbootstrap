"""Deferred-config seam: pre-root setters that queue until the App root exists.

Some settings need a live Tk root but are naturally set at the top of a file,
*before* `App()` is created (the theme's default button today; locale and the
global font in later slices). Rather than each growing its own chicken-and-egg,
they record intent here and `Style` flushes the queue once the root comes up; a
setter applies immediately if a root already exists. Kept deliberately small --
a pending-apply registry, not a config framework.

The `Style` singleton is the true root-bound object (an `App` just creates one),
so the flush hook lives in `Style.__init__`; that covers both `App()` and a bare
`Style()`.
"""
import warnings
from collections import OrderedDict
from typing import Callable

# key -> zero-arg applier. Ordered so appliers run in the order they were set;
# last write per key wins. Cleared by flush_pending_config() when the root comes
# up, so a queued setter applies to the next root created.
_pending: "OrderedDict[str, Callable[[], None]]" = OrderedDict()


def _style():
    """The live `Style` singleton, or None if no root exists yet."""
    # local import breaks the utils <- style import cycle (style imports utils)
    from ttkbootstrap.style import Style

    return Style.get_instance()


def defer(key: str, apply: Callable[[], None]) -> None:
    """Apply `apply` now if a root exists, else queue it under `key`.

    Last write per `key` wins; queued appliers run (in insertion order) when the
    root is created.
    """
    if _style() is not None:
        apply()
    else:
        _pending[key] = apply


def flush_pending_config() -> None:
    """Run and clear every queued applier, in insertion order.

    Called by `Style.__init__` once the root exists (before the base styles are
    built, so a queued `default_button` is in place in time).
    """
    while _pending:
        _key, apply = _pending.popitem(last=False)
        apply()


def set_default_button(color: str) -> None:
    """Set the fill for a bare (no-`bootstyle`) Button/Menubutton.

    - **Before the app root exists** the setting is queued and applied when the
      root is created -- the intended use, at the top of a file.
    - **If the root already exists** it is set for buttons built *after* this
      call (existing buttons are not restyled) and a `UserWarning` is emitted,
      because `default_button` is consumed when a button's base style is first
      built. Pass ``App(default_button=...)`` to style every bare button.

    Read the current value from ``App().style.default_button``.
    """
    style = _style()
    if style is not None:
        style.default_button = color
        warnings.warn(
            "set_default_button() was called after the application root was "
            "created; it affects only Button/Menubutton widgets built after this "
            "call. Set it before creating App() (or pass App(default_button=...)) "
            "to style every bare button.",
            UserWarning,
            stacklevel=2,
        )
    else:
        # Capture `color` in the closure so the queued applier carries its own
        # value -- no shared module-level state to keep in sync.
        defer("default_button", lambda: setattr(_style(), "default_button", color))


def on_theme_change(callback, *, call_now: bool = True):
    """Register ``callback(style)`` to run after every theme change.

    Use it to keep a custom style in sync with the active theme -- the callback
    re-runs on each ``theme_use`` / ``toggle_theme``. Works before the root
    exists: if no ``App``/``Style`` has been created yet, the registration is
    queued and applied when the root comes up. See ``Style.on_theme_change`` for
    the full semantics. Returns ``callback``, so it can be used as a decorator.
    """
    style = _style()
    if style is not None:
        return style.on_theme_change(callback, call_now=call_now)
    # unique key per callback so multiple registrations all survive the queue
    defer(
        f"on_theme_change:{id(callback)}",
        lambda: _style().on_theme_change(callback, call_now=call_now),
    )
    return callback


def theme_aware(callback):
    """Decorator marking ``callback(style)`` as a theme-aware style builder.

    Runs it once when a theme is active -- immediately if the app already
    exists, otherwise at app creation -- and again after every theme change, so
    the style tracks the theme::

        @theme_aware
        def build_styles(style):
            style.configure("Pill.TButton", background=style.colors.primary)
    """
    return on_theme_change(callback, call_now=True)


def remove_theme_change_callback(callback) -> None:
    """Unregister a callback previously passed to ``on_theme_change`` /
    ``theme_aware``.

    Removes it whether it is already live on the ``Style`` or still queued from a
    pre-root registration.
    """
    _pending.pop(f"on_theme_change:{id(callback)}", None)
    style = _style()
    if style is not None:
        style.remove_theme_change_callback(callback)
