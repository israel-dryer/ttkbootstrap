from __future__ import annotations

import threading

from typing_extensions import Any, ParamSpec, Protocol, TypeVar

from ttkbootstrap.exceptions import BootstyleBuilderError
from ttkbootstrap.style.element import Element, ElementImage
from ttkbootstrap.style.style import Style
from ttkbootstrap.style.theme_provider import ThemeProvider
from ttkbootstrap.style.utility import best_foreground, darken_color, lighten_color, mix_colors, relative_luminance


class BuilderCallable(Protocol):
    def __call__(self, builder: BootstyleBuilder, ttk_style: str, **options: Any) -> None:
        ...


F = TypeVar("F", bound=BuilderCallable)
P = ParamSpec("P")
R = TypeVar("R")


class BootstyleBuilder:
    _builder_registry = {}
    _builder_lock = threading.Lock()

    def __init__(self):
        self._provider = ThemeProvider()
        self._style = Style()

    @property
    def provider(self):
        return self._provider

    @property
    def style(self):
        return self._style

    @property
    def colors(self):
        return self.provider.colors

    @classmethod
    def register_builder(cls, name: str):
        if not isinstance(name, str) or not name:
            raise BootstyleBuilderError("`name` must be a non-empty string")

        def deco(func: F) -> F:
            with cls._builder_lock:
                if not name in cls._builder_registry:
                    cls._builder_registry[name] = func
            return func

        return deco

    def call_builder(self, name: str, ttk_style: str, **options):
        with BootstyleBuilder._builder_lock:
            if name in BootstyleBuilder._builder_registry:
                BootstyleBuilder._builder_registry[name](self, ttk_style, **options)
            else:
                raise BootstyleBuilderError(f"{name} is not a known style builder")

    def map_style(self, ttk_style: str, **options):
        self.style.map(ttk_style, **options)

    def configure_style(self, ttk_style, **kwargs):
        self.style.configure(ttk_style, **kwargs)

    def create_style_element_image(self, element: ElementImage):
        name, args, kwargs = element.build()
        self.style.element_create(name, "image", *args, **kwargs)

    def create_style_layout(self, ttk_style: str, element: Element):
        self.style.layout(ttk_style, [element.spec()])

    # ----- Color Utilities & Transformers -----

    def color(self, token: str, surface: str = None, role="background") -> str:
        """Return a color by name."""
        if '-' in token:
            color, level = token.split('-')
            if len(level) == 1:
                if 'subtle' in token:  # color-subtle
                    return self.subtle(color, surface, role)
                else:
                    # color-1 (elevated color)
                    base = self.colors.get(color)
                    return self.elevate(base, int(level))
            elif len(level) == 2:
                if 'subtle' in token:  # color-subtle-2 (elevated subtle color)
                    base = self.subtle(color, surface, role)
                    return self.elevate(base, int(level[1]))

            if level and len(level) == 1:
                if 'subtle' in token:
                    base = self.subtle(color, surface, role)
                    return self.elevate(base, int(level))
                else:
                    base = self.colors.get(color)
                    return self.elevate(base, int(level))
            elif 'subtle' in token:
                color, _ = token.split('-')
                return self.subtle(color, surface, role)
        return self.colors.get(token)

    def subtle(self, token: str, surface=None, role="background") -> str:
        """Return a subtle instance of this color for background or text."""
        base_color = self.colors.get(token)
        surface_color = surface or self.colors.get('background')

        if role == "text":
            # Less blending to keep text legible, just reduce intensity
            if self.provider.mode == "light":
                return darken_color(base_color, 0.25)
            else:
                return lighten_color(base_color, 0.25)
        else:  # background
            if self.provider.mode == "light":
                return mix_colors(base_color, surface_color, 0.08)
            else:
                return mix_colors(base_color, surface_color, 0.10)

    def hover(self, color):
        return self._state_color(color, "hover")

    def active(self, color):
        return self._state_color(color, "active")

    def focus(self, color):
        return self._state_color(color, "focus")

    def focus_border(self, color):
        lum = relative_luminance(color)
        if self.provider.mode == "dark":
            return lighten_color(color, 0.1)
        else:
            return darken_color(color, 0.2 if lum > 0.5 else 0.1)

    def focus_ring(self, color, surface=None):
        surface = surface or self.color(color)
        lum = relative_luminance(color)
        if self.provider.mode == "dark":
            if lum < 0.3:
                brightened = lighten_color(color, 0.2)
                mixed = mix_colors(brightened, surface, 0.2)
            else:
                mixed = mix_colors(color, surface, 0.3)
        else:
            if lum > 0.5:
                blended = mix_colors(color, surface, 0.2)
                mixed = darken_color(blended, 0.15)
            else:
                brightened = lighten_color(color, 0.25)
                mixed = mix_colors(brightened, surface, 0.25)
        return mixed

    def border(self, color):
        if self.provider.mode == "dark":
            return lighten_color(color, 0.20)
        else:
            return darken_color(color, 0.20)

    def on_color(self, color):
        background = self.color('background')
        foreground = self.color('foreground')
        return best_foreground(color, [color, background, foreground])

    def disabled(self, role="background"):
        surface = self.color('background')

        if role == "text":
            if self.provider.mode == "light":
                gray = "#6c757d"  # Bootstrap secondary gray
                mix_ratio = 0.35  # Simulate ~65% opacity
            else:
                gray = "#adb5bd"  # Bootstrap muted text on dark
                mix_ratio = 0.25
        elif role == "background":
            if self.provider.mode == "light":
                gray = "#dee2e6"  # Bootstrap border or card background
                mix_ratio = 0.15
            else:
                gray = "#495057"  # Darker gray surface
                mix_ratio = 0.20
        else:
            raise ValueError(f"Invalid role: {role}. Expected 'text' or 'background'.")

        return mix_colors(gray, surface, mix_ratio)

    def elevate(self, color, elevation=0, max_elevation=5):
        if elevation <= 0:
            return color
        blend_target = "#000000" if self.provider.mode == "light" else "#ffffff"
        weight = min(elevation / max_elevation, 1.0) * 0.3
        return mix_colors(blend_target, color, weight)

    @staticmethod
    def _state_color(color, state):
        if state == "focus":
            return color
        delta = {
            "hover": 0.08,
            "active": 0.12,
            "focus": 0.08
        }[state]
        lum = relative_luminance(color)
        if lum < 0.5:
            return lighten_color(color, delta)
        return darken_color(color, delta)
