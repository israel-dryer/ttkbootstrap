"""
Localization integration for ttkbootstrap.

Exports MessageCatalog, which bridges Tcl msgcat lookups with compiled
gettext (.mo) catalogs built via Babel.
"""
from ttkbootstrap.localization.msgcat import MessageCatalog
from ttkbootstrap.localization.intl_format import IntlFormatter

__all__ = [
    "MessageCatalog",
    "IntlFormatter",
]
