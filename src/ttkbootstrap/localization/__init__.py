"""Localization package: msgcat-based message catalog and built-in locale data."""
from ttkbootstrap.localization.msgs import initialize_localities
from ttkbootstrap.localization.msgcat import MessageCatalog
from ttkbootstrap.localization.api import L, LocaleVar, set_locale

__all__ = [
    "initialize_localities",
    "MessageCatalog",
    "L",
    "LocaleVar",
    "set_locale",
]
