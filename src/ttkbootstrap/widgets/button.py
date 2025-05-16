from tkinter import Misc
from tkinter.ttk import Button as ttkButton

from ttkbootstrap.ttk_types import (
    StyleColor,
    ButtonStyleVariant as Variant,
    ButtonOptions as BtnOpts,
)
from ttkbootstrap.styledwidget import StyledWidgetMixin

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack


class Button(StyledWidgetMixin, ttkButton):
    """
    A themed button widget with support for dynamic color and variant styling.

    This widget extends the standard `ttk.Button` by applying styles generated
    from the `color` and `variant` parameters using the themed styling system.
    These parameters determine the appearance of the button, such as its color
    scheme and whether it is filled, outlined, or has other visual variants.

    This button behaves exactly like a standard `ttk.Button`, with all the same
    interactive features, but allows for consistent theming across an application.

    Example:
        Button(root, text="Submit", color="primary", variant="outline")

    Parameters:
        master (Misc, optional): The parent container widget.
        color (StyleColor, optional): The color theme (e.g., "primary", "success").
        variant (Variant): The button's visual variant (e.g., "default", "outline").
        **kwargs (BtnOpts): Additional standard options accepted by `ttk.Button`.
    """

    def __init__(
        self,
        master: Misc = None,
        color: StyleColor = None,
        variant: Variant = "default",
        **kwargs: Unpack[BtnOpts],
    ):
        """
        Initialize a themed Button.

        Parameters:
            master (Misc, optional): The parent container.
            color (Color, optional): A ttkbootstrap color token (e.g., "primary").
            variant (Variant): The visual style variant (e.g., "default", "outline").
            **kwargs (BtnOpts): Additional standard ttk.Button options.
        """
        self._color = color
        self._variant = variant
        super().__init__(master, **kwargs)
        self._init_style(kwargs, color=color, variant=variant)
