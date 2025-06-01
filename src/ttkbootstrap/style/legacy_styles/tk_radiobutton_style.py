from __future__ import annotations

from typing import TYPE_CHECKING

from ttkbootstrap.style.style_builder_legacy import StyleBuilderLegacy

if TYPE_CHECKING:
    from tkinter import Radiobutton
    from ttkbootstrap.style.theme import Theme


class TkRadiobuttonStyle(StyleBuilderLegacy):

    def __init__(self, theme: Theme):
        super().__init__(theme)

    def invoke(self, widget: Radiobutton, *args, **kwargs) -> None:
        """Apply the radiobutton style."""
        widget.configure(
            activebackground=self.theme.background,
            activeforeground=self.theme.primary,
            background=self.theme.background,
            foreground=self.theme.foreground,
            selectcolor=self.theme.background,
        )
