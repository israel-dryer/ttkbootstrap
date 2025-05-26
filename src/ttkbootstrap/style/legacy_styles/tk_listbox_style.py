from __future__ import annotations

from typing import TYPE_CHECKING

from ttkbootstrap.style.style_builder import StyleBuilder

if TYPE_CHECKING:
    from tkinter import Listbox
    from ttkbootstrap.style.theme import Theme


class TkListboxStyle(StyleBuilder):

    def __init__(self, theme: Theme):
        super().__init__(theme)

    def invoke(self, widget: Listbox, *args, **kwargs) -> None:
        """Apply the listbox style."""
        shades = self.theme.get_shades('light')

        widget.configure(
            foreground=self.theme.foreground,
            background=self.theme.background,
            selectbackground=self.theme.primary,
            selectforeground=self.theme.get_foreground('primary'),
            highlightcolor=self.theme.primary,
            highlightbackground=shades.d1,
            highlightthickness=0,
            bd=0,
            activestyle="none",
            relief="flat",
            borderwidth=1,
            font='-size 12'
        )
