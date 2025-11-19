from __future__ import annotations

import re
from collections.abc import Sequence
from typing import List, Optional, Tuple, Union

from typing_extensions import Any, TypedDict

from ttkbootstrap.style.theme_provider import ThemeProvider, use_theme
from ttkbootstrap.style.utility import (
    best_foreground,
    darken_color,
    lighten_color,
    mix_colors,
    relative_luminance,
)
from ttkbootstrap.utility import scale_size


class IconSpec(TypedDict, total=False):
    name: str
    size: Optional[int]
    color: Optional[str]
    state: Sequence[tuple[str, str | IconStateMap]]


class IconStateMap(TypedDict, total=False):
    name: Optional[str]
    color: Optional[str]


ForegroundStateSpec = tuple[str, str | dict[str, str]]


class BootstyleBuilderBase:
    """Shared base for TTK and Tk bootstyle builders.

    Centralizes theme provider plumbing and color utilities so both
    BootstyleBuilder (TTK) and BootstyleBuilderTk (Tk) can inherit and
    avoid duplication.
    """

    _RE_TOKEN = re.compile(r"^\s*(?P<head>[a-zA-Z_][\w-]*)(?:\[(?P<mods>[^]]*)])?\s*$")

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

    def active(self, color: str) -> str:
        return self._state_color(color, "active")

    def pressed(self, color: str) -> str:
        return self._state_color(color, "pressed")

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
            "active": 0.08,
            "pressed": 0.12,
            "focus": 0.08,
        }[state]
        lum = relative_luminance(color)
        if lum < 0.5:
            return lighten_color(color, delta)
        return darken_color(color, delta)

    @staticmethod
    def scale(value: Union[int, List, Tuple]):
        return scale_size(value)

    # ----- Icon Utilities -----

    @staticmethod
    def normalize_icon_spec(icon: str | IconSpec, default_size: int = 20) -> IconSpec:
        """
            If the icon is a string, then create a icon spec where the name is known and the size is set to default_size.
            If the there is an icon spec, map the default size if one is not already specified in the spec.

            Icon sizes are automatically scaled based on DPI settings. The default size of 20px provides
            a balanced appearance, being slightly larger than the visible text (16px) but not overwhelming.
        """
        from ttkbootstrap.utility import scale_size

        # Apply DPI scaling to default size
        scaled_default = scale_size(default_size)

        if isinstance(icon, str):
            return dict(name=icon, size=scaled_default)
        else:
            if 'size' not in icon or icon.get('size') is None:
                icon['size'] = scaled_default
            elif icon.get('size'):
                # Scale user-provided size too
                icon['size'] = scale_size(icon['size'])
            return icon

    def map_stateful_icons(self, icon: IconSpec, foreground_spec: Sequence[tuple]):
        """
        Build and return a TTK image state map for icons, using the
        configured icon provider.

        Parameters:
            icon (IconSpec):
                Base icon spec with default `name` and optional `size`/`color`.
                Optional `state` provides per-state overrides where the value
                can be either a string (state-specific icon name) or a dict
                with `name` and/or `color`.

            foreground_spec (Sequence[tuple]):
                A sequence of state → foreground color items computed by the
                builder, e.g.:
                    [
                        ('disabled', '#fafafa'),
                        ('pressed !disabled', '#63f3f3'),
                        ('hover !disabled', '#f2fa5d'),
                    ]

        Behavior:
            - If `icon.color` is provided at the root, use it as the default
              color for all states unless a per-state override is provided.
            - If `icon.color` is not provided, the icon color follows the
              widget's foreground color provided by `foreground_spec`, unless
              a per-state override is provided in `icon.state`.
            - If a per-state override provides `name`, use that icon name for
              the state; otherwise, fallback to the base icon `name`.
            - Identical (name, size, color) combinations reuse the same image.

        Returns:
            list[tuple[str, str]]: List of (state, image_name) tuples suitable
            for `ttk.Style.element_create(..., 'image', default, (state, image) ...)`.
        """
        # Lazy imports to avoid circulars and keep base lightweight
        from ttkbootstrap.appconfig import use_icon_provider

        # Normalize base values
        base_name: str = icon.get('name')  # type: ignore[assignment]
        if not base_name:
            # Nothing we can do without an icon name
            return []

        base_size: int = int(icon.get('size') or 20)
        base_color: str | None = icon.get('color')

        # Build per-state override lookup: {state_str: {'name':..., 'color':...}}
        state_overrides: dict[str, IconStateMap] = {}
        for entry in icon.get('state', []) or []:
            try:
                st, ov = entry  # type: ignore[misc]
            except Exception:
                continue
            if isinstance(ov, str):
                state_overrides[st] = {'name': ov}
            elif isinstance(ov, dict):
                # Only keep known keys
                override: IconStateMap = {}
                if 'name' in ov and ov['name']:
                    override['name'] = ov['name']  # type: ignore[assignment]
                if 'color' in ov and ov['color']:
                    override['color'] = ov['color']  # type: ignore[assignment]
                if override:
                    state_overrides[st] = override

        # Obtain the provider callable (class or function). The provider itself
        # is called as the icon constructor: provider(name, size, color) -> icon
        provider = use_icon_provider()

        def _resolve_fg(value: Any) -> str | None:  # noqa: ANN401
            """Extract a color string from the foreground state spec value."""
            if isinstance(value, str):
                return value
            if isinstance(value, dict):
                # Try common keys in order
                for k in ('foreground', 'text', 'color'):
                    v = value.get(k)
                    if isinstance(v, str):
                        return v
            return None

        # Cache icons by (name, size, color) to avoid duplicates
        cache: dict[tuple[str, int, str | None], Any] = {}

        def _image_for(name: str, size: int, color: str | None):
            key = (name, size, color)
            if key in cache:
                return cache[key]

            # Call the provider directly; it returns an icon object with `.image`
            try:
                icon_obj = provider(name=name, size=size, color=color)  # type: ignore[misc]
            except TypeError:
                icon_obj = provider(name, size, color)  # type: ignore[misc]
            if icon_obj is None:
                return None

            cache[key] = icon_obj.image
            return icon_obj.image

        state_image_specs: list[tuple[str, Any]] = []

        def _match_override(expr: str) -> IconStateMap | None:
            # 1) Exact expression match (e.g., 'hover !disabled')
            if expr in state_overrides:
                return state_overrides[expr]
            # 2) Token match: treat state keywords as tokens; ignore negations like '!disabled'
            tokens = {t for t in expr.split() if t and not t.startswith('!')}
            for key, ov in state_overrides.items():
                if not key:
                    # skip empty-key overrides here; apply only to '' base state
                    continue
                if key in tokens:
                    return ov
            # 3) No match
            return None

        # Build ordered list of states to map
        base_states: list[str] = [s for s, _ in foreground_spec]
        fg_lookup: dict[str, Any] = {s: v for s, v in foreground_spec}

        # Ensure typical derivations for overrides exist (e.g., 'hover' -> 'hover !disabled')
        def _derive_expr(k: str) -> str:
            if not k:
                return ''
            if ' ' in k or '!' in k:
                return k
            if k in ('pressed', 'active'):
                return 'pressed !disabled'
            if k == 'hover':
                return 'hover !disabled'
            return k

        extra_states: list[str] = []
        seen = set(base_states)
        default_present = '' in seen
        if default_present:
            # Exclude default for ordering; add back later
            base_states_no_default = [s for s in base_states if s != '']
        else:
            base_states_no_default = base_states[:]

        # Add override-derived states if not already present
        for k in state_overrides.keys():
            expr = _derive_expr(k)
            if expr not in seen:
                extra_states.append(expr)
                seen.add(expr)

        # Compose final order: base (without ''), then extras, then default ''
        ordered_states = base_states_no_default + extra_states
        if default_present:
            ordered_states.append('')

        for state_expr in ordered_states:
            fg_val = fg_lookup.get(state_expr)
            # Derive per-state name/color
            override = _match_override(state_expr) or {}
            name = override.get('name', base_name)  # type: ignore[assignment]
            # Determine color priority: per-state override > base_color > foreground state color
            color = override.get('color')  # type: ignore[assignment]
            if color is None:
                if base_color is not None:
                    color = base_color
                else:
                    color = _resolve_fg(fg_val)

            # Build or reuse the image
            img_or_photo = _image_for(name, base_size, color)
            if img_or_photo is not None:
                state_image_specs.append((state_expr, img_or_photo))

        return state_image_specs
