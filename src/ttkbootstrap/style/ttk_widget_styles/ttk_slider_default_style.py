from __future__ import annotations
from typing import TYPE_CHECKING

from ttkbootstrap.style.style_builder import StyleBuilder
from ttkbootstrap.style.style_element import Element, ElementImage
from ttkbootstrap.style.ttk_widget_styles.assets import (
    SLIDER_HANDLE, SLIDER_TRACK_VERTICAL, SLIDER_TRACK_HORIZONTAL
)

if TYPE_CHECKING:
    from ttkbootstrap.style.theme import Theme


class TTkSliderDefaultStyle(StyleBuilder):

    def __init__(self, theme: Theme):
        super().__init__(theme)

    def invoke(self, color, **extras):
        """Create the default switch style"""

        orient = extras.pop('orient', 'horizontal')

        style = f'{color}.{orient.title()}.Scale'
        if self.theme.has_style(style):
            return style

        # color token
        color = "primary" if color == "default" else color

        # button colors
        handle_color = self.theme.get_color(color)
        track_color = self.theme.border

        # state images
        handle_img = self.theme.image_recolor(SLIDER_HANDLE, handle_color)
        self.theme.register_asset(str(handle_img), handle_img)

        slider_track = SLIDER_TRACK_VERTICAL if orient == "vertical" else SLIDER_TRACK_HORIZONTAL
        track_img = self.theme.image_recolor(slider_track, track_color)
        self.theme.register_asset(str(track_img), track_img)

        # handle element
        el = ElementImage(f'{style}.slider', handle_img)
        el.build()

        # track element
        el = ElementImage(
            f'{style}.track',
            track_img,
            width=78 if orient == "horizontal" else 12,
            height=12 if orient == "horizontal" else 78,
            border=(4, 4), padding=(0, 0))
        el.build()

        # Layout and style config
        Element(style).layout(
            [
                Element(f'{style}.track', sticky="ew" if orient == "horizontal" else "ns"),
                Element(f"{style}.slider", side="top" if orient == "vertical" else "left", sticky="")
            ]
        )
        self.theme.configure(style, background=self.theme.background)
        self.theme.add_style(style)
        return style
