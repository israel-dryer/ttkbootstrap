from __future__ import annotations
from typing import TYPE_CHECKING

from ...style_builder import StyleBuilder
from ...style_element import Element, ElementImage
from ....utils import load_asset_image

if TYPE_CHECKING:
    from ...theme import Theme


class TTkBadgePillStyle(StyleBuilder):

    def __init__(self, theme: Theme):
        super().__init__(theme)

    def invoke(self, token: str, **extras):
        """Create the default button style"""

        # check if the background color should be inherited from the parent
        parent_background = extras.get('background', None)
        container_bg = self.theme.background
        if parent_background is not None and parent_background != container_bg:
            style = f'{parent_background}.{token}.Circle.Badge.TLabel'  # inherited background style
            container_bg = parent_background
        else:
            style = f'{token}.Circle.Badge.TLabel'

        # check if style already exists
        if self.theme.has_style(style):
            return style

        # color token
        token = "border" if token == "default" else token

        # button colors
        foreground = self.theme.get_foreground(token)
        background = self.theme.get_color(token)

        base_badge_image = load_asset_image('badge-pill.png')

        # state images
        badge_img = self.theme.image_recolor(base_badge_image, background)
        self.theme.register_asset(str(badge_img), badge_img)

        border = (int(badge_img.width() / 4), int(badge_img.height() / 4))

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
            background=container_bg,
            padding=(10, 5)
        )
        self.theme.add_style(style)
        return style
