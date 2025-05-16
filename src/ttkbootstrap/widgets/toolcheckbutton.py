from tkinter import Misc
from ttkbootstrap.widgets.checkbutton import Checkbutton
from ttkbootstrap.typing import StyleColor as Color, CheckbuttonOptions as CbOpts, ToolbuttonVariant

try:
    from typing import Unpack, Literal
except ImportError:
    from typing_extensions import Unpack, Literal


class ToolCheckbutton(Checkbutton):
    """
    A styled toggleable toolbar button that behaves like a checkbutton.
    Supports `color` and `variant` styling.

    Example:
        ToolCheckbutton(root, text="Bold", color="primary", variant="outline")
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
