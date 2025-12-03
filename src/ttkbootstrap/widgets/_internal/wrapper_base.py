"""Shared base for ttk wrapper widgets with bootstyle and config delegation.

This base class wires up:
- Constructor: delegates to Bootstyle's constructor wrapper for init-time style
  setup, including surface color inheritance and default variants.
- Configure: routes keys annotated via @configure_delegate to their handlers,
  then forwards remaining options to the underlying ttk widget.
- Index access: `w['key']` and `w['key'] = value` work for delegated keys and
  for `style`/`bootstyle` queries.
- Bootstyle handler: implements @configure_delegate('bootstyle') so runtime
  updates apply via the style engine without monkey-patching ttk.
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
from ttkbootstrap.style.bootstyle_builder_ttk import BootstyleBuilderTTk
from ttkbootstrap.style.style import use_style
from ttkbootstrap.widgets.mixins.configure_mixin import (
    ConfigureDelegationMixin,
    configure_delegate,
)
from ttkbootstrap.widgets.mixins.font_mixin import FontMixin


class TTKWrapperBase(FontMixin, ConfigureDelegationMixin):
    """Base class for all ttk wrapper widgets.

    Subclasses must set `_ttk_base` to the underlying ttk class and inherit
    from that ttk class as well (MRO: WrapperBase, ttk.Class).

    Includes FontMixin for font modifier syntax support.
    """

    _ttk_base: type

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # type: ignore[override]
        font_value = self._init_font_mixin(kwargs)
        init_wrapper = Bootstyle.override_ttk_widget_constructor(self._ttk_base.__init__)  # type: ignore[attr-defined]
        init_wrapper(self, *args, **kwargs)
        if font_value is not None:
            self._delegate_font(font_value)

    def configure(self, cnf: Any | None = None, **kwargs: Any):  # type: ignore[override]
        # First, route custom keys via delegation
        if kwargs:
            for _k in list(kwargs.keys()):
                if _k in self._configure_delegate_map:
                    if self._config_delegate_set(_k, kwargs[_k]):
                        kwargs.pop(_k, None)

        # Getter path for delegated keys
        if isinstance(cnf, str) and cnf in self._configure_delegate_map:
            handled, value = self._config_delegate_get(cnf)
            if handled:
                return value

        # Forward remaining options directly to ttk
        return self._ttk_base.configure(self, cnf, **kwargs)  # type: ignore[misc]

    # tk alias
    config = configure

    # Indexing support: delegate custom keys; handle style/bootstyle queries
    def __setitem__(self, key: str, value: Any) -> None:  # noqa: D401
        if key in getattr(self, "_configure_delegate_map", {}):
            self._config_delegate_set(key, value)
            return None
        if key in ("bootstyle", "style") and getattr(self, "__class__", None).__name__ != "OptionMenu":
            return self.configure(**{key: value})
        return self._ttk_base.__setitem__(self, key, value)  # type: ignore[misc]

    def __getitem__(self, key: str) -> Any:  # noqa: D401
        if key in getattr(self, "_configure_delegate_map", {}):
            handled, value = self._config_delegate_get(key)
            if handled:
                return value
        if key in ("bootstyle", "style") and getattr(self, "__class__", None).__name__ != "OptionMenu":
            return self.configure(cnf=key)
        return self._ttk_base.__getitem__(self, key)  # type: ignore[misc]

    def _rebuild_style(self, style_options: dict[str, Any] | None = None):
        """Recreate the widget's current style with updated style options.

        This is useful when runtime style_options change (e.g., showing/hiding
        dropdown chevrons) and you need the builder to regenerate assets.
        """
        style_name = self.cget("style") or self.winfo_class()
        style_instance = use_style()
        if style_instance is None:
            return

        widget_class = self.winfo_class()
        color = extract_color_from_style(style_name, default=None)
        variant = extract_variant_from_style(style_name) or BootstyleBuilderTTk.get_default_variant(widget_class)

        style_instance.create_style(
            widget_class=widget_class,
            variant=variant,
            ttk_style=style_name,
            color=color,
            options=style_options or {},
        )

    # ----- Built-in delegated handlers -----
    @configure_delegate("bootstyle")
    def _delegate_bootstyle(self, value: Any = None):
        """Get or set the ttkbootstrap bootstyle for this widget.

        - Query: returns a best-effort "color-variant" string based on the
          current style (or None if not set).
        - Set: generates/apply a ttk style using the style engine; preserves
          surface color and orientation when applicable.
        """
        # Query path
        if value is None:
            current_style = self._ttk_base.cget(self, "style")  # type: ignore[misc]
            if not current_style:
                return None
            color = extract_color_from_style(current_style, default=None)
            variant = extract_variant_from_style(current_style)
            parts = []
            if color:
                parts.append(color)
            if variant:
                parts.append(variant)
            return "-".join(parts) if parts else None

        # Set path
        widget_class = self.winfo_class()
        style_options: dict[str, Any] = {}

        surface = getattr(self, "_surface_color", None)
        if surface and surface != "background":
            style_options["surface_color"] = surface

        if widget_class in ORIENT_CLASSES:
            try:
                style_options["orient"] = str(self.cget("orient"))
            except Exception:
                pass

        ttk_style = Bootstyle.create_ttk_style(
            widget_class=widget_class,
            bootstyle=str(value),
            style_options=style_options or None,
        )
        return self._ttk_base.configure(self, style=ttk_style)  # type: ignore[misc]


__all__ = ["TTKWrapperBase"]
