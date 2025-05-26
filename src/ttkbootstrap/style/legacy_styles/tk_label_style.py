from __future__ import annotations

from typing import TYPE_CHECKING

from ttkbootstrap.style.style_builder import StyleBuilder

if TYPE_CHECKING:
    from tkinter import Label
    from ttkbootstrap.style.theme import Theme


class TkLabelStyle(StyleBuilder):

    def __init__(self, theme: Theme):
        super().__init__(theme)

    def invoke(self, widget: Label, *args, **kwargs) -> None:
        """Apply the label style."""
        widget.configure(foreground=self.theme.foreground, background=self.theme.background)
