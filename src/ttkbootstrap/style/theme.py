import platform
from collections import namedtuple
from typing import Dict, Literal, Optional, Tuple, Union

from PIL import Image, ImageColor, ImageOps
from tkinter.ttk import Style
from tkinter import font as tkFont

from ttkbootstrap.utils import (
    color_utils,
    image_utils, load_asset_image
)
from .legacy_styles import tk_handlers
from .themed_styles import ttk_handlers
from ..exceptions import StyleHandlerNotFoundError
from ..logger import logger

DEFAULT_COLOR_1 = '#ddd'
DEFAULT_COLOR_2 = '#111'
SHADE_VALUES = [1.4, 1.3, 1.2, 1.1, 1.0, 0.9, 0.8, 0.7, 0.6]

Shades = namedtuple('Shades', 'l4 l3 l2 l1 base d1 d2 d3 d4')
ThemeMode = Literal['light', 'dark']
ThemeColor = Literal[
    'primary', 'secondary', 'success', 'info', 'warning', 'danger', 'light', 'dark', 'surface', 'background', 'foreground', 'border']
ThemeColors = Dict[str, str]

from typing import NamedTuple


class ColorPair(NamedTuple):
    color: str
    on_color: str


class ColorStates(NamedTuple):
    normal: ColorPair
    hover: ColorPair
    pressed: ColorPair
    selected: ColorPair
    disabled: ColorPair
    focused: ColorPair


class Theme:
    def __init__(
        self,
        name: str,
        mode: ThemeMode = 'light',
        *,
        primary: Tuple[str, str],
        secondary: Tuple[str, str],
        success: Tuple[str, str],
        info: Tuple[str, str],
        warning: Tuple[str, str],
        danger: Tuple[str, str],
        light: Tuple[str, str],
        dark: Tuple[str, str],
        surface: Tuple[str, str],
    ):
        self.ttk = Style()
        self.activated = False
        self.handlers = {}
        self.styles = set()
        self.assets = {}

        self.name = name
        self.mode = mode

        self.primary = ColorPair(*primary)
        self.secondary = ColorPair(*secondary)
        self.success = ColorPair(*success)
        self.info = ColorPair(*info)
        self.warning = ColorPair(*warning)
        self.danger = ColorPair(*danger)
        self.light = ColorPair(*light)
        self.dark = ColorPair(*dark)
        self.surface = ColorPair(*surface)
        self.background = self.surface.color
        self.foreground = self.surface.on_color

        tkFont.nametofont('TkDefaultFont').configure(size=12)

        for name, handler in tk_handlers:
            self.add_handler(name, handler(self))
        for name, handler in ttk_handlers:
            self.add_handler(name, handler(self))

    def __iter__(self):
        copy = self.__dict__.copy()
        for key in ['name', 'mode']: copy.pop(key, None)
        return iter(copy)

    def __repr__(self):
        return str(self.__dict__)

    def has_style(self, name: str):
        return name in self.styles

    def add_style(self, name: str):
        self.styles.add(name)

    def configure(self, style: str, **kwargs):
        return self.ttk.configure(style, **kwargs)

    def map(self, style: str, **options):
        self.ttk.map(style, **options)

    @property
    def colors(self):
        return {
            "primary": self.primary,
            "secondary": self.secondary,
            "success": self.success,
            "info": self.info,
            "warning": self.warning,
            "danger": self.danger,
            "light": self.light,
            "dark": self.dark,
            "surface": self.surface,
            "default": self.surface
        }

    def get_foreground(self, color_name: str):
        if color_name == 'light': return self.dark
        if color_name == 'dark': return self.light
        if color_name == 'background': return self.foreground
        if color_name == 'foreground': return self.background
        if color_name == 'border': return self.foreground
        return self.foreground if self.is_dark_theme else self.background

    def get_color(self, token: str):
        return self.__dict__.get(token)

    def get_shades(self, color: str) -> Shades:
        value = self.get_color(color) or color
        red, grn, blu = color_utils.color_to_rgb(value, 'hex')
        colors = [
            f'#{int(max(0, min(red * s, 255))):02x}{int(max(0, min(grn * s, 255))):02x}{int(max(0, min(blu * s, 255))):02x}'
            for s in SHADE_VALUES
        ]
        return Shades(*colors)

    def get_input_background(self) -> str:
        base = self.background
        return color_utils.adjust_color_lightness(base, -0.15 if self.is_dark_theme else 0.12)

    def get_input_text_color(self) -> str:
        return color_utils.get_contrast_text_color(self.get_input_background())

    def get_input_border_color(self) -> str:
        bg = self.get_input_background()
        return color_utils.adjust_color_lightness(bg, 0.10 if self.is_dark_theme else -0.08)

    def get_background_style(self, token: str, widget_class: str, **extras):
        """
        Get the background style for a widget, which includes checking for inherited backgrounds.
        Return the generated ttk style.
        """
        background = extras.get('background', None)
        container_bg = self.background
        if background is not None and background != container_bg:
            style = f'{background}.{token}.{widget_class}'  # inherited background style
            container_bg = background
        else:
            style = f'{token}.{widget_class}'
        return container_bg, style

    def _get_default_color_states(self, token: str) -> ColorStates:
        hover_factor = 0.08
        pressed_factor = 0.16
        selected_factor = 0.1
        focused_factor = 0.12
        disabled_factor = 0.3
        foreground_shift = 0.4

        def lighten(c, factor):
            return color_utils.adjust_color_lightness(c, abs(factor))

        def darken(c, factor):
            return color_utils.adjust_color_lightness(c, -abs(factor))

        def adjust(c, factor):
            return lighten(c, factor) if self.is_dark_theme else darken(c, factor)

        def fg_disabled(fg):
            return lighten(fg, foreground_shift) if self.is_light_theme else darken(fg, foreground_shift)

        base: ColorPair = self.colors.get(token)
        adjusted_base_color = base.color

        if token in {"light", "dark"}:
            contrast = color_utils.get_contrast_ratio(base.color, self.surface.color)
            if contrast < 3.0:
                adjusted_base_color = color_utils.adjust_color_for_theme_contrast(
                    base.color, self.surface.color, self.is_dark_theme, min_ratio=3.0
                )

        if (token == "light" and self.is_light_theme) or (token == "dark" and self.is_dark_theme):
            hover_color = lighten(base.color, 0.2)
        else:
            hover_color = adjust(adjusted_base_color, hover_factor)

        return ColorStates(
            normal=base,
            hover=ColorPair(hover_color, base.on_color),
            pressed=ColorPair(adjust(adjusted_base_color, pressed_factor), base.on_color),
            selected=ColorPair(adjust(adjusted_base_color, selected_factor), base.on_color),
            focused=ColorPair(adjust(adjusted_base_color, focused_factor), base.on_color),
            disabled=ColorPair(adjust(adjusted_base_color, disabled_factor), fg_disabled(base.on_color)),
        )

    def _get_outline_color_states(self, token: str, transparent_color: str) -> ColorStates:
        solid = self._get_default_color_states(token)
        base: ColorPair = self.colors.get(token)

        def lighten(c, factor): return color_utils.adjust_color_lightness(c, abs(factor))

        def darken(c, factor): return color_utils.adjust_color_lightness(c, -abs(factor))

        def fg_disabled(fg): return lighten(fg, 0.4) if self.is_light_theme else darken(fg, 0.4)

        return ColorStates(
            normal=ColorPair(transparent_color, base.color),
            hover=solid.hover,
            pressed=solid.pressed,
            selected=solid.selected,
            focused=solid.focused,
            disabled=ColorPair(transparent_color, fg_disabled(base.color)),
        )

    def _get_text_color_states(self, token: str, transparent_color: str) -> ColorStates:
        base: ColorPair = self.colors.get(token)

        def fg_disabled(fg): return color_utils.adjust_color_lightness(
            fg, 0.4 if self.is_light_theme else -0.4
        )

        def subtle_tint(alpha: float) -> str:
            return color_utils.blend_colors(self.surface.color, base.color, alpha)

        return ColorStates(
            normal=ColorPair(transparent_color, base.color),
            hover=ColorPair(subtle_tint(0.10), base.color),
            pressed=ColorPair(subtle_tint(0.20), base.color),
            selected=ColorPair(subtle_tint(0.18), base.color),
            focused=ColorPair(subtle_tint(0.14), base.color),
            disabled=ColorPair(transparent_color, fg_disabled(base.color)),
        )

    def get_color_states(
        self,
        token: str = "surface",
        variant: Literal["default", "outline", "text"] = "default",
        transparent_color: str = "surface"
    ) -> ColorStates:
        token = "surface" if token == "default" else token
        if variant == "default":
            return self._get_default_color_states(token)
        elif variant == "outline":
            return self._get_outline_color_states(token, transparent_color)
        elif variant == "text":
            return self._get_text_color_states(token, transparent_color)
        else:
            raise ValueError(f"Unsupported variant: {variant}")

    def image_recolor(self, data: Union[str, Image.Image], color: str, overlay: Image.Image = None):
        white = color
        black = "#ffffff" if self.is_light_theme else "#000000"
        return image_utils.image_recolor_map(data, white, black, overlay)

    @property
    def is_dark_theme(self):
        return self.mode == 'dark'

    @property
    def is_light_theme(self):
        return self.mode == 'light'

    @property
    def system(self):
        return platform.system()

    def initialize(self):
        pass

    def add_handler(self, name, handler):
        self.handlers[name] = handler

    def get_handler(self, name):
        if name not in self.handlers:
            raise StyleHandlerNotFoundError(name)
        return self.handlers[name]

    def register_asset(self, name, data):
        self.assets[name] = data

    def execute_handler(self, name, *args, **extras) -> str:
        if name not in self.handlers:
            logger.error('ThemeBuilder', f'Style handler {name} not found.')
            return ''
        return self.handlers[name].invoke(*args, **extras)

    def recolor_state_image(self, image_path: str, color: str):
        """Create a state image for the button"""
        img = load_asset_image(image_path)
        recolored = self.image_recolor(img, color)
        self.register_asset(str(recolored), recolored)
        return recolored
