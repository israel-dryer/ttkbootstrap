from __future__ import annotations

from typing import TYPE_CHECKING
from ttkbootstrap.style.style_builder import StyleBuilder

if TYPE_CHECKING:
    from tkinter import Button
    from ttkbootstrap.style.theme import Theme


class TkButtonStyle(StyleBuilder):

    def __init__(self, theme: Theme):
        super().__init__(theme)

    def invoke(self, widget: Button, *args, **kwargs) -> None:
        """Apply the button style."""
        background = self.theme.primary
        foreground = self.theme.get_foreground("primary")
        shades = self.theme.get_shades("primary")
        active_background = shades.l2

        widget.configure(
            background=background,
            foreground=foreground,
            relief="flat",
            borderwidth=0,
            activeforeground=foreground,
            activebackground=active_background,
        )
