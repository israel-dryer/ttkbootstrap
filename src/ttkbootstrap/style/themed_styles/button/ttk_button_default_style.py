from __future__ import annotations

from typing import TYPE_CHECKING

from ...style_builder import StyleBuilder
from ...style_element import Element, ElementImage

if TYPE_CHECKING:
    from ...theme import Theme

class TTkButtonDefaultStyle(StyleBuilder):

    def __init__(self, theme: Theme):
        super().__init__(theme)

    def invoke(self, token: str, **extras):
        """Create the default button style"""

        # check if the background color should be inherited from the parent
        parent_background = extras.get('background', None)
        container_bg = self.theme.background
        if parent_background is not None and parent_background != container_bg:
            style = f'{parent_background}.{token}.TButton'  # inherited background style
            container_bg = parent_background
        else:
            style = f'{token}.TButton'

        # check if style already exists
        if self.theme.has_style(style):
            return style

        # color token
        token = "primary" if token == "default" else token

        # button colors
        colors = self.theme.get_color_states(self.theme.get_color(token))

        # state images
        normal_img = self.theme.recolor_state_image('button-default.png', colors.normal)
        hover_img = self.theme.recolor_state_image('button-default.png', colors.hover)
        pressed_img = self.theme.recolor_state_image('button-default.png', colors.pressed)
        disabled_img = self.theme.recolor_state_image('button-disabled.png', colors.disabled)

        # Image element and state specs
        el = ElementImage(f'{style}.border', normal_img, sticky="nsew", border=8, padding=4)
        el.add_spec('disabled', disabled_img)
        el.add_spec('pressed !disabled', pressed_img)
        el.add_spec('hover !disabled', hover_img)
        el.build()

        # Layout and style config
        Element(style).layout(
            [
                Element(f'{style}.border', sticky="nsew"), [
                Element('Button.focus', sticky="nsew"), [
                    Element('Button.padding', sticky="nsew"), [
                        Element('Button.label', sticky="nsew")
                    ]
                ]
            ]
            ])

        self.theme.configure(
            style,
            foreground=colors.foreground,
            focuscolor=colors.foreground,
            background=container_bg,
            font="-size 12",
            relief="raised",
            anchor="center")

        self.theme.map(style, foreground=[('disabled', colors.foreground_disabled)])

        self.theme.add_style(style)
        return style
