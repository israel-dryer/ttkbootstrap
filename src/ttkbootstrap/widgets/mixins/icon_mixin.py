"""Icon mixin for widgets that support theme-aware icons.

Provides a `@configure_delegate('icon')` handler that applies an icon through
the style system and preserves current bootstyle tokens, orientation, and
surface color where applicable.
"""

from __future__ import annotations

from typing import Any
from tkinter import ttk

from ttkbootstrap.style.bootstyle import (
    Bootstyle,
    extract_color_from_style,
    extract_variant_from_style,
)
from ttkbootstrap.style.token_maps import ORIENT_CLASSES
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

        widget_class = self.winfo_class()
        style_options: dict[str, Any] = {"icon": value}

        # Preserve surface color
        surface = getattr(self, "_surface_color", None)
        if surface and surface != "background":
            style_options["surface_color"] = surface

        # Preserve orientation for oriented widgets
        if widget_class in ORIENT_CLASSES:
            try:
                style_options["orient"] = str(self.cget("orient"))
            except Exception:
                pass

        # Determine current bootstyle tokens if any
        base = getattr(self, "_ttk_base", ttk.Widget)
        try:
            current_style = base.cget(self, "style")  # type: ignore[misc]
        except Exception:
            current_style = None

        color = extract_color_from_style(current_style, default=None) if current_style else None
        variant = extract_variant_from_style(current_style) if current_style else None
        tokens = [t for t in (color, variant) if t]
        bootstyle = "-".join(tokens) if tokens else None

        ttk_style = Bootstyle.create_ttk_style(
            widget_class=widget_class,
            bootstyle=bootstyle,
            style_options=style_options or None,
        )

        # Apply via base ttk to avoid re-entry into wrapper configure
        return base.configure(self, style=ttk_style)  # type: ignore[misc]


__all__ = ["IconMixin"]

