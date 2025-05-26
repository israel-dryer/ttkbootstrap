from __future__ import annotations
from typing import TYPE_CHECKING

from ...style_builder import StyleBuilder
from ...style_element import Element, ElementImage
from ....utils import load_asset_image

if TYPE_CHECKING:
    from ...theme import Theme


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

        base_text_image = load_asset_image('button-text.png')
        base_disabled_image = load_asset_image('button-disabled.png')

        # state images
        normal_img = self.theme.image_recolor(base_text_image, background)
        self.theme.register_asset(str(normal_img), normal_img)

        hover_img = self.theme.image_recolor(base_disabled_image, hover)
        self.theme.register_asset(str(hover_img), hover_img)

        pressed_img = self.theme.image_recolor(base_disabled_image, pressed)
        self.theme.register_asset(str(pressed_img), pressed_img)

        # Image element and state specs
        el = ElementImage(f'{style}.border', normal_img, sticky="nsew", border=8, padding=4)
        el.add_spec('pressed !disabled', pressed_img)
        el.add_spec('hover !disabled', hover_img)
        el.build()

        # Layout and style config
        Element(style).layout(
            [
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
