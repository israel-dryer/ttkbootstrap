from __future__ import annotations

import re
from collections.abc import Sequence
from typing import List, Optional, Tuple, Union

from typing_extensions import Any, TypedDict

from ttkbootstrap_icons_bs import BootstrapIcon
from ttkbootstrap.style.theme_provider import ThemeProvider, use_theme
from ttkbootstrap.style.utility import best_foreground, color_to_hsl, darken_color, lighten_color, mix_colors, \
    relative_luminance
from ttkbootstrap.runtime.utility import scale_size


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

    _RE_TOKEN = re.compile(r"^\s*(?P<head>[a-zA-Z_][\w-]*)(?P<brackets>(?:\[[^]]*])*)\s*$")

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
        """Parse a color token into head and ordered list of modifiers.

        Returns a dict with:
            - head: The base color name (e.g., "primary")
            - modifiers: List of (type, value) tuples in order
        """
        m = self._RE_TOKEN.match(token)
        if not m:
            return None

        head = m.group("head")
        brackets_raw = m.group("brackets")

        modifiers = []  # List of (type, value) tuples in order

        if brackets_raw:
            # Extract all bracket contents: [content1][content2] -> ["content1", "content2"]
            bracket_contents = re.findall(r'\[([^]]*)]', brackets_raw)

            # Process each bracket in order for pipeline
            for bracket in bracket_contents:
                part = bracket.strip().lower()
                if not part:
                    continue

                if part.isdigit():
                    modifiers.append(("shade", int(part)))
                elif re.fullmatch(r'[+-]\s*\d+', part):
                    rel = int(part.replace(" ", ""))
                    modifiers.append(("elevation", rel))
                elif part == "subtle":
                    modifiers.append(("subtle", None))
                elif part == "muted":
                    modifiers.append(("muted", None))

        return {"head": head, "modifiers": modifiers}

    def color(self, token: str, surface: str | None = None, role: str = "background") -> str:
        """Resolve a color token with optional chained modifiers.

        Modifiers are applied as a pipeline from left to right:
        - primary[100][muted] → lookup primary[100], then apply muted
        - background[+1][muted] → lookup background, elevate it, then apply muted

        Args:
            token: Color token (e.g., "primary", "primary[100][muted]")
            surface: Optional surface color for subtle modifier
            role: Role for subtle modifier ("background" or "text")

        Returns:
            The resolved color value as a hex string
        """
        # Fast path: exact key (e.g., "blue[100]" or "primary")
        direct = self.colors.get(token)
        if direct is not None:
            return direct

        parsed = self._parse_color_token(token)
        if not parsed:
            return self.colors.get(token)

        head = parsed["head"]
        modifiers = parsed["modifiers"]

        # Determine base lookup key
        # If first modifier is a shade, use it for lookup and remove from pipeline
        base_key = head
        if modifiers and modifiers[0][0] == "shade":
            shade_value = modifiers[0][1]
            base_key = f"{head}[{shade_value}]"
            modifiers = modifiers[1:]  # Remove shade from pipeline

        # Get the base color
        current_color = self.colors.get(base_key)
        if current_color is None:
            # Unknown base; fall back
            return self.colors.get(token)

        # Apply each modifier in order as a pipeline transformation
        for mod_type, mod_value in modifiers:
            if mod_type == "elevation":
                current_color = self.elevate(current_color, mod_value)
            elif mod_type == "subtle":
                # Subtle needs special handling - it does its own lookup
                # Use the base_key for lookup, not the current transformed color
                current_color = self.subtle(base_key, surface, role)
            elif mod_type == "muted":
                # Muted transforms whatever color we currently have
                current_color = self.muted_foreground(current_color)

        return current_color

    def subtle(self, token: str, surface: str | None = None, role: str = "background") -> str:
        """Return a subtle instance of this color for background or text."""
        # Parse token to handle compound tokens like 'primary[subtle]' or 'primary[100]'
        parsed = self._parse_color_token(token)
        if parsed:
            base_key = parsed["head"]
            # If first modifier is a shade, include it in the lookup key
            modifiers = parsed["modifiers"]
            if modifiers and modifiers[0][0] == "shade":
                base_key = f"{base_key}[{modifiers[0][1]}]"
            base_color = self.colors.get(base_key)
        else:
            base_color = self.colors.get(token)

        # Fallback if lookup failed
        if base_color is None:
            base_color = self.colors.get(token) or self.colors.get('foreground')

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

    def selected(self, color: str) -> str:
        return self._state_color(color, "selected")

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

    def focus_inner(self, fill: str) -> str:
        """Internal focus line (2–3px), slightly brighter but not glowy."""
        from ttkbootstrap.style.utility import contrast_ratio, hex_to_rgb

        on = self.on_color(fill)

        # Brighter defaults
        w = 0.26 if self.provider.mode == "light" else 0.20
        ring = mix_colors(on, fill, w)

        # If still not distinct enough, bump once (bounded)
        try:
            bg = hex_to_rgb(fill)
            fg = hex_to_rgb(ring)
            if contrast_ratio(bg, fg) < 2.4:
                w2 = min(w + 0.08, 0.34 if self.provider.mode == "light" else 0.28)
                ring = mix_colors(on, fill, w2)
        except Exception:
            pass

        return ring

    def border(self, color: str) -> str:
        if self.provider.mode == "dark":
            return lighten_color(color, 0.20)
        else:
            return darken_color(color, 0.20)

    def on_color(self, color: str) -> str:
        """Return a readable foreground color for the given background.

        This is intentionally biased so that *dark-ish* accents get light
        text rather than the mathematically highest-contrast dark text,
        which tends to look wrong on buttons and pills.
        """
        background = self.color("background")
        foreground = self.color("foreground")

        try:
            lum = relative_luminance(color)
        except Exception:
            candidates = [foreground, background, "#000000", "#ffffff"]
            return best_foreground(color, candidates)

        # Optional HSL-based accent detection to handle saturated mid-tone
        # colors (like teal) that visually need light text even when their
        # raw luminance is not very low.
        hue = sat = hsl_lum = None
        try:
            hue, sat, hsl_lum = color_to_hsl(color, model="hex")
        except Exception:
            pass

        if self.provider.mode == "light":
            accent_force_light = False
            if hue is not None and sat is not None and hsl_lum is not None:
                # Treat saturated accents as needing light text when they are
                # not extremely light overall. This catches teal/cyan/etc. but
                # avoids triggering on near-white tinted backgrounds.
                if sat >= 40 and hsl_lum <= 80:
                    # Strong teal/cyan/blue band (e.g., teal[600], cyan[600])
                    if 140 <= hue <= 220:
                        accent_force_light = True
                    # Other saturated accents, excluding the yellow/orange band,
                    # when not extremely light.
                    elif hsl_lum <= 70 and not (35 <= hue <= 70):
                        accent_force_light = True

            # Saturated accents: force pure white text so contrast decisions
            # don't accidentally favor dark foreground on mid-tone accents.
            if accent_force_light:
                candidates = ["#ffffff"]
            # Anything darker than ~55% luminance is treated as a dark surface:
            # always use light text, even if contrast math slightly prefers dark.
            elif lum <= 0.55:
                candidates = ["#ffffff"]
            # Mid-light colors (e.g., warning/info) can work with either;
            # allow contrast to choose, but still bias toward theme foreground.
            elif lum <= 0.80:
                candidates = [foreground, "#ffffff", "#000000"]
            # Very light backgrounds -> dark text
            else:
                candidates = [foreground, "#000000"]
        else:
            # Dark mode: inverse bias.
            if lum >= 0.75:
                # Very light chips / badges -> dark text
                candidates = ["#000000", foreground]
            elif lum >= 0.45:
                # Mid tones -> let contrast pick, but include light text
                candidates = ["#ffffff", foreground, "#000000"]
            else:
                # Very dark surfaces -> light text
                candidates = ["#ffffff", foreground]

        # Deduplicate and remove empty candidates
        unique: list[str] = []
        for c in candidates:
            if c and c not in unique:
                unique.append(c)

        return best_foreground(color, unique)

    def muted_foreground(self, background: str, min_contrast: float = 4.5) -> str:
        """Return a muted foreground color with adequate contrast.

        Generates a subdued text color that maintains readability across
        varying backgrounds by ensuring minimum WCAG contrast requirements.

        Args:
            background: The background color to contrast against.
            min_contrast: Minimum WCAG contrast ratio (4.5 for AA, 7.0 for AAA).
                         Default is 4.5 (AA standard for normal text).

        Returns:
            A muted foreground color with adequate contrast against the background.
        """
        from ttkbootstrap.style.utility import hex_to_rgb, contrast_ratio

        lum = relative_luminance(background)
        bg_rgb = hex_to_rgb(background)

        # Determine if we need light or dark muted text
        if lum > 0.5:
            # Light background -> use muted dark text
            base_color = "#495057"  # Dark gray
        else:
            # Dark background -> use muted light text
            base_color = "#adb5bd"  # Light gray

        # Check if base muted color has adequate contrast
        fg_rgb = hex_to_rgb(base_color)
        ratio = contrast_ratio(bg_rgb, fg_rgb)

        if ratio >= min_contrast:
            return base_color

        # If not enough contrast, adjust toward pure black/white
        target = "#000000" if lum > 0.5 else "#ffffff"

        # Binary search for minimum adjustment needed
        for weight in [0.2, 0.4, 0.6, 0.8, 1.0]:
            adjusted = mix_colors(target, base_color, weight)
            adjusted_rgb = hex_to_rgb(adjusted)
            ratio = contrast_ratio(bg_rgb, adjusted_rgb)
            if ratio >= min_contrast:
                return adjusted

        # Fallback to pure contrast
        return target

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
            "selected": 0.18,  # was effectively ~0.10–0.16; bump a bit
            "pressed": 0.12,
            "focus": 0.08,
        }[state]

        # Selected should read as "latched": always darken.
        if state == "selected":
            return darken_color(color, delta)

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
        from ttkbootstrap.runtime.utility import scale_size

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
                icon_obj = BootstrapIcon(name=name, size=size, color=color)  # type: ignore[misc]
            except TypeError:
                icon_obj = BootstrapIcon(name, size, color)  # type: ignore[misc]
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
            if k == 'selected':
                return 'selected !disabled'
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
