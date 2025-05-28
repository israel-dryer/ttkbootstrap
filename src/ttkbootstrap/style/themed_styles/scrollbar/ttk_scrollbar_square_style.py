from __future__ import annotations

from typing import TYPE_CHECKING

from ...style_element import ElementImage, Element
from ...style_builder import StyleBuilder
from ....icons import Icon
from ....utils import load_asset_image

if TYPE_CHECKING:
    from ...theme import Theme


class TTkScrollbarSquareStyle(StyleBuilder):

    def __init__(self, theme: Theme):
        super().__init__(theme)

    def invoke(self, token: str, **extras):
        """Create the default rounded scrollbar style"""
        print('extras', extras)
        orient = extras.pop('orient', 'vertical')

        # check if the background color should be inherited from the parent
        parent_background = extras.get('background', None)
        container_bg = self.theme.background
        if parent_background is not None and parent_background != container_bg:
            style = f'{parent_background}.{token}.{orient.title()}.Square.TScrollbar'  # inherited background style
            container_bg = parent_background
        else:
            style = f'{token}.{orient.title()}.Square.TScrollbar'

        # check if style already exists
        if self.theme.has_style(style):
            return style

        trough_color = self.theme.get_input_background()
        if token == "default":
            thumb_normal_bg, thumb_hover_bg, thumb_pressed_bg = self.theme.get_scrollbar_thumb_colors()
        else:
            thumb_normal_bg, thumb_hover_bg, thumb_pressed_bg = self.theme.get_state_colors(self.theme.get_color(token))

        if orient == 'vertical':
            base_thumb_image = load_asset_image('scrollbar-thumb-square-vertical.png')
            base_trough_image = load_asset_image('scrollbar-trough-vertical.png')
            arrow_one_image = Icon('caret-up-fill', size=26, color='#ffffff', cache_image=False).image
            arrow_two_image = Icon('caret-down-fill', size=26, color='#ffffff', cache_image=False).image
            arrow_one_name = "uparrow"
            arrow_two_name = "downarrow"
            border = 10
        else:
            base_thumb_image = load_asset_image('scrollbar-thumb-square-horizontal.png')
            base_trough_image = load_asset_image('scrollbar-trough-horizontal.png')
            arrow_one_image = Icon('caret-left-fill', size=26, color='#ffffff', cache_image=False).image
            arrow_two_image = Icon('caret-right-fill', size=26, color='#ffffff', cache_image=False).image
            arrow_one_name = "leftarrow"
            arrow_two_name = "rightarrow"
            border = 10

        # state images
        thumb_normal_img = self.theme.image_recolor(base_thumb_image, thumb_normal_bg)
        self.theme.register_asset(str(thumb_normal_img), thumb_normal_img)

        thumb_hover_img = self.theme.image_recolor(base_thumb_image, thumb_hover_bg)
        self.theme.register_asset(str(thumb_hover_img), thumb_hover_img)

        thumb_pressed_img = self.theme.image_recolor(base_thumb_image, thumb_pressed_bg)
        self.theme.register_asset(str(thumb_pressed_img), thumb_pressed_img)

        trough_img = self.theme.image_recolor(base_trough_image, trough_color)
        self.theme.register_asset(str(trough_img), trough_img)

        arrow_one_img = self.theme.image_recolor(arrow_one_image, thumb_normal_bg)
        self.theme.register_asset(str(arrow_one_img), arrow_one_img)

        arrow_two_img = self.theme.image_recolor(arrow_two_image, thumb_normal_bg)
        self.theme.register_asset(str(arrow_two_img), arrow_two_img)

        # thumb element
        el = ElementImage(
            f'{style}.thumb', thumb_normal_img, border=border, sticky="ns" if orient == "vertical" else "ew")
        el.add_spec("pressed", thumb_pressed_img)
        el.add_spec("hover", thumb_hover_img)
        el.build()

        # trough element
        ElementImage(f'{style}.trough', trough_img, sticky="ns" if orient == "vertical" else "ew", padding=2).build()
        # arrow one element
        ElementImage(f'{style}.{arrow_one_name}', arrow_one_img, sticky="").build()
        # arrow two element
        ElementImage(f'{style}.{arrow_two_name}', arrow_two_img, sticky="").build()

        # thumb element
        thumb_elem = ElementImage(f"{style}.thumb", thumb_normal_img, sticky="ns" if orient == "vertical" else "ew")
        thumb_elem.add_spec("pressed", thumb_pressed_img)
        thumb_elem.add_spec("hover", thumb_hover_img)
        thumb_elem.build()

        Element(style).layout(
            [
                Element(f"{style}.trough", sticky="nsew"),
                [
                    Element(f'{style}.{arrow_one_name}', side="left" if orient == "horizontal" else "top", sticky=""),
                    Element(
                        f'{style}.{arrow_two_name}', side="right" if orient == "horizontal" else "bottom", sticky=""),
                    Element(f"{style}.thumb", sticky="ns" if orient == "vertical" else "ew"),
                ],
            ]
        )
        self.ttk.configure(style, background=container_bg)
        self.theme.add_style(style)
        return style
