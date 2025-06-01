from __future__ import annotations

from typing import TYPE_CHECKING

from ...style_builder import StyleBuilder
from ...style_element import Element, ElementImage

if TYPE_CHECKING:
    from ...theme import Theme


class TTkToolButtonSubtleStyle(StyleBuilder):

    def __init__(self, theme: Theme):
        super().__init__(theme)

    def invoke(self, token: str, **extras):
        """Create the default toolbutton style"""

        background, style = self.theme.get_background_style(token, 'Subtle.ToolButton', **extras)
        if self.theme.has_style(style):
            return style

        # button colors
        token = "primary" if token == "default" else token
        colors = self.theme.get_color_states(token, "toolbutton", background)

        # state images
        normal_img = self.theme.recolor_state_image('button-default.png', colors.normal.color)
        hover_img = self.theme.recolor_state_image('button-default.png', colors.hover.color)
        selected_img = self.theme.recolor_state_image('button-default.png', colors.selected.color)
        disabled_img = self.theme.recolor_state_image('button-disabled.png', colors.disabled.color)

        el = ElementImage(f'{style}.border', normal_img, sticky="nsew", border=8, padding=4)
        el.add_spec('disabled', disabled_img)
        el.add_spec('selected !disabled', selected_img)
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

        self.theme.map(
            style,
            foreground=[
                ('disabled', colors.disabled.on_color),
                ('selected', colors.selected.on_color),
                ('focus !selected', colors.normal.on_color),
            ],
            focuscolor=[
                ('disabled', colors.disabled.on_color),
                ('selected', colors.selected.on_color),
                ('focus !selected', colors.normal.on_color),
            ]
        )

        self.theme.add_style(style)
        return style
