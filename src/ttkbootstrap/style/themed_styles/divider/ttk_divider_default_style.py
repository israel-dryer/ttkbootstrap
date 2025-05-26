from __future__ import annotations
from typing import TYPE_CHECKING

from ...style_builder import StyleBuilder
from ...style_element import Element, ElementImage
from ....utils import load_asset_image

if TYPE_CHECKING:
    from ...theme import Theme


class TTkDividerDefaultStyle(StyleBuilder):

    def __init__(self, theme: Theme):
        super().__init__(theme)

    def invoke(self, color, **extras):
        """Create the default switch style"""

        orient = extras.pop('orient', 'horizontal')

        style = f'{color}.{orient.title()}.Divider'
        if self.theme.has_style(style):
            return style

        # color token
        color = "border" if color == "default" else color

        # button colors
        divider_color = self.theme.get_color(color)

        # state images
        if orient == "vertical":
            base_divider_image = load_asset_image('divider-default-vertical.png')
        else:
            base_divider_image = load_asset_image('divider-default-horizontal.png')

        divider_img = self.theme.image_recolor(base_divider_image, divider_color)
        self.theme.register_asset(str(divider_img), divider_img)

        # Separator element
        el = ElementImage(
            f'{style}.divider', divider_img, border=0, padding=0)
        el.build()

        # Layout and style config
        Element(style).layout([Element(f'{style}.divider', sticky="ew" if orient == "horizontal" else "ns")])
        self.theme.configure(style, background=self.theme.background)
        self.theme.add_style(style)
        return style
