from __future__ import annotations

from typing import TYPE_CHECKING

from ttkbootstrap.style.style_builder import StyleBuilder

if TYPE_CHECKING:
    from tkinter import Scale


class TkScaleStyle(StyleBuilder):

    def __init__(self, builder: StyleBuilder):
        super().__init__(builder)

    def invoke(self, widget: Scale, *args, **kwargs) -> None:
        """Apply the scale style."""
        if self.theme.is_dark_theme:
            shades = self.theme.get_shades('dark')
        else:
            shades = self.theme.get_shades('light')
        shades_active = self.theme.get_shades('primary')
        active_color = shades_active.l2
        widget.configure(
            background=self.theme.primary,
            showvalue=False,
            sliderrelief="flat",
            borderwidth=0,
            activebackground=active_color,
            highlightthickness=1,
            highlightcolor=shades.d1,
            highlightbackground=shades.l1,
            troughcolor=shades.d1,
        )
