from tkinter import Misc
from typing import Literal

from .checkbutton import Checkbutton
from ttkbootstrap.typing import StyleColor as Color, CheckbuttonOptions as CbOpts

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack

ToolbuttonVariant = Literal["default", "outline"]


class Toolbutton(Checkbutton):
    """
    A toggleable toolbar-style button that behaves like a checkable button.

    This widget extends ttkbootstrap's Checkbutton and provides styling support
    via `color` and `variant`.

    Supported variants:
        - "default": flat button with background fill
        - "outline": minimal button with border and hover effect
    """

    def __init__(
        self,
        master: Misc = None,
        color: Color = None,
        variant: ToolbuttonVariant = "default",
        **kwargs: Unpack[CbOpts],
    ):
        """
        Initialize a styled Toolbutton.

        Parameters:
            master (Misc, optional): The parent container.
            color (Color, optional): A ttkbootstrap color token (e.g., "secondary").
            variant (ToolbuttonVariant): Either "default" or "outline".
            **kwargs (CbOpts): Additional standard ttk.Checkbutton options.
        """
        self._color = color
        self._variant = variant

        variant += "-toolbutton"

        super().__init__(master, **kwargs)
        self._init_style(kwargs, color=color, variant=variant)
