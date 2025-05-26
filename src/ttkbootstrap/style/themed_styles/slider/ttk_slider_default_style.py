from __future__ import annotations
from typing import TYPE_CHECKING

from ...style_builder import StyleBuilder
from ...style_element import Element, ElementImage
from ....utils import load_asset_image

if TYPE_CHECKING:
    from ....style.theme import Theme


class TTkSliderDefaultStyle(StyleBuilder):

    def __init__(self, theme: Theme):
        super().__init__(theme)

    def invoke(self, color, **extras):
        """Create the default switch style"""

        orient = extras.pop('orient', 'horizontal')

        style = f'{color}.{orient.title()}.Scale'
        if self.theme.has_style(style):
            return style

        # color token
        color = "primary" if color == "default" else color

        # button colors
        handle_color = self.theme.get_color(color)
        track_color = self.theme.border

        base_handle_image = load_asset_image('slider-handle.png')
        if orient == 'vertical':
            base_track_image = load_asset_image('slider-track-vertical.png')
        else:
            base_track_image = load_asset_image('slider-track-horizontal.png')

        # state images
        handle_img = self.theme.image_recolor(base_handle_image, handle_color)
        self.theme.register_asset(str(handle_img), handle_img)

        track_img = self.theme.image_recolor(base_track_image, track_color)
        self.theme.register_asset(str(track_img), track_img)

        # handle element
        el = ElementImage(f'{style}.slider', handle_img)
        el.build()

        # track element
        el = ElementImage(f'{style}.track', track_img)
        el.build()

        # Layout and style config
        Element(style).layout(
            [
                Element(f'{style}.track', sticky="ew" if orient == "horizontal" else "ns"),
                Element(f"{style}.slider", side="top" if orient == "vertical" else "left", sticky="")
            ]
        )
        self.theme.configure(style, background=self.theme.background)
        self.theme.add_style(style)
        return style
