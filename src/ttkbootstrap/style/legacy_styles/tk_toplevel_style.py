from __future__ import annotations

from typing import TYPE_CHECKING

from ttkbootstrap.style.style_builder_legacy import StyleBuilderLegacy

if TYPE_CHECKING:
    from tkinter import Toplevel
    from ttkbootstrap.style.theme import Theme


class TkToplevelStyle(StyleBuilderLegacy):

    def __init__(self, theme: Theme):
        super().__init__(theme)

    def invoke(self, widget: Toplevel, *args, **kwargs) -> None:
        """Apply the toplevel style."""
        widget.configure(background=self.theme.background)
