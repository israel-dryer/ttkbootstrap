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

from ttkbootstrap.style.bootstyle import (
    Bootstyle,
    extract_color_from_style,
    extract_variant_from_style,
)
from ttkbootstrap.style.token_maps import ORIENT_CLASSES
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

    def rebuild_style(self):
        """Recreate the widget's current style with updated style options.

        This is useful when runtime style_options change (e.g., showing/hiding
        dropdown chevrons) and you need the builder to regenerate assets.

        Generates a new style name with the correct hash based on the new
        style_options, then applies it to the widget.

        NOTE: Style options are updated via the `style_options()` method.
        """
        widget_class = self.winfo_class()

        style_options = getattr(self, '_style_options', {})

        # Extract current bootstyle tokens from the current style
        current_style = self._ttk_base.cget(self, "style")  # type: ignore[misc]
        color = extract_color_from_style(current_style, default=None) if current_style else None
        variant = extract_variant_from_style(current_style) if current_style else None
        tokens = [t for t in (color, variant) if t]

        # If we have style_options but no color/variant tokens, we still need to
        # create a custom style. Pass widget_class as bootstyle to prevent early return.
        if tokens:
            bootstyle = "-".join(tokens)
        elif style_options:
            bootstyle = widget_class  # Trigger custom style creation even without color/variant
        else:
            bootstyle = None

        # Preserve surface_color and orientation in style_options
        if not style_options:
            style_options = {}
        surface = getattr(self, "_surface_color", None)
        if surface and surface != "background":
            style_options["surface_color"] = surface
        if widget_class in ORIENT_CLASSES:
            try:
                style_options["orient"] = str(self.cget("orient"))
            except Exception:
                pass

        # Generate NEW style name with NEW hash based on new options
        ttk_style = Bootstyle.create_ttk_style(
            widget_class=widget_class,
            bootstyle=bootstyle,
            style_options=style_options or None,
        )

        # Apply the new style
        return self._ttk_base.configure(self, style=ttk_style)  # type: ignore[misc]

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
        # Use stored style_options if available, otherwise create new dict
        style_options = getattr(self, '_style_options', {}).copy()

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

    def configure_style_options(self, value=None, **kwargs):
        """Get or set the widget style options if handled by the widget's style builder."""
        options = getattr(self, "_style_options", {})
        if value is None:
            options.update(**kwargs)
            setattr(self, "_style_options", options)
            return None
        else:
            return options.get(value, None)

    def _capture_style_options(self, options: list[str] = None, source: Any = None):
        """Extract options from a dictionary source.

        This method should be called before `super()` to capture the style options when they are explicitly exposed as
        keyword arguments instead of being passed indirectly in the `style_options` parameter.

        This method will also attempt to extract the style_options argument if provided.

        Parameters:
            options: A list of options to extract.
            source: The dictionary of keyword arguments to extract from.

        Returns:
            A dict of style options. e.g. {"icon_only": True, "icon": "bootstrap-fill"}.
        """
        if source is None:
            return {}

        style_options = source.pop("style_options", {})

        captured = {}
        for option in options:
            if option in source:
                captured[option] = source.pop(option)
        if captured:
            style_options.update(**captured)

        return style_options


__all__ = ["TTKWrapperBase"]
