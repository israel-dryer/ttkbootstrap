from __future__ import annotations

import re
from typing_extensions import Any

from ttkbootstrap.style.theme_provider import ThemeProvider, use_theme
from ttkbootstrap.style.utility import (
    best_foreground,
    darken_color,
    lighten_color,
    mix_colors,
    relative_luminance,
)


class BootstyleBase:
    """Shared base for TTK and Tk bootstyle builders.

    Centralizes theme provider plumbing and color utilities so both
    BootstyleBuilder (TTK) and BootstyleBuilderTk (Tk) can inherit and
    avoid duplication.
    """

    _RE_TOKEN = re.compile(r"^\s*(?P<head>[a-zA-Z_][\w-]*)(?:\[(?P<mods>[^\]]*)])?\s*$")

    def __init__(self, theme_provider: ThemeProvider | None = None, style_instance: Any | None = None):  # noqa: ANN401
        # If no provider given, try to derive from style_instance
        if theme_provider is None and style_instance is not None:
            try:
                theme_provider = style_instance.theme_provider  # type: ignore[attr-defined]
            except Exception:
                theme_provider = None
        self._provider = theme_provider or use_theme()
        self._style = style_instance

    def set_style_instance(self, style_instance: Any) -> None:  # noqa: ANN401
        self._style = style_instance

    @property
    def provider(self) -> ThemeProvider:
        return self._provider

    @property
    def style(self) -> Any | None:  # noqa: ANN401
        return self._style

    @property
    def colors(self) -> dict:
        return self.provider.colors

    # ----- Color Utilities & Transformers -----

    def _parse_color_token(self, token: str):
        m = self._RE_TOKEN.match(token)
        if not m:
            return None
        head = m.group("head")
        mods_raw = m.group("mods")
        shade = None
        subtle = False
        rel = 0
        if mods_raw:
            parts = [p.strip().lower() for p in mods_raw.split("|") if p.strip()]
            for p in parts:
                if p.isdigit():
                    shade = int(p)
                elif re.fullmatch(r"[+-]\s*\d+", p):
                    rel += int(p.replace(" ", ""))
                elif p == "subtle":
                    subtle = True
        return {"head": head, "shade": shade, "subtle": subtle, "rel": rel}

    def color(self, token: str, surface: str | None = None, role: str = "background") -> str:
        # Fast path: exact key (e.g., "blue[100]" or "primary")
        direct = self.colors.get(token)
        if direct is not None:
            return direct

        parsed = self._parse_color_token(token)
        if not parsed:
            return self.colors.get(token)

        head = parsed["head"]
        shade = parsed["shade"]
        subtle = parsed["subtle"]
        rel = parsed["rel"]

        # Compose the base *key* exactly how the map stores it
        base_key = f"{head}[{shade}]" if shade is not None else head

        # 1) SUBTLE: pass the *token/key* to subtle() so it can do its own lookup/blend
        if subtle:
            base = self.subtle(base_key, surface, role)
        else:
            # otherwise resolve the base from the map
            base = self.colors.get(base_key)

        if base is None:
            # Unknown base; fall back
            return self.colors.get(token)

        # 2) ELEVATION: apply relative elevation to the resolved color
        if rel:
            base = self.elevate(base, int(rel))

        return base

    def subtle(self, token: str, surface: str | None = None, role: str = "background") -> str:
        """Return a subtle instance of this color for background or text."""
        base_color = self.colors.get(token)
        surface_color = surface or self.colors.get('background')

        if role == "text":
            if self.provider.mode == "light":
                return darken_color(base_color, 0.25)
            else:
                return lighten_color(base_color, 0.25)
        else:  # background
            if self.provider.mode == "light":
                return mix_colors(base_color, surface_color, 0.08)
            else:
                return mix_colors(base_color, surface_color, 0.10)

    def hover(self, color: str) -> str:
        return self._state_color(color, "hover")

    def active(self, color: str) -> str:
        return self._state_color(color, "active")

    def focus(self, color: str) -> str:
        return self._state_color(color, "focus")

    def focus_border(self, color: str) -> str:
        lum = relative_luminance(color)
        if self.provider.mode == "dark":
            return lighten_color(color, 0.1)
        else:
            return darken_color(color, 0.2 if lum > 0.5 else 0.1)

    def focus_ring(self, color: str, surface: str | None = None) -> str:
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

    def border(self, color: str) -> str:
        if self.provider.mode == "dark":
            return lighten_color(color, 0.20)
        else:
            return darken_color(color, 0.20)

    def on_color(self, color: str) -> str:
        background = self.color('background')
        foreground = self.color('foreground')
        return best_foreground(color, [color, background, foreground])

    def disabled(self, role: str = "background", surface: str | None = None) -> str:
        """Return a disabled color mixed with the surface.

        Args:
            role: 'background' for surfaces, 'text' for foregrounds.
            surface: Optional surface color to mix against. If omitted,
                     uses the theme background.
        """
        surface = surface or self.color('background')

        if role == "text":
            if self.provider.mode == "light":
                gray = "#6c757d"
                mix_ratio = 0.35
            else:
                gray = "#adb5bd"
                mix_ratio = 0.25
        elif role == "background":
            if self.provider.mode == "light":
                gray = "#dee2e6"
                mix_ratio = 0.15
            else:
                gray = "#495057"
                mix_ratio = 0.20
        else:
            raise ValueError("Invalid role: {role}. Expected 'text' or 'background'.")

        return mix_colors(gray, surface, mix_ratio)

    def elevate(self, color: str, elevation: int = 0, max_elevation: int = 5) -> str:
        if elevation <= 0:
            return color
        blend_target = "#000000" if self.provider.mode == "light" else "#ffffff"
        weight = min(elevation / max_elevation, 1.0) * 0.3
        return mix_colors(blend_target, color, weight)

    @staticmethod
    def _state_color(color: str, state: str) -> str:
        if state == "focus":
            return color
        delta = {
            "hover": 0.08,
            "active": 0.12,
            "focus": 0.08,
        }[state]
        lum = relative_luminance(color)
        if lum < 0.5:
            return lighten_color(color, delta)
        return darken_color(color, delta)

