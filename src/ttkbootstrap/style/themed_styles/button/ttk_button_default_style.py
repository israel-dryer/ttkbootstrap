from __future__ import annotations
from typing import TYPE_CHECKING
from ...style_builder import StyleBuilder
from ...style_element import Element, ElementImage

if TYPE_CHECKING:
    from ...theme import Theme


class TTkButtonDefaultStyle(StyleBuilder):

    def __init__(self, theme: Theme):
        super().__init__(theme, 'TButton')

    def _generate_color_states(self, token: str):
        return self._get_color_states(token)

    def _build_state_images(self, colors) -> dict[str, str]:
        return {
            "normal": self._recolor_state_image('button-default.png', colors.normal.color),
            "hover": self._recolor_state_image('button-default.png', colors.hover.color),
            "pressed": self._recolor_state_image('button-default.png', colors.pressed.color),
            "disabled": self._recolor_state_image('button-disabled.png', colors.disabled.color),
        }

    def _build_layout(self, style: str, images: dict[str, str]):
        border = ElementImage(f'{style}.border', images["normal"], sticky="nsew", border=8, padding=4)
        border.add_spec('disabled', images["disabled"])
        border.add_spec('pressed !disabled', images["pressed"])
        border.add_spec('hover !disabled', images["hover"])
        border.build()

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

    def _configure_style(self, style: str, background: str, colors):
        print(style, background, colors)
        self._configure(
            style,
            foreground=colors.normal.on_color,
            focuscolor=colors.focused.on_color,
            background=background,
            font="-size 12",
            padding=(10, 0),
            relief="raised",
            anchor="center"
        )
        self._map(
            style,
            foreground=[
                ('disabled', colors.disabled.on_color),
                ('focus', colors.focused.on_color)
            ]
        )
        self._add_style(style)
