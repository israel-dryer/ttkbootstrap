import base64
from io import BytesIO
from math import ceil
from tkinter.ttk import Style
from tkinter import font as tkFont
import platform

from PIL import Image, ImageOps
from PIL.ImageDraw import ImageDraw
from PIL.ImageTk import PhotoImage

from .legacy_styles import tk_handlers
from .themed_styles import ttk_handlers
from ..exceptions import StyleHandlerNotFoundError
from ..logger import logger
from ..utils import style_utils

from collections import namedtuple
from typing import Any, Dict, List, Literal, Tuple, Union

DEFAULT_COLOR_1 = '#ddd'
DEFAULT_COLOR_2 = '#111'
SHADE_VALUES = [1.4, 1.3, 1.2, 1.1, 1.0, 0.9, 0.8, 0.7, 0.6]

Shades = namedtuple('Shades', 'l4 l3 l2 l1 base d1 d2 d3 d4')

ThemeMode = Literal['light', 'dark']
ThemeColor = Literal[
    'primary', 'secondary', 'success', 'info', 'warning', 'danger', 'light', 'dark', 'background', 'foreground', 'border']
ThemeColors = Dict[str, str]


def rgb_distance(c1, c2):
    """Euclidean distance between two RGB colors."""
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

        # theme colors
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

        # update default fonts
        tkFont.nametofont('TkDefaultFont').configure(size=12)

        # add tk handlers
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
        if color_name == 'light':
            return self.dark
        elif color_name == 'dark':
            return self.light
        elif color_name == 'background':
            return self.foreground
        elif color_name == 'foreground':
            return self.background
        elif color_name == 'border':
            return self.foreground
        elif self.mode == 'dark':
            return self.foreground
        else:
            return self.background

    def get_color(self, token: str):
        return self.__dict__.get(token)

    def get_token(self, color: str):
        color_map = self.colors()
        tokens = list(color_map.keys())
        colors = list(color_map.values())
        try:
            index = colors.index(color)
            return tokens[index]
        except ValueError:
            return None


    def get_shades(self, color_name: str) -> Shades:
        colors = []
        value = self.get_color(color_name)
        red, grn, blu = style_utils.color_to_rgb(value, 'hex')
        for shade in SHADE_VALUES:
            color = f'#{int(max(0, min(red * shade, 255))):02x}'
            color += f'{int(max(0, min(grn * shade, 255))):02x}'
            color += f'{int(max(0, min(blu * shade, 255))):02x}'
            colors.append(color)
        return Shades(*colors)

    @staticmethod
    def image_resize(img, size):
        """Resize a PIL image and return a PhotoImage"""
        return PhotoImage(image=img.resize(size, Image.Resampling.LANCZOS))

    @staticmethod
    def image_open(data: str):
        img_data = base64.b64decode(data)
        return Image.open(BytesIO(img_data)).convert('RGBA')

    def image_recolor(self, data: Union[str,Image], color: str, overlay: Image=None):
        """
        Recolor a grayscale-based UI asset where white represents the active pixel
        and black or transparent represents absence, using luminance-based interpolation.
        """
        if self.is_light_theme:
            white = color
            black = "#ffffff"  # background stays white
        else:
            white = color
            black = "#000000"

        return self.image_recolor_map(data, white, black, overlay)

    def image_recolor_map(self, data: Union[str,Image], white: str, black: str, overlay: Image=None):
        """
        Recolor an anti-aliased two-tone RGBA image using luminance mapping.
        Pixels closer to white get `white`, and pixels closer to black get `black`,
        with smooth interpolation for edge pixels.
        """
        if isinstance(data, str):
            img = Theme.image_open(data).convert("RGBA")
        else:
            img = data
        base_rgb = ImageOps.grayscale(img)  # Use luminance to guide interpolation
        alpha = img.getchannel("A")

        # Colors to blend between
        light = style_utils.color_to_rgb(white)
        dark = style_utils.color_to_rgb(black)

        # Create output image
        result = Image.new("RGBA", img.size)
        pixels = result.load()

        for y in range(img.height):
            for x in range(img.width):
                lum = base_rgb.getpixel((x, y)) / 255.0
                a = alpha.getpixel((x, y))
                # Interpolate between dark and light
                r = round(dark[0] + (light[0] - dark[0]) * lum)
                g = round(dark[1] + (light[1] - dark[1]) * lum)
                b = round(dark[2] + (light[2] - dark[2]) * lum)
                pixels[x, y] = (r, g, b, a)

        # apply mask if provided
        if overlay is not None:
            result = Image.alpha_composite(result, overlay)

        scaled = self.downscale_image(result)
        return PhotoImage(scaled)

    def downscale_image(self, image: Image.Image) -> Image.Image:
        scale = float(self.ttk.tk.call('tk', 'scaling')) or 1.0  # e.g. 1.0 or 1.5 or 2.0

        # Image is 2x design size, so baseline is 0.5
        effective_scale = 0.5 * scale

        new_size = (
            max(1, int(image.width * effective_scale)),
            max(1, int(image.height * effective_scale))
        )

        return image.resize(new_size, Image.Resampling.LANCZOS)

    @staticmethod
    def image_draw(size, mode=None, *args):
        """Return a PIL Image and ImageDraw object"""
        im = Image.new(mode or 'RGBA', size, *args)
        dr = ImageDraw(im)
        return im, dr

    @property
    def is_dark_theme(self):
        return self.mode == 'dark'

    @property
    def is_light_theme(self):
        return self.mode == 'light'

    def __iter__(self):
        colors = self.__dict__.copy()
        del colors['name']
        del colors['mode']
        return iter(colors)

    def __repr__(self):
        return str(self.__dict__)

    @property
    def system(self):
        return platform.system()

    def initialize(self):
        pass

    def add_handler(self, name, handler):
        self.handlers[name] = handler

    def get_handler(self, name):
        if name not in self.handlers.keys():
            raise StyleHandlerNotFoundError(name)
        return self.handlers.get(name)

    def register_asset(self, name, data):
        self.assets[name] = data

    def execute_handler(self, name, *args, **extras) -> str:
        if name not in self.handlers.keys():
            logger.error('ThemeBuilder', f'Style handler {name} not found.')
            return ''
            # raise StyleHandlerNotFoundError(name)
        return self.handlers.get(name).invoke(*args, **extras)

    @staticmethod
    def adjust_color_brightness(hex_color: str, factor: float) -> str:
        """
        Lighten or darken a hex color.

        Args:
            hex_color (str): The hex color string, e.g. "#336699" or "336699".
            factor (float): A number > 0.0 where:
                - 1.0 = no change
                - < 1.0 = darken
                - > 1.0 = lighten

        Returns:
            str: Adjusted hex color string, e.g. "#4d88b5"
        """
        hex_color = hex_color.lstrip("#")
        if len(hex_color) != 6:
            raise ValueError("Expected 6-character hex color string.")

        r, g, b = [int(hex_color[i:i + 2], 16) for i in (0, 2, 4)]

        def clamp(value: int) -> int:
            return max(0, min(255, value))

        r = clamp(int(r * factor))
        g = clamp(int(g * factor))
        b = clamp(int(b * factor))

        return f"#{r:02x}{g:02x}{b:02x}"

    @staticmethod
    def is_color_dark(hex_color: str) -> bool:
        """
        Determine if a hex color is considered dark.

        Args:
            hex_color (str): Hex color string like "#336699" or "336699"

        Returns:
            bool: True if color is dark, False if light
        """
        hex_color = hex_color.lstrip("#")
        if len(hex_color) != 6:
            raise ValueError("Expected 6-digit hex color.")

        r, g, b = [int(hex_color[i:i + 2], 16) for i in (0, 2, 4)]

        # Perceived brightness formula (W3C)
        brightness = (r * 299 + g * 587 + b * 114) / 1000

        return brightness < 128

    def scale_size(self, *size):
        """Adjust the sizes specified based on the scaling factor of the
        development environment to ensure that the sizes are consistent across
        platforms and screen resolutions.

        Parameters
        ----------
        *size : Iterable
            One or more sizes.

        Returns
        -------
        Union[Iterable, int]
            A integer or list of integers
        """
        if self.system == 'Darwin':
            baseline = 1.000492368291482
        else:
            # 4k - 3840x2160
            baseline = 2.000984736582964

        scaling = self.ttk.tk.call('tk', 'scaling')
        factor = scaling / baseline

        sizes = tuple([ceil(s * factor) for s in size])
        if len(sizes) == 1:
            return sizes[0]
        else:
            return sizes


# --- STANDARD THEMES
def get_standard_themes():
    return [
        Theme(
            'cosmo', 'light',
            primary='#2780e3',
            secondary='#7E8081',
            success='#3fb618',
            info='#9954bb',
            warning='#ff7518',
            danger='#ff0039',
            light='#F8F9FA',
            dark='#373A3C',
            background='#ffffff',
            foreground='#373a3c',
            border='#dee2e6'
        ),
        Theme(
            'flatly', 'light',
            primary='#2c3e50',
            secondary='#95a5a6',
            success='#18bc9c',
            info='#3498db',
            warning='#f39c12',
            danger='#e74c3c',
            light='#ecf0f1',
            dark='#7b8a8b',
            background='#ffffff',
            foreground='#212529',
            border='#dee2e6'
        ),
        Theme(
            'minty', 'light',
            primary='#78c2ad',
            secondary='#f3969a',
            success='#56cc9d',
            info='#6cc3d5',
            warning='#ffce67',
            danger='#ff7851',
            light='#f8f9fa',
            dark='#343a40',
            background='#ffffff',
            foreground='#5a5a5a',
            border='#dee2e6'
        ),
        Theme(
            'superhero', 'dark',
            primary='#4c9be8',
            secondary='#4e5d6c',
            success='#5cb85c',
            info='#5bc0de',
            warning='#f0ad4e',
            danger='#d9534f',
            light='#aab6c2',
            dark='#20374c',
            background='#2b3e50',
            foreground='#fff',
            border='#495057'
        ),
        Theme(
            'light', 'light',
            primary='#0d6efd',
            secondary='#6c757d',
            success='#198754',
            info='#0dcaf0',
            warning='#ffc107',
            danger='#dc3545',
            light='#aab6c2',
            dark='#20374c',
            background='#ffffff',
            foreground='#212529',
            border='#dee2e6'
        ),
        Theme(
            'dark', 'dark',
            primary='#0d6efd',
            secondary='#6c757d',
            success='#198754',
            info='#0dcaf0',
            warning='#ffc107',
            danger='#dc3545',
            light='#f8f9fa',
            dark='#212529',
            background='#212529',
            foreground='#dee2e6',
            border='#495057'
        )
    ]
