from __future__ import annotations
from typing import TYPE_CHECKING

from tkinter import PhotoImage

from ttkbootstrap.style.style_builder import StyleBuilder
from ttkbootstrap.style.style_element import Element, ElementImage
from ttkbootstrap.style.ttk_widget_styles.assets import (
    SWITCH_ON, SWITCH_OFF
)

if TYPE_CHECKING:
    from ttkbootstrap.style.theme import Theme


class TTkSwitchDefaultStyle(StyleBuilder):

    def __init__(self, theme: Theme):
        super().__init__(theme)

    def invoke(self, color: str, **_):
        """Create the default switch style"""

        style = f'{color}.Switch'
        if self.theme.has_style(style):
            return style

        # color token
        color = "primary" if color == "default" else color

        # button colors
        foreground = self.theme.foreground
        indicator_background = self.theme.get_color(color)
        indicator_foreground = self.theme.get_foreground(color)
        border = self.theme.border
        disabled = indicator_background

        # state images
        unchecked_img = self.theme.image_recolor_map(SWITCH_OFF, self.theme.background, border)
        self.theme.register_asset(str(unchecked_img), unchecked_img)

        checked_img = self.theme.image_recolor_map(SWITCH_ON, indicator_foreground, indicator_background)
        self.theme.register_asset(str(checked_img), checked_img)

        spacer_img = PhotoImage(width=6, height=1)
        self.theme.register_asset(str(spacer_img), spacer_img)

        # Spacer element
        ElementImage(f'{style}.spacer', spacer_img, sticky="ew").build()

        # Indicator element
        el = ElementImage(f'{style}.indicator', checked_img, sticky="ns", padding=3)
        el.add_spec('!selected', unchecked_img)
        el.build()

        # Layout and style config
        Element(style).layout(
            [
                Element('Checkbutton.padding', sticky="nsew"), [
                Element(f'{style}.indicator', side="left", sticky=''),
                Element(f"{style}.spacer", side="left", ),
                Element('Checkbutton.label', side="left", expand=1)]
            ])

        self.theme.configure(style, foreground=foreground, background=self.theme.background, font="-size 12")
        self.theme.map(style, foreground=[('disabled', disabled)])

        self.theme.add_style(style)
        return style
