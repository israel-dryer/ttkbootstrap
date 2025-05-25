from __future__ import annotations

from typing import TYPE_CHECKING

from ttkbootstrap.style.style_builder import StyleBuilder

if TYPE_CHECKING:
    from tkinter import LabelFrame
    from ttkbootstrap.style.theme import Theme


class TkLabelFrameStyle(StyleBuilder):

    def __init__(self, theme: Theme):
        super().__init__(theme)

    def invoke(self, widget: LabelFrame, *args, **kwargs) -> None:
        """Apply the labelframe style."""
        shades = self.theme.get_shades('light')

        widget.configure(
            highlightcolor=shades.base,
            foreground=self.theme.foreground,
            borderwidth=1,
            highlightthickness=0,
            background=self.theme.background,
        )
