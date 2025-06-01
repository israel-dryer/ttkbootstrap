from __future__ import annotations
from typing import TYPE_CHECKING

from tkinter import PhotoImage

from ...style_builder import StyleBuilder
from ...style_element import Element, ElementImage
from ....utils import load_asset_image

if TYPE_CHECKING:
    from ...theme import Theme


class TTkCheckButtonStyle(StyleBuilder):

    def __init__(self, theme: Theme):
        super().__init__(theme)

    def invoke(self, token: str, **extras):
        """Create the default checkbox style"""

        background, style = self.theme.get_background_style(token, 'TCheckbutton', **extras)

        # check if style already exists
        if self.theme.has_style(style):
            return style

        # color token
        token = "primary" if token == "default" else token
        colors = self.theme.get_color_states(token, "default", background)

        # checkbox colors
        border = self.theme.get_input_border_color()

        # base images for state images
        # base_checked_image = load_asset_image('checkbox-checked.png')
        # base_unchecked_image = load_asset_image('checkbox-unchecked.png')
        # base_disabled_image = load_asset_image('checkbox-disabled.png')
        # base_indeterminate_image = load_asset_image('checkbox-indeterminate.png')
        #
        # state images
        unchecked_img = self.theme.image_recolor_map(base_unchecked_image, container_bg, cb_border)
        self.theme.register_asset(str(unchecked_img), unchecked_img)

        checked_img = self.theme.image_recolor_map(base_checked_image, cb_indicator_fg, cb_indicator_bg)
        self.theme.register_asset(str(checked_img), checked_img)

        disabled_img = self.theme.image_recolor_map(base_disabled_image, container_bg, cb_border)
        self.theme.register_asset(str(disabled_img), disabled_img)

        indeterminate_img = self.theme.image_recolor_map(
            base_indeterminate_image, cb_indicator_fg, cb_indicator_bg)
        self.theme.register_asset(str(indeterminate_img), indeterminate_img)

        # add space between label and checkbox
        spacer_img = PhotoImage(width=6, height=1)
        self.theme.register_asset(str(spacer_img), spacer_img)

        # Spacer element
        ElementImage(f'{style}.spacer', spacer_img, sticky="ew").build()

        # Indicator element
        el = ElementImage(f'{style}.indicator', checked_img, sticky="ns", padding=3)
        el.add_spec('alternate', indeterminate_img)
        el.add_spec('disabled', disabled_img)
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

        self.theme.configure(
            style,
            foreground=cb_fg,
            background=container_bg,
            font="-size 12")
        self.theme.map(style, foreground=[('disabled', cb_disabled_bg)])

        self.theme.add_style(style)
        return style
