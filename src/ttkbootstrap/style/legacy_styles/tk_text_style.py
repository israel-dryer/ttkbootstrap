from __future__ import annotations

from typing import TYPE_CHECKING

from ttkbootstrap.style.style_builder import StyleBuilder

if TYPE_CHECKING:
    from tkinter import Text
    from ttkbootstrap.style.theme import Theme


class TkTextStyle(StyleBuilder):

    def __init__(self, theme: Theme):
        super().__init__(theme)

    def invoke(self, widget: Text, *args, **kwargs) -> None:
        """Apply the text style."""
        shades = self.theme.get_shades('light')

        widget.configure(
            background=self.theme.background,
            foreground=self.theme.foreground,
            highlightcolor=self.theme.primary,
            highlightbackground=shades.d1,
            insertbackground=self.theme.foreground,
            selectbackground=self.theme.primary,
            selectforeground=self.theme.get_foreground('primary'),
            insertwidth=2,
            highlightthickness=1,
            relief="flat",
            padx=5,
            pady=5,
        )
