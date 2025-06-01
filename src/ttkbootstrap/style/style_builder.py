from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Union
from tkinter.ttk import Style
from PIL import Image

from ..utils import color_utils, image_utils, load_asset_image
from ..utils.style_utils import ColorPair, ColorStates

if TYPE_CHECKING:
    from .theme import Theme


class StyleBuilder(ABC):
    def __init__(self, theme: "Theme", widget_class: str):
        self.theme = theme
        self.ttk = Style(theme.ttk.master)
        self.widget_class = widget_class

    def invoke(self, token: str, **extras):
        background, style = self._get_style_name(token, self.widget_class, **extras)

        if self._style_already_exists(style):
            return style

        colors = self._generate_color_states(token)
        images = self._build_state_images(colors)
        self._build_layout(style, images)
        self._configure_style(style, background, colors)

        return style

    # === ABSTRACT METHODS ===

    @abstractmethod
    def _generate_color_states(self, token: str):
        ...

    @abstractmethod
    def _build_state_images(self, colors) -> dict[str, str]:
        ...

    @abstractmethod
    def _build_layout(self, style: str, images: dict[str, str]):
        ...

    @abstractmethod
    def _configure_style(self, style: str, background: str, colors):
        ...

    # === CONVENIENCE WRAPPERS ===

    def _configure(self, style: str, **options):
        self.theme.configure(style, **options)

    def _map(self, style: str, **options):
        self.theme.map(style, **options)

    def _add_style(self, style: str):
        self.theme.add_style(style)

    def _style_already_exists(self, style: str) -> bool:
        return self.theme.has_style(style)

    # === IMAGE RECOLORING ===

    def _recolor_state_image(self, image_path: str, color: str):
        img = load_asset_image(image_path)
        recolored = self._image_recolor(img, color)
        self.theme.register_asset(str(recolored), recolored)
        return recolored

    def _recolor_state_image_map(self, image_path: str, white: str, black: str, overlay: Union[Image, None] = None):
        img = load_asset_image(image_path)
        recolored = image_utils.image_recolor_map(img, white, black, overlay)
        self.theme.register_asset(str(recolored), recolored)
        return recolored

    def _image_recolor(self, data: Union[str, Image.Image], color: str, overlay: Image.Image = None) -> Image.Image:
        black = "#ffffff" if self.theme.is_light_theme else "#000000"
        return image_utils.image_recolor_map(data, color, black, overlay)

    # === COLOR STATE GENERATION ===

    def _get_color(self, token: str):
        return self.theme.get_color(token)

    def _get_color_states(self, token: str) -> ColorStates:
        token = "primary" if token == "default" else token
        base = self.theme.get_color(token)
        return self._default_color_states(base, token)

    def _default_color_states(self, base: ColorPair, token: str) -> ColorStates:
        is_dark = self.theme.is_dark_theme
        surface_color = self.theme.background

        def lighten(c, f):
            return color_utils.adjust_color_lightness(c, abs(f))

        def darken(c, f):
            return color_utils.adjust_color_lightness(c, -abs(f))

        def adjust(c, f):
            return lighten(c, f) if is_dark else darken(c, f)

        def fg_disabled(c):
            return lighten(c, 0.4) if not is_dark else darken(c, 0.4)

        adjusted = base.color
        if token in {"light", "dark"}:
            contrast = color_utils.get_contrast_ratio(base.color, surface_color)
            if contrast < 3.0:
                adjusted = color_utils.adjust_color_for_theme_contrast(
                    base.color, surface_color, is_dark, min_ratio=3.0
                )

        hover = lighten(base.color, 0.2) if (token == "light" and not is_dark) or (
            token == "dark" and is_dark) else adjust(adjusted, 0.08)

        return ColorStates(
            normal=base,
            hover=ColorPair(hover, base.on_color),
            pressed=ColorPair(adjust(adjusted, 0.16), base.on_color),
            selected=ColorPair(adjust(adjusted, 0.10), base.on_color),
            focused=ColorPair(adjust(adjusted, 0.12), base.on_color),
            disabled=ColorPair(adjust(adjusted, 0.3), fg_disabled(base.on_color)),
        )

    # === STYLE NAMING ===

    def _get_style_name(self, token: str, widget_class: str, background: str | None = None) -> tuple[str, str]:
        container_bg = self.theme.background
        if background and background != container_bg:
            return background, f"{background}.{token}.{widget_class}"
        return container_bg, f"{token}.{widget_class}"

    # === FOREGROUND/BACKGROUND COMPUTATIONS ===

    def _get_foreground(self, color_name: str) -> str:
        theme = self.theme
        match color_name:
            case "light":
                return theme.dark.color
            case "dark":
                return theme.light.color
            case "background":
                return theme.foreground
            case "foreground":
                return theme.background
            case "border":
                return theme.foreground
            case _:
                return theme.foreground if theme.is_dark_theme else theme.background

    def _get_input_background(self) -> str:
        base = self.theme.background
        return color_utils.adjust_color_lightness(base, -0.15 if self.theme.is_dark_theme else 0.12)

    def _get_input_text_color(self) -> str:
        return color_utils.get_contrast_text_color(self._get_input_background())

    def _get_input_border_color(self) -> str:
        bg = self._get_input_background()
        return color_utils.adjust_color_lightness(bg, 0.10 if self.theme.is_dark_theme else -0.08)

    def _blend_subtle_tint(self, base_color: str, alpha: float) -> str:
        return color_utils.blend_colors(self.theme.surface.color, base_color, alpha)

    def _adjust_for_contrast(self, base_color: str, min_ratio: float = 3.0) -> str:
        surface = self.theme.surface.color
        contrast = color_utils.get_contrast_ratio(base_color, surface)
        if contrast < min_ratio:
            return color_utils.adjust_color_for_theme_contrast(
                base_color, surface, self.theme.is_dark_theme, min_ratio
            )
        return base_color

    def _get_disabled_color(self, fg: str, shift: float = 0.4) -> str:
        return color_utils.adjust_color_lightness(fg, shift if self.theme.is_light_theme else -shift)
