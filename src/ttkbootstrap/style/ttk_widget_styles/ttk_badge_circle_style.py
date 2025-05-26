from __future__ import annotations
from typing import TYPE_CHECKING

from ..style_builder import StyleBuilder
from ..style_element import Element, ElementImage
from ...utils import load_asset_image

if TYPE_CHECKING:
    from ..theme import Theme


class TTkBadgeCircleStyle(StyleBuilder):

    def __init__(self, theme: Theme):
        super().__init__(theme)

    def invoke(self, color: str, **_):
        """Create the default button style"""

        style = f'{color}.Circle.Badge.TLabel'
        if self.theme.has_style(style):
            return style

        # color token
        color = "border" if color == "default" else color

        # button colors
        foreground = self.theme.get_foreground(color)
        background = self.theme.get_color(color)

        base_badge_image = load_asset_image('badge-circle.png')

        # state images
        badge_img = self.theme.image_recolor(base_badge_image, background)
        self.theme.register_asset(str(badge_img), badge_img)

        border = int(badge_img.height() / 2)

        # Image element and state specs
        ElementImage(f'{style}.background', badge_img, sticky="nsew", border=border).build()

        # Layout and style config
        Element(style).layout(
            [
                Element(f'{style}.background', sticky="nsew"),
                Element('TLabel.padding', sticky="nsew"),
                [
                    Element('TLabel.label', sticky="nsew")
                ]
            ])

        self.theme.configure(
            style,
            foreground=foreground,
            font="-size 9 -weight bold",
            anchor="center",
            background=self.theme.background,
            padding=(10, 5)
        )
        self.theme.add_style(style)
        return style
