from typing import Any
from ttkbootstrap import Bootstyle
from ttkbootstrap.utils.style_utils import combine_style_keywords


class StyledWidgetMixin:
    """
    Mixin for ttkbootstrap-compatible widgets that support `color` and `variant`.
    Styles are applied synchronously after widget initialization.
    """

    _color: str | None
    _variant: str | None

    def _init_style(
        self,
        kwargs: dict,
        color: str | None = None,
        variant: str = "default"
    ) -> None:
        """
        Apply style immediately after widget initialization.

        This must be called after `super().__init__()`.

        Parameters:
            kwargs (dict): Remaining ttk-compatible kwargs.
            color (str | None): The ttkbootstrap color name.
            variant (str): The ttkbootstrap variant (or "" if none).
        """
        self._color = color
        self._variant = variant

        style_override = kwargs.pop("style", None)

        if style_override:
            style = Bootstyle.update_ttk_widget_style(self, style_override, **kwargs)
        else:
            style_key = combine_style_keywords(self._color, self._variant)
            style = Bootstyle.update_ttk_widget_style(self, style_key, **kwargs)
        self.configure(style=style)

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
            style = kwargs.pop("style")
            ttk_style = Bootstyle.update_ttk_widget_style(self, style, **kwargs)
            kwargs.update(style=ttk_style)
            build_style = False

        if build_style:
            style_key = combine_style_keywords(self._color, self._variant)
            ttk_style = Bootstyle.update_ttk_widget_style(self, style_key, **kwargs)
            kwargs.update(style=ttk_style)

        return super().configure(**kwargs)
