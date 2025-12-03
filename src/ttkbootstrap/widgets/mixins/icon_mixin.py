"""Icon mixin for widgets that support theme-aware icons.

Provides a `@configure_delegate('icon')` handler that applies an icon through
the style system and preserves current bootstyle tokens, orientation, and
surface color where applicable.
"""

from __future__ import annotations

from typing import Any

from ttkbootstrap.widgets.mixins.configure_mixin import configure_delegate


class IconMixin:
    """Adds `icon` configuration support via the style engine."""

    @configure_delegate("icon")
    def _delegate_icon(self, value: Any = None):
        # Query path
        if value is None:
            return getattr(self, "_tb_icon_spec", None)

        # Persist icon for subsequent queries
        setattr(self, "_tb_icon_spec", value)

        return self._rebuild_style({"icon": value})  # type: ignore[attr-defined]


__all__ = ["IconMixin"]

