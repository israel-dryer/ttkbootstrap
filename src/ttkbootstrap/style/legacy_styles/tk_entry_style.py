from __future__ import annotations

from typing import TYPE_CHECKING

from ttkbootstrap.style.style_builder import StyleBuilder

if TYPE_CHECKING:
    from tkinter import Entry
    from ttkbootstrap.style.theme import Theme


class TkEntryStyle(StyleBuilder):

    def __init__(self, theme: Theme):
        super().__init__(theme)

    def invoke(self, widget: Entry, *args, **kwargs) -> None:
        """Apply the entry style."""
        shades = self.theme.get_shades('light')
        widget.configure(
            relief="flat",
            highlightthickness=1,
            foreground=self.theme.foreground,
            highlightbackground=shades.d1,
            highlightcolor=self.theme.primary,
            background=self.theme.background,
            borderwidth=1,
            insertbackground=self.theme.foreground,
            insertwidth=2,
        )
