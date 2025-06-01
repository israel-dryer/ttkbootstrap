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
        style, background = self._resolve_style_name(token, extras)
        if self._style_already_exists(style):
            return style

        colors = self._generate_color_states(token)
        images = self._register_state_images(style, colors)
        self._build_layout(style, images)
        self._configure_style(style, background, colors)

        return style

    def _resolve_style_name(self, token: str, extras: dict) -> tuple[str, str]:
        background, style = self._get_style_name(token, 'TButton', extras.get("background"))
        return style, background

    def _generate_color_states(self, token: str):
        return self._get_color_states(token)

    def _register_state_images(self, style: str, colors) -> dict[str, str]:
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
