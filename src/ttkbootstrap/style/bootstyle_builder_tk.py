from __future__ import annotations

import threading
from typing import Callable, Dict, Optional

from typing_extensions import Any, Protocol

from ttkbootstrap.style.bootstyle_builder import BootstyleBuilder
from ttkbootstrap.style.theme_provider import ThemeProvider, use_theme


class TkBuilderCallable(Protocol):
    def __call__(self, builder: "BootstyleBuilderTk", widget: Any, **options: Any) -> None:  # noqa: ANN401
        ...


class BootstyleBuilderTk:
    """Builder registry for legacy Tk widgets.

    Mirrors the TTK BootstyleBuilder API, but targets Tk widgets and passes
    the actual widget instance to builder functions.

    Usage:
        >>> @BootstyleBuilderTk.register_builder('Button')
        ... def build_tk_button(builder, widget, **opts):
        ...     bg = builder.color(opts.get('surface_color', 'background'))
        ...     widget.configure(background=bg, foreground=builder.colors.get('foreground'))
    """

    _registry: Dict[str, TkBuilderCallable] = {}
    _lock = threading.Lock()
    _builders_loaded = False

    def __init__(self, theme_provider: Optional[ThemeProvider] = None, style_instance: Optional[Any] = None):  # noqa: ANN401
        # If no provider given, try to derive from style_instance
        if theme_provider is None and style_instance is not None:
            try:
                theme_provider = style_instance.theme_provider  # type: ignore[attr-defined]
            except Exception:
                theme_provider = None
        self._provider = theme_provider or use_theme()
        # Reuse BootstyleBuilder for color utilities
        self._ttk_utils = BootstyleBuilder(theme_provider=self._provider, style_instance=style_instance)

    @property
    def provider(self) -> ThemeProvider:
        return self._provider

    @property
    def colors(self):
        return self._ttk_utils.colors

    # ----- Utility forwards (reuse same color helpers as TTK) -----
    def color(self, token: str, surface: str = None, role: str = "background") -> str:
        return self._ttk_utils.color(token, surface, role)

    def subtle(self, token: str, surface: str = None, role: str = "background") -> str:
        return self._ttk_utils.subtle(token, surface, role)

    def hover(self, color: str) -> str:
        return self._ttk_utils.hover(color)

    def active(self, color: str) -> str:
        return self._ttk_utils.active(color)

    def focus_border(self, color: str) -> str:
        return self._ttk_utils.focus_border(color)

    def focus_ring(self, color: str, surface: str = None) -> str:
        return self._ttk_utils.focus_ring(color, surface)

    def border(self, color: str) -> str:
        return self._ttk_utils.border(color)

    def on_color(self, color: str) -> str:
        return self._ttk_utils.on_color(color)

    def disabled(self, role: str = "background", surface: str = None) -> str:
        return self._ttk_utils.disabled(role=role, surface=surface)

    # ----- Registry API -----
    @classmethod
    def register_builder(cls, widget_name: str):
        """Register a Tk widget builder by Tk class name (e.g., 'Button')."""

        if not isinstance(widget_name, str) or not widget_name:
            raise ValueError("`widget_name` must be a non-empty string")

        def deco(func: TkBuilderCallable) -> TkBuilderCallable:
            with cls._lock:
                cls._registry[widget_name] = func
            return func

        return deco

    @classmethod
    def has_builder(cls, widget_name: str) -> bool:
        cls._ensure_builders_loaded()
        with cls._lock:
            return widget_name in cls._registry

    @classmethod
    def get_registered_widgets(cls) -> list[str]:
        cls._ensure_builders_loaded()
        with cls._lock:
            return list(cls._registry.keys())

    @classmethod
    def _ensure_builders_loaded(cls) -> None:
        # Fast path
        if cls._builders_loaded:
            return
        try:
            import ttkbootstrap.style.builders_tk  # noqa: F401
        except Exception:
            # If not present, that's fine; avoid repeated import attempts
            pass
        finally:
            cls._builders_loaded = True

    def call_builder(self, widget: Any, **options: Any) -> None:  # noqa: ANN401
        """Call a registered builder for this Tk widget instance."""
        # Prefer Tk's class name; fallback to Python class name
        try:
            widget_name = widget.winfo_class()
        except Exception:
            widget_name = widget.__class__.__name__

        # Ensure builder modules are imported
        self._ensure_builders_loaded()

        with self._lock:
            builder_func = self._registry.get(widget_name)

        if builder_func is None:
            # Nothing to do for this Tk widget
            return

        builder_func(self, widget, **options)
