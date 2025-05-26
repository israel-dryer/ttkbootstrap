from __future__ import annotations

from typing import TYPE_CHECKING
from ttkbootstrap.style.style_builder import StyleBuilder

if TYPE_CHECKING:
    from tkinter import Canvas
    from ttkbootstrap.style.theme import Theme


class TkCanvasStyle(StyleBuilder):

    def __init__(self, theme: Theme):
        super().__init__(theme)

    def invoke(self, widget: Canvas, *args, **kwargs) -> None:
        """Apply the canvas style."""
        widget.configure(background=self.theme.background, highlightthickness=0)
