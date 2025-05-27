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

    def invoke(self, token: str, **extras):
        """Create the default input style"""

        # check if the background color should be inherited from the parent
        parent_background = extras.get('background', None)
        container_bg = self.theme.background
        if parent_background is not None and parent_background != container_bg:
            style = f'{parent_background}.{token}.Input'  # inherited background style
            container_bg = parent_background
        else:
            style = f'{token}.Input'

        # check if style already exists
        if self.theme.has_style(style):
            return style

        # color token
        token = "primary" if token == "default" else token

        # button colors
        input_fg = self.theme.foreground
        input_bg = self.theme.get_input_background()
        border_focused = self.theme.get_color(token)
        border_normal = self.theme.get_input_border_color()
        input_disabled_bg = border_normal

        # base image for input state
        base_border = load_asset_image('input.png')

        # state images
        normal_img = self.theme.image_recolor_map(base_border, input_bg, border_normal)
        self.theme.register_asset(str(normal_img), normal_img)

        focused_img = self.theme.image_recolor_map(base_border, input_bg, border_focused)
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
            foreground=input_fg,
            background=container_bg,
            selectbackground=self.theme.secondary,
            selectforeground=self.theme.get_foreground('primary'),
            insertcolor=input_fg,
            insertwidth=2
        )
        self.theme.map(style, foreground=[('disabled', input_disabled_bg)])

        self.theme.add_style(style)
        return style
