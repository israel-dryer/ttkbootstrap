from tkinter.ttk import Button as ttkButton
from typing import Any

from ttkbootstrap import Bootstyle
from ttkbootstrap.utils.style_utils import combine_style_keywords
from ttkbootstrap.typing import (
    StyleColor as Color,
    ButtonStyleVariant as Variant,
    ButtonOptions as BtnOpts,
)

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack


class Button(ttkButton):
    """
    A styled ttkbootstrap-compatible Button that supports `color` and `variant`
    for automatic style generation without using `bootstyle`.

    This widget wraps the standard tkinter.ttk.Button and allows you to specify:
    - `color`: A ttkbootstrap style color token (e.g. "primary", "success").
    - `variant`: A ttkbootstrap style variant (e.g. "outline", "link").

    If a `style` is not explicitly provided, the widget will automatically
    generate and apply one using the given `color` and `variant`.
    """

    def __init__(
        self,
        master: Any = None,
        color: Color = None,
        variant: Variant = "default",
        **kwargs: Unpack[BtnOpts],
    ):
        """
        Initialize a styled Button.

        Parameters:
            master (Widget, optional): The parent widget.
            color (Color, optional): A ttkbootstrap color token.
            variant (Variant, optional): A ttkbootstrap style variant (default: "default").
            **kwargs (BtnOpts): Additional standard ttk.Button options.
        """
        self._color = color
        self._variant = variant

        style_override = kwargs.pop("style", None)

        super().__init__(master, **kwargs)

        if style_override:
            self.configure(style=style_override)
        else:
            keywords = combine_style_keywords(self._color, self._variant)
            ttk_style = Bootstyle.update_ttk_widget_style(self, keywords, **kwargs)
            self.configure(style=ttk_style)

    def configure(self, cnf: str | None = None, **kwargs) -> Any:
        """
        Get or set configuration options.

        Special options:
            - color: Update the bootstyle color.
            - variant: Update the bootstyle variant.
            - style: Override with a custom ttk style name.

        Parameters:
            cnf (str | None): Option name to retrieve, or None to set values.
            **kwargs: Options to update the widget configuration.

        Returns:
            Any: Value of the queried configuration, or updated config result.
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
            style = kwargs.get("style")
            ttk_style = Bootstyle.update_ttk_widget_style(self, style, **kwargs)
            kwargs.update(style=ttk_style)
            build_style = False

        if build_style:
            keywords = combine_style_keywords(self._color, self._variant)
            ttk_style = Bootstyle.update_ttk_widget_style(self, keywords, **kwargs)
            kwargs.update(style=ttk_style)

        return super().configure(**kwargs)
