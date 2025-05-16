from tkinter import Misc
from typing import Literal

from .checkbutton import Checkbutton
from ttkbootstrap.typing import StyleColor as Color, CheckbuttonOptions as CbOpts

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack

SwitchVariant = Literal["round", "square"]


class Switch(Checkbutton):
    """
    A styled switch widget that behaves like a toggle control.

    Inherits from the ttkbootstrap Checkbutton and accepts a `color` and
    a `variant` to control its visual style. Commonly used in settings panels.

    Supported variants:
        - "round": renders a pill-style toggle
        - "square": renders a rectangular toggle
    """

    def __init__(
        self,
        master: Misc = None,
        color: Color = None,
        variant: SwitchVariant = "round",
        **kwargs: Unpack[CbOpts],
    ):
        """
        Initialize a styled Switch.

        Parameters:
            master (Misc, optional): The parent container.
            color (Color, optional): A ttkbootstrap color token (e.g., "success").
            variant (SwitchVariant): The switch shape: "round" or "square".
            **kwargs (CbOpts): Additional standard ttk.Checkbutton options.
        """
        self._color = color
        self._variant = variant

        variant += "-toggle"

        super().__init__(master, **kwargs)
        self._init_style(kwargs, color=color, variant=variant)
