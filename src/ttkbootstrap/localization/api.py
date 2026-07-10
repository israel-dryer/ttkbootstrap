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
from typing import Any, Optional

from ttkbootstrap.localization.msgcat import LOCALE_CHANGED, MessageCatalog
from ttkbootstrap.window import get_default_root


def set_locale(locale: str) -> None:
    """Set the application locale.

    Called **before** `App()` exists, the locale is queued and applied when the
    root is created (the intended top-of-file use). If a root already exists it
    applies immediately, emitting `<<LocaleChanged>>` so live `LocaleVar`s
    re-translate.
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

    The variable tracks the locale for its whole lifetime. If it outlives the
    widgets that use it, call `stop_tracking()` to release the binding.
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
        # Bind on the root (where locale() generates the event) rather than
        # bind_all, so the binding is scoped and removable by funcid.
        self._root = master or get_default_root()
        self._bind_id: Optional[str] = self._root.bind(
            LOCALE_CHANGED, self._retranslate, add="+"
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
        """Stop re-translating on `<<LocaleChanged>>` (releases the binding)."""
        if self._bind_id is not None:
            self._root.unbind(LOCALE_CHANGED, self._bind_id)
            self._bind_id = None
