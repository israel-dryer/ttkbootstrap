from __future__ import annotations
from typing import TYPE_CHECKING

from ...style_builder import StyleBuilder
from ...style_element import Element, ElementImage
from ....utils import load_asset_image

"""
    The style deviates from bootstrap on the rounded corners.  There is not a clean way
    to implement this with an image layout because the pbar is conditionally rounded on
    one side or both. The compromise is to flatten the edges. Make revisit again in the
    future if there is a way to implement this with an image layout that replicates the
    same conditional rounded corners as bootstrap.
"""

if TYPE_CHECKING:
    from ....style.theme import Theme


class TTkProgressDefaultStyle(StyleBuilder):

    def __init__(self, theme: Theme):
        super().__init__(theme)

    def invoke(self, color, **extras):
        """Create the default progress style"""

        orient = extras.pop('orient', 'horizontal')

        style = f'{color}.{orient.title()}.TProgressbar'
        if self.theme.has_style(style):
            return style

        # color token
        color = "primary" if color == "default" else color

        # button colors
        bar_color = self.theme.get_color(color)
        trough_color = self.theme.border

        if orient == 'vertical':
            base_bar_image = load_asset_image('progress-bar-default-vertical.png')
            base_trough_image = load_asset_image('progress-trough-vertical.png')
        else:
            base_bar_image = load_asset_image('progress-bar-default-horizontal.png')
            base_trough_image = load_asset_image('progress-trough-horizontal.png')

        # state images
        bar_img = self.theme.image_recolor(base_bar_image, bar_color)
        self.theme.register_asset(str(bar_img), bar_img)

        trough_img = self.theme.image_recolor(base_trough_image, trough_color)
        self.theme.register_asset(str(trough_img), trough_img)

        # bar element
        el = ElementImage(f'{style}.pbar', bar_img)
        el.build()

        # trough element
        el = ElementImage(f'{style}.trough', trough_img)
        el.build()

        # Layout and style config
        Element(style).layout(
            [
                Element(f'{style}.trough', sticky="ew" if orient == "horizontal" else "ns"), [
                Element(f"{style}.pbar", side="top" if orient == "vertical" else "left", sticky="")
                ]
            ]
        )
        self.theme.configure(style, background=self.theme.background)
        self.theme.add_style(style)
        return style
