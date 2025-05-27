from __future__ import annotations

from typing import TYPE_CHECKING

from ...style_builder import StyleBuilder
from ...style_element import Element, ElementImage
from ....utils import load_asset_image

if TYPE_CHECKING:
    from ...theme import Theme


class TTkButtonOutlineStyle(StyleBuilder):

    def __init__(self, theme: Theme):
        super().__init__(theme)

    def invoke(self, token: str, **extras) -> str:
        """Apply the outline button style"""

        # check if the background color should be inherited from the parent
        parent_background = extras.get('background', None)
        container_bg = self.theme.background
        if parent_background is not None and parent_background != container_bg:
            style = f'{parent_background}.{token}.Outline.TButton'  # inherited background style
            container_bg = parent_background
        else:
            style = f'{token}.Outline.TButton'

        if self.theme.has_style(style):
            return style

        # color token
        token = "primary" if token == "default" else token

        # button colors
        btn_bg_shades = self.theme.get_shades(token)
        btn_accent = self.theme.get_color(token)
        btn_hover_bg = btn_bg_shades.d2
        btn_hover_fg = self.theme.get_foreground(token)
        btn_pressed_bg = btn_bg_shades.d3
        btn_disabled_bg = btn_accent

        # base images used for state images
        base_button_image = load_asset_image('button-outline.png')
        base_disabled_image = load_asset_image('button-disabled.png')
        base_solid_image = load_asset_image('button-default.png')

        # state images
        normal_img = self.theme.image_recolor(base_button_image, btn_accent)
        self.theme.register_asset(str(normal_img), normal_img)

        hover_img = self.theme.image_recolor(base_solid_image, btn_hover_bg)
        self.theme.register_asset(str(hover_img), hover_img)

        pressed_img = self.theme.image_recolor(base_solid_image, btn_pressed_bg)
        self.theme.register_asset(str(pressed_img), pressed_img)

        disabled_img = self.theme.image_recolor(base_disabled_image, btn_disabled_bg)
        self.theme.register_asset(str(disabled_img), disabled_img)

        # Image element and state specs
        el = ElementImage(f'{style}.border', normal_img, sticky="nsew", border=8, padding=4)
        el.add_spec('disabled', disabled_img)
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
            foreground=btn_accent,
            background=container_bg,
            font="-size 12",
            relief="raised",
            anchor="center"
        )

        self.theme.map(
            style,
            foreground=[('disabled', btn_accent), ('hover', btn_hover_fg)],
            focuscolor=[('focus hover', btn_hover_fg), ("hover", btn_hover_fg), ('focus', btn_accent)]
        )

        self.theme.add_style(style)
        return style
