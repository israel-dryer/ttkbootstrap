import base64
from io import BytesIO
from math import ceil
import platform
from collections import namedtuple
from typing import Dict, Literal, Optional, Union

from PIL import Image, ImageColor, ImageOps
from PIL.ImageDraw import ImageDraw
from PIL.ImageTk import PhotoImage
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
    'primary', 'secondary', 'success', 'info', 'warning', 'danger', 'light', 'dark', 'background', 'foreground', 'border']
ThemeColors = Dict[str, str]

from typing import NamedTuple


class ColorStates(NamedTuple):
    normal: str
    hover: str
    pressed: str
    selected: str
    disabled: str
    foreground: str
    foreground_hover: str
    foreground_pressed: str
    foreground_selected: str
    foreground_focus: str
    foreground_disabled: str


class Theme:
    def __init__(self, name: str, mode: ThemeMode = 'light', **colors):
        self.ttk = Style()
        self.activated = False
        self.handlers = {}
        self.styles = set()
        self.assets = {}

        self.name = name
        self.mode = mode

        self.primary = colors.get('primary', DEFAULT_COLOR_1)
        self.secondary = colors.get('secondary', DEFAULT_COLOR_1)
        self.success = colors.get('success', DEFAULT_COLOR_1)
        self.info = colors.get('info', DEFAULT_COLOR_1)
        self.warning = colors.get('warning', DEFAULT_COLOR_1)
        self.danger = colors.get('danger', DEFAULT_COLOR_1)
        self.light = colors.get('light', DEFAULT_COLOR_1)
        self.dark = colors.get('dark', DEFAULT_COLOR_1)
        self.background = colors.get('background', DEFAULT_COLOR_1)
        self.foreground = colors.get('foreground', DEFAULT_COLOR_2)
        self.border = colors.get('border', DEFAULT_COLOR_2)

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
            "background": self.background,
            "foreground": self.foreground,
            "border": self.border,
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

    def get_token(self, color: str):
        color_map = self.colors()
        tokens = list(color_map.keys())
        colors = list(color_map.values())
        try:
            return tokens[colors.index(color)]
        except ValueError:
            return None

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

    def get_scrollbar_thumb_colors(self, token: str | None = None):
        """
        Return thumb colors (normal, hover, pressed) based on theme background and primary.
        Uses linear RGB lightness adjustments and blending.
        """
        token = token or "foreground"
        bg = self.get_input_background()
        primary = self.get_color(token)

        # Step 1: base thumb color is contrasty relative to trough
        if self.is_light_theme:
            thumb = color_utils.adjust_color_lightness(bg, -0.3)  # darker thumb on light bg
        else:
            thumb = color_utils.adjust_color_lightness(bg, 0.25)  # lighter thumb on dark bg

        # Step 2: hover and pressed are blends toward primary
        hover = color_utils.blend_colors(thumb, primary, 0.2)
        pressed = color_utils.blend_colors(thumb, primary, 0.4)

        return thumb, hover, pressed

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

    def get_color_states(
        self,
        base_color: str,
        variant: Literal["default", "outline", "text"] = "default",
        transparent_color: str = "transparent",
    ) -> ColorStates:
        HOVER_FACTOR = 0.08
        PRESSED_FACTOR = 0.16
        SELECTED_FACTOR = 0.1
        DISABLED_FACTOR = 0.3
        FOREGROUND_SHIFT = 0.4

        def lighten(c, factor):
            return color_utils.adjust_color_lightness(c, abs(factor))

        def darken(c, factor):
            return color_utils.adjust_color_lightness(c, -abs(factor))

        def adjust(c, factor):
            return lighten(c, factor) if self.is_dark_theme else darken(c, factor)

        def fg_disabled(fg):
            return lighten(fg, FOREGROUND_SHIFT) if self.is_light_theme else darken(fg, FOREGROUND_SHIFT)

        if variant == "default":
            token = self.get_token(base_color)

            if token in {"light", "dark"}:
                contrast = color_utils.get_contrast_ratio(base_color, self.background)
                if contrast < 3.0:
                    base_color = color_utils.adjust_color_for_theme_contrast(
                        base_color, self.background, self.is_dark_theme, min_ratio=3.0
                    )

            normal = base_color
            hover = adjust(base_color, HOVER_FACTOR)
            pressed = adjust(base_color, PRESSED_FACTOR)
            selected = adjust(base_color, SELECTED_FACTOR)
            disabled = adjust(base_color, DISABLED_FACTOR)

            if token in {"light", "info", "warning"}:
                fg = self.foreground if self.is_light_theme else self.background
            else:
                fg = self.background if self.is_light_theme else self.foreground

            return ColorStates(
                normal=normal,
                hover=hover,
                pressed=pressed,
                selected=selected,
                disabled=disabled,
                foreground=fg,
                foreground_hover=fg,
                foreground_pressed=fg,
                foreground_selected=fg,
                foreground_focus=fg,
                foreground_disabled=fg_disabled(fg),
            )

        elif variant == "outline":
            token = self.get_token(base_color)

            if token in {"light", "dark"}:
                contrast = color_utils.get_contrast_ratio(base_color, self.background)
                if contrast < 3.0:
                    base_color = color_utils.adjust_color_for_theme_contrast(
                        base_color, self.background, self.is_dark_theme, min_ratio=3.0
                    )

            solid = self.get_color_states(base_color, variant="default", transparent_color=transparent_color)

            return ColorStates(
                normal=transparent_color,
                hover=solid.hover,
                pressed=solid.pressed,
                selected=solid.selected,
                disabled=transparent_color,
                foreground=base_color,
                foreground_hover=solid.foreground_hover,
                foreground_pressed=solid.foreground_pressed,
                foreground_selected=solid.foreground_selected,
                foreground_focus=solid.foreground_focus,
                foreground_disabled=fg_disabled(base_color),
            )

        elif variant == "text":
            normal = transparent_color
            hover = adjust(base_color, 0.05)
            pressed = adjust(base_color, 0.1)
            selected = adjust(base_color, 0.2)
            disabled = transparent_color

            def fg_contrast(bg):
                return color_utils.get_contrast_text_color(
                    bg,
                    light=self.foreground if self.is_dark_theme else self.background,
                    dark=self.background if self.is_dark_theme else self.foreground,
                )

            return ColorStates(
                normal=normal,
                hover=hover,
                pressed=pressed,
                selected=selected,
                disabled=disabled,
                foreground=base_color,
                foreground_hover=fg_contrast(hover),
                foreground_pressed=fg_contrast(pressed),
                foreground_selected=fg_contrast(selected),
                foreground_focus=fg_contrast(selected),
                foreground_disabled=fg_disabled(base_color),
            )

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
