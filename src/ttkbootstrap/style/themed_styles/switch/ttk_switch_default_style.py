from __future__ import annotations
from typing import TYPE_CHECKING

from tkinter import PhotoImage

from ...style_builder import StyleBuilder
from ...style_element import Element, ElementImage
from ....utils import load_asset_image

if TYPE_CHECKING:
    from ...theme import Theme


class TTkSwitchDefaultStyle(StyleBuilder):

    def __init__(self, theme: Theme):
        super().__init__(theme)

    def invoke(self, token: str, **extras):
        """Create the default switch style"""

        # check if the background color should be inherited from the parent
        parent_background = extras.get('background', None)
        container_bg = self.theme.background
        container_fg = self.theme.foreground
        if parent_background is not None and parent_background != container_bg:
            style = f'{parent_background}.{token}.Switch'  # inherited background style
            container_bg = parent_background
            container_token = self.theme.get_token(container_bg or '')
            _fg = self.theme.get_foreground(container_token)
            container_fg = _fg if _fg else container_fg

        else:
            style = f'{token}.Switch'

        # check if style already exists
        if self.theme.has_style(style):
            return style

        # color token
        token = "primary" if token == "default" else token

        # button colors
        label_foreground = container_fg
        switch_indicator_bg = self.theme.get_color(token)
        switch_indicator_fg = self.theme.get_foreground(token)
        switch_border = self.theme.border
        switch_disabled_bg = switch_border

        # base images used for state
        base_checked_image = load_asset_image('switch-checked.png')
        base_unchecked_image = load_asset_image('switch-unchecked.png')
        base_disabled_image = load_asset_image('switch-disabled.png')

        # state images
        unchecked_img = self.theme.image_recolor_map(base_unchecked_image, container_bg, switch_border)
        self.theme.register_asset(str(unchecked_img), unchecked_img)

        checked_img = self.theme.image_recolor_map(base_checked_image, switch_indicator_fg, switch_indicator_bg)
        self.theme.register_asset(str(checked_img), checked_img)

        disabled_img = self.theme.image_recolor_map(base_disabled_image, switch_indicator_fg, switch_indicator_bg)
        self.theme.register_asset(str(disabled_img), disabled_img)

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

        self.theme.configure(style, foreground=label_foreground, background=container_bg, font="-size 12")
        self.theme.map(style, foreground=[('disabled', switch_disabled_bg)])

        self.theme.add_style(style)
        return style
