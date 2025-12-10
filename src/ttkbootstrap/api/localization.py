"""Localization API for ttkbootstrap.

This module provides the public API for internationalization and localization,
including message translation and locale-aware value formatting.
"""

from ttkbootstrap.core.localization.msgcat import MessageCatalog
from ttkbootstrap.core.localization.specs import L, LV

__all__ = [
    "MessageCatalog",
    "L",
    "LV",
]