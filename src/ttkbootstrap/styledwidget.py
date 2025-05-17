from typing import Any
from ttkbootstrap import Bootstyle
from ttkbootstrap.utils.style_utils import combine_style_keywords


class StyledWidgetMixin:
    """
    Mixin for ttkbootstrap-compatible widgets that support `color` and `variant`.

    This mixin handles applying dynamic styles to themed ttk widgets
    based on semantic parameters like `color` (e.g., "primary") and
    `variant` (e.g., "outline", "round").

    Attributes:
        _color (str | None): The style color name.
        _variant (str | None): The style variant name.

    Example:
        Used in ttkbootstrap Button, Checkbutton, etc.
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
        Initialize and apply widget style.

        This should be called after the parent widget's `__init__` method.

        Args:
            kwargs (dict): Remaining keyword arguments from the constructor.
            color (str | None): A ttkbootstrap color name.
            variant (str): A ttkbootstrap variant name or an empty string.
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
        """
        Configure the widget.

        Special keys:
            color (str): Re-applies the theme color.
            variant (str): Re-applies the visual variant.

        Args:
            cnf (str | None): A single option to retrieve.
            **kwargs: Options to set on the widget.

        Returns:
            Any: The result of the configuration query or update.
        """
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
