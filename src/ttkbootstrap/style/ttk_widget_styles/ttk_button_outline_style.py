from __future__ import annotations

from typing import TYPE_CHECKING

from ttkbootstrap.style.style_builder import StyleBuilder
from ttkbootstrap.style.style_element import Element, ElementImage
from ttkbootstrap.style.ttk_widget_styles.assets import BUTTON_DEFAULT, BUTTON_DISABLED, BUTTON_OUTLINE

if TYPE_CHECKING:
    from ttkbootstrap.style.theme import Theme


class TTkButtonOutlineStyle(StyleBuilder):

    def __init__(self, theme: Theme):
        super().__init__(theme)

    def invoke(self, color: str, **_) -> str:
        """Apply the outline button style"""

        style = f'{color}.Outline.TButton'
        if self.theme.has_style(style):
            return style

        # color token
        color = "primary" if color == "default" else color

        # button colors
        shades = self.theme.get_shades(color)
        hover_foreground = self.theme.get_foreground(color)
        accent = self.theme.get_color(color)
        hover = shades.d2
        pressed = shades.d3
        disabled = accent

        # state images
        normal_img = self.theme.image_recolor(BUTTON_OUTLINE, accent)
        self.theme.register_asset(str(normal_img), normal_img)

        hover_img = self.theme.image_recolor(BUTTON_DEFAULT, hover)
        self.theme.register_asset(str(hover_img), hover_img)

        pressed_img = self.theme.image_recolor(BUTTON_DEFAULT, pressed)
        self.theme.register_asset(str(pressed_img), pressed_img)

        disabled_img = self.theme.image_recolor(BUTTON_DISABLED, disabled)
        self.theme.register_asset(str(disabled_img), disabled_img)

        # Image element and state specs
        el = ElementImage(f'{style}.border', normal_img, sticky="nsew", border=8, padding=4)
        el.add_spec('disabled', disabled_img)
        el.add_spec('pressed !disabled', pressed_img)
        el.add_spec('hover !disabled', hover_img)
        el.build()

        # Layout and style config
        Element(style).layout([
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
            foreground=accent,
            background=self.theme.background,
            font="-size 12",
            relief="raised",
            anchor="center"
        )

        self.theme.map(
            style,
            foreground=[('disabled', accent), ('hover', hover_foreground)],
            focuscolor=[('focus hover', hover_foreground), ('focus', accent)]
        )

        self.theme.add_style(style)
        return style
