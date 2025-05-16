from tkinter import Misc
from ttkbootstrap.widgets.checkbutton import Checkbutton
from ttkbootstrap.ttk_types import StyleColor as Color, CheckbuttonOptions as CbOpts, ToolbuttonVariant

try:
    from typing import Unpack, Literal
except ImportError:
    from typing_extensions import Unpack, Literal


class ToolCheckbutton(Checkbutton):
    """
    A themed toolbar checkbutton that functions as a toggleable tool button.

    This widget behaves like a standard `Checkbutton` but is styled to match
    the appearance of a compact toolbar button. It supports both `color` and
    `variant` parameters for visual customization, making it ideal for toggling
    formatting options, view modes, or feature states in a toolbar layout.

    Example:
        ToolCheckbutton(root, text="Bold", color="primary", variant="outline")

    Parameters:
        master (Misc | None): The parent container widget.
        color (Color): The button color theme (e.g., "primary", "info").
        variant (str): The visual style variant (e.g., "outline", "solid").
        **kwargs (CheckbuttonOpts): Additional options accepted by `ttk.Checkbutton`.
    """


    def __init__(
        self,
        master: Misc | None = None,
        color: Color = None,
        variant: ToolbuttonVariant = "default",
        **kwargs: Unpack[CbOpts],
    ):
        """
        Initialize a ToolCheckbutton.

        Parameters:
            master (Misc | None): The parent container.
            color (Color, optional): A ttkbootstrap color token.
            variant (ToolbuttonVariant): "default" or "outline".
            **kwargs (CbOpts): Additional standard ttk.Checkbutton options.
        """
        self._color = color
        self._variant = variant

        variant += "-toolbutton"

        super().__init__(master, **kwargs)
        self._init_style(kwargs, color=color, variant=variant)
