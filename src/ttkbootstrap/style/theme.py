import base64
from io import BytesIO
from math import ceil
import platform
from collections import namedtuple
from typing import Dict, Literal, Union

from PIL import Image, ImageColor, ImageOps
from PIL.ImageDraw import ImageDraw
from PIL.ImageTk import PhotoImage
from tkinter.ttk import Style
from tkinter import font as tkFont

from .legacy_styles import tk_handlers
from .themed_styles import ttk_handlers
from ..exceptions import StyleHandlerNotFoundError
from ..logger import logger
from ..utils import style_utils

DEFAULT_COLOR_1 = '#ddd'
DEFAULT_COLOR_2 = '#111'
SHADE_VALUES = [1.4, 1.3, 1.2, 1.1, 1.0, 0.9, 0.8, 0.7, 0.6]

Shades = namedtuple('Shades', 'l4 l3 l2 l1 base d1 d2 d3 d4')
ThemeMode = Literal['light', 'dark']
ThemeColor = Literal[
    'primary', 'secondary', 'success', 'info', 'warning', 'danger', 'light', 'dark', 'background', 'foreground', 'border']
ThemeColors = Dict[str, str]


def rgb_distance(c1, c2):
    return ((c1[0] - c2[0]) ** 2 + (c1[1] - c2[1]) ** 2 + (c1[2] - c2[2]) ** 2) ** 0.5


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
        red, grn, blu = style_utils.color_to_rgb(value, 'hex')
        colors = [
            f'#{int(max(0, min(red * s, 255))):02x}{int(max(0, min(grn * s, 255))):02x}{int(max(0, min(blu * s, 255))):02x}'
            for s in SHADE_VALUES
        ]
        return Shades(*colors)

    def get_input_background(self) -> str:
        base = self.background
        return self.adjust_color_lightness(base, -0.15 if self.is_dark_theme else 0.12)

    def get_input_text_color(self) -> str:
        return self.get_contrast_text_color(self.get_input_background())

    def get_input_border_color(self) -> str:
        bg = self.get_input_background()
        return self.adjust_color_lightness(bg, 0.10 if self.is_dark_theme else -0.08)

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
            thumb = self.adjust_color_lightness(bg, -0.3)  # darker thumb on light bg
        else:
            thumb = self.adjust_color_lightness(bg, 0.25)  # lighter thumb on dark bg

        # Step 2: hover and pressed are blends toward primary
        hover = self.blend_colors(thumb, primary, 0.2)
        pressed = self.blend_colors(thumb, primary, 0.4)

        return thumb, hover, pressed

    def get_state_colors(self, normal: str) -> tuple[str, str, str]:
        """
        Generate (normal, hover, pressed) colors based on light or dark theme.
        Light theme → darker hover/pressed.
        Dark theme → lighter hover/pressed.
        """
        if self.is_light_theme:
            hover = self.adjust_color_lightness(normal, -0.12)
            pressed = self.adjust_color_lightness(normal, -0.24)
        else:
            hover = self.adjust_color_lightness(normal, 0.12)
            pressed = self.adjust_color_lightness(normal, 0.24)

        return normal, hover, pressed

    def get_state_colors_blend(
        self,
        normal: str,
        blend_to: str | None = None
    ) -> tuple[str, str, str]:
        """
        Generate (normal, hover, pressed) colors.
        If blend_to is given, hover/pressed blend toward that color.
        Otherwise, fallback to brightness-based logic.
        """
        if blend_to:
            hover = self.blend_colors(normal, blend_to, 0.2)
            pressed = self.blend_colors(normal, blend_to, 0.4)
            return normal, hover, pressed

        return self.get_state_colors(normal)

    @staticmethod
    def image_resize(img, size):
        return PhotoImage(image=img.resize(size, Image.Resampling.LANCZOS))

    @staticmethod
    def image_open(data: str):
        return Image.open(BytesIO(base64.b64decode(data))).convert('RGBA')

    def image_recolor(self, data: Union[str, Image.Image], color: str, overlay: Image.Image = None):
        white = color
        black = "#ffffff" if self.is_light_theme else "#000000"
        return self.image_recolor_map(data, white, black, overlay)

    def image_recolor_map(self, data: Union[str, Image.Image], white: str, black: str, overlay: Image.Image = None):
        img = self.image_open(data) if isinstance(data, str) else data
        base_rgb = ImageOps.grayscale(img)
        alpha = img.getchannel("A")
        light = style_utils.color_to_rgb(white)
        dark = style_utils.color_to_rgb(black)
        result = Image.new("RGBA", img.size)
        pixels = result.load()
        for y in range(img.height):
            for x in range(img.width):
                lum = base_rgb.getpixel((x, y)) / 255.0
                a = alpha.getpixel((x, y))
                r = round(dark[0] + (light[0] - dark[0]) * lum)
                g = round(dark[1] + (light[1] - dark[1]) * lum)
                b = round(dark[2] + (light[2] - dark[2]) * lum)
                pixels[x, y] = (r, g, b, a)
        if overlay is not None:
            result = Image.alpha_composite(result, overlay)
        return PhotoImage(self.downscale_image(result))

    def downscale_image(self, image: Image.Image) -> Image.Image:
        scale = float(self.ttk.tk.call('tk', 'scaling')) or 1.0
        factor = 0.5 * scale
        size = (max(1, int(image.width * factor)), max(1, int(image.height * factor)))
        return image.resize(size, Image.Resampling.LANCZOS)

    @staticmethod
    def image_draw(size, mode=None, *args):
        im = Image.new(mode or 'RGBA', size, *args)
        return im, ImageDraw(im)

    def __iter__(self):
        copy = self.__dict__.copy()
        for key in ['name', 'mode']: copy.pop(key, None)
        return iter(copy)

    def __repr__(self):
        return str(self.__dict__)

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

    @staticmethod
    def adjust_color_lightness(hex_color: str, factor: float) -> str:
        r, g, b = ImageColor.getrgb(hex_color)
        if factor > 0:
            r = int(r + (255 - r) * factor)
            g = int(g + (255 - g) * factor)
            b = int(b + (255 - b) * factor)
        else:
            r = int(r * (1 + factor))
            g = int(g * (1 + factor))
            b = int(b * (1 + factor))
        return f"#{r:02x}{g:02x}{b:02x}"

    @staticmethod
    def blend_colors(base_hex: str, blend_hex: str, alpha: float) -> str:
        """Blend two hex colors with given alpha (0–1)."""
        r1, g1, b1 = ImageColor.getrgb(base_hex)
        r2, g2, b2 = ImageColor.getrgb(blend_hex)
        r = int((1 - alpha) * r1 + alpha * r2)
        g = int((1 - alpha) * g1 + alpha * g2)
        b = int((1 - alpha) * b1 + alpha * b2)
        return f'#{r:02x}{g:02x}{b:02x}'

    @staticmethod
    def relative_luminance(r, g, b):
        def channel(c):
            c = c / 255.0
            return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

        return 0.2126 * channel(r) + 0.7152 * channel(g) + 0.0722 * channel(b)

    @staticmethod
    def get_contrast_text_color(bg_color: str, light="#ffffff", dark="#000000") -> str:
        r, g, b = ImageColor.getrgb(bg_color)
        lum_bg = Theme.relative_luminance(r, g, b)
        lum_light = Theme.relative_luminance(*ImageColor.getrgb(light))
        lum_dark = Theme.relative_luminance(*ImageColor.getrgb(dark))
        contrast_light = (max(lum_bg, lum_light) + 0.05) / (min(lum_bg, lum_light) + 0.05)
        contrast_dark = (max(lum_bg, lum_dark) + 0.05) / (min(lum_bg, lum_dark) + 0.05)
        return light if contrast_light >= contrast_dark else dark

    @staticmethod
    def is_color_dark(hex_color: str) -> bool:
        hex_color = hex_color.lstrip("#")
        if len(hex_color) != 6:
            raise ValueError("Expected 6-digit hex color.")
        r, g, b = [int(hex_color[i:i + 2], 16) for i in (0, 2, 4)]
        brightness = (r * 299 + g * 587 + b * 114) / 1000
        return brightness < 128

    def scale_size(self, *size):
        baseline = 1.0005 if self.system == 'Darwin' else 2.0009
        factor = float(self.ttk.tk.call('tk', 'scaling')) / baseline
        scaled = [ceil(s * factor) for s in size]
        return scaled[0] if len(scaled) == 1 else tuple(scaled)
