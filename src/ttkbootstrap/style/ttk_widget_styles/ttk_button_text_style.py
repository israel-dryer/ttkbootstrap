from __future__ import annotations
from typing import TYPE_CHECKING

from ttkbootstrap.style.style_builder import StyleBuilder
from ttkbootstrap.style.style_element import Element, ElementImage
from ttkbootstrap.style.ttk_widget_styles.assets import BUTTON_DISABLED, BUTTON_TEXT

if TYPE_CHECKING:
    from ttkbootstrap.style.theme import Theme


class TTkButtonTextStyle(StyleBuilder):

    def __init__(self, theme: Theme):
        super().__init__(theme)

    def invoke(self, color: str, **_):
        """Create the default button style"""

        style = f'{color}.Text.TButton'
        if self.theme.has_style(style):
            return style

        # color token
        color = "foreground" if color == "default" else color

        # button colors
        shades = self.theme.get_shades('background')
        foreground = self.theme.get_color(color)
        background = self.theme.background
        hover = shades.d1 if self.theme.is_light_theme else shades.l1
        pressed = shades.d2 if self.theme.is_light_theme else shades.l2
        disabled = self.theme.get_color('border')

        # state images
        normal_img = self.theme.image_recolor(BUTTON_TEXT, background)
        self.theme.register_asset(str(normal_img), normal_img)

        hover_img = self.theme.image_recolor(BUTTON_DISABLED, hover)
        self.theme.register_asset(str(hover_img), hover_img)

        pressed_img = self.theme.image_recolor(BUTTON_DISABLED, pressed)
        self.theme.register_asset(str(pressed_img), pressed_img)

        # Image element and state specs
        el = ElementImage(f'{style}.border', normal_img, sticky="nsew", border=8, padding=4)
        el.add_spec('pressed !disabled', pressed_img)
        el.add_spec('hover !disabled', hover_img)
        el.build()

        # Layout and style config
        Element(style).layout([
            Element(f'{style}.border', sticky="nsew"), [
                Element('Button.focus', sticky="nsew"), [
                    Element('Button.padding', sticky="nsew"), [
                        Element('Button.label', sticky="nsew")
                    ]
                ]
            ]
        ])

        self.theme.configure(
            style,
            foreground=foreground,
            background=self.theme.background,
            focuscolor=foreground,
            font="-size 12",
            relief="raised",
            anchor="center"
        )

        self.theme.map(style, foreground=[('disabled', disabled)])

        self.theme.add_style(style)
        return style
