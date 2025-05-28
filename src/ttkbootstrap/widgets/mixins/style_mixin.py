from tkinter import Misc

from ttkbootstrap.style.theme_manager import get_theme_manager
from ttkbootstrap.ttk_types import StyleColor


class StyleMixin:

    widget: Misc

    def _initialize_style(
        self,
        widget_class: str,
        color: StyleColor = "default",
        variant: str = "default",
        **kwargs,
    ):
        self._widget_class = widget_class
        self._color = color
        self._variant = variant
        self._extras = kwargs.pop('extras', {})

        # check for a style override
        style_override = kwargs.pop("style", None)
        if style_override:
            # use custom style
            self.widget.configure(style=style_override)
            return
        else:
            # use themed style
            self._configure_widget_style()

        # observe theme changes and rebuild style
        self.widget.bind('<<ThemeChanged>>', lambda _: self._configure_widget_style(), add=True)

    def _configure_widget_style(self):
        self.widget.configure(style=self._build_style())

    def _build_style(self):
        manager = get_theme_manager()
        handler_name = f"ttk.{self._variant}.{self._widget_class}"
        return manager.active_theme.execute_handler(handler_name, self._color, **self._extras)

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value: StyleColor):
        self._color = value
        self._configure_widget_style()

    @property
    def variant(self):
        return self._variant

    @variant.setter
    def variant(self, value: str):
        self._variant = value
        self._configure_widget_style()
