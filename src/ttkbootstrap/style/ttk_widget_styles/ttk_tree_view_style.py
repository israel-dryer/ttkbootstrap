from __future__ import annotations
from typing import TYPE_CHECKING

from ttkbootstrap.style.style_builder import StyleBuilder
from ttkbootstrap.style.style_element import Element, ElementImage
from ttkbootstrap.style.ttk_widget_styles.assets import CARD_BORDER, DASH_SQUARE, PLUS_SQUARE, EMPTY_SQUARE
from tkinter import PhotoImage, font

if TYPE_CHECKING:
    from ttkbootstrap.style.theme import Theme


class TTkTreeViewDefaultStyle(StyleBuilder):

    def __init__(self, theme: Theme):
        super().__init__(theme)

    def invoke(self, color: str, **_):
        """Create the default treeview style"""

        style = f'{color}.Treeview'

        if self.theme.has_style(style):
            return style

        # get row height from font metrics
        _font = font.nametofont('TkDefaultFont')
        row_height = _font.metrics('linespace') + 8

        # color token
        color_token = "secondary" if color == "default" else color
        header_bg_color = self.theme.get_color(color_token)
        header_fg_color = self.theme.get_foreground(color_token)
        table_bg_color = self.theme.background
        table_fg_color = self.theme.foreground
        border_color = self.theme.border

        # state images
        border_img = self.theme.image_recolor_map(CARD_BORDER, self.theme.background, border_color)
        self.theme.register_asset(str(border_img), border_img)

        close_img = self.theme.image_recolor(DASH_SQUARE, self.theme.foreground)
        self.theme.register_asset(str(close_img), close_img)

        open_img = self.theme.image_recolor(PLUS_SQUARE, self.theme.foreground)
        self.theme.register_asset(str(open_img), open_img)

        empty_img = self.theme.image_recolor(EMPTY_SQUARE, self.theme.foreground)
        self.theme.register_asset(str(empty_img), empty_img)

        # Image element and state specs
        el = ElementImage(f'{style}.border', border_img, sticky="nsew", border=8, width=261, height=128, padding=4)
        el.build()

        # header style
        self.theme.configure(
            f'{style}.Heading',
            background=header_bg_color,
            foreground=header_fg_color,
            relief="flat",
            rowheight=row_height,
            padding=8
        )

        # body style
        self.theme.configure(
            style,
            background=table_bg_color,
            foreground=table_fg_color,
            relief="flat",
            borderwidth=0,
            lightcolor=table_bg_color,
            darkcolor=table_bg_color,
            rowheight=row_height,
        )

        # create treeview indicator
        indicator = ElementImage(f'{style}.indicator', open_img, sticky="nsew")
        indicator.add_spec('user1 !user2', close_img)
        indicator.add_spec('user2', empty_img)
        indicator.build()

        spacer_img = PhotoImage(width=6, height=1)
        self.theme.register_asset(str(spacer_img), spacer_img)
        # Spacer element
        ElementImage(f'{style}.spacer', spacer_img, sticky="ew").build()


        Element('Treeview').layout([
            Element('Button.border', sticky="nsew"), [
                Element('Treeview.padding', sticky="nsew"), [
                    Element('Treeview.treearea', sticky="nsew")
                ]
            ]
        ])

        Element('Treeview.Item').layout([
            Element('Treeitem.padding'), [
                Element(f'{style}.indicator', side='left', sticky=""),
                Element(f'{style}.spacer', side='left', sticky=""),
                Element('Treeitem.image', side="left", sticky=""),
                Element('Treeitem.text', side="left", sticky="")
            ]
        ])

        self.theme.add_style(style)
        return style
