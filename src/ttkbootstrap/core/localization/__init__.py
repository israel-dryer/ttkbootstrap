"""
Localization integration for ttkbootstrap.

Exports MessageCatalog, which bridges Tcl msgcat lookups with compiled
gettext (.mo) catalogs built via Babel.
"""
from .msgcat import MessageCatalog
from .intl_format import IntlFormatter

__all__ = [
    "MessageCatalog",
    "IntlFormatter",
]
