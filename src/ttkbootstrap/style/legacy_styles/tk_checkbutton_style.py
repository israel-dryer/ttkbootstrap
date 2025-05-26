from __future__ import annotations

from typing import TYPE_CHECKING
from ttkbootstrap.style.style_builder import StyleBuilder

if TYPE_CHECKING:
    from tkinter import Checkbutton
    from ttkbootstrap.style.theme import Theme


class TkCheckbuttonStyle(StyleBuilder):

    def __init__(self, theme: Theme):
        super().__init__(theme)

    def invoke(self, widget: Checkbutton, *args, **kwargs) -> None:
        """Apply the checkbutton style."""
        widget.configure(
            activebackground=self.theme.background,
            activeforeground=self.theme.primary,
            background=self.theme.background,
            foreground=self.theme.foreground,
            selectcolor=self.theme.background,
        )
