from __future__ import annotations

from typing import TYPE_CHECKING

from ttkbootstrap.style.style_builder import StyleBuilder

if TYPE_CHECKING:
    from tkinter import Menu
    from ttkbootstrap.style.theme import Theme


class TkMenuStyle(StyleBuilder):

    def __init__(self, theme: Theme):
        super().__init__(theme)

    def invoke(self, widget: Menu, *args, **kwargs) -> None:
        """Apply the menu style."""
        widget.configure(
            tearoff=False,
            activebackground=self.theme.primary,
            activeforeground=self.theme.get_foreground("primary"),
            foreground=self.theme.foreground,
            selectcolor=self.theme.primary,
            background=self.theme.background,
            relief="flat",
            borderwidth=0,
        )
