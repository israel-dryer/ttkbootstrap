from __future__ import annotations
from typing import TYPE_CHECKING

from ...style_builder import StyleBuilder

if TYPE_CHECKING:
    from ...theme import Theme


class TTkFrameDefaultStyle(StyleBuilder):

    def __init__(self, theme: Theme):
        super().__init__(theme)

    def invoke(self, color: str, **extras):
        """Create the rounded frame style"""

        style = f'{color}.TFrame'

        if self.theme.has_style(style):
            return style

        # color token
        token = "background" if color == "default" else color
        background = self.theme.get_color(token)

        self.theme.configure(
            style,
            background=background,
            relief="flat")
        self.theme.add_style(style)
        return style
