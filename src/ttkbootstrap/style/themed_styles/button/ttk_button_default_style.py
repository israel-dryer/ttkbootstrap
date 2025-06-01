from __future__ import annotations

from typing import TYPE_CHECKING

from ...style_builder import StyleBuilder
from ...style_element import Element, ElementImage
from ....utils.style_utils import (
    get_background_style,
    get_default_color_states,
    recolor_state_image
)

if TYPE_CHECKING:
    from ...theme import Theme


class TTkButtonDefaultStyle(StyleBuilder):

    def __init__(self, theme: Theme):
        super().__init__(theme)

    def invoke(self, token: str, **extras):
        """Create the default button style"""

        background, style = get_background_style(token, 'TButton', self.theme.background, **extras)
        if self.theme.has_style(style):
            return style

        register = self.theme.register_asset
        is_light = self.theme.is_light_theme

        # button colors
        token = "primary" if token == "default" else token
        base = self.theme.get_color(token)
        colors = get_default_color_states(base, self.theme.background, self.theme.is_dark_theme, token)

        # state images
        normal_img = recolor_state_image(register, 'button-default.png', colors.normal.color, is_light)
        hover_img = recolor_state_image(register, 'button-default.png', colors.hover.color, is_light)
        pressed_img = recolor_state_image(register, 'button-default.png', colors.pressed.color, is_light)
        disabled_img = recolor_state_image(register, 'button-disabled.png', colors.disabled.color, is_light)

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
            foreground=colors.normal.on_color,
            focuscolor=colors.focused.on_color,
            background=background,
            font="-size 12",
            padding=(10, 0),
            relief="raised",
            anchor="center")

        self.theme.map(style, foreground=[('disabled', colors.disabled.on_color), ('focus', colors.focused.on_color)])
        self.theme.add_style(style)
        return style
