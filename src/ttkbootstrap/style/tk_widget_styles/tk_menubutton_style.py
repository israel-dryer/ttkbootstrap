from __future__ import annotations

from typing import TYPE_CHECKING

from ttkbootstrap.style.style_builder import StyleBuilder

if TYPE_CHECKING:
    from tkinter import Menubutton
    from ttkbootstrap.style.theme import Theme


class TkMenubuttonStyle(StyleBuilder):

    def __init__(self, theme: Theme):
        super().__init__(theme)

    def invoke(self, widget: Menubutton, *args, **kwargs) -> None:
        """Apply the menubutton style."""
        shades = self.theme.get_shades('primary')
        widget.configure(
            background=self.theme.primary,
            foreground=self.theme.get_foreground('primary'),
            activebackground=shades.d1,
            activeforeground=self.theme.get_foreground('primary'),
            borderwidth=0,
        )
