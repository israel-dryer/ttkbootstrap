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

    def invoke(self, token: str, **extras):
        """Create the default button style"""

        # check if the background color should be inherited from the parent
        parent_background = extras.get('background', None)
        container_bg = self.theme.background
        if parent_background is not None and parent_background != container_bg:
            style = f'{parent_background}.{token}.Text.TButton'  # inherited background style
            container_bg = parent_background
        else:
            style = f'{token}.Text.TButton'

        if self.theme.has_style(style):
            return style

        # color token
        token = "foreground" if token == "default" else token

        # button colors
        btn_fg = self.theme.get_color(token)
        btn_bg = container_bg

        btn_hover_bg = self.theme.adjust_color_lightness(container_bg, 0.2)
        btn_pressed_bg = self.theme.adjust_color_lightness(container_bg, 0.3)

        btn_disabled_bg = self.theme.get_color('border')

        # base images used for state images
        base_text_image = load_asset_image('button-text.png')
        base_default_image = load_asset_image('button-default.png')

        # state images
        normal_img = self.theme.image_recolor(base_text_image, btn_bg)
        self.theme.register_asset(str(normal_img), normal_img)

        hover_img = self.theme.image_recolor(base_default_image, btn_hover_bg)
        self.theme.register_asset(str(hover_img), hover_img)

        pressed_img = self.theme.image_recolor(base_default_image, btn_pressed_bg)
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
            foreground=btn_fg,
            background=container_bg,
            focuscolor=btn_fg,
            font="-size 12",
            relief="raised",
            anchor="center"
        )

        self.theme.map(style, foreground=[('disabled', btn_disabled_bg)])

        self.theme.add_style(style)
        return style
