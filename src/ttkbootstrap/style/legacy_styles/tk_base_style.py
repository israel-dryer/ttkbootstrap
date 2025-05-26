from __future__ import annotations

from typing import TYPE_CHECKING
from ..style_builder import StyleBuilder

if TYPE_CHECKING:
    from ..theme import Theme
    from tkinter import Tk


class TkBaseStyle(StyleBuilder):

    def __init__(self, theme: Theme):
        super().__init__(theme)

    def invoke(self, widget: Tk, *args, **kwargs) -> None:
        """Apply the base application style."""
        widget.configure(background=self.theme.background)
        # add default initial font for text widget
        widget.option_add('*Text*Font', 'TkDefaultFont')
