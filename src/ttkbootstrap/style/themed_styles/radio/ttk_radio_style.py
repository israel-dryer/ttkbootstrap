from __future__ import annotations
from typing import TYPE_CHECKING

from tkinter import PhotoImage

from ...style_builder import StyleBuilder
from ...style_element import Element, ElementImage
from ....utils import load_asset_image

if TYPE_CHECKING:
    from ...theme import Theme


class TTkRadioStyle(StyleBuilder):

    def __init__(self, theme: Theme):
        super().__init__(theme)

    def invoke(self, token: str, **extras):
        """Create the default radio style"""

        # check if the background color should be inherited from the parent
        parent_background = extras.get('background', None)
        container_bg = self.theme.background
        container_fg = self.theme.foreground
        if parent_background is not None and parent_background != container_bg:
            style = f'{parent_background}.{token}.TRadiobutton'  # inherited background style
            container_bg = parent_background
            container_token = self.theme.get_token(container_bg or '')
            container_fg = container_fg if not container_token else self.theme.get_foreground(container_token)
        else:
            style = f'{token}.TRadiobutton'

        if self.theme.has_style(style):
            return style

        # color token
        token = "primary" if token == "default" else token

        # radio colors
        label_fg = container_fg
        rb_indicator_bg = self.theme.get_color(token)
        rg_indicator_fg = self.theme.get_foreground(token)
        rb_disabled_bg = rb_indicator_bg
        rb_border = self.theme.border

        # base images for state images
        base_unselected_image = load_asset_image('radio-unselected.png')
        base_selected_image = load_asset_image('radio-selected.png')
        base_disabled_image = load_asset_image('radio-disabled.png')

        # state images
        unselected_img = self.theme.image_recolor_map(base_unselected_image, container_bg, rb_border)
        self.theme.register_asset(str(unselected_img), unselected_img)

        selected_img = self.theme.image_recolor_map(base_selected_image, rg_indicator_fg, rb_indicator_bg)
        self.theme.register_asset(str(selected_img), selected_img)

        disabled_img = self.theme.image_recolor_map(base_disabled_image, container_bg, rb_disabled_bg)
        self.theme.register_asset(str(disabled_img), disabled_img)

        spacer_img = PhotoImage(width=6, height=1)
        self.theme.register_asset(str(spacer_img), spacer_img)

        # Spacer element
        ElementImage(f'{style}.spacer', spacer_img, sticky="ew").build()

        # Indicator element
        el = ElementImage(f'{style}.indicator', selected_img, sticky="ns", padding=3)
        el.add_spec('disabled', disabled_img)
        el.add_spec('!selected', unselected_img)
        el.build()

        # Layout and style config
        Element(style).layout(
            [
                Element('Radiobutton.padding', sticky="nsew"), [
                Element(f'{style}.indicator', side="left", sticky=''),
                Element(f"{style}.spacer", side="left", ),
                Element('Radiobutton.label', side="left", expand=1)]
            ])

        self.theme.configure(style, foreground=label_fg, background=container_bg, font="-size 12")
        self.theme.map(style, foreground=[('disabled', rb_disabled_bg)])

        self.theme.add_style(style)
        return style
