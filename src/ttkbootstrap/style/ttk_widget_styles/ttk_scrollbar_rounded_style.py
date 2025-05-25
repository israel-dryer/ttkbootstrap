from __future__ import annotations

from typing import Literal, TYPE_CHECKING

from PIL import Image, ImageDraw

from ttkbootstrap.style.style_element import ElementImage, Element
from ttkbootstrap.style.style_builder import StyleBuilder

if TYPE_CHECKING:
    from ttkbootstrap.style.theme import Theme


class TTkScrollbarRoundStyle(StyleBuilder):

    def __init__(self, theme: Theme):
        super().__init__(theme)

    def invoke(self, color: str, **extras):
        """Create the rounded scrollbar style"""
        orient = extras.pop('orient', 'vertical')
        style = f'{color}.{orient.title()}.Rounded.TScrollbar'

        if self.theme.has_style(style):
            return style

        color = color if color != 'default' else 'light'
        background = self.theme.get_color(color)
        handle_shades = self.theme.get_shades(color)
        trough_color = self.theme.background

        if color == "light":
            background = handle_shades.d3
            active = handle_shades.d4
            pressed = handle_shades.d4
        else:
            active = handle_shades.d2
            pressed = handle_shades.d3

        self.theme.configure(
            style,
            troughcolor=trough_color,
            darkcolor=trough_color,
            bordercolor=trough_color,
            lightcolor=trough_color,
            arrowcolor=background,
            background=trough_color,
            relief="flat",
            borderwidth=0,
        )
        self.theme.map(style, arrowcolor=[("pressed", pressed), ("active", active)])

        img_normal, img_pressed, img_active = self.create_scrollbar_assets(background, pressed, active, orient)

        if orient == "horizontal":
            # horizontal scrollbar
            thumb_elem = ElementImage(f"{style}.thumb", img_normal, border=(3, 0), sticky="ew")
            thumb_elem.add_spec("pressed", img_pressed)
            thumb_elem.add_spec("active", img_active)
            thumb_elem.build()

            Element(style).layout(
                [
                    Element("Horizontal.Scrollbar.trough", sticky="we"),
                    [
                        Element("Horizontal.Scrollbar.leftarrow", side="left", sticky=""),
                        Element("Horizontal.Scrollbar.rightarrow", side="right", sticky=""),
                        Element(f"{style}.thumb", expand=1, sticky="nswe")],
                ]
            )

        else:
            # vertical scrollbar
            thumb_elem = ElementImage(f"{style}.thumb", img_normal, border=(0, 3), sticky="ns")
            thumb_elem.add_spec("pressed", img_pressed)
            thumb_elem.add_spec("active", img_active)
            thumb_elem.build()

            Element(style).layout(
                [
                    Element("Vertical.Scrollbar.trough", sticky="ns"),
                    [
                        Element("Vertical.Scrollbar.uparrow", side="top", sticky=""),
                        Element("Vertical.Scrollbar.downarrow", side="bottom", sticky=""),
                        Element(f"{style}.thumb", expand=1, sticky="nswe")
                    ]
                ])

        self.theme.add_style(style)
        return style

    def create_scrollbar_assets(self, thumb_color, pressed, active, orient):
        """Create the image assets used to build the standard scrollbar
        style.

        Parameters:

            thumb_color (str):
                The primary color value used to color the thumb.

            pressed (str):
                The color value to use when the thumb is pressed.

            active (str):
                The color value to use when the thumb is active or
                hovered.

            orient (str):
                The widget orientation
        """
        v_size = self.theme.scale_size(9, 28)
        h_size = self.theme.scale_size(28, 9)

        def draw_rect(size, fill):
            x = size[0] * 10
            y = size[1] * 10
            img = Image.new("RGBA", (x, y), (0, 0, 0, 0))

            draw = ImageDraw.Draw(img)
            draw.rounded_rectangle((0, 0, x, y), radius=40, fill=fill)

            image = self.theme.image_resize(img, size)
            self.theme.register_asset(str(image), image)
            return str(image)

        if orient == "horizontal":
            # create images
            normal_img = draw_rect(h_size, thumb_color)
            pressed_img = draw_rect(h_size, pressed)
            active_img = draw_rect(h_size, active)
        else:
            normal_img = draw_rect(v_size, thumb_color)
            pressed_img = draw_rect(v_size, pressed)
            active_img = draw_rect(v_size, active)

        return (
            normal_img,
            pressed_img,
            active_img,
        )
