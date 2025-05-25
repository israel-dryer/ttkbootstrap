from __future__ import annotations
from typing import TYPE_CHECKING

from ttkbootstrap.style.style_builder import StyleBuilder
from ttkbootstrap.style.style_element import Element, ElementImage
from ttkbootstrap.style.ttk_widget_styles.assets import CARD_BORDER

if TYPE_CHECKING:
    from ttkbootstrap.style.theme import Theme


class TTkFrameRoundStyle(StyleBuilder):

    def __init__(self, theme: Theme):
        super().__init__(theme)

    def invoke(self, color: str, **_):
        """Create the rounded frame style"""

        style = f'{color}.Round.TFrame'

        if self.theme.has_style(style):
            return style

        # color token
        color = "border" if color == "default" else color
        outline = self.theme.get_color(color)

        # state images
        outline_img = self.theme.image_recolor_map(CARD_BORDER, self.theme.background, outline)
        self.theme.register_asset(str(outline_img), outline_img)

        # Image element and state specs
        el = ElementImage(f'{style}.border', outline_img, sticky="nsew", border=8, width=261, height=128, padding=4)
        el.build()

        # Layout and style config
        Element(style).layout(
            [
                Element(f'{style}.border', sticky="nsew"), [
                    Element('Frame.padding', sticky="nsew")
                ]
            ])

        self.theme.configure(style, background=self.theme.background, relief="flat")
        self.theme.add_style(style)
        return style
