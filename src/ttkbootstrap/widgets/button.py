from tkinter import Misc
from tkinter.ttk import Button as ttkButton

from ttkbootstrap.typing import (
    StyleColor as Color,
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
    A themed ttkbootstrap-compatible Button that supports `color` and `variant`
    parameters for dynamic style generation.

    This widget wraps tkinter.ttk.Button and uses ttkbootstrap's styling system
    to apply styles based on the provided `color` and `variant`.

    Example:
        Button(root, text="Save", color="primary", variant="outline")
    """

    def __init__(
        self,
        master: Misc = None,
        color: Color = None,
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
