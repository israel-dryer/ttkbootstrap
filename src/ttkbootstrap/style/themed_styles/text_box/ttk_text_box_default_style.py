from __future__ import annotations
from typing import TYPE_CHECKING

from ...style_builder import StyleBuilder
from ...style_element import Element, ElementImage
from ....utils import load_asset_image

if TYPE_CHECKING:
    from ...theme import Theme


class TTkTextBoxDefaultStyle(StyleBuilder):

    def __init__(self, theme: Theme):
        super().__init__(theme)

    def invoke(self, color: str, **_):
        """Create the default input style"""

        style = f'{color}.Input'
        if self.theme.has_style(style):
            return style

        # color token
        color = "primary" if color == "default" else color

        # button colors
        foreground = self.theme.foreground
        focused = self.theme.get_color(color)
        border = self.theme.border
        disabled = border

        base_border = load_asset_image('input.png')

        # state images
        normal_img = self.theme.image_recolor_map(base_border, self.theme.background, border)
        self.theme.register_asset(str(normal_img), normal_img)

        focused_img = self.theme.image_recolor_map(base_border, self.theme.background, focused)
        self.theme.register_asset(str(focused_img), focused_img)

        # Border element
        el = ElementImage(f'{style}.border', normal_img, sticky="ew", padding=3, border=6)
        el.add_spec('focus', focused_img)
        el.build()

        # Layout and style config
        Element(style).layout(
            [
                Element(f'{style}.border', sticky="nsew"), [
                Element('Entry.padding', sticky="nsew"), [
                    Element('Entry.textarea', sticky='nsew')
                ]
            ]
            ]
        )

        self.theme.configure(
            style,
            padding=(6, 4),
            foreground=foreground,
            background=self.theme.background,
            selectbackground=self.theme.secondary,
            selectforeground=self.theme.get_foreground('primary'),
            insertcolor=foreground,
            insertwidth=2
        )
        self.theme.map(style, foreground=[('disabled', disabled)])

        self.theme.add_style(style)
        return style
