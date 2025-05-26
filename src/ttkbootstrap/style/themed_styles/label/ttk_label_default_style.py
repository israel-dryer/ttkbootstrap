from __future__ import annotations
from typing import TYPE_CHECKING

from ...style_builder import StyleBuilder

if TYPE_CHECKING:
    from ...theme import Theme


class TTkLabelDefaultStyle(StyleBuilder):

    def __init__(self, theme: Theme):
        super().__init__(theme)

    def invoke(self, color: str, **_):
        """Create the default label style"""

        style = f'{color}.TLabel'
        if self.theme.has_style(style):
            return style

        # color token
        color = "foreground" if color == "default" else color

        foreground = self.theme.get_foreground(color)
        background = self.theme.background
        self.theme.configure(
            style,
            foreground=foreground,
            background=background,
            font="-size 12",
        )
        self.theme.add_style(style)
        return style
