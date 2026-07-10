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
from typing import Callable, Optional

from ttkbootstrap.constants import NEUTRAL

# key -> zero-arg applier. Ordered so appliers run in the order they were set;
# last write per key wins. Cleared by flush_pending_config() when the root comes
# up, so a queued setter applies to the next root created.
_pending: "OrderedDict[str, Callable[[], None]]" = OrderedDict()

# The default-button color queued before a root existed (kept so the getter can
# report the effective value pre-root); None once applied/never set.
_pending_default_button: Optional[str] = None


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


def default_button(color: Optional[str] = None) -> str:
    """Get or set the fill for a bare (no-`bootstyle`) Button/Menubutton.

    Called with no argument, returns the current effective default. Called with a
    color name (e.g. ``"primary"``, ``"neutral"``), sets it:

    - **Before the app root exists** the setting is queued and applied when the
      root is created -- the intended use, at the top of a file.
    - **If the root already exists** it is set for buttons built *after* this
      call (existing buttons are not restyled) and a `UserWarning` is emitted,
      because `default_button` is consumed when a button's base style is first
      built. Pass ``App(default_button=...)`` to style every bare button.
    """
    global _pending_default_button
    style = _style()

    if color is None:
        if style is not None:
            return getattr(style, "default_button", NEUTRAL)
        return _pending_default_button if _pending_default_button is not None else NEUTRAL

    if style is not None:
        style.default_button = color
        warnings.warn(
            "default_button was set after the application root was created; it "
            "affects only Button/Menubutton widgets built after this call. Set "
            "it before creating App() (or pass App(default_button=...)) to style "
            "every bare button.",
            UserWarning,
            stacklevel=2,
        )
    else:
        _pending_default_button = color
        defer("default_button", _apply_pending_default_button)
    return color


def _apply_pending_default_button() -> None:
    """Flush applier for a pre-root `default_button` setting."""
    global _pending_default_button
    if _pending_default_button is not None:
        _style().default_button = _pending_default_button
        _pending_default_button = None
