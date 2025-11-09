from __future__ import annotations

import threading
from typing import Callable, Dict, Optional

from typing_extensions import Any, Protocol

from ttkbootstrap.style.bootstyle_base import BootstyleBase
from ttkbootstrap.style.theme_provider import ThemeProvider


class TkBuilderCallable(Protocol):
    def __call__(self, builder: "BootstyleBuilderTk", widget: Any, **options: Any) -> None:  # noqa: ANN401
        ...


class BootstyleBuilderTk(BootstyleBase):
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
        super().__init__(theme_provider, style_instance)

    # Color utilities and provider/colors properties are inherited from BootstyleBase

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
