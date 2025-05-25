from __future__ import annotations
from typing import TYPE_CHECKING

from ttkbootstrap.style.style_builder import StyleBuilder
from ttkbootstrap.style.style_element import Element

if TYPE_CHECKING:
    from ttkbootstrap.style.theme import Theme


class TTkFrameDefaultStyle(StyleBuilder):

    def __init__(self, theme: Theme):
        super().__init__(theme)

    def invoke(self, color: str, **_):
        """Create the rounded frame style"""

        style = f'{color}.TFrame'

        if self.theme.has_style(style):
            return style

        # color token
        color = "background" if color == "default" else color
        outline = self.theme.get_color(color)

        # state images
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
