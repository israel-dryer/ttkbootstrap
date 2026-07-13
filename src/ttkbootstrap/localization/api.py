"""Ergonomic localization helpers layered over `MessageCatalog`.

Three dependency-free conveniences on top of the msgcat engine:

- `set_locale(locale)` -- the pre-root locale setter (rides the deferred-config
  seam, so it can be called at the top of a file before `App()` exists).
- `L(src, *args, **kwargs)` -- the universal `_()` idiom: translate then
  Python-`str.format`.
- `LocaleVar` -- a `StringVar` that re-translates itself on `<<LocaleChanged>>`,
  for live language switching on vanilla widgets via `textvariable=`.
"""
import tkinter
import weakref
from typing import Any, Optional

from ttkbootstrap.localization.msgcat import LOCALE_CHANGED, MessageCatalog
from ttkbootstrap.window import get_default_root

# Weak references to the live LocaleVars, plus the roots the dispatcher is bound
# on. `tkinter.Variable` (and a `weakref.ref` to it) is unhashable, so the vars
# are tracked in a dict keyed by id(); each ref's finalizer pops its entry, so a
# dropped LocaleVar leaves the registry with no explicit unbind.
_locale_var_refs: "dict[int, weakref.ref]" = {}
_dispatch_roots: "weakref.WeakSet[tkinter.Misc]" = weakref.WeakSet()


def _dispatch_locale_change(event: Optional[tkinter.Event] = None) -> None:
    """Re-translate every live `LocaleVar` (one root binding drives them all)."""
    for key, ref in list(_locale_var_refs.items()):
        var = ref()
        if var is None:
            continue
        try:
            var._retranslate()
        except tkinter.TclError:
            # the var's interpreter is gone; drop it so we stop retrying
            _locale_var_refs.pop(key, None)


def set_locale(locale: str) -> None:
    """Set the application locale.

    Called **before** ``App()`` exists, the locale is queued and applied when the
    root is created (the intended top-of-file use). If a root already exists it
    applies immediately, emitting ``<<LocaleChanged>>`` so live ``LocaleVar``
    variables re-translate.
    """
    # local import breaks the localization <- utils.config <- style cycle; the
    # seam applies now if a root exists, else queues under "locale".
    from ttkbootstrap.utils import config

    config.defer("locale", lambda: MessageCatalog.locale(locale))


def L(src: str, *args: Any, **kwargs: Any) -> str:
    """Translate `src` for the current locale, then Python-`str.format` it.

    The universal i18n idiom (`_()`), resolved at call time -- correct for the
    common "pick the locale at startup" case. Uses Python `str.format` (`{}` /
    `{0}` / `{name}` fields), sidestepping the Tcl `format` path; for `%`-style
    specifiers use `MessageCatalog.translate` instead.
    """
    return MessageCatalog.translate(src).format(*args, **kwargs)


class LocaleVar(tkinter.StringVar):
    """A `StringVar` that re-translates its source on `<<LocaleChanged>>`.

    Hold a source string and show its translation for the current locale; pass
    it as `textvariable=` to any (vanilla or themed) widget for live language
    switching -- when `set_locale(...)` changes the locale, the variable
    re-translates itself. Format args, if any, are applied with Python
    `str.format` (like `L`).

    Every live `LocaleVar` is driven by a single `<<LocaleChanged>>` binding on
    the application root (where `locale()` generates the event), regardless of
    the variable's own `master`. The registry holds only weak references, so a
    dropped `LocaleVar` is collected without any cleanup call; use
    `stop_tracking()` to opt one out explicitly while keeping it alive.
    """

    def __init__(
        self,
        master: Optional[tkinter.Misc] = None,
        src: str = "",
        *args: Any,
        name: Optional[str] = None,
        **kwargs: Any,
    ):
        self._src = src
        self._args = args
        self._kwargs = kwargs
        super().__init__(master, name=name)
        # Bind the shared dispatcher on the *default root* -- the widget on which
        # locale() generates <<LocaleChanged>> -- not on `master`, which may be a
        # child/Toplevel the event would never reach. One binding per root drives
        # every registered var, so opting out is just leaving the WeakSet (no
        # per-var unbind, which mis-fires across Tk/Python versions).
        root = get_default_root()
        if root not in _dispatch_roots:
            root.bind(LOCALE_CHANGED, _dispatch_locale_change, add="+")
            _dispatch_roots.add(root)
        # ref finalizer pops the entry when this var is collected
        self._key = id(self)
        _locale_var_refs[self._key] = weakref.ref(
            self, lambda _ref, key=self._key: _locale_var_refs.pop(key, None)
        )
        self._retranslate()

    def _retranslate(self, event: Optional[tkinter.Event] = None) -> None:
        self.set(
            MessageCatalog.translate(self._src).format(*self._args, **self._kwargs)
        )

    def set_source(self, src: str, *args: Any, **kwargs: Any) -> None:
        """Replace the source string (and any format args) and re-translate now."""
        self._src = src
        self._args = args
        self._kwargs = kwargs
        self._retranslate()

    def stop_tracking(self) -> None:
        """Stop re-translating on `<<LocaleChanged>>` (leaves it at its current
        value). Also happens automatically when the variable is garbage-collected.
        """
        _locale_var_refs.pop(self._key, None)
