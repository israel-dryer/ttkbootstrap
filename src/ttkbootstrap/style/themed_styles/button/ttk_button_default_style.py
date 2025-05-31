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

        background, style = self.theme.get_background_style(token, 'TButton', **extras)
        if self.theme.has_style(style):
            return style

        # button colors
        token = "primary" if token == "default" else token
        base_color = self.theme.get_color(token)
        colors = self.theme.get_color_states(base_color, "default", background)

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
            focuscolor=colors.foreground_focus,
            background=background,
            font="-size 12",
            relief="raised",
            anchor="center")

        self.theme.map(style, foreground=[('disabled', colors.foreground_disabled), ('focus', colors.foreground_focus)])

        self.theme.add_style(style)
        return style
