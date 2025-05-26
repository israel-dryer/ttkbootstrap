from __future__ import annotations

from typing import TYPE_CHECKING

from ttkbootstrap.style.style_builder import StyleBuilder

if TYPE_CHECKING:
    from tkinter import Frame
    from ttkbootstrap.style.theme import Theme


class TkFrameStyle(StyleBuilder):

    def __init__(self, theme: Theme):
        super().__init__(theme)

    def invoke(self, widget: Frame, *args, **kwargs) -> None:
        """Apply the frame style."""
        widget.configure(background=self.theme.background)
