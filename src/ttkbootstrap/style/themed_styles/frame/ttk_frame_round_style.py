from __future__ import annotations
from typing import TYPE_CHECKING

from ...style_builder import StyleBuilder
from ...style_element import Element, ElementImage
from ....utils import load_asset_image

if TYPE_CHECKING:
    from ...theme import Theme


class TTkFrameRoundStyle(StyleBuilder):

    def __init__(self, theme: Theme):
        super().__init__(theme)

    def invoke(self, token: str, **extras):
        """Create the rounded frame style"""

        # check if the background color should be inherited from the parent
        parent_background = extras.get('background', None)
        container_bg = self.theme.background

        if parent_background is not None and parent_background != container_bg:
            style = f'{parent_background}.{token}.Round.TFrame'  # inherited background style
            container_bg = parent_background
        else:
            style = f'{token}.Round.TFrame'

        # check if style already exists
        if self.theme.has_style(style):
            return style

        # color token
        token = "border" if token == "default" else token
        frame_border_color = self.theme.get_input_border_color()
        frame_bg_color = frame_border_color if token == "border" else self.theme.get_color(token)

        # base image for state
        base_card_image = load_asset_image('card.png')

        # state images
        outline_img = self.theme.image_recolor_map(base_card_image, frame_bg_color, container_bg)
        self.theme.register_asset(str(outline_img), outline_img)

        # Image element and state specs
        el = ElementImage(f'{style}.border', outline_img, sticky="nsew", border=8, padding=4)
        el.build()

        # Layout and style config
        Element(style).layout(
            [
                Element(f'{style}.border', sticky="nsew"),
                [
                    Element('Frame.padding', sticky="nsew")
                ]
            ])

        self.theme.configure(
            style,
            background=frame_bg_color,
            relief="flat")

        self.theme.add_style(style)
        return style
