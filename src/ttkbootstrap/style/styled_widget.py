from tkinter import Misc
from typing import Any

from ttkbootstrap.style.theme_manager import get_theme_manager
from ttkbootstrap.ttk_types import StyleColor
from ttkbootstrap.logger import Logger

logger = Logger(False, False)

def combine_style_keywords(color: str, variant: str) -> str:
    if variant and variant != "default":
        return f"{color} {variant}"
    return color


class StyledWidget(Misc):
    _color: StyleColor
    _variant: str
    _widget_class: str

    def _init_style(
        self,
        widget_class: str,
        color: StyleColor = "default",
        variant: str = "default",
        **kwargs
    ) -> None:
        logger.debug('StyledWidget', f'Initializing style for {widget_class} with {color} {variant} {kwargs}')
        self._widget_class = widget_class
        self._color = color
        self._variant = variant
        self._extras = kwargs.pop('extras', {})

        style_override = kwargs.pop("style", None)
        if style_override:
            self.configure(style=style_override)
            return
        else:
            ttk_style = self.build_style()
            self.configure(style=ttk_style)

        # observe <<ThemeChanged>> to update style
        self.bind("<<ThemeChanged>>", lambda _: self.configure(style=self.build_style()))

    def configure(self, cnf: str | None = None, **kwargs) -> Any:
        if cnf == "color":
            return self._color
        elif cnf == "variant":
            return self._variant
        elif cnf is not None:
            return super().configure(cnf)

        build_style = False
        if "color" in kwargs:
            self._color = kwargs.pop("color")
            build_style = True
        if "variant" in kwargs:
            self._variant = kwargs.pop("variant")
            build_style = True
        if "style" in kwargs:
            build_style = False
        if build_style:
            kwargs.update(style=self.build_style())

        return super().configure(**kwargs)

    def build_style(self) -> str:
        manager = get_theme_manager()
        handler_name = f"ttk.{self._variant}.{self._widget_class}"
        return manager.active_theme.execute_handler(handler_name, self._color, **self._extras)
