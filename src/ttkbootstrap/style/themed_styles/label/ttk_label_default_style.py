from __future__ import annotations
from typing import TYPE_CHECKING

from ...style_builder import StyleBuilder

if TYPE_CHECKING:
    from ...theme import Theme


class TTkLabelDefaultStyle(StyleBuilder):

    def __init__(self, theme: Theme):
        super().__init__(theme)

    def invoke(self, token: str, **extras):
        """Create the default label style"""

        # check if the background color should be inherited from the parent
        parent_background = extras.get('background', None)
        container_bg = self.theme.background
        container_fg = self.theme.foreground
        if parent_background is not None and parent_background != container_bg:
            style = f'{parent_background}.{token}.TLabel'  # inherited background style
            container_bg = parent_background
            container_token = self.theme.get_token(container_bg or '')
            container_fg = container_fg if not container_token else self.theme.get_foreground(container_token)
        else:
            style = f'{token}.TLabel'

        # check if style already exists
        if self.theme.has_style(style):
            return style

        # color token
        token = "foreground" if token == "default" else token
        foreground = container_fg if parent_background is not None and token == "foreground" else self.theme.get_color(token)
        background = container_bg
        self.theme.configure(
            style,
            foreground=foreground,
            background=background,
            font="-size 12",
        )
        self.theme.add_style(style)
        return style
