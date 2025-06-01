import platform
from typing import Dict, Literal, Tuple

from tkinter.ttk import Style
from tkinter import font as tkFont

from .legacy_styles import tk_handlers
from .themed_styles import ttk_handlers
from ..exceptions import StyleHandlerNotFoundError
from ..logger import logger
from ..utils.style_utils import ColorPair

DEFAULT_COLOR_1 = '#ddd'
DEFAULT_COLOR_2 = '#111'

ThemeMode = Literal['light', 'dark']
ThemeColor = Literal[
    'primary', 'secondary', 'success', 'info', 'warning',
    'danger', 'light', 'dark', 'surface'
]
ThemeColors = Dict[str, str]


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

    @property
    def is_dark_theme(self):
        return self.mode == 'dark'

    @property
    def is_light_theme(self):
        return self.mode == 'light'

    @property
    def system(self):
        return platform.system()

    def has_style(self, name: str):
        return name in self.styles

    def add_style(self, name: str):
        self.styles.add(name)

    def configure(self, style: str, **kwargs):
        return self.ttk.configure(style, **kwargs)

    def map(self, style: str, **options):
        self.ttk.map(style, **options)

    def get_color(self, token: str):
        return self.__dict__.get(token)

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
